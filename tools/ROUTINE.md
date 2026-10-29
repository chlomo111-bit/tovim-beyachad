# Routine autonome — טובעים ביחד (@tovim_beyachad)

Shlomo a donné l'autonomie complète le 28.10.2026 : stories, reels, réponses de bienvenue et gestion des passagers, SANS lui demander de confirmation. La SEULE chose qu'on lui demande : l'enregistrement vocal (MP3 ElevenLabs) des reels. Le prévenir uniquement en cas de problème grave (connexion cassée, mauvais compte, publication impossible), en français, en une phrase.

## RÈGLE INSTAGRAM OBLIGATOIRE (Shlomo, 28.10.2026)
- Pour TOUTE action Instagram via Composio (publier, lire les commentaires, répondre, statistiques) : passer `account: "instagram_odoom-cither"` dans CHAQUE appel. Ne JAMAIS utiliser le compte par défaut ni un autre compte (hakaveret_shelanu, chlomo_assouline…).
- Juste avant CHAQUE publication (post, story, reel, commentaire) : INSTAGRAM_GET_USER_INFO (ig_user_id "me", account instagram_odoom-cither) et vérifier que username = tovim_beyachad. Sinon : NE RIEN PUBLIER et prévenir Shlomo immédiatement (SendUserMessage + PushNotification).

