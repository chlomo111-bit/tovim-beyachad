"""Monteur : enchaîne des plans 3D déjà filmés (dossiers d'images) + textes HTML animés, image par image.
Usage : python3 compose.py spec.json dossier_sortie"""
import sys, json, glob, os, base64, math
from playwright.sync_api import sync_playwright
spec = json.load(open(sys.argv[1])); OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
FPS = 30; D = spec['dur']
F = ''+__import__('os').environ.get('THREE3','/root/three3')+'/node_modules/@fontsource/heebo/files/'
b64 = lambda p: base64.b64encode(open(p, 'rb').read()).decode()
import subprocess, shutil
def smooth(k, v):
    """Anti-saccades (15.11.2026) : un plan filmé à moins de 30 i/s est interpolé à 30 i/s
    (sinon chaque image est répétée 2-3 fois -> petits gels sur Instagram). Cache dans <dir>_i30."""
    fps = v.get('fps', 30)
    fs = sorted(glob.glob(v['dir'] + '/f*.jpg'))
    if fps >= 30 or len(fs) < 2 or v.get('nointerp'):
        return fs
    out = v['dir'].rstrip('/') + '_i30'
    if not os.path.isdir(out) or len(glob.glob(out + '/f*.jpg')) < 2:
        tmp = out + '_tmp'; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
        lst = tmp + '/list.txt'
        with open(lst, 'w') as fh:
            for f in fs: fh.write(f"file '{os.path.abspath(f)}'\nduration {1/fps:.6f}\n")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-vf',
                        f'fps={fps},minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1',
                        '-q:v', '3', tmp + '/f%04d.jpg'], check=True)
        os.remove(lst); shutil.rmtree(out, ignore_errors=True); os.rename(tmp, out)
    v['fps'] = 30
    print(f'[fluide] {k}: {len(fs)} images a {fps} i/s -> interpolees a 30 i/s')
    return sorted(glob.glob(out + '/f*.jpg'))
CLIPS = {k: smooth(k, v) for k, v in spec['clips'].items()}
HTML = f"""<html><head><meta charset=utf-8><style>
@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b64(F+'heebo-hebrew-900-normal.woff2')})}}
@font-face{{font-family:H;font-weight:900;src:url(data:font/woff2;base64,{b64(F+'heebo-latin-900-normal.woff2')});unicode-range:U+0000-00FF}}
html{{overflow:hidden}}body{{margin:0;width:540px;height:960px;overflow:hidden;background:#000;font-family:H;direction:rtl;position:relative}}
#bg{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform-origin:50% 45%}}
.t{{position:absolute;left:0;right:0;text-align:center;color:#fff;text-shadow:0 3px 16px rgba(0,0,0,.95);padding:0 14px}}
.y{{color:#FFC24B}}.p{{color:#FF8FB8}}.b{{color:#8FD3FF}}
.box{{display:inline-block;background:rgba(10,8,24,.78);border-radius:20px;padding:8px 20px}}
.pill{{display:inline-block;border-radius:22px;padding:10px 22px;text-shadow:none}}
#vg{{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0%,rgba(0,0,0,0) 28%,rgba(0,0,0,0) 62%,rgba(0,0,0,.7) 100%)}}
#fl{{position:absolute;inset:0;background:#fff;opacity:0}}
</style></head><body><img id=bg><div id=vg></div><div class=t id=T style="top:7%"></div><div class=t id=M style="top:36%"></div><div class=t id=B style="bottom:16%"></div><div id=fl></div></body></html>"""
SET = r"""o=>{const bg=document.getElementById('bg');if(bg.dataset.src!==o.src){bg.src=o.src;bg.dataset.src=o.src}
bg.style.transform=`scale(${o.z})`;
for(const k of ['T','M','B']){const e=document.getElementById(k);const h=o[k]||'';if(e.dataset.h!==h){e.dataset.h=h;e.innerHTML=h}
 const a=o['a'+k];e.style.transform=`scale(${a.s})`;e.style.opacity=a.o}
document.getElementById('fl').style.opacity=o.fl;window.scrollTo(0,0);document.documentElement.scrollLeft=0;document.body.scrollLeft=0;document.getElementById('vg').style.opacity=o.vg??1;
return new Promise(r=>bg.complete?r():bg.onload=()=>r())}"""
def ov_at(t, pos):
    best = None
    for o in spec['ov']:
        if o['pos'] == pos and o['t0'] <= t < o['t1']: best = o
    if not best: return '', {'s': 1, 'o': 1}
    e = t - best['t0']
    if e < .28 and not best.get('np'): k = e / .28; s = .5 + .65 * k if k < .6 else 1.15 - .15 * (k - .6) / .4; a = {'s': round(s, 3), 'o': round(min(1, k * 1.8), 3)}
    else: a = {'s': 1, 'o': 1}
    return best['html'], a
WARNED = {}
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2)
    pg.set_content(HTML); pg.wait_for_timeout(300)
    n = int(round(D * FPS))
    for i in range(int(os.environ.get('START', 0)), int(os.environ.get('END', n))):
        t = i / FPS
        sg = [s for s in spec['seg'] if s['t0'] <= t < s['t1']][-1]
        cl = CLIPS[sg['clip']]; cf = spec['clips'][sg['clip']].get('fps', 30)
        idx = int((t - sg['t0'] + sg.get('off', 0)) * cf * sg.get('speed', 1))
        L = len(cl) - 1
        if L > 0:
            if L < idx <= L * 1.1:
                idx = L  # quelques images manquantes : on tient la dernière au lieu de repartir à l'envers
            if idx > L and not WARNED.get(sg['clip']):
                WARNED[sg['clip']] = 1; print(f"[attention] plan '{sg['clip']}' trop court pour le segment : il repart a l'envers (filmer plus long)")
            idx = idx % (2 * L); idx = idx if idx <= L else 2 * L - idx
        u = (t - sg['t0']) / max(.01, sg['t1'] - sg['t0']); z = 1 + sg.get('zoom', .06) * u
        hits = [h for h in spec.get('hits', []) if h <= t]; fl = 0
        if hits and t - hits[-1] < .3: fl = math.exp(-(t - hits[-1]) * 9) * spec.get('flash', .35)
        o = {'src': 'data:image/jpeg;base64,' + b64(cl[idx]), 'z': round(z, 4), 'fl': round(fl, 3), 'vg': 0 if t < spec.get('novg', 0) else spec.get('vgmax', 1)}
        for k in 'TMB':
            h, a = ov_at(t, k); o[k] = h; o['a' + k] = a
        pg.evaluate(SET, o)
        pg.screenshot(path=f'{OUT}/f{i:04d}.jpg', type='jpeg', quality=90)
    b.close(); print('ok', n)
