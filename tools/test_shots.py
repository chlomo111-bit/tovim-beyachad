"""Test visuel du jeu : python3 tools/test_shots.py <dossier_three3> <dossier_sortie> [hash...]
Charge index.html en local (Three.js et Heebo servis depuis node_modules), clique sur l'entrée,
attend, prend des captures et affiche les erreurs JavaScript."""
import sys, time, os
from playwright.sync_api import sync_playwright

SP, OUT = sys.argv[1], sys.argv[2]
HASHES = sys.argv[3:] or [""]
T = SP + "/node_modules/three/"
F = SP + "/node_modules/@fontsource/heebo/files/"
GAME = os.environ.get("GAME", "index.html")
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    for hsh in HASHES:
        pg = b.new_page(viewport={"width": 430, "height": 860}, device_scale_factor=1)
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append("console:" + m.text) if m.type == "error" else None)

        def route(r):
            u = r.request.url
            if "three.min.js" in u: r.fulfill(path=T + "build/three.min.js", content_type="text/javascript")
            elif "OrbitControls" in u: r.fulfill(path=T + "examples/js/controls/OrbitControls.js", content_type="text/javascript")
            elif "fonts.googleapis" in u: r.fulfill(body="", content_type="text/css")
            elif u.startswith("http://test/"):
                path = u.split("http://test/", 1)[1].split("#")[0].split("?")[0] or GAME
                if os.path.exists(path): r.fulfill(path=path)
                else: r.fulfill(status=404, body="")
            else: r.abort()

        pg.route("**/*", route)
        pg.goto("http://test/" + GAME + hsh, wait_until="commit", timeout=90000)
        time.sleep(4)
        name = (hsh.strip("#").replace("=", "-") or "home")
        pg.screenshot(path=f"{OUT}/{name}_0gate.png")
        if hsh in ("", "#demo=60", "#demo=600", "#demo=5000", "#demo=20000") or hsh.startswith("#demo") or hsh.startswith("#ev"):
            pg.click("#enter")
            time.sleep(2.5); pg.screenshot(path=f"{OUT}/{name}_1intro.png")
            time.sleep(7)
            if pg.is_visible("#newsOk"): pg.click("#newsOk")
            time.sleep(1.5); pg.screenshot(path=f"{OUT}/{name}_2sea.png")
            pg.evaluate("controls.autoRotate=false;const c=ship.view;camera.position.set(c.d*.35,c.h*.9+2,c.d*.3);controls.target.set(0,c.h*.4,0)")
            time.sleep(1.5); pg.screenshot(path=f"{OUT}/{name}_3close.png")
        else:
            for i in range(4):
                time.sleep(3); pg.screenshot(path=f"{OUT}/{name}_{i+1}.png")
        print(hsh or "(home)", "ERREURS:", errs[:8])
        pg.close()
    b.close()
