"""Stories image 1080x1920 centrées (22.11) : python3 story_img.py <bg.jpg> <out.jpg> <html_contenu>"""
import sys, base64
from playwright.sync_api import sync_playwright
bg, out, body = sys.argv[1:4]
F = '/root/three3/node_modules/@fontsource/heebo/files/'
b = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
html = f"""<html><head><meta charset=utf-8><style>@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b(F+'heebo-hebrew-900-normal.woff2')})}}
@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b(F+'heebo-latin-900-normal.woff2')});unicode-range:U+0000-00FF}}
html{{overflow:hidden}}body{{margin:0;width:1080px;height:1920px;position:relative;overflow:hidden;font-family:H;direction:rtl;background:#1b1d5e}}
img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:brightness(.62) saturate(1.15)}}
.c{{position:absolute;left:70px;right:70px;top:50%;transform:translateY(-50%);text-align:center;color:#fff;text-shadow:0 6px 30px rgba(0,0,0,.9)}}
.y{{color:#FFC24B}}.pill{{display:inline-block;border-radius:34px;padding:16px 40px;text-shadow:none}}
.box{{display:inline-block;background:rgba(10,8,24,.8);border-radius:36px;padding:18px 40px}}</style></head>
<body><img src="data:image/jpeg;base64,{b(bg)}"><div class=c>{body}</div></body></html>"""
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 1080, 'height': 1920}); pg.set_content(html); pg.wait_for_timeout(400)
    pg.screenshot(path=out, type='jpeg', quality=92); br.close()
