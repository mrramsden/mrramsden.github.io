# Checks for Escape the Dungeon Part 1.
CHECKS = {}

# Shared helpers, pasted into checks that need them.
H = r'''
def lines_of(text):
    return [l.rstrip() for l in text.split("\n")]

def solid(text):
    return [l.strip() for l in text.split("\n") if l.strip()]

def after_prompts(r, n):
    """Output after the first n input lines (each prompt line ends with what was typed)."""
    ls = r.out.split("\n")
    return "\n".join(ls[n:])

def str_times():
    for n in ast.walk(C.tree()):
        if isinstance(n, ast.BinOp) and isinstance(n.op, ast.Mult):
            if any(isinstance(x, ast.Constant) and isinstance(x.value, str) for x in (n.left, n.right)):
                return True
    return False

def print_kw(word):
    for n in ast.walk(C.tree()):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print":
            if any(k.arg == word for k in n.keywords):
                return True
    return False

def uses_fstring():
    return any(isinstance(n, ast.JoinedStr) for n in ast.walk(C.tree()))

def calls_named(name):
    return sum(1 for n in ast.walk(C.tree()) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == name)

def has_elif():
    src_lines = C.src.split("\n")
    return any(l.strip().startswith("elif") for l in src_lines)
'''

# ---------------- Stage 1: print ----------------
CHECKS["s1b2"] = {"win": "Three lines, and the middle one is yours.", "py": H + r'''
ls = solid(out)
if len(ls) < 3:
    fail("It should print three lines. Put your message inside the quote marks, inside the brackets.")
if ls[1] in ("", "___"):
    fail("The middle line should be your own message, in quote marks.")
if ls[0] != "Welcome, traveller." or ls[2] != "You hear footsteps above you.":
    fail("Only change the gap. The first and last lines should stay the same.")
'''}

CHECKS["s1b3"] = {"win": "Two lines of your own.", "py": H + r'''
if calls_named("print") < 2:
    fail("Write two print lines: one for what you can see, one for what you can hear.")
if len(solid(out)) < 2:
    fail("Your program should print two lines. Check each print has text in quote marks inside the brackets.")
'''}

CHECKS["s1i1"] = {"win": "Title, gap, story and speech: all there.", "py": H + r'''
ls = lines_of(out.rstrip("\n"))
filled = [l for l in ls if l.strip()]
if len(filled) < 4:
    fail(f"I can see {len(filled)} line(s) of text. You need a title and three lines of story.")
first = next(i for i, l in enumerate(ls) if l.strip())
if first + 1 >= len(ls) or ls[first + 1].strip():
    fail("Put a blank line straight after the title. `print()` with nothing inside prints a blank line.")
if not any(("'" in l or '"' in l) for l in filled[1:]):
    fail("One story line should have speech inside it, like: `The sign says 'Keep out!'` Use the other kind of quote mark inside.")
'''}

CHECKS["s1i2"] = {"win": "Borders made with *, not typed out.", "py": H + r'''
borders = [l for l in lines_of(out) if l.strip() == "=" * 30]
if not str_times():
    fail("Make the border with string repetition: `print(\"=\" * 30)`.")
if len(borders) < 2:
    fail("Put a border of 30 = signs above your title and another below it.")
'''}

CHECKS["s1a1"] = {"win": "Exactly right, made the way the spec asks.", "py": H + r'''
want = ["=" * 30, "      ESCAPE THE DUNGEON", "=" * 30, "torch ~ torch ~ torch", "You hear... a growl."]
got = lines_of(out.rstrip("\n"))
for i, w in enumerate(want):
    if i >= len(got):
        fail(f"Line {i + 1} is missing. It should be `{w}`.")
    if got[i] != w:
        extra = " The title has 6 spaces in front, so it sits in the middle of the 30 = signs." if i == 1 and got[i].strip() == w.strip() else ""
        fail(f"Line {i + 1} should be `{w}` but yours is `{got[i]}`.{extra}")
if len(got) > len(want):
    fail("You have extra lines at the end. The output should be exactly 5 lines.")
if not str_times():
    fail("The output is right, but the borders must use string repetition: `\"=\" * 30`.")
if not print_kw("sep"):
    fail("The output is right, but the torches must come from one print using sep: `print(\"torch\", \"torch\", \"torch\", sep=\" ~ \")`.")
if not print_kw("end"):
    fail("The output is right, but the last line must come from two prints joined with end: `print(\"You hear...\", end=\" \")`.")
'''}

