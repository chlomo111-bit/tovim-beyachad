import json,subprocess,numpy as np
W=[("ידעתם?",.1,.58),("חמש",1.04,1.34),("ספינות",1.38,1.68),("יצאו",1.72,1.96),("להקיף",2,2.28),("את",2.34,2.4),("העולם",2.44,2.84),("ורק",3.24,3.6),("אחת",3.66,4.019),("סיימה",4.08,4.3),("את",4.34,4.4),("המסע",4.44,4.84),("זה",5.42,5.52),("היה",5.54,5.74),("המסע",5.78,6.06),("של",6.14,6.28),("מגלן",6.34,6.78),("לפני",6.86,7.08),("יותר",7.12,7.38),("מחמש",7.42,7.92),("מאות",7.96,8.1),("שנה",8.16,8.42),("מגלן",9.06,9.34),("עצמו",9.38,9.68),("לא",9.84,9.94),("שב",10.02,10.16),("הביתה",10.2,10.58),("רק",10.94,11.08),("הספינה",11.12,11.46),("ויקטוריה",11.5,12.04),("חזרה",12.1,12.34),("לספרד",12.38,12.84),("אחרי",12.9,13.16),("שהקיפה",13.22,13.62),("את",13.66,13.8),("כל",13.9,14.06),("העולם",14.08,14.48),("שלחו",15.1,15.3),("את",15.34,15.4),("זה",15.42,15.48),("לחבר",15.52,15.88),("שאמר",15.96,16.48),("אני",16.58,16.76),("בא",16.82,17),("ונעלם",17.28,17.8),("באמצע",17.84,18.14),("הטיול",18.18,18.64),("מחר",19.32,19.72),("כמה",20.18,20.36),("מקרקעית",20.4,20.92),("הים",20.96,21.24),("באמת",21.32,21.72),("מצולם",21.76,22.22),("עקבו",22.64,22.9),("כדי",22.94,23.12),("לדעת",23.16,23.62)]
# groups
G=[];cur=None
for w,s,e in W:
    if cur and s-cur[1]<=0.3: cur[1]=e
    else:
        cur=[s,e];G.append(cur)
keep=[(max(0,a-.05),b+.09) for a,b in G]
# non-overlap
for i in range(1,len(keep)):
    if keep[i][0]<keep[i-1][1]: keep[i]=(keep[i-1][1],keep[i][1])
fc=";".join(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{i}]" for i,(a,b) in enumerate(keep))
fc+=";"+"".join(f"[a{i}]" for i in range(len(keep)))+f"concat=n={len(keep)}:v=0:a=1,atempo=1.08[o]"
subprocess.run(["ffmpeg","-y","-v","error","-i","voix_raw.mp3","-filter_complex",fc,"-map","[o]","-ar","48000","-ac","2","voix.wav"],check=True)
# mapping old->final
off=0;mp=[]
for a,b in keep: mp.append((a,b,off));off+=b-a
def f(t):
    for a,b,o in mp:
        if a<=t<=b: return (o+t-a)/1.08
    for a,b,o in mp:
        if t<a: return o/1.08
    return off/1.08
out=[(w,round(f(s),2),round(f(e),2)) for w,s,e in W]
print(off/1.08);print(json.dumps(out,ensure_ascii=False))
json.dump(out,open("words_final.json","w"),ensure_ascii=False)
# amp
import wave
x=subprocess.run(["ffmpeg","-v","error","-i","voix.wav","-f","f32le","-ac","1","-ar","16000","-"],capture_output=True).stdout
a=np.frombuffer(x,dtype=np.float32);n=int(len(a)/16000*30)
r=[float(np.sqrt(np.mean(a[int(i*16000/30):int((i+1)*16000/30)]**2))) for i in range(n)]
m=max(r);amp=[round(min(1,v/m*1.1),3) for v in r]
json.dump(amp,open("amp.json","w"))
