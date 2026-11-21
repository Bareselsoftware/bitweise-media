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

def punch(img, t, t0=0.0, dur=0.45, amount=0.14):
    """Zoom-Punch: Bild startet um `amount` vergrößert und federt bis t0+dur auf 100 % zurück (Bewegung in Sek. 0–1)."""
    k = 1 - ease((t - t0) / dur)
    if k <= 0.001 or t < t0:
        return img
    z = 1 + amount * k
    w, h = int(W / z), int(H / z)
    x, y = (W - w) // 2, (H - h) // 2
    return img.crop((x, y, x + w, y + h)).resize((W, H), Image.BILINEAR)

def scene_fade(img, t, dur, fin=0.2, fout=0.2):
    a = min(1.0, t / fin) if fin else 1.0
    b = min(1.0, (dur - t) / fout) if fout else 1.0
    k = max(0.0, min(a, b))
    return img if k >= 1 else Image.blend(Image.new("RGB", (W, H), BG), img, k)

# ---------------- Render ----------------
def render_scene(outdir, name, fn, dur, fin, fout, overlay=None, offset=0.0):
    """overlay(img, t_abs) wird NACH der Szenenblende gezeichnet (Untertitel bleiben voll sichtbar)."""
    tmp = f"{outdir}/{name}.tmp.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                          "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                          "-crf", "18", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for i in range(int(round(dur * FPS))):
        t = i / FPS
        img = scene_fade(fn(t), t, dur, fin, fout)
        if overlay:
            img = overlay(img, offset + t)
        p.stdin.write(img.tobytes())
    p.stdin.close()
    if p.wait() != 0:
        raise SystemExit(f"Render {name} fehlgeschlagen")
    os.replace(tmp, f"{outdir}/{name}.mp4")

def stills(scenes, outdir, at=0.9, voice=()):
    """Zeichnet je Szene ein Standbild bei Anteil `at` der Dauer + Kontaktbogen zum Prüfen.
    Mit voice=VOICE werden die Untertitel mitgezeichnet (zeigt Kollisionen mit Grafiken)."""
    os.makedirs(outdir, exist_ok=True)
    ims = []
    words = word_timings(voice) if voice else None
    off = 0.0
    for name, fn, dur in scenes:
        im = fn(dur * at)
        if words:
            im = subtitles(im, off + dur * at, words)
        off += dur
        im.save(f"{outdir}/still_{name}.png"); ims.append(im.resize((360, 640)))
    c = Image.new("RGB", (370 * len(ims), 640), (60, 60, 60))
    for i, im in enumerate(ims):
        c.paste(im, (i * 370, 0))
    c.save(f"{outdir}/kontaktbogen.png")
    return f"{outdir}/kontaktbogen.png"

# ---------------- Stock-Material (Pixabay) ----------------
# Regeln: nur echte Fotos/Filme (image_type=photo, video_type=film), nur Uploads bis einschließlich 2021
# (vor der Welle generativer KI-Bilder; Jahr steht im CDN-Pfad), keine Treffer mit KI-/CG-Tags.
# Jede Auswahl VOR der Verwendung als Vorschaubild ansehen (stock_preview). Quellen in werkstatt/quellen.md.
# Key: Umgebungsvariable PIXABAY_KEY (oder Datei /home/claude/.bitweise/env) – niemals ins Repo schreiben.
STOCK_DIR = "/home/claude/bitweise-stock"
STOCK_MAX_YEAR = 2021
_BAD_TAGS = ("ai generated", "ai-generated", "generated", "midjourney", "stable diffusion", "dall-e", "dalle",
             "ai art", "artificial intelligence art", "cg", "3d", "blender", "render", "rendering", "cgi", "animation")
STOCK_USED = []

def _pixabay_key():
    k = os.environ.get("PIXABAY_KEY")
    if not k and os.path.exists("/home/claude/.bitweise/env"):
        for ln in open("/home/claude/.bitweise/env"):
            if ln.startswith("PIXABAY_KEY="):
                k = ln.split("=", 1)[1].strip()
    if not k:
        raise SystemExit("PIXABAY_KEY fehlt (steht im Prompt der geplanten Aufgabe)")
    return k

def _year(url):
    import re
    m = re.search(r"/(?:photo|video)/(\d{4})/", url or "")
    return int(m.group(1)) if m else 9999

