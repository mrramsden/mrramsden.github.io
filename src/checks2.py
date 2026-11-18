# Checks for Escape the Dungeon Part 2.
CHECKS = {}

H = r'''
def solid(text):
    return [l.strip() for l in text.split("\n") if l.strip()]

def prints_in(fname):
    node = C.func_node(fname)
    return sum(1 for n in ast.walk(node) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print") if node else 0

def has_kind(fname, kind):
    node = C.func_node(fname)
    return node is not None and any(isinstance(n, kind) for n in ast.walk(node))

def has_if_else(fname):
    node = C.func_node(fname)
    return node is not None and any(isinstance(n, ast.If) and n.orelse for n in ast.walk(node))

def has_elif(fname):
    node = C.func_node(fname)
    if node is None:
        return False
    lines = C.src.split("\n")
    return any(isinstance(n, ast.If) and lines[n.lineno - 1].strip().startswith("elif") for n in ast.walk(node))

def room_names():
    return [f.name for f in C.funcs()]

def calls_input(fname):
    return C.calls("input", inside=fname)

def main_whiles():
    return [n for n in C.tree().body if isinstance(n, ast.While)]
'''

# ---------------- Stage 2: def and calling ----------------
CHECKS["p2b2"] = {"win": "A named procedure, called once.", "py": H + r'''
C.need("library", 0)
if "library" not in C.top_calls():
    fail("The procedure is there, but it never runs. Gap 2 calls it: `library()`, with brackets.")
if not has(out, "dusty library"):
    fail("When I ran it, the library didn't appear. Check the call at the bottom has brackets: `library()`.")
'''}

CHECKS["p2b3"] = {"defs_only": True, "win": "Your Room 1 is a working procedure.", "py": H + r'''
rooms = [f for f in room_names() if prints_in(f) >= 2]
if not C.funcs():
    fail("Start your room with def, a name, brackets and a colon, like `def entrance():`")
if not rooms:
    fail("Your room needs at least two print lines, indented under the def.")
called = [r for r in rooms if r in C.top_calls()]
if not called:
    fail(f"Your room `{rooms[0]}` is never called. Add `{rooms[0]}()` at the bottom, not indented.")
'''}

CHECKS["p2i1"] = {"defs_only": True, "win": "Two rooms, one with a choice, called in order.", "py": H + r'''
names = room_names()
if len(names) < 2:
    fail(f"Write two room procedures. I found {len(names)}.")
choice = [n for n in names if calls_input(n) and has_if_else(n)]
if not choice:
    fail("One room should ask the player a question with input(), then use if and else on the answer.")
calls = [c for c in C.top_calls() if c in names]
if len(set(calls)) < 2:
    fail("Call both rooms at the bottom of your program, one after the other.")
'''}

CHECKS["p2i2"] = {"defs_only": True, "win": "Written once, used lots.", "py": H + r'''
C.need("divider", 0)
r = await C.call("divider")
if r.out.strip() != "~" * 30:
    fail("`divider()` should print exactly 30 ~ signs: `print(\"~\" * 30)`. It printed: " + (r.out.strip() or "nothing"))
if C.top_calls().count("divider") < 1:
    fail("Call `divider()` between your rooms.")
'''}

CHECKS["p2a1"] = {"defs_only": True, "win": "Both rooms loop until they should stop.", "py": H + r'''
C.need("riddle_door", 0)
C.need("armoury", 0)
if not has_kind("riddle_door", ast.While) or not has_kind("armoury", ast.While):
    fail("Both rooms need a while loop that keeps asking.")
answers = [s for s in C.strings_in("riddle_door") if s.strip() and len(s) < 25 and "?" not in s]
for ans in answers:
    try:
        r = await C.call("riddle_door", inputs=["wrong one", "nope", ans])
    except CheckFail:
        continue
    if r.used == 3:
        break
else:
    fail("I gave `riddle_door()` two wrong answers and then the right one, but it didn't stop. Keep asking while the answer is wrong.")
r = await C.call("armoury", inputs=["look", "search", "look", "leave"])
if r.used != 4:
    fail("I typed look, search, look, then leave. armoury() should keep asking until leave, then stop.")
look = (await C.call("armoury", inputs=["look", "leave"])).out
search = (await C.call("armoury", inputs=["search", "leave"])).out
if norm(look.split("\n", 1)[-1]) == norm(search.split("\n", 1)[-1]):
    fail("Look and search should each give a different response.")
'''}

