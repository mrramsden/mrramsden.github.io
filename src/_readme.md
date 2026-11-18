# Source for mrramsden.github.io

Pupils only ever see the site: `index.html` (the menu) and the pages in `python/`. Everything in `src/` is how those pages are made and tested. Never hand-edit the files in `python/`: change the source here, rebuild, test, then commit both.

## What's here

| File | What it is |
|---|---|
| `runtime_v2.py` | The Python engine every page embeds: runs pupil code (async input, loop guard, path tracking), friendly error hints, and the Check my code engine. |
| `base/orig1.html`, `orig2.html`, `orig3.html` | The original Escape the Dungeon pages. `build.py` upgrades them. |
| `checks1.py`, `checks2.py`, `checks.py` | Check my code tests for Escape the Dungeon Parts 1, 2 and 3. |
| `solutions1.py`, `solutions2.py`, `solutions.py` | Model answers (must pass) and typical mistakes (must fail with the stated message) for every check. |
| `predict1.py`, `predict2.py`, `predict.py` | Predict first questions for each stage. |
| `build.py` | Builds one Escape the Dungeon part: `python3 build.py 1` (or 2, 3). Writes `../python/escape-the-dungeon-N.html`. |
| `pack_content.py` | All the Python Rescue content: topics, puzzles, Fix it and Test it tasks with their checks, quizzes, Error doctor. |
| `build_pack.py` | Builds `../python/python-rescue.html`. Uses the runner and styles in `base/`. |
| `harness.py` | Runs every check against its model answers and mistakes in normal Python: `python3 harness.py 1` (or 2, 3). |
| `test_pack.py` | Tests all Python Rescue content: examples, puzzles, checks, quiz answers, Error doctor. |
| `tests/node_harness.mjs` | Runs every Escape the Dungeon check in real Pyodide 0.26.4, the same Python the pages use. |
| `tests/ui_smoke.py` | Headless Chrome test of the whole site: menu, links, back links, a real check. |

## Making a change

1. Edit the source (content, checks or engine).
2. Rebuild: `python3 build.py 1; python3 build.py 2; python3 build.py 3; python3 build_pack.py`
3. Test, and expect `problems: 0` from each:
   - `python3 harness.py 1`, `2` and `3`, then `python3 test_pack.py`
   - `cd tests && npm install pyodide@0.26.4 && node node_harness.mjs`
   - `cd tests && python3 ui_smoke.py` (needs Playwright and Chrome)
4. Commit `src/` and `python/` together, with the author set to Mr Ramsden and a no-reply address, never a personal or business email. GitHub Pages updates the live site within a minute or two.

## House rules

- Real Python only (Pyodide 0.26.4 from the jsDelivr CDN). No imitation interpreters.
- Pupil-facing text: UK spelling, no em dashes, no emoji, warm and plain.
- Every check needs a model answer and at least one typical mistake, tested in real Pyodide before it goes live.
- Each page keeps its own `localStorage` key, so progress never clashes between pages on the same site.
- No business links, personal email addresses or contact details anywhere in the site or the commit history.
