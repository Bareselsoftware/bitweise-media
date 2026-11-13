"""Tag 04 – 2,4 GHz oder 5 GHz – welches WLAN ist besser? (Kommt drauf an: Reichweite vs. Tempo)"""
import sys, math
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *

LABEL = "WIE FUNKTIONIERT'S?"


# ---------- Bausteine ----------
def router(d, cx, cy, a=1.0, s=1.0):
    c = mix(BG, WH, a)
    d.rounded_rectangle([cx - 70 * s, cy - 28 * s, cx + 70 * s, cy + 28 * s], radius=int(12 * s), outline=c, width=6)
    for dx in (-40, 40):
        d.line([(cx + dx * s, cy - 28 * s), (cx + dx * 1.3 * s, cy - 95 * s)], fill=c, width=7)
    for i in range(3):
        d.ellipse([cx - 45 * s + i * 30 * s - 6, cy - 6, cx - 45 * s + i * 30 * s + 6, cy + 6], fill=mix(BG, CY, a))


def waves(d, cx, cy, k, wall_x, reach, behind, a=1.0):
    """Funkwellen als Bögen; hinter der Wand (wall_x) abgeschwächt auf Anteil `behind`."""
    maxr = reach * k
    r = 70
    while r <= maxr:
        fade = 1 - (r / (reach + 1)) * 0.55
        al = a * fade * (behind if cx + r > wall_x else 1.0)
        ang = min(38, math.degrees(math.asin(min(1.0, 165 / r))))
        if al > 0.02:
            d.arc([cx - r, cy - r, cx + r, cy + r], -ang, ang, fill=mix(BG, CY, al), width=6)
        r += 62


def wall(d, x, y0, y1, a=1.0):
    c = mix(BG, GR, a * 0.8)
    d.rectangle([x, y0, x + 34, y1], fill=mix(BG, PANEL, a), outline=c, width=3)
    for yy in range(int(y0) + 30, int(y1), 46):
        d.line([(x + 3, yy), (x + 31, yy)], fill=c, width=2)
    d.text((x + 17, y1 + 46), "Wand", font=font(MED, 30), fill=mix(BG, GR, a), anchor="ms")


def row(d, y, plus, title, sub, k):
    if k <= 0:
        return
    col = GN if plus else RD
    d.rounded_rectangle([110, y, 930, y + 112], radius=22, fill=mix(BG, PANEL, k))
    d.text((165, y + 76), "+" if plus else "–", font=font(BLACK, 64), fill=mix(BG, col, k), anchor="ms")
    d.text((225, y + (60 if sub else 74)), title, font=font(SEMI, 50), fill=mix(BG, WH, k), anchor="ls")
    if sub:
        d.text((225, y + 98), sub, font=font(MED, 34), fill=mix(BG, GR, k), anchor="ls")


def band_scene(t, off, band, reach, behind, rows):
    img = background(t + off); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease(t / 0.4)
    d.text((110 + int(30 * (1 - a)), 470), band, font=font(BLACK, 120), fill=mix(BG, CY, a), anchor="ls")
    router(d, 200, 760, a)
    wall(d, 610, 580, 900, a)
    k = ease((t - 0.2) / 1.6)
    if k > 0:
        waves(d, 200, 760, k, 610, reach, behind)
    for i, (st, plus, title, sub) in enumerate(rows):
        row(d, 1010 + i * 125, plus, title, sub, ease((t - st) / 0.35))
    return img


# ---------- Szenen ----------
def s1(t):  # Hook
    img = background(t); d = ImageDraw.Draw(img)
    header(d, LABEL)
    for i, (lab, st) in enumerate([("2,4 GHz", 0.1), ("5 GHz", 0.5)]):
        k = ease((t - st) / 0.4)
        if k <= 0:
            continue
        x0 = 110 + i * 450
        y = 620 + int(40 * (1 - k))
        d.rounded_rectangle([x0, y, x0 + 370, y + 300], radius=30, fill=mix(BG, PANEL, k), outline=mix(BG, CY, k * 0.7), width=4)
        router(d, x0 + 185, y + 170, k, 0.8)
        d.text((x0 + 185, y + 270), lab, font=font(BLACK, 64), fill=mix(BG, WH, k), anchor="ms")
    if t > 1.0:
        a = ease((t - 1.0) / 0.4)
        d.text((520, 775), "vs.", font=font(BOLD, 44), fill=mix(BG, GR, a), anchor="mm")
    if t > 1.2:
        a1 = ease((t - 1.2) / 0.4)
        text_c(d, 1090, "Welches WLAN", font(BLACK, 100), WH, a1, int(30 * (1 - a1)))
        text_c(d, 1215, "ist besser?", font(BLACK, 110), CY, a1, int(30 * (1 - a1)))
    if t > 3.4:
        a3 = ease((t - 3.4) / 0.4)
        text_c(d, 1380, "Ich habe nachgeschlagen.", font(MED, 50), GR, a3)
    return img


