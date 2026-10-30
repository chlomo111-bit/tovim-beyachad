"""Reel « יום 4 » (31.10.2026) : capture du vrai jeu avec les VRAIS passagers (fichier JSON PAX), calée mot à mot sur la voix.
Usage : PAX=passagers.json python3 tools/reel_jour4.py <dossier_three3> <dossier_images>"""
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

        pg.evaluate("""mode='sea';started=true;setShip(shipIdx(totalN()));setEvent({type:'shark',title:''});
tv={day:'2026-10-30',handle:'hyll.khbsvb',text:'מחר כריש חותך את הספינה לשתי חלקים ושתי הקבוצות נפרדות',likes:1};tvDraw();
document.querySelector('#gate').hidden=true;R.hideTop();
window.SPL={on:false,s:0};
window.split=function(){renderer.localClippingEnabled=true;const mk=(sx)=>{const pl=new THREE.Plane(new THREE.Vector3(sx,0,0),0);const g=ship.group.clone(true);
  g.traverse(o=>{if(o.material){o.material=o.material.clone();o.material.clippingPlanes=[pl]}});shipRoot.add(g);return {g,pl,sx}};
  SPL.a=mk(1);SPL.b=mk(-1);ship.group.visible=false;SPL.on=true;document.querySelector('.lbls').style.visibility='hidden'};
window.splitFrame=function(){if(!SPL.on)return;const s=SPL.s;for(const h of [SPL.a,SPL.b]){h.g.position.copy(ship.group.position);h.g.rotation.copy(ship.group.rotation);
  h.g.position.x+=h.sx*s;h.g.position.z+=h.sx*s*.7;h.g.rotation.y=h.sx*s*.04;h.pl.constant=-s}};
window.capHook=function(t){splitFrame()};""")
        V="const c=ship.view;"
        # 0–2.3 : הכריש לא רק הסתובב סביב הספינה
        scene("s1", 2.3, "tvGroup.visible=false;flash(1,.6)",
              "{const f=evProps.fin;if(f){const p=f.position;const a=Math.atan2(p.z,p.x);R.cam(p.x+Math.cos(a)*7,3.6,p.z+Math.sin(a)*7,p.x*.5,.5,p.z*.5)}}R.cap('הכריש לא רק <em>הסתובב</em>… 🦈')")
        # 2.3–4.3 : הוא חתך אותה לשניים
        scene("s2", 2.0, "split();flash(1,.5);$('#alarm').classList.add('on')",
              V+"SPL.s=Math.min(1,K/1.2)*Math.max(2.2,ship.len*.12);R.cam(c.d*.12,c.h*3+7,c.d*.62,0,0,0);R.cap('הוא <em>חתך אותה לשניים!</em> 😱')")
        pg.evaluate("$('#alarm').classList.remove('on')")
        # 4.3–7.6 : יום רביעי על הסיפון, וכבר 23 נוסעים
        scene("s3", 3.3, "R.top('יום 4','<b>23</b>/25 נוסעים');flash(.5,.3)",
              V+"R.orbit(K,c.d*.75,c.h*1.8+3,c.h*.1,1.1,0.18);R.cap(K<.9?'<em>יום 4</em> על הסיפון 🚢':'וכבר <em>23 נוסעים</em>!')")
        # 7.6–10.6 : PAUSE – jingle « מבזק », la caméra vole vers le studio
        scene("pause", 3.0, "tvGroup.visible=true;R.top('📺','חדשות הספינה');flash(.9,.4)",
              V+"{const k=Math.min(1,K/2.4),e=k*k*(3-2*k),p=tvGroup.position,S=tvGroup.userData.S;"
              "const ax=c.d*.4,ay=c.h*2+4,az=c.d*.8,bx=p.x+2.6*S,by=p.y+3.3*S,bz=p.z+15*S;"
              "R.cam(ax+(bx-ax)*e,ay+(by-ay)*e+Math.sin(e*Math.PI)*6,az+(bz-az)*e,p.x*e,(p.y+2.3*S)*e,(p.z-1*S)*e)}"
              "R.cap('<span style=\"background:#E8262C;color:#fff;padding:6px 26px;border-radius:14px\">🔴 מבזק</span>')")
        # 10.6–15.4 : ועכשיו חדשות הספינה. התגובה של היום עם הכי הרבה לייקים
        scene("s5", 4.8, "",
              "{const p=tvGroup.position,S=tvGroup.userData.S,d=15-K*1.2;R.cam(p.x+2.6*S,p.y+3.3*S,p.z+d*S,p.x+.9*S,p.y+2.3*S,p.z-1*S)}"
              "R.cap(K<1.9?'ועכשיו… <em>חדשות הספינה</em> 📺':'התגובה של היום – <em>הכי הרבה לייקים</em> ❤️')")
        # 15.4–20.9 : היל כתב "..." והנה זה קרה
        scene("s6", 5.5, "R.hideTop()",
              "{const p=tvGroup.position,S=tvGroup.userData.S,d=9.5-K*.4;R.cam(p.x-1*S,p.y+3*S,p.z+d*S,p.x-1.1*S,p.y+2.9*S,p.z-2*S)}"
              "R.cap(K<4.3?'<span dir=ltr>@hyll.khbsvb</span> כתב 👆':'והנה זה <em>קרה!</em> 🦈')")
        # 20.9–28.0 : עכשיו חצי ספינה פה, חצי ספינה שם… ועוד 2 נוסעים בלבד והכל טובע
        scene("s7", 7.1, "tvGroup.visible=false;flash(.6,.3)",
              V+"SPL.s=Math.max(2.2,ship.len*.12)*(1+K*.05);R.orbit(K,c.d*.55,c.h*2.6+5,0,1.6,0.12);"
              "if(K<1.95)R.cap('חצי ספינה <em>פה</em>…');else if(K<3.9)R.cap('…חצי ספינה <em>שם</em>');else{R.top('2','נוסעים חסרים');R.cap('ועוד <em>2 נוסעים</em> בלבד…<small>והכול טובע 🌊</small>')}")
        # 28.0–36.3 : והערב במוצאי שבת שתי הגרלות של 20₪…
        scene("s8", 8.3, "R.top('🎟️','הגרלות הערב');flash(.6,.3)",
              V+"R.orbit(K,c.d*.85,c.h*2+4,c.h*.1,2.5,0.1);"
              "R.cap(K<2.0?'והערב, <em>במוצאי שבת</em> 🌙':K<4.3?'<em>2 הגרלות</em> של 20₪ 💸':K<5.8?'של <em>שישי</em> ושל <em>שבת</em>':'ב־<em>20:00</em> בדיוק<small>בשידור חי במשחק 🔴</small>')")
        # 36.3–40.4 : מגיבים על הפוסט של היום, אוספים 200 מטבעות, ואתם בפנים
        scene("s9", 4.1, "R.top('יום 4','<b>23</b>/25 נוסעים')",
              V+"R.orbit(K,c.d*.45,c.h*1.5+2,c.h*.2,3.4,0.15);"
              "R.cap(K<1.4?'💬 מגיבים על <em>הפוסט של היום</em>':K<2.9?'💬 מגיבים על <em>הפוסט של היום</em><small>+ 🪙 אוספים 200 מטבעות</small>':'ואתם <em>בפנים!</em> 🎟️')")
        # 40.4–44.4 : ומה יקרה מחר? התגובה עם הכי הרבה לייקים קובעת
        scene("s10", 4.2, "R.hideTop()",
              V+"R.orbit(K,c.d*.9+K*1.5,c.h*2.4+4+K*.5,0,4.2,0.08);R.cap(K<1.4?'ומה יקרה <em>מחר</em>? 👀':'התגובה עם <em>הכי הרבה לייקים</em> קובעת 👇')")

        print("TOTAL images", frame[0], "ERREURS", errs[:5])
        b.close()

main()