CHECKS["p2a2"] = {"defs_only": True, "win": "One procedure, reused from two rooms.", "py": H + r'''
C.need("torches", 0)
r = await C.call("torches")
if len(solid(r.out)) != 3:
    fail("`torches()` should light 3 torches, one line each, using a for loop.")
if not has_kind("torches", ast.For):
    fail("Use a for loop inside torches().")
users = [f for f in room_names() if f != "torches" and C.calls("torches", inside=f)]
if len(users) < 2:
    fail(f"Call `torches()` from inside two different rooms. I found it in {len(users)}.")
if not C.comments():
    fail("Add a comment explaining one advantage of doing it this way.")
'''}

# ---------------- Stage 3: the main program ----------------
CHECKS["p3b2"] = {"inputs": ["friend"], "win": "Five torches, then the guard.", "py": H + r'''
if not has(out, "Torch 5 is lit") or has(out, "Torch 6"):
    fail("The corridor should light exactly 5 torches. range stops before the second number, so gap 1 is 6.")
calls = [c for c in C.top_calls() if c in ("torches", "guard")]
if calls != ["torches", "guard"]:
    fail("The main program should call `torches()` first, then `guard()`.")
if not has(out, "lets you pass"):
    fail("When I typed friend, the guard should let you pass.")
'''}

CHECKS["p3i1"] = {"defs_only": True, "win": "Three rooms, three different structures.", "py": H + r'''
names = room_names()
if len(names) < 3:
    fail(f"Write three room procedures. I found {len(names)}.")
if not any(has_kind(n, ast.For) for n in names):
    fail("One room should use a for loop.")
if not any(has_kind(n, ast.While) for n in names):
    fail("One room should use a while loop.")
if not any(has_elif(n) and has_if_else(n) for n in names):
    fail("One room should use if, elif and else.")
if len(set(c for c in C.top_calls() if c in names)) < 3:
    fail("The main program should call all three rooms.")
'''}

CHECKS["p3i2"] = {"defs_only": True, "win": "The player chooses, until they type exit.", "py": H + r'''
loops = main_whiles()
if not loops:
    fail("Put the choice in a while loop in the main program, so the player can choose again and again.")
if not any("exit" in ast.unparse(w) for w in loops):
    fail("The loop should end when the player types exit.")
if not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "input" for w in loops for n in ast.walk(w)):
    fail("Ask the player where they want to go inside the loop.")
'''}

CHECKS["p3a1"] = {"inputs": ["exit"], "win": "A menu that copes with anything.", "py": H + r'''
names = room_names()
if len([n for n in names if not n.startswith("show_help")]) < 3:
    fail("Write at least three room procedures.")
if not main_whiles():
    fail("The main program should be a loop that asks Where now?")
consts = [n.value for n in ast.walk(C.tree()) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
quiet = [n for n in names if not calls_input(n) and n in consts]
try:
    r = await C.rerun(["EXIT"])
except CheckFail as e:
    if "more answers" in str(e):
        fail("I typed EXIT in capitals and it kept asking. Accept any case: tidy the answer with `.strip().lower()`.")
    raise
if r.used != 1:
    fail("I typed EXIT in capitals. It should accept that and end the game.")
r = await C.rerun(["nowhere", "exit"])
if not re.search(r"(?<!\d)0(?!\d)", solid(r.out)[-1]):
    fail("I typed nowhere, then exit. nowhere isn't a room, so it shouldn't count. It should say 0 rooms visited at the end.")
if r.out.count("\n") < 3:
    fail("I typed nowhere. Tell the player that room doesn't exist.")
if quiet:
    room = quiet[0]
    r = await C.rerun([" " + room.upper() + " ", room, "exit"])
    if not re.search(r"(?<!\d)2(?!\d)", solid(r.out)[-1]):
        fail(f"I visited {room} twice (once typed as ` {room.upper()} `), then exit. The last line should say 2 rooms visited. Tidy the answer with .strip().lower().")
'''}

