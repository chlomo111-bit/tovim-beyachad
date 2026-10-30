# Automatisations du jeu (sauvegarde du directeur des jeux, 30/10/2026 12:45)

Inventaire de toutes les tâches programmées actives de ce jeu avant remise à zéro.
Les textes complets des tâches restent consultables dans les tâches désactivées (même ID) ;
la logique détaillée est dans tools/ROUTINE.md.

Règles communes (30/10) : vidéo du jour (le commentaire le plus liké décide), un événement extraordinaire par jour,
loterie 20 ₪ à 20:00 (commentaire sur le post du jour + seuil de monnaie, pas d'abonnement obligatoire),
« המגיב של היום » (badge + pouvoir de choisir un événement le lendemain), passages 6:00 / 12:00 / 17:00 / 19:55,
Shabbat : rien de vendredi 16:00 à samedi 18:30, tout est décalé à samedi 18:30.

| ID | Nom | Horaire (heure d'Israël) | Rôle |
|---|---|---|---|
| trig_014C857RU18g7hJGWDL5GqVe | Bateau – production du matin | 6:34 dim.–ven. | Événement, post du jour, texte vidéo, send_later voix, reel 19:30 |
| trig_01BqmdaMTbTEuVF8eAqh3qe9 | Bateau – passages | 5:55 · 11:55 · 16:55 · 19:55 tous les jours (stop pendant Shabbat) | Réponses, VIP, billet_eligible, story 5 דקות להגרלה |
| trig_015neEiXpEe68YX9aEkV5eaw | Bateau – loterie 20:00 | 20:01 dim.–jeu. + sam. | run_lottery (+ vendredi le samedi), story, message Bit |
| trig_01HzAmnDasTC7t7ZuPaG4AfS | Bateau – story « The Noise arrive » | sam. 31/10 19:08 (ponctuel) | Story + news vers The Noise |

Seuil : 200 pièces (la loterie remplace l'ancien billet caché)

## Tâches du directeur qui touchent ce jeu
| ID | Nom | Horaire | Rôle |
|---|---|---|---|
| trig_01CKRu6aTLCyHxQjn1bZYJsZ | Jeux – passages du vendredi | ven. 7:50 · 13:50 | Déclenche ruche + savta |
| trig_016xihjQtAaUGjNW17P6RXG2 | Jeux – décaler Shabbat | ven. 15:45 | Décale les ponctuels à sam. 18:30 |
| trig_01SweqkEFqGvYW3p6ffWU83f | Jeux – rattrapage sortie de Shabbat | sam. 18:30 | Tirage du vendredi ruche + passages ruche/savta |
