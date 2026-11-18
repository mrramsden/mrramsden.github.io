# Model answers (must pass) and typical mistakes (must fail with a helpful message).
GOOD, BAD = {}, {}

GOOD["q1b2"] = ['''def welcome(name):
    print("Welcome to the dungeon,", name)
    print("Good luck,", name)

hero = input("What is your name? ")
welcome(hero)''']
BAD["q1b2"] = [('''def welcome(name):
    print("Welcome to the dungeon,", "name")
    print("Good luck,", name)

hero = input("What is your name? ")
welcome(hero)''', "quote marks"),
('''def welcome(name):
    print("Welcome to the dungeon,", hero)
    print("Good luck,", name)

hero = input("What is your name? ")
welcome(hero)''', "welcome('Zed')")]

GOOD["q1b3"] = ['''def show_status(health, gold):
    print("Health:", health)
    print("Gold:", gold)

# main program
health = 100
gold = 10
show_status(health, gold)
health = 60
gold = 35
show_status(health, gold)
''', '''def show_status(health, gold):
    print("~~~~~~~~")
    print("Health", health, "Gold", gold)

health = 100
gold = 10
show_status(health, gold)
health = 60
gold = 35
show_status(health, gold)
''']
BAD["q1b3"] = [('''def show_status(health, gold):
    print("Gold:", gold)
    print("Health:", health)

health = 100
gold = 10
show_status(health, gold)
health = 60
gold = 35
show_status(health, gold)
''', "before the health"),
('''def show_status(h):
    print("Health:", h)

health = 100
gold = 10
show_status(health)
''', "2 parameters"),
('''# Write show_status(health, gold) here


# main program
health = 100
gold = 10
show_status(health, gold)
''', "NameError")]

GOOD["q1i1"] = ['''def show_hero(name, health, gold):
    print("==", name, "==")
    print("Health:", health)
    print("Gold:", gold)

def trap_room(health):
    print("Spikes!")
    health = health - 25
    return health

name = input("Hero name? ")
health = 100
gold = 20
show_hero(name, health, gold)
health = trap_room(health)
show_hero(name, health, gold)''']
BAD["q1i1"] = [('''def show_hero(name, health, gold):
    print("==", name, "==")
    print("Health:", health)
    print("Gold:", gold)

def trap_room(health):
    health = health - 25

name = input("Hero name? ")
health = 100
gold = 20
show_hero(name, health, gold)
trap_room(health)
show_hero(name, health, gold)''', "return health"),
('''def show_hero(name, health, gold):
    print("==", name, "==")
    print("Health:", health)
    print("Gold:", gold)

def trap_room(health):
    health = health - 25
    return health

name = input("Hero name? ")
health = 100
gold = 20
show_hero(name, health, gold)
trap_room(health)
show_hero(name, health, gold)''', "catch the result")]

GOOD["q1i2"] = ['''def divider(length, symbol):
    print(symbol * length)

divider(30, "~")
divider(10, "*")''']
BAD["q1i2"] = [('''def divider(length, symbol):
    print(symbol * 10)

divider(30, "~")
divider(10, "*")''', "divider(5, '*')")]

GOOD["q1a1"] = ['''def show_bar(health):
    if health < 0:
        health = 0
    full = health // 10
    print("Health [" + "#" * full + "-" * (10 - full) + "]", health)

for h in [100, 70, 45, 5, 0, -20]:
    show_bar(h)''']
BAD["q1a1"] = [('''def show_bar(health):
    full = health // 10
    print("Health [" + "#" * full + "-" * (10 - full) + "]", health)
''', "Below 0"),
('''def show_bar(health):
    full = round(health / 10)
    if health < 0:
        health = 0
        full = 0
    print("Health [" + "#" * full + "-" * (10 - full) + "]", health)
''', "rounded down")]

