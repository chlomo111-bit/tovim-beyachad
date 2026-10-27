"""Construit la version « aperçu Artifact » du jeu (sans balises html/head/body, voix en data URI)."""
import base64,sys
src,out=sys.argv[1],sys.argv[2]
s=open(src).read()
for a,b in [('<!doctype html>\n',''),('<html lang="he" dir="rtl">\n',''),('<head>\n',''),('</head>\n',''),('<body>\n',''),('</body>\n',''),('</html>\n',''),
            ('<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover,maximum-scale=1">\n','<meta name="claude:viewport-fit-sides" content="cover">\n'),
            ('<link rel="icon" href="icon.png">\n','')]:
    s=s.replace(a,b)
s=s.replace(':root{\n  --ink','html{direction:rtl}\n:root{\n  --ink',1)
voice="data:audio/mpeg;base64,"+base64.b64encode(open("media/intro_voix.mp3","rb").read()).decode()
s=s.replace('<script>\n/* ================= CONFIG','<script>window.INTRO_VOICE="'+voice+'";</script>\n<script>\n/* ================= CONFIG',1)
open(out,'w').write(s)
