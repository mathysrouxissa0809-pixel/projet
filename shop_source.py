"""Adaptateur de source AOTR.

Important : il n'existe pas, dans les sources publiques vérifiées pour ce projet,
d'API officielle documentée donnant le contenu de la boutique tournante en direct.
Ce module lit donc une URL JSON que tu configureras lorsqu'une source fiable sera
identifiée. Il refuse de publier des données inventées ou un exemple.
"""
import json
import os
import requests

TIMEOUT = 25

def _get_json(url):
    headers = {"User-Agent": "AOTR-Shop-Tracker/1.0"}
    token = os.getenv("AOTR_API_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    response = requests.get(url, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    return response.json()

def _extract_items(data):
    # Formats JSON courants : {"items":[...]}, {"shop":[...]},
    # ou {"data":{"items":[...]}}.
    if isinstance(data, list):
        raw = data
    elif isinstance(data, dict):
        raw = data.get("items") or data.get("shop")
        if raw is None and isinstance(data.get("data"), dict):
            raw = data["data"].get("items") or data["data"].get("shop")
    else:
        raw = None

    if not isinstance(raw, list):
        raise ValueError("Format JSON non reconnu : attendu une liste 'items' ou 'shop'.")

    items = []
    for entry in raw:
        if not isinstance(entry, dict):
            continue
        name = entry.get("name") or entry.get("title")
        if not name:
            continue
        item = {
            "name": str(name)[:256],
            "category": str(entry.get("category") or "Non précisée")[:100],
            "price": str(entry.get("price") or entry.get("cost") or "Non précisé")[:100],
            "rarity": str(entry.get("rarity") or "Non précisée")[:100],
            "image": entry.get("image") or entry.get("image_url") or "",
            "description": str(entry.get("description") or "")[:500],
        }
        items.append(item)

    # Ordre stable pour éviter de détecter un faux changement.
    return sorted(items, key=lambda x: (x["category"].lower(), x["name"].lower()))

def fetch_shop():
    url = os.getenv("AOTR_SHOP_JSON_URL", "").strip()
    if not url:
        raise RuntimeError(
            "AOTR_SHOP_JSON_URL n'est pas configurée. "
            "Il faut une source JSON fiable contenant la boutique en direct."
        )
    data = _get_json(url)
    return _extract_items(data)
