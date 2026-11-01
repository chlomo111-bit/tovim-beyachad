"""Reel « יום 5 » (1.11.2026) : capture du vrai jeu avec les VRAIS passagers (fichier JSON PAX), calée mot à mot sur la voix.
Usage : PAX=passagers.json python3 tools/reel_jour5.py <dossier_three3> <dossier_images>"""
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
            n = int(round(seconds * 30)) - start  # 1.11 : « seconds » = instant de FIN absolu (calé sur la voix), pas de dérive
            for i in range(n):
                shot(re.sub(r"\bK\b", f"{i/30:.4f}", per))
            print(name, "images", start, "->", frame[0] - 1, flush=True)

        pg.evaluate("""mode='sea';started=true;setShip(shipIdx(totalN()));setEvent({type:'party',title:''});
tv={day:'2026-11-01',handle:'shahar_b.y',text:'תעשו שיציבו פסל בספינה של דולפין או סוס ים',likes:0};tvDraw();
document.querySelector('#gate').hidden=true;R.hideTop();
const HS=['pirate','chef','party','bucket','straw','tophat','cap','beanie'];P.forEach((p,i)=>{if(i%3===0)p.style={hat:HS[i%HS.length]}});rebuild();""")
        V="const c=ship.view;"
        # 0–9.9 : naufrage de la barque → tout le monde passe sur le bateau de pêche
        scene("s1", 9.9, "tvGroup.visible=false;startSink(0,1);flash(1,.6)",
              "R.cap(K<1.1?'זה <em>קרה!</em> 😱':K<3.3?'הסירה הראשונה <em>טבעה!</em> 🌊':K<6.5?'<em>25 נוסעים</em>…<small>והיא פשוט לא החזיקה</small>':K<8.15?'כולם <em>קפצו למים!</em> 🏊':'…ועלו ל<em>ספינת הדייגים</em> 🎣')")
        pg.evaluate("endSink();setShip(1);rebuild();tvGroup.visible=false")
        # 9.9–13.4 : יום חמישי על הסיפון, וכבר 39 נוסעים
        scene("s2", 13.4, "R.top('יום 5','<b>39</b>/100 נוסעים');flash(.5,.3)",
              V+"R.orbit(K,c.d*.7,c.h*1.6+3,c.h*.1,1.1,0.16);R.cap(K<1.4?'<em>יום 5</em> על הסיפון 🚢':'וכבר <em>39 נוסעים</em>!')")
        # 13.4–18.2 : ושחר ביקשה פסל דולפין ענק… והנה הוא עומד על הסיפון
        scene("s3", 18.2, "R.hideTop();flash(.5,.3)",
              "{const w=dolphinMesh.getWorldPosition(new THREE.Vector3()),a=.9+K*.18,d=16-K*1.2;R.cam(w.x+Math.cos(a)*d,w.y+5.5-K*.4,w.z+Math.sin(a)*d,w.x,w.y+1.6,w.z)}"
              "R.cap(K<2.5?'<span dir=ltr>@shahar_b.y</span> ביקשה <em>פסל דולפין</em> 🐬':'והנה הוא… <em>על הסיפון!</em> ✨')")
        # 18.2–22.4 : PAUSE journal du jour au studio TV (commentaire le plus liké)
        scene("pause", 22.4, "tvGroup.visible=true;R.top('📺','חדשות הספינה');flash(.9,.4)",
              V+"{const k=Math.min(1,K/1.6),e=k*k*(3-2*k),p=tvGroup.position,S=tvGroup.userData.S;"
              "const ax=c.d*.4,ay=c.h*2+4,az=c.d*.8,bx=p.x+2.6*S,by=p.y+3.3*S,bz=p.z+12.5*S;"
              "R.cam(ax+(bx-ax)*e,ay+(by-ay)*e+Math.sin(e*Math.PI)*5,az+(bz-az)*e,p.x*e+(p.x+.9*S-p.x)*e,(p.y+2.3*S)*e,(p.z-1*S)*e)}"
              "R.cap(K<.8?'<span style=\"background:#E8262C;color:#fff;padding:6px 26px;border-radius:14px\">🔴 מבזק</span>':K<2.7?'ועכשיו… <em>חדשות הספינה</em> 📺':'מהערב: ההגרלה של <em>20:00</em>')")
        # 22.4–27.6 : שווה אלף מטבעות… והזוכה מחליט מה יקרה מחר בספינה
        scene("s5", 27.6, "tvGroup.visible=false;R.top('🎟️','ההגרלה של הערב');flash(.6,.3)",
              V+"R.orbit(K,c.d*.8,c.h*2+4,c.h*.1,2.3,0.11);R.cap(K<2.6?'שווה <em>1,000 מטבעות</em> 🪙':'והזוכה <em>מחליט/ה</em> מה יקרה מחר! ✨')")
        # 27.6–31.95 : מגיבים על הפוסט של היום, אוספים רק 100 מטבעות, ואתם בפנים
        scene("s6", 31.95, "R.top('יום 5','<b>39</b>/100 נוסעים')",
              V+"R.orbit(K,c.d*.45,c.h*1.4+2,c.h*.2,3.2,0.14);"
              "R.cap(K<1.7?'💬 מגיבים על <em>הפוסט של היום</em>':K<3.4?'💬 מגיבים על <em>הפוסט של היום</em><small>+ 🪙 רק 100 מטבעות</small>':'ואתם <em>בפנים!</em> 🎟️')")
        # 31.95–35.9 : ובקרוב על הסיפון… חכות דייג וכובעים לקנות
        scene("s7", 35.9, "R.hideTop();flash(.5,.3)",
              V+"{const p=draw[3]||draw[0];const w=worldOf(p,new THREE.Vector3());R.cam(w.x+3.4,w.y+2.6,w.z+4.2,w.x,w.y+.9,w.z)}"
              "R.cap(K<1.6?'ובקרוב על הסיפון… 👀':'🎣 <em>חכות דייג</em> + 🎩 <em>כובעים</em>!')")
        # 35.9–40.4 : ומה יקרה מחר? התגובה עם הכי הרבה לייקים קובעת
        scene("s8", 40.4, "flash(.4,.3)",
              V+"R.orbit(K,c.d*.9+K*1.5,c.h*2.4+4+K*.5,0,4.2,0.08);R.cap(K<1.4?'ומה יקרה <em>מחר</em>? 👀':'התגובה עם <em>הכי הרבה לייקים</em> קובעת 👇')")

        print("TOTAL images", frame[0], "ERREURS", errs[:5])
        b.close()

main()
