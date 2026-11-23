import { loadPyodide } from "pyodide";
import fs from "fs";
import path from "path";
const SRC = path.join(path.dirname(new URL(import.meta.url).pathname), "..");
const py = await loadPyodide();
py.registerJsModule("rt_js", { get_input: () => Promise.reject(new Error("real input in test")) });
for (const f of ["runtime_v2.py", "checks.py", "solutions.py", "checks1.py", "solutions1.py", "checks2.py", "solutions2.py", "checks4.py", "solutions4.py"])
  py.FS.writeFile("/home/pyodide/" + f, fs.readFileSync(path.join(SRC, f), "utf8"));
const t0 = Date.now();
await py.runPythonAsync(`
import sys, json, time, importlib
sys.path.insert(0, "/home/pyodide")
print(sys.version)
import runtime_v2 as rt
problems = 0
for cm, sm in [("checks1", "solutions1"), ("checks2", "solutions2"), ("checks", "solutions"), ("checks4", "solutions4")]:
    CHECKS = importlib.import_module(cm).CHECKS
    sol = importlib.import_module(sm)
    ran = 0
    slowest = (0, "")
    for cid in CHECKS:
        if cid not in sol.GOOD:
            print("no model answer for", cid)
        for code in sol.GOOD.get(cid, []):
            t = time.time()
            r = json.loads(await rt.check(code, json.dumps(CHECKS[cid]))); ran += 1
            slowest = max(slowest, (time.time() - t, cid))
            if r["type"] != "pass": problems += 1; print("FAIL GOOD", cid, r)
        for code, want in sol.BAD.get(cid, []):
            r = json.loads(await rt.check(code, json.dumps(CHECKS[cid]))); ran += 1
            if r["type"] == "pass" or want not in r["msg"]: problems += 1; print("FAIL BAD", cid, want, r)
    print(cm, "checks:", len(CHECKS), "cases run:", ran, f"slowest: {slowest[1]} {slowest[0]:.2f}s")
print("problems:", problems)
`);
console.log("total seconds", (Date.now() - t0) / 1000);
