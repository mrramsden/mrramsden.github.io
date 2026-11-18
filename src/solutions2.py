GOOD, BAD = {}, {}

GOOD["p2b2"] = ['''def library():
    print("You find yourself in a dusty library.")
    print("Books are piled to the ceiling.")

library()''']
BAD["p2b2"] = [('''def library():
    print("You find yourself in a dusty library.")
    print("Books are piled to the ceiling.")

library''', "brackets")]

GOOD["p2b3"] = ['''# Define your room here
def entrance():
    print("You stand at the mouth of a cave.")
    print("Bats flutter overhead.")

# Call it here
entrance()''']
BAD["p2b3"] = [('''def entrance():
    print("You stand at the mouth of a cave.")
    print("Bats flutter overhead.")
''', "never called"),
('''def entrance():
    print("You stand at the mouth of a cave.")
    print("Bats flutter overhead.")

    entrance()''', "never called")]

GOOD["p2i1"] = ['''def hall():
    print("A long hall.")
    print("Portraits watch you.")

def well():
    answer = input("Look down the well? ")
    if answer == "yes":
        print("A coin glints at the bottom.")
    else:
        print("You walk on.")

hall()
well()''']
BAD["p2i1"] = [('''def hall():
    print("A long hall.")

def well():
    answer = input("Look down the well? ")
    print("You look.")

hall()
well()''', "if and else")]

GOOD["p2i2"] = ['''def divider():
    print("~" * 30)

def hall():
    print("Hall")

hall()
divider()
hall()''']
BAD["p2i2"] = [('''def divider():
    print("~" * 20)

divider()''', "exactly 30")]

GOOD["p2a1"] = ['''def riddle_door():
    answer = input("What has keys but can't open locks? ").strip().lower()
    while answer != "piano":
        print("The door stays shut.")
        answer = input("Try again: ").strip().lower()
    print("The door swings open.")

def armoury():
    choice = input("look, search or leave? ")
    while choice != "leave":
        if choice == "look":
            print("Racks of rusty swords.")
        elif choice == "search":
            print("You find a dagger!")
        else:
            print("Eh?")
        choice = input("look, search or leave? ")
    print("You leave the armoury.")

riddle_door()
armoury()''']
BAD["p2a1"] = [('''def riddle_door():
    answer = input("What has keys but can't open locks? ")
    if answer != "piano":
        print("Wrong")
        answer = input("Try again: ")

def armoury():
    choice = input("look, search or leave? ")
    while choice != "leave":
        print("You look around.")
        choice = input("look, search or leave? ")
''', "while loop"),
('''def riddle_door():
    answer = input("Riddle? ")
    while answer != "piano":
        answer = input("Try again: ")

def armoury():
    choice = input("look, search or leave? ")
    while choice != "leave":
        print("You look around.")
        choice = input("look, search or leave? ")
''', "different response")]

GOOD["p2a2"] = ['''def torches():
    for t in range(1, 4):
        print("Torch", t, "flares into life.")

def hall():
    print("A dark hall.")
    torches()

def crypt():
    print("A cold crypt.")
    torches()

# Writing torches once means one change fixes it everywhere
hall()
crypt()''']
BAD["p2a2"] = [('''def torches():
    for t in range(1, 4):
        print("Torch", t)

def hall():
    torches()

# comment
hall()''', "two different rooms")]

GOOD["p3b2"] = ['''def torches():
    for torch in range(1, 6):
        print("Torch", torch, "is lit.")

def guard():
    answer = input("The guard asks: friend or foe? ")
    if answer == "friend":
        print("The guard lets you pass.")
    else:
        print("The guard blocks the way.")

# main program
torches()
guard()''']
BAD["p3b2"] = [('''def torches():
    for torch in range(1, 5):
        print("Torch", torch, "is lit.")

def guard():
    answer = input("The guard asks: friend or foe? ")
    if answer == "friend":
        print("The guard lets you pass.")
    else:
        print("The guard blocks the way.")

torches()
guard()''', "exactly 5"),
('''def torches():
    for torch in range(1, 6):
        print("Torch", torch, "is lit.")

def guard():
    answer = input("The guard asks: friend or foe? ")
    if answer == "friend":
        print("The guard lets you pass.")
    else:
        print("The guard blocks the way.")

guard()
torches()''', "first")]

GOOD["p3i1"] = ['''def corridor():
    for t in range(3):
        print("Torch")

def door():
    word = input("Password? ")
    while word != "open":
        word = input("Password? ")

def fork():
    way = input("left, right or back? ")
    if way == "left":
        print("Cave")
    elif way == "right":
        print("River")
    else:
        print("Back you go")

corridor()
door()
fork()''']
BAD["p3i1"] = [('''def corridor():
    for t in range(3):
        print("Torch")

def door():
    print("Door")

def fork():
    way = input("left or right? ")
    if way == "left":
        print("Cave")
    elif way == "right":
        print("River")
    else:
        print("Back")

corridor()
door()
fork()''', "while loop")]

