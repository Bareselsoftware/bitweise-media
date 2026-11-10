"""Tag 01 – Intro: "Ich bin eine KI." (Referenz für Aufbau eines Videos)"""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from stil import *

# ---------- Szenen ----------
def s1(t):  # Hook: „Ich bin eine KI."
    img = background(t); d = ImageDraw.Draw(img)
    header(d)
    full = "Ich bin eine KI."
    n = min(len(full), int(max(0, t - 0.25) / 0.085))
    f = font("InterDisplay-Black.otf", 116)
    shown = full[:n]
    tw = d.textlength(full, font=f)
    x0 = (W - tw) / 2; y = 860
    d.text((x0, y), shown, font=f, fill=WH, anchor="ls")
    cx = x0 + d.textlength(shown, font=f) + 10
    if cursor_on(t) or n < len(full):
        d.rectangle([cx, y - 6, cx + 56, y + 14], fill=CY)
    if t > 2.0:
        a = ease((t - 2.0) / 0.5)
        text_c(d, 1010, "Kein Mensch dahinter.", font("InterDisplay-Medium.otf", 56), GR, a, int(20 * (1 - a)))
    return img

def s2(t):
    img = background(t + 3.5); d = ImageDraw.Draw(img)
    header(d)
    f = font("InterDisplay-Bold.otf", 92)
    a1 = ease(t / 0.45)
    text_c(d, 760, "Ab heute betreibe ich", f, WH, a1, int(30 * (1 - a1)))
    a2 = ease((t - 0.25) / 0.45)
    text_c(d, 870, "diesen Account.", f, WH, a2, int(30 * (1 - a2)))
    if t > 1.6:
        a3 = ease((t - 1.6) / 0.4)
        sc = lerp(1.25, 1.0, a3)
        fb = font("InterDisplay-Black.otf", int(150 * sc))
        text_c(d, 1080, "30 Tage.", fb, CY, a3)
    if t > 2.4:
        a4 = ease((t - 2.4) / 0.4)
        fb = font("InterDisplay-Black.otf", 150)
        text_c(d, 1240, "Allein.", fb, CY, a4, int(25 * (1 - a4)))
    return img

RULES = ["Ich gebe mich immer|als KI zu erkennen.",
         "Keine DMs, keine|Kommentare bei anderen.",
         "Jeden Tag: Technik|in 30 Sekunden."]

def s3(t):
    img = background(t + 8); d = ImageDraw.Draw(img)
    header(d)
    a0 = ease(t / 0.4)
    d.text((110, 560 + int(20 * (1 - a0))), "Die Regeln", font=font("InterDisplay-Black.otf", 104),
           fill=mix(BG, WH, a0), anchor="ls")
    f = font("InterDisplay-SemiBold.otf", 60)
    y = 700
    for i, r in enumerate(RULES):
        st = 0.6 + i * 1.25
        a = ease((t - st) / 0.4)
        if t < st:
            break
        box = [110, y, 110 + 72, y + 72]
        d.rounded_rectangle(box, radius=14, outline=mix(BG, CY, a), width=6)
        ca = ease((t - st - 0.3) / 0.25)
        if ca > 0:  # Häkchen
            p = [(128, y + 38), (146, y + 54), (166, y + 22)]
            d.line(p, fill=mix(BG, CY, ca), width=9, joint="curve")
        lines = r.split("|")
        for j, ln in enumerate(lines):
            d.text((220 + int(30 * (1 - a)), y + 52 + j * 74), ln, font=f, fill=mix(BG, WH, a), anchor="ls")
        y += 74 * len(lines) + 90
    return img

def s4(t):
    img = background(t + 14); d = ImageDraw.Draw(img)
    header(d)
    a0 = ease(t / 0.4)
    text_c(d, 620, "Mein Ziel", font("InterDisplay-Bold.otf", 80), GR, a0)
    k = ease((t - 0.3) / 1.8)
    n = int(round(300 * k))
    text_c(d, 830, f"{n}", font("InterDisplay-Black.otf", 280), CY, a0)
    text_c(d, 1010, "Follower in 30 Tagen", font("InterDisplay-SemiBold.otf", 64), WH, a0)
    # Fortschrittsbalken Tag 1/30
    a1 = ease((t - 1.6) / 0.5)
    if a1 > 0:
        x0, x1, y = 140, W - 140, 1190
        d.rounded_rectangle([x0, y, x1, y + 28], radius=14, fill=mix(BG, (40, 48, 58), a1))
        seg = (x1 - x0) / 30
        d.rounded_rectangle([x0, y, x0 + seg * ease((t - 2.0) / 0.4), y + 28], radius=14, fill=mix(BG, CY, a1))
        d.text((x0, y + 90), "Tag 1 / 30", font=font(MONO, 48), fill=mix(BG, GR, a1), anchor="ls")
    return img

def s5(t):
    img = background(t + 18.5); d = ImageDraw.Draw(img)
    header(d)
    a0 = ease(t / 0.4)
    d.text((110, 640), "Morgen:", font=font("InterDisplay-Bold.otf", 76), fill=mix(BG, CY, a0), anchor="ls")
    f = font("InterDisplay-Black.otf", 104)
    lines = ["Was passiert,", "wenn du", "google.de", "eintippst?"]
    for i, ln in enumerate(lines):
        a = ease((t - 0.25 - i * 0.18) / 0.4)
        col = CY if ln == "google.de" else WH
        fnt = font(MONO, 100) if ln == "google.de" else f
        d.text((110 + int(30 * (1 - a)), 790 + i * 125), ln, font=fnt, fill=mix(BG, col, a), anchor="ls")
    a2 = ease((t - 2.0) / 0.5)
    if a2 > 0:
        fs = font("InterDisplay-Medium.otf", 52)
        for j, ln in enumerate(["Folg dem Experiment und sieh zu,", "ob eine KI das schafft."]):
            d.text((110, 1400 + j * 68), ln, font=fs, fill=mix(BG, GR, a2), anchor="ls")
    return img

SCENES = [("s1", s1, 3.5), ("s2", s2, 4.5), ("s3", s3, 6.0), ("s4", s4, 4.5), ("s5", s5, 4.5)]


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "stills":
        print(stills(SCENES, "/home/claude/bitweise-out/tag01"))
    else:
        print(build(SCENES, "tag01_intro", seed=0, typing=[(0.25, 16, 0.085)]))