CHECKS["s1a2"] = {"win": "Centred whatever the title and width.", "py": H + r'''
if not (C.assigned("title") and C.assigned("width")):
    fail("Keep the variables `title` and `width` at the top.")
for title, width in [("THE GOBLIN KING", 30), ("DOOM", 20), ("A VERY LONG DUNGEON NAME", 40)]:
    r = await C.rerun_vars({"title": title, "width": width})
    row = next((l for l in r.out.split("\n") if title in l), None)
    if row is None:
        fail(f"When I set the title to `{title}`, it didn't appear in your output.")
    pad = len(row) - len(row.lstrip(" "))
    if pad != (width - len(title)) // 2:
        fail(f"With title `{title}` and width {width}, there should be {(width - len(title)) // 2} spaces before the title, but there were {pad}. Work it out with `(width - len(title)) // 2`.")
    if not any(l.strip() and set(l.strip()) <= set("=-*#~+") and len(l.rstrip()) == width for l in r.out.split("\n")):
        fail(f"With width {width}, the border should be {width} characters long. Use the width variable for the border too.")
'''}

# ---------------- Stage 2: variables and input ----------------
CHECKS["s2b2"] = {"inputs": ["Asha", "sword"], "win": "Both answers stored and used.", "py": H + r'''
if C.used < 2:
    fail("Gap 1 should be a question in quote marks, so the program asks about the weapon.")
if has(out, "holding a weapon"):
    fail("It printed the word weapon instead of the answer. Gap 2 should be the variable, with no quote marks.")
if not has(out, "Welcome, Asha!") or not has(out, "You are holding a sword"):
    fail("When I typed Asha and sword, it should say `You are holding a sword`.")
'''}

CHECKS["s2b3"] = {"inputs": ["Rex"], "win": "Your companion has a name.", "py": H + r'''
if not C.assigned("pet"):
    fail("Store the answer in a variable called `pet`.")
if has(out, "companion is pet"):
    fail("It printed the word pet. Take the quote marks off so Python uses the variable.")
if not has(out, "Your loyal companion is Rex"):
    fail("When I typed Rex, it should say `Your loyal companion is Rex`. Gap 1 is a question in quote marks.")
'''}

CHECKS["s2i1"] = {"inputs": ["Asha", "sword", "red"], "win": "Works for any hero you type in.", "py": H + r'''
if C.used != 3:
    fail(f"Ask three questions: name, weapon and cloak colour. I answered {C.used}.")
for name, weapon, colour in [("Asha", "sword", "red"), ("Bram", "axe", "green")]:
    r = await C.rerun([name, weapon, colour])
    if not has(r.out, f"{name} carries a {weapon} and wears a {colour} cloak"):
        fail(f"I typed {name}, {weapon}, {colour}. It should say `{name} carries a {weapon} and wears a {colour} cloak.` Check the spaces between the words too.")
    if not has(r.out, f"Good luck, {name}!"):
        fail(f"I typed {name}. It should end with `Good luck, {name}!`")
'''}

CHECKS["s2i2"] = {"inputs": ["Asha", "sword", "red"], "win": "f-strings mastered.", "py": H + r'''
if not uses_fstring():
    fail("Use an f-string: put f before the quote mark and the variable in curly brackets, like `f\"{name} the Brave\"`.")
if not has(out, "Asha the Brave enters the dungeon"):
    fail("When I typed Asha, it should say `Asha the Brave enters the dungeon.`")
'''}