GOOD["p3i2"] = ['''def corridor():
    print("Corridor")

def door():
    print("Door")

def fork():
    print("Fork")

choice = input("corridor, door, fork or exit? ")
while choice != "exit":
    if choice == "corridor":
        corridor()
    elif choice == "door":
        door()
    elif choice == "fork":
        fork()
    choice = input("corridor, door, fork or exit? ")''']
BAD["p3i2"] = [('''def corridor():
    print("Corridor")

choice = input("Where? ")
if choice == "corridor":
    corridor()''', "while loop")]

GOOD["p3a1"] = ['''def hall():
    print("A grand hall.")

def cellar():
    print("A damp cellar.")

def tower():
    print("A windy tower.")

visited = 0
place = input("Where now? ").strip().lower()
while place != "exit":
    if place == "hall":
        hall()
        visited = visited + 1
    elif place == "cellar":
        cellar()
        visited = visited + 1
    elif place == "tower":
        tower()
        visited = visited + 1
    else:
        print("There's no room called", place)
    place = input("Where now? ").strip().lower()
print("You visited", visited, "rooms.")''']
BAD["p3a1"] = [(GOOD["p3a1"][0].replace('''    else:
        print("There's no room called", place)
''', '''    else:
        print("There's no room called", place)
        visited = visited + 1
'''), "shouldn't count"),
(GOOD["p3a1"][0].replace(".strip().lower()", ""), "EXIT in capitals and it kept asking")]

GOOD["p3a2"] = ['''def show_help():
    print("Commands: hall, cellar, help, exit")

def hall():
    print("A grand hall.")

# visited is in the main program because a room's local variables vanish when it ends
visited = 0
place = input("Where now? ").strip().lower()
while place != "exit":
    if place == "help" or place == "h":
        show_help()
    elif place == "hall":
        hall()
        visited = visited + 1
    place = input("Where now? ").strip().lower()
print(visited)''']
BAD["p3a2"] = [('''def show_help():
    print("Commands: hall, exit")

# comment
place = input("Where now? ").strip().lower()
while place != "exit":
    if place == "help":
        show_help()
    place = input("Where now? ").strip().lower()''', "typed h,")]

GOOD["p4b2"] = ['''def treasure_room(gold):
    print("You open a dusty chest.")
    gold = gold + 15
    return gold

gold = 0
gold = treasure_room(gold)
print("You now have", gold, "gold.")''']
BAD["p4b2"] = [('''def treasure_room(gold):
    print("You open a dusty chest.")
    gold = gold + 15
    return 15

gold = 0
gold = treasure_room(gold)
print("You now have", gold, "gold.")''', "treasure_room(10)")]

GOOD["p4b3"] = ['''def potion_room(health):
    print("You find a glowing potion and drink it.")
    health = health + 30
    return health

health = 50
health = potion_room(health)
print("Health:", health)''']
BAD["p4b3"] = [('''def potion_room(health):
    print("You find a glowing potion and drink it.")
    health = health + 30

health = 50
health = potion_room(health)
print("Health:", health)''', "return health")]

GOOD["p4i1"] = ['''def trap_room(health):
    print("A trap!")
    health = health - 20
    return health

def treasure_room(gold):
    print("Treasure!")
    gold = gold + 10
    return gold

health = 100
gold = 0
health = trap_room(health)
gold = treasure_room(gold)
health = trap_room(health)
print("Health:", health)
print("Gold:", gold)''']
BAD["p4i1"] = [('''def trap_room(health):
    print("A trap!")
    health = health - 20
    return health

def treasure_room(gold):
    print("Treasure!")
    gold = gold + 10
    return gold

health = 100
gold = 0
trap_room(health)
gold = treasure_room(gold)
trap_room(health)
print("Health:", health)
print("Gold:", gold)''', "Catch each result")]

GOOD["p4i2"] = ['''def dodge_room(health):
    move = input("A boulder! jump or duck? ")
    if move == "jump":
        print("You leap over it.")
    else:
        print("Ouch!")
        health = health - 30
    return health''']
BAD["p4i2"] = [('''def dodge_room(health):
    move = input("A boulder! jump or duck? ")
    if move == "jump":
        print("You leap over it.")
    else:
        health = health - 30
        return health''', "either way")]

GOOD["p4a1"] = ['''def shop(gold, health):
    answer = input("Buy a potion for 10 gold? ")
    if answer == "yes":
        if gold >= 10:
            gold = gold - 10
            health = health + 25
        else:
            print("You can't afford it.")
    return gold, health

gold = 15
health = 40
gold, health = shop(gold, health)
print(gold, health)''']
BAD["p4a1"] = [(GOOD["p4a1"][0].replace("return gold, health", "return health, gold"), "returns health first"),
(GOOD["p4a1"][0].replace("gold >= 10", "gold > 10"), "boundary"),
(GOOD["p4a1"][0].replace("gold, health = shop(gold, health)", "health, gold = shop(gold, health)"), "same order")]

GOOD["p4a2"] = ['''import random

def fight_room(health):
    goblin = 30
    while health > 0 and goblin > 0:
        hit = random.randint(5, 15)
        goblin = goblin - hit
        print("You hit for", hit)
        if goblin > 0:
            ouch = random.randint(5, 15)
            health = health - ouch
            print("The goblin hits for", ouch)
    return health''']
