"""Fond de story (1080×1920) filmé dans le vrai jeu, avec les VRAIS passagers.
Usage : python3 tools/story_fond.py <dossier_three3> <passagers.json> <sortie.png> [focus_handle]
passagers.json = liste [{handle, vip, style, joined_ship, refs, streak, created_at}] (copie de la table passengers).
Installer d'abord : mkdir three3 && cd three3 && npm i three@0.128.0 @fontsource/heebo"""
import sys, time, json
from playwright.sync_api import sync_playwright
T = sys.argv[1] + "/node_modules/three/"; PAX = json.load(open(sys.argv[2])); OUT = sys.argv[3]
FOCUS = sys.argv[4] if len(sys.argv) > 4 else ""
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
    pg.add_init_script("window.CAP=true")
    def route(r):
        u = r.request.url
        if "three.min.js" in u: r.fulfill(path=T + "build/three.min.js", content_type="text/javascript")
        elif "OrbitControls" in u: r.fulfill(path=T + "examples/js/controls/OrbitControls.js", content_type="text/javascript")
        elif u.startswith("http://test/"): r.fulfill(path="index.html")
        elif "supabase.co" in u: r.fulfill(status=200, body="[]", content_type="application/json")
        else: r.abort()
    pg.route("**/*", route); pg.goto("http://test/index.html", wait_until="commit", timeout=90000)
    pg.wait_for_function("typeof window.loop==='function' && typeof ship==='object' && ship", timeout=120000); time.sleep(3)
    pg.evaluate("(pax)=>{P.length=0;byH.clear();ingest(pax);setShip(shipIdx(totalN()));mode='sea';started=true;"
                "['#ui','#gate','#reelTop','#cap','#skip','#newsModal'].forEach(s=>{const e=document.querySelector(s);if(e)e.style.display='none'})}", PAX)
    cam = ("const f=byH.get(%s);if(f&&f.slot){const w=worldOf(f,new THREE.Vector3());camera.position.set(w.x+4.2*Math.max(1,figS*1.5),w.y+3.4,w.z+4.6);controls.target.set(w.x-.4,w.y+.2,w.z)}"
           "else{const c=ship.view;camera.position.set(c.d*.62,c.h*1.1+1.5,c.d*.5);controls.target.set(0,c.h*.25,0)}camera.lookAt(controls.target);lblT=-1") % json.dumps(FOCUS)
    for i in range(30): pg.evaluate("loop();" + cam)
    pg.screenshot(path=OUT); b.close()
print("ok", OUT)
