"""Story « הקפטן מספר » 24.11 soir : teaser du fait de demain (5 ספינות). Usage : python3 specs_story.py <dossier_images_10fps> > spec_story.json"""
import json, sys
R = sys.argv[1]; D = 6.4
Y = lambda s: f'<span class=y>{s}</span>'
LTR = lambda s: f'<span dir=ltr style="unicode-bidi:isolate">{s}</span>'
big = lambda s, sz=80: f'<div class=box style="font:900 {sz}px/1.1 H;padding:6px 26px">{s}</div>'
O = lambda t0, t1, pos, h, np=0: {'t0': t0, 't1': t1, 'pos': pos, 'html': h, 'np': np}
title = '<div class=pill style="background:#FFC24B;color:#140c04;font:900 28px/1.15 H">הקפטן מספר ⚓</div>'
ov = [O(0, D, 'T', title, 1)]
M = [(0, .95, f'{Y("מחר")}:'), (.95, 2.0, f'{Y(LTR("5"))} ספינות ⛵'), (2.0, 3.4, 'סביב העולם'), (3.4, 4.7, f'כמה {Y("חזרו")}?'), (4.7, D, f'{Y("עקבו")} ⚓')]
for a, b, h in M: ov.append(O(a, b, 'M', big(h, 72), 1 if a == 0 else 0))
spec = {'dur': D, 'fps': 30, 'clips': {'all': {'dir': R, 'fps': 10}}, 'flash': 0, 'novg': 0, 'vgmax': .3,
        'hits': [], 'seg': [{'t0': 0, 't1': D, 'clip': 'all', 'off': 0, 'zoom': 0}], 'ov': ov}
print(json.dumps(spec, ensure_ascii=False))
