let pyPromise = null;
let active = null;          // the runner currently running
const decoder = new TextDecoder();

function loadPython(){
  if (pyPromise) return pyPromise;
  pyPromise = new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = PYODIDE_URL;
    s.onload = resolve;
    s.onerror = () => reject(new Error("Could not download Python"));
    document.head.appendChild(s);
  }).then(() => loadPyodide()).then(async py => {
    py.registerJsModule("rt_js", { get_input: () => active ? active.askInput() : Promise.reject(new Error("RT_STOPPED")) });
    const write = buf => { if (active) active.write(decoder.decode(buf, {stream: true})); return buf.length; };
    py.setStdout({ write });
    py.setStderr({ write });
    py.FS.writeFile("/home/pyodide/runtime.py", RUNTIME_PY);
    await py.runPythonAsync("import runtime");
    return py;
  });
  pyPromise.catch(() => { pyPromise = null; });
  return pyPromise;
}

/* ---------------- runner ---------------- */
function makeRunner(id, starter, label, download, opts){
  opts = opts || {};
  const saved = S.code[id];
  const wrap = el(`<div class="runner">
    <div class="rbar"><span class="lbl">${esc(label || "Python")}</span>
      <button class="run" title="Run (Ctrl+Enter)">${IC.play} Run</button>
      <button class="stop" disabled>${IC.stop} Stop</button>
      <button class="reset" title="Put the starting code back">${IC.reset} Reset</button>
      ${opts.check ? `<button class="check" title="Test your code to see if the task is done">${IC.check} Check my code</button>` : ""}
      <button class="copy" title="Copy the code">${IC.copy} Copy</button>${download ? `<button class="dl" title="Save as a .py file">${IC.save} Download .py</button>` : ""}</div>
    <div class="ed"><div class="gut" aria-hidden="true"></div><textarea spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" aria-label="Python code"></textarea></div>
    <div class="con" aria-live="polite"><pre><span class="muted">Output appears here when you press Run.</span></pre></div>
    ${opts.cover ? `<div class="cov" hidden aria-live="polite"></div>` : ""}
  </div>`);
  const ta = wrap.querySelector("textarea"), gut = wrap.querySelector(".gut"), con = wrap.querySelector(".con"), out = con.querySelector("pre");
  const bRun = wrap.querySelector(".run"), bStop = wrap.querySelector(".stop"), bReset = wrap.querySelector(".reset"), bCopy = wrap.querySelector(".copy");
  ta.value = saved !== undefined ? saved : starter;
  let marks = {};

  function layout(){
    const n = ta.value.split("\n").length;
    gut.innerHTML = Array.from({length: n}, (_, i) => `<div class="${marks[i+1] || ""}">${i+1}</div>`).join("");
    ta.style.height = (Math.max(n, 4) * 22 + 20 + (ta.scrollWidth > ta.clientWidth ? 16 : 0)) + "px";
  }
  function setMarks(m){ marks = m; layout(); }
  function persist(){ S.code[id] = ta.value; save(); }
  ta.addEventListener("input", () => { setMarks({}); persist(); });
  layout();

  // ---- editor keys: tab indent, smart enter, smart backspace, ctrl+enter runs
  function insert(text){
    ta.focus();
    if (!document.execCommand("insertText", false, text)) ta.setRangeText(text, ta.selectionStart, ta.selectionEnd, "end");
  }
  ta.addEventListener("keydown", e => {
    const v = ta.value, a = ta.selectionStart, b = ta.selectionEnd;
    const lineStart = v.lastIndexOf("\n", a - 1) + 1;
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); run(); return; }
    if (e.key === "Tab") {
      e.preventDefault();
      if (a === b && !e.shiftKey) { insert("    "); return; }
      const endLine = v.indexOf("\n", b - (b > a && v[b-1] === "\n" ? 1 : 0)); const stop = endLine === -1 ? v.length : endLine;
      const block = v.slice(lineStart, stop);
      const changed = e.shiftKey ? block.split("\n").map(l => l.replace(/^ {1,4}/, "")).join("\n") : block.split("\n").map(l => "    " + l).join("\n");
      ta.setSelectionRange(lineStart, stop); insert(changed);
      ta.setSelectionRange(lineStart, lineStart + changed.length); return;
    }
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      const before = v.slice(lineStart, a);
      let indent = before.match(/^ */)[0];
      if (/:\s*$/.test(before)) indent += "    ";
      insert("\n" + indent); return;
    }
    if (e.key === "Backspace" && a === b && a > lineStart) {
      const before = v.slice(lineStart, a);
      if (/^ +$/.test(before) && before.length % 4 === 0) {
        e.preventDefault(); ta.setSelectionRange(a - 4, a); document.execCommand("delete") || ta.setRangeText("", a - 4, a, "end"); return;
      }
    }
  });

  // ---- console
  let segs = [], pending = null, inputRow = null, renderQueued = false;
  function render(){
    renderQueued = false;
    let html = segs.map(s => s.t === "in" ? `<span class="typed">${esc(s.s)}</span>` : s.t === "note" ? `<span class="muted">${esc(s.s)}</span>` : esc(s.s)).join("");
    out.innerHTML = html;
    con.scrollTop = con.scrollHeight;
  }
  function queue(){ if (!renderQueued) { renderQueued = true; requestAnimationFrame(render); } }
  let outLen = 0;
  const api = {
    write(text){
      if (outLen > 60000) return;
      outLen += text.length;
      const last = segs[segs.length - 1];
      if (last && last.t === "out") last.s += text; else segs.push({t: "out", s: text});
      if (outLen > 60000) segs.push({t: "note", s: "\n(Lots of output. The rest is hidden.)\n"});
      queue();
    },
    askInput(){
      render();
      return new Promise((resolve, reject) => {
        pending = {resolve, reject};
        inputRow = el(`<div class="inrow"><label>&gt;</label><input type="text" aria-label="Type your answer and press Enter" autocomplete="off" spellcheck="false"><small>press Enter</small></div>`);
        con.appendChild(inputRow);
        const box = inputRow.querySelector("input");
        box.addEventListener("keydown", ev => {
          if (ev.key !== "Enter") return;
          ev.preventDefault();
          const val = box.value;
          inputRow.remove(); inputRow = null;
          segs.push({t: "in", s: val}); segs.push({t: "out", s: "\n"}); render();
          const p = pending; pending = null; p.resolve(val);
        });
        box.focus({preventScroll: true});
        con.scrollTop = con.scrollHeight;
      });
    },
    stop(){
      if (pending) { if (inputRow) { inputRow.remove(); inputRow = null; } const p = pending; pending = null; p.reject(new Error("RT_STOPPED")); }
    }
  };
  function clearMsgs(){ wrap.querySelectorAll(".msg").forEach(m => m.remove()); }
  function showMsg(cls, html){ const m = el(`<div class="msg ${cls}">${html}</div>`); con.appendChild(m); con.scrollTop = con.scrollHeight; }

  function ready(code){
    if (code.includes("___")) {
      const m = {}; code.split("\n").forEach((l, i) => { if (l.includes("___")) m[i+1] = "gap"; });
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
      segs = [{t: "note", s: (window.loadPyodide && pyPromise ? "" : "Loading Python... ") + "Checking your code. I'll run it with my own test answers...\n"}]; render();
      let py;
      try { py = await loadPython(); }
      catch (e) { segs = []; render(); showMsg("error", "<strong>Python couldn't load.</strong>You might be offline, or the site that provides Python is blocked. Ask your teacher to check your work instead."); return; }
      await new Promise(r => requestAnimationFrame(() => setTimeout(r, 0)));
      py.globals.set("_rt_src", code);
      py.globals.set("_rt_spec", JSON.stringify(opts.check));
      const res = JSON.parse(await py.runPythonAsync("await runtime.check(_rt_src, _rt_spec)"));
      segs = [{t: "note", s: "Check finished. Press Run to play your program yourself.\n"}]; render();
      if (res.type === "pass") {
        S.checked[id] = true; save();
        showMsg("pass", `<strong>${IC.tick} Check passed!</strong>${esc(opts.check.win || "This task is done.")}`);
        if (opts.onPass) opts.onPass();
      } else {
        if (res.line) setMarks({[res.line]: "err"});
        showMsg("warn", `<strong>Not quite yet.</strong>${fmt(res.msg)}`);
      }
    } catch (e) {
      showMsg("error", "<strong>Something went wrong checking your code.</strong>" + esc(e && e.message ? e.message.split("\n").slice(-2).join(" ") : e));
    } finally {
      if (active === api) active = null;
      bRun.disabled = false; bCheck.disabled = false; finish();
    }
  }
  if (bCheck) bCheck.addEventListener("click", check);

  async function run(){
    if (active && active !== api) { active.stop(); await active.finished; }
    if (active === api) return;
    clearMsgs(); segs = []; outLen = 0; render();
    const code = ta.value;
    if (!ready(code)) return;
    active = api; let finish; api.finished = new Promise(r => finish = r);
    bRun.disabled = true; bStop.disabled = false; if (bCheck) bCheck.disabled = true;
    try {
      let py;
      if (!window.loadPyodide || !pyPromise) { segs = [{t: "note", s: "Loading Python... the first run takes a few seconds.\n"}]; render(); }
      try { py = await loadPython(); }
      catch (e) {
        segs = []; render();
        showMsg("error", "<strong>Python couldn't load.</strong>You might be offline, or the site that provides Python is blocked. Press <b>Copy</b> and paste your code into IDLE or Thonny instead.");
        return;
      }
      if (segs.length === 1 && segs[0].t === "note") { segs = []; render(); }
      py.globals.set("_rt_src", code);
      py.globals.set("_rt_cover", !!opts.cover);
      const res = JSON.parse(await py.runPythonAsync("await runtime.run(_rt_src, _rt_cover)"));
      render();
      if (res.type === "ok") showMsg("ok", segs.length ? "Program finished." : "Program finished. (It didn't print anything.)");
      else if (res.type === "stopped") showMsg("warn", "<strong>Program stopped.</strong>");
      else if (res.type === "loop") showMsg("warn", `<strong>${esc(res.error)}</strong>${esc(res.hint)}${refLink(res)}`);
      else {
        if (res.line) setMarks({[res.line]: "err"});
        showMsg("error", `<strong>${res.line ? "Problem on line " + res.line : "Problem"}</strong><code>${esc(res.error)}</code>${res.hint ? "<br>" + esc(res.hint) : ""}${refLink(res)}`);
      }
      showPaths(res);
    } catch (e) {
      showMsg("error", "<strong>Something went wrong running your code.</strong>" + esc(e && e.message ? e.message.split("\n").slice(-2).join(" ") : e));
    } finally {
      if (active === api) active = null;
      bRun.disabled = false; bStop.disabled = true; if (bCheck) bCheck.disabled = false; finish();
    }
  }
  bRun.addEventListener("click", run);
  bStop.addEventListener("click", () => api.stop());
  bReset.addEventListener("click", () => {
    if (bReset.dataset.confirm) {
      delete bReset.dataset.confirm; bReset.innerHTML = IC.reset + " Reset";
      ta.value = starter; delete S.code[id]; save(); setMarks({}); clearMsgs(); segs = []; render();
    } else {
      bReset.dataset.confirm = "1"; bReset.innerHTML = IC.reset + " Sure? Click again";
      setTimeout(() => { if (bReset.dataset.confirm) { delete bReset.dataset.confirm; bReset.innerHTML = IC.reset + " Reset"; } }, 4000);
    }
  });
  bCopy.addEventListener("click", async () => {
    let ok = false;
    try { await navigator.clipboard.writeText(ta.value); ok = true; } catch (e) {
      ta.select(); try { ok = document.execCommand("copy"); } catch (e2) {}
    }
    bCopy.innerHTML = IC.copy + (ok ? " Copied" : " Press Ctrl+C");
    setTimeout(() => bCopy.innerHTML = IC.copy + " Copy", 1800);
  });
  const bDl = wrap.querySelector(".dl");
  if (bDl) bDl.addEventListener("click", () => {
    const name = ((S.plan && S.plan.title) || "my_adventure").toLowerCase().replace(/[^a-z0-9]+/g, "_").replace(/^_|_$/g, "") || "my_adventure";
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([ta.value], {type: "text/x-python"}));
    a.download = name + ".py"; document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
  });
  api.finished = Promise.resolve();
  wrap._stop = () => api.stop();
  return wrap;
}
