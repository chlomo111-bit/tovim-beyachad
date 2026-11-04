"""Story VIDÉO courte (1080×1920, 6–10 s) filmée dans le vrai jeu en 3D, avec musique + bruitages (JAMAIS de voix ElevenLabs).
Règlement du 03.11 : les stories alternent image / vidéo courte avec son.
Usage :
  python3 tools/story_video.py <dossier_three3> <passagers.json> <sortie.mp4> <scene> "<titre html>" "<carte html>" "<petite ligne>" [duree] [focus_handle]
  VOIX=chemin.mp3 (variable d'environnement, optionnelle) : courte phrase parlée (Juniper, eleven_v3, 1 génération) — depuis le 04.11 (Shlomo) les stories vidéo ont des paroles ; la durée s'allonge à voix + 1 s, musique baissée sous la voix.
  scene = orbit (tour du bateau) | deck (gros plan sur un passager, focus_handle) | flyby (survol bas le long de la coque) | sink (le bateau penche/s'enfonce)
  titre/carte : même style que story_texte.py (Heebo 900, mots clés <em> en jaune). Laisser "" pour ne pas afficher.
  Pour un @ dans du texte hébreu : <span dir="ltr" style="unicode-bidi:isolate">@pseudo</span>.
Installer d'abord : mkdir three3 && cd three3 && npm i three@0.128.0 @fontsource/heebo"""
import sys, os, json, base64, subprocess, tempfile, shutil
from playwright.sync_api import sync_playwright

SP, PAXF, OUT, SCENE, TOP, MID, BOT = sys.argv[1:8]
D = float(sys.argv[8]) if len(sys.argv) > 8 else 8.0
VOIX = os.environ.get("VOIX")
if VOIX:
    vd = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", VOIX], capture_output=True, text=True).stdout.strip() or 0)
    D = max(D, round(vd + 1.2, 2))
FOCUS = sys.argv[9] if len(sys.argv) > 9 else ""
T = SP + "/node_modules/three/"; F = SP + "/node_modules/@fontsource/heebo/files/"
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
PAX = json.load(open(PAXF)); FPS = 30; N = int(D * FPS)
tmp = tempfile.mkdtemp(prefix="storyvid_")
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()

# Caméra par image (k = secondes écoulées, u = 0→1)
CAM = {
 "orbit": "const c=ship.view,a=.6+u*1.3;camera.position.set(Math.cos(a)*c.d*.75,c.h*1.0+1.2,Math.sin(a)*c.d*.75);controls.target.set(0,c.h*.25,0);",
 "deck": "const f=byH.get(FOCUS);if(f&&f.slot){const w=worldOf(f,new THREE.Vector3()),s=Math.max(1,figS*1.5),a=.8+u*.7;"
         "camera.position.set(w.x+Math.cos(a)*5*s,w.y+3.2-u*1.2,w.z+Math.sin(a)*5*s);controls.target.set(w.x,w.y+.4,w.z)}"
         "else{const c=ship.view;camera.position.set(c.d*.6,c.h+1.5,c.d*.5);controls.target.set(0,c.h*.25,0)}",
 "flyby": "const c=ship.view,x=(-1+2*u)*c.d*.6;camera.position.set(x,c.h*.35+.8,c.d*.55);controls.target.set(x*.6,c.h*.3,0);",
 "sink": "const c=ship.view,a=.9+u*.5;ship.group.position.y=-(ship.draft||1)*u*.5;ship.group.rotation.z=-u*.12;"
         "camera.position.set(Math.cos(a)*c.d*.7,c.h*.6+1,Math.sin(a)*c.d*.7);controls.target.set(0,c.h*.15,0);",
}[SCENE]

