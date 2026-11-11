"""bitweise.ki – gemeinsame Stil- und Render-Bibliothek.

Nutzung in einem Video-Skript:
    from stil import *
    def s1(t): img = background(t); d = ImageDraw.Draw(img); header(d); ...; return img
    build([("s1", s1, 3.5), ...], "tagXX_thema", seed=XX, typing=[(start, anzahl, abstand)])

Format: 1080x1920, 30 fps, H.264 CRF 18. Sichere Zone: oben ab y=300, unten bis y=1500,
rechts 150 px frei (TikTok-/Reels-Bedienelemente).
"""
import os, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
BG = (14, 17, 22)
CY = (0, 229, 255)      # Akzent
WH = (240, 244, 248)    # Haupttext
GR = (138, 148, 160)    # Nebentext
RD = (255, 92, 92)      # nur für "falsch"/Mythos
GN = (80, 220, 140)     # nur für "richtig"
PANEL = (28, 34, 43)
INTER = "/usr/share/fonts/opentype/inter/"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
BLACK, BOLD, SEMI, MED = "InterDisplay-Black.otf", "InterDisplay-Bold.otf", "InterDisplay-SemiBold.otf", "InterDisplay-Medium.otf"

_fc = {}
def font(name, size):
    k = (name, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(name if name.startswith("/") else INTER + name, size)
    return _fc[k]

def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3

def lerp(a, b, t):
    return a + (b - a) * t

def mix(c1, c2, a):
    a = max(0.0, min(1.0, a))
    return tuple(int(lerp(c1[i], c2[i], a)) for i in range(3))

_grid = None
def background(t):
    """Dunkler Grund mit feinem, langsam driftendem Pixelraster."""
    global _grid
    if _grid is None:
        g = Image.new("RGB", (W, H + 120), BG)
        d = ImageDraw.Draw(g)
        rng = np.random.default_rng(7)
        for y in range(0, H + 120, 60):
            for x in range(0, W, 60):
                c = mix(BG, CY, 0.05 if rng.random() > 0.93 else 0.018)
                d.rounded_rectangle([x + 22, y + 22, x + 38, y + 38], radius=4, fill=c)
        _grid = g
    off = int((t * 14) % 60)
    return _grid.crop((0, off, W, off + H)).copy()

def logo(d, x=90, y=150, s=12, alpha=1.0):
    pat = ["X....", "X....", "XXXX.", "X...X", "X...X", "X...X", "XXXX."]
    for r, row in enumerate(pat):
        for c, ch in enumerate(row):
            if ch == "X":
                d.rounded_rectangle([x + c * s, y + r * s, x + c * s + s - 3, y + r * s + s - 3],
                                    radius=3, fill=mix(BG, CY, alpha))
    d.text((x + 6 * s + 14, y + 7 * s - 4), "bitweise.ki", font=font(SEMI, 40), fill=mix(BG, GR, alpha), anchor="ls")

def header(d, label=None):
    """Logo oben links; optional Serien-Label oben rechts (z. B. 'MYTHOS-CHECK')."""
    logo(d)
    if label:
        f = font(MONO, 34)
        tw = d.textlength(label, font=f)
        d.rounded_rectangle([W - 90 - tw - 36, 148, W - 90, 210], radius=12, outline=CY, width=3)
        d.text((W - 90 - tw - 18, 192), label, font=f, fill=CY, anchor="ls")

def text_c(d, y, s, f, fill, alpha=1.0, dy=0):
    d.text((W // 2, y + dy), s, font=f, fill=mix(BG, fill, alpha), anchor="mm")

def text_l(d, x, y, s, f, fill, alpha=1.0, dx=0):
    d.text((x + dx, y), s, font=f, fill=mix(BG, fill, alpha), anchor="ls")

def cursor_on(t):
    return int(t * 2.2) % 2 == 0

def typed(full, t, start, step=0.085):
    """Schreibmaschinen-Effekt: liefert den bis Zeit t getippten Teil."""
    return full[:min(len(full), int(max(0, t - start) / step))]

def wrap(d, s, f, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        test = (cur + " " + w_).strip()
        if d.textlength(test, font=f) <= maxw:
            cur = test
        else:
            lines.append(cur); cur = w_
    lines.append(cur)
    return lines

def scene_fade(img, t, dur, fin=0.2, fout=0.2):
    a = min(1.0, t / fin) if fin else 1.0
    b = min(1.0, (dur - t) / fout) if fout else 1.0
    k = max(0.0, min(a, b))
    return img if k >= 1 else Image.blend(Image.new("RGB", (W, H), BG), img, k)

# ---------------- Render ----------------
def render_scene(outdir, name, fn, dur, fin, fout):
    tmp = f"{outdir}/{name}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(round(dur * FPS))):
        t = i / FPS
        p.stdin.write(scene_fade(fn(t), t, dur, fin, fout).tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit(f"Render {name} fehlgeschlagen")
    os.replace(tmp, f"{outdir}/{name}.mp4")

def stills(scenes, outdir, at=0.9):
    """Zeichnet je Szene ein Standbild bei Anteil `at` der Dauer + Kontaktbogen zum Prüfen."""
    os.makedirs(outdir, exist_ok=True)
    ims = []
    for name, fn, dur in scenes:
        im = fn(dur * at); im.save(f"{outdir}/still_{name}.png"); ims.append(im.resize((360, 640)))
    c = Image.new("RGB", (370 * len(ims), 640), (60, 60, 60))
    for i, im in enumerate(ims):
        c.paste(im, (i * 370, 0))
    c.save(f"{outdir}/kontaktbogen.png")
    return f"{outdir}/kontaktbogen.png"

# ---------------- Stimme (Piper, Thorsten-Voice, MIT) ----------------
STIMME_DIR = "/home/claude/stimme"
STIMME = "de_DE-thorsten-high"
STIMME_URL = "https://huggingface.co/Thorsten-Voice/Piper/resolve/main/"
_voice = None
_say_cache = {}

def _ensure_voice():
    """Lädt piper-tts und das Stimmmodell bei Bedarf (geplante Läufe starten leer)."""
    global _voice
    if _voice is not None:
        return _voice
    try:
        import piper  # noqa
    except ImportError:
        subprocess.run(["pip", "install", "--break-system-packages", "-q", "piper-tts"], check=True)
    os.makedirs(STIMME_DIR, exist_ok=True)
    for ext in (".onnx.json", ".onnx"):
        f = f"{STIMME_DIR}/{STIMME}{ext}"
        if not os.path.exists(f) or os.path.getsize(f) < 1000:
            subprocess.run(["curl", "-sSfL", "-o", f, STIMME_URL + STIMME + ext], check=True)
    from piper import PiperVoice
    _voice = PiperVoice.load(f"{STIMME_DIR}/{STIMME}.onnx")
    return _voice

def say(text, tempo=0.95):
    """Spricht `text` (Deutsch). Liefert (samples float32 @44,1 kHz, dauer_s). Zahlen ausschreiben!
    Dauer vorab abfragen, um Szenenlängen passend zu wählen: say("...")[1]"""
    key = (text, tempo)
    if key in _say_cache:
        return _say_cache[key]
    from piper import SynthesisConfig
    v = _ensure_voice()
    chunks = [c.audio_int16_array for c in v.synthesize(text, syn_config=SynthesisConfig(length_scale=tempo))]
    a = np.concatenate(chunks).astype(np.float32) / 32768.0
    sr0 = v.config.sample_rate
    n = int(len(a) * 44100 / sr0)
    a = np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)
    # Stille am Rand kappen
    idx = np.where(np.abs(a) > 0.01)[0]
    if len(idx):
        a = a[max(0, idx[0] - 800): idx[-1] + 2000]
    _say_cache[key] = (a, len(a) / 44100)
    return _say_cache[key]

def check_voice(voice, total, gap=0.12):
    """Bricht ab, wenn Sprechtexte sich überlappen (Mindestpause `gap` s) oder übers Ende laufen."""
    v = sorted(voice)
    errs = []
    for i, (start, text) in enumerate(v):
        end = start + say(text)[1]
        nxt = v[i + 1][0] if i + 1 < len(v) else total
        if end + (gap if i + 1 < len(v) else 0) > nxt:
            errs.append(f"{start:.2f}–{end:.2f}s überlappt mit nächstem Einsatz bei {nxt:.2f}s: {text!r}")
    if errs:
        raise SystemExit("SPRECHTEXT-TIMING FEHLERHAFT – Startzeiten/Szenen anpassen:\n" + "\n".join(errs))

def _voice_track(n, voice):
    sr = 44100
    tr = np.zeros(n, dtype=np.float32)
    for start, text in voice:
        a, _ = say(text)
        s0 = int(start * sr)
        e = min(n, s0 + len(a))
        if s0 < n:
            tr[s0:e] += a[: e - s0]
        if s0 + len(a) > n:
            print(f"WARNUNG: Sprechtext läuft über das Videoende: {text!r}")
    return tr

def audio(total, path, seed=0, typing=(), voice=()):
    """Selbst erzeugtes Musikbett (Pad + weicher Puls) + optionale Tipp-Klicks + optionale Stimme.
    seed variiert Tonart/Akkordfolge; typing = [(start_s, anzahl, abstand_s), ...];
    voice = [(start_s, "Sprechtext"), ...] – Musik wird unter der Stimme automatisch leiser."""
    sr = 44100
    n = int(total * sr); t = np.arange(n) / sr; out = np.zeros(n)
    rng = np.random.default_rng(seed + 1)
    progs = [[[57, 60, 64], [53, 57, 60], [48, 52, 55], [55, 59, 62]],
             [[50, 53, 57], [46, 50, 53], [53, 57, 60], [48, 52, 55]],
             [[52, 55, 59], [48, 52, 55], [43, 47, 50], [50, 54, 57]],
             [[45, 48, 52], [41, 45, 48], [48, 52, 55], [43, 47, 50]]]
    chords = progs[seed % len(progs)]
    bpm = [100, 96, 104, 92][seed % 4]; beat = 60 / bpm; bar = beat * 4
    for ci in range(int(total / bar) + 1):
        notes = chords[ci % 4]
        s0 = int(ci * bar * sr); s1 = min(n, int((ci + 1) * bar * sr) + int(0.3 * sr))
        if s0 >= n: break
        tt = np.arange(s1 - s0) / sr
        env = np.minimum(1, tt / 0.6) * np.exp(-tt * 0.25) * np.clip((bar + 0.3 - tt) / 0.3, 0, 1)
        for m in notes:
            fq = 440 * 2 ** ((m - 69) / 12)
            out[s0:s1] += 0.06 * env * (np.sin(2 * np.pi * fq * tt) + 0.3 * np.sin(2 * np.pi * fq * 2.003 * tt))
        out[s0:s1] += 0.07 * env * np.sin(2 * np.pi * 440 * 2 ** ((notes[0] - 81) / 12) * tt)
    for k in range(int(total / beat) + 1):
        st = k * beat
        if st < 2.0 or st > total - 0.5: continue
        s0 = int(st * sr); L = int(0.25 * sr)
        if s0 + L > n: break
        tt = np.arange(L) / sr
        fq = 55 * np.exp(-tt * 18) + 45
        out[s0:s0 + L] += 0.22 * np.sin(2 * np.pi * np.cumsum(fq) / sr) * np.exp(-tt * 14)
        h0 = int((st + beat / 2) * sr); HL = int(0.05 * sr)
        if h0 + HL < n:
            out[h0:h0 + HL] += 0.025 * rng.standard_normal(HL) * np.exp(-np.arange(HL) / sr * 90)
    for start, cnt, step in typing:
        for i in range(cnt):
            s0 = int((start + i * step) * sr); L = int(0.03 * sr)
            if s0 + L < n:
                out[s0:s0 + L] += 0.12 * rng.standard_normal(L) * np.exp(-np.arange(L) / sr * 220)
    out *= np.clip((total - t) / 1.2, 0, 1)
    out = np.tanh(out * 1.4); out /= np.max(np.abs(out)) / 0.6
    if voice:
        vt = _voice_track(n, voice)
        # Ducking: Hüllkurve der Stimme (geglättet) senkt die Musik auf ~30 %
        env = np.abs(vt)
        k = int(0.25 * sr)
        env = np.convolve(env, np.ones(k) / k, mode="same")
        env = np.clip(env / (env.max() * 0.25 + 1e-9), 0, 1)
        out = out * (1 - 0.7 * env) * 0.85
        vt = vt / (np.max(np.abs(vt)) + 1e-9) * 0.9
        out = out + vt
        out /= max(1.0, np.max(np.abs(out)) / 0.95)
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.stack([out, out], 1) * 32767).astype(np.int16).tobytes())

def build(scenes, name, outdir="/home/claude/bitweise-out", seed=0, typing=(), voice=()):
    """Rendert alle Szenen, Audio (+ Stimme), fügt zusammen. Ergebnis: {outdir}/{name}.mp4"""
    os.makedirs(outdir, exist_ok=True)
    total = sum(d for _, _, d in scenes)
    if voice:
        check_voice(voice, total)  # vor dem Rendern, spart Zeit
    for i, (sn, fn, dur) in enumerate(scenes):
        render_scene(outdir, f"{name}_{sn}", fn, dur, 0 if i == 0 else 0.2, 0 if i == len(scenes) - 1 else 0.2)
    audio(total, f"{outdir}/{name}.wav", seed, typing, voice)
    lst = f"{outdir}/{name}_list.txt"
    with open(lst, "w") as fh:
        for sn, _, _ in scenes:
            fh.write(f"file '{name}_{sn}.mp4'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", f"{outdir}/{name}_v.mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{outdir}/{name}_v.mp4", "-i", f"{outdir}/{name}.wav",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                    f"{outdir}/{name}.mp4"], check=True)
    return f"{outdir}/{name}.mp4"

def carousel_slide(draw_fn, path):
    """Karussell-Folie 1080x1350 (Instagram 4:5). draw_fn(img, d) zeichnet den Inhalt."""
    img = Image.new("RGB", (1080, 1350), BG)
    d = ImageDraw.Draw(img)
    draw_fn(img, d)
    img.save(path)
    return path
