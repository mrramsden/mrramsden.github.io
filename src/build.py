import json, re, sys, importlib
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "ks3")
sys.path.insert(0, HERE)
PART = sys.argv[1] if len(sys.argv) > 1 else "3"
NAMES = {"1": "escape-the-dungeon-1", "2": "escape-the-dungeon-2", "3": "escape-the-dungeon-3"}
MODS = {"1": ("checks1", "predict1"), "2": ("checks2", "predict2"), "3": ("checks", "predict")}
CHECKS = importlib.import_module(MODS[PART][0]).CHECKS
PREDICT = importlib.import_module(MODS[PART][1]).PREDICT
OUT = os.path.join(SITE, NAMES[PART] + ".html")

src = open(os.path.join(HERE, "base", f"orig{PART}.html"), encoding="utf-8").read()


def jsdump(obj):
    return json.dumps(obj, ensure_ascii=False).replace("<", "\\u003c")


def rep(old, new, count=1, optional=False):
    global src
    n = src.count(old)
    if optional and n == 0:
        return
    assert n == count, (n, old[:80])
    src = src.replace(old, new)


# ---------- runtime ----------
runtime = open(os.path.join(HERE, "runtime_v2.py"), encoding="utf-8").read()
m = re.search(r'const RUNTIME_PY = ".*?";\n', src)
src = src[:m.start()] + "const RUNTIME_PY = " + jsdump(runtime) + ";\n" + src[m.end():]

# ---------- checks and predict data ----------
rep('const PYODIDE_URL =', "const CHECKS = " + jsdump(CHECKS) + ";\nconst PREDICT = " + jsdump(PREDICT) + ";\nconst PYODIDE_URL =")

# ---------- CSS ----------
rep(".rbar button[disabled]{opacity:.45;cursor:default}", """.rbar button[disabled]{opacity:.45;cursor:default}
.rbar button.check{background:var(--amber);color:var(--navy)}
.gut div.todo{background:var(--amber-pale);color:#9A5B00;border-radius:4px;padding-right:4px;box-shadow:inset 3px 0 0 var(--amber)}
.msg.pass{background:#E3F4EC;color:#1C5C42;border-left:5px solid var(--green)}
.passed{background:var(--green);color:#fff;font-size:.78rem;font-weight:700;padding:3px 10px;border-radius:999px;display:inline-flex;gap:5px;align-items:center;margin-left:auto}
.cov{background:#fff;border-top:1px solid var(--line);padding:10px 14px;font-size:.95rem}
.cov[hidden]{display:none}
.cov .covtop{display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.cov .bar{flex:1;min-width:120px;height:10px;background:var(--pale);border-radius:99px;overflow:hidden}
.cov .bar i{display:block;height:100%;background:var(--green);border-radius:99px}
.cov ul{margin:6px 0 0;padding-left:1.2em}
.cov li code{font-size:.85em}
.cov .covreset{border:0;background:none;color:var(--blue);font-weight:600;font-size:.85rem;padding:0;text-decoration:underline}
.predict .opts{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0}
.predict .opt{border:2px solid var(--line);background:#fff;border-radius:10px;padding:10px 14px;text-align:left;font-family:var(--code);font-size:.95rem;color:var(--navy)}
.predict .opt:not([disabled]):hover{border-color:var(--blue)}
.predict .opt.right{border-color:var(--green);background:#E3F4EC}
.predict .opt.wrong{border-color:var(--red);background:var(--red-pale)}
.predict .opt[disabled]{cursor:default}
.predict .q{font-weight:700;margin:10px 0 0}
.checkcount{font-size:.9rem;color:var(--deep);margin-top:4px}
@media (max-width:760px){.predict .opts{grid-template-columns:1fr}}""")

# ---------- icons ----------
rep("  door: '<svg", "  tick: '<svg class=\"i\" viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M5 12.5l4.5 4.5L19 7.5\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>',\n  check: '<svg class=\"i\" viewBox=\"0 0 24 24\" aria-hidden=\"true\"><circle cx=\"12\" cy=\"12\" r=\"9\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.2\"/><path d=\"M8 12.3l2.8 2.8L16.5 9.5\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2.4\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>',\n  door: '<svg")

