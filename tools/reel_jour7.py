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
window.LIFT={h:'',y:-.15};
window.capHook=function(t){lineTick(t,LIFT)};""")
        V="SINKV();const c=ship.view;"
        TV=("{const k=Math.min(1,K/1.5),e=k*k*(3-2*k),p=tvGroup.position,S=tvGroup.userData.S;"
            "const ax=c.d*.4,ay=c.h*2+4,az=c.d*.8,bx=p.x+2.6*S,by=p.y+3.3*S,bz=p.z+12.5*S;"
            "R.cam(ax+(bx-ax)*e,ay+(by-ay)*e+Math.sin(e*Math.PI)*5,az+(bz-az)*e,(p.x+.9*S)*e,(p.y+2.3*S)*e,(p.z-1*S)*e)}")
        WH="{const w=evProps.whale;if(w){const p=w.getWorldPosition(new THREE.Vector3());const m=p.clone().multiplyScalar(.5);const a=Math.atan2(p.z,p.x)+Math.PI/2+.35+K*.05;const D=Math.max(c.d*1.0,p.length()*1.15)*ZM;R.cam(m.x+Math.cos(a)*D+SH,c.h*1.6+4+SH,m.z+Math.sin(a)*D,m.x,.5,m.z)}else R.orbit(K,c.d*.8,c.h*1.6+3,0,1,.1)}"
        # 0–4.6 : כל עוקב חדש עולה לספינה… והמטרה שלנו: להטביע אותה
        scene("s1", 4.6, "tvGroup.visible=false;flash(1,.6)",
              V+"R.orbit(K,c.d*.95-K*1.5,c.h*1.8+5-K*.6,c.h*.1,0.5,0.18);R.cap(K<2.2?'כל עוקב חדש = <em>נוסע</em> 🚢':'המטרה: <em>להטביע</em> את הספינה! 🌊')")
        # 4.6–9.3 : אתמול 43… והיום 61
        scene("s2", 9.3, "R.top('יום 7','<b>61</b>/100 נוסעים');flash(.5,.3)",
              V+"R.orbit(K,c.d*.7,c.h*1.5+3,c.h*.1,1.3,0.15);R.cap(K<2.6?'אתמול <em>43 נוסעים</em>…':'והיום? <em>61</em>! 🚀')")
        # 9.3–14.0 : 60% מתחת למים… והמים ממשיכים לעלות
        scene("s3", 14.0, "R.hideTop();flash(.6,.3)",
              "RS=.59+K*.012;"+V+"{const a=2.6+K*.1;R.cam(Math.cos(a)*c.d*.62,.9+K*.12,Math.sin(a)*c.d*.62,0,c.h*.15,0)}R.cap(K<2.9?'הספינה כבר <em>60%</em> מתחת למים 😱':'והמים <em>ממשיכים לעלות</em>… 🌊')")
        # 14.0–20.3 : עברנו את 50 וגם 60 → פעמיים 100 מטבעות
        scene("s4", 20.3, "RS=.645;R.top('🎉','בונוס לכולם');flash(.6,.3)",
              V+"R.orbit(K,c.d*.55,c.h*1.3+2.5,c.h*.2,3.4,0.12);R.cap(K<3.3?'עברנו את <em>ה־50</em> וגם את <em>ה־60</em>!':'כל נוסע קיבל<small>🪙 2 × 100 מטבעות!</small>')")
        # 20.3–22.8 : ועכשיו… חדשות הספינה
        scene("pause", 22.8, "tvGroup.visible=true;R.top('📺','חדשות הספינה');flash(.9,.4)",
              V+TV+"R.cap(K<.6?'<span style=\"background:#E8262C;color:#fff;padding:6px 26px;border-radius:14px\">🔴 מבזק</span>':'ועכשיו… <em>חדשות הספינה</em> 📺')")
        # 22.8–30.6 : התגובה עם הכי הרבה לייקים: עמית… הכריש 26 ק״ג על המסך
        scene("s5", 30.6, "flash(.4,.3)",
              V+"{const p=tvGroup.position,S=tvGroup.userData.S;R.cam(p.x+(2.4-K*.12)*S,p.y+3.0*S,p.z+(10.5-K*.3)*S,p.x+.9*S,p.y+2.3*S,p.z-1*S)}"
              "R.cap(K<2.1?'💬 התגובה עם <em>הכי הרבה לייקים</em>':K<4.5?'<span dir=ltr>@amit_azulay23</span> ביקש<small>לראות את הדג שתפס</small>':'הכריש שלו, <em>26 ק״ג</em>, על המסך! 🦈')")
        # 30.6–34.6 : וטל הפכה לדי-ג'יי. כל הספינה רוקדת
        scene("s6", 34.6, "tvGroup.visible=false;R.top('🎧','מסיבה על הסיפון');flash(.7,.3)",
              V+"{const p=byH.get('tal_neo_nitzan');if(p&&p.slot){const w=worldOf(p,new THREE.Vector3());const a=.7+K*.14;R.cam(w.x+Math.cos(a)*9,w.y+6.5,w.z+Math.sin(a)*9,w.x,w.y+1,w.z)}else R.orbit(K,c.d*.6,c.h*1.4+3,c.h*.2,4.2,0.15)}"
              "R.cap(K<1.9?'<span dir=ltr>@tal_neo_nitzan</span> הפכה ל־<em>DJ</em> 🎧':'כל הספינה <em>רוקדת</em>! 🕺')")
        # 34.6–39.9 : בהגרלה של אתמול אף אחד לא נכנס. 1000 מטבעות נשארו בקופה
        scene("s7", 39.9, "R.top('🎟️','ההגרלה');flash(.6,.3)",
              V+"R.orbit(K,c.d*.8-K*.8,c.h*2+4,c.h*.1,2.4,0.1);R.cap(K<3.3?'בהגרלה של אתמול…<small><em>אף אחד</em> לא נכנס 😮</small>':'<em>1,000 מטבעות</em><small>נשארו בקופה 🪙</small>')")
        # 39.9–44.8 : רק שאף אחד לא שם לב… שהלוויתן עדיין מסתובב מתחת לספינה
        scene("s8", 44.8, "R.hideTop();setEvent({type:'whale',title:''});flash(.5,.5)",
              "const ZM=1-K*.04,SH=0;"+V+WH+"R.cap(K<1.9?'רק שאף אחד <em>לא שם לב</em>…':'ה<em>לוויתן</em> עדיין מסתובב<small>מתחת לספינה 🐋</small>')")
        # 44.8–47.8 : ואוראל אומר שהוא הולך לחצות אותה לשניים!
        scene("s9", 47.8, "flash(1,.4)",
              "const ZM=.75,SH=Math.sin(K*40)*.25;"+V+WH+"R.cap('<span dir=ltr>@1orel_bar_on7</span> אומר שהוא<small>יחצה אותה <em>לשניים</em>! 😱</small>')")
        # 47.8–52.2 : מה יקרה בפרק הבא? התגובה עם הכי הרבה לייקים קובעת
        scene("s10", 52.2, "flash(.4,.3)",
              V+"R.orbit(K,c.d*.85+K*1.5,c.h*2.2+4+K*.5,0,4.6,0.08);R.cap(K<1.5?'מה יקרה <em>בפרק הבא</em>? 👀':'התגובה עם <em>הכי הרבה לייקים</em> קובעת 👇')")

        print("TOTAL images", frame[0], "ERREURS", errs[:5])
        b.close()

main()
