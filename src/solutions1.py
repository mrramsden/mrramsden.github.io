GOOD, BAD = {}, {}

GOOD["s1b2"] = ['print("Welcome, traveller.")\nprint("A torch flickers on the wall.")\nprint("You hear footsteps above you.")']
BAD["s1b2"] = [('print("Welcome, traveller.")\nprint()\nprint("You hear footsteps above you.")', "three lines")]

GOOD["s1b3"] = ['# Write your two print lines below\nprint("I can see a rusty gate.")\nprint("I can hear water dripping.")']
BAD["s1b3"] = [('# Write your two print lines below\nprint("I can see a rusty gate.")\n', "two print lines")]

GOOD["s1i1"] = ['''print("THE CAVE OF SHADOWS")
print()
print("You wake on a cold stone floor.")
print("The sign says 'Keep out!'")
print("Something moves in the dark.")''']
BAD["s1i1"] = [('''print("THE CAVE OF SHADOWS")
print("You wake on a cold stone floor.")
print("The sign says 'Keep out!'")
print("Something moves in the dark.")''', "blank line"),
('''print("THE CAVE OF SHADOWS")
print()
print("You wake on a cold stone floor.")
print("The sign says Keep out")
print("Something moves in the dark.")''', "speech")]

GOOD["s1i2"] = ['print("=" * 30)\nprint("THE CAVE OF SHADOWS")\nprint("=" * 30)']
BAD["s1i2"] = [('print("==============================")\nprint("THE CAVE")\nprint("==============================")', "string repetition")]

GOOD["s1a1"] = ['''print("=" * 30)
print("      ESCAPE THE DUNGEON")
print("=" * 30)
print("torch", "torch", "torch", sep=" ~ ")
print("You hear...", end=" ")
print("a growl.")''']
BAD["s1a1"] = [('''print("=" * 30)
print("ESCAPE THE DUNGEON")
print("=" * 30)
print("torch", "torch", "torch", sep=" ~ ")
print("You hear...", end=" ")
print("a growl.")''', "6 spaces"),
('''print("=" * 30)
print("      ESCAPE THE DUNGEON")
print("=" * 30)
print("torch ~ torch ~ torch")
print("You hear...", end=" ")
print("a growl.")''', "sep")]

GOOD["s1a2"] = ['''title = "THE GOBLIN KING"
width = 30
pad = (width - len(title)) // 2
print("=" * width)
print(" " * pad + title)
print("=" * width)''']
BAD["s1a2"] = [('''title = "THE GOBLIN KING"
width = 30
print("=" * 30)
print("       " + title)
print("=" * 30)''', "spaces before")]

GOOD["s2b2"] = ['''hero = input("What is your name? ")
weapon = input("What weapon do you carry? ")
print("Welcome, " + hero + "!")
print("You are holding a " + weapon)''']
BAD["s2b2"] = [('''hero = input("What is your name? ")
weapon = input("What weapon do you carry? ")
print("Welcome, " + hero + "!")
print("You are holding a " + "weapon")''', "word weapon")]

GOOD["s2b3"] = ['pet = input("What is your pet called? ")\nprint("Your loyal companion is " + pet)']
BAD["s2b3"] = [('pet = input("What is your pet called? ")\nprint("Your loyal companion is " + "pet")', "word pet")]

GOOD["s2i1"] = ['''name = input("Name? ")
weapon = input("Weapon? ")
cloak = input("Cloak colour? ")
print(name + " carries a " + weapon + " and wears a " + cloak + " cloak.")
print("Good luck, " + name + "!")''', '''name = input("Name? ")
weapon = input("Weapon? ")
cloak = input("Cloak colour? ")
print(name, "carries a", weapon, "and wears a", cloak, "cloak.")
print("Good luck,", name + "!")''']
BAD["s2i1"] = [('''name = input("Name? ")
weapon = input("Weapon? ")
cloak = input("Cloak colour? ")
print(name + "carries a" + weapon + "and wears a" + cloak + "cloak.")
print("Good luck, " + name + "!")''', "spaces between")]

