# Content for the Python Rescue support pack.
# Every code sample here is run by test_pack.py before the page is built.

TOPICS = []

# Shared check helpers, pasted in front of each check.
H = r'''
def solid(text):
    return [l.strip() for l in text.split("\n") if l.strip()]

def after(r, n):
    return "\n".join(r.out.split("\n")[n:])

async def try_run(typed, what):
    try:
        return await C.rerun(typed)
    except CheckFail as e:
        if "never ends" in str(e):
            fail(what + " it got stuck in a loop that never ends. " + LOOP_TIP)
        if "more answers" in str(e) and ASK_TIP:
            fail(what + " it asked for the password again. " + ASK_TIP)
        raise
LOOP_TIP = ""
ASK_TIP = ""
'''

# ====================================================================
TOPICS.append({
    "id": "ind", "title": "Indentation", "colour": "blue",
    "tag": "Start here if Python keeps saying IndentationError.",
    "aim": ["Know which lines belong to a block", "Fix indentation errors on your own", "Test both ways through an if"],
    "learn": """<p>Python uses the spaces at the start of a line to work out which lines belong together. Those spaces are called <strong>indentation</strong>, and Python takes them very seriously.</p>
<ol class="rules">
<li>A line that ends with a colon <code>:</code> starts a <strong>block</strong>.</li>
<li>Every line in the block is indented one step: <strong>4 spaces</strong>. Press <kbd>Tab</kbd> rather than counting spaces.</li>
<li>All the lines in a block line up exactly.</li>
<li>To finish the block, go back out with <kbd>Shift</kbd>+<kbd>Tab</kbd>. That line runs whatever happened in the block.</li>
<li>A block can hold another block. That's two steps in: 8 spaces.</li>
</ol>""",
    "example": '''score = int(input("Your score? "))
if score >= 5:
    print("Well done!")
    print("You passed.")
print("Thanks for playing.")''',
    "example_note": "The shading shows the block. Lines 3 and 4 are inside the if, so they only run when the score is 5 or more. Line 5 is back out, so it always runs. Run it twice: once with 7, then with 2.",
    "puzzle": {
        "prompt": "Only tell people to wear sun cream when it's hot. Everyone should get <code>Have a good day.</code>",
        "lines": [('temp = int(input("Temperature? "))', 0), ("if temp > 25:", 0), ('print("It\'s hot today!")', 1),
                  ('print("Wear sun cream.")', 1), ('print("Have a good day.")', 0)],
    },
    "fix": {
        "html": "<p>This should greet Sam with two lines. Everyone, including Sam, gets <code>Bye for now.</code> Press <strong>Run</strong> to see the error, read the hint, then fix it.</p>",
        "starter": '''name = input("What's your name? ")
if name == "Sam":
print("Hi Sam!")
  print("Good to see you again.")
print("Bye for now.")''',
        "check": {"inputs": ["Sam"], "win": "Both hello lines are in the block, and everyone gets the goodbye.", "py": H + r'''
ls = solid(out)
if "Hi Sam!" not in out or "Good to see you again." not in out:
    fail("When I typed Sam, I should get both `Hi Sam!` and `Good to see you again.` Both lines belong inside the if, so both need one step of indent.")
if "Bye for now." not in out:
    fail("When I typed Sam, it should end with `Bye for now.`")
r = await C.rerun(["Ali"])
if "Hi Sam" in r.out or "Good to see you" in r.out:
    fail("When I typed Ali, it still said a hello line meant for Sam. Every hello line must be indented inside the if.")
if "Bye for now." not in r.out:
    fail("When I typed Ali, it should still say `Bye for now.` That line belongs back out, with no indent.")
'''},
    },
    "test": {
        "html": """<p><strong>The spec:</strong> with 10 coins or more you buy a ride ticket, pay 10 coins and see <code>Enjoy the ride!</code>. With fewer than 10 you see <code>Not enough coins.</code> Everyone sees how many coins they have left.</p>
<p>This code runs without errors, but one line is in the wrong block. Use the test table to find it: run the program once for each row and tick what happened. Then fix it.</p>""",
        "starter": '''coins = int(input("How many coins? "))
if coins >= 10:
    print("You buy a ticket.")
    coins = coins - 10
else:
    print("Not enough coins.")
    print("Enjoy the ride!")
print("Coins left:", coins)''',
        "table": [("Normal", "15", "Ticket, Enjoy the ride!, 5 left"), ("Boundary", "10", "Ticket, Enjoy the ride!, 0 left"),
                  ("Boundary", "9", "Not enough coins, 9 left"), ("Normal", "0", "Not enough coins, 0 left")],
        "check": {"inputs": ["15"], "win": "Every test passes. That's what testing is for: the code ran fine, but it was wrong.", "py": H + r'''
for typed, ticket, left in [("15", True, 5), ("10", True, 0), ("9", False, 9), ("0", False, 0)]:
    r = await C.rerun([typed])
    text = after(r, 1)
    if ticket and "Enjoy the ride!" not in text:
        fail(f"I typed {typed}. That buys a ticket, so it should say `Enjoy the ride!` The line is in the wrong block: it belongs with the ticket lines.")
    if not ticket and "Enjoy the ride!" in text:
        fail(f"I typed {typed}. That isn't enough for a ticket, but it still said `Enjoy the ride!` Move that line into the if block, with the ticket lines.")
    if not re.search(r"Coins left:\s*" + str(left) + r"\b", text):
        fail(f"I typed {typed}. It should finish with `Coins left: {left}`.")
'''},
    },
    "quiz": [
        {"q": "What's the best way to indent a line in these code boxes?", "o": ["Press the space bar once", "Press Tab, which adds 4 spaces", "Press Enter twice", "Type a colon"], "a": 1,
         "e": "Tab adds exactly 4 spaces, so your lines always line up. Shift+Tab takes 4 away."},
        {"q": "What will this print?", "code": 'x = 3\nif x > 5:\n    print("A")\n    print("B")\nprint("C")', "o": ["A, B, C", "C", "B, C", "Nothing"], "a": 1,
         "e": "3 isn't more than 5, so the whole indented block is skipped: A and B. C is back out, so it always prints."},
        {"q": "Python says IndentationError: expected an indented block. What's wrong?", "o": ["A line is indented too far", "The line after a colon isn't indented", "A bracket is missing", "A variable is misspelt"], "a": 1,
         "e": "A colon promises a block. Python expected the next line to be indented, and it wasn't."},
        {"q": "Which line is wrong?", "code": 'if age > 12:\n    print("Teen ticket")\n     print("Enjoy the film")', "o": ["Line 1", "Line 2", "Line 3", "None of them"], "a": 2,
         "e": "Line 3 has 5 spaces, so it doesn't line up with line 2. Lines in the same block must line up exactly."},
    ],
})

