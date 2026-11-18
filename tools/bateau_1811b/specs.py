import json
R='/home/claude/b18e'
C={k:{'dir':f'{R}/c_{k}','fps':10} for k in ['wave','boat','c1','c2','jump']}
bx=lambda s,sz=30:f'<div class=box style="font:900 {sz}px/1.2 H">{s}</div>'
pill=lambda s,sz=30,bg='#FFC24B',fg='#140c04':f'<div class=pill style="background:{bg};color:{fg};font:900 {sz}px/1.2 H">{s}</div>'
Y=lambda s:f'<span class=y>{s}</span>'
O=lambda t0,t1,pos,h:{'t0':t0,'t1':t1,'pos':pos,'html':h}
btn=lambda n,w,bg:f'<div class=pill style="display:inline-block;margin:6px;width:36%;background:{bg};color:#fff;font:900 34px/1.15 H">{n}<br>{w}</div>'
B1,B2=btn('1️⃣','הקפטן 🧭','#2F6FDB'),btn('2️⃣','הטבח 🎂','#E5484D')
TAG='<div class=pill style="background:rgba(10,8,24,.6);color:#fff;font:900 17px/1.2 H;padding:4px 14px">🌊 דילמות בים · פרק 1</div>'
D=14.8
reel={'dur':D,'clips':C,'flash':.35,'novg':2.1,'vgmax':.4,'hits':[0.9],'tag':TAG,
 'seg':[{'t0':0,'t1':2.1,'clip':'wave','off':0,'zoom':.05},
        {'t0':2.1,'t1':4.3,'clip':'boat','off':0,'zoom':.06},
        {'t0':4.3,'t1':6.5,'clip':'c1','off':0,'zoom':.06},
        {'t0':6.5,'t1':9.25,'clip':'c2','off':0,'zoom':.06},
        {'t0':9.25,'t1':D,'clip':'jump','off':0,'zoom':.04}],
 'ov':[dict(O(0,1.05,'T',bx(f'{Y("גל ענק")}! 🌊',60)),np=1),
       O(1.05,2.1,'T',bx(f'הספינה {Y("טובעת")}! 😱',54)),
       O(2.1,4.3,'T',bx(f'נשאר מקום ל{Y("אחד")}<br>בסירת ההצלה… 🛟',46)),
       O(2.9,4.3,'B',pill('את מי אתם מצילים? 🤔',40,'#fff')),
       O(4.3,6.5,'T',bx(f'1️⃣ {Y("הקפטן")} 🧭',58)),O(4.75,6.5,'B',bx('שיודע לנווט הביתה',40)),
       O(6.5,9.25,'T',bx(f'2️⃣ {Y("הטבח")} 👨‍🍳',58)),O(7.65,9.25,'B',bx(f'עם {Y("עוגה ענקית")}! 🎂',42)),
       O(9.25,10.54,'T',bx(f'רגע… {Y("שניהם")} קפצו!! 😱',50)),O(9.6,10.54,'B',pill('מי נוחת בסירה? 👀',40,'#fff')),
       O(10.54,D,'T',bx(f'אתם מחליטים:<br>{Y("1 או 2")}? בתגובות 👇',48)),
       O(10.54,12.42,'B',B1+B2),
       O(12.42,D,'B',pill('🏷️ תייגו את החבר<br>שהיה קופץ ראשון',38,'#fff'))]}
json.dump(reel,open(f'{R}/reel.json','w'),ensure_ascii=False)
SD=6.6
story={'dur':SD,'clips':C,'flash':.3,'novg':1.0,'vgmax':.4,'hits':[0.05],'tag':TAG,
 'seg':[{'t0':0,'t1':1.98,'clip':'boat','off':.3,'zoom':.05},{'t0':1.98,'t1':2.9,'clip':'c1','off':.5,'zoom':.05},{'t0':2.9,'t1':3.67,'clip':'c2','off':1.2,'zoom':.05},
        {'t0':3.67,'t1':SD,'clip':'jump','off':1.3,'zoom':.06}],
 'ov':[dict(O(0,1.98,'M',bx(f'נשאר מקום<br>ל{Y("אחד")} בסירה! 🛟',54)),np=1),
       O(1.98,2.9,'M',bx(f'1️⃣ {Y("הקפטן")}?',58)),O(2.9,3.67,'M',bx(f'2️⃣ {Y("הטבח")}? 🎂',58)),
       O(3.67,SD,'M',bx(f'כתבו {Y("1 או 2")} 👇<br>בריל החדש',50))]}
json.dump(story,open(f'{R}/story.json','w'),ensure_ascii=False)
print('ok')
