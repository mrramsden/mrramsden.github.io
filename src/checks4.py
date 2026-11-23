# Checks for The Heroes Dictionary.
# Each check: inputs for the first run, optional defs_only, the test code ("py"),
# and a short "win" line shown when it passes.

CHECKS = {}

# Shared helpers, pasted in front of the tests that need them.
HELP = r'''
def shown(text):
    return " / ".join(l.strip() for l in text.split("\n") if l.strip()) or "nothing"

def get_hero(names, what="the program finished"):
    h = names.get("hero")
    if not isinstance(h, dict):
        fail("I couldn't find a dictionary called `hero` when " + what + ". Make it with curly brackets: `hero = {...}`")
    return h

def keys_read_in_prints(var):
    used = set()
    for n in ast.walk(C.tree()):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "print":
            for s in ast.walk(n):
                if (isinstance(s, ast.Subscript) and isinstance(s.value, ast.Name) and s.value.id == var
                        and isinstance(s.slice, ast.Constant)):
                    used.add(s.slice.value)
    return used
'''


# ---------------- Stage 1: make your hero ----------------
CHECKS["h1b2"] = {"win": "Every line reads its value from the dictionary.", "py": HELP + r'''
for want in ("Hero: Brin", "Health: 80", "Gold: 15"):
    if not has(out, want):
        fail("It should print `" + want + "`. It printed: " + shown(out))
r = await C.rerun_vars({"hero": {"name": "Zed", "health": 5, "gold": 99}})
if not (has(r.out, "Hero: Zed") and has(r.out, "Health: 5") and has(r.out, "Gold: 99")):
    fail("I changed the hero to Zed, with 5 health and 99 gold, but it printed: " + shown(r.out) + ". Every line should read from the dictionary, like `hero[\"name\"]`, instead of typing the value in.")
'''}

CHECKS["h1b3"] = {"win": "Your monster dictionary has all three keys, with the right values.", "py": HELP + r'''
m = ns.get("monster")
if not isinstance(m, dict):
    fail("`monster` should be a dictionary, made with curly brackets { }.")
for k, v in (("name", "goblin"), ("health", 30), ("damage", 8)):
    got = m[k]
    if got == v and type(got) == type(v):
        continue
    if isinstance(v, int) and str(got).strip() == str(v):
        fail("The " + k + " should be the number " + str(v) + ", without quote marks, so the game can do maths with it.")
    fail("The " + k + " should be " + repr(v) + ", but your monster has " + repr(got) + ".")
for want in ("A goblin attacks!", "It has 30 health.", "It does 8 damage."):
    if not has(out, want):
        fail("It should print `" + want + "`. It printed: " + shown(out))
'''}

CHECKS["h1i1"] = {"inputs": ["Ash"], "win": "Your hero card reads everything from the dictionary.", "py": HELP + r'''
h = get_hero(ns, "I typed Ash")
for k in ("name", "health", "gold"):
    if k not in h:
        fail("Your hero needs a key called \"" + k + "\". It has: " + (", ".join(repr(x) for x in h) or "no keys") + ".")
if h["name"] != "Ash":
    if isinstance(h["name"], str) and h["name"].strip().lower() in ("name", "input", "hero"):
        fail("When I typed Ash, the hero's name came out as `" + h["name"] + "`. Take the quote marks off that value, so Python uses the variable holding what was typed.")
    fail("When I typed Ash, the hero's name should be Ash, but it's " + repr(h["name"]) + ".")
if h["health"] != 100 or h["gold"] != 20:
    fail("The hero should start with 100 health and 20 gold, as numbers without quote marks. Yours has " + repr(h["health"]) + " and " + repr(h["gold"]) + ".")
for want in ("== Ash ==", "Health: 100", "Gold: 20"):
    if not has(out, want):
        fail("When I typed Ash, the card should include `" + want + "`. It printed: " + shown(out))
used = keys_read_in_prints("hero")
missing = [k for k in ("name", "health", "gold") if k not in used]
if missing:
    fail("The card should read every value from the dictionary. Use `hero[\"" + missing[0] + "\"]` in the print line, instead of another variable or typing the value in.")
r = await C.rerun(["Zed"])
if not has(r.out, "== Zed =="):
    fail("When I typed Zed, the top of the card should say `== Zed ==`. It printed: " + shown(r.out))
'''}