CHECKS["s2a1"] = {"inputs": ["  asha stormborn ", "MAGE", " corsham"], "win": "Tidy, Title Case and the right shape.", "py": H + r'''
if not uses_fstring():
    fail("Print the card using f-strings.")
for typed, want in [(["  asha stormborn ", "MAGE", " corsham"], ("Asha Stormborn", "Mage", "Corsham")),
                    (["BRAM", "  rogue", "bath  "], ("Bram", "Rogue", "Bath"))]:
    r = await C.rerun(typed)
    card = r.out.split("\n")[3:]
    shown = ", ".join(repr(t) for t in typed)
    for label, value in zip(("Name", "Class", "Home"), want):
        if not any(re.fullmatch(label + r":\s+" + re.escape(value), l.strip()) for l in card):
            fail(f"I typed {shown}. The card should have the line `{label}: {value}`, tidied with .strip().title().")
    if sum(1 for l in card if l.strip() == "-" * 30) < 2:
        fail("Put a line of 30 dashes above and below the card.")
'''}

CHECKS["s2a2"] = {"inputs": ["  asha stormborn ", "MAGE", " corsham"], "win": "The box hugs the longest line.", "py": H + r'''
for typed in (["  asha stormborn ", "MAGE", " corsham"], ["Bo", "warrior", "Weston-super-Mare"]):
    r = await C.rerun(typed)
    box = [l.rstrip() for l in r.out.split("\n")[3:] if l.strip()]
    box = [l for l in box if l.startswith("+") or l.startswith("|")]
    shown = ", ".join(repr(t) for t in typed)
    if len(box) < 5:
        fail(f"I typed {shown}. I expected a box of 5 lines starting with + or |.")
    widths = {len(l) for l in box}
    if len(widths) != 1:
        fail(f"I typed {shown}. Every line of the box should be the same length, but they're different. Use .ljust() on each line.")
    inner = [l[2:-2] for l in box if l.startswith("|")]
    if min(len(i) - len(i.rstrip()) for i in inner) != 0 or not all(l.startswith("| ") and l.endswith(" |") for l in box if l.startswith("|")):
        fail(f"I typed {shown}. The longest line should have exactly one space before the |. Work out the width with max() and len().")
'''}

# ---------------- Stage 3: int and maths ----------------
CHECKS["s3b2"] = {"inputs": ["50"], "win": "The price comes off.", "py": H + r'''
if ns.get("gold") != 35:
    fail(f"With 50 gold, you should have 35 left after the 15-gold lantern. You have {ns.get('gold')!r}. Gap is `price`.")
r = await C.rerun(["15"])
if r.ns.get("gold") != 0:
    fail("With 15 gold you should have 0 left.")
'''}

CHECKS["s3b3"] = {"inputs": ["3"], "win": "3 potions, 12 gold.", "py": H + r'''
if ns.get("cost") != 12:
    fail(f"When I asked for 3 potions, cost should be 12, but it's {ns.get('cost')!r}. Gap 1 is `potions`.")
if not re.search(r"\b12\b", out.split("\n", 1)[-1]):
    fail("It should print the cost. Gap 2 is `cost`.")
r = await C.rerun(["10"])
if r.ns.get("cost") != 40:
    fail("When I asked for 10 potions it didn't cost 40. Use the potions variable, not a fixed number.")
'''}

CHECKS["s3i1"] = {"inputs": ["50", "3"], "win": "The shop adds up.", "py": H + r'''
for g, p, cost, left in [(50, 3, 12, 38), (20, 5, 20, 0), (100, 1, 4, 96)]:
    r = await C.rerun([str(g), str(p)])
    shown = after_prompts(r, 2)
    if not re.search(r"cost\D*" + str(cost) + r"\b", shown, re.I):
        fail(f"I typed {g} gold and {p} potions. It should print `Total cost: {cost} gold`. Did you use int() on both answers?")
    if not re.search(r"left\D*" + str(left) + r"\b", shown, re.I):
        fail(f"I typed {g} gold and {p} potions. It should print `Gold left: {left}`.")
'''}