# ---------- state ----------
m = re.search(r"const fresh = \(\) => \(\{[^\n]*?done: \{\}", src)
assert m, "fresh() not found"
src = src[:m.end()] + ", checked: {}, pred: {}, cover: {}" + src[m.end():]
rep('for (const k of ["code", "ticks", "hints", "unlocked", "done"]) if (st[k] && typeof st[k] === "object") next[k] = st[k];',
    'for (const k of ["code", "ticks", "hints", "unlocked", "done", "checked", "pred", "cover"]) if (st[k] && typeof st[k] === "object") next[k] = st[k];')
rep("function el(html){", "function fmt(msg){ return esc(msg).replace(/`([^`]+)`/g, \"<code>$1</code>\"); }\nfunction el(html){")

# ---------- runner ----------
rep("function makeRunner(id, starter, label, download){", "function makeRunner(id, starter, label, download, opts){\n  opts = opts || {};", optional=True)
rep("function makeRunner(id, starter, label){", "function makeRunner(id, starter, label, download, opts){\n  opts = opts || {};", optional=True)
rep("""<button class="copy" title="Copy the code">""",
    """${opts.check ? `<button class="check" title="Test your code to see if the task is done">${IC.check} Check my code</button>` : ""}
      <button class="copy" title="Copy the code">""")
rep("""<div class="con" aria-live="polite"><pre><span class="muted">Output appears here when you press Run.</span></pre></div>
  </div>`);""", """<div class="con" aria-live="polite"><pre><span class="muted">Output appears here when you press Run.</span></pre></div>
    ${opts.cover ? `<div class="cov" hidden aria-live="polite"></div>` : ""}
  </div>`);""")

# shared "is the code ready?" check, used by Run and Check
rep("""    clearMsgs(); segs = []; outLen = 0; render();
    const code = ta.value;
    if (code.includes("___")) {
      const m = {}; code.split("\\n").forEach((l, i) => { if (l.includes("___")) m[i+1] = "gap"; });
      setMarks(m);
      showMsg("warn", "<strong>Fill in the gaps first.</strong>Replace every <code>___</code> with your answer. The gaps are on the highlighted lines.");
      return;
    }
    setMarks({});
    if (!code.trim()) { showMsg("warn", "<strong>There's no code yet.</strong>Type your program in the box above, then press Run."); return; }
    active = api; let finish; api.finished = new Promise(r => finish = r);
    bRun.disabled = true; bStop.disabled = false;""",
"""    clearMsgs(); segs = []; outLen = 0; render();
    const code = ta.value;
    if (!ready(code)) return;
    active = api; let finish; api.finished = new Promise(r => finish = r);
    bRun.disabled = true; bStop.disabled = false; if (bCheck) bCheck.disabled = true;""")
