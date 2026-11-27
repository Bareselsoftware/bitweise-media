"""Tag 18 – Kurios/Rate mal: Warum Fotos vom Bildschirm Streifen haben (Moiré)
(Format v3 + Experiment Mitmach-Einstieg: Frage mit 3 Optionen in Sek. 0–5, 3-s-Countdown, dann Auflösung; Tempo 0,82).
Fakten (Grundwissen, bewusst vereinfacht): Ein Bildschirm besteht aus einem regelmäßigen Raster aus Pixeln, der
Bildsensor der Kamera ebenfalls aus einem regelmäßigen Raster lichtempfindlicher Pixel. Überlagern sich zwei feine
regelmäßige Muster mit leicht unterschiedlichem Abstand oder Winkel, entsteht ein grobes Interferenzmuster – der
Moiré-Effekt (bekanntes Alltagsbeispiel: zwei hintereinander hängende feine Gardinen). Weder Kamera noch Bildschirm
sind kaputt. Winkel oder Abstand ändern verschiebt die Überlagerung, die Streifen werden dadurch oft kleiner bzw.
schwächer (nicht garantiert → „oft“). Ein Screenshot nimmt das Bild direkt auf, ohne Kamera → kein Moiré."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *
import stil
import math
import numpy as np

say.__defaults__ = (0.82,)
stil.AUSSPRACHE_WORT["Moiré"] = "Moarée"           # sonst „Mo-i-re“
stil.AUSSPRACHE_WORT["Screenshot"] = "Skrihnschott"  # sonst englisch-deutsches Mischmasch
LABEL = "RATE MAL"
COUNT = 3.0

VOICE = timeline([
    "Foto vom Bildschirm. Überall Streifen.",
    "Woher kommen die?",
    ("Kamera kaputt? Bildschirm kaputt?", 0.2),
    "Oder keins von beiden? Rate mit!",
    ("Keins von beiden.", COUNT),
    "Dein Bildschirm hat winzige Pixel in Reihen.",
    "Der Sensor in deiner Kamera auch.",
    ("Zwei feine Gitter übereinander.", 0.3),
    "Passen sie nicht genau zusammen, entstehen große Streifen.",
    "Das nennt man Moiré.",
    "Gibt es auch bei zwei Gardinen hintereinander.",
    ("Halt das Handy etwas schräg.", 0.35),
    "Oder ändere den Abstand.",
    "Noch einfacher ist ein Screenshot.",
    ("Team Screenshot oder Team Foto?", 0.3),
    ("Schreib es in die Kommentare.", 0.2),
])
WORDS = word_timings(VOICE)
END = VOICE[-1][0] + say(VOICE[-1][1])[1] + 0.8
CD0 = VOICE[3][0] + say(VOICE[3][1])[1] + 0.05
PAUSE = (CD0 - 0.06, VOICE[4][0] + 0.01)

T1 = VOICE[4][0] - 0.12
T2 = VOICE[7][0] - 0.15
T3 = VOICE[11][0] - 0.15


def _pick(q, i, kind="video"):
    return {h["id"]: h for h in stock_search(q, kind, n=12, lang="en")}[i]


CLIP_CAM = Clip(stock_get(_pick("taking photo smartphone", 8255)), start=0.5)   # Handy-Kamera filmt (2017)
IMG_LED = stock_get(_pick("screen pixels", 3358312, "photo"))                    # Pixel-/LED-Raster (2018)
CLIP_HAND = Clip(stock_get(_pick("taking photo smartphone", 736)), start=0.0)   # Hände mit Handy (2015)

E = {k: at(WORDS, k) for k in ["Streifen.", "Kamera", "keins", "Rate", "Keins", "Pixel", "Sensor",
                               "Gitter", "Passen", "große", "Moiré.", "Gardinen", "schräg.", "Abstand",
                               "einfacher", "Team", "Kommentare."]}
E["Bildschirm2"] = at(WORDS, "Bildschirm", 1)   # Option B (2. Vorkommen)
E["Keins"] = at(WORDS, "Keins", 1)             # Auflösung (1. Vorkommen = Option C)


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


# ---------- Moiré-Grafik: zwei feine Linienraster übereinander ----------
def grating(w, h, pitch, ang, shift=0.0):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    a = math.radians(ang)
    u = (xx - w / 2) * math.cos(a) + (yy - h / 2) * math.sin(a) + shift
    return ((u % pitch) < pitch * 0.5).astype(np.float32)   # 1 = Linie (dunkel)


def moire(w, h, ang2, pitch=9.0, pitch2=None, show1=1.0, show2=1.0, col=CY):
    """Bild w×h: Raster 1 (senkrecht) und Raster 2 (leicht gedreht) als 'Folien' übereinander."""
    g1 = grating(w, h, pitch, 0.0) * show1
    g2 = grating(w, h, pitch2 or pitch, ang2) * show2
    light = (1 - g1) * (1 - g2)                      # Licht kommt nur durch, wo beide Folien offen sind
    base = np.array(BG, np.float32); c = np.array(col, np.float32)
    arr = base + (c - base) * light[..., None]
    return Image.fromarray(arr.clip(0, 255).astype(np.uint8))


def framed(img, box, pic, r=26, outline=WH, a=1.0):
    x0, y0, x1, y1 = box
    m = Image.new("L", (x1 - x0, y1 - y0), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, x1 - x0 - 1, y1 - y0 - 1], radius=r, fill=int(255 * a))
    img.paste(pic, (x0, y0), m)
    ImageDraw.Draw(img).rounded_rectangle(box, radius=r, outline=mix(BG, outline, a), width=5)


OPTS = [("Kamera", "A", "KAMERA KAPUTT"), ("Bildschirm2", "B", "BILDSCHIRM KAPUTT"), ("keins", "C", "KEINS VON BEIDEN")]


def option(d, i, k):
    if k <= 0:
        return
    a = min(1, k); y = 770 + i * 128; dx = int(40 * (1 - a))
    d.rounded_rectangle([110 + dx, y, 970, y + 110], radius=55, fill=mix(BG, PANEL, a), outline=mix(BG, CY, a), width=4)
    d.ellipse([132 + dx, y + 14, 214 + dx, y + 96], fill=mix(BG, CY, a))
    d.text((173 + dx, y + 55), OPTS[i][1], font=font(BLACK, 50), fill=BG, anchor="mm")
    d.text((245 + dx, y + 57), OPTS[i][2], font=font(BLACK, 56), fill=mix(BG, WH, a), anchor="lm")


def s1(t):  # Hook (Streifen-Foto + Frage ab Frame 0) + Raten + Countdown
    img = stock_bg(CLIP_CAM, t, dim=0.62)
    img = punch(img, t)
    # „Foto vom Bildschirm“ mit Moiré-Streifen, die sich langsam bewegen
    framed(img, (190, 320, 890, 600), moire(700, 280, 4.5 + 0.8 * math.sin(t * 1.3)), outline=WH)
    d = ImageDraw.Draw(img); header(d, LABEL)
    d.text((W // 2, 685), "WOHER DIE STREIFEN?", font=font(BLACK, 80), fill=WH, anchor="mm")
    E_OPT = [E["Kamera"], E["Bildschirm2"], E["keins"]]
    for i in range(3):
        option(d, i, pop(t, E_OPT[i] - 0.08))
    if t >= CD0 - 0.05:
        n = 3 - int((t - CD0) / (COUNT / 3))
        if n >= 1:
            ph = ((t - CD0) % (COUNT / 3)) / (COUNT / 3)
            r = 72; cy = 1222
            d.ellipse([W // 2 - r, cy - r, W // 2 + r, cy + r], outline=mix(BG, SUB_HL, 0.35), width=10)
            d.arc([W // 2 - r, cy - r, W // 2 + r, cy + r], -90, -90 + 360 * (1 - ph), fill=SUB_HL, width=10)
            sz = int(110 * (1 + 0.25 * (1 - ease(ph / 0.25))))
            d.text((W // 2, cy), str(n), font=font(BLACK, sz), fill=SUB_HL, anchor="mm")
    elif t >= E["Rate"] - 0.05:
        k = pop(t, E["Rate"] - 0.05)
        d.text((W // 2, 1222), "RATE MIT!", font=font(BLACK, 76), fill=mix(BG, SUB_HL, min(1, k)), anchor="mm")
    return img


def s2(t0):  # Auflösung C + Pixelraster Bildschirm/Sensor
    t = t0 + T1
    img = stock_bg(IMG_LED, t0, dim=0.74); d = ImageDraw.Draw(img); header(d, LABEL)
    k = pop(t, E["Keins"] - 0.05)
    if k > 0:  # Stempel C
        a = min(1, k); s = 1 + 0.35 * (1 - min(1, k))
        d.rounded_rectangle([W // 2 - int(400 * s), 400 - int(70 * s), W // 2 + int(400 * s), 400 + int(70 * s)],
                            radius=24, fill=mix(BG, GN, a))
        d.text((W // 2, 400), "C: KEINS VON BEIDEN", font=font(BLACK, int(70 * s)), fill=BG, anchor="mm")
    kp = pop(t, E["Pixel"] - 0.1)
    if kp > 0:
        a = min(1, kp)
        d.text((110, 540), "BILDSCHIRM", font=font(MONO, 42), fill=mix(BG, GR, a), anchor="ls")
        pic = moire(860, 230, 0.0, show2=0.0, col=CY)
        framed(img, (110, 560, 970, 790), pic, outline=CY, a=a)
        d = ImageDraw.Draw(img)
        d.text((W // 2, 850), "winzige Pixel in Reihen", font=font(BLACK, 54), fill=mix(BG, WH, a), anchor="mm")
    ks = pop(t, E["Sensor"] - 0.1)
    if ks > 0:
        a = min(1, ks)
        d.text((110, 960), "KAMERA-SENSOR", font=font(MONO, 42), fill=mix(BG, GR, a), anchor="ls")
        pic = moire(860, 230, 0.0, pitch=9.6, show1=0.0, col=SUB_HL)
        framed(img, (110, 980, 970, 1210), pic, outline=SUB_HL, a=a)
        d = ImageDraw.Draw(img)
        d.text((W // 2, 1265), "auch ein Raster", font=font(BLACK, 54), fill=mix(BG, WH, a), anchor="mm")
    return img


def s3(t0):  # Überlagerung → Moiré, Gardinen
    t = t0 + T2
    img = background(t)
    d = ImageDraw.Draw(img); header(d, LABEL)
    big(d, 390, "ZWEI GITTER ÜBEREINANDER", 64, CY, ease(t0 / 0.3))
    # Raster 2 schiebt sich über Raster 1, dann dreht es leicht → große Streifen
    slide = ease((t - E["Gitter"] + 0.2) / 1.0)
    turn = ease((t - E["Passen"]) / 1.5)
    ang = 3.0 * turn + 0.4 * math.sin(max(0, t - E["große"]) * 1.1) * turn
    w, h = 860, 560
    g1 = grating(w, h, 9.0, 0.0)
    g2 = grating(w, h, 9.0, ang)
    # Folie 2 nur rechts vom Schiebe-Rand sichtbar
    edge = int(w * (1 - slide))
    mask2 = np.zeros((h, w), np.float32); mask2[:, edge:] = 1.0
    light = (1 - g1) * (1 - g2 * mask2)
    base = np.array(BG, np.float32); c = np.array(CY, np.float32)
    pic = Image.fromarray((base + (c - base) * light[..., None]).clip(0, 255).astype(np.uint8))
    framed(img, (110, 450, 110 + w, 450 + h), pic, outline=CY)
    d = ImageDraw.Draw(img)
    km = pop(t, E["Moiré."] - 0.05)
    if km > 0:
        a = min(1, km)
        d.rounded_rectangle([250, 1060, 830, 1170], radius=55, fill=mix(BG, SUB_HL, a))
        d.text((W // 2, 1117), "MOIRÉ", font=font(BLACK, 80), fill=BG, anchor="mm")
    kg = pop(t, E["Gardinen"] - 0.1)
    if kg > 0:
        d.text((W // 2, 1240), "wie bei zwei Gardinen hintereinander", font=font(SEMI, 46),
               fill=mix(BG, WH, min(1, kg)), anchor="mm")
    return img


def card(d, y, k, title, sub, col=GN):
    if k <= 0:
        return
    kk = min(1, k)
    d.rounded_rectangle([90, y, 990, y + 150], radius=28, fill=mix(BG, PANEL, kk), outline=mix(BG, col, kk * 0.8), width=4)
    check(d, 165, y + 75, 1.15, col, kk)
    d.text((240 + int(30 * (1 - kk)), y + 72), title, font=font(BLACK, 56), fill=mix(BG, WH, kk), anchor="ls")
    d.text((240, y + 122), sub, font=font(SEMI, 38), fill=mix(BG, GR, kk), anchor="ls")


def s4(t0):  # Tipps + Interaktionsfrage
    t = t0 + T3
    img = stock_bg(CLIP_HAND, t0, dim=0.72); d = ImageDraw.Draw(img); header(d, LABEL)
    big(d, 370, "WENIGER STREIFEN", 74, CY, pop(t, VOICE[11][0]))
    card(d, 430, pop(t, E["schräg."] - 0.3), "Handy etwas schräg", "Winkel ändern")
    card(d, 600, pop(t, E["Abstand"] - 0.1), "Abstand ändern", "näher ran oder weiter weg")
    card(d, 770, pop(t, E["einfacher"] - 0.1), "Screenshot", "ganz ohne Kamera – keine Streifen", col=SUB_HL)
    kq = pop(t, VOICE[14][0])
    if kq > 0:
        a = min(1, kq)
        d.rounded_rectangle([90, 965, 485, 1085], radius=60, fill=mix(BG, PANEL, a), outline=mix(BG, SUB_HL, a), width=4)
        d.text((287, 1027), "SCREENSHOT", font=font(BLACK, 50), fill=mix(BG, SUB_HL, a), anchor="mm")
        d.text((W // 2, 1027), "vs", font=font(BLACK, 46), fill=mix(BG, GR, a), anchor="mm")
        d.rounded_rectangle([595, 965, 990, 1085], radius=60, fill=mix(BG, PANEL, a), outline=mix(BG, CY, a), width=4)
        d.text((792, 1027), "FOTO", font=font(BLACK, 50), fill=mix(BG, CY, a), anchor="mm")
    kc = pop(t, E["Kommentare."] - 0.6)
    if kc > 0:
        d.text((W // 2, 1150), "Team? Ab in die Kommentare!", font=font(BLACK, 52), fill=mix(BG, WH, min(1, kc)), anchor="mm")
    kf = pop(t, END - 1.0)
    if kf > 0:
        d.text((W // 2, 1245), "Folgen = morgen schlauer", font=font(BLACK, 52), fill=mix(BG, CY, min(1, kf)), anchor="mm")
    return img


SCENES = [("s1", s1, T1), ("s2", s2, T2 - T1), ("s3", s3, T3 - T2), ("s4", s4, END - T3)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for st, txt in VOICE:
            print(f"{st:5.2f}–{st + say(txt)[1]:5.2f}  {txt}")
        print("END", END, "CD0", CD0)
        print(stills(SCENES, "/home/claude/bitweise-out/tag18", voice=VOICE))
    else:
        print(build(SCENES, "tag18_moire", seed=18, voice=VOICE, pausen_ok=[PAUSE],
                    typing=[(CD0, 3, COUNT / 3)]))
        write_credits("Tag 18 – Kurios: Warum Fotos vom Bildschirm Streifen haben")
