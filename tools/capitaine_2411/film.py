"""Reel « הקפטן מספר » : filme le plateau 3D du capitaine (sans texte) à FPS i/s.
Usage (racine du dépôt tovim-beyachad) : AMP=amp.json DUR=16 FPS=15 DSF=1.3 python3 tools/capitaine_2311/film.py /root/three3 <dossier_sortie> [frames]
AMP = liste d'amplitudes de la voix (0..1) à 30 valeurs/s, dans la timeline FINALE de la voix."""
import sys, os, time, json
from playwright.sync_api import sync_playwright
SP, OUT = sys.argv[1], sys.argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
T = SP + "/node_modules/three/"
src = open("index.html").read()
html = src.split("<body>", 1)[1].rsplit("</body>", 1)[0]
page_html = "<!doctype html><html lang='he' dir='rtl'><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'><style>#ui,#gate,#skip,#newsModal,#cap,#reelTop,#fade,#lbls,.lbl3,.lbls,.lbl{display:none!important}</style></head><body>" + html + "</body></html>"
os.makedirs(OUT, exist_ok=True)
FPS = int(os.environ.get("FPS", 15)); DUR = float(os.environ.get("DUR", 16))
ONLY = os.environ.get("FRAMES")
AMP = json.load(open(os.environ["AMP"])) if os.environ.get("AMP") else []
with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=float(os.environ.get("DSF", 1.3)))
    pg.add_init_script("window.CAP=true;Math.random=(()=>{let s=4242;return()=>{s=(s*16807)%2147483647;return(s-1)/2147483646}})();")
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    def route(r):
        u = r.request.url
        if "three.min.js" in u: r.fulfill(path=T + "build/three.min.js", content_type="text/javascript")
        elif "OrbitControls" in u: r.fulfill(path=T + "examples/js/controls/OrbitControls.js", content_type="text/javascript")
        elif "supabase.co" in u and "/rest/v1/passengers" in u: r.fulfill(status=200, body="[]", content_type="application/json")
        elif "supabase.co" in u: r.fulfill(status=200, body="[]" if "/rpc/" not in u else "{}", content_type="application/json")
        elif u.startswith("http://test/"): r.fulfill(body=page_html, content_type="text/html")
        else: r.abort()
    pg.route("**/*", route)
    pg.goto("http://test/", wait_until="commit", timeout=90000)
    pg.wait_for_function("typeof window.loop==='function' && typeof ship==='object' && ship", timeout=120000)
    time.sleep(3)
    pg.evaluate("mode='sea';started=true;document.querySelector('#gate').hidden=true;try{tvGroup.visible=false}catch(e){};ship.group.visible=false;SND.muted=true;try{controls.maxDistance=500;controls.minDistance=0;controls.enableDamping=false}catch(e){};window.capHook=function(){}")
    pg.evaluate("window.AMP=%s" % json.dumps(AMP))
    pg.evaluate("window.SHOTF=function(t){" + open(HERE + "/shot.js").read() + "}")
    for _ in range(30): pg.evaluate("loop()")
    N = int(round(DUR * FPS))
    for i in range(N):
        skip = ONLY and str(i) not in ONLY.split(",")
        for _ in range(max(1, 30 // FPS)): pg.evaluate("window.TS=%f;SHOTF(%f);loop()" % (i / FPS, float(os.environ.get("TOFF", 0)) + i / FPS * float(os.environ.get("TSC", 1))))
        if not skip: pg.screenshot(path=f"{OUT}/f{i:04d}.jpg", type="jpeg", quality=90)
    print("frames", N, "ERREURS", errs[:5]); b.close()
