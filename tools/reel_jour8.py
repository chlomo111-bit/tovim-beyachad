"""Reel « יום 8 » (5.11.2026 : tempête, cannes d'Amit, coffre, duel Ilay/Eitan) : capture du vrai jeu avec les VRAIS passagers (fichier JSON PAX), calée mot à mot sur la voix.
Usage : PAX=passagers.json python3 tools/reel_jour8.py <dossier_three3> <dossier_images>"""
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

        pg.evaluate("""mode='sea';started=true;setShip(shipIdx(totalN()));setEvent({type:'storm',title:''});
tv={day:'2026-11-05',handle:'amit_azulay23',text:'🎣 חכות שקונים במטבעות – ככל שהחכה יקרה יותר, הדגים גדולים יותר!',likes:0};tvDraw();
CROWN_H='amit_azulay23';rebuild();
document.querySelector('#gate').hidden=true;R.hideTop();
window.RS=.66;window.SINKV=function(){ship.group.position.y-=ship.draft*RS*.9;ship.group.rotation.z+=-RS*.2};
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
['ilaybaryosef','eitan_nouriel10','amit_azulay23','yardensolomovich'].forEach(mkLine);
{const d=FL.find(o=>o.h==='ilaybaryosef');if(d){d.fish=mkShark();ship.group.add(d.fish);d.fish.visible=false}}
window.LIFT={h:'',y:-.15};
window.capHook=function(t){lineTick(t,LIFT)};
try{placeChest();chest.visible=true}catch(e){}""")
        V="SINKV();const c=ship.view;"
        TV=("{const k=Math.min(1,K/1.5),e=k*k*(3-2*k),p=tvGroup.position,S=tvGroup.userData.S;"
            "const ax=c.d*.4,ay=c.h*2+4,az=c.d*.8,bx=p.x+2.6*S,by=p.y+3.3*S,bz=p.z+12.5*S;"
            "R.cam(ax+(bx-ax)*e,ay+(by-ay)*e+Math.sin(e*Math.PI)*5,az+(bz-az)*e,(p.x+.9*S)*e,(p.y+2.3*S)*e,(p.z-1*S)*e)}")
        FIG=lambda h,d=8.5,hh=6.5: ("{const p=byH.get('"+h+"');if(p&&p.slot){const w=worldOf(p,new THREE.Vector3());const side=p.slot.z>=0?1:-1;const a=(side>0?1.2:-1.2)+K*.05;"
                                    "R.cam(w.x+Math.cos(a)*"+str(d)+",w.y+"+str(hh)+",w.z+Math.sin(a)*"+str(d)+",w.x,w.y+.6,w.z+side*1.5)}else R.orbit(K,c.d*.6,c.h*1.4+3,c.h*.2,2,0.1)}")
        # 0–4.0 : סערה! הספינה נוטה… והמים נכנסים לסיפון!
        scene("s1", 4.0, "tvGroup.visible=false;flash(1,.6)",
              V+"{const a=2.4+K*.08,sh=Math.sin(K*23)*.25;R.cam(Math.cos(a)*c.d*.6+sh,1.2+sh,Math.sin(a)*c.d*.6,0,c.h*.2,0)}R.cap(K<2.2?'🌪️ <em>סערה!</em> הספינה נוטה…':'והמים <em>נכנסים לסיפון</em>! 🌊')")
        # 4.0–8.9 : כל עוקב חדש עולה לספינה, והמטרה: להטביע אותה
        scene("s2", 8.9, "flash(.5,.3)",
              V+"R.orbit(K,c.d*.9-K*1.2,c.h*1.7+4,c.h*.1,0.6,0.16);R.cap(K<2.2?'כל עוקב חדש = <em>נוסע</em> 🚢':'המטרה: <em>להטביע</em> אותה!')")
        # 8.9–16.3 : אתמול 64… היום 65… עוד 35 והספינה טובעת
        scene("s3", 16.3, "R.top('יום 8','<b>65</b>/100 נוסעים');flash(.5,.3)",
              "RS=.66+K*.008;"+V+"R.orbit(K,c.d*.7,c.h*1.5+3,c.h*.1,1.4,0.12);R.cap(K<2.75?'אתמול <em>64</em> נוסעים…':K<4.65?'והיום <em>65</em> 🚢':'עוד <em>35</em> והספינה <em>טובעת</em>! 😱')")
        # 16.3–19.0 : ועכשיו… חדשות הספינה
        scene("pause", 19.0, "RS=.72;R.top('📺','חדשות הספינה');tvGroup.visible=true;flash(.9,.4)",
              V+TV+"R.cap(K<.6?'<span style=\"background:#E8262C;color:#fff;padding:6px 26px;border-radius:14px\">🔴 מבזק</span>':'ועכשיו… <em>חדשות הספינה</em> 📺')")
        # 19.0–28.2 : עמית ביקש חכות… וזה קרה! חנות החכות פתוחה…
        scene("s4", 28.2, "flash(.4,.3)",
              V+"if(K<4.6){const p=tvGroup.position,S=tvGroup.userData.S;R.cam(p.x+(2.4-K*.12)*S,p.y+3.0*S,p.z+(10.5-K*.3)*S,p.x+.9*S,p.y+2.3*S,p.z-1*S)}else{tvGroup.visible=false;"+FIG('amit_azulay23',7.5,5.5)+"}"
              "R.cap(K<3.4?'<span dir=ltr>@amit_azulay23</span> ביקש<small>חכות שקונים במטבעות 🪙</small>':K<4.6?'וזה <em>קרה!</em> ✅':K<6.0?'🎣 <em>חנות החכות</em> פתוחה!':'חכה יקרה יותר =<small>דגים גדולים יותר 🦈</small>')")
        # 28.2–33.1 : ויש גם תיבת אוצר, שמסתתרת כל יום במקום אחר
        scene("s5", 33.1, "tvGroup.visible=false;R.top('🧰','תיבת האוצר');flash(.6,.3);try{chest.visible=true;chest.scale.multiplyScalar(2.2)}catch(e){}",
              V+"{if(chest){const w=chest.getWorldPosition(new THREE.Vector3());const a=.5+K*.2,d=11-K*.7;R.cam(w.x+Math.cos(a)*d,w.y+7-K*.5,w.z+Math.sin(a)*d,w.x,w.y+.6,w.z)}}"
              "R.cap(K<2.5?'ויש גם <em>תיבת אוצר</em> 🧰':'כל יום <em>במקום אחר</em><small>+200 מטבעות 🪙</small>')")
        # 33.1–41.6 : למה אתמול אף אחד לא זכה? צריך להגיב + 100 מטבעות באותו יום
        scene("s6", 41.6, "R.top('🎟️','ההגרלה');flash(.6,.3)",
              V+"R.orbit(K,c.d*.8-K*.5,c.h*2+4,c.h*.1,2.6,0.09);R.cap(K<2.4?'למה אתמול <em>אף אחד</em> לא זכה? 🤔':K<5.2?'צריך שני דברים:<small>1️⃣ 💬 להגיב</small>':'2️⃣ לאסוף <em>100 מטבעות</em> 🪙<small>במשחק, באותו יום!</small>')")
        # 41.6–48.8 : דו־קרב! עילאי 59 ק״ג… ואיתן חצי קילו מאחוריו
        scene("s7", 48.8, "R.top('⚔️','דו־קרב');flash(1,.4);LIFT.h='ilaybaryosef';{const d=FL.find(o=>o.h==='ilaybaryosef');if(d&&d.fish)d.fish.visible=true}",
              V+"LIFT.y=-.15+Math.max(0,K-2.6)*1.4;if(K<2.6)R.orbit(K,c.d*.6,c.h*1.6+3,c.h*.2,3.6,0.2);else if(K<5.2){"+FIG('ilaybaryosef')+"}else{"+FIG('eitan_nouriel10')+"}"
              "R.cap(K<2.6?'⚔️ <em>דו־קרב!</em>':K<5.2?'<span dir=ltr>@ilaybaryosef</span><small>🦈 59.3 ק״ג</small>':'<span dir=ltr>@eitan_nouriel10</span><small>רק חצי קילו מאחוריו! 😱</small>')")
        # 48.8–54.6 : מי ייקח את גביע הדייגים? כתבו 1 לעילאי, 2 לאיתן
        scene("s8", 54.6, "R.top('🏆','גביע הדייגים');flash(.5,.3)",
              V+"{const a=byH.get('ilaybaryosef'),b=byH.get('eitan_nouriel10');if(a&&b&&a.slot&&b.slot){const wa=worldOf(a,new THREE.Vector3()),wb=worldOf(b,new THREE.Vector3());const m=wa.clone().add(wb).multiplyScalar(.5);"
              "const D=Math.max(10,wa.distanceTo(wb)*.9),ang=.9+K*.08;R.cam(m.x+Math.cos(ang)*D,m.y+D*.55,m.z+Math.sin(ang)*D,m.x,m.y+1,m.z)}else R.orbit(K,c.d*.7,c.h*1.6+3,0,3,.1)}"
              "R.cap(K<2.7?'מי ייקח את <em>גביע הדייגים</em>? 🏆':'כתבו <em>1</em> = עילאי · <em>2</em> = איתן 👇')")
        # 54.6–59.6 : ותייגו חבר שיבחר איתכם… לפני שהסערה תטביע את כולם
        scene("s9", 59.6, "LIFT.h='';R.hideTop();flash(.4,.3)",
              "RS=.72+K*.03;"+V+"R.orbit(K,c.d*.85+K*1.5,c.h*2.2+4+K*.5,0,4.6,0.08);R.cap(K<2.2?'תייגו <em>חבר</em> שיבחר איתכם 📲':'לפני שהסערה <em>תטביע את כולם</em>… 🌪️')")

        print("TOTAL images", frame[0], "ERREURS", errs[:5])
        b.close()

main()
