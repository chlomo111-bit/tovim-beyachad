Reel Bateau 18.11 18:00 « דילמות בים · פרק 1 » (14,8 s) : גל ענק → נשאר מקום לאחד בסירת ההצלה → 1 הקפטן / 2 הטבח עם העוגה → שניהם קופצים (cliffhanger).
ep1.js = plans MODE wave/boat/c1/c2/jump (personnages voxel CH1 capitaine, CH2 cuisinier + gâteau, canot LB, vague WAV).
Filmer (racine du dépôt) : (echo "const MODE='wave';"; cat tools/bateau_1811b/ep1.js) > s_wave.js ; SHOTJS=s_wave.js DUR=2.3 PAX=pax.json DSF=1.4 python3 tools/bateau_1711/film.py /root/three3 c_wave  (boat 2.4, c1 2.4, c2 2.9, jump 5.7)
Montage : specs.py → compose.py local (= kit + étiquette fixe « פרק N » en haut, spec 'tag'). cut.py : coupe des silences de la voix.
