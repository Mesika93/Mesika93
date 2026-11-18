"""Composite 2D characters over Blender plates. usage: python3 composite3d.py PLATES OUT [preview]"""
import sys, os, json, math, random, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from common3d import *
from chars2d import person, BLACK, WHITE, RED, GOLD, FONT, FONT_S, FONT_XS, lerp, lerpc

BANK = 5.4
PL = sys.argv[1]; OUT = sys.argv[2]; PREVIEW = len(sys.argv) > 3
W, H, FPS = 720, 1280, 30
CAMS = json.load(open(os.path.join(PL, "cams.json")))
_cache = {}
def still(name, blur=0):
    k = (name, blur)
    if k not in _cache:
        im = Image.open(os.path.join(PL, name, "still.png")).convert("RGB")
        if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
        _cache[k] = im
    return _cache[k].copy()
def plate(name, now):
    fi = int(round(now * FPS)); d = os.path.join(PL, name)
    for k in range(0, 40):
        for f in (fi - k, fi + k):
            p = os.path.join(d, f"f{f:05d}.png")
            if os.path.exists(p): return Image.open(p).convert("RGB")
    raise FileNotFoundError(name)

_fgc = {}
def fg(img, name, now=None):
    if now is None: path = os.path.join(PL, name, "fg.png")
    else:
        fi = int(round(now * FPS)); path = None
        for k in range(0, 40):
            for f in (fi - k, fi + k):
                q = os.path.join(PL, name, f"fg{f:05d}.png")
                if os.path.exists(q): path = q; break
            if path: break
    if not path or not os.path.exists(path): return img
    if path not in _fgc or now is not None:
        _fgc[path] = Image.open(path).convert("RGBA")
    img.paste(_fgc[path], (0, 0), _fgc[path]); return img

def proj(cam, p):
    c = CAMS[cam]; mi = np.array(c["mi"]); rw, rh = c["res"]
    v = mi @ np.array([p[0], p[1], p[2], 1.0])
    s = c["lens"] / c["sensor_h"] * rh
    return rw / 2 + s * v[0] / -v[2], rh / 2 - s * v[1] / -v[2]

def put(d, cam, x, y, z, **kw):
    fx, fy = proj(cam, (x, y, z)); tx, ty = proj(cam, (x, y, z + 1.75))
    R = max(3, (fy - ty) / 3.97)
    person(d, fx, fy, R, **kw)
    return fx, fy, R

def cam2d(img, z=1.0, cx=0.5, cy=0.5, shake=0.0, t=0.0):
    w, h = img.size
    cxp, cyp = cx * w + math.sin(t * 53) * shake * w / W, cy * h + math.cos(t * 41) * shake * h / W
    cw, ch = w / z, h / z
    x0 = clamp(cxp - cw / 2, 0, w - cw); y0 = clamp(cyp - ch / 2, 0, h - ch)
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)

def march(d, cam, now, xs, y=0.0, step=6.0, lead=None, chaos=False, scared=False, zfun=None, hop=0.0):
    zf = zfun or (lambda x: DECK_Z + 0.12)
    for k, x in enumerate(xs):
        r = random.Random(k)
        if chaos:
            put(d, cam, x + 0.2 * math.sin(now * 3 + k), y + 0.4 * math.sin(now * 2 + k * 1.7), zf(x),
                walk=now * step * (0.6 + r.random()) + k, hop=abs(math.sin(now * 7 + k)) * 8,
                arm_l=r.choice([-30, 20, 60]), arm_r=r.choice([-150, 160, 120]), brows="worried",
                mouth="open" if k % 2 else "flat", musket=True)
        else:
            put(d, cam, x, y, zf(x), walk=now * step, brows="worried" if scared else "calm",
                mouth="open" if scared else "flat", musket=True, hop=hop * max(0, math.sin(now * 10 + k)))
    if lead:
        x = xs[-1] + 1.4
        fx, fy = proj(cam, (x, y, zf(x))); tx, ty = proj(cam, (x, y, zf(x) + 1.95))
        person(d, fx, fy, (fy - ty) / 3.97, outfit="general", walk=now * step, brows=lead,
               mouth="smile" if lead == "calm" else "open", arm_r=-100, arm_l=-80)

# ---------------- scenes ----------------
def s_order(now, t, d0):
    img = still("order"); d = ImageDraw.Draw(img)
    for k in range(6): put(d, "order", -5.5 + k * 1.25, 0.6, DECK_Z + 0.12, musket=True)
    put(d, "order", 3.6, -0.5, DECK_Z + 0.12, arm_r=60 + 20 * ease(t / 0.5), mouth="open" if t < 1.6 else "flat", flip=True)
    fg(img, "order")
    return cam2d(img, lerp(1.0, 1.15, t / d0), 0.5, 0.55)

