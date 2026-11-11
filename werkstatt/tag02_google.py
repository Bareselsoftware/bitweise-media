"""Tag 02 – Was passiert, wenn du google.de eintippst? (DNS → Verbindung → Antwort)"""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *

LABEL = "WIE FUNKTIONIERT'S?"
IP = "142.250.185.99"   # Adresse aus Googles Netz 142.250.0.0/15 (Beispiel)


# ---------- Bausteine ----------
def step_head(d, t, nr, title):
    a = ease(t / 0.4)
    d.text((110, 420), f"SCHRITT {nr}/3", font=font(MONO, 40), fill=mix(BG, CY, a), anchor="ls")
    d.text((110 + int(30 * (1 - a)), 515), title, font=font(BOLD, 74), fill=mix(BG, WH, a), anchor="ls")


def device(d, x0, y0, a=1.0, label="Dein Gerät"):
    """Laptop-Symbol, Breite 190."""
    c = mix(BG, WH, a)
    d.rounded_rectangle([x0 + 15, y0, x0 + 175, y0 + 110], radius=10, outline=c, width=6)
    d.rounded_rectangle([x0, y0 + 118, x0 + 190, y0 + 136], radius=6, fill=c)
    d.text((x0 + 95, y0 + 190), label, font=font(SEMI, 36), fill=mix(BG, GR, a), anchor="ms")


