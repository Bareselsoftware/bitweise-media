"""Tag 15 – Mythos-Check: Macht ein VPN dich unsichtbar? (Format v3 + Experiment Mitmach-Einstieg:
Ja/Nein-Frage in Sek. 0–5, 3-s-Countdown, dann Auflösung; Tempo 0,82, ohne Ton-Akzent).
Fakten (Grundwissen, bewusst vereinfacht): Ein VPN verbirgt deine IP-Adresse vor der besuchten Website und
verschlüsselt den Verkehr bis zum VPN-Server – das WLAN/der Internetanbieter sieht nur noch die Verbindung zum VPN,
nicht mehr, welche Seiten du aufrufst. Es verhindert NICHT, dass dich Logins und Cookies erkennen; und der
VPN-Anbieter selbst kann sehen, wohin du dich verbindest. → Vertrauen wird verlagert, nicht abgeschafft."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *
import stil
import math

stil.AUSSPRACHE_WORT.setdefault("Cookies", "Kuckies")  # 24.11.: sonst „Kohkies“
say.__defaults__ = (0.82,)
LABEL = "MYTHOS-CHECK"
COUNT = 3.0

VOICE = timeline([
    "VPN an. Bist du jetzt unsichtbar?",
    "Ja oder nein? Rate mit!",
    ("Nein. Nur ein bisschen versteckt.", COUNT),
    "Ein VPN versteckt vor allem zwei Dinge.",
    "Deine IP-Adresse vor der Website.",
    "Und dein WLAN sieht nicht mehr, welche Seiten du aufrufst.",
    ("Aber: Bist du eingeloggt, weiß die Seite trotzdem, wer du bist.", 0.35),
    "Cookies bleiben auch.",
    "Und der VPN-Anbieter sieht jetzt, wohin du surfst.",
    ("Du bist also nicht unsichtbar. Du vertraust nur jemand anderem.", 0.35),
    ("Und du: Nutzt du ein VPN? Ja oder nein. Ab in die Kommentare.", 0.3),
])
WORDS = word_timings(VOICE)
END = VOICE[-1][0] + say(VOICE[-1][1])[1] + 1.0
CD0 = VOICE[1][0] + say(VOICE[1][1])[1] + 0.05
PAUSE = (CD0 - 0.06, VOICE[2][0] + 0.01)

T1 = VOICE[2][0] - 0.12
T2 = VOICE[6][0] - 0.15
T3 = VOICE[9][0] - 0.15


def _pick(q, i, kind="video"):
    return {h["id"]: h for h in stock_search(q, kind, n=12, lang="en")}[i]


CLIP_NIGHT = Clip(stock_get(_pick("laptop cafe", 47158)), start=0.5)      # Hände am Laptop, dunkel (2020)
CLIP_NET = Clip(stock_get(_pick("server network", 14900)), start=0.5)     # Netzwerk-Switch mit Kabeln (2018)
CLIP_PHONE = Clip(stock_get(_pick("smartphone night", 9490)), start=0.5)  # Hände tippen am Handy (2017)
CLIP_CAFE = Clip(stock_get(_pick("laptop cafe", 38057)), start=0.5)       # Laptop + Kaffeetasse (2020)

E = {k: at(WORDS, k) for k in ["unsichtbar?", "Ja", "nein?", "Rate", "Nein.", "versteckt.", "zwei",
                               "IP-Adresse", "WLAN", "eingeloggt,", "Cookies", "VPN-Anbieter",
                               "nicht", "vertraust", "Nutzt", "Kommentare."]}
E["Ja2"] = at(WORDS, "Ja", 1)
E["nein2"] = at(WORDS, "nein.")


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


def shield(d, cx, cy, s, col, a=1.0):
    """Schild-Symbol mit „VPN“."""
    w, h = int(150 * s), int(180 * s)
    pts = [(cx - w, cy - h), (cx + w, cy - h), (cx + w, cy), (cx, cy + h), (cx - w, cy)]
    d.polygon(pts, fill=mix(BG, col, a))
    d.text((cx, cy - int(40 * s)), "VPN", font=font(BLACK, int(110 * s)), fill=mix(BG, BG, a), anchor="mm")


OPTS = [("Ja", "A", "JA, UNSICHTBAR"), ("nein?", "B", "NEIN")]


def option(d, i, k, state=0):
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


def s1(t):  # Hook + Raten + Countdown (Schild + Frage stehen ab Frame 0)
    img = stock_bg(CLIP_NIGHT, t, dim=0.6)
    img = punch(img, t)
    d = ImageDraw.Draw(img); header(d, LABEL)
    shield(d, W // 2, 470, 0.95, CY)
    d.text((W // 2, 720), "JETZT UNSICHTBAR?", font=font(BLACK, 76), fill=WH, anchor="mm")
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
    d.text((250 + int(30 * (1 - kk)), y + 85), title, font=font(BLACK, 60), fill=mix(BG, WH, kk), anchor="ls")
    d.text((250, y + 140), sub, font=font(SEMI, 40), fill=mix(BG, GR, kk), anchor="ls")


def s2(t0):  # Auflösung + was ein VPN versteckt
    t = t0 + T1
    img = stock_bg(CLIP_NET, t0, dim=0.74); d = ImageDraw.Draw(img); header(d, LABEL)
    k = pop(t, E["Nein."] - 0.05)
    if k > 0:  # Stempel NEIN
        a = min(1, k); s = 1 + 0.35 * (1 - min(1, k))
        d.rounded_rectangle([W // 2 - int(260 * s), 400 - int(75 * s), W // 2 + int(260 * s), 400 + int(75 * s)],
                            radius=24, fill=mix(BG, RD, a))
        d.text((W // 2, 400), "NEIN", font=font(BLACK, int(100 * s)), fill=mix(BG, WH, a), anchor="mm")
    kv = pop(t, E["versteckt."] - 0.05)
    big(d, 540, "nur ein bisschen versteckt", 62, WH, kv)
    kz = pop(t, E["zwei"] - 0.1)
    if kz > 0:
        d.text((110, 680), "VPN VERSTECKT:", font=font(MONO, 44), fill=mix(BG, GN, min(1, kz)), anchor="ls")
    card(d, 720, pop(t, E["IP-Adresse"] - 0.05), check, GN, "Deine IP-Adresse", "vor der Website")
    card(d, 935, pop(t, E["WLAN"] - 0.05), check, GN, "Besuchte Seiten", "vor WLAN & Internetanbieter")
    return img


def s3(t0):  # was es NICHT versteckt
    t = t0 + T2
    img = stock_bg(CLIP_PHONE, t0, dim=0.76); d = ImageDraw.Draw(img); header(d, LABEL)
    a = ease(t0 / 0.3)
    big(d, 420, "ABER:", 110, RD, a)
    card(d, 540, pop(t, E["eingeloggt,"] - 0.05), cross, RD, "Eingeloggt?", "Die Seite weiß, wer du bist")
    card(d, 755, pop(t, E["Cookies"] - 0.05), cross, RD, "Cookies", "bleiben trotzdem")
    card(d, 970, pop(t, E["VPN-Anbieter"] - 0.05), cross, RD, "VPN-Anbieter", "sieht, wohin du surfst")
    return img


def s4(t0):  # Fazit + Interaktionsfrage
    t = t0 + T3
    img = stock_bg(CLIP_CAFE, t0, dim=0.72); d = ImageDraw.Draw(img); header(d, LABEL)
    kn = pop(t, VOICE[9][0])
    big(d, 400, "NICHT UNSICHTBAR", 84, RD, kn)
    kv = pop(t, E["vertraust"] - 0.1)
    big(d, 510, "nur anderes Vertrauen", 64, WH, kv)
    kq = pop(t, E["Nutzt"] - 0.1)
    big(d, 680, "Nutzt du ein VPN?", 92, WH, kq)
    for w, lab, x, col in (("Ja2", "JA", 300, GN), ("nein2", "NEIN", 780, RD)):
        kk = pop(t, E[w] - 0.05)
        if kk > 0:
            a = min(1, kk)
            d.rounded_rectangle([x - 200, 810, x + 200, 960], radius=75, fill=mix(BG, col, a))
            d.text((x, 887), lab, font=font(BLACK, 72), fill=BG, anchor="mm")
    kc = pop(t, E["Kommentare."])
    if kc > 0:
        a = min(1, kc)
        d.rounded_rectangle([170, 1020, 910, 1140], radius=60, fill=mix(BG, PANEL, a), outline=mix(BG, SUB_HL, a), width=4)
        d.text((W // 2, 1082), "Ab in die Kommentare", font=font(BLACK, 56), fill=mix(BG, SUB_HL, a), anchor="mm")
    kf = pop(t, END - 1.0)
    if kf > 0:
        d.text((W // 2, 1235), "Folgen = morgen schlauer", font=font(BLACK, 54), fill=mix(BG, CY, min(1, kf)), anchor="mm")
    return img


SCENES = [("s1", s1, T1), ("s2", s2, T2 - T1), ("s3", s3, T3 - T2), ("s4", s4, END - T3)]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        for st, txt in VOICE:
            print(f"{st:5.2f}–{st + say(txt)[1]:5.2f}  {txt}")
        print("END", END, "CD0", CD0)
        print(stills(SCENES, "/home/claude/bitweise-out/tag15", voice=VOICE))
    else:
        print(build(SCENES, "tag15_vpn", seed=15, voice=VOICE, pausen_ok=[PAUSE],
                    typing=[(CD0, 3, COUNT / 3)]))
        write_credits("Tag 15 – Mythos-Check: VPN")
