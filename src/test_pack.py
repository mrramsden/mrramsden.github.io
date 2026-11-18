import sys, json, asyncio, io, contextlib, builtins
import os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'fake')); sys.path.insert(0, HERE)
import runtime_v2 as rt
from pack_content import TOPICS, DOCTOR

GOOD = {
 "ind_fix": ['''name = input("What's your name? ")
if name == "Sam":
    print("Hi Sam!")
    print("Good to see you again.")
print("Bye for now.")'''],
 "ind_test": ['''coins = int(input("How many coins? "))
if coins >= 10:
    print("You buy a ticket.")
    coins = coins - 10
    print("Enjoy the ride!")
else:
    print("Not enough coins.")
print("Coins left:", coins)'''],
 "if_fix": ['''mark = int(input("Mark out of 50? "))
if mark >= 40:
    print("Grade: A")
elif mark >= 25:
    print("Grade: B")
else:
    print("Grade: C")
print("Well done for finishing!")'''],
 "if_test": ['''battery = int(input("Battery %? "))
if battery >= 50:
    print("You're fine.")
elif battery >= 20:
    print("Charge it soon.")
else:
    print("Charge it now!")'''],
 "loop_fix": ['''for number in range(1, 6):
    square = number * number
    print(number, "squared is", square)
print("All done!")'''],
 "loop_test": ['''password = input("Password? ")
while password != "pizza42":
    print("Wrong password, try again.")
    password = input("Password? ")
print("Welcome in!")'''],
 "sub_fix": ['''def double(number):
    answer = number * 2
    return answer

def show_title():
    print("== Number Machine ==")

show_title()
print(double(4))
print(double(10))'''],
 "sub_test": ['''def area(width, height):
    return width * height

room1 = area(3, 4)
room2 = area(2, 5)
print("Total floor:", room1 + room2)''', '''def area(width, height):
    print(width * height)
    return width * height

print("Total floor:", area(3, 4) + area(2, 5))'''],
}
# Typical half-fixes: (code, text the message must contain)
BAD = {
 "ind_fix": [('''name = input("What's your name? ")
if name == "Sam":
    print("Hi Sam!")
print("Good to see you again.")
print("Bye for now.")''', "Ali")],
 "ind_test": [('''coins = int(input("How many coins? "))
if coins >= 10:
    print("You buy a ticket.")
    coins = coins - 10
else:
    print("Not enough coins.")
print("Enjoy the ride!")
print("Coins left:", coins)''', "isn't enough")],
 "if_fix": [('''mark = int(input("Mark out of 50? "))
if mark >= 40:
    print("Grade: A")
elif mark >= 25:
    print("Grade: B")
else:
    print("Grade: C")
    print("Well done for finishing!")''', "back out")],
 "if_test": [('''battery = int(input("Battery %? "))
if battery >= 50:
    print("You're fine.")
elif battery > 20:
    print("Charge it soon.")
else:
    print("Charge it now!")''', "20 counts")],
 "loop_fix": [('''for number in range(1, 6):
    square = number * number
    print(number, "squared is", square)
    print("All done!")''', "move it back out")],
 "loop_test": [('''password = input("Password? ")
while password != "pizza42":
    print("Wrong password, try again.")
print("Welcome in!")''', "never ends")],
 "sub_fix": [('''def double(number):
    answer = number * 2
    return answer

def show_title():
    print("== Number Machine ==")
    show_title()

print(double(4))
print(double(10))''', "never runs")],
 "sub_test": [],
}


def run_plain(code, inputs=()):
    feed = list(inputs)
    f = io.StringIO()
    old = builtins.input
    builtins.input = lambda p="": (print(p, end=""), feed.pop(0))[1]
    try:
        with contextlib.redirect_stdout(f):
            exec(compile(code, "<t>", "exec"), {})
    finally:
        builtins.input = old
    return f.getvalue()


def flat(out):
    return ", ".join(l.strip() for l in out.split("\n") if l.strip())


async def main():
    problems = 0
    for t in TOPICS:
        tid = t["id"]
        # example runs
        out = run_plain(t["example"], ["7", "7", "7"])
        print(f"[{tid}] example ok: {flat(out)[:60]}")
        # puzzle answer compiles and runs
        code = "\n".join("    " * lv + line for line, lv in t["puzzle"]["lines"])
        try:
            out = run_plain(code, ["30", "30", "30", "30"])
            print(f"[{tid}] puzzle ok: {flat(out)[:70]}")
        except Exception as e:
            problems += 1; print(f"[{tid}] PUZZLE BROKEN: {e}")
        # flat puzzle must be wrong (else the puzzle is trivial)
        if all(lv == 0 for _, lv in t["puzzle"]["lines"]):
            problems += 1; print("puzzle has no indents")
        for kind in ("fix", "test"):
            key = f"{tid}_{kind}"
            spec = t[kind]["check"]
            r = json.loads(await rt.check(t[kind]["starter"], json.dumps(spec)))
            if r["type"] == "pass":
                problems += 1; print(f"  STARTER PASSES {key}!")
            else:
                print(f"  {key} starter -> {r['msg'][:150]}")
            for g in GOOD[key]:
                r = json.loads(await rt.check(g, json.dumps(spec)))
                if r["type"] != "pass":
                    problems += 1; print(f"  GOOD FAILS {key}: {r['msg']}")
            for b, want in BAD[key]:
                r = json.loads(await rt.check(b, json.dumps(spec)))
                if r["type"] == "pass" or want not in r["msg"]:
                    problems += 1; print(f"  BAD WRONG {key} wanted {want!r}: {r}")
                else:
                    print(f"  {key} half-fix -> {r['msg'][:150]}")
        # quiz: code questions answer must match output
        for q in t["quiz"]:
            if "code" in q:
                try:
                    got = flat(run_plain(q["code"]))
                except SyntaxError as e:
                    ans = q["o"][q["a"]]
                    print(f"  quiz (broken on purpose): {type(e).__name__} line {e.lineno} {e.msg!r} vs answer {ans!r}")
                    continue
                ans = q["o"][q["a"]]
                ok = got == ans.replace(", then ", ", ")
                print(f"  quiz: {got!r} vs {ans!r} {'OK' if ok else 'MISMATCH'}")
                if not ok and q["q"] != "Which line is wrong?" and "missing" not in q["q"]:
                    problems += 1
    # doctor
    for d in DOCTOR:
        r = json.loads(await rt.run(d["bad"])) if "never stops" not in d["err"] else {"error": "(loop)"}
        g = d["good"]
        try:
            compile(g, "<g>", "exec")
            gok = True
        except SyntaxError as e:
            gok = False
        print(f"doctor: {d['err'][:45]:45} bad -> {str(r.get('error'))[:60]} | good compiles: {gok}")
        if not gok:
            problems += 1
    print("problems:", problems)

asyncio.run(main())