def stock_search(q, kind="video", n=12, lang="de"):
    """Sucht bei Pixabay und filtert: echte Aufnahmen, Upload ≤ 2021, keine KI/CG-Tags.
    kind = 'video' | 'photo'. Liefert Liste von dicts (id, url, w, h, dur, tags, page, user, year)."""
    import json, urllib.parse, urllib.request
    os.makedirs(STOCK_DIR + "/cache", exist_ok=True)
    base = "https://pixabay.com/api/videos/" if kind == "video" else "https://pixabay.com/api/"
    params = {"key": _pixabay_key(), "q": q, "lang": lang, "per_page": 100, "safesearch": "true"}
    params.update({"video_type": "film"} if kind == "video" else {"image_type": "photo"})
    cf = f"{STOCK_DIR}/cache/{kind}_{abs(hash((q, lang)))}.json"
    import time
    if os.path.exists(cf) and time.time() - os.path.getmtime(cf) < 86400:  # Pixabay verlangt 24-h-Cache
        data = json.load(open(cf))
    else:
        r = subprocess.run(["curl", "-sSf", "--max-time", "30", base + "?" + urllib.parse.urlencode(params)],
                           capture_output=True, text=True, check=True)
        data = json.loads(r.stdout)
        json.dump(data, open(cf, "w"))
    out = []
    for h in data.get("hits", []):
        tags = h.get("tags", "").lower()
        if any(b in [t.strip() for t in tags.split(",")] or (" " in b and b in tags) for b in _BAD_TAGS):
            continue
        if kind == "video":
            v = h["videos"]["large"] if h["videos"]["large"]["url"] else h["videos"]["medium"]
            yr = _year(v["url"])
            item = dict(id=h["id"], url=v["url"], w=v["width"], h=v["height"], dur=h["duration"],
                        thumb=v.get("thumbnail"), tags=tags, page=h["pageURL"], user=h["user"], year=yr, kind="video")
        else:
            yr = _year(h.get("previewURL"))
            item = dict(id=h["id"], url=h["largeImageURL"], w=h["imageWidth"], h=h["imageHeight"], dur=0,
                        thumb=h.get("webformatURL"), tags=tags, page=h["pageURL"], user=h["user"], year=yr, kind="photo")
        if yr <= STOCK_MAX_YEAR:
            out.append(item)
    return out[:n]

def stock_get(item):
    """Lädt ein Suchergebnis herunter (einmalig) und merkt es für die Quellenliste vor. Liefert Dateipfad."""
    ext = ".mp4" if item["kind"] == "video" else ".jpg"
    p = f"{STOCK_DIR}/{item['kind']}_{item['id']}{ext}"
    if not os.path.exists(p):
        subprocess.run(["curl", "-sSfL", "-o", p + ".part", item["url"]], check=True)
        os.replace(p + ".part", p)
    if not any(u["id"] == item["id"] for u in STOCK_USED):
        STOCK_USED.append(item)
    return p

