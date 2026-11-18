/* ---------------- pages ---------------- */
const page = document.getElementById("page");
const TOPIC_BY = Object.fromEntries(TOPICS.map(t => [t.id, t]));

function quizScore(t){
  const a = S.quiz[t.id] || {};
  return t.quiz.filter((q, i) => a[i] === q.a).length;
}
function stepsDone(t){
  return {
    puzzle: !!S.puzzle[t.id],
    fix: !!S.checked[t.id + "_fix"],
    test: !!S.checked[t.id + "_test"],
    quiz: quizScore(t) >= 3,
  };
}
function pips(t){
  const d = stepsDone(t);
  const names = {puzzle: "Indent it", fix: "Fix it", test: "Test it", quiz: "Quiz"};
  return `<span class="pips">${Object.keys(names).map(k => `<span class="pip ${d[k] ? "on" : ""}" title="${names[k]}${d[k] ? ": done" : ""}">${d[k] ? IC.tick : ""}<b>${names[k]}</b></span>`).join("")}</span>`;
}

function renderHome(){
  page.innerHTML = `
  <section class="intro card">
    <h1>Stuck on Python? Pick one thing and spend 15 minutes on it.</h1>
    <p>Each topic has a short explanation, a puzzle, a bug to fix, some testing and a quick quiz. Do them in order, or jump to the bit you need.</p>
    <div class="tips">
      <div><b>${IC.code} Read the error</b>It tells you the line number. Start there, then look at the line above.</div>
      <div><b>${IC.indent} Tab and Shift+Tab</b>Tab indents one step (4 spaces). Shift+Tab goes back one step. Never count spaces.</div>
      <div><b>${IC.flask} Test every way</b>Working once isn't the same as working. Try the edges and the silly answers too.</div>
    </div>
  </section>
  <div class="grid">
    ${TOPICS.map((t, i) => `<button class="topic card c-${t.colour}" data-go="${t.id}">
      <span class="tnum">${i + 1}</span>
      <span class="tbody"><span class="ttitle">${esc(t.title)}</span><span class="ttag">${esc(t.tag)}</span>${pips(t)}</span>
    </button>`).join("")}
  </div>
  <button class="doctor card" data-go="doctor">
    <span class="dicon">${IC.doctor}</span>
    <span><span class="ttitle">Error doctor</span><span class="ttag">Got an error message? Find it here, see what it means and how to fix it.</span></span>
  </button>`;
  page.querySelectorAll("[data-go]").forEach(b => b.addEventListener("click", () => go(b.dataset.go)));
}

