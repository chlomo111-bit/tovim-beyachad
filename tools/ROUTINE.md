# Routine autonome — טובעים ביחד (@tovim_beyachad)

Shlomo a donné l'autonomie complète le 28.10.2026 : stories, reels, réponses et gestion des passagers, SANS lui demander de confirmation. On lui demande SEULEMENT l'enregistrement vocal (MP3 ElevenLabs) des reels, et de payer le gagnant de la loterie (20 ₪ par Bit). Le prévenir uniquement en cas de problème grave (connexion cassée, mauvais compte, publication impossible), en français, en une phrase.

## RÈGLE INSTAGRAM OBLIGATOIRE (Shlomo, 28.10.2026)
- Pour TOUTE action Instagram via Composio (publier, lire les commentaires, répondre, statistiques) : passer `account: "instagram_odoom-cither"` dans CHAQUE appel. Ne JAMAIS utiliser le compte par défaut ni un autre compte (hakaveret_shelanu, chlomo_assouline…).
- Juste avant CHAQUE publication (post, story, reel, commentaire) : INSTAGRAM_GET_USER_INFO (ig_user_id "me", account instagram_odoom-cither) et vérifier que username = tovim_beyachad. Sinon : NE RIEN PUBLIER et prévenir Shlomo immédiatement (SendUserMessage + PushNotification).

