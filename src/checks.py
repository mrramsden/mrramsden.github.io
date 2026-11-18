# Checks for Escape the Dungeon Part 3.
# Each check: inputs for the first run, optional seed / defs_only, the test code ("py"),
# and a short "win" line shown when it passes.

CHECKS = {}

# Used by the ask tests: turns "it kept asking" into a specific message.
ASK_HELP = r'''
async def expect(name, args, typed, want, stuck):
    try:
        r = await C.call(name, *args, inputs=typed)
    except CheckFail as e:
        if "kept asking" in str(e):
            fail("I tested `" + name + "` and typed " + ", ".join(repr(t) for t in typed) + ". " + stuck)
        raise
    return r
'''


# ---------------- Stage 1: show your stats ----------------
CHECKS["q1b2"] = {"inputs": ["Ash"], "win": "Your procedure takes the name in and uses it.", "py": r'''
C.need("welcome", 1)
if has(out, "dungeon, name") or has(out, "luck, hero"):
    fail("It printed the word `name` or `hero` instead of the hero's name. Take the quote marks away so Python uses the variable.")
if not has(out, "Welcome to the dungeon, Ash"):
    fail("When I typed Ash, it should print `Welcome to the dungeon, Ash`. It printed: " + " / ".join(C.out.strip().split("\n")[1:]) )
r = await C.call("welcome", "Zed")
if not has(r.out, "Welcome to the dungeon, Zed"):
    fail("I tested `welcome('Zed')` and it didn't say Zed. Gap 1 should be the parameter, `name`.")
'''}

CHECKS["q1b3"] = {"win": "Both status boxes work, with the values in the right order.", "py": r'''
C.need("show_status", 2)
r = await C.call("show_status", 77, 3)
m77 = re.search(r"(?<!\d)77(?!\d)", r.out)
m3 = re.search(r"(?<!\d)3(?!\d)", r.out)
if not m77 or not m3:
    fail("I tested `show_status(77, 3)`. It should print 77 for health and 3 for gold, but it printed: " + (" / ".join(l for l in r.out.split("\n") if l.strip()) or "nothing"))
if m3.start() < m77.start():
    fail("I tested `show_status(77, 3)` and the gold came out before the health. Print health first, then gold.")
if not (has(out, "100") and has(out, "35")):
    fail("The main program should show two boxes: 100 and 10, then 60 and 35. Check you haven't changed the main program.")
'''}

CHECKS["q1i1"] = {"inputs": ["Ash"], "win": "The card and the trap both work, and the trap sends health back.", "py": r'''
C.need("trap_room", 1)
C.need("show_hero", 3)
r = await C.call("trap_room", 100)
if r.ret is None:
    fail("I tested `trap_room(100)` and nothing came back. Add `return health` at the end of trap_room.")
if r.ret != 75:
    fail(f"I tested `trap_room(100)`. It should return 75, but it returned {r.ret!r}.")
r = await C.call("trap_room", 30)
if r.ret != 5:
    fail(f"I tested `trap_room(30)`. It should return 5, but it returned {r.ret!r}. Use the parameter, not a fixed number.")
r = await C.call("show_hero", "Zed", 55, 7)
if not has(r.out, "== Zed =="):
    fail("I tested `show_hero('Zed', 55, 7)`. The first line should be `== Zed ==`. It printed: " + (r.out.strip().split("\n")[0] if r.out.strip() else "nothing"))
if not has(r.out, "Health: 55") or not has(r.out, "Gold: 7"):
    fail("I tested `show_hero('Zed', 55, 7)`. It should show `Health: 55` and `Gold: 7`. Check the order of the parameters.")
if not has(out, "Health: 100") or not has(out, "Health: 75"):
    fail("The main program should show the card with 100 health, visit the trap, then show the card with 75 health. Did you catch the result: `health = trap_room(health)`?")
if norm(out).count("gold: 20") < 2:
    fail("The card should show `Gold: 20` both times.")
'''}

CHECKS["q1i2"] = {"win": "One procedure, any size, any symbol.", "py": r'''
C.need("divider", 2)
r = await C.call("divider", 5, "*")
if "*****" not in r.out or "******" in r.out:
    fail("I tested `divider(5, '*')`. It should print exactly 5 stars: `*****`. It printed: " + (r.out.strip() or "nothing"))
r = await C.call("divider", 3, "~")
if r.out.strip() != "~~~":
    fail("I tested `divider(3, '~')`. It should print `~~~`. Check the order: length first, then symbol.")
if "~" * 30 not in out or "*" * 10 not in out:
    fail("Call it twice in your program: `divider(30, '~')` and `divider(10, '*')`.")
'''}