CHECKS["h1a1"] = {"defs_only": True, "win": "All three classes work, it keeps asking until it gets one, and the for loop prints every stat.", "py": HELP + r'''
TABLE = {"warrior": (120, 8), "mage": (70, 14), "rogue": (90, 10)}

def line_for(text, k, v):
    return re.search(r"(?im)^\s*" + re.escape(str(k)) + r"\s*:?\s+" + re.escape(str(v)) + r"\s*$", text)

async def try_class(typed, cls):
    said = "Ash, then " + ", then ".join(typed)
    try:
        r = await C.rerun(["Ash"] + typed)
    except CheckFail as e:
        if "more answers" in str(e):
            fail("I typed " + said + ", but it asked for more answers than that. Ask for the name first, then the class, and stop asking once the class is warrior, mage or rogue.")
        raise
    if len(typed) > 1 and r.used < 1 + len(typed):
        fail("I typed " + said + ". " + typed[0] + " isn't a class, so it should keep asking until it gets warrior, mage or rogue, then make a " + cls + ".")
    h = get_hero(r.ns, "I typed " + said)
    for k in ("name", "class", "health", "attack"):
        if k not in h:
            fail("I typed " + said + ". The hero should have a key called \"" + k + "\", but it only has: " + (", ".join(repr(x) for x in h) or "no keys") + ".")
    if h["name"] != "Ash":
        fail("I typed " + said + ". The hero's name should be Ash, but it's " + repr(h["name"]) + ". Ask for the name first, then the class.")
    if h["class"] != cls:
        fail("I typed " + said + ". The hero's class should be " + cls + ", but it's " + repr(h["class"]) + ".")
    hp, at = TABLE[cls]
    if h["health"] != hp or h["attack"] != at:
        fail("I typed " + said + ". A " + cls + " should have " + str(hp) + " health and " + str(at) + " attack, but your hero has " + repr(h["health"]) + " health and " + repr(h["attack"]) + " attack.")
    for k in h:
        if not line_for(r.out, k, h[k]):
            fail("I typed " + said + ". Each stat should print on its own line, like `" + str(k) + ": " + str(h[k]) + "`. It printed: " + shown(r.out))

for cls in ("warrior", "mage", "rogue"):
    await try_class([cls], cls)
await try_class(["wizard", "rogue"], "rogue")
await try_class(["dragon", "elf", "warrior"], "warrior")
if C.count(ast.For) == 0:
    fail("The stats print correctly, but use a `for` loop to print them: `for key in hero:` goes through every key.")
'''}


# ---------------- Stage 2: battle scars and loot ----------------
CHECKS["h2b2"] = {"win": "The health and the gold both changed inside the hero.", "py": HELP + r'''
h = get_hero(ns)
want = {"name": "Brin", "health": 90, "gold": 5}
extra = [k for k in h if k not in want]
if extra:
    fail("Your hero has a new key called `" + str(extra[0]) + "`. Gap 2 should be exactly `gold`, in lower case, so it changes the gold that's already there.")
if h.get("health") != 90:
    fail("After the rat bite, the health should be 90, but it's " + repr(h.get("health")) + ". Gap 1 is how much health to take away: 10.")
if h != want:
    fail("The hero should end up as " + repr(want) + ", but it's " + repr(h) + ".")
'''}

CHECKS["h2b3"] = {"win": "The torch and the map are in the backpack, in order.", "py": HELP + r'''
h = get_hero(ns)
bp = h.get("backpack")
if not isinstance(bp, list):
    fail("The backpack isn't a list any more: it's " + repr(bp) + ". Add to it with `hero[\"backpack\"].append(\"torch\")`, not with `=`.")
if bp != ["torch", "map"]:
    if sorted(bp) == ["map", "torch"]:
        fail("Both things are in the backpack, but the wrong way round. Add the torch first, then the map.")
    fail("The backpack should end up as ['torch', 'map'], but it's " + repr(bp) + ".")
n = sum(1 for x in ast.walk(C.tree()) if isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute) and x.func.attr == "append")
if n < 2:
    fail("The backpack has the right things, but use `append` twice to add them, and leave the backpack starting empty.")
if not has(out, "You carry 2 things"):
    fail("The last line should say `You carry 2 things.` It printed: " + shown(out))
'''}

