# Model answers (must pass) and typical mistakes (must fail with a helpful message) for The Heroes Dictionary.
GOOD, BAD = {}, {}

# ---------------- h1b2 ----------------
GOOD["h1b2"] = ['''hero = {"name": "Brin", "health": 80, "gold": 15}

print("Hero:", hero["name"])
print("Health:", hero["health"])
print("Gold:", hero["gold"])''']
BAD["h1b2"] = [('''hero = {"name": "Brin", "health": 80, "gold": 15}

print("Hero:", hero[name])
print("Health:", hero["health"])
print("Gold:", hero["gold"])''', "put it in quotes"),
('''hero = {"name": "Brin", "health": 80, "gold": 15}

print("Hero:", "Brin")
print("Health:", hero["health"])
print("Gold:", hero["gold"])''', "I changed the hero to Zed"),
('''hero = {"name": "Brin", "health": 80, "gold": 15}

print("Hero:", hero["name"])
print("Health:", hero["health"])
print("Gold:", hero["Gold"])''', "couldn't find the key 'Gold'")]

# ---------------- h1b3 ----------------
GOOD["h1b3"] = ['''# Make the monster dictionary here
monster = {"name": "goblin", "health": 30, "damage": 8}

print("A", monster["name"], "attacks!")
print("It has", monster["health"], "health.")
print("It does", monster["damage"], "damage.")''', '''monster = {"damage": 8, "health": 30, "name": "goblin"}
print("A", monster["name"], "attacks!")
print("It has", monster["health"], "health.")
print("It does", monster["damage"], "damage.")''']
BAD["h1b3"] = [('''monster = ["goblin", 30, 8]
print("A", monster["name"], "attacks!")
print("It has", monster["health"], "health.")
print("It does", monster["damage"], "damage.")''', "make a dictionary with curly brackets"),
('''monster = {"goblin", 30, 8}
print("A", monster["name"], "attacks!")
print("It has", monster["health"], "health.")
print("It does", monster["damage"], "damage.")''', "values but no keys"),
('''monster = {"name": "goblin", "health": "30", "damage": 8}
print("A", monster["name"], "attacks!")
print("It has", monster["health"], "health.")
print("It does", monster["damage"], "damage.")''', "the number 30, without quote marks"),
('''monster = {"name": "goblin", "health": 30, "Damage": 8}
print("A", monster["name"], "attacks!")
print("It has", monster["health"], "health.")
print("It does", monster["damage"], "damage.")''', "couldn't find the key 'damage'"),
('''monster = {"name": "orc", "health": 30, "damage": 8}
print("A", monster["name"], "attacks!")
print("It has", monster["health"], "health.")
print("It does", monster["damage"], "damage.")''', "should be 'goblin'")]

# ---------------- h1i1 ----------------
GOOD["h1i1"] = ['''name = input("What is your hero called? ")
hero = {"name": name, "health": 100, "gold": 20}
print("==", hero["name"], "==")
print("Health:", hero["health"])
print("Gold:", hero["gold"])''', '''hero = {"name": input("Name? "), "health": 100, "gold": 20}
print(f"== {hero['name']} ==")
print("Health: " + str(hero["health"]))
print("Gold: " + str(hero["gold"]))
''']
BAD["h1i1"] = [('''name = input("What is your hero called? ")
hero = {"name": "name", "health": 100, "gold": 20}
print("==", hero["name"], "==")
print("Health:", hero["health"])
print("Gold:", hero["gold"])''', "Take the quote marks off"),
('''name = input("What is your hero called? ")
hero = {"name": name, "health": 100, "gold": 20}
print("==", name, "==")
print("Health:", hero["health"])
print("Gold:", hero["gold"])''', 'hero["name"]'),
('''name = input("What is your hero called? ")
hero = {"name": name, "health": 100, "gold": 20}
print("==", hero["name"], "==")
print("Health: 100")
print("Gold:", hero["gold"])''', 'hero["health"]'),
('''name = input("What is your hero called? ")
hero = {"name": name, "health": 100}
print("==", hero["name"], "==")
print("Health:", hero["health"])''', 'key called "gold"'),
('''name = input("What is your hero called? ")
hero = {"name": name, "health": 100, "gold": 20}
print(hero["name"])
print("Health:", hero["health"])
print("Gold:", hero["gold"])''', "== Ash ==")]

