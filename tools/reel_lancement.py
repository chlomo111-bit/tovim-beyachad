"""Reel de lancement « טובעים ביחד » : capture image par image (1080×1920, 30 i/s) du vrai jeu.
Usage : python3 tools/reel_lancement.py <dossier_three3> <dossier_images>
Les passagers des scènes de démonstration sont anonymes (aucune étiquette @)."""
import sys, os, time, json, re
from playwright.sync_api import sync_playwright

SP, OUT = sys.argv[1], sys.argv[2]
T = SP + "/node_modules/three/"
F = SP + "/node_modules/@fontsource/heebo/files/"
os.makedirs(OUT, exist_ok=True)
ONLY = os.environ.get("ONLY")  # pour tester une seule scène
SAMPLE = int(os.environ.get("SAMPLE", "1"))  # 1 = toutes les images
FROM = int(os.environ.get("FROM", "0"))  # reprendre une capture : images déjà faites jusqu'à FROM-1

src = open("index.html").read()
html = src.split("<body>", 1)[1].rsplit("</body>", 1)[0]
fonts = ("<style>@font-face{font-family:Heebo;font-weight:900;src:url(http://test/h900.woff2);unicode-range:U+0590-05FF,U+20AA}"
         "@font-face{font-family:Heebo;font-weight:900;src:url(http://test/l900.woff2);unicode-range:U+0000-00FF}"
         "@font-face{font-family:Heebo;font-weight:700;src:url(http://test/h700.woff2)}"
         "#cap{bottom:16%!important;font-size:64px!important;line-height:1.18!important}"
         "#cap small{display:block;font-size:44px;margin-top:14px;color:#fff}"
         "#reelTop .d{font-size:96px!important}#reelTop .n{font-size:46px!important}"
         ".lbls,#ui,#gate,#skip,#newsModal{display:none!important}</style>")
page_html = "<!doctype html><html lang='he' dir='rtl'><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>" + fonts + "</head><body>" + html + "</body></html>"

