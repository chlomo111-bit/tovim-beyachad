import subprocess,sys
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
S=[(1.03,1.32),(2.36,2.70),(4.95,5.40),(5.81,6.06),(7.83,8.28),(8.73,8.94),(9.54,9.74),(11.36,11.68),(11.95,12.31),(13.24,13.70),(14.44,14.74),(15.83,16.22)]
mr=build('v_reel_raw.mp3','reel_voice.mp3',S,18.48,.08,1.06)
print({t:round(mr(t),2) for t in [0,1.32,2.70,5.40,6.06,8.28,8.94,9.74,11.68,12.31,13.70,14.74,16.22,18.48]})
ms=build('v_story_raw.mp3','story_voice.mp3',[(1.90,2.30),(3.91,4.34)],5.76,.08,1.0)
print({t:round(ms(t),2) for t in [0,2.3,4.34,5.76]})