# ---------------- h1a1 ----------------
GOOD["h1a1"] = ['''name = input("Name? ")
choice = input("Class? ")
while choice not in ["warrior", "mage", "rogue"]:
    choice = input("Warrior, mage or rogue? ")
hero = {"name": name, "class": choice}
if choice == "warrior":
    hero["health"] = 120
    hero["attack"] = 8
elif choice == "mage":
    hero["health"] = 70
    hero["attack"] = 14
else:
    hero["health"] = 90
    hero["attack"] = 10
for key in hero:
    print(key + ":", hero[key])''', '''STATS = {"warrior": [120, 8], "mage": [70, 14], "rogue": [90, 10]}
name = input("Name? ")
job = ""
while job not in STATS:
    job = input("Class? ").strip().lower()
hero = {"name": name, "class": job, "health": STATS[job][0], "attack": STATS[job][1]}
for key in hero:
    print(key, ":", hero[key])''']
BAD["h1a1"] = [('''name = input("Name? ")
choice = input("Class? ")
hero = {"name": name, "class": choice}
if choice == "warrior":
    hero["health"] = 120
    hero["attack"] = 8
elif choice == "mage":
    hero["health"] = 70
    hero["attack"] = 14
else:
    hero["health"] = 90
    hero["attack"] = 10
for key in hero:
    print(key + ":", hero[key])''', "keep asking"),
('''name = input("Name? ")
choice = input("Class? ")
while choice not in ["warrior", "mage", "rogue"]:
    choice = input("Warrior, mage or rogue? ")
hero = {"name": name, "class": choice}
if choice == "warrior":
    hero["health"] = 120
    hero["attack"] = 8
elif choice == "mage":
    hero["health"] = 70
    hero["attack"] = 10
else:
    hero["health"] = 90
    hero["attack"] = 14
for key in hero:
    print(key + ":", hero[key])''', "A mage should have 70 health and 14 attack"),
('''name = input("Name? ")
choice = input("Class? ")
while choice not in ["warrior", "mage", "rogue"]:
    choice = input("Warrior, mage or rogue? ")
hero = {"name": name, "class": choice}
if choice == "warrior":
    hero["health"] = 120
    hero["attack"] = 8
elif choice == "mage":
    hero["health"] = 70
    hero["attack"] = 14
else:
    hero["health"] = 90
    hero["attack"] = 10
print("name:", hero["name"])
print("class:", hero["class"])
print("health:", hero["health"])
print("attack:", hero["attack"])''', "use a `for` loop"),
('''choice = input("Class? ")
name = input("Name? ")
while choice not in ["warrior", "mage", "rogue"]:
    choice = input("Warrior, mage or rogue? ")
hero = {"name": name, "class": choice, "health": 90, "attack": 10}
for key in hero:
    print(key + ":", hero[key])''', "Ask for the name first")]

# ---------------- h2b2 ----------------
GOOD["h2b2"] = ['''hero = {"name": "Brin", "health": 100, "gold": 0}

print("A rat bites you!")
hero["health"] = hero["health"] - 10

print("You find a coin purse.")
hero["gold"] = hero["gold"] + 5

print(hero)''']
BAD["h2b2"] = [('''hero = {"name": "Brin", "health": 100, "gold": 0}
print("A rat bites you!")
hero["health"] = hero["health"] - 10
print("You find a coin purse.")
hero["Gold"] = hero["gold"] + 5
print(hero)''', "new key called `Gold`"),
('''hero = {"name": "Brin", "health": 100, "gold": 0}
print("A rat bites you!")
hero["health"] = hero["health"] - 1
print("You find a coin purse.")
hero["gold"] = hero["gold"] + 5
print(hero)''', "health should be 90")]

# ---------------- h2b3 ----------------
GOOD["h2b3"] = ['''hero = {"name": "Brin", "health": 100, "backpack": []}

# add the torch and the map here
hero["backpack"].append("torch")
hero["backpack"].append("map")

print("Backpack:", hero["backpack"])
print("You carry", len(hero["backpack"]), "things.")''']
BAD["h2b3"] = [('''hero = {"name": "Brin", "health": 100, "backpack": []}
hero["backpack"].append("map")
hero["backpack"].append("torch")
print("Backpack:", hero["backpack"])
print("You carry", len(hero["backpack"]), "things.")''', "wrong way round"),
('''hero = {"name": "Brin", "health": 100, "backpack": ["torch", "map"]}
print("Backpack:", hero["backpack"])
print("You carry", len(hero["backpack"]), "things.")''', "use `append` twice"),
('''hero = {"name": "Brin", "health": 100, "backpack": []}
hero["backpack"] = "torch"
hero["backpack"] = "map"
print("Backpack:", hero["backpack"])
print("You carry", len(hero["backpack"]), "things.")''', "isn't a list any more"),
('''hero = {"name": "Brin", "health": 100, "backpack": []}
hero["backpack"] = hero["backpack"].append("torch")
hero["backpack"].append("map")
print("Backpack:", hero["backpack"])
print("You carry", len(hero["backpack"]), "things.")''', "turned into None")]