DIRECTOR = r"""
window.R={};
R.hideTop=()=>{$('#reelTop').hidden=true};
R.top=(d,n)=>{$('#reelTop').hidden=false;$('#reelDay').textContent=d;$('#reelN').innerHTML=n};
R.cam=(px,py,pz,tx,ty,tz)=>{camera.position.set(px,py,pz);controls.target.set(tx,ty,tz);camera.lookAt(controls.target)};
R.orbit=(k,dist,h,ty,a0,speed)=>{const a=a0+k*speed;R.cam(Math.cos(a)*dist,h,Math.sin(a)*dist,0,ty,0)};
R.reset=(n)=>{P.length=0;byH.clear();if(n)ingest(demoData(n));};
R.cap=(h)=>caption(h);
"""

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
        pg = b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
        pg.add_init_script("window.CAP=true")
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))

        def route(r):
            u = r.request.url
            if "three.min.js" in u: r.fulfill(path=T + "build/three.min.js", content_type="text/javascript")
            elif "OrbitControls" in u: r.fulfill(path=T + "examples/js/controls/OrbitControls.js", content_type="text/javascript")
            elif u.endswith("h900.woff2"): r.fulfill(path=F + "heebo-hebrew-900-normal.woff2", content_type="font/woff2")
            elif u.endswith("l900.woff2"): r.fulfill(path=F + "heebo-latin-900-normal.woff2", content_type="font/woff2")
            elif u.endswith("h700.woff2"): r.fulfill(path=F + "heebo-hebrew-700-normal.woff2", content_type="font/woff2")
            elif "supabase.co" in u:
                r.fulfill(status=200, body="[]" if "/rpc/" not in u else "{}", content_type="application/json")
            elif u.startswith("http://test/"):
                r.fulfill(body=page_html, content_type="text/html")
            else: r.abort()

        pg.route("**/*", route)
        pg.goto("http://test/", wait_until="commit", timeout=90000)
        pg.wait_for_function("typeof window.loop==='function' && typeof ship==='object' && ship", timeout=120000)
        time.sleep(4)
        pg.evaluate(DIRECTOR)
        pg.evaluate("billet=null;applyBillet&&applyBillet();CONFIG.BILLET.on=false;noteMesh.visible=false;SND.muted=true")
        frame = [int(os.environ.get("START", "0"))]  # START : numéro de la 1re image quand on refait seulement quelques scènes (ONLY)

        def shot(js=""):
            pg.evaluate("loop();" + js)
            if frame[0] >= FROM and frame[0] % SAMPLE == 0:
                pg.screenshot(path=f"{OUT}/f{frame[0]:05d}.jpg", type="jpeg", quality=92, timeout=180000)
            frame[0] += 1

        def scene(name, seconds, setup, per):
            if ONLY and name not in ONLY.split(","):
                return
            start = frame[0]
            pg.evaluate(setup)
            n = int(round(seconds * 30))
            for i in range(n):
                shot(re.sub(r"\bK\b", f"{i/30:.4f}", per))
            print(name, "images", start, "->", frame[0] - 1, flush=True)

        # A. Hook (1,5 s) : la barque en gros plan qui tangue
        scene("hook", 1.5,
              "R.reset(8);setShip(0);mode='sea';started=true;R.hideTop();flash(1,.6)",
              "R.orbit(K,7.6,2.7,0.5,0.6,0.25);R.cap('המשחק שבו כולם רוצים <em>להטביע</em> את הספינה 😈')")

        # B. Intro (8,75 s) : la Terre → la mer, textes calés sur la voix 1
        scene("intro", 8.75,
              "R.cap('');mode='intro';introT=-1;camIntro.f=0;started=true",
              "if(introT-IT.space>IT.b)R.cap('עלו <em>לסיפון!</em> 🚢')")

        # C. Remplissage (4 s) : 0 → 24 passagers anonymes, l'eau monte
        scene("remplissage", 3.65,
              "mode='sea';R.reset(0);setShip(0);window._fill=demoData(24);window._fi=0",
              "{const want=Math.min(24,Math.floor(K*7.2));while(_fi<want){ingest([_fill[_fi++]]);}rebuild();"
              "R.top(fmtN(totalN())+'/25','🛶 סירת המשוטים');R.orbit(K,10,4,0.4,0.9,0.12);"
              "R.cap('כל עוקב חדש = הספינה <em>שוקעת עוד</em> 🌊')}")

        # D. Naufrage (10,5 s) : le 25e passager monte → la barque coule → le bateau de pêche sort de l'eau
        scene("naufrage", 7.4,
              "ingest([{handle:'last_one_25',vip:false,style:{},joined_ship:0,refs:0,streak:0,created_at:new Date().toISOString()}]);"
              "SINK.fake=undefined;startSink(0,1);SINK.who=null;R.hideTop()",
              "SINK.t0-=0.3/30;if(K<2.9)R.cap('ב־25 נוסעים… <em>היא טובעת!</em>');else R.cap('כולם עוברים <em>לספינה הבאה</em> 🔄')")
        pg.evaluate("if(SINK.on)endSink()")

        # E. Les objectifs (6,5 s) : les 5 bateaux, du plus petit au plus grand
        ladder = [(0, 20, "25", "🛶 סירת משוטים"), (1, 70, "100", "🎣 ספינת דייגים"), (2, 700, "1,000", "⛴️ מעבורת"),
                  (3, 6000, "10,000", "🚢 אוניית קיטור"), (4, 12000, "100,000", "🛳️ ספינת קרוז ענקית")]
        for i, n, d, label in ladder:
            scene(f"objectif{i}", 1.22,
                  f"R.reset({n});setShip({i});mode='sea';R.top('{d}','{label}');R.cap('');flash(.5,.3)",
                  f"{{const c=ship.view;R.orbit(K,c.d*.95,c.h*1.25,c.h*.3,0.7,0.18)}}")

        # F. Le badge (2,5 s) : gros plan sur un passager avec couronne et gilet doré
        scene("badge", 3.5,
              "mode='sea';started=true;R.reset(14);setShip(1);R.hideTop();{const p=draw[2];p.style={hat:'crown'};p.vip=true;rebuild();window._bp=p}",
              "{const w=worldOf(_bp,new THREE.Vector3());R.cam(w.x+2.6-K*.25,w.y+1.3,w.z+1.6,w.x,w.y+.8*figS,w.z)}"
              "R.cap('💥 מי שמטביע את הספינה <em>מקבל תג מיוחד</em><small>🌊 כל טביעה = עוד תג לנוסעים</small>')")

        # G. Le billet (3 s) : un billet de 20 ₪ qui brille sur le pont
        scene("billet", 4.6,
              "mode='sea';started=true;R.reset(6);setShip(1);CONFIG.BILLET.on=true;billet={day:'d',slot:1,prize:20,winner:null};placeBillet();noteMesh.position.set(1.2,1.35,0);noteMesh.scale.setScalar(2.2);flash(.6,.4)",
              "{const n=noteMesh.position.clone();ship.group.localToWorld(n);R.cam(n.x+1.9-K*.2,n.y+1.3,n.z+1.6,n.x,n.y-.1,n.z)}"
              "R.cap('💸 <em>3 שטרות של 20₪</em> מוסתרים כל יום')")
        pg.evaluate("CONFIG.BILLET.on=false;billet=null;noteMesh.scale.setScalar(1);placeBillet()")

        # H. Les règles (4,5 s)
        scene("regles", 4.6,
              "R.reset(10);setShip(0);R.hideTop()",
              "R.orbit(K,7,2.6,0.4,2.2,0.15);{const L=['➕ עקבו = <em>עולים לסיפון</em>','💬 כתבו \"עולה\" = <em>נוסע VIP</em> ⭐','❤️ לייק = עוד אנשים <em>מגלים את הספינה</em>'];"
              "const n=K<1.25?0:K<2.3?1:K<3.3?2:3;R.cap(n?'<span style=\"font-size:50px;line-height:1.35\">'+L.slice(0,n).join('<br>')+'</span>':'אז איך <em>עולים לסיפון?</em>')}")

        # I. Fin (3,5 s)
        scene("fin", 3.6,
              "R.reset(0);setShip(0);R.top('25','מקומות בסירה הראשונה')",
              "R.orbit(K,7.5+K*.5,3+K*.3,0.3,0.7,0.1);R.cap('🚢 הספינה <em>מחכה רק לכם!</em><small>הקישור בביו 🔗</small>')")

        print("TOTAL images", frame[0], "ERREURS", errs[:5])
        b.close()

main()