CHECKS["s3i2"] = {"inputs": ["50", "4"], "win": "Shared fairly with // and %.", "py": H + r'''
if "//" not in C.src or "%" not in C.src:
    fail("Use // for each person's share and % for the leftovers.")
for coins, people, each, spare in [(50, 4, 12, 2), (7, 3, 2, 1), (20, 5, 4, 0)]:
    r = await C.rerun([str(coins), str(people)])
    nums = [int(x) for x in re.findall(r"-?\d+", after_prompts(r, 2))]
    if each not in nums or spare not in nums:
        fail(f"I typed {coins} coins and {people} people. It should say {each} each with {spare} left over.")
'''}

CHECKS["s3a1"] = {"inputs": ["500"], "win": "Currency converted with only // and %.", "py": H + r'''
if C.count(ast.If) or C.count(ast.For) or C.count(ast.While):
    fail("The spec says no loops and no if. Use only // and %.")
for copper, g, s, c in [(500, 2, 1, 8), (239, 0, 19, 11), (240, 1, 0, 0), (0, 0, 0, 0)]:
    r = await C.rerun([str(copper)])
    m = re.search(r"(\d+)\s*gold\D*?(\d+)\s*silver\D*?(\d+)\s*copper", after_prompts(r, 1), re.I)
    if not m:
        fail(f"I typed {copper}. It should print `{g} gold, {s} silver, {c} copper`.")
    if tuple(int(x) for x in m.groups()) != (g, s, c):
        fail(f"I typed {copper}. It should print `{g} gold, {s} silver, {c} copper`, but yours says `{m.group(0)}`.")
'''}

CHECKS["s3a2"] = {"inputs": ["3", "0", "0"], "win": "Toll paid, change worked out.", "py": H + r'''
for typed, want in [(["3", "0", "0"], (1, 16, 8)), (["2", "5", "7"], (1, 2, 3)), (["1", "3", "4"], (0, 0, 0))]:
    r = await C.rerun(typed)
    m = re.search(r"(\d+)\s*gold\D*?(\d+)\s*silver\D*?(\d+)\s*copper", after_prompts(r, 3), re.I)
    g, s, c = want
    shown = f"{typed[0]} gold, {typed[1]} silver and {typed[2]} copper"
    if not m or tuple(int(x) for x in m.groups()) != want:
        fail(f"I typed {shown}. After the toll it should say `{g} gold, {s} silver, {c} copper`.")
'''}

# ---------------- Stage 4: if / elif / else ----------------
CHECKS["s4b2"] = {"inputs": ["yes"], "win": "Yes lights the room; anything else is spooky.", "py": H + r'''
if not has(out, "The room fills with light"):
    fail("When I typed yes, the room should fill with light. Gap 1 is `\"yes\"`, with quote marks.")
r = await C.rerun(["no"])
rest = after_prompts(r, 1).strip()
if not rest or has(rest, "fills with light"):
    fail("When I typed no, it should print your own spooky message. Gap 2 is your message in quote marks.")
'''}

CHECKS["s4b3"] = {"inputs": ["maybe"], "win": "All three answers tested.", "py": H + r'''
if not re.search(r"can.?t make up your mind", norm(out)):
    fail("When I typed maybe, it should say `You can't make up your mind. The torch goes out.` Gap 1 is `torch == \"maybe\"`.")
r = await C.rerun(["yes"])
if not has(r.out, "fills with light"):
    fail("When I typed yes, the room should still fill with light.")
r = await C.rerun(["no"])
if not has(r.out, "stays dark"):
    fail("When I typed no, it should still say `It stays dark.`")
'''}

CHECKS["s4i1"] = {"inputs": ["85"], "win": "Right on every edge.", "py": H + r'''
for h, word, band in [(85, "strong", "70 or more"), (70, "strong", "70 or more"), (69, "wounded", "30 to 69"),
                      (45, "wounded", "30 to 69"), (30, "wounded", "30 to 69"), (29, "potion", "below 30"),
                      (10, "potion", "below 30"), (0, "potion", "below 30"), (100, "strong", "70 or more")]:
    r = await C.rerun([str(h)])
    rest = norm(after_prompts(r, 1))
    others = {"strong", "wounded", "potion"} - {word}
    if word not in rest or any(o in rest for o in others):
        tip = " That's an edge: check whether you need >= or >." if h in (70, 69, 30, 29) else ""
        fail(f"I typed {h}. That's {band}, so it should say the `{word}` message.{tip}")
'''}