# ====================================================================
TOPICS.append({
    "id": "if", "title": "if statements", "colour": "green",
    "tag": "if, elif and else: making choices.",
    "aim": ["Line up if, elif and else", "Know that only one block runs", "Test the boundaries"],
    "learn": """<p>An <code>if</code> lets your program choose. Python checks each condition from the top. It runs the block of the <strong>first</strong> one that's True and skips all the rest.</p>
<ul>
<li><code>if</code>, <code>elif</code> and <code>else</code> all <strong>line up</strong> with each other, and each ends with a colon.</li>
<li>Each one's block is indented one step underneath it.</li>
<li><code>else</code> has no condition. It catches everything that's left.</li>
</ul>""",
    "example": '''battery = int(input("Battery %? "))
if battery >= 50:
    print("You're fine.")
elif battery >= 20:
    print("Charge it soon.")
else:
    print("Charge it now!")
print("Phone check done.")''',
    "example_note": "if, elif and else start in the same place. Try 80, then 30, then 5: a different block runs each time, but Phone check done. always appears.",
    "puzzle": {
        "prompt": "Under 12 pays 5 pounds, 12 to 64 pays 9 pounds, and 65 or over pays 6 pounds. Everyone is told their price.",
        "lines": [('age = int(input("How old are you? "))', 0), ("if age < 12:", 0), ("price = 5", 1), ("elif age < 65:", 0),
                  ("price = 9", 1), ("else:", 0), ("price = 6", 1), ('print("Your ticket costs", price, "pounds")', 0)],
    },
    "fix": {
        "html": "<p><strong>The spec:</strong> 40 or more is grade A, 25 to 39 is B, below 25 is C. <strong>Everyone</strong> sees <code>Well done for finishing!</code></p><p>There are two indentation bugs. Python will spot one. You'll need to test to find the other.</p>",
        "starter": '''mark = int(input("Mark out of 50? "))
if mark >= 40:
    print("Grade: A")
    elif mark >= 25:
    print("Grade: B")
else:
    print("Grade: C")
    print("Well done for finishing!")''',
        "check": {"inputs": ["45"], "win": "Right grade every time, and everyone is praised.", "py": H + r'''
for typed, grade in [("45", "A"), ("40", "A"), ("39", "B"), ("25", "B"), ("24", "C"), ("0", "C")]:
    r = await C.rerun([typed])
    text = after(r, 1)
    got = re.findall(r"Grade:\s*([ABC])", text)
    if got != [grade]:
        fail(f"I typed {typed}. It should say `Grade: {grade}`" + (f", but it said Grade: {', '.join(got)}." if got else ", but no grade appeared."))
    if "Well done for finishing!" not in text:
        fail(f"I typed {typed} and didn't get `Well done for finishing!` Everyone should see it, so it belongs back out, with no indent.")
'''},
    },
    "test": {
        "html": """<p><strong>The spec:</strong> 50% or more says <code>You're fine.</code>, 20% to 49% says <code>Charge it soon.</code>, and below 20% says <code>Charge it now!</code></p>
<p>This looks right, and it works for 80 and 5. But bugs love to hide on the <strong>boundaries</strong>: the exact numbers where the answer changes. Run every row of the test table, find the bugs, then fix them.</p>""",
        "starter": '''battery = int(input("Battery %? "))
if battery > 50:
    print("You're fine.")
elif battery > 20:
    print("Charge it soon.")
else:
    print("Charge it now!")''',
        "table": [("Normal", "80", "You're fine."), ("Boundary", "50", "You're fine."), ("Boundary", "49", "Charge it soon."),
                  ("Boundary", "20", "Charge it soon."), ("Boundary", "19", "Charge it now!"), ("Normal", "5", "Charge it now!")],
        "check": {"inputs": ["80"], "win": "Spot on at every boundary.", "py": H + r'''
for typed, want in [("80", "You're fine."), ("50", "You're fine."), ("49", "Charge it soon."), ("20", "Charge it soon."), ("19", "Charge it now!"), ("5", "Charge it now!"), ("100", "You're fine."), ("0", "Charge it now!")]:
    r = await C.rerun([typed])
    text = after(r, 1)
    if want not in text:
        tip = {"50": " That's a boundary. The spec says 50% or more, so the test needs >= not >.",
               "20": " That's a boundary. The spec says 20% to 49% is Charge it soon, so 20 counts: use >= not >."}.get(typed, "")
        fail(f"I typed {typed}. It should say: `{want}`{tip}")
'''},
    },
    "quiz": [
        {"q": "What will this print?", "code": 'temp = 30\nif temp > 20:\n    print("Warm")\nelif temp > 25:\n    print("Hot")\nelse:\n    print("Cold")', "o": ["Warm", "Hot", "Warm, then Hot", "Cold"], "a": 0,
         "e": "30 > 20 is True, so Warm prints and Python skips the rest. elif is only checked if everything above it was False."},
        {"q": "What will this print?", "code": 'score = 10\nif score > 5:\n    print("Good")\nif score > 8:\n    print("Great")', "o": ["Good", "Great", "Good, then Great", "Nothing"], "a": 2,
         "e": "These are two separate ifs, not if and elif, so Python checks both. Both are True."},
        {"q": "What's missing from this code?", "code": 'if colour == "red"\n    print("Stop")', "o": ["A bracket", "A colon at the end of line 1", "An else", "Nothing"], "a": 1,
         "e": "Every if, elif and else line ends with a colon. The colon tells Python a block is coming."},
        {"q": "The rule is: if age >= 13. Which age is the boundary test?", "o": ["13", "20", "5", "thirteen"], "a": 0,
         "e": "13 is exactly where the answer changes. Test 13 and 12, because that's where bugs hide."},
    ],
})

