"""Capture image par image (mode CAP, 30 i/s) : python3 tools/test_cap.py <three3> <sortie> <hash> <nb_images> <pas>"""
import sys,time,os
from playwright.sync_api import sync_playwright
SP,OUT,H,N,STEP=sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]),int(sys.argv[5]);T=SP+"/node_modules/three/";os.makedirs(OUT,exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch(args=["--use-gl=swiftshader","--enable-webgl","--ignore-gpu-blocklist"]);pg=b.new_page(viewport={"width":405,"height":720});errs=[]
    pg.add_init_script("window.CAP=true");pg.on("pageerror",lambda e:errs.append(str(e)))
    def route(r):
        u=r.request.url
        if "three.min.js" in u:r.fulfill(path=T+"build/three.min.js",content_type="text/javascript")
        elif "OrbitControls" in u:r.fulfill(path=T+"examples/js/controls/OrbitControls.js",content_type="text/javascript")
        elif u.startswith("http://test/"):r.fulfill(path="index.html")
        else:r.abort()
    pg.route("**/*",route);pg.goto("http://test/index.html"+H,wait_until="commit",timeout=90000)
    pg.wait_for_function("typeof window.loop==='function' && typeof ship==='object' && ship",timeout=90000);time.sleep(3)
    for i in range(N):
        pg.evaluate("loop()")
        if i%STEP==0:pg.screenshot(path=f"{OUT}/f{i:04d}.png",timeout=120000)
    print("ERREURS",errs[:5]);b.close()
