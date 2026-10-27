"""Captures rapides de scènes précises : python3 tools/test_scenes.py <three3> <sortie>"""
import sys, time, os
from playwright.sync_api import sync_playwright
SP,OUT=sys.argv[1],sys.argv[2];T=SP+"/node_modules/three/";os.makedirs(OUT,exist_ok=True)
SCENES=[("liner","#demo=5000",""),("cruise","#demo=15000",""),("storm","#demo=60&ev=storm",""),("shark","#demo=60&ev=shark",""),
        ("kraken","#demo=400&ev=kraken",""),("party","#demo=400&ev=party",""),("iceberg","#demo=400&ev=iceberg",""),("whale","#demo=400&ev=whale","W")]
ONLY=os.environ.get("ONLY")
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist"])
    for name,h,flag in SCENES:
        if ONLY and name not in ONLY.split(","): continue
        pg=b.new_page(viewport={"width":430,"height":860});errs=[]
        pg.on("pageerror",lambda e:errs.append(str(e)))
        def route(r):
            u=r.request.url
            if "three.min.js" in u:r.fulfill(path=T+"build/three.min.js",content_type="text/javascript")
            elif "OrbitControls" in u:r.fulfill(path=T+"examples/js/controls/OrbitControls.js",content_type="text/javascript")
            elif u.startswith("http://test/"):r.fulfill(path="index.html")
            else:r.abort()
        pg.route("**/*",route);pg.goto("http://test/index.html"+h,wait_until="commit",timeout=90000);pg.wait_for_function("typeof END!==\"undefined\" && typeof ship===\"object\" && ship",timeout=90000);time.sleep(2)
        pg.evaluate("started=true;introT=END;endIntro();document.querySelector('#newsModal').hidden=true;controls.autoRotate=false;const c=ship.view;camera.position.set(c.d*.8,c.h*1.2+2,c.d*.6);controls.target.set(0,c.h*.3,0)")
        if flag=="W": pg.evaluate("clock.elapsedTime=0")
        time.sleep(4);pg.screenshot(path=f"{OUT}/{name}.png",timeout=120000)
        print(name,"ERREURS:",errs[:5]);pg.close()
    b.close()