GOOD["s2i2"] = ['''name = input("Name? ")
weapon = input("Weapon? ")
cloak = input("Cloak? ")
print(f"{name} carries a {weapon} and wears a {cloak} cloak.")
print(f"{name} the Brave enters the dungeon.")''']
BAD["s2i2"] = [('''name = input("Name? ")
weapon = input("Weapon? ")
cloak = input("Cloak? ")
print(name + " the Brave enters the dungeon.")''', "f-string")]

GOOD["s2a1"] = ['''name = input("Name? ").strip().title()
job = input("Class (warrior, mage or rogue)? ").strip().title()
home = input("Home town? ").strip().title()
print("-" * 30)
print(f"Name:  {name}")
print(f"Class: {job}")
print(f"Home:  {home}")
print("-" * 30)''']
BAD["s2a1"] = [('''name = input("Name? ")
job = input("Class? ")
home = input("Home town? ")
print("-" * 30)
print(f"Name:  {name}")
print(f"Class: {job}")
print(f"Home:  {home}")
print("-" * 30)''', "strip().title()")]

GOOD["s2a2"] = ['''name = input("Name? ").strip().title()
job = input("Class? ").strip().title()
home = input("Home? ").strip().title()
rows = [f"Name:  {name}", f"Class: {job}", f"Home:  {home}"]
w = max(len(r) for r in rows)
print("+" + "-" * (w + 2) + "+")
for r in rows:
    print("| " + r.ljust(w) + " |")
print("+" + "-" * (w + 2) + "+")''']
BAD["s2a2"] = [('''name = input("Name? ").strip().title()
job = input("Class? ").strip().title()
home = input("Home? ").strip().title()
print("+-----------------------+")
print("| Name:  " + name + " |")
print("| Class: " + job + " |")
print("| Home:  " + home + " |")
print("+-----------------------+")''', "same length")]

GOOD["s3b2"] = ['''gold = int(input("How much gold do you have? "))
price = 15
gold = gold - price
print("You bought a lantern. Gold left:", gold)''']
BAD["s3b2"] = [('''gold = int(input("How much gold do you have? "))
price = 15
gold = gold - 10
print("You bought a lantern. Gold left:", gold)''', "35 left")]

GOOD["s3b3"] = ['''potions = int(input("How many potions do you want? "))
cost = potions * 4
print("That will cost", cost, "gold.")''']
BAD["s3b3"] = [('''potions = int(input("How many potions do you want? "))
cost = 3 * 4
print("That will cost", cost, "gold.")''', "fixed number")]

GOOD["s3i1"] = ['''gold = int(input("How much gold do you have? "))
potions = int(input("How many potions do you want? "))
cost = potions * 4
gold = gold - cost
print("Total cost:", cost, "gold")
print("Gold left:", gold)''']
BAD["s3i1"] = [('''gold = input("How much gold do you have? ")
potions = int(input("How many potions do you want? "))
cost = potions * 4
print("Total cost:", cost, "gold")
print("Gold left:", gold - cost)''', "TypeError")]

GOOD["s3i2"] = ['''coins = int(input("How many coins? "))
people = int(input("How many people? "))
print("Each person gets", coins // people)
print("Left over:", coins % people)''']
BAD["s3i2"] = [('''coins = int(input("How many coins? "))
people = int(input("How many people? "))
print("Each person gets", coins / people)
print("Left over:", coins % people)''', "//")]

GOOD["s3a1"] = ['''copper = int(input("How many copper coins? "))
silver = copper // 12
copper = copper % 12
gold = silver // 20
silver = silver % 20
print(gold, "gold,", silver, "silver,", copper, "copper")''']
BAD["s3a1"] = [('''copper = int(input("How many copper coins? "))
gold = copper // 240
silver = copper // 12
copper = copper % 12
print(gold, "gold,", silver, "silver,", copper, "copper")''', "500")]

