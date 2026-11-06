"""Reel CROSSOVER « L'enveloppe » (07.11.2026, 19:00) – partie 3D (0–32 s) ; la fin commune (24,9–32 s) est superposée par tools/crossover_fin.py : capture du vrai jeu avec les VRAIS passagers (fichier JSON PAX), calée mot à mot sur la voix.
Usage : PAX=passagers.json python3 tools/reel_crossover.py <dossier_three3> <dossier_images>"""
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
tv={day:'2026-11-07',handle:'ilaybaryosef',text:'⚔️ הדו־קרב: עילאי 2 · איתן 1 (הצבעות) · ☄️ מטאוריט ליד הספינה!',likes:0};tvDraw();
CROWN_H='';rebuild();
document.querySelector('#gate').hidden=true;R.hideTop();
window.LS=ship.view.d;window.RS=.70;window.SINKV=function(){ship.group.position.y-=ship.draft*RS*.9;ship.group.rotation.z+=-RS*.2};
window.mkEnv=function(s){const g=new THREE.Group();const p=new THREE.Mesh(new THREE.BoxGeometry(1.6,.06,1.05),new THREE.MeshLambertMaterial({color:0xF3E6C8}));g.add(p);
  const f=new THREE.Mesh(new THREE.BoxGeometry(1.15,.065,.08),new THREE.MeshLambertMaterial({color:0xDCCBA5}));f.position.set(0,.01,-.18);f.rotation.y=.6;g.add(f);const f2=f.clone();f2.rotation.y=-.6;g.add(f2);
  const seal=new THREE.Mesh(new THREE.CylinderGeometry(.16,.16,.08,16),new THREE.MeshLambertMaterial({color:0xB3121B,emissive:0x330000}));seal.position.set(0,.05,0);g.add(seal);g.scale.setScalar(s);return g};
window.ENV0=mkEnv(1.5);evRoot.add(ENV0);
window.ENVW=mkEnv(1.7);if(evProps.whale){evProps.whale.add(ENVW);ENVW.position.set(-1.7,-.2,0);ENVW.rotation.set(0,0,-.35)}
window.DIV=[];for(let i=0;i<4;i++){const L=[];addBox(L,.5,.5,.5,0,0,0,'#163A5F');addBox(L,.36,.18,.06,0,.08,.27,'#FFD23F');addBox(L,.2,.2,.7,0,-.1,-.5,'#0E2740');const m=vmesh(L);m.scale.setScalar((evProps.whale?evProps.whale.scale.x:1)*2.2);evRoot.add(m);DIV.push(m)}
window.WHPOS=function(K,mode){const w=evProps.whale;if(!w)return;const sc=w.scale.x,z=ship.beam/2+6*sc;w.visible=true;
  if(mode==='jump'){const u=Math.min(1,K/4.6),x=lerp(-LS*.35,LS*.15,u);w.position.set(x,Math.sin(u*Math.PI)*6*sc-1.2*sc,z);w.rotation.z=Math.cos(u*Math.PI)*.6}
  else{w.position.set(LS*.15,-.6*sc+Math.sin(K*2)*.3*sc,z);w.rotation.z=-.15}};