CHECKS["q1a1"] = {"defs_only": True, "win": "The bar is right for every value, including 0 and negative health.", "py": r'''
C.need("show_bar", 1)
for h, bar, shown in [(100, "##########", 100), (70, "#######---", 70), (45, "####------", 45),
                      (75, "#######---", 75), (99, "#########-", 99), (5, "----------", 5), (0, "----------", 0), (-20, "----------", 0)]:
    r = await C.call("show_bar", h)
    m = re.search(r"\[(.*)\]\s*(-?\d+)", r.out)
    if not m:
        fail(f"I tested `show_bar({h})`. It should print `Health [{bar}] {shown}`, but it printed: " + (r.out.strip() or "nothing"))
    if m.group(1) != bar or int(m.group(2)) != shown:
        extra = " Below 0 should show as an empty bar and 0." if h < 0 else " Use // 10 to count the tens, rounded down." if h in (45, 5, 75, 99) else ""
        fail(f"I tested `show_bar({h})`. It should print `Health [{bar}] {shown}`, but it printed `{r.out.strip()}`.{extra}")
'''}

CHECKS["q1a2"] = {"defs_only": True, "win": "Default values work, and the bar stays 10 long.", "py": r'''
f = C.need("show_bar")
import inspect
ps = list(inspect.signature(f).parameters.values())
if len(ps) != 2 or ps[1].default != 100:
    fail("The def should be `def show_bar(health, max_health=100):`")
r = await C.call("show_bar", 45)
if "[####------]" not in r.out:
    fail("I tested `show_bar(45)`. With no second value it should still draw `[####------]`.")
r = await C.call("show_bar", 45, 60)
m = re.search(r"\[(.*)\]", r.out)
if not m or len(m.group(1)) != 10 or m.group(1).count("#") not in (7, 8):
    fail("I tested `show_bar(45, 60)`. The bar should still be 10 characters, with about 7 #, because 45 is three quarters of 60. It printed: " + (r.out.strip() or "nothing"))
r = await C.call("show_bar", 60, 60)
if "[##########]" not in r.out:
    fail("I tested `show_bar(60, 60)`. Full health should give a full bar `[##########]`.")
if not C.comments():
    fail("Nearly there. Add a comment (a line starting with #) explaining what `=100` does.")
'''}

# ---------------- Stage 2: roll the dice ----------------
CHECKS["q2b2"] = {"win": "Every roll is from 1 to 6, and both 1 and 6 can come up.", "py": r'''
seen = set()
for s in range(80):
    r = await C.rerun(seed=s)
    roll = r.ns.get("roll")
    if not isinstance(roll, int):
        fail("Keep the variable `roll`, storing a random whole number.")
    if roll < 1 or roll > 6:
        fail(f"I ran it lots of times and once rolled a {roll}. A dice only goes from 1 to 6: `random.randint(1, 6)`.")
    seen.add(roll)
if seen != {1, 2, 3, 4, 5, 6}:
    fail("I ran it lots of times but never got " + ", ".join(str(n) for n in sorted({1,2,3,4,5,6} - seen)) + ". Check both numbers in randint.")
'''}

CHECKS["q2b3"] = {"win": "The chest gives 5 to 20 gold, and every amount in between can happen.", "py": r'''
C.need("treasure_room", 1)
got = set()
for s in range(300):
    r = await C.call("treasure_room", 0, seed=s)
    if r.ret is None:
        fail("treasure_room sent nothing back. Keep `return gold` at the end.")
    if not isinstance(r.ret, int):
        fail("The gold should be a whole number. Use `random.randint`, which gives whole numbers.")
    if r.ret < 5 or r.ret > 20:
        fail(f"I opened the chest lots of times and once got {r.ret} gold. It should only give 5 to 20.")
    got.add(r.ret)
if min(got) != 5 or max(got) != 20:
    fail(f"I opened the chest lots of times and got from {min(got)} to {max(got)} gold. It should go from 5 to 20.")
'''}

