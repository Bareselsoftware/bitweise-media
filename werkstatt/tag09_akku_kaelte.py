"""Tag 09 – Kurios: Warum dein Akku bei Kälte plötzlich leer ist (Format v3 + Experiment „Einstieg“:
Tempo 0,82, Hook-Satz ≤ 6 Wörter, Zoom-Punch + Whoosh in Sekunde 0)."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *
import math

say.__defaults__ = (0.82,)  # Experiment Einstieg (ab Tag 9)
LABEL = "KURIOS"

VOICE = timeline([
    "Eben noch dreißig Prozent. Jetzt aus.",
    "Das passiert im Winter ständig. Und dein Akku ist nicht kaputt.",
    "In der Kälte laufen die chemischen Vorgänge im Akku langsamer.",
    "Er liefert den Strom nicht mehr schnell genug, die Spannung bricht ein.",
    "Dein Handy denkt: leer. Und schaltet sich zur Sicherheit ab.",
    "Dabei ist die Energie noch da. Im Warmen kommt sie zurück.",
    "Mein Tipp: Handy in die Innentasche, nah am Körper.",
    "Und ein eiskaltes Handy erst aufwärmen lassen, dann laden.",
    ("Ist dir das schon passiert? Ja oder nein. Ab in die Kommentare.", 0.35),
])
WORDS = word_timings(VOICE)
END = VOICE[-1][0] + say(VOICE[-1][1])[1] + 0.9

# Szenengrenzen = Satzanfänge
T1, T2, T3, T4 = VOICE[2][0] - 0.12, VOICE[5][0] - 0.12, VOICE[6][0] - 0.12, VOICE[8][0] - 0.15


def _pick(q, i, kind="video"):
    return {h["id"]: h for h in stock_search(q, kind, n=20, lang="en")}[i]


CLIP_ICE = Clip(stock_get(_pick("frozen ice", 3147)), start=1.0)          # Eiszapfen (2016)
CLIP_BUBBLE = Clip(stock_get(_pick("frozen ice", 7105)), start=2.0)       # gefrierende Seifenblase (2017)
CLIP_FIRE = Clip(stock_get(_pick("warm jacket pocket", 1971)), start=1.0)  # Kaminfeuer (2016)
CLIP_FOREST = Clip(stock_get(_pick("winter cold snow", 29314)), start=2.0) # Tannen im Schnee (2019)
CLIP_PHONE = Clip(stock_get(_pick("snow phone", 61298)), start=3.0)       # Mann schaut aufs Handy (2021)

E = {k: at(WORDS, k) for k in ["Jetzt", "Winter", "kaputt", "Kälte", "langsamer", "Strom", "Spannung",
                               "leer", "schaltet", "Energie", "zurück", "Innentasche", "Körper",
                               "aufwärmen", "laden", "Ja", "nein", "Kommentare"]}


def pop(t, t0, d=0.18):
    x = max(0.0, min(1.0, (t - t0) / d))
    return x * (1 + 0.25 * math.sin(math.pi * x)) if x < 1 else 1.0


def big(d, y, s, size, col, k, dy=30):
    if k <= 0:
        return
    f = font(BLACK, max(8, int(size * (0.7 + 0.3 * min(k, 1.2)))))
    d.text((W // 2, y + int(dy * (1 - min(k, 1)))), s, font=f, fill=mix(BG, col, min(k, 1)), anchor="mm")


def battery(d, cx, cy, s, frac, col, a=1.0):
    """Akku-Symbol (liegend), frac = Füllstand 0..1."""
    w, h = int(420 * s), int(200 * s)
    x0, y0 = cx - w // 2, cy - h // 2
    oc = mix(BG, WH, a)
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=int(28 * s), outline=oc, width=int(12 * s))
    d.rounded_rectangle([x0 + w + int(4 * s), cy - int(40 * s), x0 + w + int(30 * s), cy + int(40 * s)],
                        radius=int(8 * s), fill=oc)
    if frac > 0.005:
        p = int(22 * s)
        d.rounded_rectangle([x0 + p, y0 + p, x0 + p + max(int(20 * s), int((w - 2 * p) * frac)), y0 + h - p],
                            radius=int(12 * s), fill=mix(BG, col, a))


def s1(t):  # Hook – Akku + Zahl stehen ab Frame 0, Zoom-Punch auf Stock
    img = stock_bg(CLIP_ICE, t, dim=0.55)
    img = punch(img, t)
    d = ImageDraw.Draw(img); header(d, LABEL)
    off = t >= E["Jetzt"]
    if not off:
        battery(d, W // 2, 560, 1.3, 0.3, SUB_HL)
        big(d, 860, "30 %", 230, WH, 1.0)
    else:
        k = pop(t, E["Jetzt"])
        battery(d, W // 2, 560, 1.3, 0.0, RD, 1.0)
        big(d, 860, "AUS", 250, RD, k)
    if t > E["Winter"] - 0.05:
        a = ease((t - E["Winter"] + 0.05) / 0.3)
        d.text((W // 2, 1060), "❄  IM WINTER  ❄", font=font(MONO, 50), fill=mix(BG, CY, a), anchor="mm")
    if t > E["kaputt"] - 0.05:
        kk = min(1, pop(t, E["kaputt"] - 0.05))
        d.rounded_rectangle([230, 1150, 850, 1250], radius=50, fill=mix(BG, GN, kk))
        d.text((W // 2, 1200), "NICHT KAPUTT", font=font(BLACK, 56), fill=BG, anchor="mm")
    return img


def s2(t0):  # Warum: Chemie langsamer → Spannung bricht ein → Abschaltung
    t = t0 + T1
    img = stock_bg(CLIP_BUBBLE, t0, dim=0.68); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    d.text((110, 420), "IM AKKU BEI KÄLTE", font=font(MONO, 44), fill=mix(BG, CY, a), anchor="ls")
    # Thermometer-Zeile
    big(d, 540, "KALT", 150, CY, a)
    if t > E["langsamer"] - 0.1:
        k = min(1, pop(t, E["langsamer"] - 0.1))
        d.rounded_rectangle([110, 680, 970, 800], radius=30, fill=mix(BG, PANEL, k))
        d.text((W // 2, 742), "Chemie läuft langsamer", font=font(BLACK, 58), fill=mix(BG, WH, k), anchor="mm")
    if t > E["Spannung"] - 0.1:  # Spannungsbalken fällt
        k = ease((t - E["Spannung"] + 0.1) / 0.7)
        x0, x1, y = 110, 970, 900
        d.text((x0, y - 24), "Spannung", font=font(SEMI, 46), fill=GR, anchor="ls")
        d.rounded_rectangle([x0, y, x1, y + 80], radius=40, fill=PANEL)
        frac = 0.85 - 0.6 * k
        col = mix(GN, RD, k)
        d.rounded_rectangle([x0, y, x0 + int((x1 - x0) * frac), y + 80], radius=40, fill=col)
        d.text((x1, y - 24), "▼", font=font(BLACK, 56), fill=col, anchor="rs")
    if t > E["leer"] - 0.1:
        k = pop(t, E["leer"] - 0.1)
        big(d, 1090, "HANDY: „LEER“", 96, SUB_HL, k)
    if t > E["schaltet"] - 0.05:
        k = min(1, pop(t, E["schaltet"] - 0.05))
        cx, cy, r = W // 2, 1225, 52  # Power-Symbol
        c = mix(BG, RD, k)
        d.arc([cx - r, cy - r, cx + r, cy + r], 300, 240, fill=c, width=12)
        d.line([(cx, cy - r - 8), (cx, cy - 6)], fill=c, width=12)
    return img


def s3(t0):  # Energie noch da – kommt im Warmen zurück
    t = t0 + T2
    img = stock_bg(CLIP_FIRE, t0, dim=0.6); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    big(d, 480, "ENERGIE", 130, WH, a)
    big(d, 620, "NOCH DA", 130, GN, a)
    k = ease((t - E["zurück"] + 0.1) / 0.8) if t > E["zurück"] - 0.1 else 0.0
    battery(d, W // 2, 900, 1.3, 0.05 + 0.25 * k, mix(RD, GN, k))
    if k > 0:
        big(d, 1170, "im Warmen: wieder da", 64, SUB_HL, min(1, k * 2))
    return img


def tip(d, y, num, txt, col, k):
    if k <= 0:
        return
    kk = min(1, k)
    d.rounded_rectangle([80, y, 1000, y + 190], radius=30, fill=mix(BG, PANEL, kk), outline=mix(BG, col, kk), width=4)
    d.ellipse([110, y + 45, 210, y + 145], fill=mix(BG, col, kk))
    d.text((160, y + 96), num, font=font(BLACK, 60), fill=BG, anchor="mm")
    for i, ln in enumerate(txt):
        d.text((250 + int(30 * (1 - kk)), y + 80 + i * 66), ln, font=font(BLACK, 54), fill=mix(BG, WH, kk), anchor="ls")


def s4(t0):  # Tipps
    t = t0 + T3
    img = stock_bg(CLIP_FOREST, t0, dim=0.7); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    big(d, 470, "SO HÄLT ER DURCH", 84, CY, a)
    tip(d, 590, "1", ["Innentasche,", "nah am Körper"], GN, pop(t, E["Innentasche"] - 0.1))
    tip(d, 830, "2", ["Erst aufwärmen,", "dann laden"], SUB_HL, pop(t, E["aufwärmen"] - 0.1))
    return img


def s5(t0):  # Interaktionsfrage
    t = t0 + T4
    img = stock_bg(CLIP_PHONE, t0, dim=0.68); d = ImageDraw.Draw(img); header(d, LABEL)
    k = pop(t, VOICE[8][0])
    big(d, 520, "SCHON PASSIERT?", 100, WH, k)
    for w, x, col in (("Ja", 330, GN), ("nein", 750, RD)):
        kk = pop(t, E[w] - 0.05)
        if kk > 0:
            a = min(1, kk)
            d.rounded_rectangle([x - 170, 680, x + 170, 840], radius=80, fill=mix(BG, col, a))
            d.text((x, 762), w.upper(), font=font(BLACK, 80), fill=BG, anchor="mm")
    kc = pop(t, E["Kommentare"])
    if kc > 0:
        a = min(1, kc); bounce = 12 * math.sin((t - E["Kommentare"]) * 9)
        d.text((W // 2, 960 + bounce), "↓  in die Kommentare  ↓", font=font(BLACK, 58), fill=mix(BG, SUB_HL, a), anchor="mm")
    kf = pop(t, END - 1.0)
    if kf > 0:
        d.text((W // 2, 1200), "Folgen = morgen schlauer", font=font(BLACK, 54), fill=mix(BG, CY, min(1, kf)), anchor="mm")
    return img


SCENES = [("s1", s1, T1), ("s2", s2, T2 - T1), ("s3", s3, T3 - T2), ("s4", s4, T4 - T3), ("s5", s5, END - T4)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for st, txt in VOICE:
            print(f"{st:5.2f}–{st + say(txt)[1]:5.2f}  {txt}")
        print(stills(SCENES, "/home/claude/bitweise-out/tag09", voice=VOICE))
    else:
        print(build(SCENES, "tag09_akku_kaelte", seed=9, voice=VOICE, sfx=[(0.0, "whoosh")]))
        write_credits("Tag 09 – Kurios: Akku bei Kälte")