CHECKS["p3a2"] = {"inputs": ["exit"], "win": "Help is at hand.", "py": H + r'''
C.need("show_help", 0)
helptext = (await C.call("show_help")).out.strip()
if not helptext:
    fail("`show_help()` should print the commands.")
for typed in ("help", "h", "HELP"):
    r = await C.rerun([typed, "exit"])
    if helptext.split("\n")[0] not in r.out:
        fail(f"I typed {typed}, but the help didn't appear.")
if not C.comments():
    fail("Add a comment explaining why visited has to live in the main program.")
'''}

# ---------------- Stage 4: parameters and return ----------------
CHECKS["p4b2"] = {"win": "15 gold in, and back out.", "py": H + r'''
C.need("treasure_room", 1)
r = await C.call("treasure_room", 0)
if r.ret is None:
    fail("Nothing came back. Gap 2 is `gold`, so it says `return gold`.")
if r.ret != 15:
    fail(f"I tested `treasure_room(0)`. It should return 15, but returned {r.ret!r}. Gap 1 is 15.")
r = await C.call("treasure_room", 10)
if r.ret != 25:
    fail("I tested `treasure_room(10)`. It should return 25.")
if not has(out, "You now have 15 gold"):
    fail("The main program should end with 15 gold. Gap 3 passes gold in: `treasure_room(gold)`.")
'''}

CHECKS["p4b3"] = {"win": "50 in, 80 out.", "py": H + r'''
C.need("potion_room", 1)
r = await C.call("potion_room", 50)
if r.ret is None:
    fail("Nothing came back. After adding 30, add `return health`.")
if r.ret != 80:
    fail(f"I tested `potion_room(50)`. It should return 80, but returned {r.ret!r}. Write `health = health + 30`.")
r = await C.call("potion_room", 0)
if r.ret != 30:
    fail("I tested `potion_room(0)`. It should return 30. Use the parameter, not a fixed number.")
'''}

CHECKS["p4i1"] = {"win": "Health 60, gold 10.", "py": H + r'''
C.need("trap_room", 1)
C.need("treasure_room", 1)
r = await C.call("trap_room", 100)
if r.ret != 80:
    fail(f"I tested `trap_room(100)`. It should return 80, but returned {r.ret!r}." + (" Add `return health`." if r.ret is None else ""))
r = await C.call("treasure_room", 0)
if r.ret != 10:
    fail(f"I tested `treasure_room(0)`. It should return 10, but returned {r.ret!r}." + (" Add `return gold`." if r.ret is None else ""))
if not re.search(r"health\D*60\b", out, re.I) or not re.search(r"gold\D*10\b", out, re.I):
    fail("The main program should end with `Health: 60` and `Gold: 10`. Catch each result, like `health = trap_room(health)`.")
'''}

CHECKS["p4i2"] = {"defs_only": True, "win": "Jump to safety; duck and it hurts.", "py": H + r'''
C.need("dodge_room", 1)
r = await C.call("dodge_room", 100, inputs=["jump"])
if r.ret is None:
    fail("Return health either way: `return health` at the end, not inside the if.")
if r.ret != 100:
    fail(f"I typed jump. That avoids the boulder, so health should stay 100. It returned {r.ret!r}.")
r = await C.call("dodge_room", 100, inputs=["duck"])
if r.ret != 70:
    fail(f"I typed duck. That takes 30 damage, so 100 should become 70. It returned {r.ret!r}.")
'''}

CHECKS["p4a1"] = {"inputs": ["yes"], "win": "Two in, two out, in the right order.", "py": H + r'''
C.need("shop", 2)
for g, h, typed, want in [(15, 40, "yes", (5, 65)), (10, 40, "yes", (0, 65)), (9, 40, "yes", (9, 40)),
                          (50, 40, "no", (50, 40)), (0, 100, "yes", (0, 100))]:
    r = await C.call("shop", g, h, inputs=[typed])
    if not isinstance(r.ret, tuple) or len(r.ret) != 2:
        fail("shop should return two values: `return gold, health`.")
    if tuple(r.ret) != want:
        if tuple(r.ret) == want[::-1]:
            fail("shop returns health first. It should be `return gold, health`, to match `gold, health = shop(gold, health)`.")
        tip = " 10 gold is a boundary: they can just afford it, so use >=." if g == 10 else ""
        fail(f"I tested `shop({g}, {h})` and typed {typed}. It should return {want}, but returned {tuple(r.ret)}.{tip}")
if ns.get("gold") != 5 or ns.get("health") != 65:
    fail(f"In the main program, after buying a potion, gold should be 5 and health 65. They're {ns.get('gold')!r} and {ns.get('health')!r}. Catch them in the same order: `gold, health = shop(gold, health)`.")
'''}

