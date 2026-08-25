import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PRODUCT_FILE = Path("products.json")
HISTORY_FILE = Path("pin_history.json")
OUTPUT_DIR = Path("generated_pins")


PRODUCT_THEMES = {
    "Life, Family & Social Media Organizer": {
        "topics": [
            "Familienplanung leicht gemacht",
            "Mehr Ordnung im Familienalltag",
            "Wochenplanung für die ganze Familie",
            "Social Media besser organisieren",
            "Mehr Zeit durch gute Planung"
        ],
        "tagline": "Dein Alltag. Deine Planung. Deine Übersicht."
    },

    "Business & Handwerker-Paket": {
        "topics": [
            "Aufträge übersichtlich organisieren",
            "Mehr Ordnung im Arbeitsalltag",
            "Kunden und Projekte im Blick behalten",
            "Effizienter planen im Handwerk",
            "Business einfach organisieren"
        ],
        "tagline": "Mehr Übersicht. Weniger Chaos. Mehr Zeit."
    },

    "Excel-Wissens-Paket": {
        "topics": [
            "Excel endlich verstehen",
            "5 Excel-Tipps für Einsteiger",
            "Formeln einfach erklärt",
            "Excel-Tabellen richtig aufbauen",
            "Mehr aus Excel herausholen"
        ],
        "tagline": "Excel verstehen. Sicher anwenden."
    },

    "Ultimate Planning & Life Bundle": {
        "topics": [
            "Deine Ziele endlich planen",
            "Mehr Struktur im Alltag",
            "Monatsplanung leicht gemacht",
            "Gewohnheiten und Ziele im Blick",
            "Das Leben besser organisieren"
        ],
        "tagline": "Plane dein Leben. Erreiche deine Ziele."
    },

    "Business & Freelancer Starter-Kit": {
        "topics": [
            "Selbstständig besser organisiert",
            "Kunden und Projekte im Griff",
            "Freelancer-Aufgaben clever planen",
            "Mehr Struktur im Business",
            "Business-Organisation leicht gemacht"
        ],
        "tagline": "Starte organisiert. Arbeite professionell."
    },

    "Excel Masterclass & Templates Bundle": {
        "topics": [
            "Excel professionell nutzen",
            "Praktische Excel-Vorlagen",
            "Excel im Business effizient einsetzen",
            "Mehr Produktivität mit Excel",
            "Excel-Funktionen clever nutzen"
        ],
        "tagline": "Mehr Wissen. Mehr Vorlagen. Mehr Excel."
    }
}


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


def find_theme(product_title):
    for key, theme in PRODUCT_THEMES.items():
        if key.lower() in product_title.lower():
            return theme

    return {
        "topics": [
            "Mehr Ordnung und Übersicht im Alltag",
            "Praktische Tipps für deine Planung",
            "Einfacher organisieren und mehr erreichen"
        ],
        "tagline": "Einfach besser organisiert."
    }


def create_pin(product, number):
    title = product["title"]
    shop_url = product["shop_url"]

    theme = find_theme(title)
    topics = theme["topics"]

    topic = topics[number % len(topics)]

    pin_title = f"{topic} | {title}"

    description = (
        f"{topic}: Entdecke {title} und bringe mehr Struktur, Übersicht "
        f"und Effizienz in deinen Alltag. Praktische Lösungen, hilfreiche "
        f"Vorlagen und verständliche Planung für mehr Ordnung. "
        f"Jetzt entdecken."
    )

    return {
        "title": pin_title,
        "description": description,
        "shop_url": shop_url,
        "topic": topic,
        "tagline": theme["tagline"]
    }


def get_font(size, bold=False):
    font_path = (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold
        else
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )

    if Path(font_path).exists():
        return ImageFont.truetype(font_path, size)

    return ImageFont.load_default()


def create_image(pin, filename, product_number):
    width = 1000
    height = 1500

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    title_font = get_font(58, True)
    subtitle_font = get_font(40, False)
    small_font = get_font(28, False)
    logo_font = get_font(48, True)

    # Kopfbereich
    draw.rectangle(
        (0, 0, width, 300),
        fill=(25, 35, 45)
    )

    draw.text(
        (65, 60),
        "TABELLENHELD",
        font=logo_font,
        fill="white"
    )

    draw.text(
        (65, 145),
        "ORGANISATION • EXCEL • BUSINESS",
        font=small_font,
        fill="white"
    )

    # Produktnummer
    draw.text(
        (800, 70),
        f"#{product_number}",
        font=small_font,
        fill="white"
    )

    # Titel
    title = pin["topic"]

    words = title.split()
    lines = []
    current = ""

    for word in words:
        test = current + " " + word if current else word

        if draw.textbbox(
            (0, 0),
            test,
            font=title_font
        )[2] <= 850:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    y = 450

    for line in lines[:5]:
        draw.text(
            (70, y),
            line,
            font=title_font,
            fill=(25, 35, 45)
        )
        y += 85

    # Trennlinie
    draw.rectangle(
        (70, y + 35, 930, y + 43),
        fill=(25, 35, 45)
    )

    # Produktname
    product_name = pin["title"].split("|")[-1].strip()

    words = product_name.split()
    lines = []
    current = ""

    for word in words:
        test = current + " " + word if current else word

        if draw.textbbox(
            (0, 0),
            test,
            font=subtitle_font
        )[2] <= 850:
            current = test
        else:
            lines.append(current)
            current = word

    if current:
        lines.append(current)

    y += 100

    for line in lines[:4]:
        draw.text(
            (70, y),
            line,
            font=subtitle_font,
            fill=(70, 80, 90)
        )
        y += 58

    # Claim
    draw.text(
        (70, 900),
        pin["tagline"],
        font=subtitle_font,
        fill=(25, 35, 45)
    )

    # CTA
    draw.rounded_rectangle(
        (70, 1130, 930, 1260),
        radius=30,
        fill=(25, 35, 45)
    )

    draw.text(
        (260, 1165),
        "JETZT ENTDECKEN",
        font=get_font(40, True),
        fill="white"
    )

    # Shop-Link
    draw.text(
        (70, 1365),
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

    for index, product in enumerate(products, start=1):

        pin_number = len(history)

        pin = create_pin(product, pin_number)

        filename = OUTPUT_DIR / f"pin_{pin_number + 1}.png"

        create_image(
            pin,
            filename,
            index
        )

        print()
        print("NEUER PIN")
        print("------------------------------")
        print("Produkt:")
        print(product["title"])
        print()
        print("Thema:")
        print(pin["topic"])
        print()
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
            "product": product["title"],
            "image": str(filename)
        })

    save_history(history)

    print()
    print(f"{len(products)} Produkte verarbeitet.")
    print("Neue Pin-Ideen und Bilder erstellt.")
    print("Pin-Verlauf gespeichert.")


if __name__ == "__main__":
    main()