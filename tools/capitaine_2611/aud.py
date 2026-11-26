import json,subprocess,numpy as np
TEMPO=1.1
W=[("ידעתם",0,.32),("שמצאו",.4,.76),("ספינה",.8,1.28),("באמצע",1.36,1.68),("האוקיינוס",1.76,2.5),("בלי",2.68,2.88),("אף",2.96,3.12),("אחד",3.24,3.36),("על",3.4,3.44),("הסיפון",3.48,4),("זאת",4.56,4.8),("מרי",4.84,5.12),("סלסט",5.2,5.76),("בשנת",5.84,6.08),("אלף",6.16,6.28),("שמונה",6.32,6.56),("מאות",6.64,6.8),("שבעים",6.88,7.08),("ושתיים",7.12,7.9),("הספינה",8.16,8.48),("הייתה",8.52,8.72),("שלמה",8.84,9.2),("והמטען",9.36,9.84),("שלה",9.88,10.08),("במקום",10.12,10.64),("אבל",11.12,11.28),("אנשי",11.4,11.52),("הצוות",11.56,12.08),("הם",12.48,12.64),("לא",12.68,12.72),("נמצאו",12.76,13.12),("אף",13.16,13.28),("פעם",13.44,13.68),("שלחו",14.24,14.48),("את",14.56,14.6),("זה",14.64,14.72),("למי",14.76,14.88),("שנעלם",14.96,15.36),("מהקבוצה",15.44,15.84),("בוואטסאפ",15.92,16.48),("בפרק",17.28,17.68),("הבא",17.72,18.08),("למה",18.48,18.64),("לטיטניק",18.72,19.28),("היו",19.32,19.44),("סירות",19.52,19.76),("הצלה",19.84,20.24),("רק",20.4,20.64),("לחלק",20.72,21.12),("מהנוסעים",21.2,22.16),("עקבו",22.24,22.56),("כדי",22.6,22.8),("לדעת",22.84,23.52)]
G=[];cur=None
for w,s,e in W:
    if cur and s-cur[1]<=0.32: cur[1]=e
    else: cur=[s,e];G.append(cur)
keep=[(max(0,a-.04),b+.08) for a,b in G]
for i in range(1,len(keep)):
    if keep[i][0]<keep[i-1][1]: keep[i]=(keep[i-1][1],keep[i][1])
fc=";".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{i}]" for i,(a,b) in enumerate(keep))
fc+=";"+"".join(f"[a{i}]" for i in range(len(keep)))+f"concat=n={len(keep)}:v=0:a=1,atempo={TEMPO}[o]"
subprocess.run(["ffmpeg","-y","-v","error","-i","voix_raw.mp3","-filter_complex",fc,"-map","[o]","-ar","48000","-ac","2","voix.wav"],check=True)
off=0;mp=[]
for a,b in keep: mp.append((a,b,off));off+=b-a
def f(t):
    for a,b,o in mp:
        if a<=t<=b: return (o+t-a)/TEMPO
    for a,b,o in mp:
        if t<a: return o/TEMPO
    return off/TEMPO
out=[(w,round(f(s),2),round(f(e),2)) for w,s,e in W]
print("DUR",off/TEMPO);print(json.dumps(out,ensure_ascii=False))
json.dump(out,open("words_final.json","w"),ensure_ascii=False)
x=subprocess.run(["ffmpeg","-v","error","-i","voix.wav","-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout
a=np.frombuffer(x,dtype=np.float32);n=int(len(a)/16000*30)
r=[float(np.sqrt(np.mean(a[int(i*16000/30):int((i+1)*16000/30)]**2))) for i in range(n)]
m=max(r);json.dump([round(min(1,v/m*1.1),3) for v in r],open("amp.json","w"))