## Identifiants
- Instagram (Composio) : compte `instagram_odoom-cither` UNIQUEMENT (username tovim_beyachad, ig_user_id `39487392790907301`). Vérifier le username avant toute action. JAMAIS hakaveret_shelanu ni chlomo_assouline. Si la connexion est expirée (session invalidée) : envoyer à Shlomo un lien COMPOSIO_MANAGE_CONNECTIONS (add, alias tovim_beyachad_v3) et s'arrêter.
- Supabase (Composio, SUPABASE_BETA_RUN_SQL_QUERY) : compte `supabase_restow-lise`, ref `xcrlfujevlvwmrswwvfq` (projet tovim-beyachad). Ne jamais toucher au projet de la ruche (ohvmnaymozoxfirkbntt).
- Site : dépôt GitHub `chlomo111-bit/tovim-beyachad` (add_repo access push puis git clone). Commits : user.name "chlomo111-bit", user.email "chlomo111-bit@users.noreply.github.com". Jeu en ligne : http://tovim.hakaveret.online
- Médias publiés depuis : https://raw.githubusercontent.com/chlomo111-bit/tovim-beyachad/main/media/AAAA-MM-JJ/...
- Voix des reels : Juniper (ElevenLabs, voice_id aMSt68OGf4xUZAnLpTU8, modèle Eleven v3, avec balises d'émotion). Shlomo génère et envoie le MP3.

## Règles éditoriales (les plus importantes)
- Jamais de spam : 1 reel par jour maximum, 2 à 3 stories par jour maximum, rien de dépassé, pas de doublon. Dans le doute, ne pas publier. Vérifier INSTAGRAM_GET_IG_USER_MEDIA / STORIES avant de publier.
- Toujours une vraie idée + un hook dès la 1re seconde / 1re ligne.
- Toujours les vrais joueurs (vrais @ de la table passengers) et les vrais chiffres. Jamais de faux joueurs ni de chiffres inventés.
- Textes en hébreu, humains et courts. Style visuel : Heebo 900, blanc + mots clés #FFC24B, carte bleu nuit bordée de jaune.
- Mention à la fin de toute description qui parle des billets : « המבצע אינו קשור לאינסטגרם ואינו ממומן על ידה. »
- 5 hashtags : #טובעים_ביחד #משחק #ספינה #זכייה #ישראל
- Billets (règle du 28.10.2026) : 3 billets de 20 ₪ par jour (60 ₪/jour), DÉBLOQUÉS SEULEMENT après le premier naufrage (25 passagers). Avant : le jeu affiche « 🔒 נפתחים כשהסירה טובעת · עוד X נוסעים ». Toujours le dire ainsi dans les textes (« השטרות נפתחים כשהסירה טובעת »). Jamais d'autres montants promis. Le billet est caché dans un coin éloigné du bateau, jamais sur un passager.

## Règlement des commentaires (à appliquer à chaque passage)
1. Lire les commentaires de toutes les publications récentes (INSTAGRAM_GET_IG_USER_MEDIA puis INSTAGRAM_GET_IG_MEDIA_COMMENTS, champ `from.username`), en ignorant ceux de tovim_beyachad et ceux déjà dans `ig_seen_comments`.
2. Tout commentateur devient passager VIP ⭐ (chlomo.assouline, the_noise_2026 et hakaveret_shelanu sont passagers simples, ajoutés par Shlomo le 29.10 : ne pas les passer VIP) : `insert into passengers(handle, vip, joined_ship) values (lower('<handle>'), true, ship_index((select count(*) from passengers))) on conflict (handle) do update set vip = true;`
3. Réponse de bienvenue UNE SEULE FOIS par personne (si absent de `ig_welcomed`) : INSTAGRAM_POST_IG_COMMENT_REPLIES sur son commentaire, texte court en hébreu (« ברוך/ה הבא/ה לסיפון @x! 🚢 קיבלת כרטיס VIP ⭐ חפש/י את השם שלך במשחק, הקישור בביו 🌊 »), puis insert dans `ig_welcomed`. Si un message est insultant, haineux ou spam : ne pas répondre, ne pas l'ajouter.
3b. Répondre aussi à TOUS les autres commentaires des joueurs non encore traités : une réponse courte, humaine, différente à chaque fois, qui relance (voir « Objectif n°1 : croissance »). Une seule réponse par commentaire.
3c. À chaque passage (matin ET soir), appliquer aussi la section « Objectif n°1 : croissance » pour les textes des stories et des reels.
4. Marquer tous les commentaires traités : `insert into ig_seen_comments(comment_id, handle) values (...) on conflict do nothing;`
4b. Quand Shlomo envoie la liste de ses abonnés : ajouter chaque @ (sans le nom) comme passager simple, `vip=false`, `on conflict do nothing`.
5. Si le nombre de passagers atteint un palier (25, 100, 1 000…), le jeu fait couler le bateau tout seul (table sinks) : c'est l'événement du jour, à mettre en avant dans la story et le reel.

## Le matin (tâche 08:00)
1. Passage commentaires (règlement ci-dessus).
2. Événement du jour : le commentaire le plus liké d'hier sous le reel, s'il est réalisable et sans risque (pas politique, pas haineux, pas de données perso) → `admin_set_event` n'est pas utilisable sans mot de passe : faire `insert into game_state(key,value) values ('event','{"type":"shark","title":"..."}') on conflict (key) do update set value=excluded.value, updated_at=now();` (types : none, storm, shark, iceberg, party, whale, kraken). Sinon en choisir un soi-même pour varier.
3. Story 09:00 : fond avec `tools/story_fond.py` (vrais passagers depuis Supabase), texte avec `tools/story_texte.py` : « עוד X נוסעים והסירה טובעת » + « 💸 3 שטרות של 20₪ היום », lien en bio. Pousser dans media/AAAA-MM-JJ/, publier (media_type STORIES).
4. Préparer le reel du soir « יום N » (N = jours depuis le 28.10.2026, +1) : écrire le texte voix (hébreu, 20–30 s, balises d'émotion v3, hook fou au début, événement révélé à la fin, CTA « כתבו "עולה" ») l'enregistrer dans media/AAAA-MM-JJ/voix.txt, mais NE PAS l'envoyer le matin : programmer (send_later) l'envoi à Shlomo à 17:00, soit 2 à 3 heures avant la mise en ligne de 19:30 (SendUserMessage + PushNotification, chiffres actualisés), en lui demandant le MP3 Juniper. C'est la SEULE chose qu'on lui demande (consigne du 29.10.2026) ; tout le reste (programmations, montage, publication) se fait sans lui demander. Ne jamais publier un reel sans sa voix.

## Le soir (tâche 19:00)
1. Passage commentaires.
2. Gagnants des billets du jour : `select slot, handle, found_at from treasure_wins where day=(now() at time zone 'Asia/Jerusalem')::date order by slot;`
3. Story du soir : gagnants (« 🏆 היום זכו: @… ») ou « 😱 שטר לא נמצא… מחר 3 שטרות חדשים », + nouveaux passagers du jour. Publier.
4. Ajouter une actualité dans le jeu si quelque chose de neuf : `insert into news(title, body) values (...)`.

## Reel (quand Shlomo envoie le MP3)
- Capture du vrai jeu avec `tools/reel_lancement.py` comme modèle (scènes, CAP, 1080×1920 30 i/s), musique `tools/musique_reel.py`, montage ffmpeg (H.264 -preset veryfast -crf 20, AAC), caler les textes sur les pauses de la voix (ffmpeg silencedetect).
- Description en mini-histoire du jour avec les vrais joueurs tagués, « יום N », CTA « כתבו "עולה" 👇 », « ומה יקרה מחר? התגובה עם הכי הרבה לייקים קובעת 👇 », mention légale, 5 hashtags. Puis commentaire CTA.

## Objectif n°1 : croissance (consigne de Shlomo, 28.10.2026)
Autonomie totale. Le but : un maximum d'abonnés, de commentaires et d'interactions, par tous les moyens HONNÊTES. Atout principal : le jeu fait gagner de l'argent réel (3 billets de 20 ₪ = 60 ₪/jour) dès que la barque a coulé : chaque nouveau passager rapproche le déblocage, c'est le moteur du parrainage.
- Hooks : mettre l'argent réel en avant dès la 1re seconde (« משחק שמחלק כסף אמיתי כל יום 💸 », « מישהו לקח 20₪ תוך 3 דקות »). Ne jamais écrire « le seul jeu » ni promettre plus que 3×20 ₪/jour.
- Preuve sociale : chaque soir, montrer les vrais gagnants (@ tagués) ; plus les gens voient que d'autres gagnent, plus ils jouent.
- Répondre à TOUS les commentaires des joueurs (pas seulement la bienvenue) : réponse courte, humaine, différente à chaque fois, qui pose une question ou relance (« ומי עוד עולה? 👀 »). Une seule réponse par commentaire.
- Le commentaire le plus liké décide de l'événement du lendemain : le rappeler dans chaque reel et chaque description.
- Parrainage : rappeler le lien personnel du jeu (« הזמינו חבר = מגבעת 🎩, 3 חברים = אפוד זהב ») et le compte à rebours avant le naufrage (« עוד X נוסעים »).
- Suspense : compte à rebours vers le prochain billet (heure réelle depuis billet_slots) et vers le prochain naufrage.
- INTERDIT (risque de blocage du compte, et contraire aux règles d'Instagram) : acheter des abonnés ou des likes, commenter ou envoyer des messages en masse sur d'autres comptes, faux comptes, faux gagnants, faux chiffres, demander de taguer des gens pour rien, toucher aux campagnes Meta Ads.

## Le midi (tâche 14:00)
1. Passage commentaires + réponse à tous les nouveaux commentaires des joueurs.
2. Story de l'après-midi (si moins de 2 stories publiées aujourd'hui) : compte à rebours vers le prochain billet (heure réelle depuis billet_slots) OU nouveaux passagers du jour, avec un hook argent.