ROWS24 = [(0.4, True, "Reichweite: weit", None), (1.6, True, "Durch Wände: gut", None),
          (4.0, False, "Langsamer", None), (5.2, False, "Oft voll", "Nachbar-WLANs · Bluetooth · Mikrowelle")]
ROWS5 = [(0.4, True, "Deutlich schneller", None), (1.8, True, "Mehr freie Kanäle", None),
         (3.5, False, "Reichweite: kürzer", None), (4.8, False, "Wände bremsen stärker", None)]


def s2(t):
    return band_scene(t, 5.3, "2,4 GHz", 700, 0.6, ROWS24)


def s3(t):
    return band_scene(t, 16.0, "5 GHz", 400, 0.12, ROWS5)


def s4(t):  # Fazit
    img = background(t + 23.6); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease(t / 0.4)
    d.text((110, 420), "FAZIT", font=font(MONO, 40), fill=mix(BG, CY, a), anchor="ls")
    d.text((110 + int(30 * (1 - a)), 520), "Kommt drauf an.", font=font(BLACK, 92), fill=mix(BG, WH, a), anchor="ls")
    for i, (st, situ, band) in enumerate([(0.2, "Nah am Router", "5 GHz"), (2.6, "Weit weg, dicke Wände", "2,4 GHz")]):
        k = ease((t - st) / 0.4)
        if k <= 0:
            continue
        y = 640 + i * 260
        d.rounded_rectangle([110, y, 930, y + 220], radius=26, fill=mix(BG, PANEL, k), outline=mix(BG, CY, k * 0.6), width=3)
        d.text((160, y + 80), situ, font=font(SEMI, 50), fill=mix(BG, GR, k), anchor="ls")
        d.text((160 + int(20 * (1 - k)), y + 180), "→ " + band, font=font(BLACK, 84), fill=mix(BG, CY, k), anchor="ls")
    if t > 5.4:
        a2 = ease((t - 5.4) / 0.4)
        text_c(d, 1270, "Viele Router wählen", font(BOLD, 64), WH, a2, int(20 * (1 - a2)))
        text_c(d, 1360, "das automatisch.", font(BOLD, 64), WH, a2, int(20 * (1 - a2)))
    return img


def s5(t):  # Ausblick
    img = background(t + 31.4); d = ImageDraw.Draw(img)
    header(d, LABEL)
    a = ease(t / 0.4)
    d.text((110, 700), "Morgen:", font=font(BOLD, 74), fill=mix(BG, CY, a), anchor="ls")
    f = font(BLACK, 88)
    for i, ln in enumerate(["Was das Schloss", "im Browser", "wirklich bedeutet"]):
        ai = ease((t - 0.2 - i * 0.15) / 0.35)
        d.text((110 + int(30 * (1 - ai)), 830 + i * 115), ln, font=f, fill=mix(BG, WH, ai), anchor="ls")
    return img


SCENES = [("s1", s1, 5.3), ("s2", s2, 10.7), ("s3", s3, 7.6), ("s4", s4, 7.8), ("s5", s5, 3.1)]

# Sprechtext: (Startzeit absolut in s, Text). Zahlen ausgeschrieben.
VOICE = [(0.3, "Zwei Komma vier oder fünf Gigahertz. Welches WLAN ist besser? Ich habe nachgeschlagen."),
         (5.5, "Zwei Komma vier Gigahertz reicht weiter und kommt besser durch Wände."),
         (9.3, "Dafür ist es langsamer. Und der Bereich ist oft voll: Nachbar-WLANs, Bluetooth, sogar die Mikrowelle stört dort."),
         (16.2, "Fünf Gigahertz ist deutlich schneller und hat mehr freie Kanäle."),
         (19.5, "Dafür ist die Reichweite kürzer. Wände schlucken mehr vom Signal."),
         (23.8, "Also: Nah am Router nimm fünf Gigahertz."),
         (26.2, "Weit weg oder hinter dicken Wänden: zwei Komma vier."),
         (29.0, "Viele Router wählen das inzwischen automatisch."),
         (31.55, "Morgen: Was das Schloss im Browser wirklich bedeutet.")]


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        print(stills(SCENES, "/home/claude/bitweise-out/tag04"))
    else:
        print(build(SCENES, "tag04_wlan", seed=4, voice=VOICE))
