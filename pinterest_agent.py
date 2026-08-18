import os
import json
import requests
from pathlib import Path

PINTEREST_API = "https://api.pinterest.com/v5"

ACCESS_TOKEN = os.environ.get("PINTEREST_ACCESS_TOKEN")
BOARD_ID = os.environ.get("PINTEREST_BOARD_ID")


def load_products():
    file = Path("products.json")

    if not file.exists():
        print("FEHLER: products.json wurde nicht gefunden.")
        return []

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def create_pin(product):
    if not ACCESS_TOKEN:
        raise RuntimeError("PINTEREST_ACCESS_TOKEN fehlt.")

    if not BOARD_ID:
        raise RuntimeError("PINTEREST_BOARD_ID fehlt.")

    title = product["title"]
    description = product["description"]
    shop_url = product["shop_url"]
    image_url = product["image_url"]

    payload = {
        "title": title[:100],
        "description": description[:800],
        "link": shop_url,
        "board_id": BOARD_ID,
        "media_source": {
            "source_type": "image_url",
            "url": image_url,
            "is_standard": True
        }
    }

    response = requests.post(
        f"{PINTEREST_API}/pins",
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=60
    )

    if response.status_code not in (200, 201):
        print("Pinterest-Fehler:")
        print(response.status_code)
        print(response.text)
        return False

    result = response.json()

    print("PIN ERFOLGREICH ERSTELLT")
    print("Pin-ID:", result.get("id"))

    return True


def main():
    products = load_products()

    if not products:
        print("Keine Produkte vorhanden.")
        return

    for product in products:
        print()
        print("Verarbeite:", product.get("title"))

        try:
            create_pin(product)
        except Exception as error:
            print("Fehler:", error)


if __name__ == "__main__":
    main()