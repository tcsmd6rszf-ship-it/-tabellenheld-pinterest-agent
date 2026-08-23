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

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return data.get("pins", [])

        return data

    except Exception:
        return []


def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=2)


def create_pin(product, number):
    title = product["title"]
    shop_url = product["shop_url"]

    ideas = [
        f"{title} – einfach erklärt für Einsteiger",
        f"{title} – 7 Tipps, die du kennen solltest",
        f"{title} – Excel endlich richtig verstehen",
        f"{title} – praktische Hilfe für deinen Excel-Alltag",
        f"{title} – von der ersten Tabelle bis zur Auswertung",
        f"{title} – Excel Schritt für Schritt lernen",
        f"{title} – mehr Sicherheit bei Excel",
        f"{title} – praktische Excel-Tipps für Anfänger",
        f"{title} – so wirst du sicherer in Excel",
        f"{title} – dein praktischer Excel-Ratgeber"
    ]

    descriptions = [
        f"Du möchtest Excel besser verstehen? {title} zeigt dir verständlich und praxisnah, wie du Excel sicherer einsetzen kannst. Entdecke den Ratgeber jetzt.",
        f"Excel muss nicht kompliziert sein. Mit {title} lernst du wichtige Grundlagen und praktische Anwendungen Schritt für Schritt kennen.",
        f"Mehr Sicherheit in Excel: {title} erklärt wichtige Funktionen, Tabellen und praktische Beispiele verständlich und übersichtlich.",
        f"Du möchtest mehr aus Excel herausholen? Entdecke {title} und lerne Excel mit verständlichen Erklärungen und praktischen Beispielen.",
        f"Der praktische Einstieg in Excel: {title} hilft dir dabei, Tabellen, Formeln und Auswertungen besser zu verstehen."
    ]

    return {
        "title": ideas[number % len(ideas)],
        "description": descriptions[number % len(descriptions)],
        "shop_url": shop_url
    }


def main():
    products = load_products()
    history = load_history()

    print("================================")
    print("     TABELLENHELD PIN AGENT")
    print("================================")

    new_pins = []

    for product in products:
        pin_number = len(history)

        pin = create_pin(product, pin_number)

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

        new_pins.append(pin)
        history.append(pin)

    save_history(history)

    print()
    print(f"{len(new_pins)} Pin-Idee(n) erstellt.")
    print("Pin-Verlauf gespeichert.")


if __name__ == "__main__":
    main()