import json, re, sys
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "..", "ks3")
sys.path.insert(0, HERE)
import importlib
import pack_content
importlib.reload(pack_content)
from pack_content import TOPICS, DOCTOR

W = os.path.join(HERE, "base") + "/"


def jsdump(o):
    return json.dumps(o, ensure_ascii=False).replace("<", "\\u003c")


runtime = open(os.path.join(HERE, "runtime_v2.py"), encoding="utf-8").read()
base_css = open(W + "v2.css", encoding="utf-8").read()
icons = open(W + "icons_base.js", encoding="utf-8").read().rstrip().rstrip("};").rstrip().rstrip(",") + ","
icons += """
  indent: '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h18M11 10h10M11 14h10M3 19h18M3 9.5l4 2.5-4 2.5z" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  flask: '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 3h6M10 3v6l-5.5 9.5A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-2.5L14 9V3M7.5 15h9" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  doctor: '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7.5v9M7.5 12h9" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/></svg>',
  home: '<svg class="i" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11l9-7 9 7M5.5 9.5V20h13V9.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
};
"""

# ---------- runner: shared engine, plus indentation guides and live warnings ----------
runner = open(W + "runner_base.js", encoding="utf-8").read()


def rep(old, new):
    global runner
    assert runner.count(old) == 1, old[:70]
    runner = runner.replace(old, new)


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
    if (first) lintBox.innerHTML = `${IC.indent} <span><b>Indentation check:</b> ${esc(lint[first])}${Object.keys(lint).length > 1 ? ` (and ${Object.keys(lint).length - 1} more amber line${Object.keys(lint).length > 2 ? "s" : ""})` : ""}</span>`;
  }
  ta.addEventListener("scroll", () => { guides.scrollLeft = ta.scrollLeft; });
  ta.addEventListener("paste", e => {
    const text = (e.clipboardData || window.clipboardData).getData("text");
    if (/\\t|[\\u201c\\u201d\\u2018\\u2019]/.test(text)) {
      e.preventDefault();
      insert(text.replace(/\\t/g, "    ").replace(/[\\u201c\\u201d]/g, '"').replace(/[\\u2018\\u2019]/g, "'"));
    }
  });""")
rep("""path through your game. Play again and try to reach""", """path through your program. Run it again and try to reach""")
rep("""You've tried every path in your game. That's proper testing!""", """You've tried every path. That's proper testing!""")

# ---------- extra CSS ----------
css = base_css + """
/* ---- Python Rescue additions ---- */
.homelink{color:#fff;background:rgba(255,255,255,.12);border-radius:999px;padding:6px 14px;font-weight:600;text-decoration:none;font-size:.9rem;display:inline-flex;align-items:center;gap:6px;white-space:nowrap}.homelink:hover{background:rgba(255,255,255,.24)}.homelink:focus-visible{outline:3px solid var(--amber);outline-offset:2px}
.top{gap:14px}
.top .brand small{opacity:.8}
.nav{display:flex;gap:6px;flex-wrap:wrap;margin-left:auto}
.nav button,.top .resetall{background:rgba(255,255,255,.1);color:#fff;border:0;border-radius:999px;padding:7px 14px;font-weight:600;font-size:.92rem;display:inline-flex;gap:6px;align-items:center}
.nav button.on{background:#fff;color:var(--navy)}
.top .resetall{background:none;opacity:.75;font-weight:500;text-decoration:underline}
main{max-width:980px;margin:0 auto;padding:22px 18px 70px}
.card{background:#fff;border-radius:16px;box-shadow:0 1px 3px rgba(11,31,58,.08);padding:20px 24px;margin:0 0 18px}
h1{font-size:1.6rem;margin:0 0 6px;line-height:1.25}
.intro p{margin:6px 0 14px}
.tips{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.tips div{background:var(--pale);border-radius:12px;padding:12px 14px;font-size:.95rem}
.tips b{display:flex;gap:6px;align-items:center;color:var(--deep);margin-bottom:4px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:18px}
.grid .card{margin:0}
button.topic,button.doctor{display:flex;gap:16px;align-items:flex-start;text-align:left;border:2px solid transparent;cursor:pointer;width:100%;font:inherit;color:inherit}
button.topic:hover,button.doctor:hover{border-color:var(--blue)}
button.topic:focus-visible,button.doctor:focus-visible{outline:3px solid var(--amber);outline-offset:2px}
.tnum{flex:none;width:52px;height:52px;border-radius:14px;display:grid;place-items:center;font-size:1.5rem;font-weight:800;color:#fff;background:var(--blue)}
.tnum.big{width:72px;height:72px;font-size:2.1rem;border-radius:18px}
.c-green .tnum{background:#2E8B6A}.c-amber .tnum{background:#D98A1E}.c-purple .tnum{background:#6C55B8}
.c-green{border-top:5px solid #2E8B6A}.c-amber{border-top:5px solid #D98A1E}.c-purple{border-top:5px solid #6C55B8}.c-blue{border-top:5px solid var(--blue)}.c-doctor{border-top:5px solid var(--red)}
.tbody,.doctor>span:last-child{display:flex;flex-direction:column;gap:4px}
.ttitle{font-size:1.2rem;font-weight:700}
.ttag{color:var(--deep);font-size:.95rem;margin:0}
.dicon{flex:none;width:52px;height:52px;border-radius:14px;display:grid;place-items:center;background:var(--red-pale);color:var(--red)}
.dicon .i{width:30px;height:30px}.dicon.big{width:72px;height:72px}.dicon.big .i{width:40px;height:40px}
.pips{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}
.pip{display:inline-flex;gap:4px;align-items:center;font-size:.78rem;border:1.5px solid var(--line);border-radius:999px;padding:2px 9px;color:#6E89A8}
.pip b{font-weight:600}
.pip.on{background:#E3F4EC;border-color:var(--green);color:#1C5C42}
.pip .i{width:14px;height:14px}
.thead{display:flex;gap:18px;align-items:flex-start}
.aims{margin:6px 0 0;font-size:.95rem}
.step h2{display:flex;align-items:center;gap:10px;font-size:1.25rem;margin:0 0 10px}
.step h2 small{font-weight:500;color:#6E89A8;font-size:.85rem;margin-left:auto}
.sn{width:32px;height:32px;border-radius:50%;background:var(--navy);color:#fff;display:grid;place-items:center;font-size:1rem;flex:none}
ol.rules{padding-left:1.3em}ol.rules li{margin:4px 0}
kbd{background:#fff;border:1px solid var(--line);border-bottom-width:3px;border-radius:5px;padding:0 6px;font-family:var(--code);font-size:.85em}
.note{background:var(--amber-pale);border-radius:10px;padding:10px 14px;display:flex;gap:8px;align-items:flex-start;font-size:.95rem}
.slot{margin-top:12px}
pre.shaded{background:#fff;color:var(--navy);border:1px solid var(--line);font-family:var(--code);font-size:15px;line-height:22px;padding:10px 14px;border-radius:10px;overflow-x:auto;margin:10px 0}
pre.shaded.small{font-size:14px;line-height:21px;padding:8px 12px}
.ig{display:inline-block;white-space:pre;box-shadow:inset 2px 0 0 rgba(31,111,178,.45)}
.ig.l1{background:rgba(31,111,178,.10)}.ig.l2{background:rgba(46,139,106,.13)}.ig.l3{background:rgba(108,85,184,.12)}
.ig.bad{background:rgba(242,165,65,.55);box-shadow:inset 2px 0 0 var(--amber)}
.edwrap{position:relative;background:#fff;min-width:0}
.edwrap .guides{position:absolute;inset:0;margin:0;padding:10px 12px;font:inherit;line-height:22px;white-space:pre;color:transparent;overflow:hidden;pointer-events:none;tab-size:4}
.edwrap textarea{position:relative;background:transparent!important;width:100%;display:block}
.gut div.lintmark{background:var(--amber-pale);color:#9A5B00;border-radius:4px;padding-right:4px;box-shadow:inset 3px 0 0 var(--amber);cursor:help}
.lint{display:flex;gap:8px;align-items:flex-start;background:var(--amber-pale);border-top:1px solid #F5D9A8;padding:8px 14px;font-size:.92rem;color:#6B4200}
.lint[hidden]{display:none}
.phow{font-size:.92rem;color:var(--deep);margin:4px 0}
.plines{list-style:none;margin:8px 0;padding:0;border:1px solid var(--line);border-radius:12px;overflow:hidden}
.plines li{display:flex;align-items:center;gap:10px;padding:4px 10px;border-bottom:1px solid var(--line);background:#fff}
.plines li:last-child{border-bottom:0}
.plines li.wrong{background:var(--red-pale)}
.pbtns{display:flex;gap:4px;flex:none}
.pbtns button{width:34px;height:30px;border:1.5px solid var(--line);background:var(--pale);border-radius:8px;font-weight:800;color:var(--blue);font-size:1rem;cursor:pointer}
.pbtns button:hover:not([disabled]){border-color:var(--blue)}
.pbtns button[disabled]{opacity:.3;cursor:default}
.pnum{color:#9AB3CF;font-family:var(--code);font-size:.85rem;width:1.5em;text-align:right;flex:none}
code.pcode{background:none;padding:0;font-size:15px;white-space:pre;line-height:22px}
.pact{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:8px}
.pmsg .bad{color:#9B1C1C}.pmsg .good{color:#1C5C42;font-weight:600;display:inline-flex;gap:6px;align-items:center}
.linkbtn{background:none;border:0;color:var(--blue);font-weight:600;text-decoration:underline;padding:0;cursor:pointer;font:inherit}
.ttable{overflow-x:auto;margin:12px 0}
.ttable table{border-collapse:collapse;width:100%;font-size:.95rem}
.ttable th{background:var(--navy);color:#fff;text-align:left;padding:8px 10px;font-weight:600;font-size:.88rem}
.ttable td{border-bottom:1px solid var(--line);padding:7px 10px;vertical-align:middle}
.ttable tr.yes td{background:#F1FAF5}.ttable tr.no td{background:var(--red-pale)}
.ttype{background:var(--pale);color:var(--deep);border-radius:999px;padding:2px 10px;font-size:.8rem;font-weight:700;white-space:nowrap}
.ttable input[type=checkbox]{width:20px;height:20px}
.ttable select{font:inherit;font-size:.9rem;padding:4px 6px;border-radius:6px;border:1px solid var(--line)}
.tcount{display:flex;gap:6px;align-items:center;font-size:.92rem;color:var(--deep);margin:8px 0 0}
.qq{border-top:1px solid var(--line);padding:12px 0}
.qq:first-child{border-top:0;padding-top:0}
.qtext{margin:0 0 6px}
.opts{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0}
.opt{border:2px solid var(--line);background:#fff;border-radius:10px;padding:9px 14px;text-align:left;font:inherit;font-size:.95rem;color:var(--navy);cursor:pointer}
.opt:not([disabled]):hover{border-color:var(--blue)}
.opt.right{border-color:var(--green);background:#E3F4EC}
.opt.wrong{border-color:var(--red);background:var(--red-pale)}
.opt[disabled]{cursor:default}
.qq .msg{border-radius:10px}
.qscore{background:var(--pale);border-radius:12px;padding:12px 16px;margin-top:6px}
.qscore.good{background:#E3F4EC}
.conf{display:flex;gap:10px;flex-wrap:wrap}
.conf button{border:2px solid var(--line);background:#fff;border-radius:999px;padding:8px 18px;font:inherit;font-weight:600;color:var(--navy);cursor:pointer}
.conf button.on{border-color:var(--blue);background:var(--pale)}
.confmsg{min-height:1.5em}
.endnav{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-top:10px}
details.doc summary{cursor:pointer;font-weight:600;list-style:none;display:flex;gap:10px;align-items:center}
details.doc summary::before{content:"+";font-weight:800;color:var(--blue);width:1em}
details.doc[open] summary::before{content:"\\2212"}
details.doc summary code{font-size:.95rem;white-space:normal}
.ba{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.lab{font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;padding:2px 10px;border-radius:999px}
.lab.bad{background:var(--red-pale);color:#9B1C1C}.lab.good{background:#E3F4EC;color:#1C5C42}
@media (max-width:760px){.tips,.grid,.ba,.opts{grid-template-columns:1fr}.thead{flex-direction:column}}
"""

html = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Python Rescue: indentation, if, loops and subroutines</title>
<style>{css}</style>
</head>
<body>
<header class="top">
  <div class="brand"><svg class="i" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2.2"/><circle cx="12" cy="12" r="3.6" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M5.6 5.6l3.9 3.9M14.5 14.5l3.9 3.9M18.4 5.6l-3.9 3.9M9.5 14.5l-3.9 3.9" stroke="currentColor" stroke-width="2.2"/></svg>
    Python Rescue <small>15-minute help</small></div>
  <a class="homelink" href="./" title="Back to the Key Stage 3 resources">&larr; Key Stage 3</a>
  <nav class="nav" aria-label="Topics">
    <button data-go="home">All topics</button>
    {"".join(f'<button data-go="{t["id"]}">{t["title"]}</button>' for t in TOPICS)}
    <button data-go="doctor">Error doctor</button>
  </nav>
  <button class="resetall" id="resetall" title="Clear all your answers on this computer">Start again</button>
</header>
<main id="page"></main>
<script>
const TOPICS = {jsdump([{k: v for k, v in t.items()} for t in TOPICS])};
const DOCTOR = {jsdump(DOCTOR)};
const RUNTIME_PY = {jsdump(runtime)};
const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";
{icons}
{open(W + "pack_app.js", encoding="utf-8").read()}
{runner}
{open(W + "pack_pages.js", encoding="utf-8").read()}
</script>
</body>
</html>
"""
# Topic data needs plain tuples as lists for JSON
open(os.path.join(SITE, "python-rescue.html"), "w", encoding="utf-8").write(html)
print("built", len(html))
