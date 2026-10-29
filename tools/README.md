# טובעים ביחד : outils

- `supabase_v3.sql` (29.10.2026) : fonctions communes à tous les jeux : pièces par jour (`coins_daily`), missions du jour, boîte à idées, chat modéré + signalements + realtime, statistiques, classements. Voir ROUTINE.md.
- `supabase.sql` : base complète (passagers, naufrages, 3 billets de 20 ₪/jour, pièces d'or, chat, actualités, événement du jour, anti-doublon Instagram). Remplacer MOT_DE_PASSE_A_CHANGER avant de lancer.
- Paliers : 25 / 100 / 1 000 / 10 000 / 100 000 / 1 000 000 (`SHIPS` dans index.html et `ship_caps()` dans le SQL : changer les deux ensemble).
- Liens utiles : `#admin` (gestion), `#reel` (tour des nouveaux passagers du jour, sans interface), `#sink` (rejoue le dernier naufrage), en démo `#demo=600` / `#ev=storm`.
- Événements du jour (admin) : storm, shark, iceberg, party, whale, kraken.
- Tests : `test_shots.py`, `test_scenes.py`, `test_cap.py` (capture image par image en mode CAP, même principe que capture_reel.py de la ruche).