# ====================================================================
TOPICS.append({
    "id": "loop", "title": "Loops", "colour": "amber",
    "tag": "for and while: doing things again and again.",
    "aim": ["Put the right lines inside the loop", "Make a while loop stop", "Test more than the easy case"],
    "learn": """<p>A loop repeats its block. The indented lines run every time round. The first line that's back out runs <strong>once</strong>, after the loop has finished.</p>
<ul>
<li><code>for</code> repeats a set number of times: <code>for lap in range(3):</code> goes round 3 times.</li>
<li><code>while</code> repeats as long as its condition is True. Something inside the loop must change, or it never stops.</li>
<li>Ask yourself about every line: <strong>should this happen every time, or just once?</strong> Every time means indented. Once means back out.</li>
</ul>""",
    "example": '''for lap in range(1, 4):
    print("Lap", lap)
    print("Keep going!")
print("Race finished!")''',
    "example_note": "Lines 2 and 3 are in the loop, so they run 3 times. Line 4 is back out, so it runs once at the end.",
    "puzzle": {
        "prompt": "Ask for 3 scores and add each one to the total. Show the total once, at the end.",
        "lines": [("total = 0", 0), ("for game in range(3):", 0), ('score = int(input("Score? "))', 1),
                  ("total = total + score", 1), ('print("Total score:", total)', 0)],
    },
    "fix": {
        "html": "<p>This should show all five square numbers, then say <code>All done!</code> once. It runs without an error, but it's wrong. Run it, spot the problem, then fix it.</p>",
        "starter": '''for number in range(1, 6):
    square = number * number
print(number, "squared is", square)
print("All done!")''',
        "check": {"win": "Five squares, then All done! just once.", "py": H + r'''
ls = solid(out)
want = [f"{n} squared is {n * n}" for n in range(1, 6)]
got = [l for l in ls if "squared is" in l]
if got != want:
    fail(f"It printed {len(got)} square line(s). It should print all five, from `1 squared is 1` to `5 squared is 25`. Which line needs to happen every time round the loop?")
if ls.count("All done!") != 1:
    fail("`All done!` should appear once. If it appears five times, it's inside the loop: move it back out.")
if ls[-1] != "All done!":
    fail("`All done!` should be the very last line.")
'''},
    },
    "test": {
        "html": """<p><strong>The spec:</strong> keep asking for the password until it's <code>pizza42</code>, saying <code>Wrong password, try again.</code> after each wrong one. Then say <code>Welcome in!</code></p>
<p>Type the right password first and it looks nearly fine. That's the trap! Run every row of the test table, including the wrong ones. (If a loop never ends, press <strong>Stop</strong>.)</p>""",
        "starter": '''password = input("Password? ")
while password != "pizza42":
    print("Wrong password, try again.")
password = input("Password? ")
print("Welcome in!")''',
        "table": [("Normal", "pizza42", "Welcome in!"), ("Wrong first", "cheese, then pizza42", "One wrong message, then Welcome in!"),
                  ("Wrong twice", "a, b, then pizza42", "Two wrong messages, then Welcome in!"), ("Capitals", "PIZZA42, then pizza42", "Wrong (capitals count), then Welcome in!")],
        "check": {"inputs": ["pizza42", "pizza42"], "loop_tip": "Testing only with the right password hides this bug. The line that asks again has to be inside the loop.", "win": "Right first time or after ten tries, it works. Great testing.", "py": H + r'''
LOOP_TIP = "The line that asks again has to be inside the loop, or the password never changes."
ASK_TIP = "The line that asks again should only run inside the loop, after a wrong answer. Indent it into the loop."
for typed in (["pizza42"], ["cheese", "pizza42"], ["a", "b", "pizza42"], ["PIZZA42", "pizza42"]):
    shown = ", then ".join(typed)
    r = await try_run(typed, f"I typed {shown}, and")
    wrongs = r.out.count("Wrong password")
    if r.used != len(typed):
        fail(f"I typed {shown}. It should keep asking until pizza42, then stop asking.")
    if wrongs != len(typed) - 1:
        fail(f"I typed {shown}. It should say `Wrong password, try again.` {len(typed) - 1} time(s), but it said it {wrongs} time(s).")
    if "Welcome in!" not in r.out:
        fail(f"I typed {shown}. It should end with `Welcome in!`")
'''},
    },
    "quiz": [
        {"q": "How many times does the block of for go in range(4): run?", "o": ["3", "4", "5", "Forever"], "a": 1,
         "e": "range(4) gives 0, 1, 2 and 3. That's 4 numbers, so 4 times round."},
        {"q": "What will this print?", "code": 'for i in range(3):\n    print("Hi")\nprint("Bye")', "o": ["Hi, Bye, Hi, Bye, Hi, Bye", "Hi, Hi, Hi, Bye", "Hi, Bye", "Hi, Hi, Hi, Bye, Bye, Bye"], "a": 1,
         "e": "Only the indented line repeats. Bye is back out, so it runs once at the end."},
        {"q": "What will this print?", "code": "n = 1\nwhile n < 10:\n    n = n * 2\nprint(n)", "o": ["8", "10", "16", "1, 2, 4, 8"], "a": 2,
         "e": "n goes 1, 2, 4, 8, 16. When n is 16, n < 10 is False and the loop stops. The print is back out, so it shows 16 once."},
        {"q": "A while loop never stops. What's the most likely cause?", "o": ["It has too many lines", "Nothing inside the loop changes the condition", "print is inside the loop", "It needs range()"], "a": 1,
         "e": "The condition is checked every time round. If nothing inside the loop changes it, it stays True forever."},
    ],
})

