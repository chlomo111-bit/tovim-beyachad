import json
exec(open('/home/claude/hasavta-shelanu/tools/hashchenim_2211/cut.py').read().split('mr=build')[0])
sil=[(2.616,2.921),(3.467,3.884),(5.135,5.583),(6.579,6.928),(7.713,8.091),(8.545,8.966),(9.444,9.881),(10.498,10.669),(11.624,12.013),(12.448,12.747),(13.591,13.979),(14.558,14.913),(16.095,16.536),(18.223,18.540)]
mr=build('reel_raw.mp3','reel_voice.mp3',sil,21.28,.1,1.12)
P={'anachnu':0,'gdola':1.3,'matara':2.92,'asheret':3.88,'uveaseret':5.58,'tovaat':6.93,'karega':8.09,'efes':8.97,'like':9.88,'nosea':10.67,'tguva':12.01,'shlosha':12.75,'shituf':13.98,'asara':14.91,'kitvu':16.54,'chamesh':18.54,'END':21.28}
print(json.dumps({k:round(mr(v),2) for k,v in P.items()}))
ms=build('story_raw.mp3','story_voice.mp3',[(2.245,2.52),(3.373,3.554)],5.92,.1,1.05)
print('story',round(ms(2.52),2),round(ms(3.554),2),round(ms(5.92),2))
