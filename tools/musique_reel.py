"""Bande son du reel : musique énergique + vagues + bruitages calés sur le montage.
Usage : python3 tools/musique_reel.py sortie.wav duree "boom:0,whoosh:4.1,horn:13.9,..." """
import numpy as np, wave, sys
SR = 44100
out, D = sys.argv[1], float(sys.argv[2])
events = [(k, float(v)) for k, v in (e.split(":") for e in sys.argv[3].split(","))] if len(sys.argv) > 3 else []
N = int(SR * D); rng = np.random.default_rng(11); tt = np.arange(N) / SR
mix = np.zeros(N)

def env(n, att, dur):
    t = np.arange(n) / SR; return np.clip(t / max(att, 1e-4), 0, 1) * np.exp(-np.maximum(t - att, 0) * (6.9 / dur))
def put(sig, t0, gain=1.0):
    i = int(t0 * SR); j = min(N, i + len(sig))
    if i < N: mix[i:j] += sig[:j - i] * gain
def tri(f, n): t = np.arange(n) / SR; return 2 * np.abs(2 * ((t * f) % 1) - 1) - 1
def noise(n): return rng.standard_normal(n)
def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    for i in range(len(x)): acc = (1 - a) * x[i] + a * acc; y[i] = acc
    return y

# --- musique : 112 bpm, pentatonique, basse + caisse + mélodie
bpm = 112; beat = 60 / bpm
CH = [[146.83, 220, 293.66], [130.81, 196, 261.63], [110, 164.81, 220], [123.47, 185, 246.94]]
SC = [293.66, 329.63, 369.99, 440, 493.88, 587.33, 659.25, 739.99]
music = np.zeros(N)
t = 0.0; st = 0
while t < D:
    ch = CH[(st // 8) % 4]
    n = int(beat * .9 * SR)
    b = np.sin(2 * np.pi * ch[0] / 2 * np.arange(n) / SR) * env(n, .005, beat * .9) * .32
    i = int(t * SR); j = min(N, i + n); music[i:j] += b[:j - i]          # basse
    k = int(.18 * SR); kick = np.sin(2 * np.pi * np.cumsum(np.linspace(140, 45, k)) / SR) * env(k, .002, .18) * .5
    if st % 2 == 0: music[i:min(N, i + k)] += kick[:min(N, i + k) - i]   # grosse caisse
    if st % 4 == 2:
        m = int(.12 * SR); sn = noise(m) * env(m, .001, .12) * .12; music[i:min(N, i + m)] += sn[:min(N, i + m) - i]
    if st % 8 == 0:
        m = int(beat * 8 * SR)
        for f in ch: pad = tri(f, m) * env(m, .6, beat * 8) * .045; music[i:min(N, i + m)] += pad[:min(N, i + m) - i]
    if rng.random() < .6:
        f = SC[rng.integers(len(SC))]; m = int(.35 * SR)
        s = tri(f, m) * env(m, .005, .35) * .07; ii = int((t + (beat / 2 if rng.random() < .3 else 0)) * SR)
        music[ii:min(N, ii + m)] += s[:min(N, ii + m) - ii]
    t += beat; st += 1
music *= np.clip(tt / 1.0, 0, 1) * np.clip((D - tt) / 1.5, 0, 1)

# --- vagues
w = lowpass(noise(N), 500) * (0.5 + 0.5 * np.sin(2 * np.pi * .14 * tt)) * .9
mix += music + w * .25

# --- bruitages
for kind, t0 in events:
    if kind == "boom":
        n = int(1.4 * SR); s = np.sin(2 * np.pi * np.cumsum(np.linspace(90, 30, n)) / SR) * env(n, .003, 1.4) * 1.1
        s += lowpass(noise(n), 900) * env(n, .002, .5) * .6; put(s, t0)
    elif kind == "whoosh":
        n = int(.7 * SR); s = lowpass(noise(n), 1500) * np.sin(np.linspace(0, np.pi, n)) * .55; put(s, t0)
    elif kind == "horn":
        n = int(2.6 * SR); s = sum(np.sign(np.sin(2 * np.pi * f * np.arange(n) / SR)) for f in (110, 116.5, 82.4))
        put(lowpass(s, 700) * env(n, .15, 2.6) * .35, t0)
    elif kind == "splash":
        n = int(1.6 * SR); put(lowpass(noise(n), 1800) * env(n, .01, 1.6) * .9, t0)
    elif kind == "rise":
        n = int(2.5 * SR); f = np.linspace(120, 600, n); put(np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .1, 2.6) * .25, t0)
    elif kind == "pop":
        n = int(.12 * SR); put(np.sin(2 * np.pi * np.cumsum(np.linspace(500, 1200, n)) / SR) * env(n, .002, .12) * .35, t0)
    elif kind == "ding":
        for k2, f in enumerate((784, 988, 1318, 1568)):
            n = int(.4 * SR); put(tri(f, n) * env(n, .003, .4) * .22, t0 + k2 * .08)

mix /= max(1e-6, np.max(np.abs(mix))) / .85
pcm = (mix * 32767).astype(np.int16)
with wave.open(out, "wb") as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes(pcm.tobytes())
print("ok", D)
