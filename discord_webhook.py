import time
import requests

COLOR_GOLD = 0xD6A84F

def _chunks(items, size=10):
    for i in range(0, len(items), size):
        yield items[i:i + size]

def _item_embed(item, index, total):
    fields = [
        {"name": "💰 Prix", "value": item["price"] or "Non précisé", "inline": True},
        {"name": "💎 Rareté", "value": item["rarity"] or "Non précisée", "inline": True},
        {"name": "📂 Catégorie", "value": item["category"] or "Non précisée", "inline": True},
    ]
    embed = {
        "title": f"🛒 {item['name']}"[:256],
        "description": item.get("description") or "Article de la rotation actuelle.",
        "color": COLOR_GOLD,
        "fields": fields,
        "footer": {"text": f"AOTR Shop Tracker • Article {index}/{total}"},
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    image = item.get("image", "")
    if image.startswith(("https://", "http://")):
        embed["image"] = {"url": image}
    return embed

def send_shop_embed(webhook_url, items):
    # Jusqu'à 10 embeds par message Discord. Chaque article a sa propre image.
    embeds = [_item_embed(item, i, len(items)) for i, item in enumerate(items, start=1)]
    for batch in _chunks(embeds, 10):
        response = requests.post(
            webhook_url,
            json={
                "username": "AOTR Shop Tracker",
                "content": "✨ **Nouvelle rotation de la boutique AOTR détectée !**",
                "embeds": batch,
            },
            timeout=25,
        )
        if response.status_code == 429:
            wait = float(response.json().get("retry_after", 2))
            time.sleep(min(wait, 15))
            response = requests.post(
                webhook_url,
                json={
                    "username": "AOTR Shop Tracker",
                    "content": "✨ **Nouvelle rotation de la boutique AOTR détectée !**",
                    "embeds": batch,
                },
                timeout=25,
            )
        response.raise_for_status()
