"""Tag 03 – Mythos-Check: Macht dich der Inkognito-Modus anonym? (Nein: nur lokal privat)"""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *

LABEL = "MYTHOS-CHECK"


# ---------- Bausteine ----------
def incognito(d, cx, cy, a=1.0, s=1.0, col=WH):
    """Inkognito-Symbol: Hut + Brille."""
    c = mix(BG, col, a)
    # Hut
    d.rounded_rectangle([cx - 70 * s, cy - 120 * s, cx + 70 * s, cy - 40 * s], radius=int(22 * s), fill=c)
    d.rounded_rectangle([cx - 125 * s, cy - 48 * s, cx + 125 * s, cy - 26 * s], radius=int(11 * s), fill=c)
    # Brille
    w = int(10 * s)
    d.ellipse([cx - 110 * s, cy + 5 * s, cx - 20 * s, cy + 85 * s], outline=c, width=w)
    d.ellipse([cx + 20 * s, cy + 5 * s, cx + 110 * s, cy + 85 * s], outline=c, width=w)
    d.arc([cx - 28 * s, cy + 22 * s, cx + 28 * s, cy + 62 * s], 200, 340, fill=c, width=w)


def device(d, x0, y0, a=1.0, label="Dein Gerät"):
    c = mix(BG, WH, a)
    d.rounded_rectangle([x0 + 15, y0, x0 + 175, y0 + 110], radius=10, outline=c, width=6)
    d.rounded_rectangle([x0, y0 + 118, x0 + 190, y0 + 136], radius=6, fill=c)
    incognito(d, x0 + 95, y0 + 55, a, 0.32, CY)
    d.text((x0 + 95, y0 + 190), label, font=font(SEMI, 36), fill=mix(BG, GR, a), anchor="ms")


def eye(d, cx, cy, a=1.0, col=CY):
    c = mix(BG, col, a)
    d.chord([cx - 42, cy - 40, cx + 42, cy + 40], 200, 340, outline=c, width=6)
    d.chord([cx - 42, cy - 40, cx + 42, cy + 40], 20, 160, outline=c, width=6)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=c)


def check(d, x, y, a=1.0, col=GN):
    c = mix(BG, col, a)
    d.line([(x, y), (x + 16, y + 18), (x + 46, y - 18)], fill=c, width=9, joint="curve")


