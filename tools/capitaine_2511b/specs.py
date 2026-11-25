"""Specs compose.py « הקפטן מספר #5 » (25.11 soir) : רבע מקרקעית הים מופה. Usage : python3 specs.py <dossier_images_10fps> > spec.json"""
import json, sys
R = sys.argv[1]; D = 15.3
Y = lambda s: f'<span class=y>{s}</span>'
big = lambda s, sz=76: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{s}</div>'
sub = lambda s: f'<div class=box style="font:900 32px/1.2 H">{s}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">הקפטן מספר #5 ⚓</div>'
ov = [O(0, D, 'T', title, 1)]
M = [(0, .87, f'{Y("ידעתם")}?'), (.87, 1.78, f'רק {Y("רבע")}'), (1.78, 2.75, 'קרקעית 🌊'), (2.75, 3.9, f'{Y("מופה")} 🗺️'),
     (3.9, 5.2, 'כל השאר'), (5.2, 5.88, 'תמונה'), (5.88, 6.9, f'{Y("גסה")} 🛰️'), (6.9, 7.9, 'שלחו 📩'),
     (7.9, 9.0, f'{Y("לחבר")}'), (9.0, 9.97, f'{Y("העולם")} 🌍'), (9.97, 10.87, f'{Y("מחר")}:'), (10.87, 11.8, 'ספינה ⛵'),
     (11.8, 12.7, 'בלי'), (12.7, 13.55, f'{Y("אף אחד")} 👻'), (13.55, 14.4, f'{Y("עקבו")}'), (14.4, D, '⚓')]
for a, b, h in M: ov.append(O(a, b, 'M', big(h), 1 if a == 0 else 0))
B = [(0.03, .86, f'{Y("ידעתם")}?'), (.87, 4.1, f'רק בערך {Y("רבע")} מקרקעית הים<br>מופה בפירוט'), (4.13, 7.0, f'על כל השאר יש רק<br>תמונה {Y("גסה")} מלוויינים'),
     (7.06, 9.9, f'שלחו את זה לחבר שחושב<br>שהוא {Y("מכיר")} את העולם 😅'), (9.97, 13.5, f'מחר: הספינה שנמצאה<br>בלי {Y("אף אחד")} על הסיפון'),
     (13.59, D, f'עקבו כדי לדעת ⚓')]
for a, b, h in B: ov.append(O(a, b, 'B', sub(h), 1 if a < .2 else 0))
spec = {'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 10}}, 'flash': .25, 'novg': 0, 'vgmax': .3,
        'hits': [0.02, 0.87, 4.13, 7.06, 9.97, 13.59],
        'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0}], 'ov': ov}
print(json.dumps(spec, ensure_ascii=False))
