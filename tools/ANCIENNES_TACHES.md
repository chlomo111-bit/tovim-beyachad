# Anciennes tâches programmées du bateau (archivées le 30.10.2026)

Ces tâches ont été désactivées par le directeur des jeux le 30.10.2026 vers 12:46 (heure d'Israël), puis supprimées.
Elles sont remplacées par un seul chat « Automatisation – טובעים ביחד » et ses réveils send_later (voir tools/AUTOMATISATIONS.md).
Texte complet gardé ici pour référence.

---

## trig_01BqmdaMTbTEuVF8eAqh3qe9 — « טובעים ביחד — passages 5:55 / 11:55 / 16:55 / 19:55 »
Cron : `CRON_TZ=Asia/Jerusalem 55 5,11,16,19 * * *` (créée le 28.10.2026)

```
Passage du jeu Instagram « טובעים ביחד » (@tovim_beyachad, tovim.hakaveret.online). Règles de Shlomo du 30.10.2026 (autonomie complète, réponds en français, textes Instagram en hébreu). Sois économe.

0. SHABBAT : regarde l'heure d'Israël (TZ=Asia/Jerusalem date). Si on est vendredi à partir de 16:00 ou samedi avant 18:30 → termine IMMÉDIATEMENT sans rien faire d'autre.
1. add_repo (owner chlomo111-bit, repo tovim-beyachad, access push), clone, LIS ENTIÈREMENT tools/ROUTINE.md et applique les sections « RÈGLES OBLIGATOIRES », « Règlement des commentaires » et « PASSAGE » à la lettre. git pull --rebase avant chaque push.
2. Comptes : Instagram via Composio account instagram_odoom-cither UNIQUEMENT (vérifier username tovim_beyachad avant toute action ; sinon STOP + prévenir Shlomo). Supabase account supabase_restow-lise, SUPABASE_BETA_RUN_SQL_QUERY, ref xcrlfujevlvwmrswwvfq uniquement. Pas de Lovable.
3. Résumé de ce que fait le passage : lire tous les nouveaux commentaires des publications récentes, répondre à chacun (court, varié, jamais de copier-coller, pas d'URL → « הקישור בביו »), passagers VIP, ig_comment_log (compte du meilleur commentateur), billet_eligible pour les commentateurs du post du jour (samedi 19:55 : aussi ceux du post du vendredi avec day = vendredi), vœu du meilleur commentateur d'hier (avant 12:00), abonnés dans game_state, modération du chat ; vérifier que le post du jour existe (sinon le créer). À 19:55 seulement : story « 5 דקות להגרלה! » (participants, meilleur commentateur du moment, 2 conditions).
4. Si rien de nouveau et rien à faire → termine tout de suite.
Ne touche à aucune autre tâche programmée ni à un autre jeu. Ne préviens Shlomo qu'en cas de problème grave (une phrase).
```

---

## trig_015neEiXpEe68YX9aEkV5eaw — « טובעים ביחד — loterie 20:00 »
Cron : `CRON_TZ=Asia/Jerusalem 1 20 * * 0-4,6` (créée le 28.10.2026)

```
Loterie du soir du jeu Instagram « טובעים ביחד » (@tovim_beyachad, tovim.hakaveret.online). Règles de Shlomo du 30.10.2026 : autonomie complète, réponds en français, textes Instagram en hébreu. Sois économe.

0. Si on est vendredi (heure d'Israël) → termine immédiatement (le tirage du vendredi a lieu samedi à 20:00).
1. add_repo (owner chlomo111-bit, repo tovim-beyachad, access push), clone, LIS ENTIÈREMENT tools/ROUTINE.md et applique « RÈGLES OBLIGATOIRES » (3 et 3 bis) et « LOTERIE » à la lettre. git pull --rebase avant chaque push.
2. Comptes : Instagram Composio account instagram_odoom-cither UNIQUEMENT (vérifier username tovim_beyachad avant chaque publication ; sinon STOP + prévenir Shlomo). Supabase account supabase_restow-lise, SUPABASE_BETA_RUN_SQL_QUERY, ref xcrlfujevlvwmrswwvfq uniquement. Pas de Lovable.
3. select run_lottery(<date du jour, heure d'Israël>) — le samedi : d'abord run_lottery(<vendredi>) puis celui du samedi (le jeu a peut-être déjà tiré en direct : la fonction renvoie alors le même résultat). Pour chaque tirage : story du résultat (gagnant + participants + 👑 המגיב של היום + « מה יקרה מחר בזכותך? »), réponse au dernier commentaire du meilleur commentateur, actualité news.
4. Message à Shlomo (SendUserMessage + PushNotification avec <routine_summary>) : « Loterie <jour> : gagnant @x (N participants) → 20 ₪ à payer par Bit. Meilleur commentateur : @y. » Sans gagnant : une ligne.
Ne touche à aucune autre tâche programmée ni à un autre jeu.
```

---

## trig_014C857RU18g7hJGWDL5GqVe — « טובעים ביחד — production du matin (6:34) »
Cron : `CRON_TZ=Asia/Jerusalem 34 6 * * 0-5` (créée le 28.10.2026)

```
Production du matin du jeu Instagram « טובעים ביחד » (@tovim_beyachad, tovim.hakaveret.online). Règles de Shlomo du 30.10.2026 : autonomie complète (y compris send_later), réponds en français, textes Instagram en hébreu. Sois économe.

0. SHABBAT : si l'heure d'Israël est vendredi ≥ 16:00 ou samedi < 18:30 → termine immédiatement.
1. add_repo (owner chlomo111-bit, repo tovim-beyachad, access push), clone, LIS ENTIÈREMENT tools/ROUTINE.md et applique « RÈGLES OBLIGATOIRES » et « PRODUCTION DU MATIN » à la lettre. git pull --rebase avant chaque push.
2. Comptes : Instagram Composio account instagram_odoom-cither UNIQUEMENT (vérifier username tovim_beyachad avant chaque publication ; sinon STOP + prévenir Shlomo). Supabase account supabase_restow-lise, ref xcrlfujevlvwmrswwvfq uniquement. Pas de Lovable.
3. Dans l'ordre : lire tous les commentaires du dernier reel/post (le plus liké décide) + résultat de la loterie d'hier et vœu du meilleur commentateur ; boîte à idées ; ÉVÉNEMENT EXTRAORDINAIRE du jour dans le jeu (+ news) ; POST DU JOUR 4:5 (hook + 2 conditions de la loterie 20:00 + « הגיבו כאן 👇 ») publié et enregistré dans billet_gate ; texte voix de la VIDÉO DU JOUR (ce qui s'est passé, vrais @, vrais chiffres, fin « מה יקרה מחר? התגובה עם הכי הרבה לייקים קובעת ») dans media/AAAA-MM-JJ/voix.txt, puis send_later à 17:00 (vendredi 10:30) pour l'envoyer à Shlomo (SendUserMessage + PushNotification) en demandant le MP3 Juniper ; mise en ligne 19:30 (vendredi : samedi 18:30, avec une tâche ponctuelle). Si un voix.txt ou un reel existe déjà pour aujourd'hui, ne refais pas la vidéo.
Ne touche à aucune autre tâche programmée ni à un autre jeu. Ne préviens Shlomo de rien d'autre, sauf problème grave.
```

---

## trig_01HzAmnDasTC7t7ZuPaG4AfS — « טובעים ביחד – story + popup « The Noise arrive » (sam. 19:08) »
Ponctuelle : samedi 31.10.2026 19:08 (17:08Z). Remplacée par un send_later dans le chat d'automatisation à la même heure.

```
Ordre du directeur des jeux (validé par Shlomo le 30/10) pour le jeu « טובעים ביחד » (@tovim_beyachad) : faire venir les passagers vers le nouveau jeu The Noise (@the_noise_2026, thenoise.hakaveret.online), qui lance ce soir son reel de lancement en collaboration. Textes en hébreu. Autonome, économe.
Instagram : compte Composio instagram_odoom-cither UNIQUEMENT (vérifie username tovim_beyachad avant). Dépôt : add_repo chlomo111-bit/tovim-beyachad (push), clone, lis tools/ROUTINE.md, git pull --rebase avant push. Supabase uniquement ref xcrlfujevlvwmrswwvfq. Ne touche à aucune tâche programmée.
1. Story 1080×1920 style du jeu (outils tools/story_fond.py et tools/story_texte.py) : « 🎤 חדש! The Noise » + « הקפטן שלנו שר בזמן שהספינה טובעת 😂 » + « תפסו מקום בקהל – @the_noise_2026 ». Héberge-la dans media/2026-10-31/story_thenoise.jpg, publie-la (STORIES), une seule fois.
2. Ajoute une actualité dans le jeu (table news) : « 🎤 The Noise – התוכנית הכי מזייפת באינסטגרם התחילה! הקפטן כבר על הבמה » avec le lien https://thenoise.hakaveret.online , visible 3 jours.
3. Termine par une ligne (story publiée, actualité ajoutée). Ne préviens Shlomo qu'en cas de problème.
```