# ====================================================================
TOPICS.append({
    "id": "sub", "title": "Subroutines", "colour": "purple",
    "tag": "def, calling, parameters and return.",
    "aim": ["Keep a subroutine's lines inside its def", "Call it from the main program", "Use return to send a value back"],
    "learn": """<p>A subroutine is a named block of code. You write it once with <code>def</code>, then use it whenever you like by <strong>calling</strong> it.</p>
<ul>
<li>The <code>def</code> line ends with a colon, and the lines that belong to the subroutine are indented underneath it.</li>
<li><code>def</code> only <strong>defines</strong> it. Nothing happens until you call it, like <code>greet("Priya")</code>.</li>
<li>Calls usually go in the <strong>main program</strong> at the bottom, with no indent.</li>
<li><code>return</code> sends a value back to wherever it was called. It must be indented inside the def.</li>
</ul>""",
    "example": '''def greet(name):
    print("Hello", name)
    print("Welcome to coding club!")

greet("Priya")
greet("Leo")''',
    "example_note": "Lines 2 and 3 belong to greet. Lines 5 and 6 are the main program: two calls, so the welcome happens twice, once for each name.",
    "puzzle": {
        "prompt": "The three menu lines belong to show_menu. Then the main program shows the menu and asks for a choice.",
        "lines": [("def show_menu():", 0), ('print("1. Pizza")', 1), ('print("2. Pasta")', 1), ('print("3. Salad")', 1),
                  ("show_menu()", 0), ('choice = input("Pick 1, 2 or 3: ")', 0)],
    },
    "fix": {
        "html": "<p>This should print the title <code>== Number Machine ==</code>, then <code>8</code>, then <code>20</code>. There are two indentation bugs. Python will tell you about one. The other is silent: the title never appears.</p>",
        "starter": '''def double(number):
    answer = number * 2
return answer

def show_title():
    print("== Number Machine ==")
    show_title()

print(double(4))
print(double(10))''',
        "check": {"win": "Title, 8, 20. Both bugs fixed.", "py": H + r'''
ls = solid(out)
if "== Number Machine ==" not in ls:
    fail("The title doesn't appear. The call `show_title()` is indented, so it's inside the def and never runs. Move it back out, above the prints.")
if ls != ["== Number Machine ==", "8", "20"]:
    fail("It should print exactly three lines: the title, then 8, then 20. Yours printed: " + " / ".join(ls))
r = await C.call("double", 7)
if r.ret != 14:
    fail("I tested `double(7)`. It should return 14.")
'''},
    },
    "test": {
        "html": """<p><strong>The spec:</strong> <code>area(width, height)</code> sends back the area of a rectangle. The main program adds two rooms together, which should give <code>Total floor: 22</code>.</p>
<p>Run it: the areas print, then it crashes. Test the subroutine with the table (you can add lines like <code>print(area(3, 4))</code> to test), then fix it.</p>""",
        "starter": '''def area(width, height):
    print(width * height)

room1 = area(3, 4)
room2 = area(2, 5)
print("Total floor:", room1 + room2)''',
        "table": [("Normal", "area(3, 4)", "Sends back 12"), ("Normal", "area(2, 5)", "Sends back 10"),
                  ("Boundary", "area(0, 7)", "Sends back 0"), ("Whole program", "Run it", "Total floor: 22")],
        "check": {"win": "area sends its answer back, so the main program can use it.", "py": H + r'''
C.need("area", 2)
for w, h in [(3, 4), (2, 5), (0, 7), (6, 6)]:
    r = await C.call("area", w, h)
    if r.ret is None:
        fail(f"I tested `area({w}, {h})` and nothing came back. Printing shows the answer, but only `return` sends it back. Write `return width * height`.")
    if r.ret != w * h:
        fail(f"I tested `area({w}, {h})`. It should send back {w * h}, but sent back {r.ret!r}.")
if not re.search(r"Total floor:\s*22\b", out):
    fail("The main program should finish with `Total floor: 22`.")
'''},
    },
    "quiz": [
        {"q": "What will this print?", "code": 'def cheer():\n    print("Go team!")\n\nprint("Start")', "o": ["Go team!, then Start", "Start", "Start, then Go team!", "Nothing"], "a": 1,
         "e": "def only defines cheer. Nothing calls cheer(), so Go team! never prints."},
        {"q": "What will this print?", "code": "def add_bonus(score):\n    return score + 5\n\npoints = add_bonus(10)\nprint(points)", "o": ["10", "5", "15", "add_bonus"], "a": 2,
         "e": "10 goes in as score. return sends back 15, which is stored in points."},
        {"q": "Where does the line that calls a subroutine usually go?", "o": ["Indented inside its own def", "In the main program, with no indent", "Above the def, indented", "Anywhere: indentation doesn't matter"], "a": 1,
         "e": "If you indent the call inside its own def, it becomes part of the subroutine and never runs."},
        {"q": "What does return do?", "o": ["Prints the answer", "Sends a value back to where the subroutine was called", "Starts the subroutine again", "Ends the whole program"], "a": 1,
         "e": "return hands a value back, so the main program can store it or use it, like total = area(3, 4)."},
    ],
})

