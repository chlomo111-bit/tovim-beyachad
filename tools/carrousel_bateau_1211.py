"""Bateau – carrousel 12.11 « כמה שיתופים צריך כדי להטביע ספינה? » : 7 slides 1080×1350 tirées du plateau 3D de reel_pirates.py (ciel de jour, clair).
Usage (racine du dépôt) : PAX=pax.json [N_PAX=41] [ONLY=1,3] python3 tools/carrousel_bateau_1211.py <dossier_three3> <dossier_sortie>"""

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

N_PAX, CAP = int(os.environ.get("N_PAX", "41")), 100
Y = lambda s: f'<span style="color:#FFC24B">{s}</span>'
CSS = """#my{position:fixed;inset:0;pointer-events:none;font-family:Heebo;direction:rtl;color:#fff;z-index:99}
#my .t{position:absolute;left:0;right:0;text-align:center;padding:0 22px;text-shadow:0 3px 14px rgba(0,0,0,.95),0 0 4px rgba(0,0,0,.8)}
#my .h{font:900 48px/1.12 Heebo}#my .s{font:900 30px/1.2 Heebo}#my .big{font:900 120px/1 Heebo;color:#FFC24B}
#my .band{position:absolute;left:0;right:0;height:30%}
#my .num{position:absolute;bottom:2.5%;left:4%;font:900 18px Heebo;opacity:.85;text-shadow:0 2px 6px #000}
#my .brand{position:absolute;top:2.5%;right:4%;background:rgba(10,30,60,.75);border:2px solid #FFC24B;border-radius:999px;padding:3px 12px;font:900 15px Heebo}
#my .bar{margin:10px auto 0;width:78%;height:30px;border-radius:999px;background:rgba(255,255,255,.25);border:3px solid #fff;overflow:hidden}
#my .bar i{display:block;height:100%;background:#FFC24B}
#my .v{display:inline-block;width:40%;margin:6px;border-radius:22px;padding:12px 0;font:900 36px/1.15 Heebo;text-shadow:none}
"""
TB = '<div class=band style="top:0;background:linear-gradient(rgba(5,20,45,.7),rgba(5,20,45,0))"></div>'
BB = '<div class=band style="bottom:0;background:linear-gradient(rgba(5,20,45,0),rgba(5,20,45,.8))"></div>'
L = "const L=ship.len,B=ship.beam,c=ship.view;[PIR,ENV,...BALLS,...FIRE].forEach(o=>{if(o.parent!==evRoot)evRoot.add(o)});"  # placeEventProps() vide evRoot
SLIDES = [
  (L+"R.orbit(0,c.d*.55,c.h*.8+1,c.h*.1,0.75,0)",
   TB+BB+f'<div class="t h" style="top:8%">כמה {Y("שיתופים")}<br>צריך כדי {Y("להטביע")}<br>ספינה? 🚢💥</div>'
   +'<div class="t s" style="bottom:6%">החליקו ← התשובה מפתיעה</div>'),
  (L+"R.cam(-L*.35,c.h*.75+1.5,L*.42,0,c.h*.2,0)",
   TB+BB+f'<div class="t h" style="top:8%">כל שיתוף =<br>{Y("נוסע חדש")} 🧍</div>'
   +f'<div class="t s" style="bottom:7%">וכל נוסע = עוד {Y("משקל")}<br>על הסיפון…</div>'),
  (L+"evRoot.visible=true;PIR.visible=true;PIRPOS(.55);SHOT(.55);{const p=PIR.position;R.cam(-L*.15,L*.55,L*1.0,p.x*.45,L*.02,p.z*.55)}",
   TB+BB+f'<div class="t h" style="top:8%">💥 כל שיתוף =<br>{Y("מכה")} בספינה</div>'
   +'<div class="t s" style="bottom:7%">היא כבר מרגישה את זה…</div>'),
  (L+"R.orbit(0,c.d*.8,c.h*1.6+4,c.h*.1,0.7,0)",
   TB+BB+f'<div class="t h" style="top:7%">כבר על הסיפון:</div><div class="t big" style="top:15%">{N_PAX}</div><div class="t s" style="top:31%">נוסעים 🧍</div>'
   +f'<div class="t" style="bottom:8%"><div class="s">{N_PAX} מתוך {CAP}</div><div class=bar><i style="width:{N_PAX}%"></i></div></div>'),
  (L+"SNK=.85;R.orbit(0,c.d*.5,c.h*.6+1,0,0.3,0)",
   TB+BB+f'<div class="t h" style="top:8%">ב־{Y("100")} נוסעים<br>היא {Y("טובעת")} 🌊</div>'
   +f'<div class="t s" style="bottom:7%">הספינה הראשונה כבר טבעה ⚓<br>עכשיו תורה של זאת</div>'),
  (L+"SNK=.25;R.orbit(0,c.d*.7,c.h*1.3+2,c.h*.2,2.4,0)",
   TB+BB+f'<div class="t h" style="top:7%">חסרים עוד<br>{Y(str(CAP-N_PAX))} שיתופים 😱</div>'
   +'<div class="t s" style="top:28%">מתי היא טובעת?</div>'
   +'<div class="t" style="bottom:12%"><div class="v" style="background:#2fbf71">1️⃣<br>השבוע</div><div class="v" style="background:#E5484D">2️⃣<br>החודש</div></div>'
   +'<div class="t s" style="bottom:4%">תענו 1 או 2 👇</div>'),
  (L+"R.orbit(0,c.d*.55,c.h*1.0+1.5,c.h*.2,-0.9,0)",
   TB+BB+f'<div class="t h" style="top:8%">רוצים לעלות<br>{Y("לספינה")}? 🚢</div>'
   +f'<div class="t h" style="bottom:17%">כתבו {Y("עולה")}<br>ותיכנסו 👇</div>'
   +'<div class="t s" style="bottom:7%">📩 שלחו לחבר שלכם</div>'),
]

def main():
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
        pg = b.new_page(viewport={"width": 540, "height": 675}, device_scale_factor=2)
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

        pg.evaluate("""mode='sea';started=true;setShip(1);setEvent({type:'none',title:''});
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
        pg.add_style_tag(content="#cap,#reelTop,#fade,#lbls,.lbl3,.lbls,.lbl{display:none!important}" + CSS)
        pg.evaluate("()=>{const d=document.createElement('div');d.id='my';document.body.appendChild(d)}")
        for _ in range(150): pg.evaluate("loop()")  # le ciel passe au jour
        only = os.environ.get("ONLY")
        for i, (js, html) in enumerate(SLIDES, 1):
            if only and str(i) not in only.split(","): continue
            pg.evaluate("PIR.visible=false;ENV.visible=false;SNK=0;SHOT(-1);" + js)
            for _ in range(6): pg.evaluate("loop();" + js)
            if os.environ.get("DBG"): print(i, pg.evaluate("[ship.len,ship.beam,ship.view.d,ship.view.h,PIR.position.toArray(),PIR.scale.x,camera.position.toArray()]"))
            pg.evaluate('h=>{document.getElementById("my").innerHTML=h}', html + f'<div class=brand>🚢 טובעים ביחד</div><div class=num>{i}/{len(SLIDES)}</div>')
            pg.wait_for_timeout(250)
            pg.screenshot(path=f"{OUT}/slide{i}.jpg", type="jpeg", quality=92)
        print("slides", len(SLIDES), "ERREURS", errs[:5])
        b.close()

main()