CHECKS["s4i2"] = {"inputs": ["yes"], "win": "Any kind of yes works.", "py": H + r'''
lit = norm(after_prompts(await C.rerun(["yes"]), 1))
dark = norm(after_prompts(await C.rerun(["no"]), 1))
if lit == dark:
    fail("yes and no give the same message. Light the room only for a yes.")
for typed in ["YES", "Yes", "y", "Y"]:
    got = norm(after_prompts(await C.rerun([typed]), 1))
    if got != lit:
        fail(f"I typed {typed} and the room didn't light. Use `.lower()` on the answer, and `or` to accept y too.")
'''}

CHECKS["s4a1"] = {"inputs": ["yes", "50"], "win": "The guard behaves in every case.", "py": H + r'''
cases = [(["yes", "5"], "waves you through", "a pass"), (["Y ", "0"], "waves you through", "a pass"),
         ([" YES", "50"], "waves you through", "a pass"), (["no", "20"], None, "no pass and 20 gold"),
         (["no", "35"], None, "no pass and 35 gold"), (["no", "19"], "laughs", "no pass and 19 gold"),
         (["no", "10"], "laughs", "no pass and 10 gold"), (["no", "9"], "go away", "no pass and 9 gold"),
         (["n", "0"], "go away", "no pass and 0 gold")]
for typed, want, what in cases:
    r = await C.rerun(typed)
    text = norm(r.out)
    shown = ", ".join(repr(t) for t in typed)
    if want is None:
        left = int(typed[1]) - 20
        tail = after_prompts(r, 2)
        if "laugh" in text or "go away" in text or "waves" in text or not re.search(r"(?<!\d)" + str(left) + r"(?!\d)", tail):
            fail(f"I typed {shown} ({what}). The guard should take 20 gold and say you have {left} left. That's a boundary, so check >=." if typed[1] == "20" else f"I typed {shown} ({what}). The guard should take 20 gold and say you have {left} left.")
    elif want not in text:
        tip = " Tidy the answer with .strip().lower(), and accept y as well as yes." if typed[0] != "no" and typed[0] != "n" else " That's a boundary, so check >= and >." if typed[1] in ("10", "9", "19", "20") else ""
        fail(f"I typed {shown} ({what}). The guard should say the `{want}` message.{tip}")
'''}

CHECKS["s4a2"] = {"inputs": ["no", "-5"], "win": "Nested selection, with royals and impossible gold.", "py": H + r'''
r = await C.rerun(["no", "-5"])
rest = norm(after_prompts(r, 2))
if "not possible" not in rest:
    fail("I typed no and -5 gold. It should say `That's not possible.`")
if "go away" in rest or "laugh" in rest:
    fail("I typed -5 gold. It should only say `That's not possible.`, and nothing else.")

async def royal(name):
    for order in (["yes", name, "50"], ["yes", "50", name]):
        try:
            r = await C.rerun(order)
        except CheckFail:
            continue
        if r.used >= 2 and (name in r.out):
            return r
    fail(f"With a pass, it should ask the player's name. I couldn't get it to accept the name {name}.")

r = await royal("Bram")
if "highness" not in norm(r.out):
    fail("I had a pass and typed Bram, who's on the royal list. It should say `Welcome, your highness.`")
r = await royal("Dave")
if "highness" in norm(r.out) or "waves" not in norm(r.out):
    fail("I had a pass and typed Dave, who isn't royal. It should give the normal pass message.")
'''}

