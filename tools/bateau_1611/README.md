Reel Bateau 16.11 « חור בספינה! » (format A, 7,6 s). Plans : hull (boulet dans la coque dès l'image 0, trou + jets d'eau, hullA.js avec HX/TI), pir (= head.js+pir.js du 15.11), tilt (hullA TI=-3 + gîte, caméra large).
Filmer depuis la racine du dépôt : SHOTJS=s_hull.js DUR=2.6 PAX=pax.json DSF=1.4 python3 tools/bateau_1611/film.py /root/three3 c_hull (pir 2.0, tilt 3.2).
Voix : cut16.py (silences coupés, atempo 1.18) ; montage specs16.py → reels_kit/compose.py (interpolation 30 i/s) → mix.sh ; vote.py = image-question story.
