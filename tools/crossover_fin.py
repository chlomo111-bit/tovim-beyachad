"""Fin commune du crossover « L'enveloppe » (6–7 s) : silhouette de lapin blanc qui saute dans un portail, puis les cartes de l'énigme.
Calque transparent image par image (1080×1920, 30 i/s), à superposer sur le fond 3D.
Usage : python3 tools/crossover_fin.py <dossier_three3> <dossier_sortie> <duree_s> <N> <LETTRE> <compte_suivant>
Ne JAMAIS écrire le mot complet ni nommer l'expéditeur."""
import sys, base64, os
from playwright.sync_api import sync_playwright
SP, OUT, D, N, L, NEXT = sys.argv[1], sys.argv[2], float(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6]
F = SP + "/node_modules/@fontsource/heebo/files/"
b64 = lambda p: base64.b64encode(open(p, "rb").read()).decode()
os.makedirs(OUT, exist_ok=True)
html = f"""<html><head><meta charset=utf-8><style>
@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b64(F+'heebo-hebrew-900-normal.woff2')})}}
@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b64(F+'heebo-latin-900-normal.woff2')});unicode-range:U+0000-00FF}}
@font-face{{font-family:H;font-weight:700;src:url(data:font/woff2;base64,{b64(F+'heebo-hebrew-700-normal.woff2')})}}
html,body{{background:transparent;margin:0}}body{{width:1080px;height:1920px;overflow:hidden;position:relative;font-family:H,sans-serif;direction:rtl}}
#veil{{position:absolute;inset:0;background:radial-gradient(circle at 50% 40%,rgba(30,10,60,.55),rgba(0,0,10,.82))}}
svg{{position:absolute;left:0;top:0}}
.c{{position:absolute;left:70px;right:70px;text-align:center;color:#fff;opacity:0;transform:translateY(30px)}}
#c1{{top:560px;background:#0B1530;border:4px solid #FFC24B;border-radius:44px;padding:40px 30px}}
#c1 .t{{font-weight:900;font-size:62px}}#c1 .l{{font-weight:900;font-size:230px;line-height:1.05;color:#FFC24B;text-shadow:0 0 40px rgba(255,194,75,.6)}}
#c2{{top:1060px;font-weight:900;font-size:56px;text-shadow:0 4px 20px #000}}
#c3{{top:1220px;font-weight:900;font-size:60px;text-shadow:0 4px 20px #000}}#c3 b{{color:#9FE7FF}}
#c4{{top:1380px;font-weight:900;font-size:58px;background:#FFC24B;color:#0B1530;border-radius:30px;padding:22px 20px}}
</style></head><body><div id=veil></div>
<svg width=1080 height=1920><defs><radialGradient id=pg><stop offset="0%" stop-color="#ffffff" stop-opacity=".95"/><stop offset="35%" stop-color="#B98CFF" stop-opacity=".8"/><stop offset="70%" stop-color="#4B2BFF" stop-opacity=".45"/><stop offset="100%" stop-color="#000" stop-opacity="0"/></radialGradient>
<filter id=gl><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<g id=portal transform="translate(560 700)"><ellipse rx=230 ry=300 fill="url(#pg)"/><g id=rings fill=none stroke-width=10 filter="url(#gl)"><ellipse rx=210 ry=280 stroke="#C9A8FF" stroke-dasharray="60 30"/><ellipse rx=170 ry=230 stroke="#7FE0FF" stroke-dasharray="40 40"/></g></g>
<g id=rabbit fill="#fff" filter="url(#gl)"><ellipse cx=0 cy=0 rx=95 ry="62"/><circle cx=-88 cy=-48 r="46"/><ellipse cx=-104 cy=-130 rx=16 ry=62 transform="rotate(-12 -104 -130)"/><ellipse cx=-74 cy=-134 rx=15 ry=58 transform="rotate(10 -74 -134)"/><circle cx=96 cy=-6 r="20"/><ellipse cx=40 cy=48 rx=50 ry="18"/></g></svg>
<div class=c id=c1><div class=t>אות {N} מתוך 5:</div><div class=l>« {L} »</div></div>
<div class=c id=c2>מי שולח את המכתבים? 5 עולמות, 5 אותיות 🔎</div>
<div class=c id=c3>האות הבאה אצל <b dir=ltr style="unicode-bidi:isolate">@{NEXT}</b></div>
<div class=c id=c4>שלחו לחבר שיעזור לכם לפתור 📩</div>
<script>
const E=(x)=>x<0?0:x>1?1:x*x*(3-2*x);
function show(id,t,t0){{const e=document.getElementById(id),k=E((t-t0)/.35);e.style.opacity=k;e.style.transform=`translateY(${{(1-k)*30}}px)`}}
window.R=function(t){{document.getElementById('veil').style.opacity=E(t/.4);
 const p=document.getElementById('portal'),pk=E(t/.5),pf=1-E((t-2.0)/.6)*.75;p.setAttribute('transform',`translate(560 700) scale(${{pk*pf}})`);
 document.getElementById('rings').setAttribute('transform',`rotate(${{t*90}})`);
 const r=document.getElementById('rabbit'),u=Math.min(1,Math.max(0,(t-.15)/1.75));
 const x=160+u*400,y=1300-Math.sin(u*Math.PI)*520-u*80,s=1-u*.85;r.setAttribute('transform',`translate(${{x}} ${{y}}) scale(${{-s}} ${{s}}) rotate(${{-20+u*60}})`);r.style.opacity=u>=1?0:(u>.85?(1-u)/.15:1);
 show('c1',t,1.6);show('c2',t,2.0);show('c3',t,2.6);show('c4',t,4.3)}}
</script></body></html>"""
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.set_content(html); pg.wait_for_timeout(800)
    if os.environ.get("DBG"):
        pg.evaluate("R(1.0)"); print(pg.evaluate("()=>{const r=document.getElementById('rabbit');const b=r.getBoundingClientRect();return [r.getAttribute('transform'),r.style.opacity,b.x,b.y,b.width,b.height]}")); b.close(); sys.exit()
    n = int(round(D * 30))
    for i in range(n):
        pg.evaluate(f"R({i/30:.4f})")
        pg.screenshot(path=f"{OUT}/o{i:04d}.png", omit_background=True)
    b.close()
print("ok", n, "images")