GOOD["q1a2"] = ['''# max_health=100 is a default: if you leave it out, it uses 100
def show_bar(health, max_health=100):
    if health < 0:
        health = 0
    full = health * 10 // max_health
    print("Health [" + "#" * full + "-" * (10 - full) + "]", health)

show_bar(45)
show_bar(45, 60)''']
BAD["q1a2"] = [('''def show_bar(health, max_health=100):
    full = health // 10
    print("Health [" + "#" * full + "-" * (10 - full) + "]", health)
''', "show_bar(45, 60)")]

GOOD["q2b2"] = ['''import random

roll = random.randint(1, 6)
print("You rolled a", roll)
if roll == 6:
    print("A critical hit!")''']
BAD["q2b2"] = [('''import random

roll = random.randint(0, 6)
print("You rolled a", roll)''', "rolled a 0"),
('''import random

roll = random.randint(1, 5)
print("You rolled a", roll)''', "never got 6")]

GOOD["q2b3"] = ['''import random

def treasure_room(gold):
    coins = random.randint(5, 20)
    print("You find", coins, "gold coins!")
    gold = gold + coins
    return gold

gold = 0
gold = treasure_room(gold)
print("Gold:", gold)''']
BAD["q2b3"] = [('''import random

def treasure_room(gold):
    coins = random.randint(5, 19)
    print("You find", coins, "gold coins!")
    gold = gold + coins
    return gold

gold = 0
gold = treasure_room(gold)''', "5 to 20"),
('''import random

def treasure_room(gold):
    coins = random.randint(20, 5)
    gold = gold + coins
    return gold

gold = 0
gold = treasure_room(gold)''', "smaller number first")]

GOOD["q2i1"] = ['''import random

def trap_room(health):
    roll = random.randint(1, 4)
    if roll == 1:
        print("You dodge the trap!")
    else:
        damage = random.randint(5, 25)
        print("Ouch! You lose", damage)
        health = health - damage
    return health

health = 100
for i in range(3):
    health = trap_room(health)
print("Health:", health)''']
BAD["q2i1"] = [('''import random

def trap_room(health):
    roll = random.randint(1, 4)
    if roll == 1:
        print("You dodge the trap!")
    damage = random.randint(5, 25)
    health = health - damage
    return health

health = 100
health = trap_room(health)
print(health)''', "inside an else"),
('''import random

def trap_room(health):
    roll = random.randint(1, 2)
    if roll == 1:
        print("You dodge the trap!")
    else:
        health = health - random.randint(5, 25)
    return health

health = trap_room(100)
print(health)''', "25%")]

GOOD["q2i2"] = ['''import random

def encounter(health):
    beast = random.choice(["rat", "bat", "snake", "ghost"])
    damage = random.randint(5, 15)
    print("A", beast, "attacks! You lose", damage)
    return health - damage

health = 100
health = encounter(health)
health = encounter(health)
health = encounter(health)''']
BAD["q2i2"] = [('''import random

def encounter(health):
    beast = "rat"
    damage = random.randint(5, 15)
    return health - damage
''', "random.choice")]

GOOD["q2a1"] = ['''import random

def fight(health):
    goblin = 30
    while health > 0 and goblin > 0:
        move = input("attack or defend? ")
        if move == "attack":
            hit = random.randint(5, 15)
            goblin = goblin - hit
            print("You hit the goblin for", hit)
        if goblin > 0:
            hurt = random.randint(4, 12)
            if move == "defend":
                hurt = hurt // 2
            health = health - hurt
            print("The goblin hits you for", hurt)
    return health

health = fight(100)
print(health)''']
BAD["q2a1"] = [('''import random

def fight(health):
    goblin = 30
    while health > 0 and goblin > 0:
        move = input("attack or defend? ")
        if move == "attack":
            goblin = goblin - random.randint(5, 15)
        if goblin > 0:
            hurt = random.randint(4, 12)
            health = health - hurt
    return health
''', "halve"),
('''import random

def fight(health):
    goblin = 30
    while health > 0 or goblin > 0:
        move = input("attack or defend? ")
        if move == "attack":
            goblin = goblin - random.randint(5, 15)
        if goblin > 0:
            hurt = random.randint(4, 12)
            if move == "defend":
                hurt = hurt // 2
            health = health - hurt
    return health
''', "")]

