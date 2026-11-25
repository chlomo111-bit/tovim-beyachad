"""Specs compose.py « הקפטן מספר #4 » (25.11 matin) : מגלן / 5 ספינות. Usage : python3 specs.py <dossier_images_10fps> > spec.json"""
import json, sys
R = sys.argv[1]; D = 19.2
Y = lambda s: f'<span class=y>{s}</span>'
LTR = lambda s: f'<span dir=ltr style="unicode-bidi:isolate">{s}</span>'
big = lambda s, sz=76: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{s}</div>'
sub = lambda s: f'<div class=box style="font:900 32px/1.2 H">{s}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">הקפטן מספר #4 ⚓</div>'
ov = [O(0, D, 'T', title, 1)]
M = [(0, .62, f'{Y("ידעתם")}?'), (.62, 1.45, 'חמש'), (1.45, 2.4, 'ספינות ⛵'), (2.4, 3.5, f'רק {Y("אחת")}!'), (3.5, 4.4, 'המסע ⚓'),
     (4.4, 5.35, f'{Y("מגלן")}'), (5.35, 6.9, f'{Y(LTR("500"))} שנה'), (6.9, 7.95, f'לא {Y("שב")}'), (7.95, 8.6, 'הביתה'),
     (8.6, 9.55, f'{Y("ויקטוריה")}'), (9.55, 10.5, 'חזרה 🏠'), (10.5, 11.85, f'{Y("הקיפה")} 🌍'), (11.85, 12.7, 'שלחו 📩'),
     (12.7, 13.8, 'אני בא'), (13.8, 15.29, f'{Y("נעלם")} 💨'), (15.29, 16.0, f'{Y("מחר")}:'), (16.0, 17.2, 'הים 🌊'),
     (17.2, 17.8, f'{Y("מצולם")}?'), (17.8, D, f'{Y("עקבו")} ⚓')]
for a, b, h in M: ov.append(O(a, b, 'M', big(h), 1 if a == 0 else 0))
B = [(0.05, 2.35, f'ידעתם? {Y("חמש")} ספינות יצאו<br>להקיף את העולם'), (2.4, 3.95, f'ורק {Y("אחת")} סיימה את המסע!'),
     (4.0, 6.85, f'המסע של {Y("מגלן")}<br>לפני יותר מ-{LTR("500")} שנה'), (6.9, 8.4, f'מגלן עצמו {Y("לא שב")} הביתה'),
     (8.45, 10.25, f'רק {Y("ויקטוריה")} חזרה לספרד'), (10.28, 11.8, f'אחרי שהקיפה {Y("את כל העולם")}'),
     (11.85, 15.25, f'שלחו את זה לחבר שאמר {Y("אני בא")}<br>ונעלם באמצע הטיול 😅'), (15.28, 17.75, f'מחר: כמה מקרקעית הים<br>{Y("באמת")} מצולם?'),
     (17.8, D, f'עקבו כדי לדעת ⚓')]
for a, b, h in B: ov.append(O(a, b, 'B', sub(h), 1 if a < .2 else 0))
spec = {'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 10}}, 'flash': .25, 'novg': 0, 'vgmax': .3,
        'hits': [0.02, 2.4, 4.0, 6.9, 8.47, 11.88, 13.9, 15.29, 17.81],
        'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0}], 'ov': ov}
print(json.dumps(spec, ensure_ascii=False))
