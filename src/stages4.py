# Content for The Heroes Dictionary (Escape the Dungeon add-on after Part 3).
# make_orig4.py turns this into base/orig4.html; build.py 4 then builds the page.

STAGES = []

# ---------------------------------------------------------------- Stage 1
STAGES.append({
 "id": "h1", "num": 1, "concept": "dictionaries: keys and values", "title": "Make your hero",
 "hook": "Health, gold, a name, a backpack. Your hero has lots of stats. Let's keep them all together in one place.",
 "learnHtml": """<p>A <strong>dictionary</strong> stores lots of values in one variable, and gives each one a label. The label is called a <strong>key</strong>. The thing stored with it is its <strong>value</strong>.</p>
<p>Make a dictionary with curly brackets. A colon joins each key to its value, and commas separate the pairs:</p>
<pre class="sample">hero = {"name": "Ash", "health": 100, "gold": 20}</pre>
<p>To get a value out, put its key in square brackets: <code>hero["health"]</code> gives <code>100</code>. Think of it as a set of labelled boxes: ask for the label, get what's inside.</p>
<p>A list finds things by position (0, 1, 2). A dictionary finds them by name, which is much easier to read.</p>""",
 "learnCode": 'hero = {"name": "Ash", "health": 100, "gold": 20}\n\nprint("Name:", hero["name"])\nprint("Health:", hero["health"])\nprint("Gold:", hero["gold"])\nprint(hero)',
 "keywords": [["dictionary", "one variable that stores values with labels, in curly brackets { }"],
              ["key", "the label you use to find a value, like \"health\""],
              ["value", "the thing stored with a key, like 100"]],
 "mistakes": ["Using square brackets to make it. A dictionary is made with curly brackets: <code>{\"gold\": 20}</code>. Square brackets are for getting a value out.",
              "Forgetting the quote marks round the key: <code>hero[health]</code>. Python looks for a variable called health. Write <code>hero[\"health\"]</code>.",
              "Spelling a key differently: <code>\"Health\"</code> and <code>\"health\"</code> are different keys. Python stops with a <code>KeyError</code>.",
              "Missing a comma between two pairs, or the colon between a key and its value."],
 "game": {"B": "If your adventure doesn't have one yet, add <code>hero = {\"health\": 100, \"gold\": 0}</code> to your main program, and print the hero's health at the start. Keep your old variables for now.",
          "I": "Add a <code>hero</code> dictionary to your main program with health, gold and a <code>\"backpack\"</code> list. Print a welcome that uses at least two of its values. Keep your old variables for now: Stage 2 swaps them over.",
          "A": "Add a <code>hero</code> dictionary holding every stat your game uses, including the backpack. Print them all at the start with a <code>for</code> loop. Keep your old variables for now: Stage 2 swaps them over."},
 "levels": {
  "B": {"intro": "Small steps, with help whenever you need it.", "parts": [
   {"id": "h1b1", "kind": "step", "title": "Run the example",
    "html": "<p>Run the example in the Learn box. Then change <code>\"Ash\"</code> to your own hero's name, and the gold to <code>50</code>. Run it again.</p>",
    "steps": ["I saw the name, health and gold", "I saw the whole dictionary at the end, in curly brackets", "I changed the name and the gold, and saw them change"]},
   {"id": "h1b2", "kind": "main", "title": "Fill the gaps: read the stats",
    "html": "<p>Gap 1 is the key for the name. Keys need quote marks. Gap 2 is the name of the dictionary. Gap 3 is the key for the gold (the quote marks are already there). When it works it should print:</p>\n<pre class=\"sample\">Hero: Brin\nHealth: 80\nGold: 15</pre>",
    "starter": 'hero = {"name": "Brin", "health": 80, "gold": 15}\n\nprint("Hero:", hero[___])\nprint("Health:", ___["health"])\nprint("Gold:", hero["___"])',
    "hints": ["Gap 1 needs the key in quote marks: \"name\"", "Gap 2 is the dictionary: hero. Gap 3 is just gold, because the quote marks are already there."]},
   {"id": "h1b3", "kind": "main", "title": "Your turn: make a monster",
    "html": "<p>Make a dictionary called <code>monster</code> with three keys: <code>\"name\"</code> is <code>\"goblin\"</code>, <code>\"health\"</code> is <code>30</code> and <code>\"damage\"</code> is <code>8</code>. The print lines are already written. When it works it should print:</p>\n<pre class=\"sample\">A goblin attacks!\nIt has 30 health.\nIt does 8 damage.</pre>",
    "steps": ["Curly brackets at the start and the end", "Three keys, each in quote marks, each with a colon and a value", "Commas between the pairs", "I ran it and saw all three lines"],
    "starter": '# Make the monster dictionary here\nmonster = ___\n\nprint("A", monster["name"], "attacks!")\nprint("It has", monster["health"], "health.")\nprint("It does", monster["damage"], "damage.")',
    "hints": ["Copy the shape of hero in the Learn box: {\"name\": ..., \"health\": ..., \"damage\": ...}", "monster = {\"name\": \"goblin\", \"health\": 30, \"damage\": 8}"]}]},
  "I": {"intro": "A short brief. Use the hints only if you need them.", "parts": [
   {"id": "h1i1", "kind": "main", "title": "The hero card",
    "html": "<p>Ask the player for their hero's name. Make a dictionary called <code>hero</code> with three keys: <code>\"name\"</code> (what they typed), <code>\"health\"</code> (100) and <code>\"gold\"</code> (20). Then print a card like this one, reading every value from the dictionary:</p>\n<pre class=\"sample\">== Ash ==\nHealth: 100\nGold: 20</pre>",
    "starter": "# ask for the name\n\n# make the hero dictionary\n\n# print the card\n",
    "hints": ["name = input(\"What is your hero called? \") then use name as a value: {\"name\": name, ...}", "print(\"==\", hero[\"name\"], \"==\") prints the top line."]},
   {"id": "h1i2", "kind": "ext", "title": "Extension: more stats",
    "html": "<p>Add two more keys to your hero: <code>\"weapon\"</code> and <code>\"backpack\"</code>. The backpack is a list, so it can start as <code>[\"torch\"]</code>. Yes, a list can live inside a dictionary! Add lines to the card that show the weapon and how many things are in the backpack.</p>",
    "starter": "", "hints": ["\"backpack\": [\"torch\"] goes inside the curly brackets, like any other pair.", "len(hero[\"backpack\"]) counts the things in the backpack."]}]},
  "A": {"intro": "A specification only. Work it out, then try the stretch.", "parts": [
   {"id": "h1a1", "kind": "main", "title": "Choose your class",
    "html": "<p>Ask for the hero's name, then their class: <code>warrior</code>, <code>mage</code> or <code>rogue</code>. If they type anything else, keep asking until they type one of the three. Make a dictionary called <code>hero</code> with the keys <code>\"name\"</code>, <code>\"class\"</code>, <code>\"health\"</code> and <code>\"attack\"</code>:</p>\n<pre class=\"sample\">warrior   health 120   attack 8\nmage      health 70    attack 14\nrogue     health 90    attack 10</pre>\n<p>Then print every key and its value with a <code>for</code> loop. <code>for key in hero:</code> goes through the keys one at a time.</p>\n<pre class=\"sample\">name: Ash\nclass: mage\nhealth: 70\nattack: 14</pre>",
    "starter": "",
    "hints": ["Make the dictionary with the name and class, then add the other two in an if/elif: hero[\"health\"] = 120", "for key in hero:\n    print(key + \":\", hero[key])"]},
   {"id": "h1a2", "kind": "stretch", "title": "Stretch: a missing key",
    "html": "<p>Add <code>print(hero[\"mana\"])</code> at the end and run it. Read the error. Now change it so it only prints the mana if the hero has some: <code>if \"mana\" in hero:</code> works on dictionaries too, and checks the keys. Then find out what <code>hero.get(\"mana\", 0)</code> does, and add a comment saying when you'd use it.</p>",
    "starter": "", "hints": ["in checks the keys of a dictionary, not the values.", "get gives back the value if the key is there, or the second thing (here 0) if it isn't."]}]}}})

