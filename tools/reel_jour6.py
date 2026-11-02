"""Reel « יום 6 » (2.11.2026) : capture du vrai jeu avec les VRAIS passagers (fichier JSON PAX), calée mot à mot sur la voix.
Usage : PAX=passagers.json python3 tools/reel_jour6.py <dossier_three3> <dossier_images>"""
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

        pg.evaluate("""mode='sea';started=true;setShip(shipIdx(totalN()));setEvent({type:'whale',title:''});
tv={day:'2026-11-02',handle:'dor_solomovich',text:'🦈 שיא הדיג של השבוע: כריש תינוק של 54 ק״ג!',likes:0};tvDraw();
CROWN_H='shahar_b.y';rebuild();
document.querySelector('#gate').hidden=true;R.hideTop();
window.FL=[];
window.mkLine=function(h){const p=byH.get(h);if(!p||!p.slot)return null;const g=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(),new THREE.Vector3()]);
  const l=new THREE.Line(g,new THREE.LineBasicMaterial({color:0xffffff}));l.frustumCulled=false;const b=new THREE.Mesh(new THREE.SphereGeometry(.12,8,6),new THREE.MeshLambertMaterial({color:0xFF3B30}));
  ship.group.add(l);ship.group.add(b);const o={h,l,b,p};FL.push(o);return o};
window.lineTick=function(t,lift){for(const o of FL){const s=o.p.slot,side=s.z>=0?1:-1,a=new THREE.Vector3(s.x+.15,s.y+1.15*figS,s.z+side*.3*figS);
  const by=(o.h===lift.h?lift.y:-.15+Math.sin(t*5+s.x)*.05);const b=new THREE.Vector3(s.x+.6,by,side*(ship.beam/2+2.2));
  o.l.geometry.setFromPoints([a,b]);o.b.position.copy(b);if(o.fish){o.fish.position.set(b.x,b.y-.9,b.z);o.fish.rotation.z=Math.sin(t*9)*.35}}};
window.mkShark=function(){const L=[];for(let k=0;k<6;k++){const s=1-Math.abs(k-1.5)/5;addBox(L,.45,.55*s+.15,.45*s+.12,0,-k*.42,0,'#6F7F8F')}
  addBox(L,.12,.35,.4,0,-.9,.25,'#5E6E7E');addBox(L,.1,.5,.1,0,.1,.0,'#5E6E7E');addBox(L,.5,.12,.5,0,-2.5,0,'#5E6E7E');addBox(L,.4,.06,.3,0,.18,.0,'#E8EEF3');
  const m=vmesh(L);m.scale.setScalar(Math.max(1,figS*1.6));return m};
['dor_solomovich','yardensolomovich','ilaybaryosef','avivi.nave'].forEach(mkLine);
{const d=FL.find(o=>o.h==='dor_solomovich');if(d){d.fish=mkShark();ship.group.add(d.fish);d.fish.visible=false}}
window.LIFT={h:'',y:-.15};
window.capHook=function(t){lineTick(t,LIFT)};""")
        V="const c=ship.view;"
        # 0–3.75 : לוויתן ענק… שוחה ממש ליד ספינת הדייגים
        scene("s1", 3.75, "tvGroup.visible=false;flash(1,.6)",
              "{const w=evProps.whale;const c=ship.view;if(w){const p=w.getWorldPosition(new THREE.Vector3());const a=Math.atan2(p.z,p.x)+.5;R.cam(p.x*.35+Math.cos(a)*c.d*.55,c.h*1.5+3,p.z*.35+Math.sin(a)*c.d*.55,p.x*.55,.4,p.z*.55)}else R.orbit(K,c.d*.8,c.h*2,0,1,.1)}"
              "R.cap(K<1.4?'🐋 <em>לוויתן ענק</em>!':'שוחה ממש ליד <em>ספינת הדייגים</em>')")
        # 3.75–7.2 : יום שישי על הסיפון, וכבר 43 נוסעים
        scene("s2", 7.2, "R.top('יום 6','<b>43</b>/100 נוסעים');flash(.5,.3)",
              V+"R.orbit(K,c.d*.7,c.h*1.6+3,c.h*.1,1.4,0.16);R.cap(K<1.45?'<em>יום 6</em> על הסיפון 🚢':'וכבר <em>43 נוסעים</em>!')")
        # 7.2–12.2 : ושחר זכתה אתמול באלף מטבעות… וגם הייתה המגיבה של היום
        scene("s3", 12.2, "R.hideTop();flash(.5,.3)",
              "{const p=byH.get('shahar_b.y');const w=worldOf(p,new THREE.Vector3());const a=.6+K*.08;R.cam(w.x+Math.cos(a)*6.5,w.y+3.6,w.z+Math.sin(a)*6.5,w.x,w.y+1.1,w.z)}"
              "R.cap(K<2.9?'<span dir=ltr>@shahar_b.y</span> זכתה ב־<em>1,000 מטבעות</em> 🪙':'וגם <em>המגיבה של היום</em> 👑')")
        # 12.2–14.9 : PAUSE studio TV « ועכשיו… החדשות של היום »
        scene("pause", 14.9, "tvGroup.visible=true;R.top('📺','חדשות הספינה');flash(.9,.4)",
              V+"{const k=Math.min(1,K/1.5),e=k*k*(3-2*k),p=tvGroup.position,S=tvGroup.userData.S;"
              "const ax=c.d*.4,ay=c.h*2+4,az=c.d*.8,bx=p.x+2.6*S,by=p.y+3.3*S,bz=p.z+12.5*S;"
              "R.cam(ax+(bx-ax)*e,ay+(by-ay)*e+Math.sin(e*Math.PI)*5,az+(bz-az)*e,(p.x+.9*S)*e,(p.y+2.3*S)*e,(p.z-1*S)*e)}"
              "R.cap(K<.6?'<span style=\"background:#E8262C;color:#fff;padding:6px 26px;border-radius:14px\">🔴 מבזק</span>':'ועכשיו… <em>חדשות הספינה</em> 📺')")
        # 14.9–20.2 : תחרות הדיג השתגעה! דור דג כריש תינוק של 54 קילו
        scene("s5", 20.2, "tvGroup.visible=false;R.top('🎣','תחרות הדיג');flash(.6,.3)",
              "{const d=FL.find(o=>o.h==='dor_solomovich');const p=d.p;const w=worldOf(p,new THREE.Vector3());const side=p.slot.z>=0?1:-1;"
              "if(K>2.1){d.fish.visible=true;LIFT.h='dor_solomovich';LIFT.y=Math.min(2.6,-.15+(K-2.1)*2.2)}"
              "R.cam(w.x+7,w.y+3.2,w.z+side*9.5,w.x+.4,w.y+.6,w.z+side*3)}"
              "R.cap(K<2.1?'🎣 תחרות הדיג <em>השתגעה!</em>':'<span dir=ltr>@dor_solomovich</span> דג <em>כריש תינוק</em><small>54 ק״ג! 🦈</small>')")
        # 20.2–24.3 : ירדן ועילאי צמודים אליו. מי ייקח את גביע הדייגים בשבת?
        scene("s6", 24.3, "flash(.4,.3)",
              V+"{const a=byH.get('yardensolomovich'),b=byH.get('ilaybaryosef');const wa=worldOf(a,new THREE.Vector3()),wb=worldOf(b,new THREE.Vector3());const m=wa.clone().add(wb).multiplyScalar(.5);"
              "const ang=.9+K*.1;R.cam(m.x+Math.cos(ang)*12,m.y+6,m.z+Math.sin(ang)*12,m.x,m.y+1,m.z)}"
              "R.cap(K<1.9?'<span dir=ltr>@yardensolomovich</span> ו־<span dir=ltr>@ilaybaryosef</span><small>צמודים אליו!</small>':'מי ייקח את <em>גביע הדייגים</em> בשבת? 🏆')")
        # 24.3–29.7 : והערב בשמונה: הגרלה על אלף מטבעות, והזוכה מחליט מה יקרה מחר
        scene("s7", 29.7, "LIFT.h='';R.top('🎟️','ההגרלה של הערב');flash(.6,.3)",
              V+"R.orbit(K,c.d*.8,c.h*2+4,c.h*.1,2.4,0.11);R.cap(K<3.15?'והערב ב־<em>20:00</em>: הגרלה על<small>🪙 1,000 מטבעות</small>':'והזוכה <em>מחליט/ה</em> מה יקרה מחר! ✨')")
        # 29.7–34.4 : ומה יקרה מחר? התגובה עם הכי הרבה לייקים קובעת
        scene("s8", 34.4, "R.hideTop();flash(.4,.3)",
              V+"R.orbit(K,c.d*.9+K*1.5,c.h*2.4+4+K*.5,0,4.0,0.08);R.cap(K<1.55?'ומה יקרה <em>מחר</em>? 👀':'התגובה עם <em>הכי הרבה לייקים</em> קובעת 👇')")

        print("TOTAL images", frame[0], "ERREURS", errs[:5])
        b.close()

main()
