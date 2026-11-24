"""Specs compose.py du reel « הקפטן מספר #3 » (24.11 soir) : Everest / Challenger Deep. Usage : python3 specs.py <dossier_images_10fps> > spec.json"""
import json, sys
R = sys.argv[1]; D = 19.7
Y = lambda s: f'<span class=y>{s}</span>'
LTR = lambda s: f'<span dir=ltr style="unicode-bidi:isolate">{s}</span>'
big = lambda s, sz=76: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{s}</div>'
sub = lambda s: f'<div class=box style="font:900 32px/1.2 H">{s}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">הקפטן מספר #3 ⚓</div>'
ov = [O(0, D, 'T', title, 1)]
M = [(0, .9, f'{Y("ידעתם")}?'), (.9, 1.8, 'אוורסט 🏔️'), (1.8, 2.8, f'{Y("לתהום")}'), (2.8, 3.7, f'{Y("ייעלם")}?'),
     (3.7, 5.0, 'הכי עמוק'), (5.0, 6.2, 'בים 🌊'), (6.2, 7.4, f'{Y(LTR("11"))} ק״מ'), (7.4, 8.4, 'אוורסט 🏔️'), (8.4, 9.5, f'{Y("הכי גבוה")}'),
     (9.5, 10.7, 'ובכל זאת'), (10.7, 12.3, f'{Y("מים")} מעליו 🌊'), (12.3, 13.5, 'שלחו 📩'), (13.5, 14.7, f'{Y("הכי גבוה")} בחדר'),
     (14.7, 15.6, f'{Y("מחר")}:'), (15.6, 17.0, f'{Y(LTR("5"))} ספינות ⛵'), (17.0, 18.2, f'כמה {Y("חזרו")}?'), (18.2, D, f'{Y("עקבו")} ⚓')]
for a, b, h in M: ov.append(O(a, b, 'M', big(h), 1 if a == 0 else 0))
B = [(0.05, 2.75, f'ידעתם שאם נפיל את האוורסט<br>לתהום הכי עמוקה בים'), (2.8, 3.6, f'{Y("הוא ייעלם?")}'),
     (3.75, 5.4, f'התהום נקראת {Y("צ׳לנג׳ר דיפ")}'), (5.5, 7.3, f'עמוקה בערך {Y(LTR("11"))} קילומטרים'),
     (7.65, 9.5, f'האוורסט – ההר {Y("הכי גבוה")} בעולם'), (9.6, 12.3, f'ובכל זאת יישארו מעליו<br>{Y("יותר מקילומטר")} של מים!'),
     (12.6, 14.5, 'שלחו למי שחושב<br>שהוא הכי גבוה בחדר'), (14.9, 18.3, f'מחר: מתוך {Y("חמש")} ספינות שיצאו<br>להקיף את העולם – כמה חזרו?'),
     (18.6, D, f'עקבו כדי לדעת ⚓')]
for a, b, h in B: ov.append(O(a, b, 'B', sub(h), 1 if a < .2 else 0))
spec = {'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 10}}, 'flash': .25, 'novg': 0, 'vgmax': .3,
        'hits': [0.02, 3.3, 7.65, 12.3, 14.9, 15.7],
        'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0}], 'ov': ov}
print(json.dumps(spec, ensure_ascii=False))