# ---------------- Stage 5: while loops ----------------
CHECKS["s5b2"] = {"inputs": ["cat", "DRAGON", "dragon"], "win": "It keeps asking until it's right.", "py": H + r'''
if C.used != 3:
    fail(f"I typed cat, DRAGON, then dragon, so it should ask 3 times. It asked {C.used}. Gap 2 should be `input(\"Enter the password: \")`.")
if norm(out).count("wrong! try again") != 2:
    fail("It should say Wrong! after each wrong guess. Gap 1 is `!=`.")
if not has(out.split("\n")[-2], "Door unlocked"):
    fail("It should finish with `Door unlocked!`")
r = await C.rerun(["dragon"])
if "wrong" in norm(r.out):
    fail("When I typed dragon first time, it still said Wrong!")
'''}

CHECKS["s5b3"] = {"win": "5, 4, 3, 2, 1... trap door!", "py": H + r'''
ls = solid(out)
if ls[:5] != ["5", "4", "3", "2", "1"]:
    fail("It should count 5, 4, 3, 2, 1. The gap is `count - 1`.")
if len(ls) != 6 or not has(ls[5], "trap door opens"):
    fail("After 1 it should stop and say `The trap door opens!`")
'''}

CHECKS["s5i1"] = {"inputs": ["3", "12", "7"], "win": "Hints and a counter, spot on.", "py": H + r'''
for typed, n in [(["3", "12", "7"], 3), (["7"], 1), (["20", "1", "8", "6", "7"], 5)]:
    r = await C.rerun(typed)
    shown = ", ".join(typed)
    if r.used != len(typed):
        fail(f"I typed {shown}. It should keep asking until 7, and then stop.")
    said = re.findall(r"too (high|low)", norm(r.out))
    want = ["high" if int(t) > 7 else "low" for t in typed[:-1]]
    if said != want:
        fail(f"I typed {shown}. After each wrong guess it should say: " + ", ".join(f"Too {w}!" for w in want) + ". Check which way round your > and < are.")
    if not re.search(r"(?<!\d)" + str(n) + r"(?!\d)", solid(r.out)[-1]):
        fail(f"I typed {shown}, so it took {n} guess{'es' if n > 1 else ''}. The last line should say so. Start the counter at 1 and add 1 each time round.")
'''}

CHECKS["s5i2"] = {"inputs": ["a", "b", "c", "d"], "win": "Three chances, tested three ways.", "py": H + r'''
pw = ns.get("password") if isinstance(ns.get("password"), str) else "dragon"
r = await C.rerun([pw])
if "remains locked" in norm(r.out):
    fail(f"I typed the password ({pw}) first time and it still said the door remains locked.")
r = await C.rerun(["x", "y", pw])
if "remains locked" in norm(r.out):
    fail(f"I got the password right on the third go, but it said the door remains locked.")
r = await C.rerun(["x", "y", "z", pw, pw])
if r.used != 3:
    fail(f"After three wrong guesses it should stop asking. It asked {r.used} times.")
if "remains locked" not in norm(r.out):
    fail("After three wrong guesses it should say `The door remains locked.`")
'''}

CHECKS["s5a1"] = {"seed": 2, "inputs": [str(n) for n in range(1, 51)], "win": "A fair goblin: hints, 7 guesses and no crashes.", "py": H + r'''
if not C.calls("randint"):
    fail("Use `random.randint(1, 50)` for the secret number.")
if not C.assigned("secret"):
    fail("Keep the variable `secret` for the goblin's number.")
async def play(typed):
    return await C.rerun_vars({"secret": 20}, typed, what="When I set the secret to 20 and typed " + ", ".join(repr(t) for t in typed))
r = await play(["10", "30", "20"])
t = norm(r.out)
if "low" not in t or "high" not in t:
    fail("I guessed 10, then 30 (the secret was 20). It should say too low, then too high.")
if r.used != 3:
    fail("I guessed 20 on my third go. The game should stop there.")
r = await play(["ten", "20"])
if r.used != 2:
    fail("I typed ten, then 20. It should tell me ten isn't a number, then let me guess again.")
if not re.search(r"(?<!\d)1(?!\d)", after_prompts(r, 2)):
    fail("I typed ten (not a number), then 20. That's 1 guess, because ten doesn't count. It should say it took 1 guess.")
try:
    r = await play(["1", "2", "3", "4", "5", "6", "8", "9"])
except CheckFail as e:
    if "more answers" in str(e):
        fail("I made 7 wrong guesses and it kept asking. The player only gets 7 guesses, so count them and stop the loop at 7.")
    raise
if r.used != 7:
    fail(f"After 7 wrong guesses the game should end. It asked {r.used} times.")
if "20" not in after_prompts(r, 7):
    fail("After 7 wrong guesses, reveal the number. The secret was 20, but it didn't say so.")
r = await play(["1", "2", "3", "4", "5", "6", "20"])
if r.used != 7 or "low" not in norm(after_prompts(r, 6)) and not re.search(r"(?<!\d)7(?!\d)", after_prompts(r, 7)):
    fail("I guessed 20 on my 7th and last go. That should still count as a win, taking 7 guesses.")
'''}

