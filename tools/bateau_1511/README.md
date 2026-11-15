Reel Bateau 15.11 « כדור תותח על הסיפון! » (format B, 7 s, 10 i/s).
Filmer (racine du dépôt) : `cat head.js hit.js > s_hit.js; SHOTJS=s_hit.js DUR=3.2 PAX=pax.json DSF=1.4 python3 tools/bateau_1511/film.py /root/three3 c_hit` (idem pir 2.0 s, tilt 3.2 s).
film.py = video_bateau_1411.py + plan paramétrable (SHOTJS : corps de SHOTF(t), t en s) ; POST() remplacé par des valeurs absolues SNK2/ROTZ/ROTX (plus de cumul).
head.js : boom(t,ti) = boulet visible dès l'image 0, explosion, cratère, fumée. Montage : specs.py → compose.py (fps 10) → ffmpeg -framerate 10.
