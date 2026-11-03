"""Reel « יום 7 » (3.11.2026, 1er épisode du règlement du 03.11) : capture du vrai jeu avec les VRAIS passagers (fichier JSON PAX), calée mot à mot sur la voix.
Usage : PAX=passagers.json python3 tools/reel_jour7.py <dossier_three3> <dossier_images>"""
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
tv={day:'2026-11-03',handle:'amit_azulay23',text:'🦈 הכריש של עמית: 26.6 ק״ג! מוצג על המסך',likes:7};tvDraw();
CROWN_H='amit_azulay23';rebuild();
document.querySelector('#gate').hidden=true;R.hideTop();
window.RS=.59;window.SINKV=function(){ship.group.position.y-=ship.draft*RS*.9;ship.group.rotation.z+=-RS*.18};
window.FL=[];
window.mkLine=function(h){const p=byH.get(h);if(!p||!p.slot)return null;const g=new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(),new THREE.Vector3()]);
  const l=new THREE.Line(g,new THREE.LineBasicMaterial({color:0xffffff}));l.frustumCulled=false;const b=new THREE.Mesh(new THREE.SphereGeometry(.12,8,6),new THREE.MeshLambertMaterial({color:0xFF3B30}));
  ship.group.add(l);ship.group.add(b);const o={h,l,b,p};FL.push(o);return o};
window.lineTick=function(t,lift){for(const o of FL){const s=o.p.slot,side=s.z>=0?1:-1,a=new THREE.Vector3(s.x+.15,s.y+1.15*figS,s.z+side*.3*figS);
  const by=(o.h===lift.h?lift.y:-.15+Math.sin(t*5+s.x)*.05);const b=new THREE.Vector3(s.x+.6,by,side*(ship.beam/2+2.2));
  o.l.geometry.setFromPoints([a,b]);o.b.position.copy(b);if(o.fish){o.fish.position.set(b.x,b.y-.3,b.z);o.fish.rotation.z=Math.sin(t*9)*.35}}};
window.mkShark=function(){const L=[];for(let k=0;k<6;k++){const s=1-Math.abs(k-1.5)/5;addBox(L,.45,.55*s+.15,.45*s+.12,0,-k*.42,0,'#6F7F8F')}
  addBox(L,.12,.35,.4,0,-.9,.25,'#5E6E7E');addBox(L,.1,.5,.1,0,.1,.0,'#5E6E7E');addBox(L,.5,.12,.5,0,-2.5,0,'#5E6E7E');addBox(L,.4,.06,.3,0,.18,.0,'#E8EEF3');
  const m=vmesh(L);m.scale.setScalar(Math.max(1.4,figS*1.9));return m};