with sync_playwright() as p:
    b = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
    pg = b.new_page(viewport={"width": 540, "height": 960}, device_scale_factor=2)
    pg.add_init_script("window.CAP=true")
    def route(r):
        u = r.request.url
        if "three.min.js" in u: r.fulfill(path=T + "build/three.min.js", content_type="text/javascript")
        elif "OrbitControls" in u: r.fulfill(path=T + "examples/js/controls/OrbitControls.js", content_type="text/javascript")
        elif u.startswith("http://test/"): r.fulfill(path=ROOT + "/index.html")
        elif "supabase.co" in u: r.fulfill(status=200, body="[]", content_type="application/json")
        else: r.abort()
    pg.route("**/*", route); pg.goto("http://test/index.html", wait_until="commit", timeout=90000)
    pg.wait_for_function("typeof window.loop==='function' && typeof ship==='object' && ship", timeout=120000)
    pg.wait_for_timeout(3000)
    pg.evaluate("(pax)=>{P.length=0;byH.clear();ingest(pax);setShip(shipIdx(totalN()));mode='sea';started=true;"
                "['#ui','#gate','#reelTop','#cap','#skip','#newsModal'].forEach(s=>{const e=document.querySelector(s);if(e)e.style.display='none'})}", PAX)
    for _ in range(20): pg.evaluate("loop()")
    js = "(arg)=>{const k=arg[0],u=arg[1],FOCUS=arg[2];loop();{" + CAM + "}camera.lookAt(controls.target);lblT=-1}"
    for i in range(N):
        pg.evaluate(js, [i / FPS, i / max(1, N - 1), FOCUS])
        pg.screenshot(path=f"{tmp}/f{i:04d}.png")
    # calque texte transparent (même style que story_texte.py)
    css = (f"@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b64(F+'heebo-hebrew-900-normal.woff2')})}}"
           f"@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b64(F+'heebo-latin-900-normal.woff2')});unicode-range:U+0000-00FF}}"
           f"@font-face{{font-family:H;font-weight:700;src:url(data:font/woff2;base64,{b64(F+'heebo-hebrew-700-normal.woff2')})}}"
           "html,body{background:transparent}body{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:H,sans-serif;direction:rtl;position:relative}"
           ".t{position:absolute;top:240px;left:60px;right:60px;text-align:center;color:#fff;font-weight:900;font-size:92px;line-height:1.12;text-shadow:0 6px 28px rgba(0,40,80,.75)}"
           "em{font-style:normal;color:#FFC24B}"
           ".card{position:absolute;left:70px;right:70px;bottom:290px;background:#04192C;border:3px solid #FFC24B;border-radius:40px;padding:38px 44px;text-align:center;color:#fff}"
           ".m{font-weight:900;font-size:62px;line-height:1.2}.b{margin-top:16px;font-weight:700;font-size:40px;color:#9DC0DA}")
    card = f"<div class=card><div class=m>{MID}</div>" + (f"<div class=b>{BOT}</div>" if BOT else "") + "</div>" if MID else ""
    html = f"<html><head><meta charset=utf-8><style>{css}</style></head><body>" + (f"<div class=t>{TOP}</div>" if TOP else "") + card + "</body></html>"
    pt = b.new_page(viewport={"width": 1080, "height": 1920}); pt.set_content(html); pt.wait_for_timeout(800)
    pt.screenshot(path=f"{tmp}/txt.png", omit_background=True); b.close()

# musique + bruitages (whoosh à l'entrée, ding quand le texte est là)
ev = "whoosh:0.05,ding:0.6" + (",splash:%.2f" % (D * .55) if SCENE in ("sink", "flyby") else "")
subprocess.run([sys.executable, HERE + "/musique_reel.py", f"{tmp}/m.wav", str(D), ev], check=True)
# texte : apparaît en fondu à 0,4 s, petit zoom continu sur l'image
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", f"{tmp}/f%04d.png",
    "-loop", "1", "-framerate", str(FPS), "-t", str(D), "-i", f"{tmp}/txt.png", "-i", f"{tmp}/m.wav", *(["-i", VOIX] if VOIX else []),
    "-filter_complex", "[0:v]scale=1080:1920,setsar=1[bg];[1:v]format=rgba,fade=in:st=0.4:d=0.35:alpha=1[tx];[bg][tx]overlay=0:0:format=auto,format=yuv420p[v]" + (";[3:a]adelay=500|500,apad[vo];[2:a]volume=0.25[mu];[vo][mu]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.95[a]" if VOIX else ""),
    "-map", "[v]", "-map", "[a]" if VOIX else "2:a", "-t", str(D), "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", OUT], check=True)
shutil.rmtree(tmp, ignore_errors=True)
print("ok", OUT, D, "s")