function renderTopic(t){
  const idx = TOPICS.indexOf(t), next = TOPICS[idx + 1];
  page.innerHTML = `
  <section class="thead card c-${t.colour}">
    <span class="tnum big">${idx + 1}</span>
    <div><h1>${esc(t.title)}</h1><p class="ttag">${esc(t.tag)} About 15 minutes.</p>
      <p class="aims"><b>By the end you can:</b> ${t.aim.map(esc).join("; ")}.</p>${pips(t)}</div>
  </section>

  <section class="card step" id="s-learn"><h2><span class="sn">1</span>The idea <small>3 minutes</small></h2>
    ${t.learn}
    ${codeBlock(t.example)}
    <p class="note">${IC.bulb} ${esc(t.example_note)}</p>
    <div class="slot" id="exslot"></div>
  </section>

  <section class="card step" id="s-puzzle"><h2><span class="sn">2</span>Indent it! <small>2 minutes</small></h2>
    <p>${t.puzzle.prompt}</p>
    <p class="phow">Use the arrows to move each line in or out. Then press <b>Check</b>.</p>
    <div class="puzzle" id="puzzle"></div>
  </section>

  <section class="card step" id="s-fix"><h2><span class="sn">3</span>Fix it <small>4 minutes</small></h2>
    ${t.fix.html}
    <div class="slot" id="fixslot"></div>
  </section>

  <section class="card step" id="s-test"><h2><span class="sn">4</span>Test it <small>4 minutes</small></h2>
    ${t.test.html}
    <div class="ttable" id="ttable"></div>
    <div class="slot" id="testslot"></div>
  </section>

  <section class="card step" id="s-quiz"><h2><span class="sn">5</span>Quick quiz <small>2 minutes</small></h2>
    <div id="quiz"></div>
  </section>

  <section class="card step endcard">
    <h2>How do you feel about ${esc(t.title.toLowerCase())} now?</h2>
    <div class="conf" id="conf">${["Still stuck", "Getting there", "Got it!"].map((c, i) => `<button data-conf="${i}" class="${S.conf[t.id] === i ? "on" : ""}">${c}</button>`).join("")}</div>
    <p class="confmsg" id="confmsg"></p>
    <div class="endnav"><button class="btn ghost" data-go="home">&larr; All topics</button>${next ? `<button class="btn primary" data-go="${next.id}">Next: ${esc(next.title)} &rarr;</button>` : `<button class="btn primary" data-go="doctor">Error doctor &rarr;</button>`}</div>
  </section>`;

  page.querySelector("#exslot").appendChild(makeRunner(t.id + "_ex", t.example, "Try it"));
  buildPuzzle(t, page.querySelector("#puzzle"));
  page.querySelector("#fixslot").appendChild(makeRunner(t.id + "_fix", t.fix.starter, "Fix it", false, {check: t.fix.check, onPass: refreshPips}));
  buildTable(t, page.querySelector("#ttable"));
  page.querySelector("#testslot").appendChild(makeRunner(t.id + "_test", t.test.starter, "Test it", false, {check: t.test.check, cover: true, onPass: refreshPips}));
  buildQuiz(t, page.querySelector("#quiz"));
  const confMsg = ["That's OK. Have another go at the Fix it, then ask your teacher. Bring the line number of your error.",
                   "Good. One more run through the quiz will help it stick.",
                   "Brilliant. Try the next topic, or go back to your own program and look for these bugs."];
  const cm = page.querySelector("#confmsg");
  if (S.conf[t.id] !== undefined) cm.textContent = confMsg[S.conf[t.id]];
  page.querySelectorAll("[data-conf]").forEach(b => b.addEventListener("click", () => {
    S.conf[t.id] = +b.dataset.conf; save();
    page.querySelectorAll("[data-conf]").forEach(x => x.classList.toggle("on", x === b));
    cm.textContent = confMsg[S.conf[t.id]];
  }));
  page.querySelectorAll("[data-go]").forEach(b => b.addEventListener("click", () => go(b.dataset.go)));
  function refreshPips(){ const p = page.querySelector(".thead .pips"); if (p) p.outerHTML = pips(t); }
  page._refresh = refreshPips;
}

