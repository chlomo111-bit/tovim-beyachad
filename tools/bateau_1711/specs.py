import json
R='/home/claude/b17'
C={k:{'dir':f'{R}/c_{k}','fps':10} for k in ['eye','hit','wide']}
bx=lambda s,sz=30:f'<div class=box style="font:900 {sz}px/1.2 H">{s}</div>'
pill=lambda s,sz=30,bg='#FFC24B',fg='#140c04':f'<div class=pill style="background:{bg};color:{fg};font:900 {sz}px/1.2 H">{s}</div>'
Y=lambda s:f'<span class=y>{s}</span>'
O=lambda t0,t1,pos,h:{'t0':t0,'t1':t1,'pos':pos,'html':h}
btn=lambda n,w,bg:f'<div class=pill style="display:inline-block;margin:6px;width:30%;background:{bg};color:#fff;font:900 38px/1.15 H">{n}<br>{w}</div>'
B1,B2=btn('1️⃣','השבוע','#2fbf71'),btn('2️⃣','החודש','#E5484D')
CNT=lambda sz=24:pill('🚢 42/100 נוסעים · כל שיתוף = 💥',sz,'rgba(10,8,24,.82)','#fff')
AMIT=pill('🧍 <bdi dir=ltr>@amit_azulay23</bdi> על הסיפון!',26,'#fff')
D=7.4
reel={'dur':D,'clips':C,'flash':.5,'novg':2.0,'vgmax':.5,
 'hits':[1.9,5.45],
 'seg':[{'t0':0,'t1':1.3,'clip':'eye','off':1.0,'zoom':.05},
        {'t0':1.3,'t1':2.9,'clip':'hit','off':.4,'zoom':.06},
        {'t0':2.9,'t1':5.45,'clip':'wide','off':0,'zoom':.06},
        {'t0':5.45,'t1':D,'clip':'eye','off':.6,'zoom':.04}],
 'ov':[dict(O(0,2.9,'T',CNT()),np=1),O(2.9,5.45,'T',CNT()+'<div style="height:10px"></div>'+AMIT),
       dict(O(0,1.3,'M',bx(f'לוויתן {Y("ענק")}! 🐋',64)),np=1),
       O(1.3,2.32,'M',bx(f'נגח {Y("בספינה")}! 💥',64)),
       O(2.32,5.45,'M',bx(f'מתי היא<br>{Y("טובעת")}? 🌊',60)),
       O(3.22,4.27,'B',B1),O(4.27,5.45,'B',B1+B2),
       O(5.45,D,'M',bx(f'כתבו {Y("עולה")}<br>ותיכנסו 🚢',62)),
       O(5.45,D,'B',pill('📩 שלחו לחבר שלכם',40,'#fff'))]}
json.dump(reel,open(f'{R}/reel.json','w'),ensure_ascii=False)
SD=6.6
story={'dur':SD,'clips':C,'flash':.4,'novg':1.0,'vgmax':.45,'hits':[.6],
 'seg':[{'t0':0,'t1':2.34,'clip':'hit','off':.4,'zoom':.05},{'t0':2.34,'t1':4.26,'clip':'wide','off':.5,'zoom':.06},
        {'t0':4.26,'t1':SD,'clip':'eye','off':.3,'zoom':.05}],
 'ov':[dict(O(0,SD,'T',pill('🚢 טובעים ביחד · 42/100',28,'#8FD3FF','#06203a')),np=1),
       dict(O(0,2.34,'M',bx(f'לוויתן {Y("ענק")}<br>נגח בספינה! 🐋💥',54)),np=1),
       O(2.34,4.26,'M',bx(f'{Y("42")} נוסעים<br>על הסיפון 🧍',56)),
       O(4.26,5.49,'M',pill('ראיתם בריל החדש? ←',46,'#fff')),
       O(5.49,SD,'M',bx(f'כתבו {Y("עולה")} 🚢<br>והשם שלכם על הסיפון!',44))]}
json.dump(story,open(f'{R}/story.json','w'),ensure_ascii=False)
print('ok')
