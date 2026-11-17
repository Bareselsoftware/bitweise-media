"""Tag 08 – Rate mal: Wie schnell ist „Passwort123“ geknackt? (Format v3, Vergleichsvideo ohne Einstiegs-Experiment)
Fakten: Wird eine Passwort-Datenbank gestohlen, prüfen Angreifer offline zuerst Wörterbücher geleakter Passwörter
plus Regeln (Wort + Ziffernfolge, Großschreibung) – „Passwort123“ fällt so praktisch sofort. Bei schnellen bzw.
schlecht gewählten Hash-Verfahren (z. B. MD5/NTLM) schafft eine aktuelle Grafikkarte Milliarden Versuche pro Sekunde
(hashcat-Benchmarks). Empfehlung: lange Passphrasen (mehrere zufällige Wörter, BSI: „je länger, desto besser“;
NIST SP 800-63B: Länge vor Komplexitätsregeln) und für jedes Konto ein eigenes Passwort."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *
import math

say.__defaults__ = (0.9,)  # Tag 8 bleibt Vergleich (Experiment „Einstieg“ erst ab Tag 9)
LABEL = "RATE MAL"
COUNT = 3.0  # Raten-Pause mit Countdown

VOICE = timeline([
    "Passwort eins zwei drei. Wie lange hält das?",
    "Ein Jahr, ein Tag oder eine Sekunde? Rate mit!",
    ("Weniger als eine Sekunde.", COUNT),
    "Wird eine Datenbank geklaut, raten Hacker nicht Buchstabe für Buchstabe.",
    "Sie probieren zuerst Millionen bekannter Passwörter und typische Muster: Wort plus eins zwei drei.",
    "Eine gute Grafikkarte schafft dabei oft Milliarden Versuche pro Sekunde.",
    "Besser: vier zufällige Wörter. Lang schlägt kompliziert.",
    "Und für jedes Konto ein eigenes.",
    ("Wie lang ist deins? Nur die Zahl. Nicht das Passwort!", 0.35),
    ("Ab in die Kommentare.", 0.2),
])
WORDS = word_timings(VOICE)
END = VOICE[-1][0] + say(VOICE[-1][1])[1] + 1.0
CD0 = VOICE[1][0] + say(VOICE[1][1])[1] + 0.05          # Countdown-Start
PAUSE = (CD0 - 0.06, VOICE[2][0] + 0.01)

T1 = VOICE[2][0] - 0.12
T2 = VOICE[4][0] - 0.15
T3 = VOICE[6][0] - 0.15
T4 = VOICE[8][0] - 0.2


def _pick(q, i, kind="video"):
    return {h["id"]: h for h in stock_search(q, kind, n=20, lang="en")}[i]


CLIP_BLUE = Clip(stock_get(_pick("graphics card computer", 31806)), start=0.5)  # beleuchtete Tastatur (2020)
CLIP_GAME = Clip(stock_get(_pick("typing keyboard", 24527)), start=1.0)          # Gaming-Tastatur (2019)
CLIP_KEYS = Clip(stock_get(_pick("typing keyboard", 10822)), start=0.5)          # Tastatur Nahaufnahme (2017)
CLIP_PHONE = Clip(stock_get(_pick("smartphone lock screen", 47743)), start=0.5, zoom=1.12)  # Handy in der Hand (2020)

E = {k: at(WORDS, k) for k in ["Wie", "Jahr,", "Tag", "Sekunde?", "Rate", "Weniger", "Datenbank", "Buchstabe",
                               "Millionen", "Muster:", "Wort", "Grafikkarte", "Milliarden", "Besser:", "vier",
                               "Lang", "Konto", "deins?", "Zahl.", "Kommentare."]}
E["Passwort!"] = at(WORDS, "Passwort!", nth=1)


def pop(t, t0, d=0.18):
    x = max(0.0, min(1.0, (t - t0) / d))
    return x * (1 + 0.25 * math.sin(math.pi * x)) if x < 1 else 1.0


def big(d, y, s, size, col, k, dy=30):
    if k <= 0:
        return
    f = font(BLACK, max(8, int(size * (0.7 + 0.3 * min(k, 1.2)))))
    d.text((W // 2, y + int(dy * (1 - min(k, 1)))), s, font=f, fill=mix(BG, col, min(k, 1)), anchor="mm")


def field(d, y, txt, col, a, cur=True, t=0.0):
    """Passwortfeld mit Schloss-Symbol."""
    d.rounded_rectangle([110, y, 970, y + 170], radius=36, fill=mix(BG, PANEL, a), outline=mix(BG, col, a), width=6)
    # Schloss
    cx, cy = 200, y + 92
    d.arc([cx - 26, cy - 62, cx + 26, cy - 10], 180, 360, fill=mix(BG, col, a), width=9)
    d.rounded_rectangle([cx - 38, cy - 34, cx + 38, cy + 34], radius=10, fill=mix(BG, col, a))
    f = font(BLACK, 92)
    d.text((280, y + 88), txt, font=f, fill=mix(BG, WH, a), anchor="lm")
    if cur and (int(t * 2) % 2 == 0):
        x = 280 + d.textlength(txt, font=f) + 12
        d.rectangle([x, y + 45, x + 8, y + 130], fill=mix(BG, CY, a))


OPTS = [("Jahr,", "A", "1 JAHR"), ("Tag", "B", "1 TAG"), ("Sekunde?", "C", "1 SEKUNDE")]


def option(d, i, k, state=0):
    """state 0 = neutral, 1 = falsch (grau), 2 = richtig (grün)."""
    if k <= 0:
        return
    a = min(1, k); y = 650 + i * 150; dx = int(40 * (1 - a))
    col = {0: CY, 1: GR, 2: GN}[state]
    d.rounded_rectangle([150 + dx, y, 930, y + 130], radius=65, fill=mix(BG, PANEL, a),
                        outline=mix(BG, col, a), width=6 if state == 2 else 4)
    d.ellipse([175 + dx, y + 20, 265 + dx, y + 110], fill=mix(BG, col, a))
    d.text((220 + dx, y + 65), OPTS[i][1], font=font(BLACK, 52), fill=BG, anchor="mm")
    d.text((300 + dx, y + 67), OPTS[i][2], font=font(BLACK, 64),
           fill=mix(BG, GR if state == 1 else WH, a), anchor="lm")
    if state == 1:
        d.line([(300 + dx, y + 67), (300 + dx + d.textlength(OPTS[i][2], font=font(BLACK, 64)), y + 67)],
               fill=mix(BG, RD, a), width=7)


def s1(t):  # Hook + Raten + Countdown (Passwortfeld steht ab Frame 0)
    img = stock_bg(CLIP_BLUE, t, dim=0.62); d = ImageDraw.Draw(img); header(d, LABEL)
    field(d, 330, "Passwort123", CY, 1.0, t=t)
    kq = 1.0  # Hook-Frage steht ab Frame 0
    if kq > 0:
        d.text((W // 2, 580), "WIE LANGE HÄLT DAS?", font=font(BLACK, 66), fill=mix(BG, WH, min(1, kq)), anchor="mm")
    for i, (w, _, _) in enumerate(OPTS):
        option(d, i, pop(t, E[w] - 0.08))
    if t >= CD0 - 0.05:  # Countdown 3-2-1
        n = 3 - int((t - CD0) / (COUNT / 3))
        if n >= 1:
            ph = ((t - CD0) % (COUNT / 3)) / (COUNT / 3)
            r = 85
            d.ellipse([W // 2 - r, 1205 - r, W // 2 + r, 1205 + r], outline=mix(BG, SUB_HL, 0.35), width=10)
            d.arc([W // 2 - r, 1205 - r, W // 2 + r, 1205 + r], -90, -90 + 360 * (1 - ph), fill=SUB_HL, width=10)
            sz = int(120 * (1 + 0.25 * (1 - ease(ph / 0.25))))
            d.text((W // 2, 1205), str(n), font=font(BLACK, sz), fill=SUB_HL, anchor="mm")
    elif t >= E["Rate"] - 0.05:
        k = pop(t, E["Rate"] - 0.05)
        d.text((W // 2, 1200), "RATE MIT!", font=font(BLACK, 80), fill=mix(BG, SUB_HL, min(1, k)), anchor="mm")
    return img


def s2(t0):  # Auflösung + Grund
    t = t0 + T1
    img = stock_bg(CLIP_GAME, t0, dim=0.72); d = ImageDraw.Draw(img); header(d, LABEL)
    tb = E["Datenbank"] - 0.2
    if t < tb:
        field(d, 330, "Passwort123", RD, 1.0, cur=False)
        for i in range(3):
            option(d, i, 1.0, 2 if i == 2 else 1)
        k = pop(t, E["Weniger"])
        if k > 0:  # Stempel
            a = min(1, k); s = 1 + 0.35 * (1 - min(1, k))
            d.rounded_rectangle([W // 2 - int(400 * s), 572 - int(70 * s), W // 2 + int(400 * s), 572 + int(70 * s)],
                                radius=24, fill=mix(BG, RD, a))
            d.text((W // 2, 572), "< 1 SEKUNDE", font=font(BLACK, int(96 * s)), fill=mix(BG, WH, a), anchor="mm")
    else:
        k = pop(t, tb)
        a = min(1, k)
        d.text((110, 430), "WENN DATEN GEKLAUT WERDEN", font=font(MONO, 42), fill=mix(BG, CY, a), anchor="ls")
        # Datenbank-Symbol
        cx, cy = W // 2, 640
        for j in range(3):
            y = cy - 90 + j * 70
            d.rounded_rectangle([cx - 170, y, cx + 170, y + 60], radius=30, fill=mix(BG, PANEL, a),
                                outline=mix(BG, CY, a), width=5)
            for q in range(5):
                d.ellipse([cx - 120 + q * 50, y + 22, cx - 104 + q * 50, y + 38], fill=mix(BG, GR, a))
        kb = pop(t, E["Buchstabe"] - 0.1)
        if kb > 0:
            aa = min(1, kb)
            y = 900
            d.text((W // 2, y), "a  b  c  d  e  f …", font=font(BLACK, 90), fill=mix(BG, GR, aa), anchor="mm")
            d.line([(170, y + 70), (910, y - 60)], fill=mix(BG, RD, aa), width=16)
            d.line([(170, y - 60), (910, y + 70)], fill=mix(BG, RD, aa), width=16)
            d.text((W // 2, 1090), "Raten? Viel zu langsam.", font=font(SEMI, 54), fill=mix(BG, WH, aa), anchor="mm")
    return img


LISTE = ["123456", "passwort", "hallo123", "qwertz", "schatz", "sommer123", "123456789", "fussball",
         "111111", "lol123", "hallo", "iloveyou", "dragon", "master"]


def s3(t0):  # Listen + Muster + Tempo
    t = t0 + T2
    img = stock_bg(CLIP_KEYS, t0, dim=0.76); d = ImageDraw.Draw(img); header(d, LABEL)
    tg = E["Grafikkarte"] - 0.2
    if t < tg:
        a = ease(t0 / 0.3)
        d.text((110, 430), "SO KNACKEN HACKER", font=font(MONO, 44), fill=mix(BG, CY, a), anchor="ls")
        km = pop(t, E["Millionen"] - 0.05)
        if km > 0:
            aa = min(1, km)
            big(d, 540, "MILLIONEN", 120, WH, km)
            d.text((W // 2, 630), "bekannter Passwörter", font=font(SEMI, 50), fill=mix(BG, GR, aa), anchor="mm")
            # durchlaufende Liste
            off = (t - E["Millionen"]) * 9
            for j in range(4):
                idx = int(off + j) % len(LISTE)
                yy = 720 + j * 62 - int((off % 1) * 62)
                fade = aa * max(0, min(1, (yy - 690) / 60, (950 - yy) / 60))
                d.text((W // 2, yy), LISTE[idx], font=font(MONO, 48), fill=mix(BG, GR, fade), anchor="mm")
        kp = pop(t, E["Muster:"] - 0.05)
        if kp > 0:
            aa = min(1, kp)
            d.rounded_rectangle([110, 990, 970, 1240], radius=36, fill=mix(BG, PANEL, aa), outline=mix(BG, RD, aa), width=5)
            d.text((W // 2, 1050), "MUSTER: WORT + 123", font=font(BLACK, 62), fill=mix(BG, RD, aa), anchor="mm")
            kw = pop(t, E["Wort"] - 0.05)
            ex = ["Sommer123", "Hallo123", "Passwort123"]
            for j, e in enumerate(ex):
                ke = pop(t, E["Wort"] + j * 0.3)
                if ke > 0:
                    col = SUB_HL if j == 2 else WH
                    d.text((250 + j * 270, 1170), e, font=font(SEMI, 44), fill=mix(BG, col, min(1, ke) * aa), anchor="mm")
    else:
        k = pop(t, tg)
        a = min(1, k)
        d.text((110, 430), "1 GRAFIKKARTE", font=font(MONO, 44), fill=mix(BG, CY, a), anchor="ls")
        kn = ease((t - E["Milliarden"] + 0.1) / 0.8)
        n = int(1_000_000_000 * max(0, kn)) + int((t * 7919) % 1000) if kn > 0 else int(2_000_000 * min(1, (t - tg) / 0.5))
        s = f"{n:,}".replace(",", ".")
        f = font(BLACK, 110 if len(s) > 11 else 130)
        d.text((W // 2, 650), s, font=f, fill=mix(BG, WH, a), anchor="mm")
        d.text((W // 2, 770), "VERSUCHE / SEKUNDE", font=font(BLACK, 62), fill=mix(BG, SUB_HL if kn >= 1 else WH, a), anchor="mm")
        if kn > 0:
            d.text((W // 2, 860), "bei schlecht geschützten Daten", font=font(SEMI, 42), fill=mix(BG, GR, min(1, kn * 2)), anchor="mm")
        # Fortschrittsbalken „Passwort123 gefunden“
        kb = ease((t - tg) / 1.4)
        d.rounded_rectangle([150, 980, 930, 1040], radius=30, fill=mix(BG, PANEL, a))
        if kb > 0:
            d.rounded_rectangle([150, 980, 150 + max(60, int(780 * kb)), 1040], radius=30, fill=mix(BG, RD, a))
        if kb >= 1:
            d.text((W // 2, 1130), "Passwort123: GEFUNDEN", font=font(BLACK, 60), fill=RD, anchor="mm")
    return img


def s4(t0):  # Besser
    t = t0 + T3
    img = background(t); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    big(d, 450, "BESSER", 110, GN, pop(t, E["Besser:"] - 0.1))
    kv = pop(t, E["vier"] - 0.05)
    words = ["Tasse", "Wolke", "Ritter", "Mond"]
    for j, w in enumerate(words):
        kk = pop(t, E["vier"] + j * 0.18)
        if kk > 0:
            aa = min(1, kk); x0 = 110 + j * 220; y = 570
            d.rounded_rectangle([x0, y, x0 + 200, y + 110], radius=24, fill=mix(BG, PANEL, aa), outline=mix(BG, GN, aa), width=4)
            d.text((x0 + 100, y + 57), w, font=font(BLACK, 44), fill=mix(BG, WH, aa), anchor="mm")
    if kv > 0:
        d.text((W // 2, 740), "4 zufällige Wörter", font=font(SEMI, 46), fill=mix(BG, GR, min(1, kv)), anchor="mm")
    kl = pop(t, E["Lang"] - 0.05)
    if kl > 0:
        aa = min(1, kl)
        d.rounded_rectangle([140, 810, 940, 940], radius=65, fill=mix(BG, GN, aa))
        d.text((W // 2, 877), "LANG > KOMPLIZIERT", font=font(BLACK, 66), fill=BG, anchor="mm")
    kk = pop(t, E["Konto"] - 0.15)
    if kk > 0:
        aa = min(1, kk)
        for j, (lab, col) in enumerate([("Mail", CY), ("Bank", GN), ("Shop", SUB_HL)]):
            x = 230 + j * 310
            d.rounded_rectangle([x - 130, 1000, x + 130, 1130], radius=28, fill=mix(BG, PANEL, aa), outline=mix(BG, col, aa), width=4)
            d.text((x, 1048), lab, font=font(BLACK, 50), fill=mix(BG, WH, aa), anchor="mm")
            d.text((x, 1100), f"Passwort {j + 1}", font=font(SEMI, 34), fill=mix(BG, col, aa), anchor="mm")
        d.text((W // 2, 1220), "1 Konto = 1 eigenes Passwort", font=font(BLACK, 52), fill=mix(BG, WH, aa), anchor="mm")
    return img


def s5(t0):  # Interaktionsfrage
    t = t0 + T4
    img = stock_bg(CLIP_PHONE, t0, dim=0.7); d = ImageDraw.Draw(img); header(d, LABEL)
    k = pop(t, E["deins?"] - 0.4)
    big(d, 480, "WIE LANG", 120, WH, k)
    big(d, 610, "IST DEINS?", 120, WH, k)
    kz = pop(t, E["Zahl."] - 0.1)
    if kz > 0:
        a = min(1, kz)
        d.rounded_rectangle([190, 730, 890, 870], radius=70, fill=mix(BG, PANEL, a), outline=mix(BG, SUB_HL, a), width=5)
        d.text((W // 2, 800), "NUR DIE ZAHL", font=font(BLACK, 72), fill=mix(BG, SUB_HL, a), anchor="mm")
        # Beispiel-Zahlen fliegen ein
        for j, (num, x) in enumerate([("8", 260), ("12", 540), ("20", 820)]):
            kn = pop(t, E["Zahl."] + 0.15 + j * 0.15)
            if kn > 0:
                d.text((x, 950), num, font=font(BLACK, 90), fill=mix(BG, CY, min(1, kn) * 0.9), anchor="mm")
    kp = pop(t, E["Passwort!"] - 0.1)
    if kp > 0:
        d.text((W // 2, 1060), "(nicht das Passwort!)", font=font(SEMI, 50), fill=mix(BG, RD, min(1, kp)), anchor="mm")
    kc = pop(t, E["Kommentare."])
    if kc > 0:
        a = min(1, kc); bounce = 12 * math.sin((t - E["Kommentare."]) * 9)
        x0, y0 = 800 + bounce, 1125
        d.line([(x0 - 120, y0 + 60), (x0 + 60, y0 - 40)], fill=mix(BG, SUB_HL, a), width=14)
        d.polygon([(x0 + 95, y0 - 60), (x0 + 30, y0 - 60), (x0 + 75, y0 - 5)], fill=mix(BG, SUB_HL, a))
    kf = pop(t, END - 0.95)
    if kf > 0:
        d.text((W // 2, 1255), "Folgen = morgen schlauer", font=font(BLACK, 50), fill=mix(BG, CY, min(1, kf)), anchor="mm")
    return img


SCENES = [("s1", s1, T1), ("s2", s2, T2 - T1), ("s3", s3, T3 - T2), ("s4", s4, T4 - T3), ("s5", s5, END - T4)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for st, txt in VOICE:
            print(f"{st:5.2f}–{st + say(txt)[1]:5.2f}  {txt}")
        print("END", END, "CD0", CD0)
        print(stills(SCENES, "/home/claude/bitweise-out/tag08", voice=VOICE))
    else:
        print(build(SCENES, "tag08_passwort", seed=8, voice=VOICE, pausen_ok=[PAUSE],
                    typing=[(CD0, 3, COUNT / 3)]))
        write_credits("Tag 08 – Rate mal: Passwort123")
