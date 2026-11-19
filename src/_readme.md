# Source for mrramsden.github.io

Pupils only ever see the site. Everything in `src/` is how its pages are made and tested. Never hand-edit the pages in `ks3/`, `ks4/`, `ks5/` or `digital-futures/`: change the source here, rebuild, test, then commit both.

## Site layout

| Path | What it is |
|---|---|
| `index.html` | Welcome page with four cards: Key Stage 3, 4 and 5, and Digital Futures. |
| `ks3/` | Escape the Dungeon 1 to 3 and Python Rescue (built), plus the HTML setup guide and HTML reference sheet (single-file). Section page `ks3/index.html`. |
| `ks4/` | GCSE (OCR J277): the pseudocode playground, Python challenge boards (Neko Neko Café, Pocket Pet, Station X, Crystal Caves, The Dungeon Architect), the sorting visualiser and Revision Jeopardy. Also links to the procedural Robot Game in `ks5/`. Section page `ks4/index.html`. |
| `ks5/` | A Level (OCR H446): algorithms lab, merge sort recursion, Dijkstra and A* table methods, Boolean algebra slips, Python challenge boards (The Robot Game procedural and object-oriented, The Shelter Project, Ashwood Manor, Little Ashford Noticeboard) and Revision Jeopardy. Also links to the playground, sorting visualiser and Crystal Caves in `ks4/`. |
| `digital-futures/` | Year 8 and Year 9 Digital Futures. `digital-futures/index.html` links to the two year pages, `year-8/index.html` and `year-9/index.html`, which hold the lesson cards. Year 8: Lesson 6 Fact-Check Challenge. Year 9: none yet. |
| `python/` | Redirect stubs only. The Escape the Dungeon pages used to live here, so old links forward to `ks3/`. |
| `assets/site.css` | Styles for the welcome and section pages. |
| `assets/fonts/` | Fonts hosted on the site (Fontsource, SIL Open Font Licence), so pages never call Google Fonts. |

To add a resource: put the page in the right section (see below), add a card to that section's `index.html`, add it to `SECTIONS` in `tests/ui_smoke.py`, test, commit.

## What's here

| File | What it is |
|---|---|
| `runtime_v2.py` | The Python engine every page embeds: runs pupil code (async input, loop guard, path tracking), friendly error hints, and the Check my code engine. |
| `base/orig1.html`, `orig2.html`, `orig3.html` | The original Escape the Dungeon pages. `build.py` upgrades them. |
| `checks1.py`, `checks2.py`, `checks.py` | Check my code tests for Escape the Dungeon Parts 1, 2 and 3. |
| `solutions1.py`, `solutions2.py`, `solutions.py` | Model answers (must pass) and typical mistakes (must fail with the stated message) for every check. |
| `predict1.py`, `predict2.py`, `predict.py` | Predict first questions for each stage. |
| `build.py` | Builds one Escape the Dungeon part: `python3 build.py 1` (or 2, 3). Writes `../ks3/escape-the-dungeon-N.html`. |
| `pack_content.py` | All the Python Rescue content: topics, puzzles, Fix it and Test it tasks with their checks, quizzes, Error doctor. |
| `build_pack.py` | Builds `../ks3/python-rescue.html`. Uses the runner and styles in `base/`. |
| `add_static.py` | Publishes a single-file HTML resource: `python3 add_static.py SOURCE.html ks5 name.html` (the section can also be `digital-futures/year-8` or `digital-futures/year-9`) (add `--shared` if more than one section links to it). Keeps the source in `static/`, swaps Google Fonts for `assets/fonts`, adds a back link and refuses pages that still load from other sites. If a page needs a font that is not in `assets/fonts/fonts.css`, add it from Fontsource first. |
| `static/` | Sources of the single-file pages (all three key stages). Edit these, then rerun `add_static.py` with the same arguments (`--shared` for pages linked from more than one section). |
| `harness.py` | Runs every check against its model answers and mistakes in normal Python: `python3 harness.py 1` (or 2, 3). |
| `test_pack.py` | Tests all Python Rescue content: examples, puzzles, checks, quiz answers, Error doctor. |
| `tests/node_harness.mjs` | Runs every Escape the Dungeon check in real Pyodide 0.26.4, the same Python the pages use. |
| `tests/ui_smoke.py` | Headless Chrome test of the whole site: welcome and section pages, every card and back link, old-link redirects, local fonts, no outside requests except Pyodide, and real Python checks. |

## Making a change

1. Edit the source (content, checks or engine).
2. Rebuild: `python3 build.py 1; python3 build.py 2; python3 build.py 3; python3 build_pack.py`
3. Test, and expect `problems: 0` from each:
   - `python3 harness.py 1`, `2` and `3`, then `python3 test_pack.py`
   - `cd tests && npm install pyodide@0.26.4 && node node_harness.mjs`
   - `cd tests && python3 ui_smoke.py` (needs Playwright and Chrome)
4. Commit `src/` and the built pages together, with the author set to Mr Ramsden and a no-reply address, never a personal or business email. GitHub Pages updates the live site within a minute or two.

## House rules

- Real Python only (Pyodide 0.26.4 from the jsDelivr CDN). No imitation interpreters.
- Pupil-facing text: UK spelling, no em dashes, warm and plain. Emoji used as small icons in pupil resources are fine.
- Every check needs a model answer and at least one typical mistake, tested in real Pyodide before it goes live.
- Each page keeps its own `localStorage` key, so progress never clashes between pages on the same site.
- No business links, personal email addresses or contact details anywhere in the site or the commit history.
- Single-file pages (KS4, KS5) carry their own self-tests where they have them. Before publishing a changed one, verify every answer it marks against an independent implementation (for example networkx for Dijkstra and A*, real CPython for the playground's Python translations), not only its built-in self-test.
- OCR house rules: Exam Reference Language for pseudocode, the table method for Dijkstra and A*, logic gates limited to AND, OR, NOT and XOR.
- Nothing tied to a specific class test: no question numbers, worked test answers or mark schemes from bought-in assessments.