rep("""  let runDone = null;
  async function run(){""", """  function ready(code){
    if (code.includes("___")) {
      const m = {}; code.split("\\n").forEach((l, i) => { if (l.includes("___")) m[i+1] = "gap"; });
      setMarks(m);
      showMsg("warn", "<strong>Fill in the gaps first.</strong>Replace every <code>___</code> with your answer. The gaps are on the highlighted lines.");
      return false;
    }
    setMarks({});
    if (!code.trim()) { showMsg("warn", "<strong>There's no code yet.</strong>Type your program in the box above, then press Run."); return false; }
    return true;
  }
  const bCheck = wrap.querySelector(".check"), cov = wrap.querySelector(".cov");

  // ---- paths tried (if / elif / else) for the adventure box
  function showPaths(res){
    if (!cov || !res.paths) return;
    const keys = new Set(res.paths.map(p => p.key));
    const tried = new Set((S.cover[id] || []).filter(k => keys.has(k)).concat(res.hits || []));
    S.cover[id] = [...tried]; save();
    const n = res.paths.length;
    if (!n) { cov.hidden = true; return; }
    const todo = res.paths.filter(p => !tried.has(p.key)), done = n - todo.length;
    const m = {}; todo.forEach(p => { if (!marks[p.line]) m[p.line] = "todo"; });
    setMarks(Object.assign({}, marks, m));
    cov.hidden = false;
    cov.innerHTML = `<div class="covtop"><strong>Paths tested: ${done} of ${n}</strong><span class="bar"><i style="width:${Math.round(done / n * 100)}%"></i></span><button class="covreset">Start counting again</button></div>` +
      (todo.length ? `<p style="margin:6px 0 0">Every <code>if</code>, <code>elif</code> and <code>else</code> is a path through your game. Play again and try to reach ${todo.length === 1 ? "this one" : "these"} (highlighted in the line numbers):</p><ul>${todo.slice(0, 6).map(p => `<li>Line ${p.line}: <code>${esc(p.label)}</code></li>`).join("")}${todo.length > 6 ? `<li>and ${todo.length - 6} more</li>` : ""}</ul>`
                   : `<p style="margin:6px 0 0">${IC.tick} You've tried every path in your game. That's proper testing!</p>`);
    cov.querySelector(".covreset").addEventListener("click", () => { S.cover[id] = []; save(); cov.hidden = true; setMarks({}); });
  }

  // ---- Check my code
  async function check(){
    if (active && active !== api) { active.stop(); await active.finished; }
    if (active === api) return;
    clearMsgs(); segs = []; outLen = 0; render();
    const code = ta.value;
    if (!ready(code)) return;
    active = api; let finish; api.finished = new Promise(r => finish = r);
    bRun.disabled = true; bCheck.disabled = true;
    try {
      segs = [{t: "note", s: (window.loadPyodide && pyPromise ? "" : "Loading Python... ") + "Checking your code. I'll run it with my own test answers...\\n"}]; render();
      let py;
      try { py = await loadPython(); }
      catch (e) { segs = []; render(); showMsg("error", "<strong>Python couldn't load.</strong>You might be offline, or the site that provides Python is blocked. Ask your teacher to check your work instead."); return; }
      await new Promise(r => requestAnimationFrame(() => setTimeout(r, 0)));
      py.globals.set("_rt_src", code);
      py.globals.set("_rt_spec", JSON.stringify(opts.check));
      const res = JSON.parse(await py.runPythonAsync("await runtime.check(_rt_src, _rt_spec)"));
      segs = [{t: "note", s: "Check finished. Press Run to play your program yourself.\\n"}]; render();
      if (res.type === "pass") {
        S.checked[id] = true; save();
        showMsg("pass", `<strong>${IC.tick} Check passed!</strong>${esc(opts.check.win || "This task is done.")}`);
        if (opts.onPass) opts.onPass();
      } else {
        if (res.line) setMarks({[res.line]: "err"});
        showMsg("warn", `<strong>Not quite yet.</strong>${fmt(res.msg)}`);
      }
    } catch (e) {
      showMsg("error", "<strong>Something went wrong checking your code.</strong>" + esc(e && e.message ? e.message.split("\\n").slice(-2).join(" ") : e));
    } finally {
      if (active === api) active = null;
      bRun.disabled = false; bCheck.disabled = false; finish();
    }
  }
  if (bCheck) bCheck.addEventListener("click", check);

  async function run(){""")
rep("""      py.globals.set("_rt_src", code);
      const res = JSON.parse(await py.runPythonAsync("await runtime.run(_rt_src)"));
      render();""", """      py.globals.set("_rt_src", code);
      py.globals.set("_rt_cover", !!opts.cover);
      const res = JSON.parse(await py.runPythonAsync("await runtime.run(_rt_src, _rt_cover)"));
      render();""")
rep("""        showMsg("error", `<strong>${res.line ? "Problem on line " + res.line : "Problem"}</strong><code>${esc(res.error)}</code>${res.hint ? "<br>" + esc(res.hint) : ""}${refLink(res)}`);
      }""", """        showMsg("error", `<strong>${res.line ? "Problem on line " + res.line : "Problem"}</strong><code>${esc(res.error)}</code>${res.hint ? "<br>" + esc(res.hint) : ""}${refLink(res)}`);
      }
      showPaths(res);""")