# ---------------------------------------------------------------- Stage 2
STAGES.append({
 "id": "h2", "num": 2, "concept": "changing and adding values", "title": "Battle scars and loot",
 "hook": "A hero who never gets hurt and never gets rich is a bit dull. Let's change the stats as the game goes on.",
 "learnHtml": """<p>To change a value, put the key on the left of an <code>=</code>, just like a variable:</p>
<pre class="sample">hero["health"] = hero["health"] - 15</pre>
<p>Read it from right to left: take the health, subtract 15, and store the answer back under <code>"health"</code>. The shortcut <code>hero["gold"] += 10</code> adds 10 to the gold.</p>
<p>To <strong>add</strong> a new key, store a value under a key that isn't there yet: <code>hero["level"] = 2</code></p>
<p>A value can even be a list. <code>hero["backpack"].append("rope")</code> puts a rope in the backpack inside the hero.</p>""",
 "learnCode": 'hero = {"name": "Ash", "health": 100, "gold": 20, "backpack": []}\n\nprint("A rat bites you!")\nhero["health"] = hero["health"] - 15\n\nprint("You find some coins.")\nhero["gold"] += 10\n\nhero["backpack"].append("rope")\nhero["level"] = 2\n\nprint(hero)\nprint("Health:", hero["health"])',
 "keywords": [["update", "change a value: hero[\"gold\"] = hero[\"gold\"] + 5"],
              ["+= and -=", "shortcuts: hero[\"gold\"] += 5 adds 5 to the gold"],
              ["add a key", "store a value under a new key: hero[\"level\"] = 2"]],
 "mistakes": ["Doing the maths but not storing it: <code>hero[\"health\"] - 15</code> on its own changes nothing. It needs <code>hero[\"health\"] =</code> in front.",
              "Spelling the key wrong when you store: <code>hero[\"helth\"] = 50</code> doesn't change the health. It quietly adds a new key called helth. Print the hero to check.",
              "Using a separate variable: <code>health = health - 15</code> changes a variable called health, not the health inside the hero.",
              "Writing <code>hero[\"backpack\"] = \"rope\"</code>. That throws the whole backpack away and puts a word there instead. Use <code>.append(\"rope\")</code>."],
 "game": {"B": "Store the health in the hero. Where your main program says <code>health = trap_room(health)</code>, write <code>hero[\"health\"] = trap_room(hero[\"health\"])</code>. Then delete the old <code>health = 100</code> line and play-test.",
          "I": "Swap every old variable in your main program for the hero's values, like <code>hero[\"gold\"] = treasure_room(hero[\"gold\"])</code>. Then delete the old variables, and play-test to make sure nothing broke.",
          "A": "Swap every old variable for the hero's values and delete the old ones. Then add a new stat that your rooms change, like <code>\"xp\"</code> or <code>\"kills\"</code>."},
 "levels": {
  "B": {"intro": "Small steps, with help whenever you need it.", "parts": [
   {"id": "h2b1", "kind": "step", "title": "Run the example",
    "html": "<p>Run the example. Then change the rat bite so it takes <code>50</code> health, and add a line that puts a <code>\"torch\"</code> in the backpack too. Run it again.</p>",
    "steps": ["The health went from 100 to 85", "I saw 'level': 2 in the dictionary, even though it wasn't there at the start", "I changed the bite to 50 and saw 50 health left", "The torch went into the backpack"]},
   {"id": "h2b2", "kind": "main", "title": "Fill the gaps: ouch, then loot",
    "html": "<p>Gap 1: the rat bite takes 10 health. Gap 2: the key for the gold (the quote marks are already there). When it works, the last line should print:</p>\n<pre class=\"sample\">{'name': 'Brin', 'health': 90, 'gold': 5}</pre>",
    "starter": 'hero = {"name": "Brin", "health": 100, "gold": 0}\n\nprint("A rat bites you!")\nhero["health"] = hero["health"] - ___\n\nprint("You find a coin purse.")\nhero["___"] = hero["gold"] + 5\n\nprint(hero)',
    "hints": ["Gap 1 is just a number: 10", "Gap 2 is the key you're changing: gold"]},
   {"id": "h2b3", "kind": "main", "title": "Your turn: pack the backpack",
    "html": "<p>The hero starts with an empty backpack. Use <code>append</code> to add a <code>\"torch\"</code>, then a <code>\"map\"</code>. The print lines are already written. When it works it should print:</p>\n<pre class=\"sample\">Backpack: ['torch', 'map']\nYou carry 2 things.</pre>",
    "steps": ["A line with hero[\"backpack\"].append(...) for the torch", "Another line for the map", "I ran it and saw 2 things"],
    "starter": 'hero = {"name": "Brin", "health": 100, "backpack": []}\n\n# add the torch and the map here\n\n\nprint("Backpack:", hero["backpack"])\nprint("You carry", len(hero["backpack"]), "things.")',
    "hints": ["hero[\"backpack\"].append(\"torch\")", "Do the same again for the map, on its own line."]}]},
  "I": {"intro": "A short brief. Use the hints only if you need them.", "parts": [
   {"id": "h2i1", "kind": "main", "title": "The potion shop",
    "html": "<p>The hero has 30 gold. Ask <code>Buy a potion for 10 gold? </code></p>\n<ul><li>If they type <code>yes</code> and have at least 10 gold: take 10 gold, put a <code>\"potion\"</code> in the backpack, and print <code>You buy a potion.</code></li>\n<li>If they type <code>yes</code> but have less than 10 gold: print <code>You can't afford it.</code></li>\n<li>Anything else: print <code>Maybe later.</code></li></ul>\n<p>Print the hero at the end. Test all three paths: to test the second one, change the hero's starting gold.</p>",
    "starter": 'hero = {"name": "Ash", "gold": 30, "backpack": []}\n\n# ask, then if / elif / else\n\nprint(hero)\n',
    "hints": ["if answer == \"yes\" and hero[\"gold\"] >= 10:", "Take the gold with hero[\"gold\"] = hero[\"gold\"] - 10, then append the potion."]},
   {"id": "h2i2", "kind": "ext", "title": "Extension: level up",
    "html": "<p>Give a hero <code>\"xp\": 0</code> and <code>\"level\": 1</code>. Write a <code>for</code> loop that runs 5 fights, each giving the hero 30 xp. Whenever the xp reaches 100 or more, the hero goes up a level and loses 100 xp. Print the level and xp after every fight. You should finish on level 2 with 50 xp.</p>",
    "starter": "", "hints": ["for fight in range(5):", "Inside the loop: if hero[\"xp\"] >= 100:"]}]},
  "A": {"intro": "A specification only. Work it out, then try the stretch.", "parts": [
   {"id": "h2a1", "kind": "main", "title": "The merchant",
    "html": "<p>A merchant buys loot. The prices are in a second dictionary, where each key is an item and each value is its price:</p>\n<pre class=\"sample\">prices = {\"gem\": 50, \"rope\": 5, \"bone\": 1}</pre>\n<p>Start with <code>hero = {\"gold\": 10, \"backpack\": [\"gem\", \"rope\", \"sock\", \"gem\"]}</code>. Sell everything the merchant will buy: add each item's price to the hero's gold, and take it out of the backpack. Items the merchant doesn't buy (like the sock) stay in the backpack. Print each sale, then the hero. You should finish with 115 gold and <code>['sock']</code>.</p>\n<p>Make sure it still works if the prices or the backpack change.</p>",
    "starter": 'prices = {"gem": 50, "rope": 5, "bone": 1}\nhero = {"gold": 10, "backpack": ["gem", "rope", "sock", "gem"]}\n',
    "hints": ["if item in prices: checks whether the merchant buys it. prices[item] gives its price.", "Removing from a list while you loop through it skips items. Build a new list of the things to keep instead, then: hero[\"backpack\"] = keep"]},
   {"id": "h2a2", "kind": "stretch", "title": "Stretch: count the loot",
    "html": "<p>A backpack like <code>[\"gem\", \"rope\", \"gem\"]</code> is easier to read as <code>{'gem': 2, 'rope': 1}</code>. Start with an empty dictionary, <code>counts = {}</code>, and loop through the backpack. If the item is already a key, add 1 to it. If not, add it with the value 1. Print the counts. Then find out how <code>counts.get(item, 0)</code> could make your code shorter.</p>",
    "starter": "", "hints": ["if item in counts: checks the keys.", "counts[item] = 1 adds a new key."]}]}}})

