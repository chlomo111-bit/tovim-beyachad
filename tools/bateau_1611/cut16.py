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
mr=build('reel_raw.mp3','reel_voice.mp3',[(.62,.79),(1.90,2.21),(3.68,4.19),(5.32,5.75),(6.22,6.38),(7.10,7.30),(8.62,8.97)],9.62,.08,1.18)
ms=build('story_raw.mp3','story_voice.mp3',[(1.12,1.39),(2.70,3.30),(5.15,5.78),(6.95,7.29)],7.95,.1,1.1)
print('R',{k:round(mr(t),2) for k,t in [('bum',0),('hor',.79),('pir',2.21),('mati',4.19),('1',5.75),('shavua',6.38),('2',7.3),('kitvu',8.97),('end',9.62)]})
print('S',{k:round(ms(t),2) for k,t in [('amit',0),('hu',1.39),('aval',3.3),('reitem',5.78),('kitvu',7.29),('end',7.95)]})