# ====================================================================
DOCTOR = [
    {"err": "IndentationError: expected an indented block", "means": "A line ends with a colon, so Python expected a block, but the next line isn't indented.",
     "bad": 'if score > 5:\nprint("Well done")', "good": 'if score > 5:\n    print("Well done")',
     "fix": "Click at the start of the line after the colon and press Tab.", "topic": "ind"},
    {"err": "IndentationError: unexpected indent", "means": "This line is indented, but nothing above it started a block.",
     "bad": 'name = "Sam"\n    print(name)', "good": 'name = "Sam"\nprint(name)',
     "fix": "Press Shift+Tab so it lines up with the line above. Or is the line above missing its colon?", "topic": "ind"},
    {"err": "IndentationError: unindent does not match any outer indentation level", "means": "This line doesn't line up with any line above it. Usually it has 1, 2 or 3 spaces too many or too few.",
     "bad": 'if score > 5:\n    print("Well done")\n  print("Bye")', "good": 'if score > 5:\n    print("Well done")\nprint("Bye")',
     "fix": "Indents come in steps of 4. Use Shift+Tab or Tab until it lines up exactly.", "topic": "ind"},
    {"err": "SyntaxError: invalid syntax (on an elif or else line)", "means": "elif and else must start in exactly the same place as their if.",
     "bad": 'if mark >= 40:\n    print("A")\n    else:\n    print("B")', "good": 'if mark >= 40:\n    print("A")\nelse:\n    print("B")',
     "fix": "Press Shift+Tab on the elif or else line until it lines up with the if.", "topic": "if"},
    {"err": "SyntaxError: expected ':'", "means": "if, elif, else, for, while and def lines all end with a colon.",
     "bad": 'while lives > 0\n    play()', "good": 'while lives > 0:\n    play()',
     "fix": "Add a colon to the end of that line.", "topic": "if"},
    {"err": "SyntaxError: 'return' outside function", "means": "The return line isn't indented, so Python thinks it's in the main program.",
     "bad": "def double(n):\n    answer = n * 2\nreturn answer", "good": "def double(n):\n    answer = n * 2\n    return answer",
     "fix": "Press Tab so return lines up with the rest of the subroutine.", "topic": "sub"},
    {"err": "My program never stops", "means": "A while loop's condition never becomes False. Often the line that changes it isn't indented inside the loop.",
     "bad": 'guess = input("Password? ")\nwhile guess != "open":\n    print("Wrong")\nguess = input("Password? ")', "good": 'guess = input("Password? ")\nwhile guess != "open":\n    print("Wrong")\n    guess = input("Password? ")',
     "fix": "Press Stop. Then find the line that should change the condition each time round and indent it into the loop.", "topic": "loop"},
    {"err": "No error, but a line runs too often (or only once)", "means": "The line is in the wrong block. Indented means it repeats with the loop. Back out means it runs once.",
     "bad": 'for i in range(3):\n    print(i)\n    print("Done")', "good": 'for i in range(3):\n    print(i)\nprint("Done")',
     "fix": "Ask: should this line happen every time, or once? Then indent it, or bring it back out.", "topic": "loop"},
    {"err": "TypeError: ... 'NoneType'", "means": "A subroutine gave back None. It probably prints its answer instead of returning it.",
     "bad": "def area(w, h):\n    print(w * h)\n\ntotal = area(2, 3) + 1", "good": "def area(w, h):\n    return w * h\n\ntotal = area(2, 3) + 1",
     "fix": "Use return to send the answer back.", "topic": "sub"},
]