# ---------------- h2i1 ----------------
GOOD["h2i1"] = ['''hero = {"name": "Ash", "gold": 30, "backpack": []}

answer = input("Buy a potion for 10 gold? ")
if answer == "yes" and hero["gold"] >= 10:
    hero["gold"] = hero["gold"] - 10
    hero["backpack"].append("potion")
    print("You buy a potion.")
elif answer == "yes":
    print("You can't afford it.")
else:
    print("Maybe later.")

print(hero)
''', '''hero = {"name": "Ash", "gold": 30, "backpack": []}
answer = input("Buy a potion for 10 gold? ").strip().lower()
if answer == "yes":
    if hero["gold"] < 10:
        print("You can't afford it.")
    else:
        hero["gold"] -= 10
        hero["backpack"].append("potion")
        print("You buy a potion.")
else:
    print("Maybe later.")
print(hero)
''']
BAD["h2i1"] = [('''hero = {"name": "Ash", "gold": 30, "backpack": []}
answer = input("Buy a potion for 10 gold? ")
if answer == "yes" and hero["gold"] > 10:
    hero["gold"] = hero["gold"] - 10
    hero["backpack"].append("potion")
    print("You buy a potion.")
elif answer == "yes":
    print("You can't afford it.")
else:
    print("Maybe later.")
print(hero)''', "check whether you need >= or >"),
('''hero = {"name": "Ash", "gold": 30, "backpack": []}
answer = input("Buy a potion for 10 gold? ")
if answer == "yes":
    hero["gold"] = hero["gold"] - 10
    hero["backpack"].append("potion")
    print("You buy a potion.")
else:
    print("Maybe later.")
print(hero)''', "I set the gold to 9"),
('''hero = {"name": "Ash", "gold": 30, "backpack": []}
answer = input("Buy a potion for 10 gold? ")
if answer == "yes" and hero["gold"] >= 10:
    gold = hero["gold"] - 10
    hero["backpack"].append("potion")
    print("You buy a potion.")
elif answer == "yes":
    print("You can't afford it.")
else:
    print("Maybe later.")
print(hero)''', "should finish with 20 gold"),
('''hero = {"name": "Ash", "gold": 30, "backpack": []}
answer = input("Buy a potion for 10 gold? ")
if answer == "yes" and hero["gold"] >= 10:
    hero["gold"] = hero["gold"] - 10
    hero["backpack"].append("potion")
    print("You buy a potion.")
elif answer == "no":
    print("Maybe later.")
print(hero)''', "I typed maybe")]

# ---------------- h2a1 ----------------
GOOD["h2a1"] = ['''prices = {"gem": 50, "rope": 5, "bone": 1}
hero = {"gold": 10, "backpack": ["gem", "rope", "sock", "gem"]}

keep = []
for item in hero["backpack"]:
    if item in prices:
        hero["gold"] = hero["gold"] + prices[item]
        print("You sell the", item, "for", prices[item], "gold.")
    else:
        keep.append(item)
hero["backpack"] = keep
print(hero)
''', '''prices = {"gem": 50, "rope": 5, "bone": 1}
hero = {"gold": 10, "backpack": ["gem", "rope", "sock", "gem"]}
for item in hero["backpack"][:]:
    if item in prices:
        hero["gold"] += prices[item]
        hero["backpack"].remove(item)
        print("Sold", item)
print(hero)
''']
BAD["h2a1"] = [('''prices = {"gem": 50, "rope": 5, "bone": 1}
hero = {"gold": 10, "backpack": ["gem", "rope", "sock", "gem"]}
for item in hero["backpack"]:
    if item in prices:
        hero["gold"] = hero["gold"] + prices[item]
        hero["backpack"].remove(item)
print(hero)''', "Some items were skipped"),
('''prices = {"gem": 50, "rope": 5, "bone": 1}
hero = {"gold": 10, "backpack": ["gem", "rope", "sock", "gem"]}
keep = []
for item in hero["backpack"]:
    if item == "gem":
        hero["gold"] += 50
    elif item == "rope":
        hero["gold"] += 5
    elif item == "bone":
        hero["gold"] += 1
    else:
        keep.append(item)
hero["backpack"] = keep
print(hero)''', "Use the prices dictionary"),
('''prices = {"gem": 50, "rope": 5, "bone": 1}
hero = {"gold": 10, "backpack": ["gem", "rope", "sock", "gem"]}
for item in hero["backpack"]:
    if item in prices:
        hero["gold"] = hero["gold"] + prices[item]
print(hero)''', "It should finish with 115 gold and ['sock']")]

