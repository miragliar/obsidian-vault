"""
Erzeugt eine anonymisierte Variante des Verkaufsauftrags ORD0001560.
Alle personen-, firmen- und kontoidentifizierenden Angaben sind durch
Musterwerte ersetzt. Layout ist an das Original (Object Carpet) angelehnt,
aber bewusst neutral gehalten.
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.pdfbase.pdfmetrics import stringWidth

OUT = (
    "/Users/raouleliasmiraglia/Library/CloudStorage/Dropbox/"
    "Miraglia-BI/0_Internal/Obsidian Raoul/50.work/anonymisierte-beispiele/"
    "Verkaufsauftrag-MUSTER-ORD9999999.pdf"
)

# ---------- Muster-Daten ---------------------------------------------------
LIEFERANT = {
    "name": "MUSTER CARPET GmbH",
    "strasse": "Musterstraße 1",
    "plz_ort": "D 12345 Musterstadt",
    "tel": "+49 711 0000-0",
    "mail": "info@muster-carpet.de",
    "gf": "Max Mustermann, Erika Musterfrau",
    "hrb": "HRB 999999",
    "vat": "DE999999999",
    "bank1": ("Musterbank 1", "DE99 9999 9999 9999 9999 99", "MUSTER1XXX"),
    "bank2": ("Musterbank 2", "DE88 8888 8888 8888 8888 88", "MUSTER2XXX"),
    "agb": "http://www.muster-carpet.de/agb",
}

KUNDE = {
    "firma": "MUSTERCARPETS",
    "zusatz": "Teppich Muster GmbH & Co. KG",
    "strasse": "Beispielstr. 99",
    "plz_ort": "12345 Musterstadt",
    "land": "DEUTSCHLAND",
    "kd_nr": "1000001",
    "datum": "28. Mai 2026",
    "innendienst": "Maria Mustermann",
    "innen_tel": "+49 711 0000 999",
    "innen_mail": "maria.mustermann@\nmuster-carpet.de",
    "gebiet": "999",
    "aussendienst": "Tom Musterfrau",
}

AUFTRAG = {
    "kommission": "Musterprojekt",
    "debitor": "1000001",
    "auftragsnr": "ORD9999999",
    "fracht": "DE, Frei Haus abgeladen ; BEARB.H 4",
    "info_frachtbrief": "",
    "warenausgang": "",
    "liefertermin": "Siehe Text unten",
    "ihr_zeichen": "",
    "gewicht": "4,30",
}

POSITIONEN = [
    {
        "pos": "1",
        "art_nr": "FXG0760-100",
        "name": "FLOW x GLOW 760",
        "typ": "RUGX, Einzelteppich",
        "wztnr": "57032999",
        "menge": "1,00 Stück  1,00 Stück",
        "specs": [
            ("LÄNGE",      "250 cm"),
            ("BREITE",     "270 cm"),
            ("FORM",       "Rechteck"),
            ("RÜCKEN",     "BlackThermo®Filz Akustik Plus mit\nRutschhemmung"),
            ("EINFASSUNG", "Protect-L"),
            ("EINF-BREIT", "3,0 cm"),
            ("EINF-FARBE", "P 4308"),
        ],
    },
    {
        "pos": "2",
        "art_nr": "FXG0760-100",
        "name": "FLOW x GLOW 760",
        "typ": "RUGX, Einzelteppich",
        "wztnr": "57032999",
        "menge": "1,00 Stück  1,00 Stück",
        "specs": [
            ("LÄNGE",      "170 cm"),
            ("BREITE",     "240 cm"),
            ("FORM",       "Rechteck"),
            ("RÜCKEN",     "BlackThermo®Filz Akustik Plus mit\nRutschhemmung"),
            ("EINFASSUNG", "Protect-L"),
            ("EINF-BREIT", "3,0 cm"),
            ("EINF-FARBE", "P 4308"),
        ],
    },
]

FUSSTEXT = [
    "Als voraussichtlichen Liefertermin haben wir die KW 27 vorgesehen.",
    "",
    "Aus produktionstechnischen Gründen kann es Größenabweichungen der RUGX Teppiche",
    "bis zu 3 cm geben.",
    "",
    "Gestalten Sie Ihren Teppich noch schneller, rund um die Uhr, im Büro oder unterwegs.",
    "Der RUGX-Konfigurator – Ihr Vertriebs- und Beratungstool – www.muster-carpet.de/konfigurator.",
]

# ---------- Zeichnen -------------------------------------------------------

PAGE_W, PAGE_H = A4
LEFT  = 2.0 * cm
RIGHT = PAGE_W - 2.0 * cm
TOP   = PAGE_H - 2.0 * cm

LABEL_FONT = "Helvetica"
BOLD       = "Helvetica-Bold"

def draw_header(c, page_no):
    # Logo-Ersatz: zentriert großer Marken-Schriftzug
    c.setFont(BOLD, 22)
    c.drawCentredString(PAGE_W / 2, TOP, "MUSTER CARPET")

    # Seitenzahl rechts oben
    c.setFont(LABEL_FONT, 8)
    c.drawRightString(RIGHT, TOP - 0.9 * cm, f"Seite {page_no}")

    # kleine Lieferanten-Zeile (Adresszeile über Kundenadresse, wie im Original)
    y = TOP - 1.8 * cm
    c.setFont(LABEL_FONT, 7)
    c.setFillColor(colors.grey)
    c.drawString(LEFT, y, f"{LIEFERANT['name']} · {LIEFERANT['strasse']} · {LIEFERANT['plz_ort']}")
    c.setFillColor(colors.black)

def draw_addr_block(c, y_start):
    # Links: Kundenadresse
    x = LEFT
    y = y_start
    c.setFont(LABEL_FONT, 11)
    c.drawString(x, y,                 KUNDE["firma"]);   y -= 0.5 * cm
    c.drawString(x, y,                 KUNDE["strasse"]); y -= 0.5 * cm
    c.drawString(x, y,                 KUNDE["plz_ort"]); y -= 0.5 * cm
    c.drawString(x, y,                 KUNDE["land"])

    # Rechts: Meta-Block (zwei Spalten)
    x_lbl = PAGE_W / 2 + 0.8 * cm
    x_val = PAGE_W / 2 + 4.6 * cm
    y = y_start
    c.setFont(BOLD, 10);  c.drawString(x_lbl, y, "Ihre Kd. Nr.:")
    c.setFont(BOLD, 10);  c.drawString(x_val, y, KUNDE["kd_nr"]);     y -= 0.45 * cm
    c.setFont(LABEL_FONT, 10); c.drawString(x_lbl, y, "Datum:")
    c.drawString(x_val, y, KUNDE["datum"]);                            y -= 0.7 * cm
    c.drawString(x_lbl, y, "Innendienst:")
    c.drawString(x_val, y, KUNDE["innendienst"]);                      y -= 0.45 * cm
    c.drawString(x_lbl, y, "Telefon:")
    c.drawString(x_val, y, KUNDE["innen_tel"]);                        y -= 0.45 * cm
    c.drawString(x_lbl, y, "E-Mail:")
    # E-Mail evtl. mehrzeilig
    for i, line in enumerate(KUNDE["innen_mail"].split("\n")):
        c.drawString(x_val, y - i * 0.4 * cm, line)
    y -= 0.85 * cm
    c.drawString(x_lbl, y, "Gebiet:")
    c.drawString(x_val, y, KUNDE["gebiet"]);                           y -= 0.45 * cm
    c.drawString(x_lbl, y, "Außendienst:")
    c.drawString(x_val, y, KUNDE["aussendienst"])

def draw_lieferanschrift(c, y_start):
    x = LEFT
    y = y_start
    c.setFont(BOLD, 11);  c.drawString(x, y, "Lieferanschrift"); y -= 0.45 * cm
    c.setFont(LABEL_FONT, 10)
    c.drawString(x, y, KUNDE["firma"]);   y -= 0.4 * cm
    c.drawString(x, y, KUNDE["zusatz"]);  y -= 0.4 * cm
    c.drawString(x, y, KUNDE["strasse"]); y -= 0.4 * cm
    c.drawString(x, y, KUNDE["plz_ort"]); y -= 0.4 * cm
    c.drawString(x, y, KUNDE["land"])

    # rechte Seite: Liefertermin / Ihr Zeichen / Gewicht
    x_lbl = PAGE_W / 2 + 0.8 * cm
    x_val = PAGE_W / 2 + 4.6 * cm
    y = y_start
    c.drawString(x_lbl, y, "Liefertermin");
    c.drawString(x_val, y, AUFTRAG["liefertermin"]); y -= 0.45 * cm
    c.drawString(x_lbl, y, "Ihr Zeichen:");
    c.drawString(x_val, y, AUFTRAG["ihr_zeichen"]); y -= 0.9 * cm
    c.drawString(x_lbl, y, "Gewicht/KG");
    c.drawString(x_val, y, AUFTRAG["gewicht"])

def draw_kommissionierpapier(c, y_start):
    x = LEFT
    y = y_start
    c.setFont(BOLD, 13); c.drawString(x, y, "Kommissionierpapier"); y -= 0.5 * cm
    c.setFont(LABEL_FONT, 10); c.drawString(x, y, f"Kommission:   {AUFTRAG['kommission']}"); y -= 0.45 * cm
    c.setFont(BOLD, 10); c.drawString(x, y, f"Rg. an Debitor-Nr: {AUFTRAG['debitor']}")
    c.drawRightString(RIGHT, y, f"Auftragsnr. {AUFTRAG['auftragsnr']}"); y -= 0.55 * cm
    c.setFont(BOLD, 10); c.drawString(x, y, "Frachtmerkmale/Lieferbedingung"); y -= 0.4 * cm
    c.setFont(LABEL_FONT, 10); c.drawString(x, y, AUFTRAG["fracht"]); y -= 0.4 * cm
    c.drawString(x, y, f"Info Frachtbrief:: {AUFTRAG['info_frachtbrief']}"); y -= 0.6 * cm
    c.setFont(BOLD, 10); c.drawString(x, y, "Warenausgangsnummer"); y -= 0.5 * cm
    c.setFont(LABEL_FONT, 9)
    c.drawString(x, y, "Bitte beachten Sie unsere AGB, die Geschäftsgrundlage für diesen Auftrag sind. Diese sind einsehbar"); y -= 0.35 * cm
    c.drawString(x, y, f"unter {LIEFERANT['agb']}."); y -= 0.7 * cm
    return y

def draw_pos_header(c, y):
    c.setFont(BOLD, 10)
    c.drawString(LEFT,             y, "Pos.")
    c.drawString(LEFT + 1.2 * cm,  y, "Art. Nr.")
    c.drawString(LEFT + 4.2 * cm,  y, "Beschreibung")
    c.drawString(LEFT + 11.0 * cm, y, "Menge")
    return y - 0.6 * cm

def draw_position(c, y, p):
    c.setFont(LABEL_FONT, 10)
    c.drawString(LEFT,             y, p["pos"])
    c.drawString(LEFT + 1.2 * cm,  y, p["art_nr"])
    c.drawString(LEFT + 4.2 * cm,  y, p["name"])
    c.drawString(LEFT + 11.0 * cm, y, p["menge"])
    y -= 0.4 * cm
    c.drawString(LEFT + 4.2 * cm,  y, p["typ"]);                    y -= 0.4 * cm
    c.drawString(LEFT + 4.2 * cm,  y, f"Warenzolltariffnr: {p['wztnr']}"); y -= 0.4 * cm
    for label, value in p["specs"]:
        c.drawString(LEFT + 4.2 * cm, y, label)
        for j, vline in enumerate(value.split("\n")):
            c.drawString(LEFT + 8.5 * cm, y - j * 0.4 * cm, vline)
        y -= 0.4 * cm * max(1, value.count("\n") + 1)
    return y

def draw_footer(c):
    # ganz unten: Firmenblock in 4 Spalten wie Original
    y = 3.2 * cm
    c.setFont(LABEL_FONT, 7)
    # 4 Spalten mit etwas mehr Luft vor der zweiten Spalte
    col_w = (RIGHT - LEFT) / 4
    x1 = LEFT
    x2 = LEFT + 1.05 * col_w
    x3 = LEFT + 2.20 * col_w
    x4 = LEFT + 3.10 * col_w

    # Spalte 1: Firmenanschrift
    c.drawString(x1, y, LIEFERANT["name"])
    c.drawString(x1, y - 0.3 * cm, LIEFERANT["strasse"])
    c.drawString(x1, y - 0.6 * cm, LIEFERANT["plz_ort"])
    c.drawString(x1, y - 0.9 * cm, f"Fon {LIEFERANT['tel']}")
    c.drawString(x1, y - 1.2 * cm, LIEFERANT["mail"])

    # Spalte 2: Geschäftsführer / Handelsregister / VAT
    # GF-Namen ggf. auf zwei Zeilen
    gf_parts = LIEFERANT["gf"].split(", ")
    c.drawString(x2, y,             "Geschäftsführer:")
    c.drawString(x2 + 1.9 * cm, y,  gf_parts[0] + ("," if len(gf_parts) > 1 else ""))
    if len(gf_parts) > 1:
        c.drawString(x2 + 1.9 * cm, y - 0.3 * cm, gf_parts[1])
        c.drawString(x2, y - 0.6 * cm, "Handelsregister:")
        c.drawString(x2 + 1.9 * cm, y - 0.6 * cm, LIEFERANT["hrb"])
        c.drawString(x2, y - 0.9 * cm, "VAT ID-no.:")
        c.drawString(x2 + 1.9 * cm, y - 0.9 * cm, LIEFERANT["vat"])
    else:
        c.drawString(x2, y - 0.3 * cm, "Handelsregister:")
        c.drawString(x2 + 1.9 * cm, y - 0.3 * cm, LIEFERANT["hrb"])
        c.drawString(x2, y - 0.6 * cm, "VAT ID-no.:")
        c.drawString(x2 + 1.9 * cm, y - 0.6 * cm, LIEFERANT["vat"])

    # Spalte 3: Bank 1
    name, iban, bic = LIEFERANT["bank1"]
    c.drawString(x3, y, name)
    c.drawString(x3, y - 0.3 * cm, f"IBAN {iban}")
    c.drawString(x3, y - 0.6 * cm, f"BIC {bic}")

    # Spalte 4: Bank 2
    name, iban, bic = LIEFERANT["bank2"]
    c.drawString(x4, y, name)
    c.drawString(x4, y - 0.3 * cm, f"IBAN {iban}")
    c.drawString(x4, y - 0.6 * cm, f"BIC {bic}")

    # Hinweis ganz unten (etwas tiefer, damit kein Overlap mit Mail-Zeile)
    c.setFont(LABEL_FONT, 7)
    c.drawString(LEFT, 1.4 * cm,
        "Bitte beachten Sie unsere AGB, die Geschäftsgrundlage für diesen Auftrag sind. "
        f"Diese sind einsehbar unter {LIEFERANT['agb']}.")

def draw_addr_only_for_page2(c):
    # Auf Seite 2 fehlt der Lieferanschrift-Block, sonst gleicher Kopf
    draw_header(c, 2)
    draw_addr_block(c, TOP - 3.0 * cm)

# ---------- Build ----------------------------------------------------------

c = canvas.Canvas(OUT, pagesize=A4)

# ----- Seite 1 -----
draw_header(c, 1)
draw_addr_block(c, TOP - 3.0 * cm)
draw_lieferanschrift(c, TOP - 8.2 * cm)

y = draw_kommissionierpapier(c, TOP - 11.5 * cm)
y = draw_pos_header(c, y - 0.2 * cm)
y = draw_position(c, y, POSITIONEN[0])

draw_footer(c)
c.showPage()

# ----- Seite 2 -----
draw_addr_only_for_page2(c)
y = TOP - 9.5 * cm
y = draw_position(c, y, POSITIONEN[1])
y -= 0.5 * cm
c.setFont(LABEL_FONT, 10)
for line in FUSSTEXT:
    c.drawString(LEFT, y, line)
    y -= 0.45 * cm

draw_footer(c)
c.showPage()
c.save()
print("PDF gespeichert:", OUT)
