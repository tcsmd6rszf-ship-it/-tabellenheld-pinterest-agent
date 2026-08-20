import json
from pathlib import Path


PRODUCT_FILE = Path("products.json")
HISTORY_FILE = Path("pin_history.json")


def load_products():
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


def create_pin_idea(product):
    title = product["title"]

    pin_title = f"{title} – praktische Tipps für deinen Alltag"

    description = (
        f"Entdecke {title} und lerne Excel Schritt für Schritt besser kennen. "
        "Verständliche Erklärungen, praktische Beispiele und hilfreiche Tipps "
        "für Einsteiger. Jetzt entdecken und mehr aus Excel herausholen."
    )

    return {
        "title": pin_title,
        "description": description,
        "shop_url": product["shop_url"]
    }


def main():
    products = load_products()
    history = load_history()

    print("================================")
    print("      TABELLENHELD PIN AGENT")
    print("================================")

    for product in products:

        pin = create_pin_idea(product)

        print()
        print("NEUER PIN")
        print("------------------------------")
        print("Titel:")
        print(pin["title"])
        print()
        print("Beschreibung:")
        print(pin["description"])
        print()
        print("Shop-Link:")
        print(pin["shop_url"])
        print("------------------------------")

    save_history(history)


if __name__ == "__main__":
    main()