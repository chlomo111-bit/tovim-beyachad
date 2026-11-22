"""Specs « הספינה הכי גדולה בעולם? » חלק 1 (22.11) + story compteur. Usage : python3 specs.py <dossier_clips> <points>"""
import json, sys, re
ISO = lambda d: [o.update(html=re.sub(r'\+(\d+)', r'<span dir=ltr style="unicode-bidi:isolate">+\1</span>', o['html'])) for o in d['ov']]
R = sys.argv[1]; PTS = int(sys.argv[2])
C = {k: {'dir': f'{R}/c_{k}', 'fps': 10} for k in ('wide', 'sink', 'empty', 'demo', 'spots', 'end')}
Y = lambda s: f'<span class=y>{s}</span>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
big = lambda s, sz=70: f'<div style="font:900 {sz}px/1.12 H">{s}</div>'
TITLE = (f'<div class=box style="font:900 42px/1.15 H">הספינה הכי {Y("גדולה")} בעולם?</div><br>'
         f'<div class=pill style="margin-top:10px;background:#FFC24B;color:#140c04;font:900 25px/1.2 H">🚢 <span dir=ltr style="unicode-bidi:isolate">{PTS:,} / 10,000</span> נוסעים</div>'
         f'<div style="margin-top:6px;font:900 16px H;opacity:.85">חלק 1</div>')
BAR = '<div class=pill style="background:rgba(8,24,48,.84);color:#fff;font:900 21px/1.35 H">❤️ לייק +1 · 💬 תגובה +3<br>🔖 שמירה +5 · 🚀 שיתוף +10</div>'
SHARE = '<br><div class=pill style="margin-top:8px;background:#8FD3FF;color:#08182f;font:900 24px H">📩 שלחו לחבר שלכם</div>'
D = 17.0
demo = lambda s: '<div style="font:900 22px H;margin-bottom:6px;opacity:.95">ככה עולים לספינה 👇</div>' + s
reel = {'dur': D, 'fps': 30, 'clips': C, 'flash': .45, 'novg': 2.0, 'vgmax': .35,
 'hits': [0.02, 2.42, 5.19, 6.48, 6.99, 8.57, 9.89, 10.49, 11.64, 13.24],
 'seg': [{'t0': 0, 't1': 2.42, 'clip': 'wide', 'off': 0, 'zoom': .04},
         {'t0': 2.42, 't1': 5.98, 'clip': 'sink', 'off': 0, 'zoom': .05},
         {'t0': 5.98, 't1': 6.99, 'clip': 'empty', 'off': 0, 'zoom': .04},
         {'t0': 6.99, 't1': 11.64, 'clip': 'demo', 'off': 0, 'zoom': .05},
         {'t0': 11.64, 't1': 13.24, 'clip': 'spots', 'off': 0, 'zoom': .04},
         {'t0': 13.24, 't1': D, 'clip': 'end', 'off': 0, 'zoom': .03}],
 'ov': [O(0, D, 'T', TITLE, 1), O(0, 15.6, 'B', BAR, 1), O(15.6, D, 'B', BAR + SHARE, 1),
        O(0, 1.16, 'M', big('אנחנו בונים… 🚢', 72), 1),
        O(1.16, 2.42, 'M', big(f'הכי {Y("גדולה")}<br>בעולם!', 80)),
        O(2.42, 3.0, 'M', big('המטרה:', 76)),
        O(3.0, 4.21, 'M', big(f'{Y("10,000")}<br>נוסעים', 90)),
        O(4.21, 5.19, 'M', big('ואז…', 84)),
        O(5.19, 5.98, 'M', '<div class=box>' + big(f'היא {Y("טובעת")}! 🌊', 72) + '</div>'),
        O(5.98, 6.48, 'M', big('כרגע?', 84)),
        O(6.48, 6.99, 'M', big(f'{Y("0")} 😱', 130)),
        O(6.99, 7.63, 'M', demo(big('לייק ❤️', 80))),
        O(7.63, 8.57, 'M', demo(big(f'{Y("+1")} נוסע', 84))),
        O(8.57, 9.05, 'M', demo(big('תגובה 💬', 80))),
        O(9.05, 9.89, 'M', demo(big(f'{Y("+3")} נוסעים', 84))),
        O(9.89, 10.49, 'M', demo(big('שיתוף 🚀', 84))),
        O(10.49, 11.64, 'M', demo(big(f'{Y("+10")} בבת אחת!', 66))),
        O(11.64, 13.24, 'M', big(f'כתבו מה אתם<br>{Y("לוקחים")} איתכם<br>לספינה 👇', 56)
          + '<div class=pill style="margin-top:12px;background:#fff;color:#08182f;font:900 24px H">🏆 המקומות פנויים – תהיו הראשונים</div>'),
        O(13.24, 15.6, 'M', big(f'{Y("5")} התגובות הכי טובות<br>נכנסות לפרק הבא 🏆', 50)),
        O(15.6, D, 'M', big(f'התחלנו {Y("מאפס")}…<br>כל לייק = עוד נוסע 🚢', 50))]}
ISO(reel); json.dump(reel, open(f'{R}/reel.json', 'w'), ensure_ascii=False)
SD = 6.6
story = {'dur': SD, 'fps': 30, 'clips': C, 'flash': .35, 'novg': 1.5, 'vgmax': .4, 'hits': [0.02, 2.23, 3.14],
 'seg': [{'t0': 0, 't1': 2.23, 'clip': 'wide', 'off': 0, 'zoom': .04}, {'t0': 2.23, 't1': SD, 'clip': 'demo', 'off': .2, 'zoom': .05}],
 'ov': [O(0, SD, 'T', TITLE, 1), O(0, SD, 'B', BAR, 1),
        O(0, 2.23, 'M', big(f'🚢 {Y(f"{PTS:,}")}<br>נוסעים… עדיין!', 74), 1),
        O(2.23, 3.14, 'M', big('שתפו את הריל 🚀', 64)),
        O(3.14, SD, 'M', '<div class=box>' + big(f'שתפו את הריל<br>= {Y("+10")} נוסעים!', 62) + '</div>')]}
ISO(story); json.dump(story, open(f'{R}/story.json', 'w'), ensure_ascii=False)
print('ok')