GOOD["q2a2"] = ['''import random
random.seed(1)  # same numbers every run, so tests repeat. Remove before release or the game is predictable.
''']

GOOD["q3b2"] = ['''bag = ["torch", "bread"]
bag.append("map")
print("You have", len(bag), "items:")
for item in bag:
    print(item)''']
BAD["q3b2"] = [('''bag = ["torch", "bread"]
bag.append("map")
print("You have", len(bag), "items:")
for item in bag:
    print(bag)''', "own line")]

GOOD["q3b3"] = ['''def armoury(inventory):
    print("Weapons hang on the walls.")
    inventory.append("sword")
    inventory.append("shield")
    return inventory

inventory = ["torch"]
inventory = armoury(inventory)
print(inventory)''']
BAD["q3b3"] = [('''def armoury(inventory):
    print("Weapons hang on the walls.")
    inventory.append("sword")
    inventory.append("shield")

inventory = ["torch"]
inventory = armoury(inventory)
print(inventory)''', "return inventory"),
('''def armoury(inventory):
    print("Weapons hang on the walls.")
    inventory = ["torch", "sword", "shield"]
    return inventory

inventory = ["torch"]
inventory = armoury(inventory)
print(inventory)''', "don't make a new one")]

GOOD["q3i1"] = ['''def pick_up(inventory, item):
    inventory.append(item)
    return inventory

def show_bag(inventory):
    if len(inventory) == 0:
        print("Your bag is empty.")
    else:
        for i in range(len(inventory)):
            print(str(i + 1) + ". " + inventory[i])

inventory = []
show_bag(inventory)
inventory = pick_up(inventory, "rope")
inventory = pick_up(inventory, "lantern")
show_bag(inventory)''']
BAD["q3i1"] = [('''def pick_up(inventory, item):
    inventory.append(item)
    return inventory

def show_bag(inventory):
    if len(inventory) == 0:
        print("Your bag is empty.")
    for i in range(len(inventory)):
        print(i, inventory[i])

inventory = []
show_bag(inventory)''', "1. rope")]

GOOD["q3i2"] = ['''def pick_up(inventory, item):
    if len(inventory) >= 4:
        print("Your bag is full!")
    else:
        inventory.append(item)
    return inventory''']
BAD["q3i2"] = [('''def pick_up(inventory, item):
    if len(inventory) > 4:
        print("Your bag is full!")
    else:
        inventory.append(item)
    return inventory''', "5th item")]

GOOD["q3a1"] = ['''import random

def chest(inventory, gold):
    loot = random.choice(["gold", "potion", "key", "nothing"])
    if loot == "gold":
        coins = random.randint(5, 20)
        print("Gold! +", coins)
        gold = gold + coins
    elif loot == "nothing":
        print("Empty. Sad.")
    else:
        print("You find a", loot)
        inventory.append(loot)
    return inventory, gold

inventory = []
gold = 0
for i in range(5):
    inventory, gold = chest(inventory, gold)
print(gold, inventory)''']
BAD["q3a1"] = [('''import random

def chest(inventory, gold):
    loot = random.choice(["gold", "potion", "key", "nothing"])
    if loot == "gold":
        gold = gold + random.randint(5, 20)
    else:
        inventory.append(loot)
    return inventory, gold
''', "Only a potion or a key")]

GOOD["q3a2"] = ['''def show_bag(inventory):
    done = []
    for item in inventory:
        if item not in done:
            print(item, "x" + str(inventory.count(item)))
            done.append(item)''']
BAD["q3a2"] = [('''def show_bag(inventory):
    for item in inventory:
        print(item, "x" + str(inventory.count(item)))''', "more than once")]