def stock_preview(items, path):
    """Kontaktbogen der Vorschaubilder (zum Ansehen mit Read), nummeriert."""
    import urllib.request, io
    tiles = []
    for it in items:
        try:
            raw = subprocess.run(["curl", "-sSfL", "--max-time", "20", it["thumb"]], capture_output=True, check=True).stdout
            im = Image.open(io.BytesIO(raw)).convert("RGB")
        except Exception:
            im = Image.new("RGB", (320, 180), (60, 0, 0))
        im.thumbnail((320, 320)); tiles.append(im)
    c = Image.new("RGB", (330 * min(4, len(tiles)), 350 * ((len(tiles) + 3) // 4)), (40, 40, 40))
    d = ImageDraw.Draw(c)
    for i, im in enumerate(tiles):
        x, y = (i % 4) * 330, (i // 4) * 350
        c.paste(im, (x, y)); d.text((x + 6, y + 4), f"{i} #{items[i]['id']} {items[i]['year']}", fill=(255, 255, 0))
    c.save(path)
    return path

class Clip:
    """Stock-Video als Bildquelle für render: Clip(pfad, start=2).frame(t) → PIL-Bild W×H (Cover-Zuschnitt).
    Frames werden sequentiell aus ffmpeg gelesen (wenig Speicher); Rückwärtssprung startet neu."""
    def __init__(self, path, start=0.0, size=(W, H), zoom=1.0, speed=1.0):
        self.path, self.start, self.size, self.zoom, self.speed = path, start, size, zoom, speed
        self.p, self.pos, self.last = None, -1, None
    def _open(self):
        if self.p:
            self.p.kill()
        w, h = self.size
        zw, zh = int(w * self.zoom) // 2 * 2, int(h * self.zoom) // 2 * 2
        vf = (f"setpts=PTS/{self.speed},fps={FPS},scale={zw}:{zh}:force_original_aspect_ratio=increase,"
              f"crop={w}:{h}")
        self.p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-stream_loop", "-1", "-ss", str(self.start),
                                   "-i", self.path, "-vf", vf, "-an", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.pos = -1
    def frame(self, t):
        idx = max(0, int(round(t * FPS)))
        if self.p is None or idx < self.pos:
            self._open()
        w, h = self.size
        while self.pos < idx:
            buf = self.p.stdout.read(w * h * 3)
            if len(buf) < w * h * 3:
                break
            self.last = buf; self.pos += 1
        return Image.frombytes("RGB", (w, h), self.last).copy()

def stock_bg(clip_or_img, t, dim=0.6, kenburns=0.04):
    """Hintergrund aus Stock (Clip oder Foto-Pfad), abgedunkelt für lesbare Grafiken/Untertitel."""
    if isinstance(clip_or_img, Clip):
        im = clip_or_img.frame(t)
    else:
        src = Image.open(clip_or_img).convert("RGB")
        z = 1 + kenburns * t / 5
        sw, sh = src.size; s = max(W / sw, H / sh) * z
        src = src.resize((int(sw * s), int(sh * s)), Image.LANCZOS)
        x, y = (src.width - W) // 2, (src.height - H) // 2
        im = src.crop((x, y, x + W, y + H))
    return Image.blend(im, Image.new("RGB", (W, H), BG), dim)

def write_credits(name, path=None):
    """Hängt die verwendeten Stock-Quellen an werkstatt/quellen.md an (Pixabay-Lizenz, keine Pflicht, aber transparent)."""
    path = path or os.path.join(os.path.dirname(__file__), "quellen.md")
    if not STOCK_USED:
        return
    new = not os.path.exists(path)
    if not new and f"## {name}\n" in open(path).read():
        return  # schon eingetragen (erneutes Rendern)
    with open(path, "a") as f:
        if new:
            f.write("# Stock-Quellen\n\nAlle Fotos/Videos von Pixabay (Pixabay Content License), echte Aufnahmen, Upload ≤ 2021.\n\n")
        f.write(f"## {name}\n")
        for u in STOCK_USED:
            f.write(f"- {u['kind']} #{u['id']} ({u['year']}) von {u['user']}: {u['page']}\n")

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

# Aussprache-Wörterbuch: Schreibweise im Untertitel → Lautschrift für die Stimme.
# Ersetzt Wortanfänge (auch in Komposita/Flexion: „Sneaker-Werbung“, „Sneakern“). Wortanzahl bleibt gleich.
# Neue Einträge, sobald Tilman oder die QA eine falsche Aussprache meldet. Prüfen mit: _ensure_voice().phonemize(...)
AUSSPRACHE = {
    "Sneaker": "Snieker",   # Tilman 16.11.: nicht „Sne-a-ker“
}
# Nur ganze Wörter (Groß-/Kleinschreibung beachtet), z. B. Abkürzungen, die sonst buchstabiert werden.
AUSSPRACHE_WORT = {
    "TAN": "Tahn",          # 19.11.: sonst „T-A-N“ buchstabiert
    "Bot": "Bott",          # 21.11. Tilman: sonst „Boot“ (langes o)
    "Bots": "Botts",
}

def spoken(text):
    """Text so umschreiben, wie die Stimme ihn sprechen soll (Groß/klein bleibt erhalten)."""
    import re
    for src, dst in AUSSPRACHE.items():
        def _r(m, dst=dst):
            w = m.group(0)
            return dst.upper() if w.isupper() else (dst.lower() if w.islower() else dst)
        text = re.sub(r"\b" + re.escape(src), _r, text, flags=re.IGNORECASE)
    for src, dst in AUSSPRACHE_WORT.items():
        text = re.sub(r"\b" + re.escape(src) + r"\b", dst, text)
    return text

def say(text, tempo=0.95):
    """Spricht `text` (Deutsch). Liefert (samples float32 @44,1 kHz, dauer_s). Zahlen ausschreiben!
    Dauer vorab abfragen, um Szenenlängen passend zu wählen: say("...")[1]"""
    key = (text, tempo)
    if key in _say_cache:
        return _say_cache[key]
    v = _ensure_voice()
    from piper import SynthesisConfig
    chunks = [c.audio_int16_array for c in v.synthesize(spoken(text), syn_config=SynthesisConfig(length_scale=tempo))]
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

# ---------------- Wortzeiten (Whisper) & Untertitel ----------------
_whisper = None
_wt_cache = {}
SUB_Y = 1400            # Mitte der Untertitelzeile; Grafiken frei lassen: y 1310–1500
SUB_HL = (255, 214, 10) # Highlight-Farbe aktives Wort (Gelb, knallt auf Dunkel)

def _get_whisper():
    global _whisper
    if _whisper is None:
        try:
            from faster_whisper import WhisperModel
        except ImportError:
            subprocess.run(["pip", "install", "--break-system-packages", "-q", "faster-whisper"], check=True)
            from faster_whisper import WhisperModel
        _whisper = WhisperModel("small", device="cpu", compute_type="int8")
    return _whisper

def _norm(w):
    import re
    return re.sub(r"[^a-zäöüß0-9]", "", w.lower())

def _to16k(a, sr=44100):
    n = int(len(a) * 16000 / sr)
    return np.interp(np.linspace(0, len(a) - 1, n), np.arange(len(a)), a).astype(np.float32)

def _transcribe(a16, prompt=None):
    segs, _ = _get_whisper().transcribe(a16, language="de", word_timestamps=True, beam_size=5,
                                        initial_prompt=prompt, condition_on_previous_text=False)
    return [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]

def _align(ref_words, hyp, t0, t1):
    """Ordnet Skript-Wörter erkannten Wörtern zu; Lücken nach Zeichenlänge interpolieren."""
    from difflib import SequenceMatcher
    rn = [_norm(w) for w in ref_words]; hn = [_norm(h[0]) for h in hyp]
    times = [None] * len(ref_words)
    for blk in SequenceMatcher(None, rn, hn, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = (hyp[blk.b + k][1], hyp[blk.b + k][2])
    matched = sum(t is not None for t in times)
    i = 0
    while i < len(times):
        if times[i] is not None:
            i += 1; continue
        j = i
        while j < len(times) and times[j] is None:
            j += 1
        a = times[i - 1][1] if i > 0 else t0
        b = times[j][0] if j < len(times) else t1
        lens = [max(1, len(ref_words[k])) for k in range(i, j)]
        tot = sum(lens); cur = a
        for k, L in zip(range(i, j), lens):
            d = (b - a) * L / tot
            times[k] = (cur, cur + d); cur += d
        i = j
    return times, matched / max(1, len(ref_words))

def word_timings(voice):
    """[(wort, start_abs, ende_abs), ...] aus der tatsächlich erzeugten Stimme (je Satz per Whisper)."""
    out = []
    for start, text in sorted(voice):
        a, dur = say(text)
        key = (text, dur)
        if key not in _wt_cache:
            hyp = _transcribe(_to16k(a), prompt=spoken(text))
            times, q = _align(spoken(text).split(), hyp, 0.0, dur)  # Zeiten der gesprochenen Form, Anzeige = Original
            _wt_cache[key] = (times, q, " ".join(h[0] for h in hyp))
        times, q, heard = _wt_cache[key]
        out += [(w, start + s, start + e) for w, (s, e) in zip(text.split(), times)]
    return out

def timeline(lines, start=0.05, gap=0.3):
    """Legt Sprechsätze lückenlos hintereinander: [(start, text), ...]. gap kann je Satz als
    (text, pause_davor) überschrieben werden. Robust, weil die Dauern im selben Lauf gemessen werden."""
    out, t = [], start
    for i, ln in enumerate(lines):
        text, pause = (ln, gap) if isinstance(ln, str) else ln
        if i:
            t += pause
        out.append((round(t, 3), text))
        t += say(text)[1]
    return out

def at(words, word, nth=0):
    """Startzeit (absolut) des nth-ten Vorkommens von `word` – um Grafik-Ereignisse aufs Wort zu legen."""
    k = 0
    for w, s, e in words:
        if _norm(w) == _norm(word):
            if k == nth:
                return s
            k += 1
    raise KeyError(word)

def _chunks(words, max_words=3, max_chars=17):
    ch, cur = [], []
    for w in words:
        if cur and (len(cur) >= max_words or len(" ".join(x[0] for x in cur + [w])) > max_chars):
            ch.append(cur); cur = []
        cur.append(w)
        if w[0][-1:] in ".?!:":
            ch.append(cur); cur = []
    if cur:
        ch.append(cur)
    return ch

def subtitles(img, t, words, y=SUB_Y):
    """Zeichnet die Untertitel für Zeitpunkt t: 1–3 Wörter, GROSS, weiß mit dicker Kontur,
    aktives Wort gelb hinterlegt mit kurzem Pop. Satzzeichen am Wortende werden weggelassen."""
    chunks = _chunks(words)
    cur = None
    for i, c in enumerate(chunks):
        nxt = chunks[i + 1][0][1] if i + 1 < len(chunks) else None
        end = nxt if (nxt is not None and nxt - c[-1][2] < 0.6) else c[-1][2] + 0.25
        if c[0][1] - 0.03 <= t < end:
            cur = c; break
    if not cur:
        return img
    d = ImageDraw.Draw(img)
    base = 86
    pop_in = ease((t - cur[0][1] + 0.03) / 0.09)
    f = font(BLACK, int(base * (0.86 + 0.14 * pop_in)))
    toks = [w[0].strip(",.;:!?„“\"").upper() for w in cur]
    sp = d.textlength(" ", font=f) * 1.9
    widths = [d.textlength(tk, font=f) for tk in toks]
    total = sum(widths) + sp * (len(toks) - 1)
    if total > W - 120:  # notfalls kleiner
        f = font(BLACK, int(f.size * (W - 120) / total)); widths = [d.textlength(tk, font=f) for tk in toks]
        sp = d.textlength(" ", font=f) * 1.9; total = sum(widths) + sp * (len(toks) - 1)
    x = (W - total) / 2
    for j, (tk, wd, w) in enumerate(zip(toks, widths, cur)):
        nxt_s = cur[j + 1][1] - 0.02 if j + 1 < len(cur) else 1e9
        active = w[1] - 0.02 <= t < min(w[2] + 0.05, nxt_s)  # immer genau ein Wort aktiv
        if active:
            k = ease((t - w[1]) / 0.08)
            pad = 14 + 6 * (1 - k)
            d.rounded_rectangle([x - pad, y - f.size * 0.62 - pad * 0.5, x + wd + pad, y + f.size * 0.5 + pad * 0.5],
                                radius=18, fill=SUB_HL)
            d.text((x, y), tk, font=f, fill=BG, anchor="lm")
        else:
            d.text((x, y), tk, font=f, fill=WH, anchor="lm", stroke_width=7, stroke_fill=(0, 0, 0))
        x += wd + sp
    return img

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

def audio(total, path, seed=0, typing=(), voice=(), sfx=()):
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
    for st, kind in sfx:  # Ton-Akzente: "whoosh" (Rauschen, steigend) | "hit" (tiefer Schlag)
        s0 = int(st * sr)
        if kind == "whoosh":
            L = int(0.38 * sr); tt = np.arange(L) / sr
            nz = rng.standard_normal(L)
            env = np.sin(np.pi * np.minimum(1, tt / 0.38)) ** 2
            # einfacher steigender Bandpass: gleitender Mittelwert mit schrumpfendem Fenster
            sw = np.zeros(L); acc = 0.0
            for i in range(L):
                a_ = 0.02 + 0.5 * i / L
                acc += a_ * (nz[i] - acc); sw[i] = acc
            seg = 0.5 * sw * env
        else:  # hit
            L = int(0.3 * sr); tt = np.arange(L) / sr
            fq = 90 * np.exp(-tt * 12) + 40
            seg = 0.6 * np.sin(2 * np.pi * np.cumsum(fq) / sr) * np.exp(-tt * 10)
        e = min(n, s0 + L)
        if s0 < n:
            out[s0:e] += seg[: e - s0]
    out *= np.clip((total - t) / 1.2, 0, 1)
    out = np.tanh(out * 1.4); out /= np.max(np.abs(out)) / 0.6
    if voice:
        vt = _voice_track(n, voice)
        with wave.open(path.replace(".wav", "_stimme.wav"), "wb") as w:  # für die QA-Prüfung
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
            w.writeframes((np.clip(vt, -1, 1) * 32767).astype(np.int16).tobytes())
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

def _read_wav(path):
    with wave.open(path) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        ch, sr = w.getnchannels(), w.getframerate()
    return (a.reshape(-1, ch).mean(1) if ch > 1 else a), sr

def _runs(mask, sr, min_s):
    """Zusammenhängende True-Abschnitte (start_s, ende_s) mit Länge >= min_s."""
    out, i, n = [], 0, len(mask)
    edges = np.flatnonzero(np.diff(np.concatenate([[0], mask.astype(np.int8), [0]])))
    for a, b in zip(edges[::2], edges[1::2]):
        if (b - a) / sr >= min_s:
            out.append((a / sr, b / sr))
    return out

def qa(mp4, voice, words, voice_wav, pausen_ok=(), max_gap=1.6):
    """Prüft das FERTIGE Video. Liefert (ok, bericht). Prüft:
    1) Stimmen-Überlappung, 2) Aussetzer (Stille mitten im Satz > 0,45 s, Lücke zwischen Sätzen > max_gap,
    digitale Stille im Mix), 3) Untertitel-Sync gegen eine unabhängige Whisper-Erkennung des fertigen Tons,
    4) Ton/Bild-Länge, 5) Übersteuerung. pausen_ok=[(von, bis)] erlaubt gewollte Pausen (z. B. Rate-Countdown)."""
    errs, warns, info = [], [], []
    v = sorted(voice)
    # 1) Überlappung (aus dem Zeitplan)
    for i in range(len(v) - 1):
        e = v[i][0] + say(v[i][1])[1]
        if e > v[i + 1][0] - 0.05:
            errs.append(f"Überlappung: {v[i][1]!r} endet {e:.2f}s, nächster Satz startet {v[i+1][0]:.2f}s")
    # 2) Aussetzer
    vt, sr = _read_wav(voice_wav)
    k = int(0.03 * sr)
    env = np.sqrt(np.convolve(vt ** 2, np.ones(k) / k, mode="same"))
    silent = env < 0.006
    for i, (st, tx) in enumerate(v):
        en = st + say(tx)[1]
        for a, b in _runs(silent[int(st * sr):int(en * sr)], sr, 0.45):
            a += st; b += st
            if not any(p0 <= a and b <= p1 for p0, p1 in pausen_ok):
                errs.append(f"Aussetzer im Satz {tx[:40]!r}: Stille {a:.2f}–{b:.2f}s")
        if i + 1 < len(v):
            gap = v[i + 1][0] - en
            if gap > max_gap and not any(p0 <= en and v[i + 1][0] <= p1 for p0, p1 in pausen_ok):
                errs.append(f"Lange Sprechpause {en:.2f}–{v[i+1][0]:.2f}s ({gap:.1f}s) – füllen oder in pausen_ok erlauben")
    mix_wav = mp4.replace(".mp4", "_qa.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", mp4, "-ac", "1", "-ar", "16000", mix_wav], check=True)
    mx, msr = _read_wav(mix_wav)
    km = int(0.03 * msr)
    menv = np.sqrt(np.convolve(mx ** 2, np.ones(km) / km, mode="same"))
    for a, b in _runs(menv < 0.0008, msr, 0.3):
        if b < len(mx) / msr - 0.6:
            errs.append(f"Tonloch im fertigen Video: {a:.2f}–{b:.2f}s")
    peak = float(np.max(np.abs(mx)))
    if peak > 0.995:
        warns.append(f"Pegelspitze {peak:.3f} – evtl. Übersteuerung")
    # 3) Untertitel-Sync: fertigen Ton unabhängig erkennen, mit Untertitel-Zeiten vergleichen
    hyp = _transcribe(mx)
    ref = [spoken(w[0]) for w in words]
    times, q = _align(ref, hyp, 0, len(mx) / msr)
    from difflib import SequenceMatcher
    rn = [_norm(w) for w in ref]; hn = [_norm(h[0]) for h in hyp]
    devs = []
    for blk in SequenceMatcher(None, rn, hn, autojunk=False).get_matching_blocks():
        for j in range(blk.size):
            devs.append(abs(words[blk.a + j][1] - hyp[blk.b + j][1]))
    if devs:
        med, p90 = float(np.median(devs)), float(np.percentile(devs, 90))
        info.append(f"Untertitel-Sync: {len(devs)}/{len(ref)} Wörter geprüft, Abweichung Median {med*1000:.0f} ms, 90 % ≤ {p90*1000:.0f} ms")
        if med > 0.12 or p90 > 0.3:
            errs.append(f"Untertitel nicht synchron (Median {med*1000:.0f} ms, 90 % {p90*1000:.0f} ms)")
    if q < 0.75:
        warns.append(f"Nur {q*100:.0f} % der Wörter im fertigen Ton wiedererkannt – Aussprache/Lautstärke prüfen. Gehört: {' '.join(h[0] for h in hyp)!r}")
    # Aussprache je Satz (Warnung)
    for st, tx in v:
        heard = _wt_cache.get((tx, say(tx)[1]), (None, 1.0, ""))
        if heard[1] < 0.7:
            warns.append(f"Satz evtl. undeutlich: {tx!r} → gehört {heard[2]!r}")
    # 4) Längen
    def dur(stream):
        r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", stream, "-show_entries", "stream=duration",
                            "-of", "csv=p=0", mp4], capture_output=True, text=True).stdout.strip()
        return float(r or 0)
    dv, da = dur("v:0"), dur("a:0")
    info.append(f"Länge Bild {dv:.2f}s / Ton {da:.2f}s")
    if abs(dv - da) > 0.15:
        errs.append(f"Ton/Bild-Länge weicht ab: {dv:.2f}s vs {da:.2f}s")
    os.remove(mix_wav)
    rep = "\n".join(["QA " + ("OK" if not errs else "FEHLER")] + [f"✗ {e}" for e in errs] +
                    [f"! {w_}" for w_ in warns] + [f"· {i_}" for i_ in info])
    return not errs, rep

def build(scenes, name, outdir="/home/claude/bitweise-out", seed=0, typing=(), voice=(), subs=True,
          pausen_ok=(), max_gap=1.6, sfx=()):
    """Rendert alle Szenen mit Untertiteln, Audio (+ Stimme), fügt zusammen und prüft das Ergebnis (qa).
    Ergebnis: {outdir}/{name}.mp4. Bricht bei QA-Fehlern ab (Bericht in {name}_qa.txt)."""
    os.makedirs(outdir, exist_ok=True)
    total = sum(d for _, _, d in scenes)
    words = None
    if voice:
        check_voice(voice, total)  # vor dem Rendern, spart Zeit
        words = word_timings(voice)
    overlay = (lambda img, t: subtitles(img, t, words)) if (voice and subs) else None
    off = 0.0
    for i, (sn, fn, dur) in enumerate(scenes):
        render_scene(outdir, f"{name}_{sn}", fn, dur, 0 if i == 0 else 0.2, 0 if i == len(scenes) - 1 else 0.2,
                     overlay=overlay, offset=off)
        off += dur
    audio(total, f"{outdir}/{name}.wav", seed, typing, voice, sfx)
    lst = f"{outdir}/{name}_list.txt"
    with open(lst, "w") as fh:
        for sn, _, _ in scenes:
            fh.write(f"file '{name}_{sn}.mp4'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", f"{outdir}/{name}_v.mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f"{outdir}/{name}_v.mp4", "-i", f"{outdir}/{name}.wav",
                    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
                    f"{outdir}/{name}.mp4"], check=True)
    if voice:
        ok, rep = qa(f"{outdir}/{name}.mp4", voice, words, f"{outdir}/{name}_stimme.wav", pausen_ok, max_gap)
        open(f"{outdir}/{name}_qa.txt", "w").write(rep)
        print(rep)
        if not ok:
            raise SystemExit("QA fehlgeschlagen – Video NICHT verwenden. Bericht: " + f"{outdir}/{name}_qa.txt")
    return f"{outdir}/{name}.mp4"

def carousel_slide(draw_fn, path):
    """Karussell-Folie 1080x1350 (Instagram 4:5). draw_fn(img, d) zeichnet den Inhalt."""
    img = Image.new("RGB", (1080, 1350), BG)
    d = ImageDraw.Draw(img)
    draw_fn(img, d)
    img.save(path)
    return path
