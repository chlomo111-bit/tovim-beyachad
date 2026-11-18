import json
R='/home/claude/b18'
C={k:{'dir':f'{R}/c_{k}','fps':10} for k in ['pir','eye','wide']}
bx=lambda s,sz=30:f'<div class=box style="font:900 {sz}px/1.2 H">{s}</div>'
pill=lambda s,sz=30,bg='#FFC24B',fg='#140c04':f'<div class=pill style="background:{bg};color:{fg};font:900 {sz}px/1.2 H">{s}</div>'
Y=lambda s:f'<span class=y>{s}</span>'
O=lambda t0,t1,pos,h:{'t0':t0,'t1':t1,'pos':pos,'html':h}
btn=lambda n,w,bg:f'<div class=pill style="display:inline-block;margin:6px;width:30%;background:{bg};color:#fff;font:900 36px/1.15 H">{n}<br>{w}</div>'
B1,B2=btn('1️⃣','חבר 🐋','#2fbf71'),btn('2️⃣','אויב 😈','#E5484D')
CNT=pill('🚢 42/100 נוסעים · כל שיתוף = 💥',24,'rgba(10,8,24,.82)','#fff')
AMIT=pill('🧍 <bdi dir=ltr>@amit_azulay23</bdi> על הסיפון!',24,'#fff')
D=7.3
reel={'dur':D,'clips':C,'flash':.5,'novg':2.0,'vgmax':.45,'hits':[1.5],
 'seg':[{'t0':0,'t1':2.55,'clip':'pir','off':0,'zoom':.07},
        {'t0':2.55,'t1':5.27,'clip':'wide','off':.2,'zoom':.06},
        {'t0':5.27,'t1':D,'clip':'eye','off':.5,'zoom':.05}],
 'ov':[dict(O(0,1.2,'T',bx(f'הוא {Y("חזר")}! 🐋',54)),np=1),
       O(1.2,2.55,'T',bx(f'הפיל את {Y("הפיראטים")}! 💥',50)),
       O(2.55,5.27,'T',bx(f'הוא {Y("שומר")} עלינו? 🐋',50)),
       dict(O(0,2.55,'B',CNT),np=1),O(2.55,3.33,'B',AMIT),
       O(3.33,4.28,'B',B1),O(4.28,5.27,'B',B1+B2),
       O(5.27,D,'T',bx(f'כתבו {Y("עולה")} ותיכנסו 🚢',50)),
       O(6.0,D,'B',pill('📩 שלחו לחבר שלכם',38,'#fff'))]}
json.dump(reel,open(f'{R}/reel.json','w'),ensure_ascii=False)
SD=6.5
story={'dur':SD,'clips':C,'flash':.4,'novg':1.0,'vgmax':.45,'hits':[1.3],
 'seg':[{'t0':0,'t1':2.95,'clip':'pir','off':.2,'zoom':.05},{'t0':2.95,'t1':4.19,'clip':'wide','off':.5,'zoom':.06},
        {'t0':4.19,'t1':SD,'clip':'eye','off':.3,'zoom':.05}],
 'ov':[dict(O(0,SD,'T',pill('🚢 טובעים ביחד · 42/100',28,'#8FD3FF','#06203a')),np=1),
       dict(O(0,2.25,'M',bx(f'הלוויתן הפיל<br>את {Y("הפיראטים")}! 🐋💥',52)),np=1),
       O(2.25,2.95,'M',bx(f'איך {Y("נקרא")} לו? 🤔',56)),
       O(2.95,4.19,'M',pill('ראיתם בריל החדש? ←',46,'#fff')),
       O(4.19,SD,'M',bx(f'כתבו {Y("עולה")} 🚢<br>והשם שלכם על הסיפון!',44))]}
json.dump(story,open(f'{R}/story.json','w'),ensure_ascii=False)
print('ok')
