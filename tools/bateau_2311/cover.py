import sys,base64
from playwright.sync_api import sync_playwright
bg,out,title,sub,col=sys.argv[1:6]
F=''+__import__('os').environ.get('THREE3','/root/three3')+'/node_modules/@fontsource/heebo/files/'
b=lambda p:base64.b64encode(open(p,'rb').read()).decode()
html=f"""<html><head><meta charset=utf-8><style>@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b(F+'heebo-hebrew-900-normal.woff2')})}}
@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b(F+'heebo-latin-900-normal.woff2')});unicode-range:U+0000-00FF}}
html{{overflow:hidden}}body{{margin:0;background:#000;width:1080px;height:1920px;position:relative;overflow:hidden;font-family:H;direction:rtl}}
img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:blur(16px) brightness(.6) saturate(1.2);transform:scale(1.08)}}
.c{{position:absolute;left:60px;right:60px;top:50%;transform:translateY(-50%);text-align:center;color:#fff}}
.t{{font:900 128px/1.08 H;text-shadow:0 8px 40px rgba(0,0,0,.9)}}.t span{{color:{col}}}
.s{{display:inline-block;margin-top:30px;background:{col};color:#140c04;border-radius:30px;padding:14px 40px;font:900 58px H}}</style></head>
<body><img src="data:image/jpeg;base64,{b(bg)}"><div class=c><div class=t>{title}</div><div class=s>{sub}</div></div></body></html>"""
with sync_playwright() as p:
    br=p.chromium.launch();pg=br.new_page(viewport={'width':1080,'height':1920});pg.set_content(html);pg.wait_for_timeout(400);pg.evaluate('()=>{window.scrollTo(0,0);document.documentElement.scrollLeft=0;document.body.scrollLeft=0}');pg.screenshot(path=out,type='jpeg',quality=92);br.close()
