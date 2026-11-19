import json
R='/home/claude/b19'
C={k:{'dir':f'{R}/c_{k}','fps':10} for k in ['leap','land','cap','eye','mouth']}
bx=lambda s,sz=30:f'<div class=box style="font:900 {sz}px/1.2 H">{s}</div>'
pill=lambda s,sz=30,bg='#FFC24B',fg='#140c04':f'<div class=pill style="background:{bg};color:{fg};font:900 {sz}px/1.2 H">{s}</div>'
Y=lambda s:f'<span class=y>{s}</span>'
O=lambda t0,t1,pos,h:{'t0':t0,'t1':t1,'pos':pos,'html':h}
btn=lambda n,w,bg:f'<div class=pill style="display:inline-block;margin:6px;width:36%;background:{bg};color:#fff;font:900 34px/1.15 H">{n}<br>{w}</div>'
B1,B2=btn('1️⃣','העוגה 🎂','#E5484D'),btn('2️⃣','הקפטן 🧭','#2F6FDB')
TAG='<div class=pill style="background:rgba(10,8,24,.6);color:#fff;font:900 17px/1.2 H;padding:4px 14px">🌊 דילמות בים · פרק 2</div>'
D=14.95
reel={'dur':D,'clips':C,'flash':.3,'novg':1.45,'vgmax':.4,'hits':[2.0,7.65],'tag':TAG,
 'seg':[{'t0':0,'t1':1.45,'clip':'leap','off':0,'zoom':.05},
        {'t0':1.45,'t1':4.75,'clip':'land','off':0,'zoom':.06},
        {'t0':4.75,'t1':6.15,'clip':'cap','off':0,'zoom':.06},
        {'t0':6.15,'t1':7.6,'clip':'eye','off':0,'zoom':.07},
        {'t0':7.6,'t1':D,'clip':'mouth','off':0,'zoom':.04}],
 'ov':[dict(O(0,1.45,'T',bx(f'{Y("לוויתן ענק")}! 🐋',62)),np=1),
       O(1.45,2.92,'T',bx(f'⏪ בפרק הקודם:<br>{Y("שניהם")} קפצו…',48)),
       O(2.92,4.75,'T',bx(f'הטבח {Y("נחת בסירה")}! 👨‍🍳',50)),O(3.6,4.75,'B',pill('עם העוגה! 🎂',40,'#fff')),
       O(4.75,6.15,'T',bx(f'והקפטן?<br>{Y("נפל למים")}! 😱',54)),
       O(6.15,7.6,'T',bx(f'הלוויתן… {Y("מריח")}<br>את העוגה 👃🎂',50)),
       O(7.6,8.62,'T',bx(f'הוא {Y("פותח את הפה")}!! 😱',50)),
       O(8.62,10.05,'T',bx(f'אפשר להציל<br>רק {Y("אחד")}! 😬',54)),O(8.9,10.05,'B',pill('מה הטבח מציל? 👀',40,'#fff')),
       O(10.05,D,'T',bx(f'אתם מחליטים:<br>{Y("1 או 2")}? בתגובות 👇',48)),
       O(10.05,13.15,'B',B1+B2),
       O(13.15,D,'B',pill('📩 שלחו לחבר<br>שהיה מציל את העוגה 😂',36,'#fff'))]}
json.dump(reel,open(f'{R}/reel.json','w'),ensure_ascii=False)
SD=6.8
story={'dur':SD,'clips':C,'flash':.3,'novg':1.0,'vgmax':.4,'hits':[0.05],'tag':TAG,
 'seg':[{'t0':0,'t1':2.09,'clip':'mouth','off':.4,'zoom':.05},{'t0':2.09,'t1':3.16,'clip':'mouth','off':3.0,'zoom':.06},{'t0':3.16,'t1':4.11,'clip':'land','off':2.2,'zoom':.05},
        {'t0':4.11,'t1':5.25,'clip':'cap','off':.6,'zoom':.05},{'t0':5.25,'t1':SD,'clip':'mouth','off':4.5,'zoom':.06}],
 'ov':[dict(O(0,2.09,'M',bx(f'הלוויתן {Y("פותח את הפה")}! 😱',54)),np=1),
       O(2.09,3.16,'M',bx(f'מה הטבח {Y("מציל")}? 👀',56)),
       O(3.16,4.11,'M',bx(f'1️⃣ את {Y("העוגה")}? 🎂',56)),O(4.11,5.25,'M',bx(f'2️⃣ את {Y("הקפטן")}? 🧭',56)),
       O(5.25,SD,'M',bx(f'כתבו {Y("1 או 2")} 👇<br>בריל החדש',50))]}
json.dump(story,open(f'{R}/story.json','w'),ensure_ascii=False)
print('ok')
