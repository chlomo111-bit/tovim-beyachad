import json
R='/home/claude/b15'
C={k:{'dir':f'{R}/c_{k}','fps':10} for k in ['hit','pir','tilt']}
bx=lambda s,sz=30:f'<div class=box style="font:900 {sz}px/1.2 H">{s}</div>'
pill=lambda s,sz=30,bg='#FFC24B',fg='#140c04':f'<div class=pill style="background:{bg};color:{fg};font:900 {sz}px/1.2 H">{s}</div>'
Y=lambda s:f'<span class=y>{s}</span>'
O=lambda t0,t1,pos,h:{'t0':t0,'t1':t1,'pos':pos,'html':h}
btn=lambda n,w,bg:f'<div class=pill style="display:inline-block;margin:6px;width:40%;background:{bg};color:#fff;font:900 40px/1.15 H">{n}<br>{w}</div>'
B1,B2=btn('1️⃣','השבוע','#2fbf71'),btn('2️⃣','החודש','#E5484D')
CNT=pill('🚢 42/100 נוסעים · כל שיתוף = 💣',26,'rgba(10,8,24,.82)','#fff')
D=7.0
reel={'dur':D,'fps':10,'clips':C,'flash':.5,'novg':2.0,'vgmax':.5,
 'hits':[0.05,0.9,1.6,2.85,6.2],
 'seg':[{'t0':0,'t1':1.6,'clip':'hit','off':0,'zoom':.06},
        {'t0':1.6,'t1':2.85,'clip':'pir','off':.4,'zoom':.08},
        {'t0':2.85,'t1':6.2,'clip':'tilt','off':0,'zoom':.07},
        {'t0':6.2,'t1':D,'clip':'hit','off':0,'zoom':.04}],
 'ov':[dict(O(0,1.6,'T',CNT),np=1),
       dict(O(0,.85,'M',bx(f'כדור {Y("תותח")} 💣',64)),np=1),
       O(.85,1.6,'M',bx(f'על {Y("הסיפון")}! 💥',64)),
       O(1.6,2.85,'M',bx(f'ועוד {Y("3")} בדרך! 🏴‍☠️',60)),
       O(2.85,4.74,'T',CNT),
       O(2.85,3.81,'M',bx(f'מתי היא {Y("טובעת")}? 🌊',58)),
       O(3.81,4.74,'M',bx(f'מתי היא {Y("טובעת")}? 🌊',50)),
       O(2.85,3.81,'B',pill('🧍 <bdi dir=ltr>@yonatan.leibo</bdi> עלה לסיפון!',30,'#fff')),
       O(3.81,4.3,'B',B1),dict(O(4.3,D,'B',B1+B2),np=1),
       O(4.74,6.2,'T',pill(f'כתבו "עולה" ותיכנסו 🚢',44)),
       O(4.74,6.2,'M',bx('תענו 1 או 2 👇',46)),
       O(6.2,D,'T',pill('📩 שלחו לחבר שלכם',46)),
       dict(O(6.2,D,'M',bx(f'כדור {Y("תותח")} 💣',64)),np=1)]}
json.dump(reel,open(f'{R}/reel.json','w'),ensure_ascii=False)
SD=6.9
story={'dur':SD,'fps':10,'clips':C,'flash':.4,'novg':1.0,'vgmax':.45,'hits':[0.05,0.9,2.07,4.45],
 'seg':[{'t0':0,'t1':2.07,'clip':'hit','off':.2,'zoom':.05},{'t0':2.07,'t1':4.45,'clip':'tilt','off':.5,'zoom':.06},
        {'t0':4.45,'t1':5.6,'clip':'pir','off':.3,'zoom':.06},{'t0':5.6,'t1':SD,'clip':'tilt','off':2.0,'zoom':.04}],
 'ov':[dict(O(0,SD,'T',pill('🚢 טובעים ביחד · 42/100',28,'#8FD3FF','#06203a')),np=1),
       dict(O(0,.64,'M',bx(f'{Y("בום")}! 💥',72)),np=1),
       O(.64,2.07,'M',bx(f'הפיראטים פגעו<br>{Y("בסיפון")}! 🏴‍☠️',52)),
       O(2.07,3.85,'M',bx(f'נוסע חדש: {Y("יונתן")} 🧍<br><bdi dir=ltr style="font-size:30px">@yonatan.leibo</bdi>',48)),
       O(3.85,4.45,'M',bx(f'והיא כבר {Y("שוקעת")}! 🌊',52)),
       O(4.45,5.6,'M',pill('ראיתם בריל החדש? ←',48,'#fff')),
       O(5.6,SD,'M',bx(f'כתבו {Y("עולה")} 🚢<br>והשם שלכם על הסיפון!',46))]}
json.dump(story,open(f'{R}/story.json','w'),ensure_ascii=False)
print('ok')