GOOD["s3a2"] = ['''g = int(input("Gold: "))
s = int(input("Silver: "))
c = int(input("Copper: "))
total = g * 240 + s * 12 + c
total = total - (240 + 3 * 12 + 4)
print("After the toll you have", total // 240, "gold,", total % 240 // 12, "silver,", total % 12, "copper")''']
BAD["s3a2"] = [('''g = int(input("Gold: "))
s = int(input("Silver: "))
c = int(input("Copper: "))
total = g * 240 + s * 12 + c - 280
print(total // 240, "gold,", total // 12, "silver,", total % 12, "copper")''', "16 silver")]

GOOD["s4b2"] = ['''torch = input("Do you light the torch? (yes/no) ")
if torch == "yes":
    print("The room fills with light.")
else:
    print("Something breathes in the dark...")''']
BAD["s4b2"] = [('''torch = input("Do you light the torch? (yes/no) ")
if torch == "Yes":
    print("The room fills with light.")
else:
    print("Something breathes in the dark...")''', "fill with light")]

GOOD["s4b3"] = ['''torch = input("Do you light the torch? (yes/no/maybe) ")
if torch == "yes":
    print("The room fills with light.")
elif torch == "maybe":
    print("You can't make up your mind. The torch goes out.")
else:
    print("It stays dark.")''']
BAD["s4b3"] = [('''torch = input("Do you light the torch? (yes/no/maybe) ")
if torch == "yes":
    print("The room fills with light.")
elif torch == maybe:
    print("You can't make up your mind. The torch goes out.")
else:
    print("It stays dark.")''', "NameError")]

GOOD["s4i1"] = ['''health = int(input("Health? "))
if health >= 70:
    print("You feel strong. Onwards!")
elif health >= 30:
    print("You are wounded. Be careful.")
else:
    print("You need a potion, fast!")''']
BAD["s4i1"] = [('''health = int(input("Health? "))
if health > 70:
    print("You feel strong. Onwards!")
elif health > 30:
    print("You are wounded. Be careful.")
else:
    print("You need a potion, fast!")''', "edge"),
('''health = int(input("Health? "))
if health >= 30:
    print("You are wounded. Be careful.")
elif health >= 70:
    print("You feel strong. Onwards!")
else:
    print("You need a potion, fast!")''', "strong")]

GOOD["s4i2"] = ['''torch = input("Light the torch? ").lower()
if torch == "yes" or torch == "y":
    print("The room fills with light.")
else:
    print("It stays dark.")''']
BAD["s4i2"] = [('''torch = input("Light the torch? ").lower()
if torch == "yes" or "y":
    print("The room fills with light.")
else:
    print("It stays dark.")''', "same message"),
('''torch = input("Light the torch? ")
if torch == "yes" or torch == "y":
    print("The room fills with light.")
else:
    print("It stays dark.")''', ".lower()")]

GOOD["s4a1"] = ['''p = input("Do you have a pass? ").strip().lower()
gold = int(input("How much gold do you have? "))
if p == "yes" or p == "y":
    print("The guard waves you through.")
elif gold >= 20:
    gold = gold - 20
    print("The guard takes 20 gold. You have", gold, "left.")
elif gold >= 10:
    print("The guard laughs. That's not enough.")
else:
    print("Go away!")''']
BAD["s4a1"] = [('''p = input("Do you have a pass? ")
gold = int(input("How much gold do you have? "))
if p == "yes":
    print("The guard waves you through.")
elif gold >= 20:
    gold = gold - 20
    print("The guard takes 20 gold. You have", gold, "left.")
elif gold >= 10:
    print("The guard laughs. That's not enough.")
else:
    print("Go away!")''', ".strip().lower()"),
('''p = input("Do you have a pass? ").strip().lower()
gold = int(input("How much gold do you have? "))
if p == "yes" or p == "y":
    print("The guard waves you through.")
elif gold > 20:
    gold = gold - 20
    print("The guard takes 20 gold. You have", gold, "left.")
elif gold > 10:
    print("The guard laughs. That's not enough.")
else:
    print("Go away!")''', ">=")]

