# Makes base/orig4.html (The Heroes Dictionary) from base/orig3.html and the content in stages4.py.
# Run it after changing stages4.py, then run:  python3 build.py 4
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stages4 import STAGES

src = open(os.path.join(HERE, "base", "orig3.html"), encoding="utf-8").read()


def jsdump(obj):
    return json.dumps(obj, ensure_ascii=False).replace("<", "\\u003c")


def rep(old, new, count=1):
    global src
    n = src.count(old)
    assert n == count, (n, old[:90])
    src = src.replace(old, new)


# ---------- title, brand, storage ----------
rep("<title>Escape the Dungeon Part 3: Loot and legends</title>", "<title>The Heroes Dictionary: Escape the Dungeon</title>")
rep("Escape the Dungeon <small>Part 3: loot and legends</small>", "Escape the Dungeon <small>The Heroes Dictionary</small>")
rep('const KEY = "escapeTheDungeonPart3.v1";', 'const KEY = "escapeTheDungeonHeroes.v1";')
rep('const FILE_APP = "escapeTheDungeonPart3";', 'const FILE_APP = "escapeTheDungeonHeroes";')
rep("a.download = `Escape the Dungeon Part 3 progress ${stamp}.json`;", "a.download = `Heroes Dictionary progress ${stamp}.json`;")

# ---------- stages ----------
m = re.search(r"^const STAGES = .*;$", src, re.M)
assert m
src = src[:m.start()] + "const STAGES = " + jsdump(STAGES) + ";" + src[m.end():]

# ---------- loading files: bring a Part 3 (or Part 2) adventure across ----------
rep("""    if (data && data.app === "escapeTheDungeonPython") { toast('That\\'s your Part 1 file. Pick a file that starts "Escape the Dungeon Part 3 progress", or your newest Part 2 file to bring your adventure across.', true); return; }
    if (data && data.app === "escapeTheDungeonPart2") { importPart2(data.state); return; }""",
    """    if (data && data.app === "escapeTheDungeonPython") { toast('That\\'s your Part 1 file. Pick a file that starts "Heroes Dictionary progress", or your newest Part 3 file to bring your adventure across.', true); return; }
    if (data && data.app === "escapeTheDungeonPart3") { importAdventure(data.state, "Part 3"); return; }
    if (data && data.app === "escapeTheDungeonPart2") { importAdventure(data.state, "Part 2"); return; }""")
rep("""/* bring a Part 2 adventure (code and plan) into Part 3, without overwriting Part 3 work */
function importPart2(st){
  if (!st || typeof st !== "object") { toast("That Part 2 file couldn't be read. Check you picked the right one.", true); return; }""",
    """/* bring a Part 3 (or Part 2) adventure (code and plan) across, without overwriting work done here */
function importAdventure(st, from){
  if (!st || typeof st !== "object") { toast("That " + from + " file couldn't be read. Check you picked the right one.", true); return; }""")
rep("""  if (p2 && hasOwn && cur !== p2) { toast("You already have a Part 3 adventure on this computer, so it wasn't replaced. To start again from your Part 2 game, use Reset my progress on the Finish page first.", true); return; }""",
    """  if (p2 && hasOwn && cur !== p2) { toast("You already have an adventure in this page on this computer, so it wasn't replaced. To start again from your " + from + " game, use Reset my progress on the Finish page first.", true); return; }""")
rep("""  toast(p2 ? "Your Part 2 adventure has come across. It's in the My adventure box on every stage. Press Save progress at the end of the lesson to keep a Part 3 file."
           : "Your Part 2 plan has come across, but there was no adventure code in that file. Start your game in the My adventure box.");""",
    """  toast(p2 ? "Your " + from + " adventure has come across. It's in the My adventure box on every stage. Press Save progress at the end of the lesson to keep a Heroes Dictionary file."
           : "Your " + from + " plan has come across, but there was no adventure code in that file. Start your game in the My adventure box.");""")

m = re.search(r'^const GAME_STARTER = ".*";$', src, re.M)
assert m
src = src[:m.start()] + "const GAME_STARTER = " + json.dumps(
    "# My adventure\n# Tip: press Load progress and pick your Part 3 file to bring your game across.\nimport random\n\n"
    "# 1. Define your rooms here (def ...)\n\n\n# 2. Main program\nhero = {\"health\": 100, \"gold\": 0, \"backpack\": []}\n") + ";" + src[m.end():]