['ilaybaryosef','yardensolomovich','dor_solomovich'].forEach(mkLine);
{const d=FL.find(o=>o.h==='ilaybaryosef');if(d){d.fish=mkShark();ship.group.add(d.fish);d.fish.visible=false}}
window.LIFT={h:'',y:-.15};
window.capHook=function(t){lineTick(t,LIFT)};""")
        V="SINKV();const c=ship.view;"
        # 0–2.6 : המטרה שלנו: להטביע את הספינה!
        scene("s1", 2.6, "tvGroup.visible=false;flash(1,.6)",
              V+"R.orbit(K,c.d*.95-K*2,c.h*1.8+5-K,c.h*.1,0.5,0.22);R.cap(K<1.0?'המטרה שלנו:':'<em>להטביע</em> את הספינה! 🌊')")
        # 2.6–7.7 : אתמול 43 נוסעים… והיום? 59!
        scene("s2", 7.7, "R.top('יום 7','<b>59</b>/100 נוסעים');flash(.5,.3)",
              V+"R.orbit(K,c.d*.7,c.h*1.5+3,c.h*.1,1.3,0.15);R.cap(K<2.8?'אתמול <em>43 נוסעים</em>…':'והיום? <em>59</em>! 🚢')")
        # 7.7–10.0 : הספינה כבר 60% מתחת למים
        scene("s3", 10.0, "R.hideTop();flash(.6,.3)",
              V+"{const a=2.6+K*.12;R.cam(Math.cos(a)*c.d*.62,.9+K*.15,Math.sin(a)*c.d*.62,0,c.h*.15,0)}R.cap('הספינה כבר <em>60%</em> מתחת למים 😱')")
        # 10.0–14.8 : עברנו את ה־50 → 100 מטבעות לכולם
        scene("s4", 14.8, "R.top('🎉','בונוס לכולם');flash(.6,.3)",
              V+"R.orbit(K,c.d*.55,c.h*1.3+2.5,c.h*.2,3.4,0.14);R.cap(K<2.3?'עברנו את <em>ה־50</em>…':'כל הנוסעים קיבלו<small>🪙 100 מטבעות!</small>')")
        # 14.8–18.0 : PAUSE studio TV
        scene("pause", 18.0, "tvGroup.visible=true;R.top('📺','חדשות הספינה');flash(.9,.4)",
              V+"{const k=Math.min(1,K/1.5),e=k*k*(3-2*k),p=tvGroup.position,S=tvGroup.userData.S;"
              "const ax=c.d*.4,ay=c.h*2+4,az=c.d*.8,bx=p.x+2.6*S,by=p.y+3.3*S,bz=p.z+12.5*S;"
              "R.cam(ax+(bx-ax)*e,ay+(by-ay)*e+Math.sin(e*Math.PI)*5,az+(bz-az)*e,(p.x+.9*S)*e,(p.y+2.3*S)*e,(p.z-1*S)*e)}"
              "R.cap(K<.7?'<span style=\"background:#E8262C;color:#fff;padding:6px 26px;border-radius:14px\">🔴 מבזק</span>':'ועכשיו… <em>חדשות הספינה</em> 📺')")
        # 18.0–25.4 : התגובה של היום: עמית… הכריש שלו 26 ק״ג על המסך
        scene("s5", 25.4, "flash(.4,.3)",
              V+"{const p=tvGroup.position,S=tvGroup.userData.S;const a=K*.03;R.cam(p.x+(2.2+Math.sin(a)*2)*S,p.y+3.0*S,p.z+(9.5-K*.25)*S,p.x+.9*S,p.y+2.3*S,p.z-1*S)}"
              "R.cap(K<1.6?'💬 <em>התגובה של היום</em>':K<4.1?'<span dir=ltr>@amit_azulay23</span> ביקש<small>שהדג שלו יוצג על הסיפון</small>':'הכריש שלו, <em>26 ק״ג</em>, על המסך! 🦈')")
        # 25.4–29.3 : וטל הפכה לדי-ג'יי: מסיבת ריקודים על הסיפון
        scene("s6", 29.3, "tvGroup.visible=false;R.top('🎧','מסיבה על הסיפון');flash(.7,.3)",
              V+"{const p=byH.get('tal_neo_nitzan');if(p&&p.slot){const w=worldOf(p,new THREE.Vector3());const a=.7+K*.12;R.cam(w.x+Math.cos(a)*9,w.y+6.5,w.z+Math.sin(a)*9,w.x,w.y+1,w.z)}else R.orbit(K,c.d*.6,c.h*1.4+3,c.h*.2,4.2,0.15)}"
              "R.cap(K<1.9?'<span dir=ltr>@tal_neo_nitzan</span> הפכה ל־<em>DJ</em> 🎧':'<em>מסיבת ריקודים</em> על הסיפון! 🕺')")
        # 29.3–34.0 : ובתחרות הדיג? עילאי עם כריש של כמעט 60 ק״ג
        scene("s7", 34.0, "R.top('🎣','תחרות הדיג');flash(.6,.3);LIFT.h='ilaybaryosef';{const d=FL.find(o=>o.h==='ilaybaryosef');if(d&&d.fish)d.fish.visible=true}",
              V+"{const p=byH.get('ilaybaryosef');const w=worldOf(p,new THREE.Vector3());const side=p.slot.z>=0?1:-1;const a=(side>0?1.2:-1.2)+K*.05;"
              "LIFT.y=-.15+Math.max(0,K-1.8)*1.6;R.cam(w.x+Math.cos(a)*9,w.y+6,w.z+Math.sin(a)*9,w.x,w.y+.6,w.z+side*2)}"
              "R.cap(K<2.0?'🎣 ובתחרות <em>הדיג</em>?':'<span dir=ltr>@ilaybaryosef</span> עם כריש של<small>כמעט 60 ק״ג! 🦈</small>')")
        # 34.0–38.6 : מה יקרה בפרק הבא? התגובה עם הכי הרבה לייקים קובעת
        scene("s8", 38.6, "LIFT.h='';R.hideTop();flash(.4,.3)",
              V+"R.orbit(K,c.d*.85+K*1.5,c.h*2.2+4+K*.5,0,4.6,0.08);R.cap(K<1.9?'מה יקרה <em>בפרק הבא</em>? 👀':'התגובה עם <em>הכי הרבה לייקים</em> קובעת 👇')")

        print("TOTAL images", frame[0], "ERREURS", errs[:5])
        b.close()

main()
