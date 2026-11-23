import ast
import builtins
import copy
import difflib
import inspect
import io
import json
import random
import re
import sys
import tokenize
import traceback

import rt_js

FILENAME = "<your code>"
LOOP_LIMIT = 200000


class LoopLimit(Exception):
    pass


class NeedInput(Exception):
    pass


class CheckFail(Exception):
    pass


# queue: None = ask the real person; a list = scripted answers (used by Check)
# hits: None = not tracking paths; a set = keys of the if/elif/else paths that ran
_state = {"count": 0, "queue": None, "used": 0, "hits": None}


def _rt_guard():
    _state["count"] += 1
    if _state["count"] > LOOP_LIMIT:
        raise LoopLimit()


def _rt_hit(key):
    if _state["hits"] is not None:
        _state["hits"].add(key)


async def _rt_input(prompt=""):
    sys.stdout.write(str(prompt))
    q = _state["queue"]
    if q is not None:
        if not q:
            raise NeedInput()
        value = q.pop(0)
        _state["used"] += 1
        sys.stdout.write(value + "\n")
        return value
    sys.stdout.flush()
    value = await rt_js.get_input()
    return str(value)


def _calls_any(node, names):
    for sub in ast.walk(node):
        if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id in names:
            return True
    return False


def _async_names(tree):
    # input() becomes awaitable, so any function that (directly or indirectly) calls it must be async too
    names = {"input"}
    funcs = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
    changed = True
    while changed:
        changed = False
        for f in funcs:
            if f.name not in names and _calls_any(f, names):
                names.add(f.name)
                changed = True
    return names


# ---------------- paths (branch coverage) ----------------

def _branches(tree, lines):
    """Find every if / elif / else path. Returns {(lineno, kind): info} plus a display list."""
    found = []

    def text(n):
        return lines[n - 1].strip() if 0 < n <= len(lines) else ""

    for node in ast.walk(tree):
        if not isinstance(node, ast.If):
            continue
        kind = "elif" if text(node.lineno).startswith("elif") else "if"
        found.append((node.lineno, kind, node))
        orelse = node.orelse
        is_elif = (len(orelse) == 1 and isinstance(orelse[0], ast.If)
                   and text(orelse[0].lineno).startswith("elif"))
        if orelse and not is_elif:
            ln = orelse[0].lineno - 1
            while ln > node.lineno and not text(ln).startswith("else"):
                ln -= 1
            found.append((ln, "else", node))
    found.sort(key=lambda x: (x[0], x[1] == "else"))
    seen, table, shown = {}, {}, []
    for ln, kind, node in found:
        label = text(ln)
        if kind == "else":
            label = "else  (after: " + text(node.lineno)[:40] + ")"
        base = text(ln) + ("|else|" + text(node.lineno) if kind == "else" else "")
        seen[base] = seen.get(base, 0) + 1
        key = base + "#" + str(seen[base])
        table[(id(node), kind)] = key
        shown.append({"key": key, "line": ln, "label": label[:70]})
    return table, shown


class _Transform(ast.NodeTransformer):
    def __init__(self, names, paths=None):
        self.names = names
        self.paths = paths

    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Name) and node.func.id in self.names:
            if node.func.id == "input":
                node.func = ast.copy_location(ast.Name("_rt_input", ast.Load()), node.func)
            return ast.copy_location(ast.Await(node), node)
        return node

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        if node.name in self.names:
            new = ast.AsyncFunctionDef(**{f: getattr(node, f) for f in node._fields})
            return ast.copy_location(new, node)
        return node

    def _hit(self, key, where):
        call = ast.Expr(ast.Call(ast.Name("_rt_hit", ast.Load()), [ast.Constant(key)], []))
        return ast.copy_location(call, where)

    def visit_If(self, node):
        keys = {}
        if self.paths is not None:
            for kind in ("if", "elif", "else"):
                if (id(node), kind) in self.paths:
                    keys[kind] = self.paths[(id(node), kind)]
        self.generic_visit(node)
        own = keys.get("if") or keys.get("elif")
        if own:
            node.body.insert(0, self._hit(own, node.body[0]))
        if keys.get("else") and node.orelse:
            node.orelse.insert(0, self._hit(keys["else"], node.orelse[0]))
        return node

    def _guard_loop(self, node):
        self.generic_visit(node)
        guard = ast.Expr(ast.Call(ast.Name("_rt_guard", ast.Load()), [], []))
        ast.copy_location(guard, node.body[0])
        node.body.insert(0, guard)
        return node

    visit_While = _guard_loop
    visit_For = _guard_loop


