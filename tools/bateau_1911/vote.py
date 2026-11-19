import base64
from playwright.sync_api import sync_playwright
F='/root/three3/node_modules/@fontsource/heebo/files/'
b=lambda p:base64.b64encode(open(p,'rb').read()).decode()
H=f"""<html><head><meta charset=utf-8><style>@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b(F+'heebo-hebrew-900-normal.woff2')})}}
@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b(F+'heebo-latin-900-normal.woff2')});unicode-range:U+0000-00FF}}
body{{margin:0;width:540px;height:960px;overflow:hidden;font-family:H;direction:rtl;background:url(data:image/jpeg;base64,{b('c_mouth/f0045.jpg')}) center/cover}}
.c{{position:absolute;left:30px;right:30px;text-align:center;color:#fff}}
.box{{background:rgba(10,8,24,.82);border-radius:24px;padding:14px 18px;font:900 46px/1.2 H}}
.y{{color:#FFC24B}}.p{{display:inline-block;border-radius:22px;padding:8px 18px;font:900 26px H}}
.v{{display:inline-block;vertical-align:top;white-space:nowrap;width:40%;margin:8px;border-radius:24px;padding:14px 0;font:900 42px/1.15 H;color:#fff}}</style></head><body>
<div class=c style="top:7%"><span class=p style="background:#8FD3FF;color:#06203a">🚢 42/100 נוסעים · פרק 2</span></div>
<div class=c style="top:16%"><div class=box>הלוויתן <span class=y>פותח את הפה</span>! 😱<br>מה הטבח מציל?</div></div>
<div class=c style="top:52%"><span class=p style="background:#fff;color:#140c04">🧍 על הסיפון: <bdi dir=ltr>@amit_azulay23</bdi></span></div>
<div class=c style="bottom:14%"><div class=v style="background:#E5484D">1️⃣<br>העוגה 🎂</div><div class=v style="background:#2F6FDB">2️⃣<br>הקפטן 🧭</div></div>
<div class=c style="bottom:6%"><div class=box style="font-size:34px;display:inline-block">תענו 1 או 2 בהודעה 📩</div></div></body></html>"""
with sync_playwright() as p:
    br=p.chromium.launch();pg=br.new_page(viewport={'width':540,'height':960},device_scale_factor=2);pg.set_content(H);pg.wait_for_timeout(500)
    pg.screenshot(path='story_vote.jpg',type='jpeg',quality=90);br.close()
