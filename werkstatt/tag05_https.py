"""Tag 05 – Was das Schloss im Browser wirklich bedeutet (HTTPS: sichere Leitung, nicht sicherer Laden)"""
import sys, math
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *

LABEL = "WIE FUNKTIONIERT'S?"


# ---------- Bausteine ----------
def lock(d, cx, cy, s=1.0, col=CY, a=1.0):
    c = mix(BG, col, a)
    w, h = 64 * s, 50 * s
    d.arc([cx - 22 * s, cy - h / 2 - 34 * s, cx + 22 * s, cy - h / 2 + 10 * s], 180, 360, fill=c, width=max(3, int(8 * s)))
    d.line([(cx - 22 * s + 4 * s, cy - h / 2 - 12 * s), (cx - 22 * s + 4 * s, cy - h / 2 + 2)], fill=c, width=max(3, int(8 * s)))
    d.line([(cx + 22 * s - 4 * s, cy - h / 2 - 12 * s), (cx + 22 * s - 4 * s, cy - h / 2 + 2)], fill=c, width=max(3, int(8 * s)))
    d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=int(8 * s), fill=c)
    d.ellipse([cx - 6 * s, cy - 8 * s, cx + 6 * s, cy + 4 * s], fill=mix(BG, BG, 1))


def check(d, cx, cy, s, col, a):
    c = mix(BG, col, a)
    d.line([(cx - 22 * s, cy), (cx - 6 * s, cy + 16 * s), (cx + 24 * s, cy - 18 * s)], fill=c, width=int(9 * s), joint="curve")


def addressbar(d, y, url, a=1.0, col=WH, lock_col=CY, x0=110, x1=930):
    d.rounded_rectangle([x0, y, x1, y + 110], radius=55, fill=mix(BG, PANEL, a), outline=mix(BG, GR, a * 0.5), width=3)
    lock(d, x0 + 70, y + 62, 0.62, lock_col, a)
    d.text((x0 + 125, y + 72), url, font=font(MONO, 38), fill=mix(BG, col, a), anchor="ls")


def device(d, cx, cy, a, lab):
    c = mix(BG, WH, a)
    d.rounded_rectangle([cx - 55, cy - 90, cx + 55, cy + 90], radius=18, outline=c, width=6)
    d.line([(cx - 18, cy + 70), (cx + 18, cy + 70)], fill=c, width=5)
    d.text((cx, cy + 150), lab, font=font(MED, 34), fill=mix(BG, GR, a), anchor="ms")


def server(d, cx, cy, a, lab):
    c = mix(BG, WH, a)
    for i in range(3):
        y = cy - 85 + i * 60
        d.rounded_rectangle([cx - 70, y, cx + 70, y + 48], radius=10, outline=c, width=5)
        d.ellipse([cx + 38, y + 18, cx + 50, y + 30], fill=mix(BG, CY, a))
    d.text((cx, cy + 150), lab, font=font(MED, 34), fill=mix(BG, GR, a), anchor="ms")


def spy(d, cx, cy, a):
    c = mix(BG, RD, a)
    d.ellipse([cx - 32, cy - 70, cx + 32, cy - 6], outline=c, width=6)
    d.arc([cx - 60, cy, cx + 60, cy + 110], 180, 360, fill=c, width=6)
    # Brille / Lupe
    d.ellipse([cx + 40, cy - 70, cx + 90, cy - 20], outline=c, width=5)
    d.line([(cx + 83, cy - 27), (cx + 108, cy - 2)], fill=c, width=6)


SALAT = "x9#Qe!7&kP"