# ---------------- h3b2 ----------------
GOOD["h3b2"] = ['''def treasure_room(hero):
    print("You open a dusty chest.")
    hero["gold"] = hero["gold"] + 25
    return hero

hero = {"health": 100, "gold": 0}
hero = treasure_room(hero)
print("Gold:", hero["gold"])''']
BAD["h3b2"] = [('''def treasure_room(hero):
    print("You open a dusty chest.")
    hero["gold"] = hero["gold"] + 25
    return

hero = {"health": 100, "gold": 0}
hero = treasure_room(hero)
print("Gold:", hero["gold"])''', "return hero"),
('''def treasure_room(hero):
    print("You open a dusty chest.")
    hero["gold"] = hero["gold"] + 25
    return hero

hero = {"health": 100, "gold": 0}
hero = treasure_room()
print("Gold:", hero["gold"])''', "number of values in the call")]

# ---------------- h3b3 ----------------
GOOD["h3b3"] = ['''# Write trap_room(hero) here
def trap_room(hero):
    print("Spikes shoot up from the floor!")
    hero["health"] = hero["health"] - 20
    return hero

# main program
hero = {"health": 100, "gold": 10}
hero = trap_room(hero)
print("Health:", hero["health"])''', '''def trap_room(hero):
    print("Ouch!")
    hero["health"] -= 20
    return hero

hero = {"health": 100, "gold": 10}
hero = trap_room(hero)
print("Health:", hero["health"])''']
BAD["h3b3"] = [('''def trap_room(hero):
    print("Spikes!")
    hero["health"] = hero["health"] - 20

hero = {"health": 100, "gold": 10}
hero = trap_room(hero)
print("Health:", hero["health"])''', "not subscriptable"),
('''def trap_room(hero):
    print("Spikes!")
    hero = {"health": 80, "gold": 10}
    return hero

hero = {"health": 100, "gold": 10}
hero = trap_room(hero)
print("Health:", hero["health"])''', "makes a new hero"),
('''def trap_room(hero):
    print("Spikes!")
    hero["health"] = 80
    return hero

hero = {"health": 100, "gold": 10}
hero = trap_room(hero)
print("Health:", hero["health"])''', "take 20 from whatever health"),
('''def trap_room(hero):
    hero["health"] = hero["health"] - 20
    return hero

hero = {"health": 100, "gold": 10}
hero = trap_room(hero)
print("Health:", hero["health"])''', "add a print line"),
('''def trap_room(hero):
    print("Spikes!")
    health = hero["health"] - 20
    return hero

hero = {"health": 100, "gold": 10}
hero = trap_room(hero)
print("Health:", hero["health"])''', "It should come back with 30")]

# ---------------- h3i1 ----------------
GOOD["h3i1"] = ['''def show_status(hero):
    print("Health:", hero["health"])
    print("Gold:", hero["gold"])
    print("Backpack:", hero["backpack"])

def armoury(hero):
    print("Swords line the walls.")
    hero["backpack"].append("sword")
    return hero

def well(hero):
    answer = input("Throw a coin in the well? ")
    if answer == "yes" and hero["gold"] >= 1:
        hero["gold"] = hero["gold"] - 1
        hero["health"] = hero["health"] + 5
        print("You feel better.")
    elif answer == "yes":
        print("You have no coins.")
    return hero

# main program
hero = {"health": 90, "gold": 3, "backpack": []}
hero = armoury(hero)
hero = well(hero)
show_status(hero)
''']
BAD["h3i1"] = [('''def show_status(hero):
    print(hero)

def armoury(hero):
    hero["backpack"].append("sword")

def well(hero):
    answer = input("Throw a coin in the well? ")
    if answer == "yes" and hero["gold"] >= 1:
        hero["gold"] -= 1
        hero["health"] += 5
    elif answer == "yes":
        print("You have no coins.")
    return hero

hero = {"health": 90, "gold": 3, "backpack": []}
armoury(hero)
hero = well(hero)
show_status(hero)''', "`armoury` and nothing came back"),
('''def show_status(hero):
    print(hero)

def armoury(hero):
    hero["backpack"].append("sword")
    return hero

def well(hero):
    answer = input("Throw a coin in the well? ")
    if answer == "yes" and hero["gold"] > 1:
        hero["gold"] -= 1
        hero["health"] += 5
    elif answer == "yes":
        print("You have no coins.")
    return hero

hero = {"health": 90, "gold": 3, "backpack": []}
hero = armoury(hero)
hero = well(hero)
show_status(hero)''', "1 gold is enough"),
('''def show_status(hero):
    print(hero)

def armoury(hero):
    hero["backpack"].append("sword")
    return hero

def well(hero):
    answer = input("Throw a coin in the well? ")
    if answer == "yes":
        hero["gold"] -= 1
        hero["health"] += 5
    return hero

hero = {"health": 90, "gold": 3, "backpack": []}
hero = armoury(hero)
hero = well(hero)
show_status(hero)''', "0 gold to the well")]