CHECKS["p4a2"] = {"defs_only": True, "win": "A fair fight that always ends.", "py": H + r'''
C.need("fight_room", 1)
won = lost = 0
for s in range(150):
    r = await C.call("fight_room", 30, seed=s)
    if not isinstance(r.ret, int):
        fail("fight_room should return the player's health." + (" Add `return health`." if r.ret is None else ""))
    if r.ret > 30:
        fail("The player's health went up during the fight.")
    if r.ret <= 0:
        lost += 1
    else:
        won += 1
if not won or not lost:
    fail("I ran lots of fights starting on 30 health. The player should sometimes win and sometimes lose. Does the loop stop when either side reaches 0?")
for s in range(60):
    r = await C.call("fight_room", 1, seed=s)
    if r.ret < 1 - 15:
        fail(f"Starting on 1 health, the player should be beaten by the goblin's first hit, but finished on {r.ret}. The fight kept going after the player reached 0. The loop needs `while health > 0 and goblin > 0:`.")
for s in range(30):
    r = await C.call("fight_room", 100, seed=s)
    if r.ret > 95:
        fail("Starting on 100, the player finished on " + str(r.ret) + ". The goblin needs at least two hits to fall, so it always hits back at least once (5 to 15).")
'''}

# ---------------- Stage 5: branching and game over ----------------
CHECKS["p5b2"] = {"inputs": ["left"], "win": "Each way leads somewhere different.", "py": H + r'''
if not has(out, "dark cave") or has(out, "freezing river"):
    fail("When I typed left, it should go into the cave only. Gap 1 is `\"left\"` and gap 2 is `cave()`.")
for typed, room, other in [("right", "freezing river", "dark cave"), ("LEFT", "dark cave", "freezing river"), ("up", "freezing river", "dark cave")]:
    r = await C.rerun([typed])
    if not has(r.out, room) or has(r.out, other):
        fail(f"When I typed {typed}, it should go to the {'river' if 'river' in room else 'cave'}. Gap 3 is `river()`.")
'''}

CHECKS["p5i1"] = {"win": "The game stops as soon as health runs out.", "py": H + r'''
C.need("trap_room", 1)
C.need("escaped", 0)
C.need("game_over", 0)
r = await C.call("trap_room", 50)
if r.ret != 30:
    fail(f"I tested `trap_room(50)`. It should return 30, but returned {r.ret!r}.")
trap_line = solid(r.out)[0] if solid(r.out) else None
win = solid((await C.call("escaped")).out)
lose = solid((await C.call("game_over")).out)
if not win or not lose or win == lose:
    fail("escaped() and game_over() should each print a different message.")
if not main_whiles():
    fail("Use a while loop in the main program, so the game can stop early.")
r = await C.rerun_vars({"health": 50})
if lose[0] not in r.out or win[0] in r.out:
    fail("Starting on 50 health, the hero doesn't survive 3 traps, so only game_over() should run.")
r = await C.rerun_vars({"health": 100})
if win[0] not in r.out or lose[0] in r.out:
    fail("I changed the start to 100 health. The hero survives 3 traps, so only escaped() should run.")
if trap_line:
    r = await C.rerun_vars({"health": 30})
    n = r.out.count(trap_line)
    if n != 2:
        fail(f"I changed the start to 30 health. After 2 traps the hero is below 0, so the game should stop. Your hero went through {n} traps. The while condition needs `and health > 0`.")
'''}