/* ---- Indent it! puzzle */
function buildPuzzle(t, box){
  const lines = t.puzzle.lines;
  const solved = !!S.puzzle[t.id];
  let levels = solved ? lines.map(l => l[1]) : lines.map(() => 0);
  let tries = 0;
  function draw(){
    box.innerHTML = `<ol class="plines">${lines.map((l, i) => `<li data-i="${i}">
        <span class="pbtns"><button class="pl" aria-label="Move line ${i + 1} out" ${levels[i] === 0 || S.puzzle[t.id] ? "disabled" : ""}>&larr;</button><button class="pr" aria-label="Move line ${i + 1} in" ${levels[i] >= 2 || S.puzzle[t.id] ? "disabled" : ""}>&rarr;</button></span>
        <span class="pnum">${i + 1}</span><code class="pcode">${shadeLine("    ".repeat(levels[i]) + l[0])}</code></li>`).join("")}</ol>
      <div class="pact">${S.puzzle[t.id] ? "" : `<button class="btn primary pcheck">${IC.check} Check</button>`}<span class="pmsg" aria-live="polite"></span></div>
      <div class="pslot"></div>`;
    box.querySelectorAll(".pl").forEach(b => b.addEventListener("click", () => { const i = +b.closest("li").dataset.i; levels[i]--; draw(); }));
    box.querySelectorAll(".pr").forEach(b => b.addEventListener("click", () => { const i = +b.closest("li").dataset.i; levels[i]++; draw(); }));
    const c = box.querySelector(".pcheck");
    if (c) c.addEventListener("click", check);
    if (S.puzzle[t.id]) done(false);
  }
  function check(){
    tries++;
    const wrong = lines.map((l, i) => levels[i] !== l[1] ? i : -1).filter(i => i >= 0);
    box.querySelectorAll(".plines li").forEach((li, i) => li.classList.toggle("wrong", wrong.includes(i)));
    const msg = box.querySelector(".pmsg");
    if (!wrong.length) { S.puzzle[t.id] = true; save(); draw(); if (page._refresh) page._refresh(); return; }
    const colonMiss = wrong.find(i => i > 0 && /:\s*$/.test(lines[i - 1][0]) && levels[i] <= levels[i - 1]);
    let tip;
    if (colonMiss !== undefined) tip = `Look at line ${colonMiss}: it ends with a colon, so line ${colonMiss + 1} must be indented.`;
    else tip = `Line${wrong.length > 1 ? "s" : ""} ${wrong.map(i => i + 1).join(", ")} ${wrong.length > 1 ? "aren't" : "isn't"} right yet. For each one, ask: does it belong to the block, or should it run whatever happens?`;
    msg.innerHTML = `<span class="bad">${esc(tip)}</span>` + (tries >= 3 ? ` <button class="linkbtn pshow">Show me the answer</button>` : "");
    const sh = box.querySelector(".pshow");
    if (sh) sh.addEventListener("click", () => { levels = lines.map(l => l[1]); draw(); box.querySelector(".pmsg").innerHTML = "<span>Here's the answer. Read it through: why is each line where it is? Then press Check.</span>"; });
  }
  function done(){
    box.querySelector(".pmsg").innerHTML = `<span class="good">${IC.tick} Spot on. Every line is in the right block. Try running it:</span>`;
    const slot = box.querySelector(".pslot");
    if (!slot.firstChild) slot.appendChild(makeRunner(t.id + "_puz", lines.map(l => "    ".repeat(l[1]) + l[0]).join("\n"), "Your puzzle as code"));
  }
  draw();
}

/* ---- test table */
function buildTable(t, box){
  const rows = t.test.table;
  function draw(){
    const tried = rows.filter((r, i) => (S.table[t.id + ":" + i] || {}).tried).length;
    box.innerHTML = `<table><thead><tr><th>Type of test</th><th>What to try</th><th>What should happen</th><th>Tried it?</th><th>Did it do that?</th></tr></thead><tbody>
      ${rows.map((r, i) => { const st = S.table[t.id + ":" + i] || {}; return `<tr class="${st.ok === "no" ? "no" : st.ok === "yes" ? "yes" : ""}">
        <td><span class="ttype">${esc(r[0])}</span></td><td><code>${esc(r[1])}</code></td><td>${esc(r[2])}</td>
        <td><input type="checkbox" data-tried="${i}" aria-label="Tried test ${i + 1}" ${st.tried ? "checked" : ""}></td>
        <td><select data-ok="${i}" aria-label="Did test ${i + 1} do the right thing?"><option value="">Choose</option><option value="yes" ${st.ok === "yes" ? "selected" : ""}>Yes</option><option value="no" ${st.ok === "no" ? "selected" : ""}>No: found a bug!</option></select></td></tr>`; }).join("")}
      </tbody></table>
      <p class="tcount">${IC.flask} Tests tried: ${tried} of ${rows.length}${rows.some((r, i) => (S.table[t.id + ":" + i] || {}).ok === "no") ? ". You found a bug. Now fix it, then run the tests again." : tried === rows.length ? ". Every test tried. Now press Check my code." : "."}</p>`;
    box.querySelectorAll("[data-tried]").forEach(c => c.addEventListener("change", () => { const k = t.id + ":" + c.dataset.tried; S.table[k] = Object.assign({}, S.table[k], {tried: c.checked}); save(); draw(); }));
    box.querySelectorAll("[data-ok]").forEach(c => c.addEventListener("change", () => { const k = t.id + ":" + c.dataset.ok; S.table[k] = Object.assign({}, S.table[k], {ok: c.value, tried: true}); save(); draw(); }));
  }
  draw();
}