def s_wide(now, t, d0):
    img = still("wide"); d = ImageDraw.Draw(img)
    for k in range(6): put(d, "wide", -6 + k * 1.25, 0.0, DECK_Z + 0.12, musket=True)
    put(d, "wide", 2.5, 0, DECK_Z + 0.12, arm_r=80, flip=True)
    fg(img, "wide")
    return cam2d(img, lerp(1.35, 1.0, ease(t / d0)), 0.5, 0.5)

def s_parade(now, t, d0):
    img = still("parade"); d = ImageDraw.Draw(img)
    for k, o in enumerate(["civ1", "civ3", "civ2", "civ4", "civ1", "civ3", "civ2", "civ4"]):
        put(d, "parade", 37.0, -19 + k * 1.3, BANK + 0.08, outfit=o, arm_r=-120 + 70 * math.sin(now * 6 + k), mouth="smile")
    for k in range(5):
        put(d, "parade", 32.5, -22 + now * 1.0 + k * 1.6 - T["yousee"], BANK + 0.08, walk=now * 6, musket=True,
            hop=abs(math.sin(now * 6)) * 5)
    return cam2d(img, lerp(1.0, 1.08, t / d0), 0.5, 0.55)

def s_boots(now, t, d0):
    img = cam2d(still("boots"), 1.0); d = ImageDraw.Draw(img)
    beats = [T["left1"], T["right"], T["left2"]]
    for i, (bx, b) in enumerate(zip((250, 470, 250), beats)):
        if i == 2 and now < beats[2]: continue
        if i == 0 and now >= beats[2]: continue
        k = now - b
        yb = 300 if k < 0 else (860 if k >= 0.12 else lerp(200, 860, clamp(k / 0.12)))
        d.rectangle([bx - 30, -10, bx + 30, yb - 60], fill=(235, 235, 230), outline=BLACK, width=5)
        d.rounded_rectangle([bx - 70, yb - 80, bx + 90, yb + 40], radius=40, fill=BLACK)
        d.rectangle([bx - 30, yb - 120, bx + 30, yb - 60], fill=RED, outline=BLACK, width=4)
    sh = 10 if any(0 <= now - b < 0.15 for b in beats) else 0
    return cam2d(img, 1.04 if sh else 1.0, 0.5, 0.5, shake=sh, t=now)

def s_crowd(now, t, d0):
    img = still("crowd", blur=7); d = ImageDraw.Draw(img)
    for k, (o, y) in enumerate(zip(["civ3", "civ1", "civ2", "civ4"], [-15.6, -14.5, -13.4, -12.3])):
        fx, fy, R = put(d, "crowd", 35.8 + (k % 2) * 0.6, y, BANK + 0.08, outfit=o, hop=abs(math.sin(now * 7 + k)) * 40,
                        arm_l=40 + 30 * math.sin(now * 9 + k), arm_r=140 - 30 * math.sin(now * 9 + k), mouth="open", brows="none")
    return cam2d(img, lerp(1.0, 1.08, t / d0), 0.5, 0.6)
s_crowd2 = s_crowd

def closeup_bg(): return cam2d(still("close", blur=9), 1.0)

def s_officer(now, t, d0):
    img = closeup_bg(); d = ImageDraw.Draw(img)
    sh = now >= T["break"]
    person(d, 360, 1250, 150, arm_r=70 if sh else -110, arm_l=-60, brows="angry" if sh else "calm", mouth="shout" if sh else "flat")
    return cam2d(img, 1.06 if sh else 1.0, 0.5, 0.5, shake=8 if sh and now - T["break"] < 0.5 else 0, t=now)

def s_purple(now, t, d0):
    img = closeup_bg(); d = ImageDraw.Draw(img)
    face = lerpc(WHITE, (150, 60, 140), ease(t / max(0.4, d0 * 0.8)))
    person(d, 360, 1350, 190, outfit="general", face=face, brows="angry", mouth="frown", arm_l=-80, arm_r=-100)
    return cam2d(img, lerp(1.0, 1.25, ease(t / d0)), 0.5, 0.44)

def s_nose(now, t, d0):
    img = closeup_bg(); d = ImageDraw.Draw(img)
    lean = ease(t / 0.6) * 40
    person(d, 170, 1300, 120, arm_r=-110)
    person(d, 560 - lean, 1330, 135, outfit="general", face=(150, 60, 140), brows="angry",
           mouth="shout" if int(t * 8) % 2 else "open", flip=True, arm_l=150, arm_r=-100)
    return cam2d(img, 1.05, 0.5, 0.55, shake=3, t=now)