CHECKS["p5a1"] = {"defs_only": True, "win": "Rooms that choose where you go next.", "py": H + r'''
if not C.assigned("location"):
    fail("Keep the variable `location` in the main program.")
loops = main_whiles()
if not loops or not any("exit" in ast.unparse(w.test) for w in loops):
    fail("The main program should loop `while location != \"exit\":`.")
rooms = [f.name for f in C.funcs() if not f.args.args]
if len(rooms) < 2:
    fail("Write at least two room functions with no parameters.")
branching = False
for room in rooms:
    opts = (C.options_in(room) + ["zzz"]) if calls_input(room) else []
    results = set()
    if not opts:
        r = await C.call(room)
        if not isinstance(r.ret, str):
            fail(f"`{room}()` should return the name of the next room, like `return \"hall\"`.")
        continue
    for o in opts:
        try:
            r = await C.call(room, inputs=[o, o, o])
        except CheckFail:
            continue
        if not isinstance(r.ret, str):
            fail(f"I tested `{room}()` and typed {o}. It should return the name of the next room, but returned {r.ret!r}.")
        results.add(r.ret)
    if len(results) >= 2:
        branching = True
if not branching:
    fail("At least one room should offer a choice of two ways out, returning a different room name for each.")
'''}

CHECKS["p5a2"] = {"defs_only": True, "win": "Two values out, and health can end the run.", "py": H + r'''
C.need("pit", 1)
r = await C.call("pit", 100)
if not isinstance(r.ret, tuple) or len(r.ret) != 2:
    fail("pit should return two things: `return location, health`.")
loc, h = r.ret
if isinstance(loc, int) and isinstance(h, str):
    fail("pit returns health first. It should be `return location, health`.")
if h != 60 or not isinstance(loc, str):
    fail(f"I tested `pit(100)`. It should take 40 health, returning the next room and 60. It returned {r.ret!r}.")
if not any("health" in ast.unparse(w.test) for w in main_whiles()):
    fail("The main loop should also stop if health runs out: add `and health > 0` to the while.")
'''}

# ---------------- Stage 6: testing and debugging ----------------
CHECKS["p6b1"] = {"win": "All 3 bugs squashed.", "py": H + r'''
if not has(out, "Books everywhere"):
    fail("The library should run. Check the spelling and capital letters in the call: `library()`.")
if not re.search(r"Gold:\s*10\b", out):
    fail("It should print `Gold: 10`. The treasure room returns the gold, so catch it: `gold = treasure_room(gold)`.")
'''}

CHECKS["p6i1"] = {"win": "All 3 silent bugs found.", "py": H + r'''
if not has(out, "long hall"):
    fail("The hall message should appear. A call needs brackets: `hall()`.")
m = re.search(r"Health:\s*(-?\d+)", out)
got = int(m.group(1)) if m else None
if got != 70:
    if got == 80:
        fail("Health ends at 80, so the potion works but the dart doesn't. Code after return never runs, so move the damage above it.")
    if got == 50 or got == 40:
        fail(f"Health ends at {got}. `health + 30` works out the answer but doesn't store it. Write `health = health + 30`.")
    fail(f"Health should end at 70, but it's {got}.")
'''}

CHECKS["p6a1"] = {"loop_tip": "Look at what cellar() returns, and what the while loop is waiting for. Python is fussy about capital letters.", "win": "Both nasty bugs fixed.", "py": H + r'''
if not re.search(r"Gold:\s*20\s+Health:\s*75", out):
    fail("It should print `Gold: 20  Health: 75`. Catch the values in the same order shop returns them: `gold, health = shop(gold, health)`.")
if not has(out, "climb the stairs and escape"):
    fail("It should escape. Python is fussy about capitals: \"Exit\" and \"exit\" are different.")
'''}

CHECKS["p6a2"] = {"defs_only": True, "win": "A proper test plan, run in code.", "py": H + r'''
text = " ".join(C.comments()).lower()
for word, why in [("normal", "normal data"), ("boundary", "boundary data (exactly 10 gold)")]:
    if word not in text:
        fail(f"Your test plan comments should include {why}.")
if not any(w in text for w in ("refused", "erroneous", "invalid", "reject")):
    fail("Your test plan should include data that should be refused, like 9 gold and 0 gold.")
C.need("shop", 2)
if C.top_calls().count("shop") < 3:
    fail("Write code that runs each test: call shop() once for each row of your plan.")
'''}