# ---------- Szenen ----------
def s1(t):  # Hook
    img = background(t); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease((t - 0.1) / 0.4)
    addressbar(d, 560 + int(30 * (1 - a)), "https://deine-bank.de", a)
    if t > 0.7:
        k = ease((t - 0.7) / 0.5)
        lock(d, W // 2, 880, 2.4 * (0.7 + 0.3 * k), CY, k)
    if t > 1.4:
        a1 = ease((t - 1.4) / 0.4)
        text_c(d, 1110, "Schloss =", font(BLACK, 100), WH, a1, int(30 * (1 - a1)))
        text_c(d, 1230, "sichere Seite?", font(BLACK, 110), CY, a1, int(30 * (1 - a1)))
    if t > 2.6:
        a3 = ease((t - 2.6) / 0.4)
        text_c(d, 1390, "Ich habe nachgeschlagen.", font(MED, 50), GR, a3)
    return img


def s2(t):  # Verschlüsselung
    img = background(t + 4.8); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease(t / 0.4)
    d.text((110, 400), "1  VERSCHLÜSSELT", font=font(MONO, 40), fill=mix(BG, CY, a), anchor="ls")
    device(d, 190, 700, a, "Du")
    server(d, 790, 700, a, "Website")
    # Leitung
    k = ease((t - 0.2) / 0.8)
    if k > 0:
        x0, x1 = 260, 700
        d.rounded_rectangle([x0, 680, x0 + (x1 - x0) * k, 720], radius=20, fill=mix(BG, CY, 0.25 * a), outline=mix(BG, CY, a), width=3)
        if k > 0.95:
            lock(d, 480, 650, 0.7, CY, ease((t - 1.0) / 0.3))
    # Paket wandert, wird verschlüsselt
    if t > 1.2:
        p = ((t - 1.2) / 2.6) % 1.0
        px = 340 + p * 260
        txt = "passwort123" if p < 0.12 else SALAT
        col = WH if p < 0.12 else CY
        d.text((px, 790), txt, font=font(MONO, 34), fill=col, anchor="ms")
    if t > 0.3:
        a1 = ease((t - 0.3) / 0.4)
        text_c(d, 940, "Die Verbindung ist", font(BOLD, 64), WH, a1, int(20 * (1 - a1)))
        text_c(d, 1030, "verschlüsselt.", font(BLACK, 76), CY, a1, int(20 * (1 - a1)))
    if t > 2.7:
        k2 = ease((t - 2.7) / 0.4)
        spy(d, 230, 1200, k2)
        d.text((380, 1185), "Mitleser im WLAN", font=font(SEMI, 44), fill=mix(BG, WH, k2), anchor="ls")
        d.text((380, 1255), "sieht nur: " + SALAT, font=font(MONO, 36), fill=mix(BG, GR, k2), anchor="ls")
    return img


def s3(t):  # Zertifikat
    img = background(t + 11.8); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease(t / 0.4)
    d.text((110, 400), "2  ZERTIFIKAT", font=font(MONO, 40), fill=mix(BG, CY, a), anchor="ls")
    k = ease((t - 0.2) / 0.45)
    y = 520 + int(40 * (1 - k))
    if k > 0:
        d.rounded_rectangle([110, y, 930, y + 470], radius=30, fill=mix(BG, PANEL, k), outline=mix(BG, CY, k * 0.7), width=4)
        d.text((170, y + 95), "ZERTIFIKAT", font=font(MONO, 44), fill=mix(BG, CY, k), anchor="ls")
        d.text((170, y + 190), "ausgestellt für", font=font(MED, 40), fill=mix(BG, GR, k), anchor="ls")
        d.text((170, y + 270), "deine-bank.de", font=font(BLACK, 76), fill=mix(BG, WH, k), anchor="ls")
        # Siegel
        d.ellipse([740, y + 300, 870, y + 430], outline=mix(BG, CY, k * 0.8), width=5)
        lock(d, 805, y + 375, 0.7, CY, k)
    if t > 1.9:
        k2 = ease((t - 1.9) / 0.4)
        check(d, 160, y + 390, 1.0, GN, k2)
        d.text((215, y + 405), "Adresse bestätigt", font=font(SEMI, 46), fill=mix(BG, GN, k2), anchor="ls")
    if t > 2.3:
        a2 = ease((t - 2.3) / 0.4)
        text_c(d, 1150, "Du bist wirklich mit", font(BOLD, 62), WH, a2, int(20 * (1 - a2)))
        text_c(d, 1240, "dieser Adresse verbunden.", font(BOLD, 62), WH, a2, int(20 * (1 - a2)))
    return img


def s4(t):  # Aber
    img = background(t + 16.6); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease(t / 0.4)
    d.text((110 + int(30 * (1 - a)), 470), "Aber:", font=font(BLACK, 110), fill=mix(BG, RD, a), anchor="ls")
    if t > 0.9:
        a1 = ease((t - 0.9) / 0.4)
        d.text((110, 590), "Ob die Seite seriös ist,", font=font(BOLD, 60), fill=mix(BG, WH, a1), anchor="ls")
        d.text((110, 670), "sagt das Schloss nicht.", font=font(BOLD, 60), fill=mix(BG, WH, a1), anchor="ls")
    if t > 3.5:
        k = ease((t - 3.5) / 0.4)
        d.rounded_rectangle([110, 770, 930, 880], radius=22, fill=mix(BG, PANEL, k))
        d.text((165, 846), "€", font=font(BLACK, 56), fill=mix(BG, CY, k), anchor="ms")
        d.text((225, 845), "Zertifikat: kostenlos", font=font(SEMI, 50), fill=mix(BG, WH, k), anchor="ls")
    if t > 4.6:
        k = ease((t - 4.6) / 0.4)
        d.text((110, 960), "… auch für Betrüger:", font=font(SEMI, 50), fill=mix(BG, GR, k), anchor="ls")
        addressbar(d, 1000 + int(20 * (1 - k)), "deine-bank.login-hilfe.xyz", k, RD)
    if t > 6.0:
        a3 = ease((t - 6.0) / 0.4)
        text_c(d, 1250, "Viele Phishing-Seiten", font(BLACK, 72), WH, a3, int(20 * (1 - a3)))
        text_c(d, 1345, "haben das Schloss.", font(BLACK, 72), RD, a3, int(20 * (1 - a3)))
    return img


def s5(t):  # Fazit
    img = background(t + 25.2); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease(t / 0.4)
    d.text((110, 420), "FAZIT", font=font(MONO, 40), fill=mix(BG, CY, a), anchor="ls")
    for i, (st, col, mark, txt) in enumerate([(0.3, GN, "=", "sichere Leitung"), (1.6, RD, "≠", "sicherer Laden")]):
        k = ease((t - st) / 0.4)
        if k <= 0:
            continue
        y = 500 + i * 250
        d.rounded_rectangle([110, y, 930, y + 210], radius=26, fill=mix(BG, PANEL, k), outline=mix(BG, col, k * 0.6), width=3)
        lock(d, 200, y + 118, 1.1, CY, k)
        d.text((290, y + 140), mark, font=font(BLACK, 90), fill=mix(BG, col, k), anchor="ls")
        d.text((370 + int(20 * (1 - k)), y + 135), txt, font=font(BLACK, 66), fill=mix(BG, WH, k), anchor="ls")
    if t > 3.6:
        a2 = ease((t - 3.6) / 0.4)
        text_c(d, 1130, "Prüf immer", font(BLACK, 92), WH, a2, int(20 * (1 - a2)))
        text_c(d, 1240, "die Adresse.", font(BLACK, 92), CY, a2, int(20 * (1 - a2)))
    return img


def s6(t):  # Ausblick
    img = background(t + 30.2); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease(t / 0.4)
    d.text((110, 700), "Morgen:", font=font(BOLD, 74), fill=mix(BG, CY, a), anchor="ls")
    f = font(BLACK, 88)
    for i, ln in enumerate(["KI-Logbuch #1", "Meine Zahlen der", "ersten Woche"]):
        ai = ease((t - 0.2 - i * 0.15) / 0.35)
        d.text((110 + int(30 * (1 - ai)), 830 + i * 115), ln, font=f, fill=mix(BG, WH, ai), anchor="ls")
    return img


SCENES = [("s1", s1, 4.8), ("s2", s2, 7.0), ("s3", s3, 4.8), ("s4", s4, 8.6), ("s5", s5, 5.0), ("s6", s6, 3.8)]

# Sprechtext: (Startzeit absolut in s, Text). Zahlen ausgeschrieben.
VOICE = [(0.3, "Das Schloss im Browser. Heißt das: sichere Seite? Ich habe nachgeschlagen."),
         (4.95, "Das Schloss heißt: Die Verbindung ist verschlüsselt."),
         (7.5, "Wer im offenen WLAN mitliest, sieht von deinen Eingaben nur Zeichensalat."),
         (12.0, "Ein Zertifikat bestätigt außerdem: Du bist wirklich mit dieser Adresse verbunden."),
         (16.8, "Aber: Ob die Seite seriös ist, sagt das Schloss nicht."),
         (20.1, "Zertifikate gibt es kostenlos, auch für Betrüger. Viele Phishing-Seiten haben das Schloss."),
         (25.4, "Also: Schloss heißt sichere Leitung, nicht sicherer Laden."),
         (28.75, "Prüf immer die Adresse."),
         (30.35, "Morgen: KI-Logbuch Nummer eins. Meine Zahlen der ersten Woche.")]


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        print(stills(SCENES, "/home/claude/bitweise-out/tag05"))
    else:
        print(build(SCENES, "tag05_https", seed=5, voice=VOICE))