GOOD["s4a2"] = ['''p = input("Do you have a pass? ").strip().lower()
gold = int(input("How much gold do you have? "))
if gold < 0:
    print("That's not possible.")
elif p == "yes" or p == "y":
    name = input("Your name? ").strip().title()
    if name in ["Asha", "Bram", "Cora"]:
        print("Welcome, your highness.")
    else:
        print("The guard waves you through.")
elif gold >= 20:
    gold = gold - 20
    print("The guard takes 20 gold. You have", gold, "left.")
elif gold >= 10:
    print("The guard laughs. That's not enough.")
else:
    print("Go away!")''', '''p = input("Do you have a pass? ").strip().lower()
if p == "yes" or p == "y":
    name = input("Your name? ")
    if name in ["Asha", "Bram", "Cora"]:
        print("Welcome, your highness.")
    else:
        print("The guard waves you through.")
else:
    gold = int(input("How much gold do you have? "))
    if gold < 0:
        print("That's not possible.")
    elif gold >= 20:
        print("The guard takes 20 gold. You have", gold - 20, "left.")
    elif gold >= 10:
        print("The guard laughs. That's not enough.")
    else:
        print("Go away!")''']
BAD["s4a2"] = [('''p = input("Do you have a pass? ").strip().lower()
gold = int(input("How much gold do you have? "))
if gold < 0:
    print("That's not possible.")
if p == "yes" or p == "y":
    print("The guard waves you through.")
elif gold >= 20:
    print("The guard takes 20 gold.", gold - 20)
elif gold >= 10:
    print("The guard laughs. That's not enough.")
else:
    print("Go away!")''', "nothing else")]

GOOD["s5b2"] = ['''password = "dragon"
guess = input("Enter the password: ")
while guess != password:
    print("Wrong! Try again.")
    guess = input("Enter the password: ")
print("Door unlocked!")''']
BAD["s5b2"] = [('''password = "dragon"
guess = input("Enter the password: ")
while guess != password:
    print("Wrong! Try again.")
    guess = password
print("Door unlocked!")''', "Gap 2")]

GOOD["s5b3"] = ['''count = 5
while count >= 1:
    print(count)
    count = count - 1
print("The trap door opens!")''']
BAD["s5b3"] = [('''count = 5
while count >= 1:
    print(count)
    count = count
print("The trap door opens!")''', "never ends")]

GOOD["s5i1"] = ['''secret = 7
guesses = 1
guess = int(input("Guess the number (1-20): "))
while guess != secret:
    if guess > secret:
        print("Too high!")
    else:
        print("Too low!")
    guess = int(input("Guess again: "))
    guesses = guesses + 1
print("You got it! Guesses taken:", guesses)''']
BAD["s5i1"] = [('''secret = 7
guesses = 0
guess = int(input("Guess the number (1-20): "))
while guess != secret:
    if guess > secret:
        print("Too high!")
    else:
        print("Too low!")
    guess = int(input("Guess again: "))
    guesses = guesses + 1
print("You got it! Guesses taken:", guesses)''', "counter at 1"),
('''secret = 7
guesses = 1
guess = int(input("Guess the number (1-20): "))
while guess != secret:
    if guess < secret:
        print("Too high!")
    else:
        print("Too low!")
    guess = int(input("Guess again: "))
    guesses = guesses + 1
print("You got it! Guesses taken:", guesses)''', "which way round")]