CHECKS["h2i1"] = {"inputs": ["yes"], "win": "All three paths work, including exactly 10 gold.", "py": HELP + r'''
def state(h):
    return repr(h.get("gold")) + " gold and the backpack " + repr(h.get("backpack"))

h = get_hero(ns, "I typed yes")
if h.get("gold") != 20 or h.get("backpack") != ["potion"]:
    fail("I typed yes with 30 gold. The hero should finish with 20 gold and ['potion'], but has " + state(h) + ".")
if not has(out, "You buy a potion"):
    fail("I typed yes with 30 gold. It should print `You buy a potion.` It printed: " + shown(out))
for typed in ("no", "maybe"):
    r = await C.rerun([typed])
    h = get_hero(r.ns, "I typed " + typed)
    if h.get("gold") != 30 or h.get("backpack") != []:
        fail("I typed " + typed + ". Nothing should change, but the hero finished with " + state(h) + ".")
    if not has(r.out, "Maybe later"):
        fail("I typed " + typed + ". It should print `Maybe later.` It printed: " + shown(r.out))
r = await C.rerun_vars({"hero": {"name": "Ash", "gold": 10, "backpack": []}}, ["yes"])
h = get_hero(r.ns, "I typed yes with 10 gold")
if h.get("gold") != 0 or h.get("backpack") != ["potion"]:
    fail("I set the gold to exactly 10 and typed yes. That's enough, so they should buy it, but the hero finished with " + state(h) + ". That's an edge: check whether you need >= or >.")
r = await C.rerun_vars({"hero": {"name": "Ash", "gold": 9, "backpack": []}}, ["yes"])
h = get_hero(r.ns, "I typed yes with 9 gold")
if h.get("gold") != 9 or h.get("backpack") != []:
    fail("I set the gold to 9 and typed yes. They can't afford it, so nothing should change, but the hero finished with " + state(h) + ".")
if not has(r.out, "can't afford"):
    fail("I set the gold to 9 and typed yes. It should print `You can't afford it.` It printed: " + shown(r.out))
'''}

CHECKS["h2a1"] = {"win": "It sells by the price list, keeps what the merchant won't buy, and never skips an item.", "py": HELP + r'''
DEFAULT = {"gem": 50, "rope": 5, "bone": 1}

async def sell(gold, bag, prices=None):
    vals = {"hero": {"gold": gold, "backpack": list(bag)}}
    if prices is not None:
        vals["prices"] = prices
    p = prices if prices is not None else DEFAULT
    r = await C.rerun_vars(vals)
    h = get_hero(r.ns)
    want_gold = gold + sum(p[i] for i in bag if i in p)
    want_bag = [i for i in bag if i not in p]
    if h.get("gold") != want_gold or h.get("backpack") != want_bag:
        said = "I started the hero with " + str(gold) + " gold and the backpack " + repr(list(bag))
        if prices is not None:
            said += ", and changed the prices to " + repr(prices)
        msg = said + ". It should finish with " + str(want_gold) + " gold and " + repr(want_bag) + ", but finished with " + repr(h.get("gold")) + " gold and " + repr(h.get("backpack")) + "."
        if isinstance(h.get("gold"), int) and h.get("gold") < want_gold:
            msg += " Some items were skipped. Removing from a list while you loop through it skips the next item: build a new list of things to keep instead."
        elif prices is not None and h.get("gold") != want_gold:
            msg += " Use the prices dictionary, like `prices[item]`, instead of typing prices into your code."
        fail(msg)

if not ("prices" in ns and isinstance(ns["prices"], dict)):
    fail("Keep the price list as a dictionary called `prices`.")
await sell(10, ["gem", "rope", "sock", "gem"])
await sell(0, ["gem", "gem", "gem", "bone"])
await sell(3, ["apple", "gem", "rope"], {"gem": 7, "apple": 2})
await sell(5, [])
'''}