CHECKS["q2i1"] = {"seed": 3, "win": "About 1 in 4 dodges, and the damage is always 5 to 25.", "py": r'''
C.need("trap_room", 1)
results = []
for s in range(400):
    r = await C.call("trap_room", 100, seed=s)
    if r.ret is None:
        fail("trap_room sent nothing back. Add `return health` at the end.")
    results.append(r.ret)
hurt = [100 - x for x in results if x != 100]
dodges = results.count(100)
bad = [d for d in hurt if d < 5 or d > 25]
if bad:
    fail(f"I ran the trap lots of times and once it took {bad[0]} health. It should take 5 to 25.")
if not hurt:
    fail("In all my tests the player always dodged. Only a 1 should dodge.")
if dodges == 0:
    fail("Even when the player dodges, they still lose health. Put the damage inside an else, so it only happens when they don't dodge.")
if dodges < 50 or dodges > 160:
    pct = round(dodges / 4)
    fail(f"The player dodged {pct}% of the time. It should be about 25% (a 1 out of 1 to 4).")
if min(hurt) != 5 or max(hurt) != 25:
    fail(f"The damage went from {min(hurt)} to {max(hurt)}. It should be able to be anything from 5 to 25.")
if not re.search(r"\d", out):
    fail("The trap works. Now make the main program print the health at the end.")
'''}

CHECKS["q2i2"] = {"defs_only": True, "win": "Random monsters from your list, and 5 to 15 damage.", "py": r'''
C.need("encounter", 1)
if not C.calls("choice", inside="encounter"):
    fail("Use `random.choice` to pick the monster from your list.")
names = [s for s in C.strings_in("encounter")]
got = []
for s in range(200):
    r = await C.call("encounter", 100, seed=s)
    if r.ret is None:
        fail("encounter sent nothing back. Add `return health` at the end.")
    got.append(100 - r.ret)
if min(got) < 5 or max(got) > 15:
    fail(f"The fight took between {min(got)} and {max(got)} health. It should be 5 to 15.")
if min(got) != 5 or max(got) != 15:
    fail(f"The damage went from {min(got)} to {max(got)}. It should be able to be anything from 5 to 15.")
'''}

CHECKS["q2a1"] = {"defs_only": True, "win": "Attacks, defence, halving and the end of the fight all work.", "py": r'''
C.need("fight", 1)
for s in range(40):
    r = await C.call("fight", 100, inputs=["attack"] * 40, seed=s)
    if not isinstance(r.ret, int):
        fail("fight should return the player's health as a whole number." + (" It returned nothing: add `return health`." if r.ret is None else ""))
    if r.ret > 96:
        fail(f"I attacked every round and finished on {r.ret} health. A goblin with 30 health needs at least two hits, so it always hits back at least once (4 to 12).")
    if r.ret < 100 - 12 * 6:
        fail(f"I attacked every round and finished on {r.ret} health. That's more damage than the goblin can do before it falls.")
    if r.used > 6:
        fail(f"I attacked every round, but the fight took {r.used} rounds. Attacks do 5 to 15, so a 30-health goblin falls in 6 rounds at most. Is the goblin's health going down?")
long = 0
for s in range(10):
    r = await C.call("fight", 100, inputs=["defend"] * 200, seed=s)
    if r.ret is None or r.ret > 0:
        fail("I defended every round. The goblin never takes damage, so the fight should only end when the player reaches 0 or less.")
    long = max(long, r.used)
    if r.used < 17:
        fail(f"I defended every round and lost after only {r.used} rounds. Defending should halve the goblin's hit with //, so it takes at least 17 rounds.")
'''}

CHECKS["q2a2"] = {"defs_only": True, "win": "Seeded dice, with a comment explaining why.", "py": r'''
if not re.search(r"random\.seed\(", C.src):
    fail("Add `random.seed(1)` on the line after `import random`.")
if not C.comments():
    fail("Add a comment explaining why a tester might use seed, and why it must come out before release.")
'''}

# ---------------- Stage 3: the backpack ----------------
CHECKS["q3b2"] = {"win": "The map is in, the count is 3, and the loop lists every item.", "py": r'''
bag = ns.get("bag")
if bag != ["torch", "bread", "map"]:
    fail(f"The bag should end up as `['torch', 'bread', 'map']`, but it's `{bag!r}`. Gap 1 is `append`.")
if not has(out, "You have 3 items"):
    fail("It should say `You have 3 items:`. Gap 2 is `len`.")
for item in ["torch", "bread", "map"]:
    if not any(l.strip() == item for l in out.split("\n")):
        fail(f"Each item should be printed on its own line, but I couldn't find `{item}`. Gap 3 is the list, `bag`.")
'''}