def s_ducks(now, t, d0):
    img = still("mid"); d = ImageDraw.Draw(img)
    march(d, "mid", now, [-4.5 + k * 1.2 for k in range(7)], chaos=True)
    fg(img, "mid")
    img = cam2d(img, 1.25, 0.5, 0.55); d = ImageDraw.Draw(img)
    if now >= T["ducks"]:
        for k in range(3):
            d.text((90 + k * 190 + t * 15, 380 - k * 25), "QUACK", font=FONT_XS, fill=WHITE, stroke_width=3, stroke_fill=BLACK)
    return img

def s_news(now, t, d0):
    img = cam2d(still("news"), 2.35, 0.5, 0.215)
    p = Image.new("RGBA", (560, 760), (238, 230, 205, 255)); d = ImageDraw.Draw(p)
    d.rectangle([0, 0, 559, 759], outline=BLACK, width=4)
    d.text((280, 50), "THE MANCHESTER", font=FONT_XS, fill=BLACK, anchor="mm")
    d.text((280, 90), "DAILY COURIER", font=FONT_XS, fill=BLACK, anchor="mm")
    d.line([(20, 120), (540, 120)], fill=BLACK, width=3)
    d.text((280, 175), "THE DUCK", font=FONT_S, fill=BLACK, anchor="mm")
    d.text((280, 240), "BRIGADE", font=FONT_S, fill=BLACK, anchor="mm")
    d.rectangle([60, 290, 500, 600], outline=BLACK, width=3, fill=(225, 218, 190))
    person(d, 280, 570, 70, walk=0.9, brows="worried", musket=True)
    hc = 570 - 3.15 * 70
    d.polygon([(310, hc + 20), (380, hc + 35), (310, hc + 50)], fill=(240, 150, 30), outline=BLACK)
    for yy in range(630, 740, 22): d.line([(40, yy), (520, yy)], fill=(120, 120, 120), width=6)
    k = ease(t / 0.7)
    p = p.rotate(lerp(380, 6, k), expand=True, resample=Image.BICUBIC)
    s = lerp(0.2, 1.0, k); p = p.resize((max(1, int(p.width * s)), max(1, int(p.height * s))))
    sh = Image.new("RGBA", p.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 90), mask=p.split()[3])
    sh = sh.filter(ImageFilter.GaussianBlur(12))
    img.paste(sh, (360 - p.width // 2 + 18, 620 - p.height // 2 + 24), sh)
    img.paste(p, (360 - p.width // 2, 620 - p.height // 2), p)
    return cam2d(img, lerp(1.0, 1.1, t / d0), 0.5, 0.47)

def s_proud(now, t, d0):
    img = still("mid"); d = ImageDraw.Draw(img)
    march(d, "mid", now, [-6.5 + t * 1.0 + k * 1.2 for k in range(5)], lead="calm")
    fg(img, "mid")
    return cam2d(img, lerp(1.25, 1.1, t / d0), 0.5, 0.55)

def s_hum(now, t, d0):
    img = plate("hum", now); d = ImageDraw.Draw(img)
    amp, f, c = bridge_state(now)
    x0 = -6.5 + (now - T["next"]) * 1.0
    march(d, "hum", now, [x0 + k * 1.2 for k in range(5)], lead="calm" if now < T["bounce"] else "worried",
          zfun=lambda x: deck_z(x, now) + 0.12)
    fg(img, "hum", now)
    return cam2d(img, 1.0, 0.5, 0.5, shake=min(10, amp * 25), t=now)

def s_swing(now, t, d0):
    img = plate("swing", now); d = ImageDraw.Draw(img)
    x0 = -6.5 + (now - T["next"]) * 1.0
    march(d, "swing", now, [x0 + k * 1.2 for k in range(5)], lead="worried", scared=True,
          zfun=lambda x: deck_z(x, now) + 0.12, hop=6)
    fg(img, "swing", now)
    return cam2d(img, 1.0, 0.5, 0.5, shake=4, t=now)

def s_bolts(now, t, d0):
    img = plate("bolts", now)
    flash = any(0 <= now - p < 0.07 for p in POP_TIMES)
    if flash:
        ov = Image.new("RGB", img.size, (255, 235, 180)); img = Image.blend(img, ov, 0.35)
    return cam2d(img, 1.06 if flash else 1.0, 0.5, 0.5, shake=6 + (14 if flash else 0) + 6 * t / d0, t=now)

def s_collapse(now, t, d0):
    img = plate("collapse", now); d = ImageDraw.Draw(img)
    _, _, c = bridge_state(now)
    x0 = -6.5 + (T["folds"] - T["next"]) * 1.0
    if c < 0.08:
        march(d, "collapse", now, [x0 + k * 1.2 for k in range(5)], lead="worried", scared=True,
              zfun=lambda x: deck_z(x, now) + 0.12)
    else:
        tf = now - T["folds"] - 0.15
        r = random.Random(4)
        for k in range(6):
            x = x0 + k * 1.2; z = DECK_Z + 0.12 - 4.9 * max(0, tf - 0.05 * k) ** 2 + r.uniform(0, 0.4)
            if z > 0.5:
                put(d, "collapse", x + r.uniform(-1, 1) * tf, -0.5 + r.uniform(-1, 1), z, arm_l=150, arm_r=30,
                    brows="worried", mouth="open")
    fg(img, "collapse", now)
    return cam2d(img, 1.0, 0.5, 0.5, shake=10 if 0.15 < t < 2.5 else 0, t=now)

def s_diagram(now, t, d0):
    img = Image.new("RGB", (W, H), (25, 60, 120)); d = ImageDraw.Draw(img)
    for x in range(0, W, 40): d.line([(x, 0), (x, H)], fill=(45, 85, 150), width=1)
    for y in range(0, H, 40): d.line([(0, y), (W, y)], fill=(45, 85, 150), width=1)
    LC = (220, 235, 255)
    d.text((360, 170), "RESONANCE", font=FONT_S, fill=LC, anchor="mm")
    d.line([(80, 1060), (640, 1060)], fill=LC, width=5)
    for tx in (80, 640): d.rectangle([tx - 15, 980, tx + 15, 1150], outline=LC, width=4)
    amp = 10 + 110 * clamp((now - T["match"]) / max(0.5, T["apart"] - T["match"])) if now > T["match"] else 10
    pts = [(x, 1060 - amp * math.sin(math.pi * (x - 80) / 560) * math.sin(now * 2 * math.pi * 1.5)) for x in range(80, 641, 8)]
    d.line(pts, fill=(255, 210, 90), width=7)
    d.text((360, 1200), "bridge: 1.5 swings / sec", font=FONT_XS, fill=LC, anchor="mm")
    for i in range(6):
        bx = 120 + i * 95; on = now > T["match"] and i <= int((now - T["match"]) * 1.5) % 6
        d.rounded_rectangle([bx - 26, 360, bx + 34, 400], radius=14, fill=(255, 210, 90) if on else None, outline=LC, width=3)
        d.rectangle([bx - 12, 300, bx + 12, 362], outline=LC, width=3)
    d.text((360, 470), "boots: 1.5 steps / sec", font=FONT_XS, fill=LC, anchor="mm")
    return img

FN = {n: globals()[n] for _, n in SCENES}

def caption(img, now):
    cur = None
    for i, w in enumerate(WORDS):
        if w["s"] <= now and (i + 1 == len(WORDS) or now < WORDS[i + 1]["s"]): cur = (i, w)
    if not cur or now > cur[1]["e"] + 0.6: return
    i, w = cur; txt = w["w"]
    if len(txt) <= 3 and i + 1 < len(WORDS) and WORDS[i + 1]["s"] - w["s"] < 0.35: txt += " " + WORDS[i + 1]["w"]
    pop = 1.0 + 0.12 * clamp(1 - (now - w["s"]) / 0.1)
    f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(76 * pop))
    ImageDraw.Draw(img).text((W // 2, int(H * 0.70)), txt, font=f, fill=WHITE, anchor="mm", stroke_width=7, stroke_fill=BLACK)

def frame(now):
    si = max(i for i in range(len(SCENES)) if STARTS[i] <= now)
    t = now - STARTS[si]; d0 = STARTS[si + 1] - STARTS[si]
    img = FN[SCENES[si][1]](now, t, d0); caption(img, now); return img

if PREVIEW:
    only = sys.argv[3].split(",") if sys.argv[3] != "all" else None
    for i, (k, n) in enumerate(SCENES):
        if only and n not in only: continue
        try: frame(min(STARTS[i] + 0.6 * (STARTS[i + 1] - STARTS[i]), DUR - 0.01)).save(f"{OUT}_{i:02d}.jpg", quality=85)
        except FileNotFoundError as e: print("missing", n, e)
    sys.exit()

AUD = os.path.join(HERE, "out", "01-broughton-bridge.wav")
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                      "-i", "-", "-i", AUD, "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium",
                      "-crf", "19", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100",
                      "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
nf = int(DUR * FPS)
for i in range(nf):
    p.stdin.write(frame(i / FPS).tobytes())
    if i % 300 == 0: print("frame", i, "/", nf, flush=True)
p.stdin.close(); p.wait(); print("done")