rep("""      if (active === api) active = null;
      bRun.disabled = false; bStop.disabled = true; finish();""", """      if (active === api) active = null;
      bRun.disabled = false; bStop.disabled = true; if (bCheck) bCheck.disabled = false; finish();""")

# ---------- task cards: passed badge ----------
rep("""    <h3><span class="tasknum">${label}</span>${esc(cap(p.title.replace(/^(Extension|Stretch): /, "")))}</h3>""",
    """    <h3><span class="tasknum">${label}</span>${esc(cap(p.title.replace(/^(Extension|Stretch): /, "")))}${S.checked[p.id] ? `<span class="passed">${IC.tick} Checked</span>` : ""}</h3>""")

# ---------- predict card ----------
rep("function renderHints(box, p){", r"""function predictHtml(st){
  const P = PREDICT[st.id];
  if (!P) return "";
  return `<div class="card predict" id="predict"><h2 class="sec">${IC.bulb} Predict first</h2>
    <p>Before you run anything, read this code and decide what it does.</p>
    <pre class="sample">${esc(P.code)}</pre><p class="q">${esc(P.q)}</p>
    <div class="opts">${P.o.map((o, i) => `<button class="opt" data-opt="${i}">${esc(o)}</button>`).join("")}</div>
    <div class="pfb"></div><div class="pslot"></div></div>`;
}
function wirePredict(st){
  const P = PREDICT[st.id], box = page.querySelector("#predict");
  if (!P || !box) return;
  const btns = [...box.querySelectorAll(".opt")];
  function reveal(pick, fresh){
    btns.forEach((b, i) => { b.disabled = true; if (i === P.a) b.classList.add("right"); else if (i === pick) b.classList.add("wrong"); });
    box.querySelector(".pfb").innerHTML = `<div class="msg ${pick === P.a ? "pass" : "warn"}"><strong>${pick === P.a ? IC.tick + " You predicted it." : "Not this time, and that's fine. Now you know."}</strong>${esc(P.e)} Run it to see for yourself.</div>`;
    if (!box.querySelector(".runner")) box.querySelector(".pslot").appendChild(makeRunner(st.id + "-predict", P.code, "Run it to check"));
  }
  btns.forEach((b, i) => b.addEventListener("click", () => { S.pred[st.id] = i; save(); reveal(i, true); }));
  if (S.pred[st.id] !== undefined) reveal(S.pred[st.id], false);
}

function renderHints(box, p){""")
rep("""  <div class="card learn"><h2 class="sec">${IC.book} Learn</h2>${st.learnHtml}<div id="learnslot"></div></div>""",
    """  ${predictHtml(st)}
  <div class="card learn"><h2 class="sec">${IC.book} Learn</h2>${st.learnHtml}<div id="learnslot"></div></div>""")

# ---------- stage wiring ----------
rep("""  const doneKey = st.id + ":" + lv, isDone = !!S.done[doneKey];""", """  const doneKey = st.id + ":" + lv, isDone = !!S.done[doneKey];
  const checkable = L.parts.filter(p => CHECKS[p.id] && p.kind === "main"), nChecked = checkable.filter(p => S.checked[p.id]).length;
  const checkLine = checkable.length ? `<p class="checkcount">${IC.check} Tasks checked on this route: ${nChecked} of ${checkable.length}</p>` : "";""")
rep("""             : `<p><strong>Finished everything you can on this stage?</strong></p><p>Mark it complete, then move on.</p>`}</div>""",
    """             : `<p><strong>Finished everything you can on this stage?</strong></p><p>Mark it complete, then move on.</p>`}${checkLine}</div>""")
rep("""  if (st.game) page.querySelector("#gameslot").appendChild(makeRunner("mygame", GAME_STARTER, "My adventure", true));
  page.querySelectorAll("[data-plan]")""", """  if (st.game) page.querySelector("#gameslot").appendChild(makeRunner("mygame", GAME_STARTER, "My adventure", true, {cover: true}));
  page.querySelectorAll("[data-plan]")""", optional=True)
