"""Reel 10.11 « שודדי ים » – événement des 100 abonnés : pirates, canons, voie d'eau, l'enveloppe ; CTA « תייגו את החבר שהייתם לוקחים איתכם לסירת ההצלה ». Voix Juniper eleven_v4 (26,7 s), découpage mot à mot.
Usage : PAX=passagers.json python3 tools/reel_pirates.py <dossier_three3> <dossier_images>"""

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

        pg.evaluate("""mode='sea';started=true;setShip(1);setEvent({type:'storm',title:''});
tvGroup.visible=false;CROWN_H='';rebuild();
document.querySelector('#gate').hidden=true;R.hideTop();
window.LS=ship.view.d;window.SNK=0;
window.mkEnv=function(s){const g=new THREE.Group();const p=new THREE.Mesh(new THREE.BoxGeometry(1.6,.06,1.05),new THREE.MeshLambertMaterial({color:0xF3E6C8}));g.add(p);
  const f=new THREE.Mesh(new THREE.BoxGeometry(1.15,.065,.08),new THREE.MeshLambertMaterial({color:0xDCCBA5}));f.position.set(0,.01,-.18);f.rotation.y=.6;g.add(f);const f2=f.clone();f2.rotation.y=-.6;g.add(f2);
  const seal=new THREE.Mesh(new THREE.CylinderGeometry(.16,.16,.08,16),new THREE.MeshLambertMaterial({color:0xB3121B,emissive:0x330000}));seal.position.set(0,.05,0);g.add(seal);g.scale.setScalar(s);return g};
// bateau pirate en voxels
{const L=[];addBox(L,10,1.4,3.6,0,0,0,'#3B2414');addBox(L,10.4,.35,3.9,0,.75,0,'#5A3820');addBox(L,2.4,1.6,3.6,-4.2,1.4,0,'#4A2E18');addBox(L,1.2,.9,2.4,5.2,.4,0,'#3B2414');
 addBox(L,.4,8,.4,0,4.6,0,'#2A1A0E');addBox(L,.3,6,.3,-3,4,0,'#2A1A0E');
 addBox(L,.2,4.2,4.4,0,5.4,0,'#151515');addBox(L,.2,3.2,3.4,-3,4.6,0,'#151515');
 addBox(L,.25,1.1,1.1,.12,6,0,'#EDEDED');addBox(L,.25,.3,.3,.18,6.15,.25,'#151515');addBox(L,.25,.3,.3,.18,6.15,-.25,'#151515');addBox(L,.25,.2,.9,.12,5.3,0,'#EDEDED');
 addBox(L,.2,.7,1.2,0,8.9,.6,'#151515');
 for(const x of [-2.5,0,2.5]){addBox(L,.9,.55,.55,x,.55,2.05,'#111111')}
 window.PIR=vmesh(L);PIR.scale.setScalar(ship.len/9);evRoot.add(PIR);}
window.BALLS=[];for(let i=0;i<3;i++){const b=new THREE.Mesh(new THREE.SphereGeometry(.45,10,8),new THREE.MeshBasicMaterial({color:0x222222}));b.scale.setScalar(ship.len/14);b.visible=false;evRoot.add(b);BALLS.push(b)}
window.FIRE=[];for(let i=0;i<3;i++){const f=new THREE.Mesh(new THREE.SphereGeometry(.9,10,8),new THREE.MeshBasicMaterial({color:0xFFA020,transparent:true,opacity:.9}));f.scale.setScalar(ship.len/14);f.visible=false;evRoot.add(f);FIRE.push(f)}
window.ENV=mkEnv(2.2);evRoot.add(ENV);ENV.visible=false;
window.PIRPOS=function(k){const z=-(ship.beam/2+ship.len*.6);PIR.position.set(lerp(ship.len*2.2,ship.len*.15,Math.min(1,k)),-.2+Math.sin(k*5)*.15,z);PIR.rotation.set(0,0,Math.sin(k*3)*.05)};
window.SHOT=function(u){const z0=-(ship.beam/2+ship.len*.6);BALLS.forEach((b,i)=>{const v=u-i*.18;b.visible=v>0&&v<1;FIRE[i].visible=v>0&&v<.25;if(v>0){const x0=PIR.position.x+(i-1)*2.5*PIR.scale.x,x1=(i-1)*ship.len*.18;b.position.set(lerp(x0,x1,Math.min(1,v)),Math.sin(Math.min(1,v)*Math.PI)*3+1.2,lerp(z0+2*PIR.scale.x,-ship.beam/2,Math.min(1,v)));FIRE[i].position.set(x0,1.2,z0+2.4*PIR.scale.x);FIRE[i].material.opacity=Math.max(0,.9-v*3.5)}})};
window.POST=function(){ship.group.position.y-=ship.draft*SNK;ship.group.rotation.z+=-SNK*.35;ship.group.rotation.x+=SNK*.08};
{const _ff=flyFrame;window.flyFrame=function(dt){_ff(dt);try{POST()}catch(e){}}}
PIR.visible=false;window.capHook=function(t){};""")
        if os.environ.get("NOTEXT"): pg.add_style_tag(content="#cap,#reelTop{display:none!important}")
        V="const c=ship.view;"
        PV="{const p=PIR.position;R.cam(p.x+ZX*ship.len,p.y+ship.len*.32,p.z+ship.len*ZZ,p.x,p.y+ship.len*.15,p.z)}"
        # 0–3.5 : 100 עוקבים… ושודדי ים תקפו את הספינה!
        scene("s1", 3.5, "PIR.visible=true;PIRPOS(.75);flash(1,.5);R.top('🏴‍☠️','<b>100</b> עוקבים!')",
              V+"PIRPOS(.75+K*.02);const ZX=.55-K*.08,ZZ=-1.9+K*.18;"+PV+"R.cap(K<1.15?'<em>100</em> עוקבים… 🎉':'🏴‍☠️ שודדי ים <em>תקפו</em><small>את הספינה!</small>')")
        # 3.5–8.7 : בטובעים ביחד כל עוקב חדש עולה על הספינה, המטרה: להטביע אותה
        scene("s2", 8.7, "PIR.visible=false;R.top('🚢','טובעים ביחד');flash(.5,.3)",
              V+"R.orbit(K,c.d*.85-K*.8,c.h*1.6+4,c.h*.1,0.7,0.14);R.cap(K<2.9?'כל עוקב חדש<small>= עוד נוסע על הספינה 🧍</small>':'המטרה שלנו:<small>להטביע אותה! 🌊</small>')")
        # 8.7–11.76 : עברנו את ה־100 → אירוע ענק
        scene("s3", 11.76, "R.top('🎉','<b>106</b> עוקבים');flash(.7,.4)",
              V+"R.orbit(K,c.d*.6,c.h*1.2+2,c.h*.3,2.2,0.2);R.cap(K<1.1?'עברנו את ה־<em>100</em>! 🎉':'הבטחנו <em>אירוע ענק</em>…')")
        # 11.76–16.48 : ספינת פיראטים מופיעה, התותחים יורים (15.12)
        scene("s4", 16.48, "PIR.visible=true;R.top('🌙','באמצע הלילה');flash(.4,.4)",
              V+"PIRPOS(K/3.4);SHOT((K-3.3)/1.0);R.orbit(K,c.d*.85,c.h*1.5+3,c.h*.1,1.3,0.05);R.cap(K<1.8?'🌙 באמצע הלילה…':K<2.7?'🏴‍☠️ ספינת <em>פיראטים</em>!':K<3.36?'והתותחים…':'💥 פתחו <em>באש</em>!');if(K>3.3&&K<3.4)flash(1,.3);if(K>3.75&&K<3.85)flash(.8,.3)")
        # 16.48–19.33 : חור בצד, המים נכנסים
        scene("s5", 19.33, "R.top('🕳️','חור בצד!');flash(.9,.4)",
              V+"PIRPOS(1);SHOT(-1);SNK=Math.min(.55,K*.2);R.orbit(K,c.d*.55,c.h*.9+1,c.h*.1,0.3,0.1);R.cap(K<1.3?'🕳️ חור בצד…':'💧 המים <em>נכנסים</em>…')")
        # 19.33–23.68 : מה הפיראטים מחפשים? את המעטפה שהלוויתן הביא
        scene("s6", 23.68, "R.top('✉️','?');flash(.6,.3);ENV.visible=true",
              V+"PIRPOS(1);SNK=.55;{const q=new THREE.Vector3(PIR.position.x*.5,2.5+Math.sin(K*2)*.3,-(ship.beam/2+ship.len*.25));ENV.position.copy(q);ENV.rotation.set(.3,K*.8,.15);R.cam(q.x+ship.len*.12*Math.cos(K*.3),q.y+ship.len*.08,q.z-ship.len*.22,q.x,q.y,q.z)}R.cap(K<2.1?'מה הפיראטים <em>מחפשים</em>? 🏴‍☠️':'✉️ את <em>המעטפה</em><small>שהלוויתן הביא</small>')")
        # 23.68–27.6 : CTA
        scene("s7", 27.6, "ENV.visible=false;R.top('🛟','סירת ההצלה');flash(.7,.3)",
              V+"PIRPOS(1);SNK=.55+K*.03;R.orbit(K,c.d*.95+K*1.2,c.h*1.8+4,0,3.9,0.07);R.cap('🏷️ תייגו את <em>החבר</em><small>שהייתם לוקחים איתכם לסירת ההצלה! 🛟</small>')")

        print("TOTAL images", frame[0], "ERREURS", errs[:5])
        b.close()

main()
