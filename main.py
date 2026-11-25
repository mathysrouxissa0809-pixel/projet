import hashlib
import json
import os
import sys
from pathlib import Path

import requests

from shop_source import fetch_shop
from discord_webhook import send_shop_embed

STATE_FILE = Path("data/last_shop_hash.txt")

def canonical_hash(items):
    payload = json.dumps(items, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def main():
    webhook = os.getenv("DISCORD_WEBHOOK_URL", "").strip()
    if not webhook:
        raise RuntimeError("Secret DISCORD_WEBHOOK_URL manquant.")

    items = fetch_shop()
    if not items:
        raise RuntimeError(
            "La source a répondu, mais aucun article n'a été trouvé. "
            "Vérifie AOTR_SHOP_JSON_URL et le format JSON."
        )

    current_hash = canonical_hash(items)
    previous_hash = STATE_FILE.read_text().strip() if STATE_FILE.exists() else ""

    if current_hash == previous_hash:
        print(f"Boutique inchangée ({len(items)} articles). Aucun message envoyé.")
        return

    print(f"Nouvelle boutique détectée : {len(items)} articles.")
    send_shop_embed(webhook, items)

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(current_hash + "\n", encoding="utf-8")
    print("Publication Discord réussie et empreinte sauvegardée.")

if __name__ == "__main__":
    try:
        main()
    except (requests.RequestException, ValueError, RuntimeError) as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        raise
