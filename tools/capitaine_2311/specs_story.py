"""Specs de la story « הקפטן מספר » (teaser du fait de demain : Vasa). Usage : python3 specs_story.py <dossier_images_15fps> > spec_story.json"""
import json, sys
R = sys.argv[1]; D = 6.95
Y = lambda s: f'<span class=y>{s}</span>'
big = lambda s, sz=70: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{s}</div>'
sub = lambda s: f'<div class=box style="font:900 32px/1.2 H">{s}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">הקפטן מספר ⚓</div>'
ov = [O(0, D, 'T', title, 1)]
for a, b, h in [(0, .85, f'{Y("מחר")}'), (.85, 2.4, f'{Y("ספינה")} 🚢'), (2.4, 3.75, f'ביום {Y("הראשון")}'), (3.75, 5.7, f'{Y("קילומטר")} 🌊'), (5.7, D, f'{Y("אל תפספסו")} ⚓')]:
    ov.append(O(a, b, 'M', big(h), 1 if a == 0 else 0))
for a, b, h in [(0.05, .8, 'מחר:'), (.85, 3.6, f'ספינת מלחמה ענקית שטבעה {Y("ביום הראשון")} שלה'), (3.75, 5.6, f'אחרי קצת יותר {Y("מקילומטר")}!'), (5.7, D, f'אל תפספסו ⚓')]:
    ov.append(O(a, b, 'B', sub(h), 1 if a < .2 else 0))
spec = {'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 15}}, 'flash': .25, 'novg': 0, 'vgmax': .3, 'hits': [0.02, .85, 3.75, 5.7],
        'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0}], 'ov': ov}
print(json.dumps(spec, ensure_ascii=False))
