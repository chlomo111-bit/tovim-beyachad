import subprocess
def build(src,out,sil,total,keep,tempo):
    segs=[];cur=0
    for a,b in sil:
        segs.append((cur,a+keep/2));cur=b-keep/2
    segs.append((cur,total))
    f=''.join(f'[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[s{i}];' for i,(a,b) in enumerate(segs))
    f+=''.join(f'[s{i}]' for i in range(len(segs)))+f'concat=n={len(segs)}:v=0:a=1,atempo={tempo}[o]'
    subprocess.run(['ffmpeg','-v','error','-y','-i',src,'-filter_complex',f,'-map','[o]','-ar','44100',out],check=True)
    def m(t):
        acc=0
        for a,b in segs:
            if t<=b: return (acc+max(0,t-a))/tempo
            acc+=b-a
        return acc/tempo
    return m
mr=build('reel_raw.mp3','reel_voice.mp3',[(1.62,2.18),(3.42,3.74),(5.71,6.01)],7.68,.1,1.08)
ms=build('story_raw.mp3','story_voice.mp3',[(0.60,0.80),(2.26,2.98),(5.52,5.93),(7.10,7.29)],8.24,.1,1.1)
RW=[("כדור",.08),("הסיפון",.92),("ועוד",2.2),("בדרך",2.8),("מתי",3.76),("טובעת",4.24),("אחת",4.8),("שתיים",5.32),("כתבו",6.0),("עולה",6.43),("END",7.6)]
SW=[("בום",.16),("הפיראטים",.8),("יונתן",3.0),("שוקעת",4.96),("ראיתם",5.92),("כתבו",7.28),("END",8.2)]
print({w:round(mr(t),2) for w,t in RW});print({w:round(ms(t),2) for w,t in SW})