rep("No plan here yet. Press Load progress and pick your newest Part 2 file to bring your plan and your adventure across.",
    "No plan here yet. Press Load progress and pick your newest Part 3 file to bring your plan and your adventure across.")

# ---------- welcome ----------
rep("""    <h1>Escape the Dungeon: Part 3</h1>
    <p>Your adventure is about to get bigger. Dice that make every game different, a backpack full of loot, locked doors that need the right key, and a boss to beat at the end.</p></div></section>
  <div class="card gamecard"><h2 class="sec">${IC.map} Bring your Part 2 adventure</h2>
    <p>Press <strong>Load progress</strong> at the top and pick your newest file that starts <strong>Escape the Dungeon Part 2 progress</strong>. Your adventure code and your plan come across, and you keep building the same game.</p>
    <p>No Part 2 file? No problem. Start a new adventure in the box at the bottom of each stage.</p></div>""",
    """    <h1>The Heroes Dictionary</h1>
    <p>Your hero has health, gold and a backpack, and the list keeps growing. This short add-on to Part 3 keeps every stat in one place: a dictionary. Three stages, one lesson.</p></div></section>
  <div class="card gamecard"><h2 class="sec">${IC.map} Bring your Part 3 adventure</h2>
    <p>Press <strong>Load progress</strong> at the top and pick your newest file that starts <strong>Escape the Dungeon Part 3 progress</strong>. Your adventure code and your plan come across, and by the end of the lesson your whole game runs on one hero dictionary.</p>
    <p>No Part 3 file? No problem. Start a new adventure in the box at the bottom of each stage.</p></div>""")
m = re.search(r'<span class="d">Add random traps.*?</span></button>', src)
assert m
src = src[:m.start()] + '<span class="d">Make a hero, change its stats, and write a room that takes the hero in. Worked examples, fill-the-gap code, tick lists and plenty of hints.</span></button>' + src[m.end():]
m = re.search(r'<span class="d">Add a backpack, items.*?</span></button>', src)
assert m
src = src[:m.start()] + '<span class="d">A hero card, a potion shop, and rooms that share one hero. Short briefs, hints if you need them, plus extensions.</span></button>' + src[m.end():]
m = re.search(r'<span class="d">Random loot, potions.*?</span></button>', src)
assert m
src = src[:m.start()] + '<span class="d">Hero classes, a merchant with a price list, and a boss fight that uses the backpack. Specifications only, and stretch tasks beyond the lesson.</span></button>' + src[m.end():]

# ---------- finish ----------
rep("""<section class="hero">${IC.door}<div><h1>Legend complete?</h1>
    <p>Your adventure now has luck, loot, locked doors and a boss, all built from subroutines you can reuse. Download it from the box below so you have a copy, and hand it in if you've been asked to.</p></div></section>""",
    """<section class="hero">${IC.door}<div><h1>Hero complete?</h1>
    <p>Your hero now keeps every stat in one dictionary, and every room takes the hero in and sends it back. Download your adventure from the box below so you have a copy, and hand it in if you've been asked to.</p></div></section>""")
m = re.search(r'      "I can write a subroutine with more than one parameter.*?\]\.map\(\(s, i\)', src, re.S)
assert m
src = src[:m.start()] + """      "I can make a dictionary with keys and values, and read a value using its key",
      "I can explain the difference between a key and a value",
      "I can change a value, add a new key, and add to a list inside a dictionary",
      "I can pass a dictionary into a subroutine and send it back with return",
      "I can explain why hero = room(hero) is better than passing lots of separate values"].map((s, i)""" + src[m.end():]