GOOD["s5i2"] = ['''password = "dragon"
tries = 1
guess = input("Password: ")
while guess != password and tries < 3:
    print("Wrong!")
    guess = input("Password: ")
    tries = tries + 1
if guess == password:
    print("Door unlocked!")
else:
    print("The door remains locked.")''']
BAD["s5i2"] = [('''password = "dragon"
tries = 0
guess = input("Password: ")
while guess != password and tries < 3:
    print("Wrong!")
    guess = input("Password: ")
    tries = tries + 1
if guess == password:
    print("Door unlocked!")
else:
    print("The door remains locked.")''', "stop asking")]

GOOD["s5a1"] = ['''import random

secret = random.randint(1, 50)
guesses = 0
won = False
while guesses < 7 and not won:
    typed = input("Your guess: ").strip()
    if not typed.isdigit():
        print("That's not a whole number.")
    else:
        guess = int(typed)
        guesses = guesses + 1
        if guess == secret:
            won = True
        elif guess > secret:
            print("Too high!")
        else:
            print("Too low!")
if won:
    print("You got it in", guesses, "guesses!")
else:
    print("Out of guesses. It was", secret)''']
BAD["s5a1"] = [('''import random

secret = random.randint(1, 50)
guesses = 0
won = False
while guesses < 7 and not won:
    guess = int(input("Your guess: "))
    guesses = guesses + 1
    if guess == secret:
        won = True
    elif guess > secret:
        print("Too high!")
    else:
        print("Too low!")
print("Game over")''', "ValueError"),
('''import random

secret = random.randint(1, 50)
guesses = 0
won = False
while not won:
    typed = input("Your guess: ")
    if typed.isdigit():
        guesses = guesses + 1
        if int(typed) == secret:
            won = True
        elif int(typed) > secret:
            print("Too high!")
        else:
            print("Too low!")
print("Done in", guesses)''', "only gets 7 guesses")]

GOOD["s6b2"] = ['for step in range(3):\n    print("You take a step forward.")\nprint("You reach the end of the corridor.")']
BAD["s6b2"] = [('for step in range(1, 3):\n    print("You take a step forward.")\nprint("You reach the end of the corridor.")', "took 2 steps")]

GOOD["s6b3"] = ['for letter in "ASHA":\n    print(letter)\n    print("*")']
BAD["s6b3"] = [('for letter in "ASHA":\n    print(letter)\nprint("*")', "indented")]

GOOD["s6i1"] = ['''strength = int(input("Sword strength: "))
for hits in range(1, 13):
    print(hits, "x", strength, "=", hits * strength)''']
BAD["s6i1"] = [('''strength = int(input("Sword strength: "))
for hits in range(1, 12):
    print(hits, "x", strength, "=", hits * strength)''', "range(1, 13)")]

GOOD["s6i2"] = ['''total = 0
for chest in range(1, 6):
    coins = int(input("Coins in chest " + str(chest) + ": "))
    total = total + coins
print("Total:", total)''']
BAD["s6i2"] = [('''for chest in range(1, 6):
    total = 0
    coins = int(input("Coins in chest " + str(chest) + ": "))
    total = total + coins
print("Total:", total)''', "Start total at 0")]

GOOD["s6a1"] = ['''height = int(input("How tall is the staircase? "))
for row in range(1, height + 1):
    for col in range(row):
        print("#", end="")
    print()''']
BAD["s6a1"] = [('''height = int(input("How tall is the staircase? "))
for row in range(1, height + 1):
    print("#" * row)''', "bans string repetition"),
('''height = int(input("How tall is the staircase? "))
for row in range(height):
    for col in range(row):
        print("#", end="")
    print()''', "Height 4")]

GOOD["s6a2"] = ['''row = int(input("Player row (1-5): "))
col = int(input("Player column (1-5): "))
# A for loop is better: we know there are exactly 5 rows and 5 columns
for r in range(1, 6):
    for c in range(1, 6):
        if r == row and c == col:
            print("P", end=" ")
        else:
            print(".", end=" ")
    print()''']