GOOD["q4b2"] = ['''def bridge(inventory):
    print("The rope bridge has snapped.")
    if "rope" in inventory:
        print("You tie your rope across and climb over.")
    else:
        print("You'll have to find another way.")
    return inventory

inventory = ["torch", "rope"]
inventory = bridge(inventory)''']
BAD["q4b2"] = [('''def bridge(inventory):
    print("The rope bridge has snapped.")
    if "rope" not in inventory:
        print("You tie your rope across and climb over.")
    else:
        print("You'll have to find another way.")
    return inventory

inventory = ["torch", "rope"]
inventory = bridge(inventory)''', "get across")]

GOOD["q4b3"] = ['''def troll(inventory):
    print("A huge troll blocks the path.")
    if "bread" in inventory:
        inventory.remove("bread")
        print("The troll munches the bread and lets you pass.")
    else:
        print("The troll ROARS. You turn back.")
    return inventory

inventory = ["torch", "bread"]
inventory = troll(inventory)
print("Bag:", inventory)
inventory = troll(inventory)''']
BAD["q4b3"] = [('''def troll(inventory):
    print("A huge troll blocks the path.")
    inventory.remove("bread")
    print("The troll lets you pass.")
    return inventory

inventory = ["torch", "bread"]
inventory = troll(inventory)
print("Bag:", inventory)
inventory = troll(inventory)''', "isn't in the list"),
('''def troll(inventory):
    print("A huge troll blocks the path.")
    if "bread" in inventory:
        print("The troll lets you pass.")
    else:
        print("ROAR")
    return inventory

inventory = ["torch", "bread"]
inventory = troll(inventory)''', "should be removed")]

GOOD["q4i1"] = ['''def cell(inventory):
    if "key" not in inventory:
        print("You find a key!")
        inventory.append("key")
    return inventory

def door(inventory):
    if "key" in inventory:
        print("The door opens.")
        inventory.remove("key")
    else:
        print("Locked.")
    return inventory

inventory = []
inventory = door(inventory)
inventory = cell(inventory)
inventory = door(inventory)''']
BAD["q4i1"] = [('''def cell(inventory):
    inventory.append("key")
    return inventory

def door(inventory):
    if "key" in inventory:
        inventory.remove("key")
        print("Open")
    else:
        print("Locked")
    return inventory
''', "shouldn't get another")]

GOOD["q4i2"] = ['''def use_item(inventory):
    thing = input("What do you want to use? ")
    if thing in inventory:
        print("You use the", thing)
        inventory.remove(thing)
    else:
        print("You don't have that.")
    return inventory''']
BAD["q4i2"] = [('''def use_item(inventory):
    thing = input("What do you want to use? ")
    print("You use the", thing)
    inventory.remove(thing)
    return inventory''', "isn't in the list")]

GOOD["q4a1"] = ['''def drink(inventory, health):
    if "potion" in inventory:
        inventory.remove("potion")
        health = health + 30
        if health > 100:
            health = 100
        print("Glug. Health:", health)
    else:
        print("No potions left.")
    return inventory, health

inventory = ["potion", "potion"]
health = 50
for i in range(3):
    inventory, health = drink(inventory, health)''', '''def drink(inventory, health):
    if "potion" in inventory:
        inventory.remove("potion")
        health = min(100, health + 30)
    return inventory, health''']
BAD["q4a1"] = [('''def drink(inventory, health):
    if "potion" in inventory:
        inventory.remove("potion")
        health = health + 30
    return inventory, health''', "above 100"),
('''def drink(inventory, health):
    if "potion" in inventory:
        inventory.remove("potion")
        health = min(100, health + 30)
    return health, inventory''', "wrong way round")]

ASK = '''def ask(question, options):
    answer = input(question).strip().lower()
    while answer not in options:
        print("Please type one of:", options)
        answer = input(question).strip().lower()
    return answer
'''
GOOD["q5b2"] = [ASK + '''
choice = ask("Open the door? ", ["yes", "no"])
if choice == "yes":
    print("The door creaks open.")
else:
    print("You walk away.")''']