# ---------------- friendly error hints ----------------

ERL_LINES = [
    (r"\bthen\s*:?\s*$", "Python doesn't use then. End the line with a colon instead, like: if health > 0:"),
    (r"^\s*(endif|endwhile|endfor|endfunction|endprocedure|endswitch)\b",
     "Python doesn't need {0}. The indentation shows where a block ends, so delete this line."),
    (r"^\s*next\s+\w+\s*$", "Python doesn't need next. The indentation shows where the loop ends, so delete this line."),
    (r"^\s*(elseif|else\s+if)\b", "In Python it's elif, like: elif health > 50:"),
    (r"^\s*for\s+\w+\s*=.*\bto\b", "That's how exam papers write a loop. In Python it's: for i in range(1, 11):  (range stops before the last number)."),
    (r"^\s*(procedure|function)\s+\w+", "In Python, procedures and functions both start with def, like: def show_bag(inventory):"),
    (r"^\s*(do|until)\b", "Python doesn't have do ... until. Use a while loop instead."),
    (r"\b(AND|OR|NOT)\b", "In Python, and, or and not are written in lower case."),
]


def _erl_hint(line_text):
    if not line_text:
        return ""
    for pat, msg in ERL_LINES:
        m = re.search(pat, line_text)
        if m:
            return msg.format(m.group(1) if m.groups() else "")
    return ""


COMMON_BUILTINS = {"print", "input", "int", "str", "float", "len", "range", "round", "abs", "min", "max",
                   "sum", "sorted", "list", "bool", "type", "ord", "chr", "True", "False", "None"}


def _did_you_mean(bad, names):
    builtin_names = set(dir(builtins))
    cands = sorted({n for n in names if not n.startswith("_") and n != bad
                    and (n not in builtin_names or n in COMMON_BUILTINS)})
    for c in cands:
        if c.lower() == bad.lower():
            return c
    close = difflib.get_close_matches(bad, cands, n=1, cutoff=0.8)
    return close[0] if close else ""


