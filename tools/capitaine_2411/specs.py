"""Specs compose.py du reel « הקפטן מספר » #2 (24.11 matin) : Vasa. Usage : python3 specs.py <dossier_images_10fps> > spec.json"""
import json, sys
R = sys.argv[1]; D = 18.2
Y = lambda s: f'<span class=y>{s}</span>'
big = lambda s, sz=76: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{s}</div>'
sub = lambda s: f'<div class=box style="font:900 32px/1.2 H">{s}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">הקפטן מספר #2 ⚓</div>'
ov = [O(0, D, 'T', title, 1)]
M = [(0, 1.15, f'{Y("ידעתם")}?'), (1.15, 2.0, 'ספינה 🚢'), (2.0, 2.5, f'{Y("טבעה")}!'), (2.5, 3.4, f'{Y("יום ראשון")}!'),
     (3.4, 4.5, 'יצאה מהנמל'), (4.5, 6.2, f'<span dir=ltr style="unicode-bidi:isolate">{Y("1")}</span> ק״מ'), (6.2, 7.1, f'{Y("משב רוח")} 💨'),
     (7.1, 8.1, f'{Y("שקעה")}! 🌊'), (8.1, 9.1, f'<span dir=ltr style="unicode-bidi:isolate">{Y("300")}</span> שנה'), (9.1, 10.4, 'הוציאו אותה'),
     (10.4, 11.4, f'{Y("שלמה")}!'), (11.4, 12.9, 'שלחו 📩'), (12.9, 14.3, f'{Y("יום ראשון")} בעבודה'), (14.3, 15.5, f'{Y("מחר")}:'),
     (15.5, 16.5, f'{Y("אוורסט")} 🏔️'), (16.5, 17.4, 'כתבו שם'), (17.4, D, f'{Y("ואקרא")} לכם ⚓')]
for a, b, h in M: ov.append(O(a, b, 'M', big(h), 1 if a == 0 else 0))
B = [(0.01, 1.95, 'ידעתם שספינת המלחמה המלכותית הזאת'), (1.95, 3.3, f'טבעה {Y("ביום הראשון")} שלה?'),
     (3.6, 6.15, f'יצאה מהנמל, ואחרי קצת יותר {Y("מקילומטר")}'), (6.3, 7.75, f'{Y("משב רוח")}, והיא שקעה!'),
     (8.1, 10.3, 'אחרי שלוש מאות שנה הוציאו אותה מהמים'), (10.3, 11.3, f'{Y("כמעט שלמה")}!'),
     (11.45, 13.25, 'שלחו למי שהיום הראשון שלו בעבודה'), (13.25, 14.25, 'לא הלך חלק'),
     (14.3, 16.45, f'מחר: מפילים את {Y("האוורסט")} לתהום!'), (16.6, D, f'כתבו שם – {Y("ואקרא לכם")}!')]
for a, b, h in B: ov.append(O(a, b, 'B', sub(h), 1 if a < .2 else 0))
spec = {'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 10}}, 'flash': .25, 'novg': 0, 'vgmax': .3,
        'hits': [0.02, 3.4, 6.3, 8.1, 10.3, 11.45, 14.3, 16.6],
        'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0}], 'ov': ov}
print(json.dumps(spec, ensure_ascii=False))