CHECKS["q3b3"] = {"win": "The sword and shield go into whichever bag you pass in.", "py": r'''
C.need("armoury", 1)
r = await C.call("armoury", ["torch"])
if r.ret is None:
    fail("I tested `armoury(['torch'])` and nothing came back. The last line should be `return inventory`.")
if r.ret != ["torch", "sword", "shield"]:
    fail(f"I tested `armoury(['torch'])`. It should return `['torch', 'sword', 'shield']`, but it returned `{r.ret!r}`. Use `inventory.append(...)` twice.")
r = await C.call("armoury", ["apple", "rope"])
if r.ret != ["apple", "rope", "sword", "shield"]:
    fail(f"I tested `armoury(['apple', 'rope'])`. It should return `['apple', 'rope', 'sword', 'shield']`, but it returned `{r.ret!r}`. Add to the list that comes in, don't make a new one.")
'''}

CHECKS["q3i1"] = {"win": "Picking up and showing the bag both work, including an empty bag.", "py": r'''
C.need("pick_up", 2)
C.need("show_bag", 1)
r = await C.call("pick_up", [], "rope")
if r.ret is None:
    fail("I tested `pick_up([], 'rope')` and nothing came back. Add `return inventory`.")
if r.ret != ["rope"]:
    fail(f"I tested `pick_up([], 'rope')`. It should return `['rope']`, but it returned `{r.ret!r}`.")
r = await C.call("pick_up", ["torch"], "map")
if r.ret != ["torch", "map"]:
    fail(f"I tested `pick_up(['torch'], 'map')`. It should return `['torch', 'map']`, but it returned `{r.ret!r}`.")
r = await C.call("show_bag", [])
if not has(r.out, "Your bag is empty"):
    fail("I tested `show_bag([])`. It should print `Your bag is empty.`")
r = await C.call("show_bag", ["rope", "lantern", "apple"])
if has(r.out, "empty"):
    fail("I tested `show_bag` with 3 items and it still said the bag was empty. Only say that when `len(inventory) == 0`.")
want = ["1. rope", "2. lantern", "3. apple"]
lines = [norm(l) for l in r.out.split("\n") if l.strip()]
if [norm(w) for w in want] != lines:
    fail("I tested `show_bag(['rope', 'lantern', 'apple'])`. It should print `1. rope`, `2. lantern`, `3. apple` on separate lines. It printed: " + " / ".join(r.out.strip().split("\n")))
if not has(out, "Your bag is empty") or not has(out, "1."):
    fail("Your subroutines work. Now the main program: show the empty bag, pick up two items, then show it again.")
'''}

CHECKS["q3i2"] = {"defs_only": True, "win": "The bag stops at 4 items.", "py": r'''
C.need("pick_up", 2)
r = await C.call("pick_up", ["a", "b", "c"], "d")
if r.ret != ["a", "b", "c", "d"]:
    fail("I tested picking up a 4th item. It should still fit, giving 4 items.")
if has(r.out, "full"):
    fail("I picked up a 4th item and it said the bag was full. 4 items should fit.")
r = await C.call("pick_up", ["a", "b", "c", "d"], "e")
if r.ret is None:
    fail("When the bag is full, pick_up should still return the inventory.")
if len(r.ret) != 4:
    fail(f"I picked up a 5th item and the bag now has {len(r.ret)}. It should stay at 4.")
if not has(r.out, "Your bag is full"):
    fail("I picked up a 5th item. It should print `Your bag is full!`")
'''}