# ---------- reference panel: add dictionaries ----------
DICT_REFS = [
 {"id": "dict", "part": 4, "cat": "Dictionaries", "title": "dictionaries { }", "short": "values with labels",
  "keys": ["dictionary", "dict", "key", "value", "{", "curly", "hero"],
  "syntax": 'hero = {"name": "Ash", "health": 100}\nhero["health"]',
  "html": "<p>A dictionary stores values with labels, called <strong>keys</strong>. Make it with curly brackets, with a colon between each key and its value and commas between the pairs. Get a value out with its key in square brackets.</p>",
  "example": 'hero = {"name": "Ash", "health": 100, "gold": 20}\nprint(hero["name"], "has", hero["gold"], "gold")',
  "watch": "Keys need quote marks, and must match exactly: <code>\"Gold\"</code> and <code>\"gold\"</code> are different keys."},
 {"id": "dictchange", "part": 4, "cat": "Dictionaries", "title": "change or add a value", "short": "update the hero",
  "keys": ["change", "update", "add", "+=", "-=", "new key"],
  "syntax": 'hero["gold"] = hero["gold"] + 5\nhero["gold"] += 5\nhero["level"] = 2',
  "html": "<p>Put the key on the left of <code>=</code> to store a new value. If the key isn't there yet, it's added. A list inside a dictionary works like any list: <code>hero[\"backpack\"].append(\"rope\")</code></p>",
  "example": 'hero = {"health": 100, "backpack": []}\nhero["health"] = hero["health"] - 15\nhero["backpack"].append("rope")\nhero["level"] = 2\nprint(hero)',
  "watch": "A misspelt key doesn't give an error when you store: <code>hero[\"helth\"] = 50</code> quietly adds a new key."},
 {"id": "dictloop", "part": 4, "cat": "Dictionaries", "title": "for key in hero", "short": "loop through a dictionary",
  "keys": ["for key", "loop", "every key", "get", "in"],
  "syntax": 'for key in hero:\n    print(key, hero[key])\nif "mana" in hero:',
  "html": "<p>A <code>for</code> loop over a dictionary gives you each key in turn. Use <code>hero[key]</code> to get its value. <code>in</code> checks whether a key is there.</p>",
  "example": 'hero = {"name": "Ash", "health": 100, "gold": 20}\nfor key in hero:\n    print(key + ":", hero[key])\nif "mana" not in hero:\n    print("No mana yet.")'},
 {"id": "dictpass", "part": 4, "cat": "Dictionaries", "title": "hero = room(hero)", "short": "pass the hero into a room",
  "keys": ["pass", "room", "return hero", "subroutine", "none", "subscriptable"],
  "syntax": 'def trap_room(hero):\n    hero["health"] = hero["health"] - 10\n    return hero\n\nhero = trap_room(hero)',
  "html": "<p>Pass the whole hero in, change what you need, then send it back with <code>return hero</code>. However many stats the hero has, the call stays the same length.</p>",
  "example": 'def trap_room(hero):\n    print("Spikes!")\n    hero["health"] = hero["health"] - 10\n    return hero\n\nhero = {"health": 100}\nhero = trap_room(hero)\nprint(hero["health"])',
  "watch": "Forget <code>return hero</code> and the room sends back None, so the next line stops with <code>'NoneType' object is not subscriptable</code>."},
]
line_start = src.index("const REF_ALL = [")
line_end = src.index("\n", line_start)
line = src[line_start:line_end]
dec = json.JSONDecoder()
refs, end = dec.raw_decode(line, line.index("["))
err_at = next(i for i, r in enumerate(refs) if r["id"] == "errors")
refs = refs[:err_at] + DICT_REFS + refs[err_at:]
rest = line[end:]
rest = rest.replace('"Lists", "Fixing errors"]', '"Lists", "Dictionaries", "Fixing errors"]')
rest = re.sub(r"REF_STAGES = \{.*?\}, REF_ERR", 'REF_STAGES = ' + json.dumps({
    "h1": ["dict", "dictloop", "strings"], "h2": ["dictchange", "dict", "lists"], "h3": ["dictpass", "return", "in"]}) + ", REF_ERR", rest)
rest = rest.replace('["NoneType", "return"]', '["KeyError", "dict"], ["indices must be integers or slices, not str", "dict"], ["not subscriptable", "dictpass"], ["NoneType", "return"]')
rest = rest.replace("REF_PART = 3;", "REF_PART = 4;")
for need in ('"Dictionaries", "Fixing errors"', '"h1":', '"KeyError", "dict"', "REF_PART = 4;"):
    assert need in rest, need
src = src[:line_start] + "const REF_ALL = " + jsdump(refs) + rest + src[line_end:]

open(os.path.join(HERE, "base", "orig4.html"), "w", encoding="utf-8").write(src)
print("wrote base/orig4.html", len(src))
