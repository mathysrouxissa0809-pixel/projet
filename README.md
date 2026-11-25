# AOTR Shop Tracker

Tracker Python qui compare une boutique AOTR récupérée depuis une source JSON et envoie un embed Discord via webhook uniquement lorsqu'un changement est détecté.

## Attention : source des données

La rotation du Market AOTR est décrite comme ayant lieu toutes les 5 heures par le wiki communautaire. En revanche, ce dépôt ne prétend pas disposer d'une API officielle publique de la boutique en direct. Le programme attend donc une URL JSON fiable dans `AOTR_SHOP_JSON_URL`.

Le JSON doit ressembler à l'un de ces formats :

```json
{
  "items": [
    {
      "name": "Nom de l'article",
      "category": "Cosmetic",
      "price": "250 Gems",
      "rarity": "Epic",
      "image": "https://exemple.com/image.png",
      "description": "Description facultative"
    }
  ]
}
```

ou simplement une liste JSON d'articles. Les champs `name` (ou `title`) sont nécessaires. Les autres sont facultatifs.

**Ne mets pas une URL supposée au hasard.** Si aucune source JSON publique fiable n'est disponible, il faudra identifier une source autorisée avant que la récupération automatique puisse fonctionner. Le script s'arrête sans publier de faux articles.

## Installation

1. Crée un dépôt GitHub nommé `AOTR-Shop-Tracker`.
2. Envoie tous les fichiers de ce dossier dans le dépôt.
3. Dans Discord, crée un webhook pour le salon voulu : Paramètres du salon → Intégrations → Webhooks → Nouveau webhook → Copier l'URL.
4. Dans GitHub, ouvre Settings → Secrets and variables → Actions.
5. Dans **Secrets**, ajoute :
   - `DISCORD_WEBHOOK_URL` : URL du webhook Discord.
   - `AOTR_API_TOKEN` : seulement si la source JSON exige un jeton (sinon inutile).
6. Dans **Variables**, ajoute :
   - `AOTR_SHOP_JSON_URL` : URL de la source JSON fiable.
7. Ouvre l'onglet Actions et autorise les workflows si GitHub le demande.
8. Lance `AOTR Shop Tracker` → Run workflow pour tester.

## Automatisation

Le workflow vérifie toutes les 5 heures selon le cron UTC de GitHub Actions. GitHub peut décaler légèrement le démarrage d'une tâche planifiée. Le workflow peut aussi être lancé manuellement.

## Sécurité

- Ne publie jamais l'URL du webhook dans le dépôt.
- Ne colle jamais un token ou un mot de passe dans le code.
- Si le webhook est exposé, supprime-le et recrée-en un.
- Le workflow n'utilise pas de cookie Roblox ni de mot de passe de compte.

## Limites actuelles

- Les champs d'image, prix et rareté ne seront présents que si la source les fournit.
- Le hash est stocké dans `data/last_shop_hash.txt` et sauvegardé par le workflow.
- Une première exécution publie la boutique trouvée, puis les suivantes publient uniquement si le contenu change.