CHECKS["q3a1"] = {"defs_only": True, "win": "Every kind of loot works, and both values come back.", "py": r'''
C.need("chest", 2)
kinds = set(); gains = []
for s in range(300):
    r = await C.call("chest", ["torch"], 10, seed=s)
    if not isinstance(r.ret, tuple) or len(r.ret) != 2:
        fail("chest should return two things: `return inventory, gold`.")
    inv, gold = r.ret
    if isinstance(inv, int) and isinstance(gold, list):
        fail("chest returns the two values the wrong way round. It should be `return inventory, gold`.")
    if gold != 10:
        if inv != ["torch"]:
            fail("When the loot is gold, the bag shouldn't change.")
        gains.append(gold - 10); kinds.add("gold")
    elif inv == ["torch"]:
        kinds.add("nothing")
        if not r.out.strip():
            fail("When the chest has nothing, print a sad message.")
    else:
        new = inv[1:]
        if inv[0] != "torch" or len(new) != 1 or new[0] not in ("potion", "key"):
            fail(f"Opening one chest changed the bag from `['torch']` to `{inv!r}`. Only a potion or a key should be added.")
        kinds.add(new[0])
missing = {"gold", "potion", "key", "nothing"} - kinds
if missing:
    fail("I opened lots of chests but never got: " + ", ".join(sorted(missing)) + ". Check your list of loot.")
if min(gains) < 5 or max(gains) > 20 or min(gains) != 5 or max(gains) != 20:
    fail(f"Gold chests gave {min(gains)} to {max(gains)} gold. They should give 5 to 20.")
'''}

CHECKS["q3a2"] = {"defs_only": True, "win": "Each item once, with its count.", "py": r'''
C.need("show_bag", 1)
r = await C.call("show_bag", ["potion", "key", "potion"])
text = norm(r.out)
if not re.search(r"potion\s*x\s*2", text) or not re.search(r"key\s*x\s*1", text):
    fail("I tested `show_bag(['potion', 'key', 'potion'])`. It should show `potion x2` and `key x1`. It printed: " + " / ".join(r.out.strip().split("\n")))
if text.count("potion") != 1:
    fail("Potion appears more than once. Each item should only be printed once. Keep a list of items you've already shown.")
'''}

# ---------------- Stage 4: locked doors ----------------
CHECKS["q4b2"] = {"win": "With a rope you get across.", "py": r'''
C.need("bridge", 1)
if not has(out, "You tie your rope across"):
    fail("The player should get across. Gap 1 is `in`, and gap 2 is `\"rope\"` with quote marks.")
r = await C.call("bridge", ["torch"])
if not has(r.out, "another way"):
    fail("I tested the bridge with no rope, and the player still got across. Gap 1 should be `in`.")
'''}

CHECKS["q4b3"] = {"win": "The troll takes the bread, and roars when there isn't any.", "py": r'''
C.need("troll", 1)
r = await C.call("troll", ["torch", "bread"])
if r.ret is None:
    fail("Keep `return inventory` as the last line of troll.")
if "bread" in r.ret:
    fail("I tested the troll with bread. The bread should be removed: `inventory.remove(\"bread\")`.")
if r.ret != ["torch"]:
    fail(f"I tested the troll with `['torch', 'bread']`. The bag should end as `['torch']`, but it was `{r.ret!r}`.")
with_bread = r.out
r = await C.call("troll", ["torch"])
if r.ret != ["torch"]:
    fail("Without bread, the bag shouldn't change.")
if norm(r.out) == norm(with_bread):
    fail("The troll says the same thing with and without bread. Add an else that makes the troll roar.")
'''}

CHECKS["q4i1"] = {"defs_only": True, "win": "One key at most, and the door uses it up.", "py": r'''
C.need("cell", 1)
C.need("door", 1)
r = await C.call("cell", [])
if r.ret != ["key"]:
    fail(f"I tested `cell([])`. The player should find a key, giving `['key']`, but it returned `{r.ret!r}`.")
r = await C.call("cell", ["key"])
if r.ret != ["key"]:
    fail(f"I tested `cell(['key'])`. They already have a key, so they shouldn't get another. It returned `{r.ret!r}`.")
r = await C.call("door", ["torch", "key"])
if r.ret != ["torch"]:
    fail(f"I tested `door(['torch', 'key'])`. The door should open and use up the key, leaving `['torch']`. It returned `{r.ret!r}`.")
opened = r.out
r = await C.call("door", ["torch"])
if r.ret != ["torch"]:
    fail("I tested the door with no key. The bag shouldn't change.")
if norm(r.out) == norm(opened):
    fail("The door says the same thing with and without a key. Tell the player it's locked when there's no key.")
'''}

