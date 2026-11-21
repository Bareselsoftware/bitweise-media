"""Tag 11 – Kurios: Warum Captchas dich nach Ampeln fragen (Format v3 + Experiment „Einstieg“:
Tempo 0,82, Hook-Satz ≤ 6 Wörter, Zoom-Punch + Whoosh in Sekunde 0).
Captcha-Kasten ist nachgebaut (kein Logo, keine Marke)."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *
import math

say.__defaults__ = (0.82,)  # Experiment Einstieg (ab Tag 9)
LABEL = "KURIOS"

VOICE = timeline([
    "Warum immer diese Ampeln?",
    "Diese Bilderrätsel heißen Captchas. Sie prüfen, ob du ein Mensch bist oder ein Bot.",
    "Der echte Test kommt aber oft schon vorher.",
    "Beim Häkchen „Ich bin kein Roboter“ schaut das System, wie du dich auf der Seite verhältst.",
    "Wirkt das verdächtig, kommen die Bilder.",
    "Und warum Straßen? Ampeln, Busse, Zebrastreifen erkennst du sofort. Computer hatten damit lange Probleme.",
    "Laut Google helfen deine Klicks nebenbei, Bilder zu beschriften und Maschinen zu trainieren.",
    ("Jetzt die wichtigste Frage: Gehört der Mast zur Ampel? Ja oder nein. Ab in die Kommentare.", 0.35),
])
WORDS = word_timings(VOICE)
END = VOICE[-1][0] + say(VOICE[-1][1])[1] + 0.9

# Szenengrenzen = Satzanfänge
T1, T2, T3, T4 = VOICE[2][0] - 0.12, VOICE[5][0] - 0.12, VOICE[6][0] - 0.12, VOICE[7][0] - 0.15


def _pick(q, i, kind="video"):
    return {h["id"]: h for h in stock_search(q, kind, n=12, lang="en")}[i]


CLIP_AMPEL = Clip(stock_get(_pick("traffic light", 37844)), start=0.5)       # Fahrradampel (2020)
CLIP_MOUSE = Clip(stock_get(_pick("computer mouse hand", 127)), start=1.0)   # Hand an Maus (2015)
CLIP_STREET = Clip(stock_get(_pick("traffic light", 98176)), start=1.0)      # Kreuzung (2021)
CLIP_ROAD = Clip(stock_get(_pick("traffic light", 23712)), start=1.0)        # Straße von oben (2019)
FOTO = Image.open(stock_get(_pick("traffic light", 6803755, "photo"))).convert("RGB")  # Ampel am Mast (2021)
TILE_SRC = FOTO.crop((290, 120, 720, 550))  # quadratischer Ausschnitt: Ampeln + Mast

E = {k: at(WORDS, k) for k in ["Ampeln", "Captchas", "Mensch", "Bot", "echte", "vorher", "Häkchen",
                               "System", "verhältst", "verdächtig", "Bilder", "Straßen", "Busse", "Zebrastreifen",
                               "sofort", "Computer", "Probleme", "Google", "beschriften", "trainieren",
                               "Mast", "Ja", "nein", "Kommentare"]}
E["Ampeln2"] = at(WORDS, "Ampeln", 1)


def pop(t, t0, d=0.18):
    x = max(0.0, min(1.0, (t - t0) / d))
    return x * (1 + 0.25 * math.sin(math.pi * x)) if x < 1 else 1.0


def big(d, y, s, size, col, k, dy=30):
    if k <= 0:
        return
    f = font(BLACK, max(8, int(size * (0.7 + 0.3 * min(k, 1.2)))))
    d.text((W // 2, y + int(dy * (1 - min(k, 1)))), s, font=f, fill=mix(BG, col, min(k, 1)), anchor="mm")


def cross(d, cx, cy, s, col, a):
    c = mix(BG, col, a); r = int(22 * s)
    d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=c, width=int(9 * s))
    d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=c, width=int(9 * s))


def check(d, cx, cy, s, col, a):
    c = mix(BG, col, a)
    d.line([(cx - 22 * s, cy), (cx - 6 * s, cy + 16 * s), (cx + 24 * s, cy - 18 * s)], fill=c, width=int(9 * s), joint="curve")


def captcha(img, y, size=640, picked=(), a=1.0):
    """Nachgebauter Bilder-Captcha-Kasten (4×4 aus einem Foto). picked = Kachel-Indizes mit Haken."""
    d = ImageDraw.Draw(img)
    x0 = (W - size) // 2
    d.rectangle([x0 - 14, y - 150, x0 + size + 14, y + size + 14], fill=mix(BG, (250, 250, 250), a))
    d.rectangle([x0, y - 136, x0 + size, y - 14], fill=mix(BG, (40, 120, 230), a))
    d.text((x0 + 28, y - 96), "Wähle alle Bilder mit", font=font(SEMI, 38), fill=mix(BG, WH, a), anchor="ls")
    d.text((x0 + 28, y - 36), "AMPELN", font=font(BLACK, 58), fill=mix(BG, WH, a), anchor="ls")
    tile = TILE_SRC.resize((size, size), Image.LANCZOS)
    if a < 1:
        tile = Image.blend(Image.new("RGB", tile.size, BG), tile, a)
    img.paste(tile, (x0, y))
    n = 4; c = size // n
    for i in range(1, n):
        d.line([(x0 + i * c, y), (x0 + i * c, y + size)], fill=mix(BG, (250, 250, 250), a), width=6)
        d.line([(x0, y + i * c), (x0 + size, y + i * c)], fill=mix(BG, (250, 250, 250), a), width=6)
    for idx, k in picked:
        if k <= 0:
            continue
        kk = min(1, k); cx, cy = x0 + (idx % n) * c + c // 2, y + (idx // n) * c + c // 2
        d.rectangle([cx - c // 2 + 4, cy - c // 2 + 4, cx + c // 2 - 4, cy + c // 2 - 4], outline=mix(BG, (40, 120, 230), kk), width=8)
        d.ellipse([cx - c // 2 + 10, cy - c // 2 + 10, cx - c // 2 + 60, cy - c // 2 + 60], fill=mix(BG, (40, 120, 230), kk))
        check(d, cx - c // 2 + 35, cy - c // 2 + 37, 0.7, WH, kk)
    return d


def s1(t):  # Hook – Captcha steht ab Frame 0, Zoom-Punch + Kacheln werden angeklickt
    img = stock_bg(CLIP_AMPEL, t, dim=0.6)
    img = punch(img, t)
    d = ImageDraw.Draw(img); header(d, LABEL)
    # Kacheln mit Ampel (Ausschnitt 290–720 × 120–550): Spalten 1–2, Reihen 0–2
    clicks = [(5, 0.35), (1, 0.75), (6, 1.1), (9, 1.45), (2, E["Captchas"]), (10, E["Mensch"] - 0.3)]
    captcha(img, 400, picked=[(i, pop(t, ts)) for i, ts in clicks])
    d = ImageDraw.Draw(img)
    if t < E["Captchas"] - 0.05:  # Hook-Zeile ab Frame 0
        d.text((W // 2, 1150), "WARUM IMMER AMPELN?", font=font(BLACK, 76), fill=WH, anchor="mm")
    else:
        k = pop(t, E["Captchas"] - 0.05)
        big(d, 1120, "CAPTCHA", 96, CY, k)
    if t > E["Mensch"] - 0.05:
        a = ease((t - E["Mensch"] + 0.05) / 0.3)
        d.text((W // 2 - 40, 1235), "MENSCH", font=font(BLACK, 62), fill=mix(BG, GN, a), anchor="rm")
        d.text((W // 2, 1235), "/", font=font(BLACK, 62), fill=mix(BG, GR, a), anchor="mm")
    if t > E["Bot"] - 0.05:
        a = ease((t - E["Bot"] + 0.05) / 0.3)
        d.text((W // 2 + 40, 1235), "BOT", font=font(BLACK, 62), fill=mix(BG, RD, a), anchor="lm")
    return img


def s2(t0):  # Der eigentliche Test: Verhalten beim Häkchen
    t = t0 + T1
    img = stock_bg(CLIP_MOUSE, t0, dim=0.72); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    big(d, 440, "DER ECHTE TEST", 92, CY, a)
    big(d, 545, "läuft vorher", 64, GR, pop(t, E["vorher"] - 0.1))
    kh = pop(t, E["Häkchen"] - 0.1)
    if kh > 0:  # Kästchen „Ich bin kein Roboter“ (nachgebaut, ohne Logo)
        kk = min(1, kh)
        d.rounded_rectangle([130, 650, 950, 800], radius=18, fill=mix(BG, (250, 250, 250), kk))
        d.rectangle([180, 690, 250, 760], outline=mix(BG, (120, 120, 120), kk), width=5)
        d.text((290, 742), "Ich bin kein Roboter", font=font(SEMI, 52), fill=mix(BG, (30, 30, 30), kk), anchor="ls")
        kc = pop(t, E["System"] + 0.2)
        if kc > 0:
            check(d, 215, 727, 1.2, GN, min(1, kc))
    ks = pop(t, E["System"] - 0.05)
    if ks > 0:  # Maus-Spur: Punkte, die nach und nach erscheinen
        n = int(min(1, (t - E["System"]) / 1.6) * 14) + 1
        for i in range(n):
            x = 220 + i * 50; y = 1010 + 60 * math.sin(i * 0.7)
            d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=mix(BG, CY, min(1, ks) * (0.4 + 0.6 * i / 14)))
        d.text((W // 2, 900), "Wie verhältst du dich?", font=font(BLACK, 58), fill=mix(BG, WH, min(1, ks)), anchor="mm")
    kv = pop(t, E["verdächtig"] - 0.1)
    if kv > 0:
        kk = min(1, kv)
        d.rounded_rectangle([140, 1130, 940, 1260], radius=30, fill=mix(BG, PANEL, kk), outline=mix(BG, RD, kk), width=4)
        d.text((W // 2, 1197), "Verdächtig → Bilder", font=font(BLACK, 62), fill=mix(BG, WH, kk), anchor="mm")
    return img


def chip(d, y, txt, k, t, tc):
    if k <= 0:
        return
    kk = min(1, k)
    d.rounded_rectangle([110, y, 970, y + 130], radius=28, fill=mix(BG, PANEL, kk), outline=mix(BG, CY, kk * 0.8), width=4)
    d.text((160 + int(30 * (1 - kk)), y + 88), txt, font=font(BLACK, 62), fill=mix(BG, WH, kk), anchor="ls")
    km = pop(t, E["sofort"] - 0.05)
    if km > 0:
        d.text((735, y + 88), "Du", font=font(SEMI, 40), fill=mix(BG, GR, min(1, km)), anchor="rs")
        check(d, 780, y + 62, 1.0, GN, min(1, km))
    kc = pop(t, tc)
    if kc > 0:
        d.text((885, y + 88), "PC", font=font(SEMI, 40), fill=mix(BG, GR, min(1, kc)), anchor="rs")
        cross(d, 930, y + 64, 0.9, RD, min(1, kc))


def s3(t0):  # Warum Straßenbilder?
    t = t0 + T2
    img = stock_bg(CLIP_STREET, t0, dim=0.72); d = ImageDraw.Draw(img); header(d, LABEL)
    k = pop(t, E["Straßen"] - 0.1)
    big(d, 450, "WARUM STRASSEN?", 92, CY, max(ease(t0 / 0.3), min(1, k)))
    for i, (w, txt) in enumerate((("Ampeln2", "Ampel"), ("Busse", "Bus"), ("Zebrastreifen", "Zebrastreifen"))):
        chip(d, 590 + i * 170, txt, pop(t, E[w] - 0.08), t, E["Computer"] + i * 0.15)
    kp = pop(t, E["Probleme"] - 0.1)
    big(d, 1170, "Computer: lange schwer", 62, RD, kp)
    return img


def s4(t0):  # Nebeneffekt: Daten für Maschinen
    t = t0 + T3
    img = stock_bg(CLIP_ROAD, t0, dim=0.7); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    big(d, 450, "NEBENEFFEKT", 96, CY, a)
    kb = pop(t, E["beschriften"] - 0.1)
    if kb > 0:  # Kachel mit Etikett „Ampel“
        kk = min(1, kb)
        tile = TILE_SRC.resize((360, 360), Image.LANCZOS)
        tile = Image.blend(Image.new("RGB", tile.size, BG), tile, kk)
        img.paste(tile, (W // 2 - 180, 560))
        d = ImageDraw.Draw(img)
        d.rounded_rectangle([W // 2 - 140, 880, W // 2 + 140, 960], radius=20, fill=mix(BG, SUB_HL, kk))
        d.text((W // 2, 922), "„Ampel“", font=font(BLACK, 54), fill=BG, anchor="mm")
    kt = pop(t, E["trainieren"] - 0.1)
    big(d, 1060, "→ Maschinen lernen", 70, WH, kt)
    big(d, 1170, "(laut Google)", 48, GR, pop(t, E["Google"] - 0.05))
    return img


def s5(t0):  # Interaktionsfrage
    t = t0 + T4
    img = stock_bg(CLIP_AMPEL, t0 + 4.0, dim=0.68); d = ImageDraw.Draw(img); header(d, LABEL)
    k = pop(t, VOICE[7][0])
    big(d, 430, "WICHTIGSTE FRAGE", 70, CY, k)
    km = pop(t, E["Mast"] - 0.3)
    big(d, 540, "Gehört der Mast", 90, WH, km)
    big(d, 640, "zur Ampel?", 90, WH, km)
    for w, x, col in (("Ja", 330, GN), ("nein", 750, RD)):
        kk = pop(t, E[w] - 0.05)
        if kk > 0:
            a = min(1, kk)
            d.rounded_rectangle([x - 170, 760, x + 170, 920], radius=80, fill=mix(BG, col, a))
            d.text((x, 842), w.upper(), font=font(BLACK, 80), fill=BG, anchor="mm")
    kc = pop(t, E["Kommentare"])
    if kc > 0:
        a = min(1, kc)
        d.rounded_rectangle([170, 990, 910, 1110], radius=60, fill=mix(BG, PANEL, a), outline=mix(BG, SUB_HL, a), width=4)
        d.text((W // 2, 1052), "Ab in die Kommentare", font=font(BLACK, 56), fill=mix(BG, SUB_HL, a), anchor="mm")
    kf = pop(t, END - 1.0)
    if kf > 0:
        d.text((W // 2, 1220), "Folgen = morgen schlauer", font=font(BLACK, 54), fill=mix(BG, CY, min(1, kf)), anchor="mm")
    return img


SCENES = [("s1", s1, T1), ("s2", s2, T2 - T1), ("s3", s3, T3 - T2), ("s4", s4, T4 - T3), ("s5", s5, END - T4)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for st, txt in VOICE:
            print(f"{st:5.2f}–{st + say(txt)[1]:5.2f}  {txt}")
        print(f"END {END:.2f}")
        print(stills(SCENES, "/home/claude/bitweise-out/tag11", voice=VOICE))
    else:
        print(build(SCENES, "tag11_captcha", seed=11, voice=VOICE, sfx=[(0.0, "swish")]))
        write_credits("Tag 11 – Kurios: Warum Captchas nach Ampeln fragen")