# ---------------- Stage 6: for loops ----------------
CHECKS["s6b2"] = {"win": "Exactly 3 steps.", "py": H + r'''
n = norm(out).count("you take a step forward")
if n != 3:
    fail(f"The player took {n} steps. It should be exactly 3. The gap is `3`.")
'''}

CHECKS["s6b3"] = {"win": "Your name, letter by letter.", "py": H + r'''
if "DRAGON" in C.src:
    fail("Change DRAGON to your own name.")
ls = solid(out)
stars = [l for l in ls if "*" in l]
letters = [l for l in ls if "*" not in l]
if not stars:
    fail("Add a second print inside the loop, so each letter is followed by a *.")
if len(stars) != len(letters):
    fail("Each letter should be followed by a *. Make sure both prints are indented inside the loop.")
'''}

CHECKS["s6i1"] = {"inputs": ["7"], "win": "A perfect damage table.", "py": H + r'''
for s in (7, 3):
    r = await C.rerun([str(s)])
    rows = re.findall(r"(\d+)\s*x\s*(\d+)\s*=\s*(\d+)", r.out)
    want = [(str(i), str(s), str(i * s)) for i in range(1, 13)]
    if rows != want:
        if rows and rows[-1][0] == "11":
            fail(f"Sword strength {s}: it stops at 11. range stops before the second number, so use range(1, 13).")
        if rows and rows[0][0] == "0":
            fail(f"Sword strength {s}: it starts at 0. Use range(1, 13).")
        fail(f"Sword strength {s}: it should print 12 lines, from `1 x {s} = {s}` to `12 x {s} = {12 * s}`.")
'''}

CHECKS["s6i2"] = {"inputs": ["1", "2", "3", "4", "5"], "win": "A running total across 5 chests.", "py": H + r'''
if C.used != 5:
    fail(f"There are 5 chests, so it should ask 5 times. It asked {C.used}.")
for i in range(1, 6):
    if not re.search(r"chest\s*" + str(i), out, re.I):
        fail(f"Each question should say which chest it is, like `Coins in chest {i}:`. Use the loop variable.")
for typed, total in [(["1", "2", "3", "4", "5"], 15), (["10", "0", "0", "0", "7"], 17)]:
    r = await C.rerun(typed)
    if not re.search(r"(?<!\d)" + str(total) + r"(?!\d)", after_prompts(r, 5)):
        fail(f"I typed {', '.join(typed)}. The total should be {total}. Start total at 0 before the loop, and add each chest inside it.")
'''}

CHECKS["s6a1"] = {"inputs": ["4"], "win": "Nested loops, no shortcuts.", "py": H + r'''
if str_times():
    fail("This one bans string repetition (*). Print each # from an inner loop.")
nested = any(isinstance(m, ast.For) for n in ast.walk(C.tree()) if isinstance(n, ast.For) for m in ast.walk(n) if m is not n)
if not nested:
    fail("Use a for loop inside a for loop.")
for h in (4, 1, 6):
    r = await C.rerun([str(h)])
    rows = [l.replace(" ", "") for l in after_prompts(r, 1).split("\n") if l.strip()]
    if rows != ["#" * i for i in range(1, h + 1)]:
        fail(f"Height {h}: it should draw {h} rows, from `#` up to `{'#' * h}`. Use print(\"#\", end=\"\") in the inner loop, then print() to end the row.")
'''}