# ---------------- Stage 3: one hero, every room ----------------
CHECKS["h3b2"] = {"win": "The hero goes into the room and comes back out richer.", "py": HELP + r'''
C.need("treasure_room", 1)
r = await C.call("treasure_room", {"health": 50, "gold": 7})
if r.ret is None:
    fail("I tested `treasure_room` and nothing came back. Gap 1 should send the hero back: `return hero`.")
if not isinstance(r.ret, dict) or r.ret.get("gold") != 32 or r.ret.get("health") != 50:
    fail("I sent in a hero with 50 health and 7 gold. It should come back with 50 health and 32 gold, but came back as " + repr(r.ret) + ".")
if not has(out, "Gold: 25"):
    fail("The main program should print `Gold: 25`. It printed: " + shown(out))
'''}

CHECKS["h3b3"] = {"win": "Your trap takes 20 health from whichever hero walks in, and sends the hero back.", "py": HELP + r'''
C.need("trap_room", 1)
r = await C.call("trap_room", {"health": 50, "gold": 3})
if r.ret is None:
    fail("I tested `trap_room` and nothing came back, so the hero turns into None. Add `return hero` as the last line of trap_room, indented.")
h = r.ret
if not isinstance(h, dict):
    fail("trap_room should send back the hero dictionary, but it sent back " + repr(h) + ". End it with `return hero`.")
if h.get("gold") != 3:
    fail("I sent in a hero with 3 gold, and it came back with " + repr(h.get("gold")) + ". It looks like trap_room makes a new hero. Change the hero that was passed in instead, or every stat resets.")
if h.get("health") == 80:
    fail("I sent in a hero with 50 health, and it came back with 80. trap_room should take 20 from whatever health the hero has: `hero[\"health\"] = hero[\"health\"] - 20`")
if h.get("health") != 30:
    fail("I sent in a hero with 50 health. It should come back with 30, but came back with " + repr(h.get("health")) + ".")
if not r.out.strip():
    fail("The health works. Now add a print line so the player knows they walked into a trap.")
if not has(out, "Health: 80"):
    fail("The main program should print `Health: 80`. It printed: " + shown(out))
'''}

CHECKS["h3i1"] = {"inputs": ["yes"], "win": "Both rooms take the hero in and send it back, and the well handles every case.", "py": HELP + r'''
for name in ("show_status", "armoury", "well"):
    C.need(name, 1)

def back(r, name):
    if r.ret is None:
        fail("I tested `" + name + "` and nothing came back. End it with `return hero`.")
    if not isinstance(r.ret, dict):
        fail("`" + name + "` should send back the hero dictionary, but sent back " + repr(r.ret) + ".")
    return r.ret

h = back(await C.call("armoury", {"health": 50, "gold": 0, "backpack": ["torch"]}), "armoury")
if h.get("backpack") != ["torch", "sword"]:
    fail("I sent a hero with ['torch'] into the armoury. The backpack should come back as ['torch', 'sword'], but came back as " + repr(h.get("backpack")) + ".")

async def well(gold, typed, want_gold, want_health, note=""):
    r = await C.call("well", {"health": 90, "gold": gold, "backpack": []}, inputs=[typed])
    h = back(r, "well")
    if h.get("gold") != want_gold or h.get("health") != want_health:
        fail("I sent a hero with 90 health and " + str(gold) + " gold to the well and typed " + typed + ". It should come back with " + str(want_health) + " health and " + str(want_gold) + " gold, but came back with " + repr(h.get("health")) + " health and " + repr(h.get("gold")) + " gold." + note)
    return r

await well(3, "yes", 2, 95)
await well(1, "yes", 0, 95, " That's an edge: 1 gold is enough. Check whether you need >= or >.")
r = await well(0, "yes", 0, 90)
if not has(r.out, "no coins"):
    fail("I sent a hero with 0 gold to the well and typed yes. It should print `You have no coins.` It printed: " + shown(r.out))
await well(3, "no", 3, 90)

r = await C.call("show_status", {"health": 42, "gold": 7, "backpack": ["gem"]})
for want in ("42", "7", "gem"):
    if want not in r.out:
        fail("I tested `show_status` with 42 health, 7 gold and ['gem'] in the backpack. It should show all three, but printed: " + shown(r.out))
if not (has(out, "95") and has(out, "sword")):
    fail("When I typed yes, the main program's status should show 95 health and the sword. It printed: " + shown(out) + ". Check the main program makes the hero with 90 health, 3 gold and an empty backpack, then visits both rooms.")
'''}