## Identifiants
- Instagram (Composio) : compte `instagram_odoom-cither` UNIQUEMENT (username tovim_beyachad, ig_user_id `39487392790907301`). Vérifier le username avant toute action. JAMAIS hakaveret_shelanu ni chlomo_assouline. Si la connexion est expirée (session invalidée) : envoyer à Shlomo un lien COMPOSIO_MANAGE_CONNECTIONS (add, alias tovim_beyachad_v3) et s'arrêter.
- Supabase (Composio, SUPABASE_BETA_RUN_SQL_QUERY) : compte `supabase_restow-lise`, ref `xcrlfujevlvwmrswwvfq` (projet tovim-beyachad). Ne jamais toucher au projet de la ruche (ohvmnaymozoxfirkbntt).
- Site : dépôt GitHub `chlomo111-bit/tovim-beyachad` (add_repo access push puis git clone). Commits : user.name "chlomo111-bit", user.email "chlomo111-bit@users.noreply.github.com". Jeu en ligne : http://tovim.hakaveret.online
- Médias publiés depuis : https://raw.githubusercontent.com/chlomo111-bit/tovim-beyachad/main/media/AAAA-MM-JJ/...
- Voix des reels : Juniper (ElevenLabs, voice_id aMSt68OGf4xUZAnLpTU8, modèle Eleven v3, avec balises d'émotion). Shlomo génère et envoie le MP3.


## RÈGLES OBLIGATOIRES DE TOUS LES JEUX (Shlomo, 30.10.2026) — priment sur tout le reste
1. VIDÉO DU JOUR : chaque jour un reel qui raconte ce qui s'est passé dans le jeu (vrais joueurs tagués, vrais chiffres), terminé par « מה יקרה מחר? התגובה עם הכי הרבה לייקים קובעת ». AVANT d'écrire la vidéo : lire TOUS les commentaires du post/reel précédent ; le commentaire valable le plus liké décide de ce qui arrive. Texte écrit pour la voix (hébreu, balises Eleven v3, voix Juniper) envoyé à Shlomo 2–3 h avant la mise en ligne (SendUserMessage + PushNotification) : c'est la SEULE chose qu'on lui demande. Couverture dédiée, jamais une image noire. Mise en ligne 19:30 (texte envoyé à 17:00).
2. CHAQUE JOUR QUELQUE CHOSE D'EXTRAORDINAIRE dans le jeu (événement fou, surprise, nouveauté visible : `game_state` clé `event`, actualité `news`…), idéalement inspiré des commentaires ou de la boîte à idées, et raconté dans la vidéo.
3. LOTERIE 20 ₪ TOUS LES SOIRS À 20:00 — REMPLACE le billet caché (supprimé le 30.10.2026 : `CONFIG.BILLET.on=false`, `billets_unlocked()`=false). Un seul gagnant, payé par Shlomo par Bit. 2 conditions : (a) commenter le POST DU JOUR, (b) avoir récolté 200 pièces dans la journée (`coins_daily`). Pas de condition d'abonnement. Tirage EN DIRECT dans le jeu (`lottery_live()` : animation chez tous les joueurs connectés) ; la tâche « loterie » appelle aussi `run_lottery(date)` (idempotent), publie la story du résultat et écrit à Shlomo : gagnant + « 20 ₪ à payer par Bit ». Le naufrage (paliers 25, 100, 1 000…) reste l'objectif collectif et l'événement spectaculaire, mais ne débloque plus rien.
   - POST DU JOUR : créé CHAQUE MATIN (tâche « production du matin »), image 4:5 (1080×1350, vrais passagers, style du jeu) : hook + rappel des 2 conditions (« 🎟️ הגרלה על 20₪ הערב ב־20:00 · 💬 מגיבים כאן + 🪙 אוספים 200 מטבעות במשחק ») + « הגיבו כאן 👇 », mention légale, 5 hashtags. L'API ne permet pas d'épingler (ne pas embêter Shlomo avec ça). Enregistrer son id : `insert into billet_gate(day, post_id) values (<jour>, '<id>') on conflict (day) do update set post_id = excluded.post_id;`. Ne jamais l'oublier : chaque passage vérifie qu'il existe, sinon le crée.
   - Participants : à chaque passage, chaque commentateur du post du jour → `insert into billet_eligible(day, handle) values (<jour>, lower('<handle>')) on conflict do nothing;` (valide aussi la mission « הגיבו על הפוסט של היום »).
   - Jamais gagnants : tovim_beyachad, chlomo.assouline, the_noise_2026, hakaveret_shelanu, hasavta.shelanu (`lottery_excluded()`).
3 bis. « המגיב של היום » : à 20:00, `run_lottery` enregistre aussi le joueur qui a écrit le plus de commentaires valables dans la journée sur TOUS les posts du compte (`top_commenter_of(date)` depuis `ig_comment_log` ; textes identiques comptés une seule fois ; égalité = premier à atteindre ce nombre). Dans le jeu : couronne 👑 sur son personnage + étiquette « 👑 @x » jusqu'au tirage suivant (automatique via `lottery_state().crown`). Annoncé dans la story du résultat, tagué dans la vidéo du lendemain. Pas d'argent, un POUVOIR : il choisit une chose extraordinaire qui arrivera dans le jeu le lendemain, EN PLUS de l'événement prévu et du commentaire le plus liké. La tâche loterie répond à son dernier commentaire : « 👑 ניצחת! את/ה המגיב/ה של היום. מה יקרה מחר בספינה בזכותך? כתבו כאן עד 12:00 ». Sa réponse (commentaire sous le post du jour suivant, ou réponse) avant 12:00 le lendemain → `update lottery_draws set top_wish='<texte>', top_wish_status='pending' where day=<veille>;`, la réaliser dans le jeu (event/news/décor), puis `top_wish_status='done'`. Refuser ce qui est insultant, sexuel, vise une vraie personne ou est impossible (proposer une version proche ; `refused`). Raconter dans la vidéo : « @x החליט ש… ». Sans réponse avant 12:00 : rien de plus (`none`).
4. PASSAGES : 4 par jour, une seule tâche (5:55 / 11:55 / 16:55 / 19:55) — section « PASSAGE ».
5. SHABBAT : rien entre vendredi 16:00 et samedi 18:30 (heure d'Israël). Toute tâche qui se déclenche dans ce créneau s'arrête immédiatement sans rien faire. Loterie du vendredi : tirée samedi à 20:00 juste AVANT celle du samedi (`lottery_draw_at(vendredi)` = samedi 20:00 ; le jeu les enchaîne, vendredi d'abord). Le passage de samedi 19:55 enregistre aussi les commentateurs du post du vendredi dans billet_eligible (day = vendredi). Le post du jour du samedi = le reel publié à la sortie de Shabbat (18:30). La vidéo du vendredi sort samedi à 18:30 (texte envoyé à Shlomo le vendredi vers 10:30 pour qu'il enregistre avant Shabbat). Pas de production du matin le samedi ; les meilleurs commentateurs du vendredi et du samedi ont jusqu'à dimanche 12:00 pour leur vœu.
6. ÉCONOMIE : un passage sans nouveau commentaire ni rien à faire se termine immédiatement. Tâches programmées du jeu, une seule de chaque : « passages », « loterie 20:00 », « production du matin » (+ tâches ponctuelles de publication). Pas de doublon.

## Règles éditoriales
- Jamais de spam : 1 reel par jour maximum, 3 stories par jour maximum (« 5 דקות להגרלה » + résultat inclus), rien de dépassé, pas de doublon. Vérifier INSTAGRAM_GET_IG_USER_MEDIA / STORIES avant de publier.
- Toujours une vraie idée + un hook dès la 1re seconde / 1re ligne.
- Toujours les vrais joueurs (vrais @ de la table passengers) et les vrais chiffres. Jamais de faux joueurs ni de chiffres inventés.
- Textes en hébreu, humains et courts. Style visuel : Heebo 900, blanc + mots clés #FFC24B, carte bleu nuit bordée de jaune.
- Mention à la fin de toute description qui parle de la loterie : « המבצע אינו קשור לאינסטגרם ואינו ממומן על ידה. »
- 5 hashtags : #טובעים_ביחד #משחק #ספינה #זכייה #ישראל
- Argent : UNE loterie de 20 ₪ par soir à 20:00, rien d'autre. Ne plus jamais parler de billet caché ni de « השטרות נפתחים כשהסירה טובעת ».

## Règlement des commentaires (à appliquer à chaque passage)
1. Lire les commentaires de toutes les publications des 7 derniers jours (INSTAGRAM_GET_IG_USER_MEDIA puis INSTAGRAM_GET_IG_MEDIA_COMMENTS, champs id,text,from,timestamp,like_count,replies), en ignorant ceux de tovim_beyachad et ceux déjà dans `ig_seen_comments`.
1b. Journal « המגיב של היום » : chaque nouveau commentaire ou réponse d'un joueur → `insert into ig_comment_log(comment_id, handle, media_id, body, commented_at, valid) values ('<id>', lower('<handle>'), '<media>', '<texte>', '<timestamp>', <true|false>) on conflict do nothing;` (valid=false : insultant, sexuel, spam).
2. Tout commentateur devient passager VIP ⭐ (chlomo.assouline, the_noise_2026 et hakaveret_shelanu restent passagers simples) : `insert into passengers(handle, vip, joined_ship) values (lower('<handle>'), true, ship_index((select count(*) from passengers))) on conflict (handle) do update set vip = true;`
3. Bienvenue UNE SEULE FOIS par personne (si absent de `ig_welcomed`) : INSTAGRAM_POST_IG_COMMENT_REPLIES, court, en hébreu (« ברוך/ה הבא/ה לסיפון @x! 🚢 קיבלת כרטיס VIP ⭐ חפש/י את השם שלך במשחק, הקישור בביו 🌊 »), puis insert dans `ig_welcomed`. Insultant, haineux ou spam : ne pas répondre, ne pas l'ajouter.
3b. Répondre à TOUS les autres commentaires des joueurs : réponse courte, humaine, différente à chaque fois (jamais de copier-coller), qui relance (« 🎟️ עוד X מטבעות ואתם בהגרלה של 20:00 », « ומי עוד עולה? 👀 », « מה יקרה מחר? »). Pas d'URL → « הקישור בביו ». Une seule réponse par commentaire.
4. Marquer tous les commentaires traités : `insert into ig_seen_comments(comment_id, handle) values (...) on conflict do nothing;`
4b. Quand Shlomo envoie la liste de ses abonnés : ajouter chaque @ comme passager simple, `vip=false`, `on conflict do nothing`.
5. Palier de passagers atteint (25, 100, 1 000…) : le jeu fait couler le bateau tout seul (table sinks) : événement spectaculaire du jour, à mettre en avant dans la story et le reel.

## Fonctions communes à tous les jeux (V3, ordre du directeur des jeux validé par Shlomo le 29.10.2026)
SQL : `tools/supabase_v3.sql` (déjà appliqué en ligne). Dans le jeu : bouton 🎯 en bas à gauche (fiche « היום שלי »), pilule 🎟️ en haut, onglet 🏆 שיאים du panneau 💬.
- Monnaie unique : les pièces (מטבעות). `coins` (total + jour courant) et `coins_daily(handle, day, coins)` = historique par joueur et par jour (ramassage + bonus de missions).
- Loterie du jour (V4, `tools/supabase_v4_loterie.sql`, appliqué le 30.10.2026) : 200 pièces dans la journée + commentaire du post du jour (`billet_eligible`). Le joueur voit en permanence « 🪙 X/200 · 💬 ✓/✗ » et le compte à rebours ; à l'heure, le jeu lance le tirage en direct. Tables `lottery_draws` (day, winner, entrants, top_commenter, top_count, top_wish, top_wish_status) et `ig_comment_log`. Fonctions : `run_lottery(d)`, `lottery_live()`, `lottery_state(h)`, `lottery_eligible(d)`, `top_commenter_of(d)`, `lottery_draw_at(d)`. Le billet caché est désactivé (`billets_unlocked()` = false, `CONFIG.BILLET.on` = false) ; ses tables restent pour l'historique.
- Missions du jour : `missions_of(date)` tire 3 missions (1 facile : login/chat/idée · 1 pièces : 50/100/200 · 1 sociale : commenter le post du jour / amener un ami), mêmes pour tous, remise à zéro à minuit heure d'Israël. `missions_sync(h)` valide et crédite les bonus (table `mission_done`). La mission « commenter » se valide grâce à `billet_eligible` (étape 4c) : bien remplir cette table à CHAQUE passage.
- Boîte à idées : table `ideas` (200 caractères, 3 par jour, filtrée), privée (lecture uniquement par la routine).
- Chat public en direct (realtime) : 140 caractères, 1 message / 10 s, filtre `mod_check` (insultes, contenu sexuel, liens, téléphones, e-mails, invitations en privé). Aucun message privé entre joueurs (jeu ouvert aux jeunes) : ne JAMAIS ajouter de DM. 🚩 signaler ; masqué automatiquement à 3 signalements ; admin : `#admin` > 🚩.
- Statistiques : `my_stats(h)` (fiche « הסטטיסטיקות שלי ») et `global_stats()` (passagers, abonnés, restants avant le naufrage, pièces du jour). Les abonnés viennent de `game_state` clé `ig` (mis à jour le matin, voir ci-dessous).
- Classements : `leaderboard(h, 'today'|'all')` (top 10 + place du joueur).
- Requêtes utiles pour les textes : `select leaderboard('', 'today');` · `select global_stats();` · `select * from missions_of((now() at time zone 'Asia/Jerusalem')::date);`

## PRODUCTION DU MATIN (tâche 6:34, dimanche → vendredi)
1. Shabbat → stop. Lire les commentaires du dernier reel/post : le commentaire valable le plus liké = événement du jour (réalisable, sans risque : pas politique, pas haineux, pas de données perso). Lire `select * from lottery_draws order by day desc limit 2;` : gagnant d'hier (à taguer), meilleur commentateur d'hier et son vœu (jusqu'à 12:00 : le passage de 11:55 le réalise s'il arrive plus tard).
2. Boîte à idées : `select id, handle, body from ideas where status='new';` → s'il y a de BONNES idées, les résumer à Shlomo en UNE ligne (SendUserMessage) ; puis `update ideas set status='read' where status='new';`. Jamais réaliser une idée qui change les règles ou l'argent sans son accord.
3. ÉVÉNEMENT EXTRAORDINAIRE du jour : `insert into game_state(key,value) values ('event','{"type":"shark","title":"..."}') on conflict (key) do update set value=excluded.value, updated_at=now();` (types : none, storm, shark, iceberg, party, whale, kraken) + actualité `news` (titre court + 3–6 lignes). Varier chaque jour.
4. POST DU JOUR 4:5 (règle 3) publié vers 7:00, vrais passagers et vrai nombre restant avant le naufrage ; id dans billet_gate.
5. VIDÉO DU JOUR : texte voix (hébreu, 20–30 s, balises v3, hook fou, ce qui s'est passé avec les vrais @ : gagnant de la loterie, המגיב של היום et ce qu'il a décidé, l'événement, nouveaux passagers, compte à rebours du naufrage ; fin : « מה יקרה מחר? התגובה עם הכי הרבה לייקים קובעת ») dans media/AAAA-MM-JJ/voix.txt, puis send_later à 17:00 (vendredi : 10:30) pour l'envoyer à Shlomo avec les chiffres actualisés (SendUserMessage + PushNotification) en demandant le MP3 Juniper. Mise en ligne 19:30 (vendredi : samedi 18:30). Jamais de reel sans sa voix. Si un voix.txt ou un reel existe déjà pour le jour, ne rien refaire.
6. Abonnés → `game_state` clé `ig`. Modération du chat (comme dans le passage).

## PASSAGE (tâche 5:55 / 11:55 / 16:55 / 19:55)
1. Shabbat (vendredi ≥ 16:00 ou samedi < 18:30, heure d'Israël) → stop immédiat.
2. Règlement des commentaires (ci-dessus), y compris ig_comment_log et billet_eligible pour le post du jour (samedi 19:55 : aussi le post du vendredi, day = vendredi). Si AUCUN nouveau commentaire, que le post du jour existe et qu'il n'est pas 19:55 → stop.
3. Post du jour absent (billet_gate du jour vide) → le créer (samedi : le reel de 18:30 en tient lieu ; s'il manque, enregistrer le dernier post publié).
4. Vœu du meilleur commentateur d'hier (avant 12:00) : le repérer et le réaliser (règle 3 bis).
5. Abonnés : INSTAGRAM_GET_USER_INFO → `insert into game_state(key,value) values ('ig', jsonb_build_object('followers', <n>)) on conflict (key) do update set value=excluded.value, updated_at=now();`
6. Chat : `select id, handle, body, reports, hidden from messages where reports > 0 or created_at > now() - interval '8 hours' order by id desc limit 100;` → supprimer insultes/sexuel/coordonnées/invitations en privé ; remettre un message masqué à tort (`update messages set hidden=false, reports=0 where id=…; delete from chat_reports where message_id=…;`).
7. À 19:55 seulement : story « 5 דקות להגרלה! » (fond `tools/story_fond.py`, texte `tools/story_texte.py`) avec le vrai nombre de participants (`select lottery_state('')` → entrants), le meilleur commentateur du moment (top_now) et le rappel des 2 conditions + « ההגרלה בשידור חי במשחק · הקישור בביו ». Samedi : « 2 הגרלות הערב: שישי + שבת! ». Vendredi : pas de story (Shabbat).

## LOTERIE (tâche 20:01, dimanche → jeudi + samedi)
1. Vendredi → stop. `select run_lottery((now() at time zone 'Asia/Jerusalem')::date);` — samedi : d'abord `run_lottery(<vendredi>)`, puis celui du samedi. Idempotent : si le jeu a déjà tiré (`already`), utiliser ce résultat.
2. Story du résultat (une par tirage ; vérifier qu'elle n'est pas déjà en ligne) : « 🎉 הזוכה של הערב: @x · 20 ₪ 💸 » + « N משתתפים » + « 👑 המגיב של היום: @y – מה יקרה מחר בזכותך? » + « מחר הגרלה חדשה ב־20:00 ». Sans gagnant : « אף אחד לא עמד בשני התנאים… 😱 מחר הגרלה חדשה ».
3. Réponse au dernier commentaire du meilleur commentateur (« 👑 … מה יקרה מחר בספינה בזכותך? כתבו כאן עד 12:00 »).
4. Actualité `news` : gagnant + meilleur commentateur.
5. SendUserMessage + PushNotification à Shlomo : « Loterie <jour> : gagnant @x (N participants) → 20 ₪ à payer par Bit. Meilleur commentateur : @y ». Sans gagnant : une ligne.

## Reel (quand Shlomo envoie le MP3)
- Capture du vrai jeu avec `tools/reel_lancement.py` comme modèle (scènes, CAP, 1080×1920 30 i/s), musique `tools/musique_reel.py`, montage ffmpeg (H.264 -preset veryfast -crf 20, AAC), textes calés sur les pauses de la voix (ffmpeg silencedetect). Couverture dédiée (jamais noire).
- Description : mini-histoire du jour avec les vrais joueurs tagués, « יום N », « 🎟️ הגרלה על 20₪ כל ערב ב־20:00: מגיבים על הפוסט של היום + 200 מטבעות במשחק », « ומה יקרה מחר? התגובה עם הכי הרבה לייקים קובעת 👇 », mention légale, 5 hashtags. Puis commentaire CTA.

## Objectif n°1 : croissance (consigne de Shlomo, 28.10.2026)
Autonomie totale. Le but : un maximum d'abonnés, de commentaires et d'interactions, par tous les moyens HONNÊTES. Atout principal : une loterie de 20 ₪ chaque soir à 20:00, en direct dans le jeu, + la couronne du meilleur commentateur qui décide de la suite.
- Hooks : l'argent réel dès la 1re seconde (« משחק שמגריל 20₪ כל ערב 💸 », « @x זכה אתמול ב־20₪ »). Ne jamais écrire « le seul jeu » ni promettre plus de 20 ₪ par soir.
- Preuve sociale : chaque soir les vrais gagnants et le vrai המגיב של היום (@ tagués).
- Répondre à TOUS les commentaires des joueurs. Le commentaire le plus liké décide de l'événement du lendemain, le meilleur commentateur ajoute le sien : le rappeler partout.
- Parrainage : lien personnel du jeu (« הזמינו חבר = מגבעת 🎩, 3 חברים = אפוד זהב ») et compte à rebours avant le naufrage (« עוד X נוסעים »).
- INTERDIT (risque de blocage, contraire aux règles d'Instagram) : acheter des abonnés ou des likes, commenter ou envoyer des messages en masse sur d'autres comptes, faux comptes, faux gagnants, faux chiffres, demander de taguer des gens pour rien, toucher aux campagnes Meta Ads.
