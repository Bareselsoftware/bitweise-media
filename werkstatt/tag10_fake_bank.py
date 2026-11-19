"""Tag 10 – Alltags-Trick: Falsche Bank-/PayPal-Nachricht in 3 Sekunden erkennen (Format v3 + Experiment „Einstieg“:
Tempo 0,82, Hook-Satz ≤ 6 Wörter, Zoom-Punch + Whoosh in Sekunde 0)."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *
import math

say.__defaults__ = (0.82,)  # Experiment Einstieg (ab Tag 9)
LABEL = "ALLTAGS-TRICK"

VOICE = timeline([
    "Konto gesperrt? Bitte nicht klicken.",
    "Im November sind wieder massenhaft falsche Nachrichten von PayPal und Banken unterwegs.",
    "So erkennst du sie in drei Sekunden.",
    "Erstens: Zeitdruck. Sofort, heute noch, sonst gesperrt.",
    "Zweitens: ein Link, über den du deine Daten bestätigen sollst.",
    "Drittens: Die Adresse sieht nur fast echt aus.",
    "Und merk dir: Deine Bank fragt nie per SMS oder E-Mail nach Passwort oder TAN.",
    "Also: Link ignorieren, die App selbst öffnen und dort nachschauen.",
    ("Hast du so eine schon bekommen? Ja oder nein. Und schick das deinen Eltern.", 0.35),
])
WORDS = word_timings(VOICE)
END = VOICE[-1][0] + say(VOICE[-1][1])[1] + 0.9

# Szenengrenzen = Satzanfänge
T1, T2, T3, T4 = VOICE[2][0] - 0.12, VOICE[6][0] - 0.12, VOICE[7][0] - 0.12, VOICE[8][0] - 0.15


def _pick(q, i, kind="video"):
    return {h["id"]: h for h in stock_search(q, kind, n=20, lang="en")}[i]


CLIP_THUMBS = Clip(stock_get(_pick("smartphone message", 9490)), start=1.0)   # Daumen tippen aufs Handy (2017)
CLIP_SCREEN = Clip(stock_get(_pick("smartphone message", 3172)), start=1.0)   # Handy-Display Nahaufnahme (2016)
CLIP_TAP = Clip(stock_get(_pick("phone hand typing", 3176)), start=1.0)       # Finger tippt auf Handy (2016)
CLIP_KEYS = Clip(stock_get(_pick("phone hand typing", 10822)), start=1.0)     # Tastatur (2017)
CLIP_STREET = Clip(stock_get(_pick("bank card phone", 6590)), start=1.0)      # Mann mit Handy auf der Straße (2016)

E = {k: at(WORDS, k) for k in ["Bitte", "klicken", "November", "PayPal", "drei", "Zeitdruck", "Sofort", "heute",
                               "gesperrt", "Link", "bestätigen", "Adresse", "echt", "nie", "Passwort", "TAN",
                               "ignorieren", "App", "nachschauen", "Ja", "nein", "Eltern"]}
E["gesperrt2"] = at(WORDS, "gesperrt", 1)
E["Link2"] = at(WORDS, "Link", 1)


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


def sms(d, y, a=1.0, hl=None):
    """Nachgebaute Fake-SMS (fiktiver Absender, fiktive Adresse). hl: 'zeit' | 'link' | 'adr' hebt Teil rot hervor."""
    x0, x1 = 110, 970
    d.text((x0 + 10, y - 20), "SMS · jetzt", font=font(SEMI, 36), fill=mix(BG, GR, a), anchor="ls")
    d.rounded_rectangle([x0, y, x1, y + 330], radius=40, fill=mix(BG, (44, 52, 64), a))
    rows = [("Ihr Konto wird gesperrt!", "zeit", WH), ("Bestätigen Sie heute noch", "zeit", WH),
            ("Ihre Daten unter:", "link", WH), ("konto-sicher-pruefen.xyz/login", "adr", CY)]
    for i, (txt, key, col) in enumerate(rows):
        yy = y + 70 + i * 70
        f = font(BLACK if i == 0 else SEMI, 50 if i < 3 else 44)
        c = mix(BG, col, a)
        if hl == key or (hl == "link" and key == "adr"):
            tw = d.textlength(txt, font=f)
            d.rounded_rectangle([x0 + 30, yy - 46, x0 + 50 + tw, yy + 14], radius=12, fill=mix(BG, RD, a * 0.85))
            c = mix(BG, WH, a)
        d.text((x0 + 40, yy), txt, font=f, fill=c, anchor="ls")


def s1(t):  # Hook – Fake-SMS steht ab Frame 0, Zoom-Punch auf Stock
    img = stock_bg(CLIP_THUMBS, t, dim=0.6)
    img = punch(img, t)
    d = ImageDraw.Draw(img); header(d, LABEL)
    sms(d, 470)
    if t > E["Bitte"] - 0.05:
        k = pop(t, E["Bitte"] - 0.05)
        kk = min(1, k)
        d.rounded_rectangle([200, 870, 880, 1000], radius=65, fill=mix(BG, RD, kk))
        d.text((W // 2, 937), "NICHT KLICKEN", font=font(BLACK, 70), fill=BG, anchor="mm")
    if t > E["November"] - 0.05:
        a = ease((t - E["November"] + 0.05) / 0.3)
        d.text((W // 2, 1085), "NOVEMBER-WELLE", font=font(MONO, 50), fill=mix(BG, CY, a), anchor="mm")
    if t > E["PayPal"] - 0.05:
        k = pop(t, E["PayPal"] - 0.05)
        big(d, 1190, "PayPal · Banken", 78, WH, k)
    return img


def card(d, y, num, title, k, col=RD):
    if k <= 0:
        return
    kk = min(1, k)
    d.rounded_rectangle([80, y, 1000, y + 120], radius=28, fill=mix(BG, PANEL, kk), outline=mix(BG, col, kk), width=4)
    d.ellipse([105, y + 20, 185, y + 100], fill=mix(BG, col, kk))
    d.text((145, y + 61), num, font=font(BLACK, 50), fill=BG, anchor="mm")
    d.text((220 + int(30 * (1 - kk)), y + 80), title, font=font(BLACK, 56), fill=mix(BG, WH, kk), anchor="ls")


def s2(t0):  # 3 Erkennungszeichen, SMS wird jeweils markiert
    t = t0 + T1
    img = stock_bg(CLIP_SCREEN, t0, dim=0.72); d = ImageDraw.Draw(img); header(d, LABEL)
    k3 = pop(t, E["drei"] - 0.05)
    big(d, 415, "IN 3 SEKUNDEN ERKANNT", 70, CY, max(ease(t0 / 0.3), min(1, k3)))
    hl = None
    if t > E["Zeitdruck"] - 0.1: hl = "zeit"
    if t > E["Link"] - 0.1: hl = "link"
    if t > E["Adresse"] - 0.1: hl = "adr"
    sms(d, 540, ease(t0 / 0.3), hl)
    card(d, 920, "1", "Zeitdruck", pop(t, E["Zeitdruck"] - 0.1))
    card(d, 1050, "2", "Link „Daten bestätigen“", pop(t, E["Link"] - 0.1))
    card(d, 1180, "3", "Adresse nur fast echt", pop(t, E["Adresse"] - 0.1))
    return img


def s3(t0):  # Bank fragt nie nach Passwort/TAN
    t = t0 + T2
    img = stock_bg(CLIP_TAP, t0, dim=0.7); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    big(d, 470, "DEINE BANK FRAGT", 84, WH, a)
    kn = pop(t, E["nie"] - 0.05)
    big(d, 620, "NIE", 200, RD, kn)
    big(d, 780, "per SMS oder E-Mail", 64, GR, kn)
    for w, y in (("Passwort", 900), ("TAN", 1060)):
        k = pop(t, E[w] - 0.08)
        if k > 0:
            kk = min(1, k)
            d.rounded_rectangle([200, y, 880, y + 130], radius=30, fill=mix(BG, PANEL, kk), outline=mix(BG, RD, kk), width=4)
            cross(d, 280, y + 65, 1.4, RD, kk)
            d.text((360, y + 88), w, font=font(BLACK, 70), fill=mix(BG, WH, kk), anchor="ls")
    return img


def s4(t0):  # Richtig machen
    t = t0 + T3
    img = stock_bg(CLIP_KEYS, t0, dim=0.72); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    big(d, 470, "SO MACHST DU’S", 84, CY, a)
    steps = [("ignorieren", "Link ignorieren", RD, False), ("App", "App selbst öffnen", GN, True),
             ("nachschauen", "Dort nachschauen", GN, True)]
    for i, (w, txt, col, ok) in enumerate(steps):
        k = pop(t, E[w] - 0.08)
        if k <= 0:
            continue
        kk = min(1, k); y = 580 + i * 190
        d.rounded_rectangle([90, y, 990, y + 150], radius=28, fill=mix(BG, PANEL, kk), outline=mix(BG, col, kk * 0.9), width=4)
        (check if ok else cross)(d, 180, y + 75, 1.3, col, kk)
        d.text((270 + int(30 * (1 - kk)), y + 98), txt, font=font(BLACK, 62), fill=mix(BG, WH, kk), anchor="ls")
    return img


def s5(t0):  # Interaktionsfrage + Teilen
    t = t0 + T4
    img = stock_bg(CLIP_STREET, t0, dim=0.68); d = ImageDraw.Draw(img); header(d, LABEL)
    k = pop(t, VOICE[8][0])
    big(d, 480, "SCHON BEKOMMEN?", 96, WH, k)
    for w, x, col in (("Ja", 330, GN), ("nein", 750, RD)):
        kk = pop(t, E[w] - 0.05)
        if kk > 0:
            a = min(1, kk)
            d.rounded_rectangle([x - 170, 620, x + 170, 780], radius=80, fill=mix(BG, col, a))
            d.text((x, 702), w.upper(), font=font(BLACK, 80), fill=BG, anchor="mm")
    ke = pop(t, E["Eltern"] - 0.3)
    if ke > 0:
        a = min(1, ke)
        d.rounded_rectangle([140, 880, 940, 1020], radius=70, fill=mix(BG, PANEL, a), outline=mix(BG, SUB_HL, a), width=4)
        d.text((W // 2, 952), "Schick’s deinen Eltern", font=font(BLACK, 58), fill=mix(BG, SUB_HL, a), anchor="mm")
    kf = pop(t, END - 1.0)
    if kf > 0:
        d.text((W // 2, 1200), "Folgen = morgen schlauer", font=font(BLACK, 54), fill=mix(BG, CY, min(1, kf)), anchor="mm")
    return img


SCENES = [("s1", s1, T1), ("s2", s2, T2 - T1), ("s3", s3, T3 - T2), ("s4", s4, T4 - T3), ("s5", s5, END - T4)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for st, txt in VOICE:
            print(f"{st:5.2f}–{st + say(txt)[1]:5.2f}  {txt}")
        print(stills(SCENES, "/home/claude/bitweise-out/tag10", voice=VOICE))
    else:
        print(build(SCENES, "tag10_fake_bank", seed=10, voice=VOICE, sfx=[(0.0, "whoosh")]))
        write_credits("Tag 10 – Alltags-Trick: Falsche Bank-/PayPal-Nachricht")
