"""Tag 12 – Mythos-Check: Lädt der Flugmodus dein Handy schneller? (Format v3 + Experiment „Einstieg“:
Tempo 0,82, Hook-Satz ≤ 6 Wörter, Zoom-Punch in Sekunde 0; ab Tag 12 ohne Ton-Akzent)."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *
import math

say.__defaults__ = (0.82,)  # Experiment Einstieg (ab Tag 9)
LABEL = "MYTHOS-CHECK"

VOICE = timeline([
    "Flugmodus beim Laden: Turbo oder Mythos?",
    "Ehrliche Antwort: ein kleines bisschen Turbo.",
    "Im Flugmodus funkt dein Handy nicht mehr mit dem Mobilfunknetz.",
    "Es braucht also weniger Strom, und mehr davon landet im Akku.",
    "Am meisten bringt das bei schlechtem Empfang. Da funkt das Handy besonders kräftig.",
    "Aber meistens sparst du nur ein paar Minuten.",
    "Mehr bringt ein stärkeres Ladegerät, das dein Handy unterstützt. Und: Bildschirm aus, Handy kühl halten.",
    ("Jetzt du: Flugmodus beim Laden? Team Ja oder Team Nein. Ab in die Kommentare.", 0.35),
])
WORDS = word_timings(VOICE)
END = VOICE[-1][0] + say(VOICE[-1][1])[1] + 0.9

# Szenengrenzen = Satzanfänge
T1, T2, T3 = VOICE[2][0] - 0.12, VOICE[5][0] - 0.12, VOICE[7][0] - 0.15


def _pick(q, i, kind="video"):
    return {h["id"]: h for h in stock_search(q, kind, n=12, lang="en")}[i]


CLIP_PLUG = Clip(stock_get(_pick("phone charging", 44082)), start=0.3)      # Ladekabel wird eingesteckt (2020)
CLIP_TOWER = Clip(stock_get(_pick("cell tower", 58484)), start=2.0)         # Funkmast (2020)
CLIP_TABLE = Clip(stock_get(_pick("smartphone charger", 3176)), start=0.5)  # Handy auf Tisch (2016)
CLIP_HAND = Clip(stock_get(_pick("phone charging", 736)), start=0.0)        # Hand mit Handy (2015)

E = {k: at(WORDS, k) for k in ["Mythos", "kleines", "Turbo", "funkt", "nicht", "weniger", "Akku", "schlechtem",
                               "kräftig", "Minuten", "Ladegerät", "Bildschirm", "kühl", "Ja", "Nein", "Kommentare"]}
E["Turbo2"] = at(WORDS, "Turbo", 1)


def pop(t, t0, d=0.18):
    x = max(0.0, min(1.0, (t - t0) / d))
    return x * (1 + 0.25 * math.sin(math.pi * x)) if x < 1 else 1.0


def big(d, y, s, size, col, k, dy=30):
    if k <= 0:
        return
    f = font(BLACK, max(8, int(size * (0.7 + 0.3 * min(k, 1.2)))))
    d.text((W // 2, y + int(dy * (1 - min(k, 1)))), s, font=f, fill=mix(BG, col, min(k, 1)), anchor="mm")


def check(d, cx, cy, s, col, a):
    c = mix(BG, col, a)
    d.line([(cx - 22 * s, cy), (cx - 6 * s, cy + 16 * s), (cx + 24 * s, cy - 18 * s)], fill=c, width=int(9 * s), joint="curve")


def plane(d, cx, cy, s, col):
    """Einfaches Flugzeug-Symbol (von oben, Nase nach oben)."""
    p = lambda pts: [(cx + x * s, cy + y * s) for x, y in pts]
    d.rounded_rectangle([cx - 9 * s, cy - 60 * s, cx + 9 * s, cy + 55 * s], radius=int(9 * s), fill=col)
    d.polygon(p([(-8, -12), (-62, 14), (-62, 26), (-8, 12), (8, 12), (62, 26), (62, 14), (8, -12)]), fill=col)
    d.polygon(p([(-6, 38), (-26, 52), (-26, 60), (6, 52), (26, 60), (26, 52), (6, 38)]), fill=col)


def battery(d, x, y, w, h, frac, col, a):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, outline=mix(BG, WH, a), width=6)
    d.rectangle([x + w, y + h // 3, x + w + 14, y + 2 * h // 3], fill=mix(BG, WH, a))
    if frac > 0:
        d.rounded_rectangle([x + 12, y + 12, x + 12 + int((w - 24) * frac), y + h - 12], radius=8, fill=mix(BG, col, a))


def s1(t):  # Hook – steht ab Frame 0, Zoom-Punch
    img = stock_bg(CLIP_PLUG, t, dim=0.55)
    img = punch(img, t)
    d = ImageDraw.Draw(img); header(d, LABEL)
    plane(d, W // 2, 470, 1.5, CY)
    d.text((W // 2, 650), "FLUGMODUS", font=font(BLACK, 110), fill=WH, anchor="mm")
    d.text((W // 2, 760), "BEIM LADEN", font=font(BLACK, 80), fill=WH, anchor="mm")
    kv = pop(t, E["kleines"] - 0.1)
    if kv <= 0:  # Entweder-oder ab Frame 0
        d.text((W // 2 - 40, 930), "TURBO", font=font(BLACK, 90), fill=GN, anchor="rm")
        d.text((W // 2, 930), "/", font=font(BLACK, 90), fill=GR, anchor="mm")
        d.text((W // 2 + 40, 930), "MYTHOS?", font=font(BLACK, 90), fill=RD, anchor="lm")
    else:
        a = min(1, kv)
        d.rounded_rectangle([120, 860, 960, 1000], radius=70, fill=mix(BG, GN, a))
        d.text((W // 2, 930), "EIN BISSCHEN TURBO", font=font(BLACK, 66), fill=BG, anchor="mm")
        # Akku füllt sich etwas schneller
        battery(d, W // 2 - 150, 1080, 300, 130, min(1, 0.35 + (t - E["kleines"]) * 0.18), GN, a)
    return img


def waves(d, cx, cy, col, a, n=3):
    for i in range(n):
        r = 60 + i * 55
        d.arc([cx - r, cy - r, cx + r, cy + r], 220, 320, fill=mix(BG, col, a), width=14)


def s2(t0):  # Warum: weniger Funken
    t = t0 + T1
    img = stock_bg(CLIP_TOWER, t0, dim=0.74); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    big(d, 380, "WARUM?", 100, CY, a)
    kf = pop(t, E["funkt"] - 0.1)
    if kf > 0:  # Handy + Funkwellen, die bei „nicht“ durchgestrichen werden
        kk = min(1, kf)
        d.rounded_rectangle([W // 2 - 60, 650, W // 2 + 60, 850], radius=20, outline=mix(BG, WH, kk), width=8)
        waves(d, W // 2, 650, CY, kk)
        kn = pop(t, E["nicht"] - 0.05)
        if kn > 0:
            c = mix(BG, RD, min(1, kn))
            d.line([(W // 2 - 150, 470), (W // 2 + 150, 610)], fill=c, width=16)
            d.text((W // 2, 905), "kein Mobilfunk", font=font(BLACK, 58), fill=c, anchor="mm")
    kw = pop(t, E["weniger"] - 0.1)
    if kw > 0:
        kk = min(1, kw)
        d.text((130, 1030), "Verbrauch", font=font(BLACK, 56), fill=mix(BG, WH, kk), anchor="ls")
        d.text((950, 1030), "weniger", font=font(BLACK, 56), fill=mix(BG, GN, kk), anchor="rs")
    ka = pop(t, E["Akku"] - 0.1)
    if ka > 0:
        kk = min(1, ka)
        d.text((130, 1110), "In den Akku", font=font(BLACK, 56), fill=mix(BG, WH, kk), anchor="ls")
        d.text((950, 1110), "mehr", font=font(BLACK, 56), fill=mix(BG, GN, kk), anchor="rs")
    ks = pop(t, E["schlechtem"] - 0.1)
    if ks > 0:  # Empfangsbalken: 1 von 4
        kk = min(1, ks)
        for i in range(4):
            x = 130 + i * 42; hh = 24 + i * 22
            d.rectangle([x, 1215 - hh, x + 30, 1215], fill=mix(BG, (RD if i == 0 else PANEL), kk))
        d.text((320, 1210), "Schwacher Empfang", font=font(BLACK, 54), fill=mix(BG, WH, kk), anchor="ls")
        kp = pop(t, E["kräftig"] - 0.25)
        if kp > 0:
            d.text((320, 1285), "= größter Effekt", font=font(BLACK, 54), fill=mix(BG, SUB_HL, min(1, kp)), anchor="ls")
    return img


def s3(t0):  # Aber: kleiner Effekt, was mehr bringt
    t = t0 + T2
    img = stock_bg(CLIP_TABLE, t0, dim=0.74); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    big(d, 430, "ABER", 110, RD, a)
    km = pop(t, E["Minuten"] - 0.15)
    big(d, 545, "meist nur ein paar Minuten", 60, WH, km)
    kh = pop(t, E["Ladegerät"] - 0.4)
    big(d, 680, "MEHR BRINGT:", 72, CY, kh)
    items = [("Ladegerät", "Stärkeres Ladegerät"), ("Bildschirm", "Bildschirm aus"), ("kühl", "Handy kühl halten")]
    for i, (w, txt) in enumerate(items):
        k = pop(t, E[w] - 0.05)
        if k <= 0:
            continue
        kk = min(1, k); y = 760 + i * 170
        d.rounded_rectangle([90, y, 990, y + 140], radius=28, fill=mix(BG, PANEL, kk), outline=mix(BG, GN, kk * 0.8), width=4)
        check(d, 170, y + 72, 1.2, GN, kk)
        d.text((250 + int(30 * (1 - kk)), y + 92), txt, font=font(BLACK, 58), fill=mix(BG, WH, kk), anchor="ls")
    return img


def s4(t0):  # Interaktionsfrage
    t = t0 + T3
    img = stock_bg(CLIP_HAND, t0, dim=0.68); d = ImageDraw.Draw(img); header(d, LABEL)
    k = pop(t, VOICE[7][0])
    big(d, 430, "JETZT DU", 80, CY, k)
    kq = pop(t, VOICE[7][0] + 0.4)
    big(d, 545, "Flugmodus", 96, WH, kq)
    big(d, 650, "beim Laden?", 96, WH, kq)
    for w, lab, x, col in (("Ja", "TEAM JA", 300, GN), ("Nein", "TEAM NEIN", 780, RD)):
        kk = pop(t, E[w] - 0.05)
        if kk > 0:
            a = min(1, kk)
            d.rounded_rectangle([x - 220, 770, x + 220, 920], radius=75, fill=mix(BG, col, a))
            d.text((x, 847), lab, font=font(BLACK, 66), fill=BG, anchor="mm")
    kc = pop(t, E["Kommentare"])
    if kc > 0:
        a = min(1, kc)
        d.rounded_rectangle([170, 990, 910, 1110], radius=60, fill=mix(BG, PANEL, a), outline=mix(BG, SUB_HL, a), width=4)
        d.text((W // 2, 1052), "Ab in die Kommentare", font=font(BLACK, 56), fill=mix(BG, SUB_HL, a), anchor="mm")
    kf = pop(t, END - 1.0)
    if kf > 0:
        d.text((W // 2, 1220), "Folgen = morgen schlauer", font=font(BLACK, 54), fill=mix(BG, CY, min(1, kf)), anchor="mm")
    return img


SCENES = [("s1", s1, T1), ("s2", s2, T2 - T1), ("s3", s3, T3 - T2), ("s4", s4, END - T3)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for st, txt in VOICE:
            print(f"{st:5.2f}–{st + say(txt)[1]:5.2f}  {txt}")
        print(f"END {END:.2f}")
        print(stills(SCENES, "/home/claude/bitweise-out/tag12", voice=VOICE))
    else:
        print(build(SCENES, "tag12_flugmodus", seed=12, voice=VOICE))
        write_credits("Tag 12 – Mythos-Check: Lädt der Flugmodus schneller?")