CHECKS["h3a1"] = {"defs_only": True, "win": "The boss fight works for swords, potions, the 100 cap, and losing.", "py": HELP + r'''
C.need("boss", 1)

async def fight(hero, moves, label, early=""):
    said = "I sent in " + label + " and typed " + ", ".join(moves)
    try:
        r = await C.call("boss", hero, inputs=moves)
    except CheckFail as e:
        if "kept asking" in str(e):
            fail(said + ". By then the fight should be over, but it kept asking. Stop the loop as soon as either health is 0 or less.")
        raise
    if r.ret is None:
        fail("`boss` didn't send anything back. Add `return hero` at the end, outside the loop.")
    if not isinstance(r.ret, dict):
        fail("`boss` should send back the hero dictionary, but sent back " + repr(r.ret) + ".")
    if r.used < len(moves):
        fail(said + ", but the fight ended after " + str(r.used) + " move" + ("" if r.used == 1 else "s") + ". It should only end when the boss or the hero is on 0 health or less." + early)
    return r, r.ret, said

r, h, said = await fight({"health": 100, "backpack": ["sword"]}, ["attack"] * 3, "a hero with 100 health and a sword")
if h.get("health") != 80:
    tip = " Once the boss is on 0 or less, it shouldn't hit back." if h.get("health") == 70 else ""
    fail(said + ". The boss should hit back twice, leaving 80 health, but the hero has " + repr(h.get("health")) + "." + tip)
if h.get("boss_beaten") is not True:
    fail("The boss was beaten, so set `hero[\"boss_beaten\"] = True` before you return the hero.")

r, h, said = await fight({"health": 100, "backpack": []}, ["attack"] * 8, "a hero with 100 health and no sword", " Without a sword each attack does 5, so the boss lasts 8 attacks.")
if h.get("health") != 30 or h.get("boss_beaten") is not True:
    fail(said + ". Without a sword each attack does 5, so it takes 8 attacks, and the hero should finish on 30 health with the boss beaten. The hero finished as " + repr(h) + ".")

r, h, said = await fight({"health": 50, "backpack": ["sword", "potion"]}, ["potion", "attack", "attack", "attack"], "a hero with 50 health, a sword and a potion")
if h.get("backpack") != ["sword"]:
    fail(said + ". The potion should be used up, leaving ['sword'], but the backpack is " + repr(h.get("backpack")) + ".")
if h.get("health") != 50:
    fail(said + ". The potion takes them to 80, then the boss hits back three times, so they should finish on 50 health, but finished on " + repr(h.get("health")) + ".")

r, h, said = await fight({"health": 90, "backpack": ["sword", "potion"]}, ["potion", "attack", "attack", "attack"], "a hero with 90 health, a sword and a potion")
if h.get("health") != 70:
    tip = " The potion took the health above 100. Cap it: if it goes over 100, set it back to 100." if h.get("health") == 90 else ""
    fail(said + ". The potion should stop at 100, then three hits leave 70, but they finished on " + repr(h.get("health")) + "." + tip)

r, h, said = await fight({"health": 100, "backpack": ["sword"]}, ["potion", "attack", "attack", "attack"], "a hero with a sword but no potion")
if not has(r.out, "no potion"):
    fail(said + ". It should print `You have no potion.` It printed: " + shown(r.out))
if h.get("health") != 70:
    fail(said + ". The boss still hits back after the wasted turn, so they should finish on 70 health, but finished on " + repr(h.get("health")) + ".")

r, h, said = await fight({"health": 15, "backpack": []}, ["attack", "attack"], "a hero with 15 health and no sword")
if h.get("health", 1) > 0:
    fail(said + ". Two hits from the boss should take them to -5, but they finished on " + repr(h.get("health")) + ".")
if h.get("boss_beaten") is True:
    fail(said + ". The hero lost, so `boss_beaten` shouldn't be True.")
'''}