def _hint(e):
    kind = type(e).__name__
    msg = str(e)
    low = (getattr(e, "msg", "") or msg).lower()
    if kind in ("IndentationError", "TabError"):
        return ("Check the spaces at the start of this line. Lines inside an if, while or for "
                "need 4 spaces, and the lines after it need to line up again.")
    if kind == "SyntaxError":
        if "'await'" in low:
            return ("This page's runner can't use input() in this exact spot. "
                    "Try moving the input() onto its own line.")
        if "invalid character" in low:
            if any(c in low for c in "\u201c\u201d\u2018\u2019"):
                return ("This line has curly quotes, which sneak in when code is copied from a document. "
                        "Delete them and type the quote marks again, straight from the keyboard.")
            return ("This line has a special character Python can't read, often from copying out of a "
                    "document. Delete the odd symbol and type it again from the keyboard.")
        if "expected ':'" in low:
            return "You might be missing a colon : at the end of this line."
        if "maybe you meant '=='" in low:
            return "To compare two things, use == (two equals signs). One = stores a value."
        if "unterminated string" in low or "eol while" in low:
            return "A quote mark is missing. Text needs a quote at the start AND at the end."
        if "never closed" in low or "unmatched" in low or "does not match" in low:
            return "Your brackets don't match up. Every ( needs a ). The mistake may be on the line above."
        return ("Python can't understand this line. Check your brackets, quote marks and colons. "
                "Sometimes the real mistake is on the line above.")
    if kind == "NameError":
        bad = msg.split("'")[1] if msg.count("'") >= 2 else "this name"
        if bad == "random":
            return "Python doesn't know what random is yet. Put import random on the very first line of your program."
        return (f"Python doesn't know what {bad} is. Check the spelling and capital letters "
                "(print, not Print). If it's a variable, give it a value first. "
                "If it's meant to be text, put it in quotes.")
    if kind == "TypeError":
        if "positional argument" in msg:
            return ("The number of values in the call doesn't match the def. Count the values in the "
                    "brackets where you call it, and the parameters in the brackets of the def.")
        if "NoneType" in msg and "subscriptable" in msg:
            return ("This value is None, which usually means a function gave nothing back. "
                    "Check the function ends with a return line, like: return hero")
        if "'set' object is not subscriptable" in msg:
            return ("Your curly brackets hold values but no keys. Give each value a key and a colon, "
                    "like: {\"name\": \"goblin\", \"health\": 30}")
        if "indices must be integers or slices, not str" in msg:
            return ("You're asking a list for something by name. Lists only use positions (0, 1, 2). "
                    "To look things up by name, make a dictionary with curly brackets { }.")
        if "NoneType" in msg:
            return ("One of these values is None, which means a subroutine gave nothing back. A subroutine "
                    "that prints its answer doesn't return it: add return, like: return width * height")
        if "not supported between instances of 'str' and 'int'" in msg or \
           "not supported between instances of 'int' and 'str'" in msg:
            return "You're comparing text with a number. Did you forget int() around input()?"
        if "concatenate str" in msg or ("unsupported operand" in msg and "str" in msg) or "can't multiply" in msg:
            return ("You're mixing text and numbers. Use int() to turn typed text into a number. "
                    "To show a number with text, use a comma in print instead of +.")
        return "Something is the wrong type here, for example text where a number should be."
    if kind == "AttributeError" and "NoneType" in msg:
        return ("Your list has turned into None. Check for list = list.append(...) (just write "
                "list.append(...)), or a function that forgot to return the list.")
    if kind == "AttributeError" and "random" in msg:
        return "Check the spelling after random. It's random.randint or random.choice."
    if kind == "ValueError" and "x not in list" in msg:
        return "You tried to remove something that isn't in the list. Check with in before you remove it."
    if kind == "ValueError" and "empty range" in msg:
        return "random.randint needs the smaller number first, e.g. random.randint(1, 6)."
    if kind == "ValueError" and "invalid literal for int()" in msg:
        return "int() can only turn whole numbers into numbers. What was typed in wasn't a whole number."
    if kind == "KeyError":
        return (f"Python couldn't find the key {msg} in your dictionary. Check its spelling and capital "
                "letters match exactly, and that the key is in quote marks.")
    if kind == "ZeroDivisionError":
        return "You can't divide by zero. Check the number you're dividing by."
    if kind == "IndexError":
        return "You asked for a position that doesn't exist. Remember positions start at 0."
    return ""



def _error_line(e):
    if isinstance(e, SyntaxError):
        return e.lineno
    frames = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == FILENAME]
    return frames[-1].lineno if frames else None


def _known_names(e, ns):
    names = set(ns or {}) | set(dir(builtins))
    tb = e.__traceback__
    while tb is not None:
        if tb.tb_frame.f_code.co_filename == FILENAME:
            names |= set(tb.tb_frame.f_locals) | set(tb.tb_frame.f_globals)
        tb = tb.tb_next
    return names


