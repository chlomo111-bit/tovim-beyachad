"""Reel « יום 3 » (30.10.2026) : capture du vrai jeu avec les VRAIS passagers (fichier JSON PAX), calée mot à mot sur la voix.
Usage : PAX=passagers.json python3 tools/reel_jour3.py <dossier_three3> <dossier_images>"""
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
         "#ui,#gate,#skip,#newsModal{display:none!important}.lbl3{font-size:17px!important;padding:3px 9px!important}</style>")
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
            elif "supabase.co" in u and "/rest/v1/passengers" in u:
                r.fulfill(status=200, body=open(os.environ["PAX"]).read(), content_type="application/json")
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
            if per: pg.evaluate(re.sub(r"\bK\b", "0", per))
            n = int(round(seconds * 30))
            for i in range(n):
                shot(re.sub(r"\bK\b", f"{i/30:.4f}", per))
            print(name, "images", start, "->", frame[0] - 1, flush=True)

        pg.evaluate("mode='sea';started=true;setShip(shipIdx(totalN()));setEvent({type:'shark',title:''});R.top('יום 3','<b>'+totalN()+'</b>/25 נוסעים');document.querySelector('#gate').hidden=true")
        V="const c=ship.view;"
        # 0–4.2 : יש פה סירה שכולם מנסים להטביע… ואנחנו כמעט שם
        scene("s1", 4.2, "flash(1,.6)",
              V+"R.orbit(K,c.d*.7-K*1.5,c.h*1.8+2.5,c.h*.2,0.4,0.15);R.cap(K<2.5?'יש פה סירה שכולם<br>מנסים <em>להטביע</em> 😈':'ואנחנו <em>כמעט שם</em>…')")
        # 4.2–7.4 : יום שלישי על הסיפון, וכבר 20 נוסעים עלו
        scene("s2", 3.2, "flash(.5,.3)",
              V+"R.orbit(K,c.d*.5,c.h*1.4+1.8,c.h*.25,1.2,0.22);R.cap(K<1.4?'<em>יום 3</em> על הסיפון 🚢':'וכבר <em>20 נוסעים</em> עלו!')")
        # 7.4–11.6 : המקום הראשון בטבלה… 1,470 מטבעות
        scene("s3", 4.2, "window._ip=byH.get('mor.levi134');flash(.5,.3)",
              "{const w=worldOf(_ip,new THREE.Vector3());const d=10-K*.7;R.cam(w.x+d*.75,w.y+d*.75,w.z+d*.6,w.x,w.y+.4,w.z)}"
              "R.cap(K<1.7?'והמקום <em>הראשון</em> בטבלה… 🏆':'<span dir=ltr>@mor.levi134</span><br><em>1,470 מטבעות</em> 🪙')")
        # 11.6–16.3 : וברגע שהסירה טובעת, נפתח שטר של 20 ₪ אמיתיים
        scene("s4", 4.7, "billet=null;CONFIG.BILLET.on=false;ship.group.add(noteMesh);noteMesh.visible=true;noteMesh.position.set(1,.75,ship.beam/2+2.2);noteMesh.scale.setScalar(2.6);water.material.opacity=.45;flash(.4,.4)",
              V+"{const n=ship.group.localToWorld(noteMesh.position.clone());R.cam(n.x+6.5-K*.6,n.y+8-K*.7,n.z+8-K*.5,n.x,n.y,n.z-1)}"
              "R.cap(K<2.1?'וברגע שהסירה <em>טובעת</em>…':'נפתח <em>שטר של 20₪</em> אמיתיים 💸')")
        pg.evaluate("water.material.opacity=.93;noteMesh.visible=false;noteMesh.scale.setScalar(1);if(noteMesh.parent)noteMesh.parent.remove(noteMesh)")
        # 16.3–18.4 : נשארו רק 5 נוסעים
        scene("s5", 2.1, "R.top('5','נוסעים חסרים');flash(.8,.3);$('#alarm').classList.add('on')",
              V+"R.orbit(K,c.d*.5-K*2,c.h*1.3+1.5,c.h*.25,3.4,0.3);R.cap('נשארו רק <em>5</em> נוסעים! 😱')")
        pg.evaluate("$('#alarm').classList.remove('on')")
        # 18.4–21.3 : ועכשיו… כריש מסתובב סביב הספינה
        scene("s6", 2.9, "R.top('🦈','האירוע של היום')",
              "{const f=evProps.fin;if(f){const p=f.position;const a=Math.atan2(p.z,p.x);R.cam(p.x+Math.cos(a)*9,4.5,p.z+Math.sin(a)*9,p.x*.6,0,p.z*.6)}}"
              "R.cap(K<.7?'ועכשיו…':'<em>כריש</em> מסתובב<br>סביב הספינה 🦈')")
        # 21.3–25.8 : כתבו עולה בתגובות, ותביאו חבר. אולי בזכותכם היא טובעת
        scene("s7", 4.5, "R.top('יום 3','<b>20</b>/25 נוסעים');flash(.5,.3)",
              V+"R.orbit(K,c.d*.6,c.h*1.5+2,c.h*.25,4.9,0.2);R.cap(K<1.6?'כתבו <em>\"עולה\"</em> בתגובות 👇':K<2.8?'כתבו <em>\"עולה\"</em> בתגובות 👇<small>ותביאו חבר 🧍</small>':'אולי <em>בזכותכם</em><br>היא טובעת! 🌊')")
        # 25.8–29.8 : ומה יקרה מחר? התגובה עם הכי הרבה לייקים קובעת
        scene("s8", 4.0, "R.hideTop()",
              V+"R.orbit(K,c.d*.85+K*1.5,c.h*2+2+K*.5,c.h*.1,5.6,0.08);R.cap(K<1.3?'ומה יקרה <em>מחר</em>? 👀':'התגובה עם <em>הכי הרבה לייקים</em> קובעת 👇')")

        print("TOTAL images", frame[0], "ERREURS", errs[:5])
        b.close()

main()
