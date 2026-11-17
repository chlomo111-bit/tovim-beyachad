Reel Bateau 17.11 « לוויתן ענק! » (format B, 7,4 s). whale.js = lavyatan voxel (WHL) qui saute et percute la coque + gerbes ; MODE eye (gros plan de l'œil, ship plein derrière), hit (profil, impact à TI), wide (queue géante derrière la ספינה qui gîte).
Filmer (racine du dépôt) : (echo "const MODE='eye',TI=2.5;"; cat whale.js) > s_eye.js ; SHOTJS=s_eye.js DUR=2.6 PAX=pax.json DSF=1.4 python3 tools/bateau_1711/film.py /root/three3 c_eye (hit TI=1.0 DUR 2.2 ; wide TI=-2 DUR 3.0).
pax.json : supabase bloqué par le proxy → liste synthétique (75 inscrits, 42 sur la ספינה), les étiquettes sont cachées de toute façon.
compose.py local = kit + html{overflow:hidden} et scrollTo(0,0) : une boîte de texte trop large faisait glisser toute l'image (bande noire à gauche).