BAD["q5b2"] = [(ASK.replace("return answer", "return options") + '''
choice = ask("Open the door? ", ["yes", "no"])
if choice == "yes":
    print("The door creaks open.")
else:
    print("You walk away.")''', "banana"),
(ASK + '''
choice = ask("Open the door? ", [yes, no])
if choice == "yes":
    print("The door creaks open.")''', "NameError")]

GOOD["q5b3"] = [ASK + '''
def well():
    print("You find an old well with a bucket on a rope.")
    way = ask("Up or down? ", ["up", "down"])
    if way == "up":
        print("You pull up a bucket of gold!")
    else:
        print("You climb down into the dark.")

def statue():
    print("A stone statue stares at you.")
    choice = ask("Touch or leave? ", ["touch", "leave"])
    if choice == "touch":
        print("It crumbles to dust.")
    else:
        print("You back away slowly.")

well()
statue()''']
BAD["q5b3"] = [(ASK + '''
def well():
    print("You find an old well with a bucket on a rope.")
    way = input("Up or down? ")
    print("You chose", way)

def statue():
    print("A stone statue stares at you.")
    choice = ask("Touch or leave? ", ["touch", "leave"])
    if choice == "touch":
        print("It crumbles to dust.")
    else:
        print("You back away slowly.")

well()
statue()''', "well room should use")]

GOOD["q5i1"] = ['''def ask(question, options):
    answer = input(question).strip().lower()
    while answer not in options:
        print("Choose from", options)
        answer = input(question).strip().lower()
    return answer

def door():
    if ask("Open? ", ["yes", "no"]) == "yes":
        print("Creak")

def river():
    if ask("Swim or wade? ", ["swim", "wade"]) == "swim":
        print("Splash")

def tunnel():
    way = ask("Left or right? ", ["left", "right"])
    print("You go", way)

door()
river()
tunnel()''']
BAD["q5i1"] = [('''def ask(question, options):
    answer = input(question)
    while answer not in options:
        answer = input(question)
    return answer

def door():
    ask("Open? ", ["yes", "no"])
''', "strip().lower()"),
('''def ask(question, options):
    answer = input(question).strip().lower()
    while answer not in options:
        answer = input(question).strip().lower()
    return answer

def door():
    ask("Open? ", ["yes", "no"])
''', "I found 1")]

GOOD["q5i2"] = ['''def ask_number(question, low, high):
    while True:
        answer = input(question).strip()
        if answer.isdigit() and low <= int(answer) <= high:
            return int(answer)
        print("Type a whole number from", low, "to", high)''']
BAD["q5i2"] = [('''def ask_number(question, low, high):
    number = int(input(question))
    while number < low or number > high:
        number = int(input(question))
    return number''', "ValueError"),
('''def ask_number(question, low, high):
    answer = input(question)
    while not answer.isdigit() or int(answer) < low or int(answer) >= high:
        answer = input(question)
    return int(answer)''', "use <= so the end numbers count")]

GOOD["q5a1"] = ['''def ask(question, options):
    while True:
        answer = input(question).strip().lower()
        for option in options:
            if answer != "" and (answer == option or answer == option[0]):
                return option
        print("Please choose from", options)''']
BAD["q5a1"] = [('''def ask(question, options):
    while True:
        answer = input(question).strip().lower()
        for option in options:
            if option.startswith(answer):
                return option''', "blank answer"),
('''def ask(question, options):
    while True:
        answer = input(question).strip().lower()
        for option in options:
            if answer == option or answer[0] == option[0]:
                return option''', "")]

GOOD["q5a2"] = ['''# Test plan
# normal: 3 -> returns 3
# boundary: 1 and 5 -> accepted, 0 and 6 -> asked again
# erroneous: ten, blank, 2.5 -> asked again, no crash
def ask_number(question, low, high):
    while True:
        answer = input(question).strip()
        try:
            number = int(answer)
        except ValueError:
            print("That isn't a whole number.")
            continue
        if low <= number <= high:
            return number
        print("Out of range.")''']