window.DIVPOS=function(K){const w=evProps.whale;if(!w)return;const z=w.position.z;DIV.forEach((d,i)=>{const a=i*1.57,r=lerp(LS*.45,4*w.scale.x,Math.min(1,K/3.8));d.visible=true;d.position.set(w.position.x+Math.cos(a)*r,-.3+Math.sin(K*6+i)*.15,z+Math.sin(a)*r*.6+3);d.lookAt(w.position.x,-.3,z)})};
window.WST=null;window.POST=function(){SINKV();if(WST){WHPOS(WST.k,WST.mode);if(WST.div!=null)DIVPOS(WST.div);else DIV.forEach(d=>d.visible=false)}};
{const _ff=flyFrame;window.flyFrame=function(dt){_ff(dt);try{POST()}catch(e){}}}
window.capHook=function(t){};""")
        V="const c=ship.view;"
        TVC=("{const p=tvGroup.position,S=tvGroup.userData.S;const k=Math.min(1,K/1.2),e=k*k*(3-2*k);R.cam(p.x+(2.6-e*.4)*S,p.y+(3.3-e*.3)*S,p.z+(12.5-e*2.5)*S,p.x+.9*S,p.y+2.3*S,p.z-1*S)}")
        WH="{const w=evProps.whale;const p=w.getWorldPosition(new THREE.Vector3());const a=1.25+K*.04;const D=Math.max(c.d*.55,22*w.scale.x/1.5)*ZM;R.cam(p.x+Math.cos(a)*D,p.y+5+D*.18,p.z+Math.sin(a)*D,p.x,p.y+1,p.z)}"
        # 0–2.0 : המכתב הגיע גם אלינו… (gros plan sur l'enveloppe)
        scene("s1", 2.0, "tvGroup.visible=false;flash(1,.6)",
              V+"R.orbit(K,c.d*.7,c.h*1.6+3,c.h*.2,1.0,0.08);{const dir=new THREE.Vector3();camera.getWorldDirection(dir);const q=camera.position.clone().add(dir.multiplyScalar(5.5-K*.6));q.y+=.5;ENV0.position.copy(q);ENV0.lookAt(camera.position);ENV0.rotateX(Math.PI/2+.25);ENV0.rotateY(Math.sin(K*2)*.25)}"+"R.cap('המכתב הגיע <em>גם אלינו</em>… ✉️')")
        # 2.0–9.8 : מאז הפרק הקודם עלו עוד 3… 69! עוד 31 והספינה טובעת
        scene("s2", 9.8, "ENV0.visible=false;R.top('✉️','<b>69</b>/100 נוסעים');flash(.5,.3)",
              V+"WST=null;R.orbit(K,c.d*.8-K*.6,c.h*1.6+4,c.h*.1,0.7,0.12);R.cap(K<3.3?'מאז הפרק הקודם…<small>עוד 3 נוסעים עלו 🚢</small>':K<5.0?'<em>69</em> נוסעים!':'עוד <em>31</em> והספינה <em>טובעת</em>! 😱')")
        # 9.8–16.1 : חדשות הספינה: עילאי מוביל בדו־קרב, מטאוריט…
        scene("s3", 16.1, "R.top('📺','חדשות הספינה');tvGroup.visible=true;flash(.8,.4)",
              V+"WST=null;"+TVC+"R.cap(K<1.8?'📺 <em>חדשות הספינה</em>':K<3.15?'⚔️ <span dir=ltr>@ilaybaryosef</span> מוביל<small>בדו־קרב</small>':'☄️ מטאוריט נפל ליד הספינה<small>בזכות <span dir=ltr>@ido.benbasat</span></small>')")
        # 16.1–20.8 : ופתאום… הלוויתן קפץ מהמים, עם מעטפה בפה!
        scene("s4", 20.8, "tvGroup.visible=false;R.top('🐋','הלוויתן');flash(1,.4)",
              V+"WST={k:K,mode:'jump',div:null};const ZM=1-K*.03;"+WH+"R.cap(K<1.6?'ופתאום… 😱':K<3.4?'ה<em>לוויתן</em> קפץ מהמים!':'עם <em>מעטפה</em> בפה! ✉️🐋')")
        # 20.8–24.9 : והצוללנים שוחים אליו כדי לגנוב אותה
        scene("s5", 24.9, "R.top('🤿','הצוללנים');flash(.6,.3)",
              V+"WST={k:K,mode:'float',div:K};const ZM=.8-K*.03;"+WH+"R.cap(K<1.3?'🤿 <em>הצוללנים</em>…':'שוחים אליו כדי <em>לגנוב</em> אותה!')")
        # 24.9–32.0 : fond pour la fin commune (superposée ensuite)
        scene("s6", 32.0, "R.hideTop();R.cap('');document.querySelector('#cap').style.opacity=0",
              V+"WST={k:K+4,mode:'float',div:4};R.orbit(K,c.d*.95+K*1.2,c.h*2.2+5,0,4.2,0.06)")

        print("TOTAL images", frame[0], "ERREURS", errs[:5])
        b.close()

main()
