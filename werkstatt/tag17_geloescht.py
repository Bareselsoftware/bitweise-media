"""Tag 17 – Mythos-Check: Gelöscht ist gelöscht? (Format v3 + Experiment Mitmach-Einstieg:
Ja/Nein-Frage in Sek. 0–5, 3-s-Countdown, dann Auflösung; Tempo 0,82, ohne Ton-Akzent).
Fakten (Grundwissen, bewusst vereinfacht): Gelöschte Dateien landen zuerst im Papierkorb; am Handy in
„Zuletzt gelöscht“ (iPhone-Fotos: 30 Tage; Google Fotos: 30 bzw. 60 Tage) → „oft dreißig Tage“.
Nach dem Leeren gibt eine klassische Festplatte (HDD) nur den Platz frei; die Daten bleiben, bis sie überschrieben
werden → Rettungsprogramme kommen oft wieder ran. Moderne Handys sind verschlüsselt und räumen gelöschte Bereiche
selbst auf (Flash-Speicher/TRIM) → dort ist es meist wirklich weg. Vor dem Verkauf: auf Werkseinstellungen
zurücksetzen (löscht bei verschlüsselten Handys den Schlüssel), nicht nur einzelne Fotos löschen."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *
import stil
import math

say.__defaults__ = (0.82,)
LABEL = "MYTHOS-CHECK"
COUNT = 3.0

VOICE = timeline([
    "Gelöscht ist gelöscht. Oder?",
    "Für immer weg?",
    ("Ja oder nein? Rate mit!", 0.2),
    ("Nein. Zumindest nicht sofort.", COUNT),
    "Zuerst landet alles im Papierkorb.",
    "Am Handy: Zuletzt gelöscht. Oft für dreißig Tage.",
    ("Und selbst nach dem Leeren?", 0.35),
    "Eine klassische Festplatte gibt nur den Platz frei.",
    "Die Daten bleiben, bis Neues drüber geschrieben wird.",
    "Rettungsprogramme holen sie oft zurück.",
    "Moderne Handys sind verschlüsselt.",
    ("Da ist es meist weg.", 0.2),
    ("Altes Handy verkaufen? Auf Werkseinstellungen zurücksetzen.", 0.35),
    "Nicht nur die Fotos löschen.",
    ("Schon mal was aus Versehen gelöscht?", 0.3),
    ("Ja oder nein. Ab in die Kommentare.", 0.25),
])
WORDS = word_timings(VOICE)
END = VOICE[-1][0] + say(VOICE[-1][1])[1] + 0.8
CD0 = VOICE[2][0] + say(VOICE[2][1])[1] + 0.05
PAUSE = (CD0 - 0.06, VOICE[3][0] + 0.01)

T1 = VOICE[3][0] - 0.12
T2 = VOICE[6][0] - 0.15
T3 = VOICE[12][0] - 0.15


def _pick(q, i, kind="video"):
    return {h["id"]: h for h in stock_search(q, kind, n=12, lang="en")}[i]


CLIP_LAPTOP = Clip(stock_get(_pick("computer keyboard typing", 43559)), start=0.5)  # Laptop-Tastatur (2020)
CLIP_PHONE = Clip(stock_get(_pick("smartphone photos", 3176)), start=0.5)          # Finger tippt aufs Handy (2016)
CLIP_HDD = Clip(stock_get(_pick("hard drive", 73328)), start=1.0)                  # offene Festplatte (2021)
CLIP_HAND = Clip(stock_get(_pick("smartphone photos", 736)), start=0.0)            # Hände mit Handy (2015)

E = {k: at(WORDS, k) for k in ["Oder?", "immer", "Ja", "nein?", "Rate", "Nein.", "sofort.", "Papierkorb.",
                               "Handy", "Zuletzt", "dreißig", "Leeren?", "Festplatte", "frei.", "bleiben,",
                               "Neues", "Rettungsprogramme", "verschlüsselt.", "Altes",
                               "Werkseinstellungen", "Fotos", "Versehen", "Kommentare."]}
E["Handy2"] = at(WORDS, "Handys")


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


def cross(d, cx, cy, s, col, a):
    c = mix(BG, col, a); r = int(20 * s)
    d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=c, width=int(9 * s))
    d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=c, width=int(9 * s))


def trash(d, cx, cy, s, col, a=1.0):
    """Papierkorb-Symbol."""
    c = mix(BG, col, a)
    w, h = int(80 * s), int(110 * s)
    d.rounded_rectangle([cx - int(60 * s), cy - h - int(28 * s), cx + int(60 * s), cy - h - int(10 * s)], radius=int(6 * s), fill=c)
    d.rounded_rectangle([cx - int(22 * s), cy - h - int(44 * s), cx + int(22 * s), cy - h - int(24 * s)], radius=int(6 * s), fill=c)
    d.polygon([(cx - w, cy - h), (cx + w, cy - h), (cx + int(62 * s), cy + int(70 * s)), (cx - int(62 * s), cy + int(70 * s))], fill=c)
    for dx in (-35, 0, 35):
        d.line([(cx + int(dx * s), cy - h + int(25 * s)), (cx + int(dx * 0.8 * s), cy + int(50 * s))], fill=BG, width=max(3, int(10 * s)))


OPTS = [("Ja", "A", "JA, FÜR IMMER"), ("nein?", "B", "NEIN")]


def option(d, i, k):
    if k <= 0:
        return
    a = min(1, k); y = 790 + i * 155; dx = int(40 * (1 - a))
    d.rounded_rectangle([150 + dx, y, 930, y + 130], radius=65, fill=mix(BG, PANEL, a), outline=mix(BG, CY, a), width=4)
    d.ellipse([175 + dx, y + 20, 265 + dx, y + 110], fill=mix(BG, CY, a))
    d.text((220 + dx, y + 65), OPTS[i][1], font=font(BLACK, 52), fill=BG, anchor="mm")
    d.text((300 + dx, y + 67), OPTS[i][2], font=font(BLACK, 64), fill=mix(BG, WH, a), anchor="lm")


def s1(t):  # Hook + Raten + Countdown (Papierkorb + Frage stehen ab Frame 0)
    img = stock_bg(CLIP_LAPTOP, t, dim=0.62)
    img = punch(img, t)
    d = ImageDraw.Draw(img); header(d, LABEL)
    trash(d, W // 2, 470, 1.15, CY)
    d.text((W // 2, 690), "GELÖSCHT = WEG?", font=font(BLACK, 82), fill=WH, anchor="mm")
    for i, (w, _, _) in enumerate(OPTS):
        option(d, i, pop(t, E[w] - 0.08))
    if t >= CD0 - 0.05:
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


def card(d, y, k, mark, col, title, sub):
    if k <= 0:
        return
    kk = min(1, k)
    d.rounded_rectangle([90, y, 990, y + 175], radius=28, fill=mix(BG, PANEL, kk), outline=mix(BG, col, kk * 0.8), width=4)
    mark(d, 170, y + 88, 1.25, col, kk)
    d.text((250 + int(30 * (1 - kk)), y + 85), title, font=font(BLACK, 58), fill=mix(BG, WH, kk), anchor="ls")
    d.text((250, y + 140), sub, font=font(SEMI, 40), fill=mix(BG, GR, kk), anchor="ls")


def s2(t0):  # Auflösung: Nein + Papierkorb / Zuletzt gelöscht
    t = t0 + T1
    img = stock_bg(CLIP_PHONE, t0, dim=0.74); d = ImageDraw.Draw(img); header(d, LABEL)
    k = pop(t, E["Nein."] - 0.05)
    if k > 0:  # Stempel B
        a = min(1, k); s = 1 + 0.35 * (1 - min(1, k))
        d.rounded_rectangle([W // 2 - int(260 * s), 400 - int(75 * s), W // 2 + int(260 * s), 400 + int(75 * s)],
                            radius=24, fill=mix(BG, RD, a))
        d.text((W // 2, 400), "B: NEIN", font=font(BLACK, int(100 * s)), fill=BG, anchor="mm")
    big(d, 540, "zumindest nicht sofort", 62, WH, pop(t, E["sofort."] - 0.3))
    kp = pop(t, E["Papierkorb."] - 0.1)
    if kp > 0:
        a = min(1, kp)
        trash(d, 210, 760, 0.75, CY, a)
        d.text((330, 730), "Papierkorb", font=font(BLACK, 66), fill=mix(BG, WH, a), anchor="lm")
        d.text((330, 800), "am Computer", font=font(SEMI, 44), fill=mix(BG, GR, a), anchor="lm")
    kz = pop(t, E["Zuletzt"] - 0.05)
    if kz > 0:
        a = min(1, kz)
        d.rounded_rectangle([90, 920, 990, 1150], radius=28, fill=mix(BG, PANEL, a), outline=mix(BG, CY, a * 0.8), width=4)
        d.text((W // 2, 990), "Handy: „Zuletzt gelöscht“", font=font(BLACK, 58), fill=mix(BG, WH, a), anchor="mm")
        kd = pop(t, E["dreißig"] - 0.05)
        if kd > 0:
            d.text((W // 2, 1085), "oft 30 Tage aufgehoben", font=font(BLACK, 56), fill=mix(BG, SUB_HL, min(1, kd)), anchor="mm")
    return img


def s3(t0):  # Festplatte vs. Handy
    t = t0 + T2
    img = stock_bg(CLIP_HDD, t0, dim=0.76); d = ImageDraw.Draw(img); header(d, LABEL)
    big(d, 380, "PAPIERKORB GELEERT?", 76, CY, ease(t0 / 0.3))
    kf = pop(t, E["Festplatte"] - 0.1)
    if kf > 0:
        a = min(1, kf)
        d.text((90, 490), "FESTPLATTE", font=font(MONO, 44), fill=mix(BG, GR, a), anchor="lm")
        # 8 Blöcke: Datei (cyan) → als „frei“ markiert (gestrichelt), Daten noch da → überschrieben (grau)
        frei = t >= E["frei."] - 0.2
        neu = max(0.0, min(1.0, (t - E["Neues"] + 0.1) / 1.4))
        for i in range(8):
            x0 = 90 + i * 115; y0 = 530
            over = i < int(round(neu * 5))
            col = GR if over else CY
            d.rounded_rectangle([x0, y0, x0 + 100, y0 + 100], radius=14, fill=mix(BG, mix(PANEL, col, 0.55), a),
                                outline=mix(BG, WH if frei and not over else col, a), width=5 if frei else 3)
            d.text((x0 + 50, y0 + 50), "neu" if over else "01", font=font(MONO, 34), fill=mix(BG, WH, a), anchor="mm")
        if frei:
            d.text((90, 690), "Platz „frei“ – Daten noch da", font=font(SEMI, 46), fill=mix(BG, WH, min(1, pop(t, E["frei."] - 0.2))), anchor="lm")
    card(d, 760, pop(t, E["Rettungsprogramme"] - 0.05), check, GN, "Oft rettbar", "mit Rettungsprogrammen")
    card(d, 975, pop(t, E["Handy2"] - 0.05), cross, RD, "Modernes Handy", "verschlüsselt: meist endgültig weg")
    return img


def s4(t0):  # Tipp + Interaktionsfrage
    t = t0 + T3
    img = stock_bg(CLIP_HAND, t0, dim=0.72); d = ImageDraw.Draw(img); header(d, LABEL)
    big(d, 380, "ALTES HANDY VERKAUFEN?", 70, CY, pop(t, VOICE[12][0]))
    kw = pop(t, E["Werkseinstellungen"] - 0.1)
    if kw > 0:
        a = min(1, kw)
        d.rounded_rectangle([90, 450, 990, 560], radius=55, fill=mix(BG, PANEL, a), outline=mix(BG, GN, a), width=4)
        check(d, 165, 505, 1.1, GN, a)
        d.text((230, 507), "Werkseinstellungen", font=font(BLACK, 58), fill=mix(BG, WH, a), anchor="lm")
    kn = pop(t, E["Fotos"] - 0.1)
    if kn > 0:
        a = min(1, kn)
        d.rounded_rectangle([90, 590, 990, 700], radius=55, fill=mix(BG, PANEL, a), outline=mix(BG, RD, a), width=4)
        cross(d, 165, 645, 1.0, RD, a)
        d.text((230, 647), "nur Fotos löschen", font=font(BLACK, 58), fill=mix(BG, GR, a), anchor="lm")
    kq = pop(t, VOICE[14][0])
    big(d, 820, "Schon mal was aus", 80, WH, kq)
    big(d, 915, "Versehen gelöscht?", 80, WH, kq)
    kc = pop(t, E["Kommentare."] - 0.6)
    if kc > 0:
        a = min(1, kc)
        d.rounded_rectangle([170, 1010, 910, 1130], radius=60, fill=mix(BG, PANEL, a), outline=mix(BG, SUB_HL, a), width=4)
        d.text((W // 2, 1072), "Ja oder nein? Kommentar!", font=font(BLACK, 52), fill=mix(BG, SUB_HL, a), anchor="mm")
    kf = pop(t, END - 1.0)
    if kf > 0:
        d.text((W // 2, 1230), "Folgen = morgen schlauer", font=font(BLACK, 54), fill=mix(BG, CY, min(1, kf)), anchor="mm")
    return img


SCENES = [("s1", s1, T1), ("s2", s2, T2 - T1), ("s3", s3, T3 - T2), ("s4", s4, END - T3)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for st, txt in VOICE:
            print(f"{st:5.2f}–{st + say(txt)[1]:5.2f}  {txt}")
        print("END", END, "CD0", CD0)
        print(stills(SCENES, "/home/claude/bitweise-out/tag17", voice=VOICE))
    else:
        print(build(SCENES, "tag17_geloescht", seed=17, voice=VOICE, pausen_ok=[PAUSE],
                    typing=[(CD0, 3, COUNT / 3)]))
        write_credits("Tag 17 – Mythos-Check: Gelöscht ist gelöscht?")
