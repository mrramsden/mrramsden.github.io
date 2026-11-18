"""Smoke test the whole site in headless Chrome, served over HTTP like GitHub Pages.

Usage (from src/tests):  python3 ui_smoke.py [base_url]
With no base_url it serves the repository root on a local port.
Needs: pip playwright, Chrome at /usr/bin/google-chrome, and `npm install pyodide@0.26.4`
in this folder (the page's CDN requests for Pyodide are answered from node_modules).
"""
import asyncio, os, sys, threading, http.server, functools, socketserver
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PYO = os.path.join(HERE, "node_modules", "pyodide") + "/"
sys.path.insert(0, os.path.join(HERE, ".."))
from solutions import GOOD as G3          # noqa: E402
from solutions2 import GOOD as G2         # noqa: E402

# section page -> the pages its cards should open
SECTIONS = {
    "ks3/": ["escape-the-dungeon-1.html", "escape-the-dungeon-2.html", "escape-the-dungeon-3.html", "python-rescue.html"],
    "ks4/": ["pseudocode-playground.html", "station-x.html", "../ks5/robot-game-procedural.html"],
    "ks5/": ["algorithms-lab.html", "merge-sort-recursion.html", "dijkstra-table-method.html",
             "a-star-table-method.html", "boolean-algebra-slips.html", "../ks4/pseudocode-playground.html",
             "robot-game-procedural.html", "robot-game-oop.html"],
}
MOVED = ["escape-the-dungeon-1", "escape-the-dungeon-2", "escape-the-dungeon-3", "python-rescue"]


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Quiet, directory=ROOT)
    httpd = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{httpd.server_address[1]}/"


async def main(base):
    problems = 0
    async with async_playwright() as p:
        br = await p.chromium.launch(executable_path="/usr/bin/google-chrome")
        pg = await br.new_page(viewport={"width": 1280, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(m.text) if m.type == "error" else None)

        async def route(r):
            name = r.request.url.split("/full/")[-1].split("?")[0]
            path = PYO + name
            if os.path.exists(path):
                ct = "application/wasm" if name.endswith(".wasm") else "application/javascript" if name.endswith(".js") else "application/octet-stream"
                await r.fulfill(path=path, content_type=ct, headers={"Access-Control-Allow-Origin": "*"})
            else:
                await r.continue_()
        if os.path.isdir(PYO):
            await pg.route("**/pyodide/v0.26.4/full/**", route)

        outside = set()
        pg.on("request", lambda r: outside.add(r.url.split("/")[2]) if not r.url.startswith(base) and not r.url.startswith("data:") else None)

        await pg.goto(base)
        cards = await pg.locator("a.card").count()
        print("welcome page cards:", cards); problems += cards != 3
        await pg.screenshot(path=os.path.join(HERE, "smoke_menu.png"), full_page=True)
        for sec, pages in SECTIONS.items():
            await pg.goto(base); await pg.click(f'a.card[href="{sec}"]'); await pg.wait_for_load_state("load")
            hrefs = await pg.locator("a.card").evaluate_all("els => els.map(e => e.getAttribute('href'))")
            if hrefs != pages: print("  card list differs:", sec, hrefs); problems += 1
            await pg.screenshot(path=os.path.join(HERE, "smoke_" + sec.strip("/") + ".png"), full_page=True)
            await pg.click("a.homelink"); await pg.wait_for_load_state("load")
            back_home = await pg.locator("a.card").count() == 3
            print(f"{sec:5} {len(hrefs)} cards | All key stages link returns home: {back_home}"); problems += not back_home
            for href in pages:
                await pg.goto(base + sec); await pg.click(f'a.card[href="{href}"]'); await pg.wait_for_load_state("load")
                await pg.wait_for_timeout(300)
                title = await pg.title()
                back = pg.locator("a.homelink, nav.mr-back a").first
                ok_back = await back.count() == 1
                if ok_back:
                    await back.click(); await pg.wait_for_load_state("load")
                returned = pg.url == base + sec
                print(f"   {href:38} {title[:46]:46} | back to {sec}: {returned}")
                problems += (not ok_back) + (not returned)
        await pg.goto(base + "ks5/algorithms-lab.html"); await pg.wait_for_timeout(500)
        fonts = await pg.evaluate("document.fonts.ready.then(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight))")
        print("fonts loaded on the lab:", sorted(set(fonts))); problems += not any("Atkinson" in f for f in fonts)
        for old in MOVED:
            await pg.goto(base + "python/" + old + ".html#keep"); await pg.wait_for_load_state("load"); await pg.wait_for_timeout(200)
            ok = pg.url == base + "ks3/" + old + ".html#keep"
            print(f"old link python/{old}.html redirects: {ok}"); problems += not ok

        # one real check per family, to prove Python loads from the hosted page
        await pg.goto(base + "ks3/escape-the-dungeon-2.html")
        await pg.click(".lvcard.lv-B")
        await pg.click('#dots [data-go="4"]')
        art = pg.locator('[data-part="p4b3"]')
        await art.locator("textarea").fill(G2["p4b3"][0])
        await art.locator(".check").click()
        await art.locator(".msg.pass, .msg.warn, .msg.error").first.wait_for(timeout=90000)
        msg = (await art.locator(".msg").first.inner_text()).replace("\n", " | ")
        print("Part 2 check:", msg[:60]); problems += "passed" not in msg

        await pg.goto(base + "ks3/python-rescue.html#loop")
        fix = pg.locator("#fixslot .runner")
        await fix.locator(".run").click()
        await fix.locator(".msg").first.wait_for(timeout=90000)
        msg = (await fix.locator(".msg").first.inner_text()).replace("\n", " | ")
        print("Rescue run:", msg[:60]); problems += "finished" not in msg

        allowed = {"cdn.jsdelivr.net"}
        print("other sites contacted:", sorted(outside)); problems += len(outside - allowed)
        print("page errors:", errs)
        problems += len(errs)
        await br.close()
    print("problems:", problems)
    return problems


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else serve()
    sys.exit(1 if asyncio.run(main(base.rstrip("/") + "/")) else 0)