CHECKS["q4i2"] = {"defs_only": True, "win": "Items you have get used up; items you don't are refused.", "py": r'''
C.need("use_item", 1)
r = await C.call("use_item", ["rope", "apple"], inputs=["apple"])
if r.ret != ["rope"]:
    fail(f"I typed apple with `['rope', 'apple']` in the bag. The apple should be removed, leaving `['rope']`. It returned `{r.ret!r}`.")
if not has(r.out, "You use the apple"):
    fail("When I used the apple it should say `You use the apple`.")
r = await C.call("use_item", ["rope"], inputs=["sword"])
if r.ret != ["rope"]:
    fail("I typed sword, which isn't in the bag. The bag shouldn't change.")
if not re.search(r"don.?t have", norm(r.out)):
    fail("I typed sword, which isn't in the bag. It should say `You don't have that`.")
'''}

CHECKS["q4a1"] = {"defs_only": True, "win": "Potions get used up, and health never goes over 100.", "py": r'''
C.need("drink", 2)
tests = [((["potion", "potion"], 50), (["potion"], 80)),
         ((["potion"], 80), ([], 100)),
         ((["torch", "potion"], 95), (["torch"], 100)),
         ((["torch"], 40), (["torch"], 40)),
         (([], 100), ([], 100))]
for args, want in tests:
    r = await C.call("drink", *args)
    if not isinstance(r.ret, tuple) or len(r.ret) != 2:
        fail("drink should send two things back: `return inventory, health`.")
    if isinstance(r.ret[0], int) and isinstance(r.ret[1], list):
        fail("drink returns the two values the wrong way round. It should be `return inventory, health`.")
    if tuple(r.ret) != want:
        extra = " Health should never go above 100." if want[1] == 100 and isinstance(r.ret[1], int) and r.ret[1] > 100 else ""
        fail(f"I tested `drink{args!r}`. It should return `{want!r}`, but it returned `{tuple(r.ret)!r}`.{extra}")
'''}

# ---------------- Stage 5: write it once ----------------
CHECKS["q5b2"] = {"inputs": ["maybe", "yes"], "win": "ask sends the answer back, and silly answers are refused.", "py": r'''
C.need("ask", 2)
r = await C.call("ask", "Open the door? ", ["yes", "no"], inputs=["banana", " YES "])
if r.ret is None:
    fail("ask sent nothing back. Gap 1 is `answer`, so it says `return answer`.")
if r.ret != "yes":
    fail(f"I typed banana, then YES. ask should return `'yes'`, but it returned `{r.ret!r}`.")
if not has(out, "creaks open"):
    fail("When I typed yes, the door should creak open. Gaps 2 and 3 are `\"yes\"` and `\"no\"`, with quote marks.")
r = await C.rerun(["no"])
if not has(r.out, "walk away"):
    fail("When I typed no, you should walk away.")
'''}

CHECKS["q5b3"] = {"inputs": ["up", "touch"], "win": "Both rooms use ask, and each answer does something different.", "py": r'''
for room in ("well", "statue"):
    C.need(room, 0)
    if not C.calls("ask", inside=room):
        fail(f"The {room} room should use `ask(...)` to ask its question.")
if C.used != 2:
    fail(f"Each room should ask one question with ask. I answered {C.used} question(s).")
a = await C.rerun(["up", "touch"])
b = await C.rerun(["down", "leave"])
c = await C.rerun(["sideways", "UP", "run", " Leave "])
ws = [norm(x.out.split("stares at you")[0]) for x in (a, b)]
ss = [norm(x.out.split("stares at you")[-1]) for x in (a, b)]
if ws[0] == ws[1]:
    fail("The well does the same thing for up and down. Use if and else on the answer.")
if ss[0] == ss[1]:
    fail("The statue does the same thing for touch and leave. Use if and else on the answer.")
'''}

CHECKS["q5i1"] = {"defs_only": True, "win": "Your ask copes with capitals, spaces and rubbish, and three rooms use it.", "py": ASK_HELP + r'''
C.need("ask", 2)
r = await expect("ask", ("Which way? ", ["left", "right"]), ["  LEFT "], "left", "It should accept that as left, but it kept asking. Use `.strip().lower()` on the answer.")
if r.ret != "left":
    fail(f"I typed `  LEFT ` (capitals and spaces). ask should return `'left'`, but it returned `{r.ret!r}`. Use .strip().lower().")
r = await C.call("ask", "Which way? ", ["left", "right"], inputs=["up", "banana", "Right"])
if r.ret != "right":
    fail(f"I typed up, banana, then Right. ask should keep asking and return `'right'`, but it returned `{r.ret!r}`.")
if r.used != 3:
    fail("ask should keep asking until it gets one of the options.")
ast_funcs = [n for n in ast.walk(C.tree()) if isinstance(n, ast.FunctionDef)]
rooms = [n.name for n in ast_funcs if n.name != "ask" and C.calls("ask", inside=n.name)]
if len(rooms) < 3:
    fail(f"ask works. Now write three rooms that each use it. I found {len(rooms)}" + (": " + ", ".join(rooms) if rooms else "") + ".")
'''}