CHECKS["s6a2"] = {"inputs": ["2", "4"], "win": "The map, with you on it.", "py": H + r'''
for row, col in [(2, 4), (1, 1), (5, 5)]:
    r = await C.rerun([str(row), str(col)])
    grid = [l.replace(" ", "") for l in after_prompts(r, 2).split("\n") if l.strip()]
    want = ["".join("P" if (rr, cc) == (row, col) else "." for cc in range(1, 6)) for rr in range(1, 6)]
    if grid != want:
        fail(f"I typed row {row}, column {col}. The P should be on row {row}, column {col} of a 5 by 5 grid of dots.")
if not C.comments():
    fail("The map works. Now add a comment explaining why a for loop is better than a while loop here.")
'''}

# ---------------- Stage 7: putting it together ----------------
CHECKS["s7b1"] = {"inputs": ["Asha", "left", "nope", "freedom"], "win": "Every step of the escape works.", "py": H + r'''
if C.used != 4:
    fail("It should ask your name, left or right, then keep asking for the password until freedom.")
for i in (1, 2, 3):
    if not re.search(r"step\s*" + str(i) + r"\b", out, re.I):
        fail(f"It should print Step 1, Step 2 and Step 3. The gap in Step 4 is `step`.")
last = solid(out)[-1]
if "Asha" not in last:
    fail("The victory message (the last line) should use the player's name. Gap 5 should include `name`.")
left = after_prompts(await C.rerun(["Asha", "left", "freedom"]), 3).split("Enter the password")[0]
right = after_prompts(await C.rerun(["Asha", "right", "freedom"]), 3).split("Enter the password")[0]
if norm(left) == norm(right) or not left.strip() or not right.strip():
    fail("Left and right should print different messages. Fill both gaps in Step 2.")
'''}

CHECKS["s7b2"] = {"inputs": ["Asha", "left", "freedom"], "win": "15 gold for 3 steps.", "py": H + r'''
if ns.get("gold") != 15:
    fail(f"After 3 steps at 5 gold each, gold should be 15. It's {ns.get('gold')!r}. Put gold = 0 before the loop and gold = gold + 5 inside it.")
if not re.search(r"(?<!\d)15(?!\d)", out.split("Step 3")[-1]):
    fail("Print how much gold they escaped with, after the loop.")
'''}

CHECKS["s7i1"] = {"defs_only": True, "win": "Everything on the list is in your adventure.", "py": H + r'''
need = []
if calls_named("input") < 2:
    need.append("input() to ask at least two things")
if calls_named("int") < 1:
    need.append("int() to turn an answer into a number")
if not has_elif() or not any(isinstance(n, ast.If) and n.orelse for n in ast.walk(C.tree())):
    need.append("if, elif and else")
if not C.count(ast.While):
    need.append("a while loop")
if not C.count(ast.For):
    need.append("a for loop")
if need:
    fail("Your adventure still needs: " + "; ".join(need) + ".")
'''}

CHECKS["s7a1"] = {"defs_only": True, "win": "A dungeon run that always ends properly.", "py": H + r'''
if not C.calls("randint"):
    fail("Use random.randint for the events.")
whiles = [n for n in ast.walk(C.tree()) if isinstance(n, ast.While)]
if not any("health" in ast.unparse(w.test) for w in whiles):
    fail("The rooms should be in a loop that stops early if health drops to 0 or below, so the while condition needs `health`.")
for s in range(30):
    r = await C.rerun(["7"] * 60, seed=s, what="When I played, answering 7 to every question")
    h, g = r.ns.get("health"), r.ns.get("gold")
    if not isinstance(h, int) or not isinstance(g, int):
        fail("Keep the variables `health` and `gold` as whole numbers.")
    if g > 100:
        fail(f"One run ended with {g} gold, which is more than 5 rooms of treasure can give. Is the loop stopping after 5 rooms?")
    if r.used > 5 + 3 + 5:
        fail("The game asked too many questions. Only 5 rooms, then 3 password attempts.")
'''}