# ---------------------------------------------------------------- Stage 3
STAGES.append({
 "id": "h3", "num": 3, "concept": "passing a dictionary to subroutines", "title": "One hero, every room",
 "hook": "In Part 3, a room that changed two things needed two values in and two out. With a dictionary, every room takes just one thing: the whole hero.",
 "learnHtml": """<p>Pass the whole hero into a room, change what you need, then send it back with <code>return</code>. It's the same rule you've used since Part 2: in, then back out.</p>
<pre class="sample">hero = trap_room(hero)</pre>
<p>That line never gets longer, however many stats your hero has. Compare it with Part 3: <code>inventory, gold = chest(inventory, gold)</code></p>
<p>A procedure that only shows the stats, like <code>show_status(hero)</code>, takes the hero in but doesn't need to send it back.</p>""",
 "learnCode": 'def show_status(hero):\n    print("~" * 20)\n    print("Health:", hero["health"])\n    print("Gold:", hero["gold"])\n    print("Backpack:", hero["backpack"])\n    print("~" * 20)\n\ndef trap_room(hero):\n    print("Spikes shoot from the floor!")\n    hero["health"] = hero["health"] - 10\n    return hero\n\ndef treasure_room(hero):\n    print("A chest! You take the gold and a rusty key.")\n    hero["gold"] = hero["gold"] + 25\n    hero["backpack"].append("rusty key")\n    return hero\n\nhero = {"health": 100, "gold": 0, "backpack": []}\nhero = trap_room(hero)\nhero = treasure_room(hero)\nshow_status(hero)\n\nif "rusty key" in hero["backpack"]:\n    print("You unlock the door and escape!")',
 "keywords": [["pass in", "give a subroutine a value to use: trap_room(hero)"],
              ["return", "sends a value back out of a function: return hero"],
              ["None", "what a function sends back if it has no return"]],
 "mistakes": ["Forgetting <code>return hero</code>. The room sends back <code>None</code>, so <code>hero = trap_room(hero)</code> wipes your hero out. The next line that reads a stat stops with <code>'NoneType' object is not subscriptable</code>.",
              "Making the dictionary inside a room. <code>hero = {\"health\": 100, ...}</code> in a room resets every stat each time the player walks in. Make the hero once, in the main program.",
              "Calling a room without catching the hero: <code>trap_room(hero)</code> on its own. It happens to work for dictionaries (the Advanced stretch finds out why), but keep the rule: <code>hero = trap_room(hero)</code>."],
 "game": {"B": "Pick one room in your adventure and change it to take the hero in and send it back: <code>def trap_room(hero):</code> and <code>hero = trap_room(hero)</code>.",
          "I": "Change every room to take the hero in and return it, and add a <code>show_status(hero)</code>. Every room call in your main program should now look like <code>hero = room(hero)</code>.",
          "A": "Change every room to <code>hero = room(hero)</code>, add a <code>show_status(hero)</code> with a health bar, and make your boss fight check the hero's backpack."},
 "levels": {
  "B": {"intro": "Small steps, with help whenever you need it.", "parts": [
   {"id": "h3b1", "kind": "step", "title": "Run the example",
    "html": "<p>Run the example. Then delete the line <code>return hero</code> from <code>trap_room</code> and run it again. Read the error. Put the line back.</p>",
    "steps": ["I saw the status box and escaped", "Without return hero, Python stopped with an error about NoneType", "I put return hero back and it worked again"]},
   {"id": "h3b2", "kind": "main", "title": "Fill the gaps: the treasure room",
    "html": "<p>Gap 1 sends the hero back out of the room. Gap 2 passes the hero in. When it works it should print <code>Gold: 25</code>.</p>",
    "starter": 'def treasure_room(hero):\n    print("You open a dusty chest.")\n    hero["gold"] = hero["gold"] + 25\n    return ___\n\nhero = {"health": 100, "gold": 0}\nhero = treasure_room(___)\nprint("Gold:", hero["gold"])',
    "hints": ["Both gaps are the same word.", "return hero and treasure_room(hero)"]},
   {"id": "h3b3", "kind": "main", "title": "Your turn: the spike trap",
    "html": "<p>Write <code>trap_room(hero)</code>. It prints a warning, takes 20 health away from the hero, and sends the hero back. The main program is already written. When it works it should print <code>Health: 80</code>.</p>",
    "steps": ["def trap_room(hero): with a colon", "A print line, indented", "hero[\"health\"] = hero[\"health\"] - 20", "return hero, indented, at the end"],
    "starter": '# Write trap_room(hero) here\n\n\n# main program\nhero = {"health": 100, "gold": 10}\nhero = trap_room(hero)\nprint("Health:", hero["health"])',
    "hints": ["Copy the shape of the treasure room above, or trap_room in the Learn box.", "def trap_room(hero):\n    print(\"Spikes!\")\n    hero[\"health\"] = hero[\"health\"] - 20\n    return hero"]}]},
  "I": {"intro": "A short brief. Use the hints only if you need them.", "parts": [
   {"id": "h3i1", "kind": "main", "title": "The armoury and the wishing well",
    "html": "<p>Write three subroutines. The two rooms take the hero in and return it.</p>\n<ul><li><code>show_status(hero)</code> prints the health, the gold and the backpack.</li>\n<li><code>armoury(hero)</code> puts a <code>\"sword\"</code> in the backpack.</li>\n<li><code>well(hero)</code> asks <code>Throw a coin in the well? </code> If they type <code>yes</code> and have at least 1 gold, take 1 gold and add 5 health. If they type <code>yes</code> with no gold, print <code>You have no coins.</code> Anything else: nothing happens.</li></ul>\n<p>The main program makes the hero with 90 health, 3 gold and an empty backpack, visits the armoury and the well, then shows the status.</p>",
    "starter": "# show_status(hero)\n\n# armoury(hero)\n\n# well(hero)\n\n# main program\n",
    "hints": ["Every room ends with return hero, and every call looks like hero = armoury(hero).", "In the well: if answer == \"yes\" and hero[\"gold\"] >= 1:"]},
   {"id": "h3i2", "kind": "ext", "title": "Extension: is the hero still alive?",
    "html": "<p>Write a function <code>alive(hero)</code> that returns <code>True</code> if the hero's health is above 0, and <code>False</code> if not. Use it in your main program: <code>while alive(hero):</code> keep sending the hero into a trap room until they fall. Count how many traps it took.</p>",
    "starter": "", "hints": ["return hero[\"health\"] > 0 gives back True or False on its own.", "Keep a counter, traps = 0, and add 1 every time round the loop."]}]},
  "A": {"intro": "A specification only. Work it out, then try the stretch.", "parts": [
   {"id": "h3a1", "kind": "main", "title": "The boss",
    "html": "<p>Write <code>boss(hero)</code>. The boss starts with 40 health. Each round, ask <code>attack or potion? </code></p>\n<ul><li><code>attack</code>: the boss loses 15 health if <code>\"sword\"</code> is in the hero's backpack, or 5 if not.</li>\n<li><code>potion</code>: if there's a <code>\"potion\"</code> in the backpack, use it up and add 30 health, but never go above 100. If not, print <code>You have no potion.</code></li></ul>\n<p>After the hero's move, if the boss is still standing, it hits the hero for 10. The fight ends when either health is 0 or less. If the boss loses, set <code>hero[\"boss_beaten\"] = True</code>. Return the hero.</p>\n<p>Test it: with a sword and 100 health, three attacks win with 80 health left.</p>",
    "starter": "",
    "hints": ["Keep the boss's health in a normal variable inside the function: boss_health = 40", "while hero[\"health\"] > 0 and boss_health > 0:"]},
   {"id": "h3a2", "kind": "stretch", "title": "Stretch: why does it work without return?",
    "html": "<p>Delete <code>hero = </code> from one room call in your main program, so it just says <code>trap_room(hero)</code>, and run your game. The health still changes! Now try the same with Part 2's <code>trap_room(health)</code>, which takes a number. Add a comment explaining the difference. Which style would you use in a big game, and why?</p>",
    "starter": "", "hints": ["The hero inside the room and the hero outside are the same dictionary, not a copy.", "health = health - 10 makes a new number inside the function. The one outside is untouched."]}]}}})