CHECKS["q5i2"] = {"defs_only": True, "win": "ask_number only accepts whole numbers in range, and never crashes.", "py": ASK_HELP + r'''
C.need("ask_number", 3)
for typed, low, high, want in [(["3"], 0, 5, 3), (["5"], 0, 5, 5), (["0"], 0, 5, 0),
                               (["9", "4"], 0, 5, 4), (["ten", "2"], 0, 5, 2), (["", "1"], 0, 5, 1)]:
    r = await expect("ask_number", ("How many? ", low, high), typed, want,
                     f"It should accept {want}, because it's from {low} to {high}, but it kept asking." + (" Check the boundaries: use <= so the end numbers count." if want in (low, high) else ""))
    if r.ret != want or not isinstance(r.ret, int):
        fail(f"I tested `ask_number('How many? ', {low}, {high})` and typed " + ", ".join(repr(t) for t in typed) + f". It should return the number {want}, but it returned `{r.ret!r}`.")
'''}

CHECKS["q5a1"] = {"defs_only": True, "win": "Full words, first letters, capitals and rubbish all handled.", "py": r'''
C.need("ask", 2)
opts = ["left", "right"]
for typed, want in [(["l"], "left"), ([" R "], "right"), (["LEFT"], "left"), (["right"], "right"),
                    (["x", "banana", "left"], "left"), (["", "r"], "right")]:
    r = await C.call("ask", "Which way? ", opts, inputs=typed)
    if r.ret != want:
        tip = " A blank answer should be refused, not crash or count as an option." if "" in typed else ""
        fail("I typed " + ", ".join(repr(t) for t in typed) + f". ask should return `{want!r}`, but it returned `{r.ret!r}`.{tip}")
'''}

CHECKS["q5a2"] = {"defs_only": True, "win": "Rock solid: no input can crash it.", "py": ASK_HELP + r'''
C.need("ask_number", 3)
for typed, low, high, want in [(["", "ten", "2.5", "9", "4"], 1, 5, 4), (["1"], 1, 5, 1), (["5"], 1, 5, 5),
                               (["0", "6", "3"], 1, 5, 3), (["-3"], -5, 5, -3), ([" 2 "], 1, 5, 2)]:
    r = await expect("ask_number", ("Number? ", low, high), typed, want,
                     f"It should accept {want}, but it kept asking." + (" Negative numbers can be valid when low is below 0. `isdigit()` says no to a minus sign, so try int() inside try/except." if want < 0 else " Check the boundaries: use <= so the end numbers count." if want in (low, high) else ""))
    if r.ret != want or not isinstance(r.ret, int):
        tip = " Negative numbers can be valid when low is below 0. Try int() inside try/except." if want == -3 else ""
        fail(f"I tested `ask_number('Number? ', {low}, {high})` and typed " + ", ".join(repr(t) for t in typed) + f". It should return {want}, but it returned `{r.ret!r}`.{tip}")
text = " ".join(C.comments()).lower()
for word in ("normal", "boundary", "erroneous"):
    if word not in text:
        fail(f"ask_number works. Now add your test plan as comments, including a {word} test.")
'''}

# ---------------- Stage 6: the boss room ----------------
CHECKS["q6b2"] = {"win": "The bite is 5 to 15, and the shield halves it.", "py": r'''
C.need("spider", 2)
with_s, without = set(), set()
for s in range(200):
    r = await C.call("spider", 30, ["torch", "shield"], seed=s)
    if r.ret is None:
        fail("spider sent nothing back. Gap 4 is `health`, so it says `return health`.")
    with_s.add(30 - r.ret)
    r = await C.call("spider", 30, ["torch"], seed=s)
    without.add(30 - r.ret)
if max(without) <= 7:
    fail("The bite is halved even without a shield. Gap 3 should be `\"shield\"`, with quote marks.")
if min(without) != 5 or max(without) != 15:
    fail(f"Without a shield the bite took {min(without)} to {max(without)} health. It should be 5 to 15.")
if max(with_s) > 7:
    fail("With a shield, the bite should be halved. Gap 3 is `\"shield\"`, with quote marks.")
'''}

