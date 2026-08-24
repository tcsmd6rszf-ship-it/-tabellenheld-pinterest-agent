import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PRODUCT_FILE = Path("products.json")
HISTORY_FILE = Path("pin_history.json")
OUTPUT_DIR = Path("generated_pins")


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
        f"Du möchtest Excel besser verstehen? {title} zeigt dir verständlich und praxisnah, wie du Excel sicherer einsetzen kannst.",
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


def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]

    for path in paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def create_image(pin, filename):
    width = 1000
    height = 1500

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    title_font = get_font(62, True)
    subtitle_font = get_font(42, False)
    small_font = get_font(30, False)

    # Kopfbereich
    draw.rectangle((0, 0, width, 300), fill=(25, 35, 45))

    draw.text(
        (70, 65),
        "TABELLENHELD",
        font=get_font(48, True),
        fill="white"
    )

    draw.text(
        (70, 150),
        "Excel • Vorlagen • Ratgeber",
        font=small_font,
        fill="white"
    )

    # Haupttitel
    title = pin["title"]

    words = title.split()
    lines = []
    current = ""

    for word in words:
        test = current + " " + word if current else word

        if draw.textbbox((0, 0), test, font=title_font)[2] <= 860:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    y = 430

    for line in lines[:5]:
        draw.text(
            (70, y),
            line,
            font=title_font,
            fill=(25, 35, 45)
        )
        y += 85

    # Trennlinie
    draw.rectangle((70, y + 40, 930, y + 48), fill=(25, 35, 45))

    # Hinweis
    draw.text(
        (70, y + 100),
        "Jetzt Excel einfacher verstehen",
        font=subtitle_font,
        fill=(55, 65, 75)
    )

    # Call-to-Action
    draw.rounded_rectangle(
        (70, 1180, 930, 1310),
        radius=30,
        fill=(25, 35, 45)
    )

    draw.text(
        (250, 1215),
        "JETZT ENTDECKEN",
        font=get_font(42, True),
        fill="white"
    )

    # URL
    draw.text(
        (70, 1380),
        pin["shop_url"],
        font=small_font,
        fill=(70, 70, 70)
    )

    image.save(filename, "PNG")


def main():
    products = load_products()
    history = load_history()

    OUTPUT_DIR.mkdir(exist_ok=True)

    print("================================")
    print("     TABELLENHELD PIN AGENT")
    print("================================")

    for product in products:

        pin_number = len(history)

        pin = create_pin(product, pin_number)

        filename = OUTPUT_DIR / f"pin_{pin_number + 1}.png"

        create_image(pin, filename)

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
        print()
        print("Bild:")
        print(filename)
        print("------------------------------")

        history.append({
            **pin,
            "image": str(filename)
        })

    save_history(history)

    print()
    print("Bild erfolgreich erstellt.")
    print("Pin-Verlauf gespeichert.")


if __name__ == "__main__":
    main()