rep("""    if (p.starter !== undefined && p.kind !== "step") art.querySelector(".rslot").appendChild(makeRunner(p.id, p.starter, "Your code"));""",
    """    if (p.starter !== undefined && p.kind !== "step") art.querySelector(".rslot").appendChild(makeRunner(p.id, p.starter, "Your code", false, {
      check: CHECKS[p.id],
      onPass: () => {
        const h = art.querySelector("h3");
        if (!h.querySelector(".passed")) h.insertAdjacentHTML("beforeend", `<span class="passed">${IC.tick} Checked</span>`);
        const cc = page.querySelector(".checkcount");
        if (cc) { const n = checkable.filter(q => S.checked[q.id]).length; cc.innerHTML = `${IC.check} Tasks checked on this route: ${n} of ${checkable.length}`; }
      }}));""")
rep("""  page.querySelector("#gameslot").appendChild(makeRunner("mygame", GAME_STARTER, "My adventure", true));
  const w = page.querySelector("#wipe");""", """  page.querySelector("#gameslot").appendChild(makeRunner("mygame", GAME_STARTER, "My adventure", true, {cover: true}));
  const w = page.querySelector("#wipe");""", optional=True)

rep("""  page.querySelector("#learnslot").appendChild(makeRunner(st.id + "-learn", st.learnCode, "Example"));""",
    """  page.querySelector("#learnslot").appendChild(makeRunner(st.id + "-learn", st.learnCode, "Example"));
  wirePredict(st);""")

# ---------- welcome text ----------
rep("""<div><b>${IC.code} 2. Code here</b>Type Python straight into this page and press <strong>Run</strong>. When a program asks a question, type in the box and press Enter.</div>""",
    """<div><b>${IC.code} 2. Code here</b>Type Python straight into this page and press <strong>Run</strong>. When a program asks a question, type in the box and press Enter. On most tasks, <strong>Check my code</strong> tests your work and tells you what to fix.</div>""")
rep("""<div><b>${IC.stairs} 3. Your adventure</b>Every stage ends with your own game, which grows as you go. Tasks match your level, which you can change at the top.</div>""",
    """<div><b>${IC.stairs} 3. Your adventure</b>Every stage ends with your own game, which grows as you go. It counts the paths you've tested, so you can find the ones you haven't tried.</div>""", optional=True)
rep("""<div><b>${IC.stairs} 3. Your adventure</b>Every stage ends with your own game, saved as you go. Tasks match your level, which you can change at the top.</div>""",
    """<div><b>${IC.stairs} 3. Your adventure</b>Every stage ends with your own game, saved as you go. It counts the paths you've tested, so you can find the ones you haven't tried.</div>""", optional=True)


# ---------- light indentation help (from Python Rescue): shading, amber line numbers, better paste ----------
rep("function fmt(msg){", open(os.path.join(HERE, "base", "indent_helpers.js"), encoding="utf-8").read() + "\nfunction fmt(msg){")
rep("""    <div class="ed"><div class="gut" aria-hidden="true"></div><textarea spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" aria-label="Python code"></textarea></div>""",
    """    <div class="ed"><div class="gut" aria-hidden="true"></div><div class="edwrap"><pre class="guides" aria-hidden="true"></pre><textarea spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" aria-label="Python code"></textarea></div></div>
    <div class="lint" hidden aria-live="polite"></div>""")
rep("""  const ta = wrap.querySelector("textarea"), gut = wrap.querySelector(".gut"), con = wrap.querySelector(".con"), out = con.querySelector("pre");""",
    """  const ta = wrap.querySelector("textarea"), gut = wrap.querySelector(".gut"), con = wrap.querySelector(".con"), out = con.querySelector("pre");
  const guides = wrap.querySelector(".guides"), lintBox = wrap.querySelector(".lint");""")