BAD["q5a2"] = [('''# normal boundary erroneous
def ask_number(question, low, high):
    while True:
        answer = input(question).strip()
        if answer.isdigit() and low <= int(answer) <= high:
            return int(answer)''', "Negative numbers"),
('''def ask_number(question, low, high):
    while True:
        answer = input(question).strip()
        try:
            number = int(answer)
        except ValueError:
            continue
        if low <= number <= high:
            return number''', "test plan")]

GOOD["q6b2"] = ['''import random

def spider(health, inventory):
    print("A giant spider drops from the ceiling!")
    bite = random.randint(5, 15)
    if "shield" in inventory:
        bite = bite // 2
        print("Your shield blocks some of the bite.")
    health = health - bite
    print("You lose", bite, "health.")
    return health

health = 30
inventory = ["torch", "shield"]
health = spider(health, inventory)
print("Health:", health)''']
BAD["q6b2"] = [('''import random

def spider(health, inventory):
    bite = random.randint(5, 15)
    if "torch" in inventory:
        bite = bite // 2
    health = health - bite
    return health
''', "halved"),
('''import random

def spider(health, inventory):
    bite = random.randint(5, 15)
    if shield in inventory:
        bite = bite // 2
    health = health - bite
    return health
''', "NameError")]

BOSS = ASK + '''
import random

def boss(health, inventory):
    boss_hp = 60
    while health > 0 and boss_hp > 0:
        move = ask("Swing or block? ", ["swing", "block"])
        if move == "swing":
            hit = random.randint(8, 16)
            if "axe" in inventory:
                hit = hit + 8
            boss_hp = boss_hp - hit
        if boss_hp > 0:
            claw = random.randint(10, 18)
            if move == "block":
                claw = claw // 2
            health = health - claw
    return health
'''
GOOD["q6i1"] = [BOSS + '''
health = boss(100, ["axe"])
if health > 0:
    print("You win!")
else:
    print("Game over")''']
BAD["q6i1"] = [(BOSS.replace('if "axe" in inventory:\n                hit = hit + 8', 'if "axe" in inventory:\n                hit = hit + 0'), "didn't help"),
(ASK + '''
import random

def boss(health, inventory):
    boss_hp = 60
    while health > 0 and boss_hp > 0:
        move = ask("Swing or block? ", ["swing", "block"])
        if "axe" in inventory:
            boss_hp = boss_hp - 1
        health = health - random.randint(1, 5)
''', "return")]

GOOD["q6a1"] = [ASK + '''
import random

def drink(inventory, health):
    if "potion" in inventory:
        inventory.remove("potion")
        health = min(100, health + 30)
    else:
        print("No potion!")
    return inventory, health

def boss(health, inventory):
    boss_hp = 70
    while health > 0 and boss_hp > 0:
        move = ask("attack, shield or drink? ", ["attack", "shield", "drink"])
        if move == "attack":
            hit = random.randint(5, 15)
            if "sword" in inventory:
                hit = hit + 10
            boss_hp = boss_hp - hit
        elif move == "drink":
            inventory, health = drink(inventory, health)
        if boss_hp > 0:
            burn = random.randint(8, 16)
            if move == "shield":
                burn = burn // 2
            health = health - burn
    return inventory, health
''']
BAD["q6a1"] = [(GOOD["q6a1"][0].replace('        inventory.remove("potion")\n', ''), "still in the bag"),
(GOOD["q6a1"][0].replace("return inventory, health\n", "return health\n").replace("return health\n\ndef boss", "return inventory, health\n\ndef boss"), "two things")]

GOOD["q6a2"] = ['''# normal: attack with sword -> boss falls
# boundary: health exactly 0 after a hit -> game over
# erroneous: type banana -> asked again
import random
random.seed(5)''']