BAD["p4a2"] = [('''import random

def fight_room(health):
    goblin = 30
    while goblin > 0:
        goblin = goblin - random.randint(5, 15)
        health = health - random.randint(5, 15)
    return health''', "kept going after the player reached 0")]

GOOD["p5b2"] = ['''def cave():
    print("You squeeze into a dark cave.")

def river():
    print("You wade across a freezing river.")

way = input("Left or right? ").lower()
if way == "left":
    cave()
else:
    river()''']
BAD["p5b2"] = [('''def cave():
    print("You squeeze into a dark cave.")

def river():
    print("You wade across a freezing river.")

way = input("Left or right? ").lower()
if way == "left":
    cave()
else:
    cave()''', "river")]

GOOD["p5i1"] = ['''def trap_room(health):
    print("Spikes shoot up!")
    health = health - 20
    return health

def escaped():
    print("You escaped!")

def game_over():
    print("Game over.")

health = 50
room = 1
while room <= 3 and health > 0:
    health = trap_room(health)
    room = room + 1
if health > 0:
    escaped()
else:
    game_over()''']
BAD["p5i1"] = [(GOOD["p5i1"][0].replace("while room <= 3 and health > 0:", "while room <= 3:"), "and health > 0"),
(GOOD["p5i1"][0].replace("if health > 0:\n    escaped()\nelse:\n    game_over()", "escaped()\ngame_over()"), "only game_over")]

GOOD["p5a1"] = ['''def entrance():
    print("The entrance.")
    return "fork"

def fork():
    way = input("left or right? ")
    if way == "left":
        return "cave"
    else:
        return "exit"

def cave():
    print("A cave. Back you go.")
    return "fork"

location = "entrance"
while location != "exit":
    if location == "entrance":
        location = entrance()
    elif location == "fork":
        location = fork()
    elif location == "cave":
        location = cave()
print("Free!")''']
BAD["p5a1"] = [(GOOD["p5a1"][0].replace('''    if way == "left":
        return "cave"
    else:
        return "exit"''', '''    return "exit"'''), "two ways out")]

GOOD["p5a2"] = ['''def pit(health):
    print("You fall into a pit!")
    health = health - 40
    return "cave", health

location = "pit"
health = 100
while location != "exit" and health > 0:
    if location == "pit":
        location, health = pit(health)
    else:
        location = "exit"''']
BAD["p5a2"] = [(GOOD["p5a2"][0].replace('return "cave", health', 'return health, "cave"').replace("location, health = pit", "health, location = pit"), "returns health first"),
(GOOD["p5a2"][0].replace(' and health > 0', ''), "health runs out")]

GOOD["p6b1"] = ['''def library():
    print("Books everywhere.")

def treasure_room(gold):
    gold = gold + 10
    return gold

gold = 0
gold = treasure_room(gold)
library()
print("Gold:", gold)''']
BAD["p6b1"] = [('''def library():
    print("Books everywhere.")

def treasure_room(gold):
    gold = gold + 10
    return gold

gold = 0
treasure_room(gold)
library()
print("Gold:", gold)''', "catch it")]

GOOD["p6i1"] = ['''def hall():
    print("A long hall stretches ahead.")

def potion_room(health):
    print("You drink a potion.")
    health = health + 30
    return health

def trap_room(health):
    print("A dart hits you!")
    health = health - 10
    return health

health = 50
hall()
health = potion_room(health)
health = trap_room(health)
print("Health:", health)''']
BAD["p6i1"] = [(GOOD["p6i1"][0].replace('''    health = health - 10
    return health''', '''    return health
    health = health - 10'''), "after return"),
(GOOD["p6i1"][0].replace("    health = health + 30", "    health + 30"), "doesn't store it")]

GOOD["p6a1"] = ['''def shop(gold, health):
    if gold >= 10:
        gold = gold - 10
        health = health + 25
    return gold, health

def cellar():
    print("A damp cellar. Stairs lead up.")
    return "exit"

gold = 30
health = 50
gold, health = shop(gold, health)
print("Gold:", gold, " Health:", health)
location = "cellar"
while location != "exit":
    if location == "cellar":
        location = cellar()
print("You climb the stairs and escape.")''']
BAD["p6a1"] = [(GOOD["p6a1"][0].replace("gold, health = shop(gold, health)", "health, gold = shop(gold, health)"), "same order"),
(GOOD["p6a1"][0].replace('return "exit"', 'return "Exit"'), "fussy about capital letters")]

GOOD["p6a2"] = ['''def shop(gold, health):
    if gold >= 10:
        gold = gold - 10
        health = health + 25
    return gold, health

# Test plan for shop()
# normal: 30 gold -> 20 gold, health +25
# boundary: exactly 10 gold -> 0 gold, health +25
# refused: 9 gold and 0 gold -> nothing changes
print(shop(30, 50))
print(shop(10, 50))
print(shop(9, 50))
print(shop(0, 50))''']
BAD["p6a2"] = [('''def shop(gold, health):
    return gold, health

# normal: 30
print(shop(30, 50))''', "boundary data")]