# ---------- Szenen ----------
def s1(t):  # Hook
    img = background(t); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease((t - 0.1) / 0.45)
    incognito(d, W // 2, 760, a, lerp(1.25, 1.0, a))
    if t > 0.8:
        a1 = ease((t - 0.8) / 0.4)
        text_c(d, 1080, "Inkognito-Modus", font(BLACK, 104), WH, a1, int(30 * (1 - a1)))
        a2 = ease((t - 1.1) / 0.4)
        text_c(d, 1215, "= anonym?", font(BLACK, 128), CY, a2, int(30 * (1 - a2)))
    if t > 2.6:
        a3 = ease((t - 2.6) / 0.4)
        text_c(d, 1380, "Ich habe nachgeschlagen.", font(MED, 50), GR, a3)
    return img


ITEMS = [("Verlauf", 0.9), ("Cookies", 1.6), ("Formulardaten", 2.3)]


def s2(t):  # Was Inkognito wirklich tut
    img = background(t + 4.4); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease(t / 0.4)
    d.text((110, 420), "WAS ES TUT", font=font(MONO, 40), fill=mix(BG, CY, a), anchor="ls")
    d.text((110 + int(30 * (1 - a)), 515), "Beim Schließen weg:", font=font(BOLD, 74), fill=mix(BG, WH, a), anchor="ls")
    for i, (lab, st) in enumerate(ITEMS):
        k = ease((t - st) / 0.35)
        if k <= 0:
            continue
        y = 640 + i * 150
        d.rounded_rectangle([110, y, 930, y + 120], radius=24, fill=mix(BG, PANEL, k))
        d.text((170, y + 80), lab, font=font(SEMI, 58), fill=mix(BG, WH, k), anchor="ls")
        kc = ease((t - st - 0.4) / 0.3)
        if kc > 0:
            check(d, 820, y + 62, kc)
    if t > 4.15:
        a2 = ease((t - 4.15) / 0.4)
        sc = lerp(1.15, 1.0, a2)
        text_c(d, 1250, "…aber nur auf", font(BOLD, int(74 * sc)), WH, a2)
        text_c(d, 1360, "deinem Gerät.", font(BLACK, int(96 * sc)), CY, a2)
    return img


VIEWERS = [("Website", "sieht deine IP-Adresse", 0.3), ("Internetanbieter", "sieht, welche Seiten du aufrufst", 5.6),
           ("WLAN-Betreiber", "Firma, Schule …", 8.8)]


def s3(t):  # Wer trotzdem sieht
    img = background(t + 10.4); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease(t / 0.4)
    d.text((110, 420), "IM NETZ", font=font(MONO, 40), fill=mix(BG, CY, a), anchor="ls")
    d.text((110 + int(30 * (1 - a)), 515), "Wer trotzdem sieht:", font=font(BOLD, 74), fill=mix(BG, WH, a), anchor="ls")
    device(d, 110, 700, a)
    # Leitung vom Gerät nach rechts, Abzweige zu den Beobachtern
    xs = 330
    k0 = ease((t - 0.1) / 0.5)
    if k0 > 0:
        d.line([(xs - 20, 760), (lerp(xs - 20, xs + 40, k0), 760)], fill=GR, width=5)
    for i, (who, what, st) in enumerate(VIEWERS):
        k = ease((t - st) / 0.45)
        if k <= 0:
            continue
        y = 700 + i * 230
        d.line([(xs + 40, 760), (xs + 40, y + 60)], fill=mix(BG, GR, k), width=5)
        d.line([(xs + 40, y + 60), (lerp(xs + 40, 450, k), y + 60)], fill=mix(BG, GR, k), width=5)
        d.rounded_rectangle([450, y, 930, y + 175], radius=22, fill=mix(BG, PANEL, k), outline=mix(BG, CY, k * 0.6), width=3)
        eye(d, 510, y + 60, k)
        d.text((570, y + 78), who, font=font(BOLD, 44), fill=mix(BG, WH, k), anchor="ls")
        d.text((478, y + 143), what, font=font(MED, 31), fill=mix(BG, GR, k), anchor="ls")
    if t > 2.6:
        a2 = ease((t - 2.6) / 0.4)
        d.text((110, 1020), "Eingeloggt?", font=font(BOLD, 44), fill=mix(BG, CY, a2), anchor="ls")
        d.text((110, 1075), "Dann weiß sie,", font=font(MED, 38), fill=mix(BG, GR, a2), anchor="ls")
        d.text((110, 1120), "wer du bist.", font=font(MED, 38), fill=mix(BG, GR, a2), anchor="ls")
    return img


def s4(t):  # Verdikt
    img = background(t + 22.2); d = ImageDraw.Draw(img)
    header(d, LABEL)
    k = ease((t - 0.1) / 0.35)
    sc = lerp(1.6, 1.0, k)
    f = font(BLACK, int(150 * sc))
    tw = d.textlength("FALSCH", font=f)
    if k > 0:
        cx, cy = W // 2, 720
        d.rounded_rectangle([cx - tw / 2 - 40, cy - 110 * sc, cx + tw / 2 + 40, cy + 110 * sc],
                            radius=24, outline=mix(BG, RD, k), width=10)
        text_c(d, cy, "FALSCH", f, RD, k)
    if t > 1.4:
        a1 = ease((t - 1.4) / 0.4)
        text_c(d, 1030, "Inkognito =", font(BOLD, 64), WH, a1)
        text_c(d, 1125, "privat auf deinem Gerät", font(BOLD, 64), GN, a1)
    if t > 3.0:
        a2 = ease((t - 3.0) / 0.4)
        text_c(d, 1290, "nicht anonym", font(BLACK, 96), RD, a2, int(20 * (1 - a2)))
        text_c(d, 1385, "im Internet", font(BOLD, 64), WH, a2, int(20 * (1 - a2)))
    return img


def s5(t):  # Ausblick
    img = background(t + 27.7); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease(t / 0.4)
    d.text((110, 700), "Morgen:", font=font(BOLD, 74), fill=mix(BG, CY, a), anchor="ls")
    f = font(BLACK, 96)
    for i, ln in enumerate(["2,4 oder 5 GHz –", "welches WLAN", "ist besser?"]):
        ai = ease((t - 0.3 - i * 0.2) / 0.4)
        d.text((110 + int(30 * (1 - ai)), 840 + i * 120), ln, font=f, fill=mix(BG, WH, ai), anchor="ls")
    return img


SCENES = [("s1", s1, 4.4), ("s2", s2, 6.0), ("s3", s3, 11.8), ("s4", s4, 5.5), ("s5", s5, 4.3)]

# Sprechtext: (Startzeit absolut in s, Text). Zahlen ausgeschrieben.
VOICE = [(0.3, "Inkognito an, und keiner sieht, was du machst? Ich habe nachgeschlagen."),
         (4.6, "Inkognito löscht beim Schließen Verlauf, Cookies und Formulardaten."),
         (8.5, "Aber nur auf deinem Gerät."),
         (10.6, "Jede Website sieht deine IP-Adresse. Und eingeloggt weiß sie sowieso, wer du bist."),
         (16.0, "Dein Internetanbieter sieht, welche Seiten du ansteuerst."),
         (19.2, "Im WLAN von Firma oder Schule auch der Betreiber."),
         (22.4, "Mythos: falsch."),
         (23.7, "Inkognito ist privat auf deinem Gerät, aber nicht anonym im Internet."),
         (27.9, "Morgen: Zwei Komma vier oder fünf Gigahertz. Welches WLAN ist besser?")]


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        print(stills(SCENES, "/home/claude/bitweise-out/tag03"))
    else:
        print(build(SCENES, "tag03_inkognito", seed=3, voice=VOICE))
