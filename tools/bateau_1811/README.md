Reel Bateau 18.11 « הוא חזר! » (format A, 7,3 s) : le lavyatan saute et retombe sur le bateau PIRATE qui chavire.
pir.js = MODE pir (vue de côté, impact à TI, T0 = élan déjà commencé à l'image 0). Plans wide/eye = ../bateau_1711/whale.js.
Filmer (racine du dépôt) : (echo "const MODE='pir',TI=1.5,T0=.35;"; cat tools/bateau_1811/pir.js) > s_pir.js ; SHOTJS=s_pir.js DUR=3.3 PAX=pax.json DSF=1.4 python3 tools/bateau_1711/film.py /root/three3 c_pir
Montage : specs18.py -> reel.json/story.json, compose.py du kit (10 i/s interpolé à 30). cut18.py : coupe des silences de la voix.
