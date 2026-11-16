"""Tag 07 – Mythos-Check: Hört dein Handy heimlich mit? (Format v3)
Fakten: Northeastern University 2018 (Pan et al.) – 17.260 Android-Apps getestet, keine heimlichen
Audio-Aufnahmen/-Übertragungen gefunden. Werbe-Targeting über Standort, Suchen, gemeinsame IP/WLAN.
Mikro-Anzeige: iOS ab 14 oranger Punkt, Android ab 12 grünes Symbol oben rechts."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *
import math

say.__defaults__ = (0.9,)
LABEL = "MYTHOS-CHECK"
ORANGE = (255, 159, 10)

VOICE = timeline([
    "Du redest über neue Sneaker. Eine Stunde später: Sneaker-Werbung.",
    "Hört dein Handy also heimlich mit? Ich hab's geprüft.",
    "Forscher haben über siebzehntausend Apps getestet.",
    "Sie fanden keine einzige, die heimlich Gespräche verschickt.",
    "Mithören ist nämlich gar nicht nötig.",
    "Werbefirmen kennen deinen Standort, deine Suchen und oft auch, was andere in deinem WLAN suchen.",
    "Hat dein Kumpel nach Sneakern gesucht, landet die Werbung auch bei dir.",
    "Und wenn das Mikro wirklich an ist, zeigt dein Handy oben ein kleines Symbol.",
    ("Ist dir das schon mal passiert? Ja oder Nein?", 0.35),
    ("Ab in die Kommentare.", 0.2),
])
WORDS = word_timings(VOICE)
END = VOICE[-1][0] + say(VOICE[-1][1])[1] + 1.0

T1, T2, T3 = VOICE[2][0] - 0.1, VOICE[5][0] - 0.15, VOICE[7][0] - 0.15  # VOICE[8], [9] = Schlussfrage


def _pick(q, i, kind="video"):
    return {h["id"]: h for h in stock_search(q, kind, n=20, lang="en")}[i]


CLIP_SHOE = Clip(stock_get(_pick("sneakers shoes", 84885)), start=0.5)      # Sneaker (2021)
CLIP_TYPE = Clip(stock_get(_pick("smartphone table", 9490)), start=0.5)     # tippen (2017)
CLIP_ROUTER = Clip(stock_get(_pick("wifi router", 45535)), start=0.0)       # Router (2020)
CLIP_HOLD = Clip(stock_get(_pick("smartphone table", 38084)), start=0.5)    # Handy in der Hand (2020)

E = {k: at(WORDS, k) for k in ["Stunde", "Sneaker-Werbung.", "heimlich", "geprüft.", "siebzehntausend", "keine",
                               "Gespräche", "Mithören", "nötig.", "Standort,", "Suchen", "WLAN", "Kumpel",
                               "dir.", "Mikro", "Symbol.", "passiert?", "Ja", "Nein?", "Kommentare."]}


def pop(t, t0, d=0.18):
    x = max(0.0, min(1.0, (t - t0) / d))
    return x * (1 + 0.25 * math.sin(math.pi * x)) if x < 1 else 1.0


def big(d, y, s, size, col, k, dy=30):
    if k <= 0:
        return
    f = font(BLACK, max(8, int(size * (0.7 + 0.3 * min(k, 1.2)))))
    d.text((W // 2, y + int(dy * (1 - min(k, 1)))), s, font=f, fill=mix(BG, col, min(k, 1)), anchor="mm")


def mic(d, cx, cy, s, col):
    d.rounded_rectangle([cx - 22 * s, cy - 48 * s, cx + 22 * s, cy + 14 * s], radius=int(22 * s), fill=col)
    d.arc([cx - 38 * s, cy - 30 * s, cx + 38 * s, cy + 34 * s], 0, 180, fill=col, width=int(8 * s))
    d.line([(cx, cy + 34 * s), (cx, cy + 58 * s)], fill=col, width=int(8 * s))
    d.line([(cx - 24 * s, cy + 58 * s), (cx + 24 * s, cy + 58 * s)], fill=col, width=int(8 * s))


def s1(t):  # Hook – steht ab Frame 0
    img = stock_bg(CLIP_SHOE, t, dim=0.55); d = ImageDraw.Draw(img); header(d, LABEL)
    fade = 1 - 0.6 * min(1, pop(t, E["heimlich"] - 0.3))
    d.text((W // 2, 440), "DU REDEST ÜBER", font=font(MONO, 46), fill=mix(BG, GR, fade), anchor="mm")
    big(d, 560, "SNEAKER", 170, mix(BG, WH, fade), 1.0)
    ks = pop(t, E["Stunde"] - 0.15)
    if ks > 0:
        a = min(1, ks) * fade
        d.text((W // 2, 720), "1 STUNDE SPÄTER", font=font(MONO, 46), fill=mix(BG, CY, a), anchor="mm")
    kw = pop(t, E["Sneaker-Werbung."])
    if kw > 0:  # generische Werbekarte
        a = min(1, kw) * fade; y = 790 + int(40 * (1 - min(1, kw)))
        d.rounded_rectangle([200, y, 880, y + 230], radius=30, fill=mix(BG, WH, a))
        d.text((240, y + 40), "ANZEIGE", font=font(MONO, 30), fill=mix(BG, GR, a), anchor="lt")
        d.text((240, y + 95), "Sneaker", font=font(BLACK, 80), fill=mix(BG, BG, a), anchor="lt")
        d.rounded_rectangle([640, y + 90, 840, y + 180], radius=20, fill=mix(BG, RD, a))
        d.text((740, y + 135), "-30 %", font=font(BLACK, 54), fill=mix(BG, WH, a), anchor="mm")
    kh = pop(t, E["heimlich"] - 0.1)
    if kh > 0:
        a = min(1, kh)
        d.rounded_rectangle([110, 1080, 970, 1270], radius=40, fill=mix(BG, PANEL, a), outline=mix(BG, RD, a), width=5)
        mic(d, 210, 1170, 1.15, mix(BG, RD, a))
        d.text((300, 1140), "HÖRT DEIN HANDY", font=font(BLACK, 58), fill=mix(BG, WH, a), anchor="lm")
        d.text((300, 1210), "HEIMLICH MIT?", font=font(BLACK, 58), fill=mix(BG, RD, a), anchor="lm")
    return img


def s2(t0):  # Studie
    t = t0 + T1
    img = stock_bg(CLIP_TYPE, t0, dim=0.74); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    d.text((110, 430), "DIE STUDIE", font=font(MONO, 44), fill=mix(BG, CY, a), anchor="ls")
    k = ease((t - E["siebzehntausend"] + 0.1) / 0.9)
    if k > 0:
        n = int(17260 * k)
        big(d, 560, f"{n:,}".replace(",", "."), 190, WH, min(1, k * 3))
        d.text((W // 2, 690), "APPS GETESTET", font=font(BLACK, 62), fill=mix(BG, WH, min(1, k * 3)), anchor="mm")
        d.text((W // 2, 760), "Northeastern University, 2018", font=font(SEMI, 38), fill=mix(BG, GR, min(1, k * 3)), anchor="mm")
    kk = pop(t, E["keine"] - 0.05)
    if kk > 0:
        a = min(1, kk)
        d.rounded_rectangle([110, 830, 970, 1030], radius=36, fill=mix(BG, PANEL, a), outline=mix(BG, GN, a), width=5)
        d.text((200, 930), "0", font=font(BLACK, 150), fill=mix(BG, GN, a), anchor="mm")
        d.text((300, 895), "heimlich verschickte", font=font(SEMI, 50), fill=mix(BG, WH, a), anchor="lm")
        d.text((300, 965), "Gespräche", font=font(BLACK, 60), fill=mix(BG, WH, a), anchor="lm")
    km = pop(t, E["Mithören"] - 0.05, d=0.22)
    if km > 0:  # Stempel MYTHOS
        a = min(1, km); s = 1 + 0.4 * (1 - min(1, km))
        cx, cy = W // 2, 1170
        bw, bh = int(330 * s), int(70 * s)
        d.rounded_rectangle([cx - bw, cy - bh, cx + bw, cy + bh], radius=20, outline=mix(BG, RD, a), width=10)
        d.text((cx, cy), "MYTHOS", font=font(BLACK, int(100 * s)), fill=mix(BG, RD, a), anchor="mm")
    return img


def chip(d, y, txt, col, k, icon):
    if k <= 0:
        return
    a = min(1, k); dx = int(40 * (1 - a))
    d.rounded_rectangle([110 + dx, y, 970, y + 120], radius=60, fill=mix(BG, PANEL, a), outline=mix(BG, col, a * 0.9), width=4)
    d.ellipse([140 + dx, y + 20, 220 + dx, y + 100], fill=mix(BG, col, a))
    d.text((180 + dx, y + 60), icon, font=font(BLACK, 46), fill=BG, anchor="mm")
    d.text((250 + dx, y + 62), txt, font=font(BLACK, 58), fill=mix(BG, WH, a), anchor="lm")


def phone(d, cx, cy, s, col, a, label):
    w, h = int(95 * s), int(170 * s)
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], radius=int(24 * s), outline=mix(BG, col, a), width=7)
    d.text((cx, cy), label, font=font(BLACK, int(34 * s)), fill=mix(BG, WH, a), anchor="mm")


def s3(t0):  # Was Werbefirmen wirklich wissen
    t = t0 + T2
    img = stock_bg(CLIP_ROUTER, t0, dim=0.75); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    t_k = E["Kumpel"] - 0.15
    if t < t_k:
        d.text((110, 430), "WAS WERBEFIRMEN WISSEN", font=font(MONO, 44), fill=mix(BG, CY, a), anchor="ls")
        chip(d, 520, "Dein Standort", CY, pop(t, E["Standort,"] - 0.05), "1")
        chip(d, 680, "Deine Suchen", CY, pop(t, E["Suchen"] - 0.05), "2")
        chip(d, 840, "Suchen im selben WLAN", ORANGE, pop(t, E["WLAN"] - 0.05), "3")
    else:
        k = pop(t, t_k)
        d.text((110, 430), "GLEICHES WLAN", font=font(MONO, 44), fill=mix(BG, CY, min(1, k)), anchor="ls")
        phone(d, 280, 760, 1.25, GR, min(1, k), "KUMPEL")
        d.text((280, 1030), "sucht „Sneaker“", font=font(SEMI, 44), fill=mix(BG, WH, min(1, k)), anchor="mm")
        kd = pop(t, E["dir."] - 0.6)
        if kd > 0:
            aa = min(1, kd)
            x1 = 420 + int(180 * min(1, kd))
            d.line([(410, 760), (x1, 760)], fill=mix(BG, ORANGE, aa), width=14)
            d.polygon([(x1 + 40, 760), (x1, 730), (x1, 790)], fill=mix(BG, ORANGE, aa))
            phone(d, 760, 760, 1.25, CY, aa, "DU")
            d.rounded_rectangle([590, 1000, 930, 1070], radius=18, fill=mix(BG, WH, aa))
            d.text((760, 1035), "ANZEIGE: Sneaker", font=font(BLACK, 34), fill=BG, anchor="mm")
        # Funkwellen über beiden
        for i in range(3):
            r = 40 + i * 35
            d.arc([520 - r, 540 - r, 520 + r, 540 + r], 225, 315, fill=mix(BG, CY, min(1, k) * 0.8), width=8)
    return img


def s4(t0):  # Mikro-Symbol + Frage
    t = t0 + T3
    img = stock_bg(CLIP_HOLD, t0, dim=0.72); d = ImageDraw.Draw(img); header(d, LABEL)
    tq = E["passiert?"] - 0.25
    if t < tq:
        a = ease(t0 / 0.3)
        d.text((110, 430), "SO ERKENNST DU ES", font=font(MONO, 44), fill=mix(BG, CY, a), anchor="ls")
        # stilisierter Bildschirm-Ausschnitt mit Statusleiste
        k = pop(t, E["Mikro"] - 0.05)
        if k > 0:
            aa = min(1, k)
            d.rounded_rectangle([140, 500, 940, 820], radius=60, fill=mix(BG, PANEL, aa), outline=mix(BG, GR, aa), width=6)
            d.text((220, 580), "18:00", font=font(BLACK, 54), fill=mix(BG, WH, aa), anchor="lm")
            ks = pop(t, E["Symbol."] - 0.2)
            if ks > 0:
                pulse = 1 + 0.15 * math.sin((t - E["Symbol."]) * 8)
                r = int(22 * pulse * min(1, ks))
                d.ellipse([560 - r, 580 - r, 560 + r, 580 + r], fill=ORANGE)
                d.rounded_rectangle([760, 550, 880, 610], radius=30, fill=GN)
                mic(d, 820, 590, 0.42, BG)
                d.line([(560, 620), (480, 700)], fill=ORANGE, width=6)
                d.line([(820, 620), (820, 700)], fill=GN, width=6)
                d.text((440, 740), "iPhone", font=font(BLACK, 46), fill=ORANGE, anchor="mm")
                d.text((820, 740), "Android", font=font(BLACK, 46), fill=GN, anchor="mm")
            big(d, 960, "Symbol = Mikro an", 76, WH, pop(t, E["Symbol."] - 0.1))
    else:
        k = pop(t, tq)
        big(d, 520, "SCHON MAL", 110, WH, k)
        big(d, 650, "PASSIERT?", 110, WH, k)
        for (w, txt, x, col) in [("Ja", "JA", 330, GN), ("Nein?", "NEIN", 750, RD)]:
            kk = pop(t, E[w] - 0.05)
            if kk > 0:
                a = min(1, kk)
                d.rounded_rectangle([x - 170, 800, x + 170, 940], radius=70, fill=mix(BG, PANEL, a), outline=mix(BG, col, a), width=6)
                d.text((x, 872), txt, font=font(BLACK, 80), fill=mix(BG, col, a), anchor="mm")
        kc = pop(t, E["Kommentare."])
        if kc > 0:
            a = min(1, kc); bounce = 12 * math.sin((t - E["Kommentare."]) * 9)
            x0, y0 = 760 + bounce, 1080
            d.line([(x0 - 120, y0 + 60), (x0 + 60, y0 - 40)], fill=mix(BG, SUB_HL, a), width=14)
            d.polygon([(x0 + 95, y0 - 60), (x0 + 30, y0 - 60), (x0 + 75, y0 - 5)], fill=mix(BG, SUB_HL, a))
        kf = pop(t, END - 0.95)
        if kf > 0:
            d.text((W // 2, 1230), "Folgen = morgen schlauer", font=font(BLACK, 54), fill=mix(BG, CY, min(1, kf)), anchor="mm")
    return img


SCENES = [("s1", s1, T1), ("s2", s2, T2 - T1), ("s3", s3, T3 - T2), ("s4", s4, END - T3)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for st, txt in VOICE:
            print(f"{st:5.2f}–{st + say(txt)[1]:5.2f}  {txt}")
        print(stills(SCENES, "/home/claude/bitweise-out/tag07", voice=VOICE))
    else:
        print(build(SCENES, "tag07_mithoeren", seed=7, voice=VOICE))
        write_credits("Tag 07 – Mythos-Check: Hört dein Handy mit?")