def server(d, x0, y0, a=1.0, label="Server", w=200, accent=False):
    """Server-Rack-Symbol."""
    c = mix(BG, CY if accent else WH, a)
    for i in range(3):
        y = y0 + i * 46
        d.rounded_rectangle([x0, y, x0 + w, y + 38], radius=8, outline=c, width=5)
        d.ellipse([x0 + 16, y + 13, x0 + 28, y + 25], fill=c)
        d.line([(x0 + 50, y + 19), (x0 + w - 20, y + 19)], fill=mix(BG, GR, a * 0.6), width=4)
    d.text((x0 + w // 2, y0 + 190), label, font=font(SEMI, 36), fill=mix(BG, GR, a), anchor="ms")


def arrow(d, x0, x1, y, k, col, width=6):
    """Pfeil von x0 nach x1 (k = Fortschritt 0..1)."""
    if k <= 0:
        return
    xe = lerp(x0, x1, k)
    d.line([(x0, y), (xe, y)], fill=col, width=width)
    s = 1 if x1 > x0 else -1
    if k > 0.15:
        d.polygon([(xe, y), (xe - s * 22, y - 14), (xe - s * 22, y + 14)], fill=col)


def lock(d, cx, cy, a=1.0, s=1.0):
    c = mix(BG, CY, a)
    d.arc([cx - 26 * s, cy - 62 * s, cx + 26 * s, cy - 10 * s], 180, 360, fill=c, width=int(9 * s))
    d.line([(cx - 26 * s, cy - 36 * s), (cx - 26 * s, cy - 14 * s)], fill=c, width=int(9 * s))
    d.line([(cx + 26 * s, cy - 36 * s), (cx + 26 * s, cy - 14 * s)], fill=c, width=int(9 * s))
    d.rounded_rectangle([cx - 42 * s, cy - 18 * s, cx + 42 * s, cy + 46 * s], radius=int(10 * s), fill=c)
    d.ellipse([cx - 8 * s, cy + 4 * s, cx + 8 * s, cy + 20 * s], fill=BG)


# ---------- Szenen ----------
def s1(t):  # Hook
    img = background(t); d = ImageDraw.Draw(img)
    header(d, LABEL)
    # Adressleiste
    d.rounded_rectangle([110, 680, 930, 810], radius=65, fill=PANEL, outline=mix(PANEL, CY, 0.5), width=3)
    full = "google.de"
    shown = typed(full, t, 0.35, 0.11)
    f = font(MONO, 72)
    d.text((175, 768), shown, font=f, fill=WH, anchor="ls")
    cx = 175 + d.textlength(shown, font=f) + 8
    if t < 1.9 and (cursor_on(t) or len(shown) < len(full)):
        d.rectangle([cx, 705, cx + 8, 785], fill=CY)
    # Enter-Taste
    if t > 1.45:
        a = ease((t - 1.45) / 0.3)
        press = 8 if 1.85 < t < 2.05 else 0
        x0, y0 = 690, 860 + press
        d.rounded_rectangle([x0, y0, x0 + 240, y0 + 110], radius=18,
                            fill=mix(BG, CY if press else PANEL, a), outline=mix(BG, CY, a), width=4)
        d.text((x0 + 120, y0 + 72), "Enter ↵", font=font(MONO, 44),
               fill=mix(BG, BG if press else WH, a), anchor="ms")
    if t > 2.3:
        a = ease((t - 2.3) / 0.45)
        fb = font(BLACK, 128)
        text_c(d, 1150, "Was passiert", fb, WH, a, int(30 * (1 - a)))
        a2 = ease((t - 2.55) / 0.45)
        text_c(d, 1290, "dann?", fb, CY, a2, int(30 * (1 - a2)))
    return img


def s2(t):  # Schritt 1: DNS
    img = background(t + 5); d = ImageDraw.Draw(img)
    header(d, LABEL)
    step_head(d, t, 1, "Adresse nachschlagen")
    a = ease((t - 0.2) / 0.4)
    fs = font(MED, 50)
    d.text((110, 640), "Computer verstehen keine Namen –", font=fs, fill=mix(BG, GR, a), anchor="ls")
    d.text((110, 705), "nur Zahlen.", font=fs, fill=mix(BG, GR, a), anchor="ls")
    ad = ease((t - 1.2) / 0.4)
    device(d, 110, 850, ad)
    server(d, 700, 845, ad, "DNS-Server", w=200, accent=True)
    # Frage hin
    k1 = ease((t - 2.7) / 0.9)
    arrow(d, 320, 685, 930, k1, CY)
    if t > 2.9:
        a1 = ease((t - 2.9) / 0.35)
        d.text((502, 905), "google.de?", font=font(MONO, 42), fill=mix(BG, CY, a1), anchor="ms")
    # Antwort zurück
    k2 = ease((t - 5.7) / 0.8)
    arrow(d, 685, 320, 1030, k2, WH)
    if t > 6.3:
        a2 = ease((t - 6.3) / 0.35)
        d.text((502, 1085), IP, font=font(MONO, 40), fill=mix(BG, WH, a2), anchor="ms")
        d.text((502, 1130), "IP-Adresse", font=font(SEMI, 32), fill=mix(BG, GR, a2), anchor="ms")
    if t > 7.2:
        a3 = ease((t - 7.2) / 0.45)
        sc = lerp(1.15, 1.0, a3)
        text_c(d, 1330, "= Telefonbuch", font(BLACK, int(96 * sc)), CY, a3)
        text_c(d, 1430, "des Internets", font(BOLD, 64), WH, a3)
    return img


def s3(t):  # Schritt 2: Verbindung
    img = background(t + 14.6); d = ImageDraw.Draw(img)
    header(d, LABEL)
    step_head(d, t, 2, "Verbindung aufbauen")
    a = ease((t - 0.2) / 0.4)
    fs = font(MED, 50)
    d.text((110, 640), "Mit der Nummer geht's direkt", font=fs, fill=mix(BG, GR, a), anchor="ls")
    d.text((110, 705), "zum Server von Google.", font=fs, fill=mix(BG, GR, a), anchor="ls")
    device(d, 110, 850, a)
    server(d, 700, 845, a, IP, w=200)
    k = ease((t - 0.8) / 1.4)
    sec = t > 3.8
    col = CY if sec else GR
    # Verbindung als gestrichelte bzw. durchgehende Leitung
    if k > 0:
        xe = lerp(320, 685, k)
        if sec:
            d.line([(320, 930), (685, 930)], fill=CY, width=8)
        else:
            x = 320
            while x < xe:
                d.line([(x, 930), (min(x + 26, xe), 930)], fill=col, width=6)
                x += 44
    # Pakete pendeln
    if 1.5 < t < 3.9:
        for i in range(2):
            ph = ((t - 1.5) * 0.9 + i * 0.5) % 1.0
            px = lerp(320, 685, ph) if i == 0 else lerp(685, 320, ph)
            d.rounded_rectangle([px - 14, 916, px + 14, 944], radius=6, fill=WH)
    if sec:
        a2 = ease((t - 3.8) / 0.4)
        lock(d, 502, 1010, a2, lerp(1.4, 1.0, a2))
        text_c(d, 1260, "Verschlüsselt:", font(BOLD, 64), WH, a2, int(20 * (1 - a2)))
        text_c(d, 1370, "HTTPS", font(BLACK, 110), CY, a2, int(20 * (1 - a2)))
    return img


PACKETS = [("Text", 0.8), ("Code", 1.4), ("Bilder", 2.0)]


def s4(t):  # Schritt 3: Antwort
    img = background(t + 20.6); d = ImageDraw.Draw(img)
    header(d, LABEL)
    step_head(d, t, 3, "Die Seite kommt zurück")
    a = ease(t / 0.4)
    server(d, 730, 700, a, "Server", w=170)
    # Browserfenster
    done = t > 3.2
    bx0, by0, bx1, by1 = 110, 680, 560, 1150
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=18, fill=mix(BG, PANEL, a),
                        outline=mix(BG, CY if done else GR, a), width=4)
    d.line([(bx0, by0 + 56), (bx1, by0 + 56)], fill=mix(BG, GR, a * 0.6), width=3)
    for i, c in enumerate([RD, (240, 200, 80), GN]):
        d.ellipse([bx0 + 24 + i * 34, by0 + 18, bx0 + 44 + i * 34, by0 + 38], fill=mix(BG, c, a * 0.8))
    arrived = []
    for i, (lab, st) in enumerate(PACKETS):
        k = ease((t - st) / 1.0)
        if k <= 0:
            continue
        if k < 1:
            px = lerp(720, 590, k); py = 760 + i * 110
            fp = font(MONO, 36)
            tw = d.textlength(lab, font=fp)
            d.rounded_rectangle([px - tw - 30, py - 34, px, py + 22], radius=12, fill=CY)
            d.text((px - tw / 2 - 15, py + 6), lab, font=fp, fill=BG, anchor="ms")
        else:
            arrived.append(lab)
    # Inhalte im Browser
    if "Text" in arrived:
        for j, w in enumerate([340, 290, 320]):
            d.rounded_rectangle([bx0 + 40, by0 + 100 + j * 40, bx0 + 40 + w, by0 + 120 + j * 40], radius=8, fill=WH)
    if "Code" in arrived:
        d.rounded_rectangle([bx0 + 40, by0 + 240, bx0 + 230, by0 + 300], radius=14, fill=CY)
        d.text((bx0 + 135, by0 + 282), "Suche", font=font(SEMI, 32), fill=BG, anchor="ms")
    if "Bilder" in arrived:
        d.rounded_rectangle([bx0 + 40, by0 + 330, bx1 - 40, by1 - 30], radius=14, fill=(40, 48, 58))
        d.polygon([(bx0 + 80, by1 - 50), (bx0 + 190, by0 + 380), (bx0 + 290, by1 - 50)], fill=GR)
        d.ellipse([bx1 - 130, by0 + 360, bx1 - 80, by0 + 410], fill=(240, 200, 80))
    if done:
        a2 = ease((t - 3.2) / 0.4)
        text_c(d, 1300, "Dein Browser setzt", font(BOLD, 70), WH, a2, int(20 * (1 - a2)))
        text_c(d, 1390, "alles zusammen.", font(BOLD, 70), CY, a2, int(20 * (1 - a2)))
    return img


def s5(t):  # Schluss + Ausblick
    img = background(t + 26.2); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a0 = ease(t / 0.4)
    text_c(d, 560, "Das alles dauert meist", font(SEMI, 60), WH, a0)
    a1 = ease((t - 0.5) / 0.5)
    sc = lerp(1.25, 1.0, a1)
    text_c(d, 760, "< 1 Sekunde", font(BLACK, int(124 * sc)), CY, a1)
    if t > 2.9:
        a2 = ease((t - 2.9) / 0.4)
        d.text((110, 1040), "Morgen:", font=font(BOLD, 70), fill=mix(BG, CY, a2), anchor="ls")
        f = font(BLACK, 86)
        for i, ln in enumerate(["Macht dich der", "Inkognito-Modus", "anonym?"]):
            ai = ease((t - 3.1 - i * 0.18) / 0.4)
            d.text((110 + int(30 * (1 - ai)), 1160 + i * 108), ln, font=f, fill=mix(BG, WH, ai), anchor="ls")
    return img


SCENES = [("s1", s1, 5.0), ("s2", s2, 9.6), ("s3", s3, 6.0), ("s4", s4, 5.6), ("s5", s5, 6.6)]

# Sprechtext: (Startzeit absolut in s, Text). Zahlen/Domains ausgeschrieben.
VOICE = [(0.3, "Du tippst google punkt de ein und drückst Enter. Was passiert dann eigentlich?"),
         (5.2, "Computer verstehen keine Namen, nur Zahlen."),
         (7.8, "Also fragt dein Gerät zuerst einen DNS-Server: Welche IP-Adresse hat google punkt de?"),
         (12.3, "Das ist das Telefonbuch des Internets."),
         (14.8, "Mit dieser Nummer baut dein Browser eine Verbindung zum Server von Google auf."),
         (18.5, "Verschlüsselt, per HTTPS."),
         (20.8, "Der Server schickt die Seite zurück: Text, Code und Bilder."),
         (23.9, "Dein Browser setzt alles zusammen."),
         (26.4, "Und das alles meist in weniger als einer Sekunde."),
         (29.2, "Morgen: Macht dich der Inkognito-Modus wirklich anonym?")]


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        print(stills(SCENES, "/home/claude/bitweise-out/tag02"))
    else:
        print(build(SCENES, "tag02_google", seed=2, typing=[(0.35, 9, 0.11)], voice=VOICE))