rep("""  function layout(){
    const n = ta.value.split("\\n").length;
    gut.innerHTML = Array.from({length: n}, (_, i) => `<div class="${marks[i+1] || ""}">${i+1}</div>`).join("");
    ta.style.height = (Math.max(n, 4) * 22 + 20 + (ta.scrollWidth > ta.clientWidth ? 16 : 0)) + "px";
  }""", """  function layout(){
    const n = ta.value.split("\\n").length;
    const lint = lintIndent(ta.value);
    gut.innerHTML = Array.from({length: n}, (_, i) => `<div class="${marks[i+1] || (lint[i+1] ? "lintmark" : "")}" ${lint[i+1] ? `title="${esc(lint[i+1])}"` : ""}>${i+1}</div>`).join("");
    ta.style.height = (Math.max(n, 4) * 22 + 20 + (ta.scrollWidth > ta.clientWidth ? 16 : 0)) + "px";
    guides.innerHTML = shadeCode(ta.value) + "\\n";
    guides.scrollLeft = ta.scrollLeft;
    const first = Object.keys(lint)[0];
    lintBox.hidden = !first;
    if (first) lintBox.innerHTML = `${IC.bulb} <span><b>Indentation check:</b> ${esc(lint[first])}${Object.keys(lint).length > 1 ? ` (and ${Object.keys(lint).length - 1} more amber line${Object.keys(lint).length > 2 ? "s" : ""})` : ""}</span>`;
  }
  ta.addEventListener("scroll", () => { guides.scrollLeft = ta.scrollLeft; });
  ta.addEventListener("paste", e => {
    const text = (e.clipboardData || window.clipboardData).getData("text");
    if (/\\t|[\\u201c\\u201d\\u2018\\u2019]/.test(text)) {
      e.preventDefault();
      insert(text.replace(/\\t/g, "    ").replace(/[\\u201c\\u201d]/g, '"').replace(/[\\u2018\\u2019]/g, "'"));
    }
  });""")
rep(".gut div.err{", """.ig{display:inline-block;white-space:pre;box-shadow:inset 2px 0 0 rgba(31,111,178,.45)}
.ig.l1{background:rgba(31,111,178,.10)}.ig.l2{background:rgba(46,139,106,.13)}.ig.l3{background:rgba(108,85,184,.12)}
.ig.bad{background:rgba(242,165,65,.55);box-shadow:inset 2px 0 0 var(--amber)}
.edwrap{position:relative;background:#fff;min-width:0}
.edwrap .guides{position:absolute;inset:0;margin:0;padding:10px 12px;font:inherit;line-height:22px;white-space:pre;color:transparent;overflow:hidden;pointer-events:none;tab-size:4;background:none}
.edwrap textarea{position:relative;background:transparent!important;width:100%;display:block}
.gut div.lintmark{background:var(--amber-pale);color:#9A5B00;border-radius:4px;padding-right:4px;box-shadow:inset 3px 0 0 var(--amber);cursor:help}
.lint{display:flex;gap:8px;align-items:flex-start;background:var(--amber-pale);border-top:1px solid #F5D9A8;padding:8px 14px;font-size:.92rem;color:#6B4200}
.lint[hidden]{display:none}
.gut div.err{""")


# ---------- link back to the site menu ----------
_m = re.search(r'(<div class="brand">.*?</div>)', src, re.S)
assert _m, "brand not found"
src = src[:_m.end()] + '\n  <a class="homelink" href="./" title="Back to the Key Stage 3 resources">&larr; Key Stage 3</a>' + src[_m.end():]
rep(".gut div.err{", "HOMECSS\n.gut div.err{".replace("HOMECSS", '.homelink{color:#fff;background:rgba(255,255,255,.12);border-radius:999px;padding:6px 14px;font-weight:600;text-decoration:none;font-size:.9rem;display:inline-flex;align-items:center;gap:6px;white-space:nowrap}.homelink:hover{background:rgba(255,255,255,.24)}.homelink:focus-visible{outline:3px solid var(--amber);outline-offset:2px}'))

open(OUT, "w", encoding="utf-8").write(src)
print("built", OUT, len(src))