BAD["s6a2"] = [('''row = int(input("Player row (1-5): "))
col = int(input("Player column (1-5): "))
for r in range(5):
    for c in range(5):
        if r == row and c == col:
            print("P", end=" ")
        else:
            print(".", end=" ")
    print()''', "row 2, column 4")]

GOOD["s7b1"] = ['''# THE FINAL ESCAPE
print("THE FINAL ESCAPE")
name = input("What is your name? ")

door = input("Do you go left or right? ")
if door == "left":
    print("You find a ladder.")
else:
    print("You fall into a pit, but climb out.")

password = "freedom"
guess = input("Enter the password: ")
while guess != password:
    print("Wrong! Try again.")
    guess = input("Enter the password: ")

for step in range(1, 4):
    print("Step", step)

print("You escaped, " + name + "!")''']
BAD["s7b1"] = [('''print("THE FINAL ESCAPE")
name = input("What is your name? ")
door = input("Do you go left or right? ")
if door == "left":
    print("You find a ladder.")
else:
    print("You find a ladder.")
password = "freedom"
guess = input("Enter the password: ")
while guess != password:
    guess = input("Enter the password: ")
for step in range(1, 4):
    print("Step", step)
print("You escaped, " + name + "!")''', "different messages"),
('''print("THE FINAL ESCAPE")
name = input("What is your name? ")
door = input("Do you go left or right? ")
if door == "left":
    print("Ladder.")
else:
    print("Pit.")
password = "freedom"
guess = input("Enter the password: ")
while guess != password:
    guess = input("Enter the password: ")
for step in range(1, 4):
    print("Step", step)
print("You escaped, name!")''', "player's name")]

GOOD["s7b2"] = [GOOD["s7b1"][0].replace('for step in range(1, 4):\n    print("Step", step)', 'gold = 0\nfor step in range(1, 4):\n    print("Step", step)\n    gold = gold + 5\nprint("You escaped with", gold, "gold")')]
BAD["s7b2"] = [(GOOD["s7b1"][0].replace('for step in range(1, 4):\n    print("Step", step)', 'for step in range(1, 4):\n    gold = 0\n    print("Step", step)\n    gold = gold + 5\nprint("Gold:", gold)'), "gold = 0 before the loop")]

GOOD["s7i1"] = ['''name = input("Name? ")
gold = int(input("Gold? "))
way = input("left, right or down? ")
if way == "left":
    gold = gold + 10
elif way == "right":
    gold = gold - 5
else:
    print("Down you go")
answer = input("Riddle: what has keys but no locks? ")
while answer != "piano":
    answer = input("Try again: ")
for t in range(3):
    print("Torch", t + 1)
print("Well done", name)''']
BAD["s7i1"] = [('''name = input("Name? ")
way = input("left or right? ")
if way == "left":
    print("Left")
else:
    print("Right")
for t in range(3):
    print("Torch")''', "while loop")]

GOOD["s7a1"] = ['''import random

health = 100
gold = 0
room = 1
while room <= 5 and health > 0:
    event = random.randint(1, 3)
    if event == 1:
        health = health - random.randint(10, 30)
    elif event == 2:
        gold = gold + random.randint(5, 20)
    else:
        if input("What has keys but no locks? ").lower() != "piano":
            health = health - 15
    room = room + 1
escaped = False
if health > 0:
    for attempt in range(3):
        if input("Password: ") == "freedom":
            escaped = True
            break
print("Health:", health, "Gold:", gold, "Escaped:", escaped)''']
BAD["s7a1"] = [('''import random

health = 100
gold = 0
for room in range(5):
    event = random.randint(1, 3)
    if event == 1:
        health = health - random.randint(10, 30)
    elif event == 2:
        gold = gold + random.randint(5, 20)
print(health, gold)''', "while condition")]
