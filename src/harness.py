import sys, json, asyncio
import os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'fake')); sys.path.insert(0, HERE)
import runtime_v2 as rt
import importlib
PART = sys.argv[1] if len(sys.argv) > 1 else '3'
CHECKS = importlib.import_module({'1':'checks1','2':'checks2','3':'checks'}[PART]).CHECKS
_s = importlib.import_module({'1':'solutions1','2':'solutions2','3':'solutions'}[PART])
GOOD, BAD = _s.GOOD, _s.BAD

async def chk(cid, code):
    spec = dict(CHECKS[cid]); return json.loads(await rt.check(code, json.dumps(spec)))

async def main():
    bad = 0
    for cid in CHECKS:
        for i, g in enumerate(GOOD.get(cid, [])):
            r = await chk(cid, g)
            if r["type"] != "pass":
                bad += 1; print(f"FAIL GOOD {cid}#{i}: {r['msg']}")
        for i, (b, want) in enumerate(BAD.get(cid, [])):
            r = await chk(cid, b)
            if r["type"] == "pass" or want not in r["msg"]:
                bad += 1; print(f"FAIL BAD  {cid}#{i} (wanted {want!r}): {r}")
            else:
                print(f"ok  bad  {cid}#{i}: {r['msg'][:150]}")
        if cid not in GOOD: print("NO GOOD for", cid)
    print("problems:", bad)
asyncio.run(main())
