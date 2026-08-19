import json
from pathlib import Path


PRODUCT_FILE = Path("products.json")
HISTORY_FILE = Path("pin_history.json")


def load_products():
    if not PRODUCT_FILE.exists():
        print("Keine products.json gefunden.")
        return []

    with open(PRODUCT_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def load_history():
    if not HISTORY_FILE.exists():
        return []

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


def main():
    products = load_products()
    history = load_history()

    print("================================")
    print("      TABELLENHELD PIN AGENT")
    print("================================")
    print()

    print(f"Produkte gefunden: {len(products)}")
    print(f"Bisherige Pins: {len(history)}")
    print()

    for product in products:
        title = product.get("title", "Unbekanntes Produkt")

        print("Produkt:", title)
        print("→ Pin-Idee wird vorbereitet")
        print("→ Beschreibung wird vorbereitet")
        print("→ Bild wird vorbereitet")
        print()

    save_history(history)

    print("Agent erfolgreich ausgeführt.")


if __name__ == "__main__":
    main()