def _indent_hint(e, line, lines, text):
    """Plain-English, line-specific help for indentation mistakes."""
    kind = type(e).__name__
    low = (getattr(e, "msg", "") or str(e)).lower()
    if kind in ("IndentationError", "TabError"):
        m = re.search(r"expected an indented block after (.+?) on line (\d+)", low)
        if m:
            what = m.group(1).replace("'", "").replace(" statement", "").replace("function definition", "def")
            return (f"Line {m.group(2)} ends with a colon, so the line after it must be indented one step. "
                    f"Click at the start of line {line} and press Tab. Everything that belongs to the {what} "
                    "goes in that indented block.")
        if "unexpected indent" in low:
            return (f"Line {line} is indented, but the line above doesn't end with a colon, so nothing has "
                    "started a block. Press Shift+Tab to line it up with the line above. (Or is a colon "
                    "missing from the line above?)")
        if "unindent does not match" in low or "inconsistent" in low:
            return (f"Line {line} doesn't line up with any line above it. Indents come in steps of 4 spaces: "
                    "press Shift+Tab until it lines up exactly with the lines it belongs with.")
        if kind == "TabError":
            return "This line mixes tabs and spaces. Delete the gap at the start and press Tab again."
    if kind == "SyntaxError":
        stripped = text.strip()
        if re.match(r"(elif|else)\b", stripped) and text != stripped:
            word = stripped.split()[0].rstrip(":")
            return (f"{word} must line up exactly with the if it belongs to. Press Shift+Tab until this "
                    "line starts in the same place as its if.")
        if "'return' outside function" in low:
            return (f"return only works inside a def. Press Tab at the start of line {line} so it lines up "
                    "with the other lines of the subroutine above.")
    return ""


def _full_hint(e, line, lines, ns=None):
    kind = type(e).__name__
    text = lines[line - 1] if line and 0 < line <= len(lines) else ""
    ind = _indent_hint(e, line, lines, text)
    if ind:
        return ind
    if kind in ("SyntaxError", "NameError", "IndentationError"):
        erl = _erl_hint(text)
        if erl:
            return erl
    hint = _hint(e)
    if kind == "NameError":
        msg = str(e)
        bad = msg.split("'")[1] if msg.count("'") >= 2 else ""
        guess = _did_you_mean(bad, _known_names(e, ns)) if bad and bad != "random" else ""
        if guess:
            hint = f"Did you mean {guess}? " + hint
    return hint


def _report(e, line, lines=(), ns=None):
    return {
        "type": "error",
        "line": line,
        "error": f"{type(e).__name__}: {getattr(e, 'msg', None) or e}",
        "hint": _full_hint(e, line, lines, ns),
    }