BOSS_HELPERS = r'''
async def try_boss(health, inv, moves, seed, rounds=200):
    seq = (moves * rounds)[:rounds]
    return await C.call("boss", health, inv, inputs=seq, seed=seed)
'''

CHECKS["q6i1"] = {"defs_only": True, "win": "Your boss uses ask, random damage and a helpful item, and the fight always ends.", "py": BOSS_HELPERS + r'''
C.need("ask", 2)
C.need("boss", 2)
if not C.calls("ask", inside="boss"):
    fail("The boss should use `ask(...)` for the player's moves.")
if not C.calls("randint", inside="boss") and not C.calls("choice", inside="boss"):
    fail("The boss should use random damage, like `random.randint(5, 15)`.")
moves = [m for m in C.options_in("boss")]
items = C.items_checked_in("boss")
if not moves:
    fail("I couldn't find the moves in your boss. Give ask a list, like `ask('Attack or block? ', ['attack', 'block'])`.")
if not items:
    fail("The boss should check for an item, like `if \"sword\" in inventory:`.")
ends = set()
for s in range(6):
    r = await try_boss(100, [], moves, s)
    if not isinstance(r.ret, int):
        fail("boss should return the player's health." + (" Add `return health` at the end." if r.ret is None else ""))
    ends.add(r.ret > 0)
helped = False
for plan in [moves] + [[m] for m in moves]:
    total_with = total_without = 0
    for s in range(16):
        total_with += (await try_boss(100, [items[0]], plan, s)).ret
        total_without += (await try_boss(100, [], plan, s)).ret
    if total_with > total_without:
        helped = True
        break
if not helped:
    fail(f"I fought the boss with and without `{items[0]}` lots of times, and it didn't help the player. Make the item lower the damage or raise the player's hits.")
'''}

CHECKS["q6a1"] = {"defs_only": True, "win": "Three moves, potions used up, and the sword makes a difference.", "py": BOSS_HELPERS + r'''
C.need("boss", 2)
moves = C.options_in("boss")
drink = [m for m in moves if "drink" in m or "potion" in m or "heal" in m]
hit = [m for m in moves if "attack" in m or "hit" in m or "strike" in m or "fight" in m]
if len(moves) < 3:
    fail("Each round the player should have three moves: attack, shield, or drink a potion. I found: " + (", ".join(moves) or "none") + ".")
if not drink or not hit:
    fail("I couldn't find an attack move and a drink (or potion) move in your boss.")
for s in range(5):
    r = await try_boss(100, ["sword"], hit, s)
    if not isinstance(r.ret, tuple) or len(r.ret) != 2:
        fail("boss should return two things: `return inventory, health`.")
    if isinstance(r.ret[0], int) and isinstance(r.ret[1], list):
        fail("boss returns the two values the wrong way round. It should be `return inventory, health`.")
r = await try_boss(60, ["potion", "sword"], [drink[0]] + hit, 1)
if "potion" in r.ret[0]:
    fail("I drank the potion in the first round, but it was still in the bag afterwards. Use it up with `remove`.")
r = await try_boss(60, ["sword"], [drink[0]] + hit, 1)   # drinking with no potion must not crash
s_with = s_without = 0
for s in range(20):
    s_with += (await try_boss(100, ["sword"], hit, s)).ret[1]
    s_without += (await try_boss(100, [], hit, s)).ret[1]
if s_with <= s_without:
    fail("I fought lots of times with and without a sword, and the sword didn't help. A sword should add damage.")
'''}

CHECKS["q6a2"] = {"defs_only": True, "win": "A repeatable test plan.", "py": r'''
text = " ".join(C.comments()).lower()
for word in ("normal", "boundary", "erroneous"):
    if word not in text:
        fail(f"Your test table (as comments) should include a {word} test.")
if not re.search(r"random\.seed\(", C.src):
    fail("Use `random.seed(...)` so your tests give the same numbers every time.")
'''}
