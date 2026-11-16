import json
R='/home/claude/b16'
C={k:{'dir':f'{R}/c_{k}','fps':10} for k in ['hull','pir','tilt']}
bx=lambda s,sz=30:f'<div class=box style="font:900 {sz}px/1.2 H">{s}</div>'
pill=lambda s,sz=30,bg='#FFC24B',fg='#140c04':f'<div class=pill style="background:{bg};color:{fg};font:900 {sz}px/1.2 H">{s}</div>'
Y=lambda s:f'<span class=y>{s}</span>'
O=lambda t0,t1,pos,h:{'t0':t0,'t1':t1,'pos':pos,'html':h}
btn=lambda n,w,bg:f'<div class=pill style="display:inline-block;margin:6px;width:30%;background:{bg};color:#fff;font:900 38px/1.15 H">{n}<br>{w}</div>'
B1,B2=btn('1️⃣','השבוע','#2fbf71'),btn('2️⃣','החודש','#E5484D')
CNT=lambda sz=24:pill('🚢 42/100 נוסעים · כל שיתוף = 💣',sz,'rgba(10,8,24,.82)','#fff')
AMIT=pill('🧍 <bdi dir=ltr>@amit_azulay23</bdi> עלה לסיפון!',28,'#fff')
D=7.6
reel={'dur':D,'clips':C,'flash':.5,'novg':2.0,'vgmax':.5,
 'hits':[0.25,1.75,6.52],
 'seg':[{'t0':0,'t1':1.6,'clip':'hull','off':0,'zoom':.05},
        {'t0':1.6,'t1':2.92,'clip':'pir','off':.5,'zoom':.07},
        {'t0':2.92,'t1':6.27,'clip':'tilt','off':0,'zoom':.06,'speed':.95},
        {'t0':6.27,'t1':D,'clip':'hull','off':0,'zoom':.04}],
 'ov':[dict(O(0,.59,'T',bx(f'{Y("בום")}! 💥',46)),np=1),
       O(.59,1.6,'T',bx(f'חור {Y("בספינה")}! 🕳️',46)),
       dict(O(0,2.92,'B',CNT()),np=1),
       O(1.6,2.92,'T',bx(f'עוד {Y("ירייה")}! 🏴‍☠️',46)),
       O(2.92,6.27,'T',bx(f'מתי היא {Y("טובעת")}? 🌊',44)+'<div style="height:10px"></div>'+CNT(22)),
       O(2.92,3.94,'B',AMIT),
       O(3.94,4.6,'B',B1),dict(O(4.6,6.27,'B',B1+B2),np=1),
       O(6.27,D,'T',pill('כתבו "עולה" ותיכנסו 🚢',40)),
       O(6.27,D,'B',pill('📩 שלחו לחבר שלכם',40,'#fff'))]}
json.dump(reel,open(f'{R}/reel.json','w'),ensure_ascii=False)
SD=6.6
story={'dur':SD,'clips':C,'flash':.4,'novg':1.0,'vgmax':.45,'hits':[2.64],
 'seg':[{'t0':0,'t1':2.39,'clip':'tilt','off':.7,'zoom':.05},{'t0':2.39,'t1':4.16,'clip':'hull','off':0,'zoom':.06},
        {'t0':4.16,'t1':5.32,'clip':'pir','off':.6,'zoom':.06},{'t0':5.32,'t1':SD,'clip':'tilt','off':1.7,'zoom':.04}],
 'ov':[dict(O(0,SD,'T',pill('🚢 טובעים ביחד · 42/100',28,'#8FD3FF','#06203a')),np=1),
       dict(O(0,1.11,'M',bx(f'{Y("עמית")} כתב עולה! 🧍<br><bdi dir=ltr style="font-size:30px">@amit_azulay23</bdi>',48)),np=1),
       O(1.11,2.39,'M',bx(f'והוא כבר<br>{Y("על הסיפון")}! 🚢',52)),
       O(2.39,4.16,'M',bx(f'אבל יש {Y("חור")}<br>בספינה… 🕳️',54)),
       O(4.16,5.32,'M',pill('ראיתם בריל החדש? ←',46,'#fff')),
       O(5.32,SD,'M',bx(f'כתבו {Y("עולה")} 🚢<br>והשם שלכם על הסיפון!',44))]}
json.dump(story,open(f'{R}/story.json','w'),ensure_ascii=False)
print('ok')
