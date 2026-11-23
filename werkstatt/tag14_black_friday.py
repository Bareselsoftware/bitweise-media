"""Tag 14 – Rate mal: Black Friday „-50 %“ – echter Rabatt oder Trick? (Format v3 + Experiment Mitmach-Einstieg:
Rate-Frage mit 2 Optionen in Sek. 0–5, 3-s-Countdown, dann Auflösung; Tempo 0,82, ohne Ton-Akzent).
Fakten (Verbraucherzentrale SH 19.11.2026, Netzwelt; Wochenrecap 23.11.): Rabatte werden oft gegen die UVP gerechnet,
die häufig deutlich über dem tatsächlichen Marktpreis liegt → Preisverlauf/Preisvergleich prüfen; Countdown-Druck
ignorieren; unbekannte Shops mit dem Fakeshop-Finder der Verbraucherzentrale prüfen; nicht per Vorkasse zahlen.
Die Preise im Bild (199/99/119 €) sind ein gekennzeichnetes Rechenbeispiel."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *
import math

say.__defaults__ = (0.82,)
LABEL = "RATE MAL"
COUNT = 3.0  # Raten-Pause mit Countdown

VOICE = timeline([
    "Minus fünfzig Prozent. Echter Rabatt oder Trick?",
    "Rate mit!",
    ("Oft ist der Rabatt kleiner, als er aussieht.", COUNT),
    "Viele Shops rechnen gegen die unverbindliche Preisempfehlung.",
    "Und die lag oft schon vorher weit über dem echten Preis.",
    "Also: Preisverlauf checken.",
    "Vergleichsportale zeigen dir den Preis von vor ein paar Wochen.",
    "Countdown läuft? Ignorieren. Der soll dich nur hetzen.",
    "Unbekannter Shop? Erst beim Fakeshop-Finder prüfen.",
    "Und nie per Vorkasse zahlen.",
    ("Speicher dir das für Black Friday.", 0.35),
    ("Und du: Schon mal reingefallen? Ja oder nein. Ab in die Kommentare.", 0.3),
])
WORDS = word_timings(VOICE)
END = VOICE[-1][0] + say(VOICE[-1][1])[1] + 1.0
CD0 = VOICE[1][0] + say(VOICE[1][1])[1] + 0.05          # Countdown-Start
PAUSE = (CD0 - 0.06, VOICE[2][0] + 0.01)

T1 = VOICE[2][0] - 0.12
T2 = VOICE[5][0] - 0.15
T3 = VOICE[10][0] - 0.15


def _pick(q, i, kind="video"):
    return {h["id"]: h for h in stock_search(q, kind, n=12, lang="en")}[i]


CLIP_SALE = Clip(stock_get(_pick("sale shop", 993)), start=0.5)          # „SALE 50%“-Schild, Straße (2015)
CLIP_CART = Clip(stock_get(_pick("sale shop", 47601)), start=1.0)        # Einkaufswagen im Markt (2020)
CLIP_TYPE = Clip(stock_get(_pick("credit card laptop", 52823)), start=0.5)  # Hände am Laptop (2020)
CLIP_MALL = Clip(stock_get(_pick("shopping bags", 12876)), start=1.0)    # Einkaufszentrum (2017)

E = {k: at(WORDS, k) for k in ["Echter", "Trick?", "Rate", "Oft", "unverbindliche", "vorher", "echten",
                               "Preisverlauf", "Vergleichsportale", "Wochen", "Countdown", "Ignorieren.", "hetzen.",
                               "Fakeshop-Finder", "Vorkasse", "Speicher", "reingefallen?", "Ja", "nein.",
                               "Kommentare."]}


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


def tag(d, cx, cy, s, txt, col, a=1.0):
    """Preisschild mit Loch."""
    w, h = int(330 * s), int(170 * s)
    d.rounded_rectangle([cx - w, cy - h, cx + w, cy + h], radius=int(40 * s), fill=mix(BG, col, a))
    d.ellipse([cx - w + int(22 * s), cy - int(16 * s), cx - w + int(54 * s), cy + int(16 * s)], fill=mix(BG, BG, a))
    d.text((cx + int(40 * s), cy + int(8 * s)), txt, font=font(BLACK, int(180 * s)), fill=mix(BG, WH, a), anchor="mm")


OPTS = [("Echter", "A", "ECHTER RABATT"), ("Trick?", "B", "TRICK")]


def option(d, i, k, state=0):
    """state 0 = neutral, 1 = eher nicht (grau), 2 = eher ja (grün)."""
    if k <= 0:
        return
    a = min(1, k); y = 790 + i * 155; dx = int(40 * (1 - a))
    col = {0: CY, 1: GR, 2: GN}[state]
    d.rounded_rectangle([150 + dx, y, 930, y + 130], radius=65, fill=mix(BG, PANEL, a),
                        outline=mix(BG, col, a), width=6 if state == 2 else 4)
    d.ellipse([175 + dx, y + 20, 265 + dx, y + 110], fill=mix(BG, col, a))
    d.text((220 + dx, y + 65), OPTS[i][1], font=font(BLACK, 52), fill=BG, anchor="mm")
    d.text((300 + dx, y + 67), OPTS[i][2], font=font(BLACK, 64),
           fill=mix(BG, GR if state == 1 else WH, a), anchor="lm")


def s1(t):  # Hook + Raten + Countdown („-50 %“ steht ab Frame 0)
    img = stock_bg(CLIP_SALE, t, dim=0.62)
    img = punch(img, t)
    d = ImageDraw.Draw(img); header(d, LABEL)
    d.text((W // 2, 310), "BLACK FRIDAY", font=font(MONO, 46), fill=CY, anchor="mm")
    tag(d, W // 2, 530, 0.9, "-50 %", RD)
    d.text((W // 2, 720), "ECHTER RABATT ODER TRICK?", font=font(BLACK, 58), fill=WH, anchor="mm")
    for i, (w, _, _) in enumerate(OPTS):
        option(d, i, pop(t, E[w] - 0.08))
    if t >= CD0 - 0.05:  # Countdown 3-2-1
        n = 3 - int((t - CD0) / (COUNT / 3))
        if n >= 1:
            ph = ((t - CD0) % (COUNT / 3)) / (COUNT / 3)
            r = 85
            d.ellipse([W // 2 - r, 1195 - r, W // 2 + r, 1195 + r], outline=mix(BG, SUB_HL, 0.35), width=10)
            d.arc([W // 2 - r, 1195 - r, W // 2 + r, 1195 + r], -90, -90 + 360 * (1 - ph), fill=SUB_HL, width=10)
            sz = int(120 * (1 + 0.25 * (1 - ease(ph / 0.25))))
            d.text((W // 2, 1195), str(n), font=font(BLACK, sz), fill=SUB_HL, anchor="mm")
    elif t >= E["Rate"] - 0.05:
        k = pop(t, E["Rate"] - 0.05)
        d.text((W // 2, 1195), "RATE MIT!", font=font(BLACK, 80), fill=mix(BG, SUB_HL, min(1, k)), anchor="mm")
    return img


def s2(t0):  # Auflösung + Rechenbeispiel UVP
    t = t0 + T1
    img = stock_bg(CLIP_CART, t0, dim=0.74); d = ImageDraw.Draw(img); header(d, LABEL)
    k = pop(t, E["Oft"] - 0.05)
    if k > 0:  # Stempel
        a = min(1, k); s = 1 + 0.35 * (1 - min(1, k))
        d.rounded_rectangle([W // 2 - int(430 * s), 400 - int(70 * s), W // 2 + int(430 * s), 400 + int(70 * s)],
                            radius=24, fill=mix(BG, RD, a))
        d.text((W // 2, 400), "OFT KLEINER ALS GEDACHT", font=font(BLACK, int(62 * s)), fill=mix(BG, WH, a), anchor="mm")
    ku = pop(t, E["unverbindliche"] - 0.1)
    if ku > 0:
        a = min(1, ku)
        d.text((W // 2, 535), "BEISPIEL", font=font(MONO, 38), fill=mix(BG, GR, a), anchor="mm")
        d.rounded_rectangle([110, 580, 970, 1000], radius=36, fill=mix(BG, PANEL, a))
        f = font(BLACK, 66)
        d.text((160, 660), "UVP", font=f, fill=mix(BG, GR, a), anchor="lm")
        d.text((920, 660), "199 €", font=f, fill=mix(BG, GR, a), anchor="rm")
        x0 = 920 - d.textlength("199 €", font=f)
        d.line([(x0 - 8, 662), (928, 662)], fill=mix(BG, RD, a), width=7)
        d.text((160, 770), "Black Friday", font=f, fill=mix(BG, WH, a), anchor="lm")
        d.text((920, 770), "99 €", font=f, fill=mix(BG, WH, a), anchor="rm")
        d.text((W // 2, 900), "„-50 %“", font=font(BLACK, 90), fill=mix(BG, WH, a), anchor="mm")
    kv = pop(t, E["vorher"] - 0.1)
    if kv > 0:
        a = min(1, kv)
        d.rounded_rectangle([110, 1040, 970, 1270], radius=36, fill=mix(BG, PANEL, a), outline=mix(BG, RD, a), width=5)
        d.text((160, 1100), "Preis letzten Monat", font=font(BLACK, 54), fill=mix(BG, WH, a), anchor="lm")
        d.text((920, 1100), "119 €", font=font(BLACK, 54), fill=mix(BG, WH, a), anchor="rm")
        ke = pop(t, E["echten"])
        if ke > 0:
            d.text((W // 2, 1205), "echt nur -17 %", font=font(BLACK, 76), fill=mix(BG, RD, min(1, ke)), anchor="mm")
    return img


def s3(t0):  # So checkst du's
    t = t0 + T2
    img = stock_bg(CLIP_TYPE, t0, dim=0.74); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    big(d, 400, "SO CHECKST DU'S", 92, CY, a)
    items = [("Preisverlauf", "Preisverlauf checken"), ("Countdown", "Countdown ignorieren"),
             ("Fakeshop-Finder", "Fakeshop-Finder"), ("Vorkasse", "Keine Vorkasse")]
    for i, (w, txt) in enumerate(items):
        k = pop(t, E[w] - 0.05)
        if k <= 0:
            continue
        kk = min(1, k); y = 520 + i * 185
        d.rounded_rectangle([90, y, 990, y + 155], radius=28, fill=mix(BG, PANEL, kk), outline=mix(BG, GN, kk * 0.8), width=4)
        check(d, 170, y + 78, 1.2, GN, kk)
        d.text((250 + int(30 * (1 - kk)), y + 100), txt, font=font(BLACK, 60), fill=mix(BG, WH, kk), anchor="ls")
        if w == "Fakeshop-Finder":
            d.text((250, y + 140), "der Verbraucherzentrale", font=font(SEMI, 34), fill=mix(BG, GR, kk), anchor="ls")
    return img


def s4(t0):  # Speichern + Interaktionsfrage
    t = t0 + T3
    img = stock_bg(CLIP_MALL, t0, dim=0.7); d = ImageDraw.Draw(img); header(d, LABEL)
    ks = pop(t, E["Speicher"] - 0.05)
    if ks > 0:  # Lesezeichen-Symbol + „Speicher dir das“
        a = min(1, ks); cx, cy = 230, 420
        d.polygon([(cx - 40, cy - 60), (cx + 40, cy - 60), (cx + 40, cy + 60), (cx, cy + 30), (cx - 40, cy + 60)],
                  fill=mix(BG, SUB_HL, a))
        d.text((300, 420), "SPEICHER DIR DAS", font=font(BLACK, 66), fill=mix(BG, SUB_HL, a), anchor="lm")
    kq = pop(t, E["reingefallen?"] - 0.5)
    big(d, 600, "Schon mal", 96, WH, kq)
    big(d, 710, "reingefallen?", 96, WH, kq)
    for w, lab, x, col in (("Ja", "JA", 300, GN), ("nein.", "NEIN", 780, RD)):
        kk = pop(t, E[w] - 0.05)
        if kk > 0:
            a = min(1, kk)
            d.rounded_rectangle([x - 200, 830, x + 200, 980], radius=75, fill=mix(BG, col, a))
            d.text((x, 907), lab, font=font(BLACK, 72), fill=BG, anchor="mm")
    kc = pop(t, E["Kommentare."])
    if kc > 0:
        a = min(1, kc)
        d.rounded_rectangle([170, 1040, 910, 1160], radius=60, fill=mix(BG, PANEL, a), outline=mix(BG, SUB_HL, a), width=4)
        d.text((W // 2, 1102), "Ab in die Kommentare", font=font(BLACK, 56), fill=mix(BG, SUB_HL, a), anchor="mm")
    kf = pop(t, END - 1.0)
    if kf > 0:
        d.text((W // 2, 1250), "Folgen = mehr solche Checks", font=font(BLACK, 54), fill=mix(BG, CY, min(1, kf)), anchor="mm")
    return img


SCENES = [("s1", s1, T1), ("s2", s2, T2 - T1), ("s3", s3, T3 - T2), ("s4", s4, END - T3)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for st, txt in VOICE:
            print(f"{st:5.2f}–{st + say(txt)[1]:5.2f}  {txt}")
        print("END", END, "CD0", CD0)
        print(stills(SCENES, "/home/claude/bitweise-out/tag14", voice=VOICE))
    else:
        print(build(SCENES, "tag14_black_friday", seed=14, voice=VOICE, pausen_ok=[PAUSE],
                    typing=[(CD0, 3, COUNT / 3)]))
        write_credits("Tag 14 – Rate mal: Black Friday")
