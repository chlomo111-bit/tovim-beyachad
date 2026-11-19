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
S=[(1.82,2.23),(4.06,4.38),(6.87,7.19),(7.82,8.15),(9.02,9.55),(10.46,10.83),(11.73,12.22),(13.41,13.88),(15.68,16.0),(17.02,17.37),(18.65,18.97),(20.49,20.81)]
mr=build('v_reel_raw.mp3','reel_voice.mp3',S,23.12,.07,1.3)
print('R',{t:round(mr(t),2) for t in [0,2.23,4.38,7.19,8.15,9.55,10.83,12.22,13.88,16.0,17.37,18.97,20.81,23.12]})
SS=[(2.27,2.63),(3.76,4.01),(5.0,5.32),(6.53,6.85)]
ms=build('v_story_raw.mp3','story_voice.mp3',SS,8.56,.07,1.12)
print('S',{t:round(ms(t),2) for t in [0,2.63,4.01,5.32,6.85,8.56]})
