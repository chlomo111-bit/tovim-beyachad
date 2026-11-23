"""Specs compose.py du reel « הקפטן מספר » #1 (23.11 soir) : Endurance. Usage : python3 specs.py <dossier_images_15fps> > spec.json"""
import json, sys
R = sys.argv[1]; D = 16.0
Y = lambda s: f'<span class=y>{s}</span>'
big = lambda s, sz=76: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{s}</div>'
sub = lambda s: f'<div class=box style="font:900 32px/1.2 H">{s}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">הקפטן מספר ⚓</div>'
ov = [O(0, D, 'T', title, 1)]
M = [(0.0, 1.15, f'{Y("ידעתם")}?'), (1.15, 2.2, f'{Y("בקרח")} ❄️'), (2.2, 3.3, 'אחרי'), (3.3, 4.15, f'{Y("מאה")} שנה!'),
     (4.15, 5.45, f'{Y("אנדיורנס")} 🚢'), (5.45, 7.85, f'<span dir=ltr style="unicode-bidi:isolate">{Y("3,008")}</span> מ׳ 🌊'),
     (7.85, 9.5, f'{Y("זקופה")}!'), (9.5, 10.9, 'שלחו 📩'), (10.9, 11.95, f'{Y("מפתחות")} 🔑'),
     (11.95, 13.3, f'{Y("מחר")}'), (13.3, 14.9, f'{Y("טובעת")} 🌊'), (14.9, D, f'{Y("עקבו")} ⚓')]
for a, b, h in M: ov.append(O(a, b, 'M', big(h), 1 if a == 0 else 0))
B = [(0.09, 2.15, f'ידעתם שהספינה הזאת נעלמה {Y("בקרח")}'), (2.25, 4.1, f'ונמצאה אחרי יותר ממאה שנה?'), (4.17, 5.45, f'קוראים לה {Y("אנדיורנס")}'),
     (5.5, 7.85, f'מצאו אותה בערך {Y("3 ק״מ")} מתחת למים'), (7.9, 9.55, f'עומדת {Y("זקופה")}, כמעט שלמה!'),
     (9.6, 11.95, f'שלחו את זה לחבר {Y("שמחפש כל הזמן את המפתחות")}'), (11.99, 14.9, f'מחר: ספינה שטבעה אחרי {Y("קצת יותר מקילומטר")}'),
     (14.9, D, f'עקבו כדי לדעת ⚓')]
for a, b, h in B: ov.append(O(a, b, 'B', sub(h), 1 if a < .2 else 0))
spec = {'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 15}}, 'flash': .25, 'novg': 0, 'vgmax': .3,
        'hits': [0.02, 2.25, 5.5, 7.9, 9.6, 11.99, 14.9],
        'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0}], 'ov': ov}
print(json.dumps(spec, ensure_ascii=False))