/* ---- quiz */
function buildQuiz(t, box){
  function draw(){
    const a = S.quiz[t.id] || {};
    const answered = Object.keys(a).length, score = quizScore(t);
    box.innerHTML = t.quiz.map((q, qi) => `<div class="qq" data-q="${qi}"><p class="qtext"><b>${qi + 1}.</b> ${esc(q.q)}</p>
        ${q.code ? codeBlock(q.code, "small") : ""}
        <div class="opts">${q.o.map((o, oi) => {
          const cls = a[qi] === undefined ? "" : oi === q.a ? "right" : oi === a[qi] ? "wrong" : "";
          return `<button class="opt ${cls}" data-o="${oi}" ${a[qi] !== undefined ? "disabled" : ""}>${esc(o)}</button>`; }).join("")}</div>
        ${a[qi] !== undefined ? `<div class="msg ${a[qi] === q.a ? "pass" : "warn"}"><strong>${a[qi] === q.a ? IC.tick + " Yes!" : "Not quite."}</strong>${esc(q.e)}</div>` : ""}
      </div>`).join("") +
      (answered === t.quiz.length ? `<div class="qscore ${score >= 3 ? "good" : ""}"><b>You scored ${score} out of ${t.quiz.length}.</b> ${score === 4 ? "Perfect!" : score === 3 ? "Great work." : "Read the explanations, then have another go."} <button class="linkbtn qagain">Try the quiz again</button></div>` : "");
    box.querySelectorAll(".qq").forEach(div => div.querySelectorAll(".opt").forEach(b => b.addEventListener("click", () => {
      S.quiz[t.id] = Object.assign({}, S.quiz[t.id], {[div.dataset.q]: +b.dataset.o}); save(); draw();
      if (page._refresh) page._refresh();
    })));
    const ag = box.querySelector(".qagain");
    if (ag) ag.addEventListener("click", () => { S.quiz[t.id] = {}; save(); draw(); if (page._refresh) page._refresh(); });
  }
  draw();
}

/* ---- error doctor */
function renderDoctor(){
  page.innerHTML = `<section class="thead card c-doctor"><span class="dicon big">${IC.doctor}</span>
    <div><h1>Error doctor</h1><p class="ttag">Find the message Python gave you. Most of these are indentation.</p>
    <p class="aims">Remember: the error points at a line number. If that line looks fine, check the line above it.</p></div></section>
    ${DOCTOR.map(d => `<details class="card doc"><summary><code>${esc(d.err)}</code></summary>
      <p><b>What it means:</b> ${esc(d.means)}</p>
      <div class="ba"><div><span class="lab bad">Before</span>${codeBlock(d.bad)}</div><div><span class="lab good">After</span>${codeBlock(d.good)}</div></div>
      <p><b>How to fix it:</b> ${esc(d.fix)}</p>
      <p><button class="linkbtn" data-go="${d.topic}">Practise this: ${esc(TOPIC_BY[d.topic].title)} &rarr;</button></p>
    </details>`).join("")}
    <div class="endnav"><button class="btn ghost" data-go="home">&larr; All topics</button></div>`;
  page.querySelectorAll("[data-go]").forEach(b => b.addEventListener("click", () => go(b.dataset.go)));
}

/* ---------------- navigation ---------------- */
function go(where){
  if (active) active.stop && active.stop();
  location.hash = where === "home" ? "" : where;
  draw();
  window.scrollTo(0, 0);
}
function draw(){
  const h = location.hash.slice(1);
  document.querySelectorAll(".nav button").forEach(b => b.classList.toggle("on", b.dataset.go === (h || "home")));
  if (TOPIC_BY[h]) renderTopic(TOPIC_BY[h]);
  else if (h === "doctor") renderDoctor();
  else renderHome();
}
window.addEventListener("hashchange", draw);
document.querySelectorAll(".nav button").forEach(b => b.addEventListener("click", () => go(b.dataset.go)));
document.getElementById("resetall").addEventListener("click", e => {
  const b = e.currentTarget;
  if (b.dataset.confirm) { S = fresh(); save(); delete b.dataset.confirm; b.textContent = "Start again"; draw(); }
  else { b.dataset.confirm = "1"; b.textContent = "Sure? Click again"; setTimeout(() => { delete b.dataset.confirm; b.textContent = "Start again"; }, 4000); }
});
draw();
