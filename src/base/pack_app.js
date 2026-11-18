/* ---------------- state ---------------- */
const KEY = "pythonRescue.v1";
const fresh = () => ({code: {}, checked: {}, cover: {}, puzzle: {}, quiz: {}, table: {}, conf: {}});
let S = fresh();
try { const raw = localStorage.getItem(KEY); if (raw) S = Object.assign(fresh(), JSON.parse(raw)); } catch (e) {}
function save(){ try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} }

function esc(s){ return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;"); }
function fmt(msg){ return esc(msg).replace(/`([^`]+)`/g, "<code>$1</code>"); }
function el(html){ const t = document.createElement("template"); t.innerHTML = html.trim(); return t.content.firstElementChild; }
function refLink(){ return ""; }

/* ---------------- indentation shading ---------------- */
// Each 4-space step gets a tinted band; leftover spaces (not a multiple of 4) show amber.
function shadeLine(line){
  const lead = line.match(/^ */)[0].length;
  const steps = Math.floor(lead / 4), extra = lead % 4;
  let html = "";
  for (let i = 0; i < steps; i++) html += `<span class="ig l${(i % 3) + 1}">    </span>`;
  if (extra) html += `<span class="ig bad">${" ".repeat(extra)}</span>`;
  return html + esc(line.slice(lead));
}
function shadeCode(code){ return code.split("\n").map(shadeLine).join("\n"); }
function codeBlock(code, cls){ return `<pre class="shaded ${cls || ""}">${shadeCode(code)}</pre>`; }

/* ---------------- live indentation checker ---------------- */
// Returns {line: message} for lines whose indentation looks wrong. Mirrors what Python will complain about.
function lintIndent(code){
  const lines = code.split("\n"), out = {};
  const stack = [0];
  let prevColon = false, depth = 0;
  lines.forEach((raw, i) => {
    const n = i + 1, line = raw.replace(/\t/g, "    ");
    const body = line.trim();
    if (!body || body.startsWith("#")) return;
    if (depth > 0) { depth += bracketDelta(body); return; }   // continuation of an open bracket
    const ind = line.length - line.trimStart().length;
    const top = stack[stack.length - 1];
    if (ind % 4) out[n] = `Line ${n} has ${ind} space${ind === 1 ? "" : "s"} at the start. Indents come in steps of 4: use Tab and Shift+Tab.`;
    else if (prevColon && ind <= top) out[n] = `Line ${n} comes straight after a line ending in a colon, so it should be indented one more step. Press Tab at the start of it.`;
    else if (!prevColon && ind > top) out[n] = `Line ${n} is indented, but the line above doesn't end with a colon. Line it up with the line above, or add the missing colon.`;
    else if (prevColon && ind > top + 4) out[n] = `Line ${n} is indented two steps. One step (4 spaces) is enough.`;
    else if (!prevColon && ind < top && !stack.includes(ind)) out[n] = `Line ${n} doesn't line up with any line above it. Press Shift+Tab or Tab until it lines up exactly.`;
    else if (/^(elif|else)\b/.test(body) && !stack.slice(0, -1).includes(ind) && !prevColon) out[n] = `Line ${n}: ${body.split(/[\s:]/)[0]} must line up exactly with its if.`;
    if (prevColon && ind > top) stack.push(ind);
    else while (stack.length > 1 && stack[stack.length - 1] > ind) stack.pop();
    const code_ = body.replace(/#.*$/, "").replace(/("[^"]*"|'[^']*')/g, "\"\"").trimEnd();
    prevColon = code_.endsWith(":");
    depth = Math.max(0, bracketDelta(code_));
  });
  return out;
}
function bracketDelta(s){
  s = s.replace(/("[^"]*"|'[^']*')/g, "");
  return (s.match(/[([{]/g) || []).length - (s.match(/[)\]}]/g) || []).length;
}

/* ---------------- Python loading ---------------- */