# ---------------- h3a1 ----------------
GOOD["h3a1"] = ['''def boss(hero):
    boss_health = 40
    while hero["health"] > 0 and boss_health > 0:
        move = input("attack or potion? ")
        if move == "attack":
            if "sword" in hero["backpack"]:
                boss_health = boss_health - 15
            else:
                boss_health = boss_health - 5
            print("The boss has", boss_health, "health.")
        elif move == "potion":
            if "potion" in hero["backpack"]:
                hero["backpack"].remove("potion")
                hero["health"] = hero["health"] + 30
                if hero["health"] > 100:
                    hero["health"] = 100
            else:
                print("You have no potion.")
        if boss_health > 0:
            hero["health"] = hero["health"] - 10
            print("The boss hits you! Health:", hero["health"])
    if boss_health <= 0:
        hero["boss_beaten"] = True
    return hero

hero = {"health": 100, "backpack": ["sword", "potion"]}
hero = boss(hero)
print(hero)
''', '''def boss(hero):
    enemy = 40
    while True:
        move = input("attack or potion? ").lower()
        if move == "attack":
            enemy -= 15 if "sword" in hero["backpack"] else 5
        elif move == "potion" and "potion" in hero["backpack"]:
            hero["backpack"].remove("potion")
            hero["health"] = min(100, hero["health"] + 30)
        elif move == "potion":
            print("You have no potion.")
        if enemy <= 0:
            hero["boss_beaten"] = True
            return hero
        hero["health"] -= 10
        if hero["health"] <= 0:
            print("You fall.")
            return hero
''']
_BOSS = '''def boss(hero):
    boss_health = 40
    while hero["health"] > 0 and boss_health > 0:
        move = input("attack or potion? ")
        if move == "attack":
            if "sword" in hero["backpack"]:
                boss_health = boss_health - 15
            else:
                boss_health = boss_health - 5
        elif move == "potion":
            if "potion" in hero["backpack"]:
                hero["backpack"].remove("potion")
                hero["health"] = hero["health"] + 30
                if hero["health"] > 100:
                    hero["health"] = 100
            else:
                print("You have no potion.")
        if boss_health > 0:
            hero["health"] = hero["health"] - 10
    if boss_health <= 0:
        hero["boss_beaten"] = True
    return hero
'''
BAD["h3a1"] = [
 (_BOSS.replace('        if boss_health > 0:\n            hero["health"] = hero["health"] - 10\n', '        hero["health"] = hero["health"] - 10\n'), "shouldn't hit back"),
 (_BOSS.replace('                if hero["health"] > 100:\n                    hero["health"] = 100\n', ''), "took the health above 100"),
 (_BOSS.replace('    if boss_health <= 0:\n        hero["boss_beaten"] = True\n', ''), "boss_beaten"),
 (_BOSS.replace('    return hero\n', ''), "Add `return hero`"),
 (_BOSS.replace('while hero["health"] > 0 and boss_health > 0:', 'while boss_health > 0:'), "it kept asking"),
 (_BOSS.replace('''            if "potion" in hero["backpack"]:
                hero["backpack"].remove("potion")
                hero["health"] = hero["health"] + 30
                if hero["health"] > 100:
                    hero["health"] = 100
            else:
                print("You have no potion.")''', '''            hero["backpack"].remove("potion")
            hero["health"] = hero["health"] + 30
            if hero["health"] > 100:
                hero["health"] = 100'''), "isn't in the list"),
 (_BOSS.replace('''            if "sword" in hero["backpack"]:
                boss_health = boss_health - 15
            else:
                boss_health = boss_health - 5''', '''            boss_health = boss_health - 15'''), "Without a sword each attack does 5"),
]
