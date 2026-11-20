"""Prepare a single-file HTML resource for the site.

    python3 add_static.py SOURCE.html SECTION NAME.html

SECTION is ks3/year-7, ks3/year-8, ks3/year-9, ks4, ks5, digital-futures/year-8 or digital-futures/year-9. The source is kept in src/static/ and the page is
written to ../SECTION/NAME.html. The script:
  - swaps Google Fonts links for the fonts hosted in assets/fonts (no outside requests),
  - adds a small back link to the section page at the top,
  - adds an empty tab icon so browsers do not ask for a missing favicon,
  - refuses pages that still load anything from another site.
"""
import os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
LABELS = {"ks3": "Key Stage 3", "ks3/year-7": "Year 7", "ks3/year-8": "Year 8", "ks3/year-9": "Year 9", "ks4": "Key Stage 4", "ks5": "Key Stage 5",
          "digital-futures/year-8": "Year 8 Digital Futures", "digital-futures/year-9": "Year 9 Digital Futures"}

BACK = (
    '<nav class="mr-back" style="font:600 14px/1.4 system-ui,-apple-system,\'Segoe UI\',Roboto,Arial,sans-serif;'
    'padding:8px 16px;max-width:1200px;margin:0 auto">'
    '<a href="./" style="color:#1F6FB2;text-decoration:none">&larr; {label}</a></nav>'
)
# Shared pages (linked from more than one section) send pupils back where they came from.
BACK_SCRIPT = (
    "<script>(function(){try{var r=document.referrer,a=document.querySelector('.mr-back a');"
    "var m=r&&r.indexOf(location.origin)===0&&r.match(/\\/(ks[345])\\//);"
    "if(m&&a){a.href='../'+m[1]+'/';a.innerHTML='&larr; '+{ks3:'Key Stage 3',ks4:'Key Stage 4',ks5:'Key Stage 5'}[m[1]];}}catch(e){}})();</script>"
)


def prepare(html, section, shared=False):
    up = "../" * (section.count("/") + 1)  # path from the page back to the site root
    html = re.sub(r'\s*<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>', "", html)
    html = html.replace("</head>", '<link rel="stylesheet" href="' + up + 'assets/fonts/fonts.css">\n<link rel="icon" href="data:,">\n</head>', 1)
    back = BACK.format(label=LABELS[section]) + (BACK_SCRIPT if shared else "")
    html, n = re.subn(r"(<body[^>]*>)", lambda m: m.group(1) + "\n" + back, html, count=1)
    assert n == 1, "no <body> tag"
    outside = sorted(set(re.findall(r'(?:src|href)\s*=\s*["\'](https?://[^"\']+)', html)))
    outside = [u for u in outside if not u.startswith("http://www.w3.org")]
    assert not outside, "page still loads from outside the site: " + ", ".join(outside)
    return html


if __name__ == "__main__":
    src, section, name = sys.argv[1], sys.argv[2], sys.argv[3]
    shared = "--shared" in sys.argv
    keep = os.path.join(HERE, "static", name)
    if os.path.abspath(src) != os.path.abspath(keep):
        os.makedirs(os.path.dirname(keep), exist_ok=True)
        shutil.copy(src, keep)
    html = prepare(open(keep, encoding="utf-8").read(), section, shared)
    out = os.path.join(ROOT, section, name)
    open(out, "w", encoding="utf-8").write(html)
    print("built", os.path.relpath(out, ROOT), len(html))
