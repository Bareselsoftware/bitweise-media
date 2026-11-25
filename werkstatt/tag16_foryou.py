"""Tag 16 – Kurios / Rate mal: Woher weiß TikTok, was dir gefällt? (Format v3 + Experiment Mitmach-Einstieg:
Rate-Frage mit 3 Optionen in Sek. 0–5, 3-s-Countdown, dann Auflösung; Tempo 0,82, ohne Ton-Akzent).
Fakten (TikTok Newsroom „How TikTok recommends videos #ForYou“, 2020; Grundwissen, bewusst vereinfacht):
Empfehlungen beruhen auf Interaktionen (Likes, Teilen, Kommentare, Anschauen bis zum Ende), Video-Infos
(Beschreibung, Sounds, Hashtags) und – schwächer – Geräte-/Kontoeinstellungen. Ob jemand ein längeres Video bis zum
Ende schaut, nennt TikTok einen starken Hinweis auf Interesse. Follower-Zahl und frühere Erfolge des Accounts sind
laut TikTok keine direkten Faktoren."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *
import stil
import math

stil.AUSSPRACHE_WORT.setdefault("TikTok", "Ticktock")   # sonst „Tick Tohk“
stil.AUSSPRACHE_WORT.setdefault("Likes", "Leiks")       # sonst „Likkes“
stil.AUSSPRACHE_WORT.setdefault("Hashtags", "Häschtäggs")
say.__defaults__ = (0.82,)
LABEL = "RATE MAL"
COUNT = 3.0

VOICE = timeline([
    "Woher weiß TikTok, was dir gefällt?",
    "Was zählt am meisten? Likes, Zuschauen oder Follower? Rate mit!",
    ("Zuschauen. Wie lange du dranbleibst.", COUNT),
    "Schaust du ein Video bis zum Ende, ist das ein starkes Signal.",
    "Wischt du sofort weiter, eher nicht.",
    ("Dazu kommen Likes, Kommentare und Teilen.", 0.35),
    "Und was im Video steckt: Ton, Hashtags, Beschreibung.",
    "Wie viele Follower jemand hat, ist laut TikTok kein direkter Faktor.",
    ("Heißt: Deine For You baust du selbst. Mit jedem Wisch.", 0.35),
    ("Und du: Was zeigt dir deine For You gerade? Ein Wort reicht. Ab in die Kommentare.", 0.3),
])
WORDS = word_timings(VOICE)
END = VOICE[-1][0] + say(VOICE[-1][1])[1] + 1.0
CD0 = VOICE[1][0] + say(VOICE[1][1])[1] + 0.05
PAUSE = (CD0 - 0.06, VOICE[2][0] + 0.01)

T1 = VOICE[2][0] - 0.12
T2 = VOICE[5][0] - 0.15
T3 = VOICE[8][0] - 0.15


def _pick(q, i, kind="video"):
    return {h["id"]: h for h in stock_search(q, kind, n=12, lang="en")}[i]


CLIP_FEED = Clip(stock_get(_pick("scrolling phone", 64595)), start=0.5)      # Feed-Raster auf dem Handy (2021)
CLIP_WATCH = Clip(stock_get(_pick("watching phone video", 79154)), start=0.5)  # Video quer auf dem Handy (2021)
CLIP_SCROLL = Clip(stock_get(_pick("scrolling phone", 44859)), start=0.5)    # Daumen scrollt (2020)
CLIP_HAND = Clip(stock_get(_pick("scrolling phone", 38084)), start=0.5)      # Hände mit Handy (2020)

E = {k: at(WORDS, k) for k in ["gefällt?", "Was", "Likes,", "Zuschauen", "Follower?", "Rate", "Zuschauen.",
                               "dranbleibst.", "Ende,", "Signal.", "Wischt", "nicht.", "Kommentare", "Teilen.",
                               "Ton,", "Hashtags,", "Beschreibung.", "Faktor.", "selbst.", "Wisch.",
                               "zeigt", "Wort", "Kommentare."]}
E["Follower2"] = at(WORDS, "Follower", 1)
E["Zuschauen."] = at(WORDS, "Zuschauen", 1)
E["Kommentare."] = at(WORDS, "Kommentare", 1)


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


OPTS = [("Likes,", "A", "LIKES"), ("Zuschauen", "B", "ZUSCHAUEN"), ("Follower?", "C", "FOLLOWER")]


def option(d, i, k):
    if k <= 0:
        return
    a = min(1, k); y = 640 + i * 145; dx = int(40 * (1 - a))
    d.rounded_rectangle([170 + dx, y, 910, y + 120], radius=60, fill=mix(BG, PANEL, a), outline=mix(BG, CY, a), width=4)
    d.ellipse([195 + dx, y + 18, 279 + dx, y + 102], fill=mix(BG, CY, a))
    d.text((237 + dx, y + 60), OPTS[i][1], font=font(BLACK, 50), fill=BG, anchor="mm")
    d.text((310 + dx, y + 62), OPTS[i][2], font=font(BLACK, 62), fill=mix(BG, WH, a), anchor="lm")


def s1(t):  # Hook + Raten + Countdown (Frage steht ab Frame 0)
    img = stock_bg(CLIP_FEED, t, dim=0.62)
    img = punch(img, t)
    d = ImageDraw.Draw(img); header(d, LABEL)
    d.text((W // 2, 330), "DEINE FOR YOU", font=font(MONO, 46), fill=CY, anchor="mm")
    d.text((W // 2, 430), "Woher weiß TikTok,", font=font(BLACK, 76), fill=WH, anchor="mm")
    d.text((W // 2, 525), "was dir gefällt?", font=font(BLACK, 76), fill=WH, anchor="mm")
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
    elif t >= E["Was"] - 0.05:
        k = pop(t, E["Was"] - 0.05)
        d.text((W // 2, 1195), "WAS ZÄHLT AM MEISTEN?", font=font(BLACK, 58), fill=mix(BG, WH, min(1, k)), anchor="mm")
    return img


def s2(t0):  # Auflösung: Zuschauen
    t = t0 + T1
    img = stock_bg(CLIP_WATCH, t0, dim=0.74); d = ImageDraw.Draw(img); header(d, LABEL)
    k = pop(t, E["Zuschauen."] - 0.05)
    if k > 0:  # Stempel B
        a = min(1, k); s = 1 + 0.35 * (1 - min(1, k))
        d.rounded_rectangle([W // 2 - int(380 * s), 400 - int(75 * s), W // 2 + int(380 * s), 400 + int(75 * s)],
                            radius=24, fill=mix(BG, GN, a))
        d.text((W // 2, 400), "B: ZUSCHAUEN", font=font(BLACK, int(90 * s)), fill=mix(BG, BG, a), anchor="mm")
    big(d, 540, "wie lange du dranbleibst", 62, WH, pop(t, E["dranbleibst."] - 0.25))
    # Fortschrittsbalken eines Videos bis zum Ende
    if t > E["Ende,"] - 0.6:
        kk = ease((t - E["Ende,"] + 0.6) / 0.7)
        x0, x1, y = 130, 950, 700
        d.rounded_rectangle([x0, y, x1, y + 40], radius=20, fill=PANEL)
        d.rounded_rectangle([x0, y, x0 + max(40, int((x1 - x0) * kk)), y + 40], radius=20, fill=GN)
        d.text((x0, y + 100), "bis zum Ende geschaut", font=font(SEMI, 46), fill=WH, anchor="lm")
        ks = pop(t, E["Signal."] - 0.2)
        if ks > 0:
            check(d, 900, y + 100, 1.4, GN, min(1, ks))
            big(d, 900, "STARKES SIGNAL", 84, GN, ks)
    kw = pop(t, E["Wischt"] - 0.05)
    if kw > 0:
        a = min(1, kw)
        d.rounded_rectangle([110, 1020, 970, 1190], radius=28, fill=mix(BG, PANEL, a), outline=mix(BG, RD, a * 0.8), width=4)
        ph = ((t - E["Wischt"]) % 0.8) / 0.8
        y = 1130 - 60 * ease(ph)
        d.polygon([(200, y - 30), (170, y + 10), (230, y + 10)], fill=mix(BG, WH, a * (1 - ph)))
        d.text((280, 1090), "Sofort weggewischt", font=font(BLACK, 58), fill=mix(BG, WH, a), anchor="ls")
        d.text((280, 1150), "eher kein Interesse", font=font(SEMI, 42), fill=mix(BG, GR, a), anchor="ls")
    return img


def card(d, y, k, mark, col, title, sub):
    if k <= 0:
        return
    kk = min(1, k)
    d.rounded_rectangle([90, y, 990, y + 175], radius=28, fill=mix(BG, PANEL, kk), outline=mix(BG, col, kk * 0.8), width=4)
    mark(d, 170, y + 88, 1.25, col, kk)
    d.text((250 + int(30 * (1 - kk)), y + 85), title, font=font(BLACK, 58), fill=mix(BG, WH, kk), anchor="ls")
    d.text((250, y + 140), sub, font=font(SEMI, 40), fill=mix(BG, GR, kk), anchor="ls")


def s3(t0):  # weitere Signale + Follower kein Faktor
    t = t0 + T2
    img = stock_bg(CLIP_SCROLL, t0, dim=0.76); d = ImageDraw.Draw(img); header(d, LABEL)
    big(d, 420, "AUSSERDEM", 96, CY, ease(t0 / 0.3))
    card(d, 540, pop(t, at(WORDS, "Likes", 1) - 0.05), check, GN, "Likes, Kommentare", "und Teilen")
    card(d, 755, pop(t, E["Ton,"] - 0.05), check, GN, "Ton, Hashtags", "und Beschreibung")
    card(d, 970, pop(t, E["Follower2"] - 0.05), cross, RD, "Follower-Zahl", "laut TikTok kein direkter Faktor")
    return img


def s4(t0):  # Fazit + Interaktionsfrage
    t = t0 + T3
    img = stock_bg(CLIP_HAND, t0, dim=0.72); d = ImageDraw.Draw(img); header(d, LABEL)
    big(d, 400, "DEINE FOR YOU", 84, CY, pop(t, VOICE[8][0]))
    big(d, 510, "baust du selbst", 70, WH, pop(t, E["selbst."] - 0.3))
    kq = pop(t, E["zeigt"] - 0.2)
    big(d, 690, "Was zeigt dir", 88, WH, kq)
    big(d, 790, "deine For You?", 88, WH, kq)
    kw = pop(t, E["Wort"])
    if kw > 0:
        a = min(1, kw)
        d.rounded_rectangle([240, 880, 840, 1000], radius=60, fill=mix(BG, PANEL, a), outline=mix(BG, SUB_HL, a), width=4)
        d.text((W // 2, 942), "1 Wort reicht", font=font(BLACK, 58), fill=mix(BG, SUB_HL, a), anchor="mm")
    kc = pop(t, E["Kommentare."])
    if kc > 0:
        a = min(1, kc)
        d.rounded_rectangle([170, 1040, 910, 1160], radius=60, fill=mix(BG, PANEL, a), outline=mix(BG, SUB_HL, a), width=4)
        d.text((W // 2, 1102), "Ab in die Kommentare", font=font(BLACK, 56), fill=mix(BG, SUB_HL, a), anchor="mm")
    kf = pop(t, END - 1.0)
    if kf > 0:
        d.text((W // 2, 1245), "Folgen = morgen schlauer", font=font(BLACK, 54), fill=mix(BG, CY, min(1, kf)), anchor="mm")
    return img


SCENES = [("s1", s1, T1), ("s2", s2, T2 - T1), ("s3", s3, T3 - T2), ("s4", s4, END - T3)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for st, txt in VOICE:
            print(f"{st:5.2f}–{st + say(txt)[1]:5.2f}  {txt}")
        print("END", END, "CD0", CD0)
        print(stills(SCENES, "/home/claude/bitweise-out/tag16", voice=VOICE))
    else:
        print(build(SCENES, "tag16_foryou", seed=16, voice=VOICE, pausen_ok=[PAUSE],
                    typing=[(CD0, 3, COUNT / 3)]))
        write_credits("Tag 16 – Rate mal: Woher weiß TikTok, was dir gefällt?")
