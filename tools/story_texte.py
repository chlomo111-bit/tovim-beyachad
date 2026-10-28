"""Texte par-dessus un fond de story : python3 tools/story_texte.py <dossier_avec_three3> <fond.png> <sortie.jpg> "<titre html>" "<carte html>" "<petite ligne>"
Style validé : Heebo 900, blanc + mots clés <em> en #FFC24B, carte bleu nuit bordée de jaune en bas. Ne jamais cacher un @ ou un visage."""
import base64,sys
from playwright.sync_api import sync_playwright
SP,BG,OUT,TOP,MID,BOT=sys.argv[1:7];F=SP+"/three3/node_modules/@fontsource/heebo/files/"
b64=lambda p:base64.b64encode(open(p,"rb").read()).decode()
css=f"""@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b64(F+'heebo-hebrew-900-normal.woff2')})}}
@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b64(F+'heebo-latin-900-normal.woff2')});unicode-range:U+0000-00FF}}
@font-face{{font-family:H;font-weight:700;src:url(data:font/woff2;base64,{b64(F+'heebo-hebrew-700-normal.woff2')})}}
body{{margin:0;width:1080px;height:1920px;overflow:hidden;font-family:H,sans-serif;direction:rtl;background:url(data:image/png;base64,{b64(BG)}) center/cover;position:relative}}
.t{{position:absolute;top:220px;left:60px;right:60px;text-align:center;color:#fff;font-weight:900;font-size:96px;line-height:1.12;text-shadow:0 6px 28px rgba(0,40,80,.55)}}
em{{font-style:normal;color:#FFC24B}}
.card{{position:absolute;left:70px;right:70px;bottom:250px;background:rgba(4,25,44,.84);border:3px solid #FFC24B;border-radius:40px;padding:40px 46px;text-align:center;color:#fff}}
.m{{font-weight:900;font-size:66px;line-height:1.2}}.b{{margin-top:18px;font-weight:700;font-size:42px;color:#9DC0DA}}"""
html=f"<html><head><meta charset=utf-8><style>{css}</style></head><body><div class=t>{TOP}</div><div class=card><div class=m>{MID}</div><div class=b>{BOT}</div></div></body></html>"
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={"width":1080,"height":1920})
    pg.set_content(html);pg.wait_for_timeout(800);pg.screenshot(path=OUT,type="jpeg",quality=92);b.close()
