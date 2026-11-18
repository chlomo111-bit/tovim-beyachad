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
mr=build('v_reel_raw.mp3','reel_voice.mp3',[(1.26,1.55),(2.99,3.48),(4.27,4.72),(5.15,5.36),(5.83,6.20),(6.74,6.98),(7.39,7.85)],9.40,.08,1.12)
ms=build('v_story_raw.mp3','story_voice.mp3',[(2.28,2.62),(3.28,3.70),(4.92,5.13)],5.85,.08,1.05)
print('R',{k:round(mr(t),2) for k,t in [('hazar',0),('pil',1.55),('shomer',3.48),('1',4.72),('2',6.2),('kitvu',7.85),('end',9.4)]})
print('S',{k:round(ms(t),2) for k,t in [('pil',0),('eich',2.62),('reitem',3.7),('kitvu',5.13),('end',5.85)]})