def _compile(src, cover=False, defs_only=False):
    """Returns (code, paths_display) or raises SyntaxError."""
    tree = ast.parse(src, FILENAME)
    if defs_only:
        keep = []
        known = set(dir(builtins))
        for n in tree.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                keep.append(n)
                known.add(n.name)
            elif isinstance(n, (ast.Import, ast.ImportFrom)):
                keep.append(n)
                known.update((a.asname or a.name).split(".")[0] for a in n.names)
            elif isinstance(n, (ast.Assign, ast.AnnAssign)) and not any(isinstance(s, ast.Call) for s in ast.walk(n)):
                # skip constants built from names that only exist once the main program runs
                if n.value is not None and any(isinstance(s, ast.Name) and s.id not in known for s in ast.walk(n.value)):
                    continue
                keep.append(n)
                for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
                    known.update(x.id for x in ast.walk(t) if isinstance(x, ast.Name))
        tree.body = keep
    shown = None
    table = None
    if cover:
        table, shown = _branches(tree, src.split("\n"))
    tree = _Transform(_async_names(tree), table).visit(tree)
    ast.fix_missing_locations(tree)
    code = compile(tree, FILENAME, "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
    return code, shown


def _compile_tree(tree):
    tree = _Transform(_async_names(tree), None).visit(tree)
    ast.fix_missing_locations(tree)
    return compile(tree, FILENAME, "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)


def _fresh_ns():
    return {"__name__": "__main__", "_rt_input": _rt_input, "_rt_guard": _rt_guard, "_rt_hit": _rt_hit}


async def run(src, cover=False):
    """Run the pupil's program for real (the Run button)."""
    _state.update(count=0, queue=None, used=0, hits=set() if cover else None)
    lines = src.split("\n")
    result = {"type": "ok"}
    shown = None
    try:
        code, shown = _compile(src, cover)
    except SyntaxError as e:
        result = _report(e, e.lineno, lines)
    else:
        ns = _fresh_ns()
        try:
            r = eval(code, ns)
            if r is not None:
                await r
        except LoopLimit:
            result = {
                "type": "loop",
                "error": f"Stopped: a loop ran more than {LOOP_LIMIT:,} times.",
                "hint": ("That usually means an infinite loop. Check that something inside the loop "
                         "changes, so the condition can become False."),
            }
        except SystemExit:
            pass
        except BaseException as e:
            if "RT_STOPPED" in str(e):
                result = {"type": "stopped"}
            else:
                result = _report(e, _error_line(e), lines, ns)
    sys.stdout.flush()
    if cover and shown is not None:
        result["paths"] = shown
        result["hits"] = sorted(_state["hits"] or [])
    _state["hits"] = None
    return json.dumps(result)


# ---------------- Check my code ----------------

def _show(v):
    return repr(v)


def _say_inputs(inputs):
    inputs = list(inputs)
    if not inputs:
        return ""
    shown = [repr(x) if x.strip() != x or x == "" else x for x in inputs]
    if len(shown) > 6:
        return f" and typed {', '.join(shown[:3])} and so on ({len(shown)} answers)"
    return " and typed " + ", ".join(shown)


class Result:
    def __init__(self, out, ns, used, ret=None):
        self.out = out
        self.ns = ns
        self.used = used
        self.ret = ret

    @property
    def lines(self):
        return [l.rstrip() for l in self.out.split("\n") if l.strip()]


async def _exec_captured(coro_or_none, inputs, seed):
    """Run something with scripted input and captured output. Returns (out, error, used)."""
    old = sys.stdout
    buf = io.StringIO()
    sys.stdout = buf
    _state.update(count=0, queue=list(inputs), used=0)
    random.seed(seed)
    err = None
    value = None
    try:
        value = await coro_or_none()
    except SystemExit:
        pass
    except BaseException as e:
        err = e
    finally:
        sys.stdout = old
        _state["queue"] = None
    return buf.getvalue(), err, _state["used"], value


def _crash_text(err, lines, ns=None):
    if isinstance(err, NeedInput):
        return None
    if isinstance(err, LoopLimit):
        return "it got stuck in a loop that never ends. Check that something inside the loop changes."
    line = _error_line(err)
    where = f" on line {line}" if line else ""
    hint = _full_hint(err, line, lines, ns)
    return f"it stopped with an error{where}: `{type(err).__name__}: {err}`. " + hint


class Checker:
    def __init__(self, src, code, spec):
        self.src = src
        self.lines = src.split("\n")
        self.code = code
        self.full = code
        self.spec = spec
        self.ns = None
        self.out = ""
        self.used = 0
        self.fail_line = None

    # ----- running -----
    async def rerun(self, inputs=(), seed=None, what=None, _code=None):
        ns = _fresh_ns()
        code = _code or self.full

        async def go():
            r = eval(code, ns)
            if r is not None:
                await r

        out, err, used, _ = await _exec_captured(go, inputs, seed)
        if err is not None:
            ctx = what or ("When I ran your program" + _say_inputs(inputs))
            if isinstance(err, NeedInput):
                raise CheckFail(f"{ctx}, it asked for more answers than I expected. "
                                "Check how many times your program uses input().")
            if not isinstance(err, LoopLimit):
                self.fail_line = _error_line(err)
            tip = (" " + self.spec["loop_tip"]) if isinstance(err, LoopLimit) and self.spec.get("loop_tip") else ""
            raise CheckFail(f"{ctx}, " + _crash_text(err, self.lines, ns) + tip)
        return Result(out, ns, used)

    async def rerun_vars(self, values, inputs=(), seed=None, what=None):
        """Run the whole program again, with the first top-level  name = ...  replaced for each name given."""
        tree = ast.parse(self.src, FILENAME)
        done = set()
        for node in tree.body:
            if (isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                    and node.targets[0].id in values and node.targets[0].id not in done):
                v = values[node.targets[0].id]
                expr = ast.Constant(v) if not isinstance(v, (dict, list, tuple)) else ast.parse(repr(v), mode="eval").body
                node.value = ast.copy_location(expr, node.value)
                ast.fix_missing_locations(node)
                done.add(node.targets[0].id)
        return await self.rerun(inputs, seed, what, _code=_compile_tree(tree))

    def assigned(self, name):
        """True if the program has a top-level  name = ...  line."""
        for node in self.tree().body:
            if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
                return True
        return False

    def count(self, kind, inside=None):
        """How many nodes of an ast type, e.g. C.count(ast.For)."""
        node = self.func_node(inside) if inside else self.tree()
        return sum(isinstance(n, kind) for n in ast.walk(node)) if node is not None else 0

    def funcs(self):
        return [n for n in self.tree().body if isinstance(n, ast.FunctionDef)]

    def top_calls(self):
        """Names of subroutines called by the main program (not inside a def), in order."""
        names = []
        for stmt in self.tree().body:
            if isinstance(stmt, ast.FunctionDef):
                continue
            for n in ast.walk(stmt):
                if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
                    names.append(n.func.id)
        return names

    async def call(self, name, *args, inputs=(), seed=None):
        f = self.ns.get(name)
        if not callable(f):
            raise CheckFail(f"I couldn't find a subroutine called `{name}`. Check the def line and its spelling.")
        shown_args = ", ".join(_show(a) for a in args)
        args = copy.deepcopy(args)

        async def go():
            r = f(*args)
            if inspect.iscoroutine(r):
                r = await r
            return r

        out, err, used, value = await _exec_captured(go, inputs, seed)
        if err is not None:
            ctx = f"I tested `{name}({shown_args})`" + _say_inputs(inputs)
            if isinstance(err, NeedInput):
                raise CheckFail(f"{ctx}, and it kept asking for more answers. "
                                "Does the loop stop once it gets a good answer?")
            if not isinstance(err, LoopLimit):
                self.fail_line = _error_line(err)
            raise CheckFail(f"{ctx}, and " + _crash_text(err, self.lines, self.ns))
        return Result(out, self.ns, used, value)

    # ----- helpers for the checks -----
    def need(self, name, nparams=None):
        f = self.ns.get(name)
        if f is None:
            close = _did_you_mean(name, [k for k, v in self.ns.items() if callable(v)])
            extra = f" I can see `{close}`. Is that meant to be `{name}`?" if close else ""
            raise CheckFail(f"I couldn't find a subroutine called `{name}`. Write it with `def {name}(...):`.{extra}")
        if not callable(f):
            raise CheckFail(f"`{name}` should be a subroutine made with def, but it's a variable.")
        if nparams is not None:
            try:
                params = list(inspect.signature(f).parameters)
            except (TypeError, ValueError):
                params = []
            required = [p for p in inspect.signature(f).parameters.values() if p.default is inspect.Parameter.empty]
            if len(required) != nparams and len(params) != nparams:
                want = f"{nparams} parameter" + ("" if nparams == 1 else "s")
                raise CheckFail(f"`{name}` should have {want} in its brackets, but it has {len(params)}"
                                + (f": `{', '.join(params)}`." if params else "."))
        return f

    def comments(self):
        found = []
        try:
            for tok in tokenize.generate_tokens(io.StringIO(self.src).readline):
                if tok.type == tokenize.COMMENT:
                    found.append(tok.string)
        except (tokenize.TokenError, IndentationError, SyntaxError):
            pass
        return found

    def tree(self):
        return ast.parse(self.src)

    def func_node(self, name):
        for n in ast.walk(self.tree()):
            if isinstance(n, ast.FunctionDef) and n.name == name:
                return n
        return None

    def calls(self, name, inside=None):
        node = self.func_node(inside) if inside else self.tree()
        if node is None:
            return False
        for n in ast.walk(node):
            if isinstance(n, ast.Call):
                f = n.func
                if (isinstance(f, ast.Name) and f.id == name) or (isinstance(f, ast.Attribute) and f.attr == name):
                    return True
        return False

    def strings_in(self, inside):
        node = self.func_node(inside)
        out = []
        if node is None:
            return out
        for n in ast.walk(node):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                out.append(n.value)
        return out

    def options_in(self, inside):
        """Move words a fight function accepts: from ask(..., [list]) or from == "word" comparisons."""
        node = self.func_node(inside)
        found = []
        if node is None:
            return found
        for n in ast.walk(node):
            if isinstance(n, ast.Call) and len(n.args) >= 2 and isinstance(n.args[1], (ast.List, ast.Tuple)):
                for e in n.args[1].elts:
                    if isinstance(e, ast.Constant) and isinstance(e.value, str) and e.value not in found:
                        found.append(e.value)
        if not found:
            for n in ast.walk(node):
                if isinstance(n, ast.Compare) and any(isinstance(o, (ast.Eq, ast.In)) for o in n.ops):
                    for e in [n.left] + n.comparators:
                        if isinstance(e, ast.Constant) and isinstance(e.value, str) and e.value not in found:
                            found.append(e.value)
        return found

    def items_checked_in(self, inside):
        """Strings tested with  "x" in inventory  inside a function."""
        node = self.func_node(inside)
        found = []
        if node is None:
            return found
        for n in ast.walk(node):
            if isinstance(n, ast.Compare) and any(isinstance(o, (ast.In, ast.NotIn)) for o in n.ops):
                if isinstance(n.left, ast.Constant) and isinstance(n.left.value, str):
                    found.append(n.left.value)
        return found


def norm(s):
    return re.sub(r"\s+", " ", str(s)).strip().lower()


def has(text, piece):
    return norm(piece) in norm(text)


def fail(msg):
    raise CheckFail(msg)


async def check(src, spec_json):
    spec = json.loads(spec_json)
    lines = src.split("\n")
    try:
        code, _ = _compile(src, defs_only=spec.get("defs_only", False))
    except SyntaxError as e:
        r = _report(e, e.lineno, lines)
        return json.dumps({"type": "fail", "line": e.lineno,
                           "msg": "Your code has a mistake Python can't read yet, so I can't check it. "
                                  f"Press Run to see it. ({r['hint'] or r['error']})"})
    C = Checker(src, code, spec)
    try:
        C.full, _ = _compile(src)
        first = await C.rerun(spec.get("inputs", []), spec.get("seed", 1),
                              what=spec.get("what"), _code=code)
        C.ns, C.out, C.used = first.ns, first.out, first.used
        env = {"C": C, "out": C.out, "ns": C.ns, "fail": fail, "has": has, "norm": norm,
               "random": random, "re": re, "ast": ast, "CheckFail": CheckFail}
        test = compile(spec["py"], "<check>", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
        r = eval(test, env)
        if r is not None:
            await r
    except CheckFail as e:
        return json.dumps({"type": "fail", "msg": str(e), "line": C.fail_line})
    except Exception as e:
        return json.dumps({"type": "fail", "line": C.fail_line,
                           "msg": "Something unexpected happened while checking, so I couldn't finish. "
                                  "Press Run and make sure your program works, then check again. "
                                  f"(Details for your teacher: {type(e).__name__}: {e})"})
    finally:
        _state["queue"] = None
    return json.dumps({"type": "pass"})
