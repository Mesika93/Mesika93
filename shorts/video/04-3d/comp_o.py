"""Otis safety elevator: 2D characters over Blender plates.
usage: python3 comp_d.py PLATES OUT.mp4 | python3 comp_d.py PLATES PREFIX scene,scene|all"""
import sys, os, json, math, random, re, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
PL = sys.argv[1]; OUT = sys.argv[2]; PREVIEW = len(sys.argv) > 3
W, H, FPS = 720, 1280, 30
PW, PH = 1080, 1920
BLACK = (20, 20, 20); WHITE = (250, 250, 248); RED = (200, 30, 40); GOLD = (230, 185, 60)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; FS = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
def font(sz, serif=False): return ImageFont.truetype(FS if serif else FB, max(1, int(sz)))
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def ease(t): t = clamp(t); return t * t * (3 - 2 * t)
def lerp(a, b, t): return a + (b - a) * t

# ---------------- timeline ----------------
data = json.load(open(os.path.join(HERE, "r", "words.json")))
WORDS = data["words"]; DUR = data["dur"] + 0.15
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())
NW = [norm(w["w"]) for w in WORDS]
def find(phrase, after=0):
    p = [norm(x) for x in phrase.split()]
    for i in range(after, len(NW)):
        if NW[i:i + len(p)] == p: return i
    raise SystemExit("not found: " + phrase)
def wt(phrase, after=0): return WORDS[find(phrase, after)]["s"]
T = {"he": 0.0}
for k, ph in [("cut", "cut the only"), ("yousee", "you see"), ("1854", "1854"), ("buildings", "buildings stop"), ("because", "because nobody"),
              ("ropes", "ropes snap"), ("snap1", "snap"), ("platforms", "platforms fall"), ("workers", "workers die"), ("elisha", "elisha otis"),
              ("says", "says he's"), ("nobody", "nobody believes"), ("quote", "a rope is"), ("when", "when it breaks"), ("so", "so at the"),
              ("builds", "he builds"), ("rises", "rises above"), ("then", "then he hands"), ("cutit", "cut it"), ("crowd", "the crowd screams"),
              ("snaps", "the rope snaps"), ("drops", "the platform drops"), ("inches", "inches"), ("stops", "and stops"), ("allsafe", "all safe gentlemen"),
              ("allsafe2", "all safe", ), ("above", "above that"), ("spring", "wagon spring"), ("snapped", "snapped open"), ("slack", "slack"),
              ("jammed", "jammed iron"), ("thats", "that's why the"), ("cities", "and that's why cities"), ("up", "grew up")]:
    T[k] = wt(ph)
T["allsafe2"] = wt("all safe", find("gentlemen"))
SCENES = [("he", "s_hook"), ("yousee", "s_street"), ("buildings", "s_up"), ("because", "s_site"), ("ropes", "s_fall"),
          ("elisha", "s_shop"), ("nobody", "s_nobody"), ("quote", "s_quote"), ("so", "s_hall"), ("builds", "s_rise"),
          ("then", "s_axe"), ("crowd", "s_scream"), ("snaps", "s_snap"), ("drops", "s_drop"), ("allsafe", "s_safe"),
          ("allsafe2", "s_cheer"), ("above", "s_mech"), ("thats", "s_city")]
STARTS = [T[k] for k, _ in SCENES] + [DUR]
CY, TZ, WY = 500.0, 9.0, 1500.0
SX, SY = 13.5, 23.0
CROWD = ["rich1", "lady", "crew", "rich2", "lady2", "prosp1", "banker", "assistant", "prosp2", "lady"]

def crowd(d, cam, pts, now, mood="calm", seed=0, look=0):
    rr = random.Random(seed)
    for k, (x, y) in enumerate(sorted(pts, key=lambda p: -p[1])):
        who = CROWD[(k + seed) % len(CROWD)]
        if mood == "scream":
            kw = dict(brows="worried", mouth="open", eyes="big", arm_l=100 + 20 * math.sin(now * 12 + k), arm_r=80 - 20 * math.sin(now * 12 + k),
                      hop=abs(math.sin(now * 10 + k)) * 6)
        elif mood == "cheer":
            kw = dict(brows="up", mouth="laugh", eyes="closed", arm_l=120, arm_r=60, hop=abs(math.sin(now * 9 + k)) * 14)
        elif mood == "up":
            kw = dict(brows="up", mouth="o", eyes="dot", arm_l=-70, arm_r=-110, look=0)
        else:
            kw = dict(brows="calm", mouth=rr.choice(["flat", "smile"]), arm_l=-70, arm_r=-110, look=rr.choice([-1, 1]))
        put(d, cam, x, y, 0.0, height=rr.uniform(1.6, 1.8), who=who, **kw)

def fg_heads(d, now, mood="up", seed=0, skip=()):
    for k, (x, R) in enumerate([(120, 150), (380, 170), (660, 160), (930, 155)]):
        if k in skip: continue
        who = CROWD[(k + seed) % len(CROWD)]
        if mood == "scream": kw = dict(brows="worried", mouth="open", eyes="big", arm_l=110, arm_r=70)
        elif mood == "cheer": kw = dict(brows="up", mouth="laugh", eyes="closed", arm_l=130, arm_r=50)
        else: kw = dict(brows="up", mouth="o", eyes="dot")
        hop = abs(math.sin(now * 9 + k)) * (30 if mood == "cheer" else 10 if mood == "scream" else 0)
        guy(d, x, PH + 2.2 * R, R, who=who, hop=hop, look=0, **kw)

def dust(d, cx, cy, now, t0, n=24, spread=320, seed=0):
    if now < t0: return
    rr = random.Random(seed); tt_ = now - t0
    for k in range(n):
        a = rr.uniform(math.pi, 2 * math.pi); v = rr.uniform(0.4, 1.0)
        x = cx + math.cos(a) * spread * v * min(1, tt_ * 2); y = cy + math.sin(a) * spread * 0.35 * v * min(1, tt_ * 2) - 40 * tt_
        r = 30 + 70 * min(1, tt_ * 1.5) * v; g = int(170 + 40 * v)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(g, g - 15, g - 35))

def s_hook(now, t, d0):
    img = still("towerlow"); d = ImageDraw.Draw(img)
    put(d, "towerlow", 0.3, CY - 0.3, TZ + 0.2, who="otis", brows="calm", mouth="flat", arm_r=-20, arm_l=-70, look=1)
    fg_heads(d, now, "up", 1)
    put(d, "towerlow", 2.0, CY - 2.0, 0.0, who="assistant", brows="worried", mouth="o", eyes="big", arm_r=60, arm_l=-60, prop="axe", look=-1)
    if now >= T["cut"]:
        rx, ry = proj("towerlow", (0.0, CY, TZ + 3.8)); k = pop(now, T["cut"], 0.2)
        arrow(d, rx + 300, ry - 160, rx + 30, ry - 10, col=(255, 220, 60))
        label(d, min(rx + 300, 760), ry - 220, "THE ONLY ROPE", int(64 * k), (255, 220, 60))
    return cam2d(img, 1.0 + 0.1 * t / d0, 0.5, 0.45)

def s_street(now, t, d0):
    img = still("street"); d = ImageDraw.Draw(img)
    for k, (x0, y, sp) in enumerate([(-7.5, 4, 1.0), (7.4, 0, -0.8), (-7.0, 14, 0.7), (7.6, 18, -1.0), (2.0, 30, 0.5)]):
        x = x0; yy = y + sp * now * 1.2
        put(d, "street", x, yy, 0.15 if abs(x) > 6 else 0.0, who=CROWD[k], walk=now * 7 + k, look=0, mouth="flat")
    stamp(img, "1854", now, T["1854"], 540, 420, 140, (240, 235, 220), -6)
    return cam2d(img, 1.05 + 0.05 * t / d0, 0.5, 0.5)

def s_up(now, t, d0):
    img = still("streetup"); d = ImageDraw.Draw(img)
    if t > 0.5:
        k = pop(now, STARTS[2] + 0.5, 0.3)
        y = proj("streetup", (9.0, 30.0, 20.5))[1]
        d.line([(0, y), (PW * k, y)], fill=(255, 220, 60), width=10)
        label(d, 540, y - 90, "MAX ~6 FLOORS", int(70 * k), (255, 220, 60))
    return cam2d(img, 1.0, 0.5, 0.5)

def s_site(now, t, d0):
    img = still("site"); d = ImageDraw.Draw(img)
    put(d, "site", 5.0, 15.0, 0.0, who="crew", brows="worried", mouth="frown", look=1)
    put(d, "site", 6.5, 13.8, 0.0, who="prosp2", brows="angry", mouth="flat", look=1)
    return cam2d(img, 1.05, 0.5, 0.5)

def s_fall(now, t, d0):
    fallen = now >= T["snap1"]
    img = still("fall" if fallen else "site"); d = ImageDraw.Draw(img)
    if fallen:
        px, py = proj("fall", (SX, SY, 0.5))
        dust(d, px, py, now, T["snap1"], 30, 420, 3)
        hx, hy = proj("fall", (SX - 3.5, SY - 4.5, 0.1))
        d.chord([hx - 60, hy - 55, hx + 60, hy + 10], 180, 360, fill=(110, 82, 52), outline=BLACK, width=4)
        d.ellipse([hx - 95, hy - 12, hx + 95, hy + 14], fill=(95, 70, 45), outline=BLACK, width=4)
        if now >= T["workers"]: stamp(img, "ACCIDENT", now, T["workers"], 540, 420, 110, RED, -8)
    else:
        put(d, "site", 5.0, 15.0, 0.0, who="crew", brows="worried", mouth="o", eyes="big", look=1)
    return cam2d(img, 1.05, 0.5, 0.5, shake=10 if fallen and now - T["snap1"] < 0.5 else 0, t=now)

def s_shop(now, t, d0):
    img = still("shop"); d = ImageDraw.Draw(img)
    put(d, "shop", 0.9, WY + 1.8, 0.0, who="otis", brows="calm", mouth="smile", arm_r=20 if now < T["says"] else -10, arm_l=-70,
        prop="wrench" if now < T["says"] else None, look=-1)
    if now >= T["says"]:
        mx, my = proj("shop", (-0.8, WY + 3.2, 1.6)); sparkle(d, mx + 30, my - 60, 60, abs(math.sin(now * 4)) * 0.6 + 0.4)
        label(d, mx, my - 200, "CAN'T FALL", int(70 * pop(now, T["says"] + 0.6, 0.2)), (255, 220, 60))
    return cam2d(img, 1.1 + 0.06 * t / d0, 0.5, 0.52)

def s_nobody(now, t, d0):
    img = still("street", 8); d = ImageDraw.Draw(img)
    guy(d, 600, 1800 - abs(math.sin(now * 13)) * 25, 240, who="skeptic", face=(250, 215, 205), mouth="laugh", eyes="closed", brows="up", arm_l=60, arm_r=120)
    guy(d, 230, 1760, 200, who="otis", brows="calm", mouth="flat", arm_l=-60, arm_r=-110, look=1)
    for k in range(3): label(d, 620 + 170 * math.cos(k * 2.1 + now * 2), 700 + 60 * k + 15 * math.sin(now * 9 + k), "HA", 72, WHITE)
    return cam2d(img, 1.0, 0.5, 0.5, shake=3, t=now)

def s_quote(now, t, d0):
    img = still("street", 12); d = ImageDraw.Draw(img)
    for k in range(5):   # cigar smoke
        ph = (now * 0.5 + k * 0.2) % 1.0
        d.ellipse([700 + 60 * ph - 40 - 30 * ph, 900 - 500 * ph - 40, 700 + 60 * ph + 40 + 30 * ph, 900 - 500 * ph + 40], fill=(200, 200, 200))
    guy(d, 540, 2450, 420, who="skeptic", face=(250, 200, 190), mouth="open" if int(now * 7) % 2 else "smug", brows="angry",
        arm_l=-100, arm_r=70 + 12 * math.sin(now * 10), look=-0.3)
    return cam2d(img, 1.0 + 0.06 * t / d0, 0.5, 0.5)

def s_hall(now, t, d0):
    img = still("hall"); d = ImageDraw.Draw(img)
    rr = random.Random(5)
    pts = [(rr.uniform(-9, 9), CY - rr.uniform(8, 30)) for _ in range(14)]
    pts = [(x, y + t * 1.5) for x, y in pts]
    crowd(d, "hall", pts, now, "calm", 2)
    return cam2d(img, 1.05 + 0.08 * t / d0, 0.5, 0.48)

def s_rise(now, t, d0):
    img = still("towerlow"); d = ImageDraw.Draw(img)
    put(d, "towerlow", 0.3, CY - 0.3, TZ + 0.2, who="otis", brows="up", mouth="smile", arm_r=60 + 20 * math.sin(now * 6),
        arm_l=-70, look=1)
    fg_heads(d, now, "up", 1)
    return cam2d(img, 1.25, 0.5, lerp(0.62, 0.36, ease(t / d0)))

def s_axe(now, t, d0):
    img = still("ropetop"); d = ImageDraw.Draw(img)
    sh = 6 * math.sin(now * 40)
    guy(d, 780 + sh, 2350, 360, who="assistant", brows="worried", mouth="o", eyes="big", arm_r=55, arm_l=-40, prop="axe", look=-1)
    for j in range(3):
        yy = 1150 + ((now * 260 + j * 60) % 160)
        d.ellipse([560 + j * 40, yy, 590 + j * 40, yy + 45], fill=(150, 200, 255))
    if now >= T["cutit"]: label(d, 360, 520, "CUT IT.", int(110 * pop(now, T["cutit"], 0.15)), WHITE)
    return cam2d(img, 1.0 + 0.1 * t / d0, 0.5, 0.5)

def s_scream(now, t, d0):
    img = still("hall", 7); d = ImageDraw.Draw(img)
    for k, (x, y, R, who) in enumerate([(220, 1900, 210, "lady"), (560, 1960, 230, "rich1"), (880, 1880, 200, "lady2"), (400, 1500, 120, "crew"), (760, 1480, 120, "prosp1")]):
        guy(d, x, y - abs(math.sin(now * 10 + k)) * 12, R, who=who, brows="worried", mouth="open", eyes="big" if k % 2 else "closed",
            arm_l=110 + 15 * math.sin(now * 12 + k), arm_r=70 - 15 * math.sin(now * 12 + k))
    label(d, 540, 600, "AAAA!", 150, WHITE)
    return cam2d(img, 1.0, 0.5, 0.5, shake=6, t=now)

def s_snap(now, t, d0):
    img = still("ropecut" if t > 0.25 else "ropetop"); d = ImageDraw.Draw(img)
    if t > 0.25:
        rx, ry = proj("ropecut", (0.0, CY, TZ + 4.4)); rr = random.Random(7); tt_ = t - 0.25
        for k in range(30):
            a = rr.uniform(0, 2 * math.pi); v = rr.uniform(150, 600)
            x, y = rx + math.cos(a) * v * tt_, ry + math.sin(a) * v * tt_ + 300 * tt_ * tt_
            d.line([(x, y), (x + 14 * math.cos(a), y + 14 * math.sin(a))], fill=(190, 160, 110), width=4)
        if tt_ < 0.08: img = Image.blend(img, Image.new("RGB", img.size, (255, 255, 255)), 0.6)
    else:
        guy(ImageDraw.Draw(img), 800, 2350, 360, who="assistant", brows="angry", mouth="shout" if False else "open", eyes="closed", arm_r=120, arm_l=60, prop="axe", look=-1)
    return cam2d(img, 1.1, 0.5, 0.5, shake=14 if 0.2 < t < 0.7 else 0, t=now)

def s_drop(now, t, d0):
    img = still("towerlow"); d = ImageDraw.Draw(img)
    drop = 0.0 if now < T["drops"] + 0.4 else min(0.08, (now - T["drops"] - 0.4) * 0.6)
    put(d, "towerlow", 0.3, CY - 0.3, TZ + 0.2 - drop, who="otis", brows="calm", mouth="flat", arm_r=-30, arm_l=-70, look=1)
    fg_heads(d, now, "scream" if now < T["stops"] else "up", 1)
    if now >= T["inches"]:
        px, py = proj("towerlow", (1.4, CY - 1.0, TZ)); k = pop(now, T["inches"], 0.2)
        d.rectangle([px + 40, py - 90, px + 70, py + 30], fill=(255, 220, 60), outline=BLACK, width=3)
        for j in range(5): d.line([(px + 40, py - 90 + j * 30), (px + 58, py - 90 + j * 30)], fill=BLACK, width=3)
        label(d, px + 190, py - 30, "3 in", int(70 * k), (255, 220, 60))
    if now >= T["stops"]: stamp(img, "STOPPED", now, T["stops"] + 0.2, 540, 420, 110, (60, 200, 90), -8)
    sh = 16 if T["drops"] + 0.4 < now < T["drops"] + 0.75 else 0
    return cam2d(img, 1.12, 0.5, 0.42, shake=sh, t=now)

def s_safe(now, t, d0):
    img = still("platform"); d = ImageDraw.Draw(img)
    guy(d, 520, 2100, 330, who="otisbare", brows="calm", mouth="smile", arm_r=35 + 10 * math.sin(now * 3), arm_l=-60, prop="tophat", look=0.5)
    return cam2d(img, 1.0 + 0.05 * t / d0, 0.5, 0.5)

def s_cheer(now, t, d0):
    img = still("towerlow"); d = ImageDraw.Draw(img)
    put(d, "towerlow", 0.3, CY - 0.3, TZ + 0.2, who="otisbare", brows="calm", mouth="smile", arm_r=75, arm_l=-60, prop="tophat", look=1)
    fg_heads(d, now, "cheer", 1, skip=(3,))
    fx, fy, R = 860, 2150, 220
    guy(d, fx, fy, R, who="skeptic", face=(250, 215, 205), mouth="o", eyes="big", brows="up", arm_l=-80, arm_r=-100)
    cy0 = fy - 2.8 * R + 900 * max(0, t - 0.4) ** 2
    d.line([(fx + 0.4 * R, cy0), (fx + 0.9 * R, cy0 + 0.1 * R)], fill=(110, 70, 40), width=int(R * 0.15))
    rr = random.Random(4)
    for k in range(60):   # confetti
        x = rr.uniform(0, PW); y = (rr.uniform(-PH, 0) + now * rr.uniform(300, 600)) % PH
        d.rectangle([x, y, x + 14, y + 8], fill=rr.choice([(220, 40, 50), (250, 220, 60), (60, 120, 220), (250, 250, 250)]))
    return cam2d(img, 1.05, 0.5, 0.48)

def s_mech(now, t, d0):
    b = now >= T["snapped"]
    img = still("mechB" if b else "mechA"); d = ImageDraw.Draw(img); cam = "mechB" if b else "mechA"
    G = (80, 230, 110)
    if now >= T["slack"] or b:
        x, y = proj(cam, (0.0, CY, TZ + 3.4)); label(d, x, y - 260, "ROPE SLACK", 60, (255, 220, 60))
    if b:
        x, y = proj(cam, (0.0, CY, TZ + 2.55)); k = pop(now, T["snapped"], 0.2)
        arrow(d, x - 200, y - 200, x - 30, y - 20, col=G); label(d, x - 160, y - 260, "SPRING SNAPS", int(58 * k), G)
    if now >= T["jammed"]:
        k = pop(now, T["jammed"], 0.2)
        for s in (-1, 1):
            x, y = proj(cam, (s * 1.3, CY, TZ + 2.6))
            d.ellipse([x - 90 * k, y - 90 * k, x + 90 * k, y + 90 * k], outline=G, width=9)
        label(d, 540, 1560, "TEETH LOCK", int(90 * k), G)
    return cam2d(img, 1.0, 0.5, 0.5, shake=8 if b and now - T["snapped"] < 0.25 else 0, t=now)

def s_city(now, t, d0):
    lo = still("streetup"); hi = ImageEnhance.Brightness(still("skyline")).enhance(1.5)
    u = ease(clamp((now - T["cities"]) / 1.6))
    if u <= 0: img = lo
    else:
        mask = Image.new("L", lo.size, 0); md = ImageDraw.Draw(mask)
        md.rectangle([0, int(PH * (1 - u)), PW, PH], fill=255); md.rectangle([0, 0, PW, PH], fill=int(255 * u ** 2))
        md.rectangle([0, int(PH * (1 - u)), PW, PH], fill=255)
        img = Image.composite(hi, lo, mask)
    d = ImageDraw.Draw(img)
    cam = "skyline"
    put(d, cam, 0.5, -16.0, 0.0, who="otis", brows="up", mouth="o" if u > 0.3 else "smile", eyes="big" if u > 0.5 else "dot", arm_l=-60, arm_r=-110)
    if now < T["cities"]:
        label(d, 540, 420, "EVERY ELEVATOR", 80, (255, 220, 60)); label(d, 540, 520, "HAS ONE", 80, (255, 220, 60))
    return cam2d(img, 1.0, 0.5, 0.5)

FN = {n: globals()[n] for _, n in SCENES}

# ---------------- plates ----------------
CAMS = json.load(open(os.path.join(PL, "cams.json")))
_cache = {}
def still(name, blur=0):
    k = (name, blur)
    if k not in _cache:
        im = Image.open(os.path.join(PL, name, "still.png")).convert("RGB")
        if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
        _cache[k] = im
    return _cache[k].copy()

def proj(cam, p):
    c = CAMS[cam]; mi = np.array(c["mi"]); rw, rh = c["res"]
    v = mi @ np.array([p[0], p[1], p[2], 1.0])
    s = c["lens"] / c["sensor_h"] * rh
    return rw / 2 + s * v[0] / -v[2], rh / 2 - s * v[1] / -v[2]

def cam2d(img, z=1.0, cx=0.5, cy=0.5, shake=0.0, t=0.0):
    w, h = img.size
    cxp, cyp = cx * w + math.sin(t * 53) * shake * w / W, cy * h + math.cos(t * 41) * shake * h / W
    cw, ch = w / z, h / z
    x0 = clamp(cxp - cw / 2, 0, w - cw); y0 = clamp(cyp - ch / 2, 0, h - ch)
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.LANCZOS)

# ---------------- characters ----------------
COATS = {"king": (150, 120, 75), "prosp1": (120, 70, 45), "prosp2": (70, 85, 110), "banker": (35, 35, 45),
         "jeweler": (90, 40, 60), "expert": (60, 75, 60), "rich1": (40, 40, 50), "rich2": (70, 40, 40),
         "otis": (105, 105, 112), "otisbare": (105, 105, 112), "skeptic": (125, 60, 40), "assistant": (70, 90, 120), "lady": (150, 60, 90), "lady2": (60, 110, 120),
         "wald": (45, 45, 55), "colonel": (95, 98, 58), "officer": (105, 108, 66), "crew": (115, 75, 45)}
def guy(d, x, y, R, who="king", walk=0.0, arm_l=-70, arm_r=-110, brows="calm", mouth="flat", eyes="dot",
        face=WHITE, hop=0.0, crouch=False, look=0.0, prop=None):
    y = y - hop; lw = max(2, int(R * 0.1)); col = COATS.get(who, (120, 120, 120))
    hipdrop = 0.55 * R if crouch else 0
    hip = y - 1.35 * R + hipdrop; neck = y - 2.4 * R + hipdrop; hc = y - 3.2 * R + hipdrop; hr = 0.86 * R
    sw = math.sin(walk) * 0.4 * R
    for s in (1, -1):
        hx = x + s * 0.18 * R
        if crouch:
            kx, ky = hx + 0.45 * R, y - 0.75 * R
            d.line([(hx, hip), (kx, ky), (hx + 0.1 * R, y)], fill=BLACK, width=lw, joint="curve")
            fx = hx + 0.1 * R
        else:
            fx = hx + s * sw; d.line([(hx, hip), (fx, y)], fill=BLACK, width=lw)
        d.ellipse([fx - 0.16 * R, y - 0.09 * R, fx + 0.22 * R, y + 0.07 * R], fill=BLACK)
    tw = 0.52 * R; sh = neck + 0.18 * R
    hands = []
    for ang, sx in ((arm_l, -1), (arm_r, 1)):
        a = math.radians(ang); ex = x + sx * tw * 0.85 + math.cos(a) * 1.05 * R; ey = sh - math.sin(a) * 1.05 * R
        d.line([(x + sx * tw * 0.85, sh), (ex, ey)], fill=BLACK, width=lw)
        d.ellipse([ex - 0.1 * R, ey - 0.1 * R, ex + 0.1 * R, ey + 0.1 * R], fill=WHITE, outline=BLACK, width=max(1, lw // 2))
        hands.append((ex, ey))
    d.rounded_rectangle([x - tw, neck, x + tw, hip + 0.08 * R], radius=int(0.2 * R), fill=col, outline=BLACK, width=lw)
    if who in ("banker", "rich1", "rich2"):
        d.polygon([(x - 0.18 * R, neck), (x + 0.18 * R, neck), (x, neck + 0.55 * R)], fill=WHITE)
        d.line([(x - 0.3 * R, neck + 0.6 * R), (x + 0.1 * R, neck + 0.75 * R)], fill=GOLD, width=max(1, lw // 2))
        d.ellipse([x + 0.05 * R, neck + 0.66 * R, x + 0.18 * R, neck + 0.8 * R], fill=GOLD)
    if who == "king":
        for k in range(3): d.ellipse([x - 0.05 * R, neck + (0.25 + 0.25 * k) * R, x + 0.05 * R, neck + (0.35 + 0.25 * k) * R], fill=BLACK)
    if who.startswith("prosp"):
        d.line([(x - tw + 4, neck + 4), (x - 0.1 * R, hip)], fill=(60, 40, 25), width=lw)
        d.rectangle([x + 0.1 * R, hip - 0.45 * R, x + 0.35 * R, hip - 0.2 * R], fill=(90, 60, 35), outline=BLACK)
    if who in ("lady", "lady2"):
        d.polygon([(x - tw * 0.9, hip - 0.4 * R), (x + tw * 0.9, hip - 0.4 * R), (x + tw * 1.9, y - 0.15 * R), (x - tw * 1.9, y - 0.15 * R)], fill=col, outline=BLACK)
    if who in ("skeptic",):
        d.ellipse([x - tw * 1.35, neck + 0.1 * R, x + tw * 1.35, hip + 0.25 * R], fill=col, outline=BLACK, width=lw)
    # head
    d.ellipse([x - hr, hc - hr, x + hr, hc + hr], fill=face, outline=BLACK, width=lw)
    if who in ("prosp1", "prosp2"):
        bc = (110, 70, 40) if who == "prosp1" else (70, 70, 70)
        d.chord([x - hr * 0.9, hc - 0.1 * R, x + hr * 0.9, hc + hr * 1.25], 0, 180, fill=bc, outline=BLACK, width=lw)
    if who == "banker":
        for s in (-1, 1):
            d.chord([x + s * hr * 0.95 - 0.26 * R, hc - 0.15 * R, x + s * hr * 0.95 + 0.26 * R, hc + 0.65 * R], 0, 360, fill=(170, 170, 170), outline=BLACK)
    ex1, ex2 = x - 0.3 * R + look * 0.1 * R, x + 0.3 * R + look * 0.1 * R; ey = hc - 0.05 * R
    for k, exx in enumerate((ex1, ex2)):
        if eyes == "big" or (eyes == "loupe" and k == 1):
            rr = 0.32 * R if eyes == "loupe" else 0.15 * R
            d.ellipse([exx - rr, ey - rr, exx + rr, ey + rr], fill=WHITE, outline=BLACK, width=lw)
            d.ellipse([exx - rr * 0.4, ey - rr * 0.4, exx + rr * 0.4, ey + rr * 0.4], fill=BLACK)
            if eyes == "loupe": d.ellipse([exx - rr - 4, ey - rr - 4, exx + rr + 4, ey + rr + 4], outline=GOLD, width=lw + 3)
        elif eyes == "closed":
            d.arc([exx - 0.12 * R, ey - 0.1 * R, exx + 0.12 * R, ey + 0.1 * R], 200, 340, fill=BLACK, width=lw)
        elif eyes == "glasses":
            d.ellipse([exx - 0.07 * R, ey - 0.07 * R, exx + 0.07 * R, ey + 0.07 * R], fill=BLACK)
            d.ellipse([exx - 0.17 * R, ey - 0.17 * R, exx + 0.17 * R, ey + 0.17 * R], outline=BLACK, width=max(1, lw // 2))
        else:
            d.ellipse([exx - 0.075 * R, ey - 0.075 * R, exx + 0.075 * R, ey + 0.075 * R], fill=BLACK)
    if eyes == "glasses": d.line([(ex1 + 0.17 * R, ey), (ex2 - 0.17 * R, ey)], fill=BLACK, width=max(1, lw // 2))
    by = ey - 0.27 * R
    for exx, s in ((ex1, -1), (ex2, 1)):
        if brows == "angry": d.line([(exx - s * 0.16 * R, by - 0.09 * R), (exx + s * 0.16 * R, by + 0.06 * R)], fill=BLACK, width=lw)
        elif brows == "worried": d.line([(exx - s * 0.16 * R, by + 0.06 * R), (exx + s * 0.16 * R, by - 0.09 * R)], fill=BLACK, width=lw)
        elif brows == "up": d.arc([exx - 0.15 * R, by - 0.15 * R, exx + 0.15 * R, by + 0.05 * R], 200, 340, fill=BLACK, width=lw)
        elif brows == "raised" and s == 1: d.line([(exx - 0.15 * R, by - 0.12 * R), (exx + 0.15 * R, by - 0.16 * R)], fill=BLACK, width=lw)
        elif brows in ("calm", "raised"): d.line([(exx - 0.15 * R, by), (exx + 0.15 * R, by)], fill=BLACK, width=lw)
    my = hc + 0.4 * R; mx = x + look * 0.08 * R
    if who in ("banker", "expert", "king", "rich1", "colonel", "wald"):
        mc = (90, 60, 40) if who != "banker" else (150, 150, 150)
        d.chord([mx - 0.32 * R, my - 0.2 * R, mx + 0.32 * R, my + 0.05 * R], 180, 360, fill=mc)
    if who not in ("prosp1", "prosp2") or mouth in ("open", "shout", "laugh"):
        if mouth == "flat": d.line([(mx - 0.18 * R, my), (mx + 0.18 * R, my)], fill=BLACK, width=lw)
        elif mouth == "smile": d.arc([mx - 0.26 * R, my - 0.2 * R, mx + 0.26 * R, my + 0.14 * R], 20, 160, fill=BLACK, width=lw)
        elif mouth == "smug": d.arc([mx - 0.1 * R, my - 0.18 * R, mx + 0.3 * R, my + 0.1 * R], 20, 120, fill=BLACK, width=lw)
        elif mouth in ("open", "laugh"):
            hh = 0.3 if mouth == "laugh" else 0.2
            d.chord([mx - 0.26 * R, my - 0.1 * R, mx + 0.26 * R, my + hh * R + 0.1 * R], 0, 180, fill=(130, 25, 35), outline=BLACK, width=lw)
        elif mouth == "o": d.ellipse([mx - 0.12 * R, my - 0.05 * R, mx + 0.12 * R, my + 0.22 * R], fill=(130, 25, 35), outline=BLACK, width=lw)
        elif mouth == "frown": d.arc([mx - 0.22 * R, my, mx + 0.22 * R, my + 0.3 * R], 200, 340, fill=BLACK, width=lw)
    top = hc - hr
    if who == "king":       # slouch hat
        d.ellipse([x - 1.2 * R, top + 0.05 * R, x + 1.2 * R, top + 0.4 * R], fill=(95, 70, 45), outline=BLACK, width=lw)
        d.chord([x - 0.65 * R, top - 0.55 * R, x + 0.65 * R, top + 0.6 * R], 180, 360, fill=(110, 82, 52), outline=BLACK, width=lw)
        d.rectangle([x - 0.62 * R, top + 0.0 * R, x + 0.62 * R, top + 0.08 * R], fill=(60, 40, 25))
    elif who.startswith("prosp"):  # battered hat
        c = (130, 100, 60) if who == "prosp1" else (90, 80, 70)
        d.polygon([(x - 1.0 * R, top + 0.3 * R), (x + 1.05 * R, top + 0.2 * R), (x + 0.6 * R, top - 0.05 * R), (x + 0.5 * R, top - 0.65 * R),
                   (x - 0.1 * R, top - 0.5 * R), (x - 0.55 * R, top - 0.62 * R), (x - 0.6 * R, top)], fill=c, outline=BLACK)
    elif who in ("banker", "rich1", "rich2"):
        d.rectangle([x - 0.95 * R, top + 0.05 * R, x + 0.95 * R, top + 0.22 * R], fill=BLACK)
        d.rectangle([x - 0.6 * R, top - 1.05 * R, x + 0.6 * R, top + 0.12 * R], fill=BLACK)
        d.rectangle([x - 0.6 * R, top - 0.12 * R, x + 0.6 * R, top + 0.0 * R], fill=(120, 20, 30) if who != "rich2" else (60, 60, 120))
    elif who == "expert":   # bowler
        d.chord([x - 0.7 * R, top - 0.6 * R, x + 0.7 * R, top + 0.55 * R], 180, 360, fill=BLACK)
        d.ellipse([x - 0.95 * R, top + 0.02 * R, x + 0.95 * R, top + 0.2 * R], fill=BLACK)
    elif who in ("colonel", "officer"):   # peaked / garrison cap
        if who == "colonel":
            d.chord([x - 0.95 * R, top - 0.55 * R, x + 0.95 * R, top + 0.35 * R], 180, 360, fill=(85, 88, 50), outline=BLACK, width=lw)
            d.rectangle([x - 0.75 * R, top - 0.1 * R, x + 0.75 * R, top + 0.12 * R], fill=(60, 45, 30))
            d.chord([x - 0.8 * R, top + 0.0 * R, x + 0.95 * R, top + 0.42 * R], 0, 180, fill=(30, 25, 20))
            d.ellipse([x - 0.12 * R, top - 0.3 * R, x + 0.12 * R, top - 0.06 * R], fill=GOLD)
        else:
            d.polygon([(x - 0.7 * R, top + 0.12 * R), (x + 0.7 * R, top + 0.12 * R), (x + 0.5 * R, top - 0.35 * R), (x - 0.6 * R, top - 0.2 * R)], fill=(85, 88, 50), outline=BLACK)
    elif who == "crew":    # leather flight cap
        d.chord([x - hr * 1.02, hc - hr * 1.02, x + hr * 1.02, hc + hr * 0.3], 180, 360, fill=(95, 60, 35), outline=BLACK, width=lw)
        for s2 in (-1, 1): d.ellipse([x + s2 * hr * 0.92 - 0.2 * R, hc - 0.1 * R, x + s2 * hr * 0.92 + 0.2 * R, hc + 0.4 * R], fill=(95, 60, 35), outline=BLACK)
    elif who in ("otis", "otisbare"):     # grey top hat + jaw beard
        d.chord([x - hr * 0.95, hc - 0.05 * R, x + hr * 0.95, hc + hr * 1.12], 0, 180, outline=(70, 55, 45), width=int(lw * 2.2))
        if who == "otisbare": d.arc([x - hr, hc - hr, x + hr, hc + hr], 200, 340, fill=(70, 55, 45), width=int(lw * 2))
        if who == "otis": d.rectangle([x - 0.9 * R, top + 0.05 * R, x + 0.9 * R, top + 0.22 * R], fill=(50, 50, 55))
        if who == "otis":
            d.rectangle([x - 0.58 * R, top - 1.0 * R, x + 0.58 * R, top + 0.12 * R], fill=(60, 60, 66))
            d.rectangle([x - 0.58 * R, top - 0.12 * R, x + 0.58 * R, top + 0.0 * R], fill=(20, 20, 20))
    elif who == "skeptic":  # bowler + cigar
        d.chord([x - 0.7 * R, top - 0.6 * R, x + 0.7 * R, top + 0.55 * R], 180, 360, fill=(60, 40, 25))
        d.ellipse([x - 0.95 * R, top + 0.02 * R, x + 0.95 * R, top + 0.2 * R], fill=(60, 40, 25))
        cx0 = x + 0.15 * R; cy0 = hc + 0.42 * R
        d.line([(cx0, cy0), (cx0 + 0.6 * R, cy0 + 0.1 * R)], fill=(110, 70, 40), width=int(lw * 1.6))
        d.ellipse([cx0 + 0.55 * R, cy0 + 0.03 * R, cx0 + 0.67 * R, cy0 + 0.17 * R], fill=(255, 120, 40))
    elif who == "assistant":  # flat cap
        d.chord([x - 0.85 * R, top - 0.45 * R, x + 0.75 * R, top + 0.45 * R], 180, 360, fill=(90, 90, 95), outline=BLACK)
        d.polygon([(x - 0.1 * R, top), (x + 1.05 * R, top + 0.12 * R), (x + 0.7 * R, top + 0.2 * R), (x - 0.1 * R, top + 0.12 * R)], fill=(70, 70, 75))
    elif who in ("lady", "lady2"):  # bonnet
        d.chord([x - hr * 1.15, hc - hr * 1.2, x + hr * 1.15, hc + hr * 0.5], 180, 360, fill=(235, 215, 170), outline=BLACK, width=lw)
        d.line([(x - hr * 0.9, hc + 0.2 * R), (x, hc + hr * 1.05), (x + hr * 0.9, hc + 0.2 * R)], fill=(200, 60, 80), width=lw)
    elif who == "wald":    # dark side hair
        for s2 in (-1, 1): d.chord([x + s2 * hr * 0.8 - 0.3 * R, hc - 0.6 * R, x + s2 * hr * 0.8 + 0.3 * R, hc + 0.1 * R], 0, 360, fill=(40, 35, 30))
        d.line([(x - tw * 0.2, neck + 2), (x, neck + 0.6 * R), (x + tw * 0.2, neck + 2)], fill=WHITE, width=lw)
    elif who == "jeweler":  # bald + visor band
        d.arc([x - hr, hc - hr, x + hr, hc + hr], 200, 340, fill=(60, 120, 60), width=int(lw * 2.5))
    if prop == "stick":
        hx, hy = hands[1]; d.line([(hx, hy), (hx + 1.6 * R, hy + 1.3 * R)], fill=(100, 70, 35), width=lw + 2)
    if prop == "telegram":
        hx, hy = hands[1]; hx2, hy2 = hands[0]
        d.polygon([(hx2 - 0.1 * R, hy2 - 0.9 * R), (hx + 0.1 * R, hy - 0.9 * R), (hx + 0.1 * R, hy + 0.3 * R), (hx2 - 0.1 * R, hy2 + 0.3 * R)],
                  fill=(240, 230, 200), outline=BLACK)
    if prop == "axe":
        hx, hy = hands[1]
        d.line([(hx, hy + 0.3 * R), (hx + 0.2 * R, hy - 1.4 * R)], fill=(120, 80, 40), width=lw + 3)
        d.polygon([(hx + 0.2 * R, hy - 1.4 * R), (hx + 0.85 * R, hy - 1.6 * R), (hx + 0.85 * R, hy - 0.95 * R), (hx + 0.15 * R, hy - 1.05 * R)], fill=(150, 155, 160), outline=BLACK)
    if prop == "wrench":
        hx, hy = hands[1]; d.line([(hx, hy), (hx + 0.5 * R, hy - 0.7 * R)], fill=(150, 150, 155), width=lw + 3)
        d.ellipse([hx + 0.4 * R, hy - 0.9 * R, hx + 0.65 * R, hy - 0.62 * R], outline=(150, 150, 155), width=lw + 1)
    if prop == "tophat":
        hx, hy = hands[1]
        d.rectangle([hx - 0.4 * R, hy - 0.9 * R, hx + 0.4 * R, hy], fill=(60, 60, 66)); d.rectangle([hx - 0.65 * R, hy - 0.08 * R, hx + 0.65 * R, hy + 0.06 * R], fill=(50, 50, 55))
    if prop == "walkstick":
        hx, hy = hands[1]; d.line([(hx, hy - 0.2 * R), (hx + 0.2 * R, y)], fill=(100, 70, 35), width=lw + 1)
    if prop == "bag":
        hx, hy = hands[0]; d.rounded_rectangle([hx - 0.4 * R, hy, hx + 0.4 * R, hy + 0.6 * R], radius=int(0.1 * R), fill=(80, 45, 25), outline=BLACK, width=lw)
    if prop == "diamond":
        hx, hy = hands[1]; sparkle(d, hx, hy - 0.25 * R, 0.3 * R, 1.0)
    return hands

def put(d, cam, x, y, z, height=1.75, **kw):
    fx, fy = proj(cam, (x, y, z)); tx, ty = proj(cam, (x, y, z + height))
    R = max(3, (fy - ty) / 4.06)
    return guy(d, fx, fy, R, **kw), (fx, fy, R)

def sparkle(d, x, y, r, a=1.0, col=(255, 255, 240)):
    if a <= 0: return
    r *= a
    d.polygon([(x, y - r), (x + r * 0.18, y - r * 0.18), (x + r, y), (x + r * 0.18, y + r * 0.18), (x, y + r),
               (x - r * 0.18, y + r * 0.18), (x - r, y), (x - r * 0.18, y - r * 0.18)], fill=col)

def glints(d, pts, now, r=26, seed=0):
    for k, (x, y) in enumerate(pts):
        ph = (now * 2.2 + k * 0.37 + seed) % 1.0
        sparkle(d, x, y, r, max(0, math.sin(ph * math.pi)) ** 2)

def stamp(img, text, now, t0, cx, cy, size=120, col=RED, rot=-12):
    if now < t0: return
    k = clamp((now - t0) / 0.15); s = lerp(2.2, 1.0, ease(k))
    f = font(size * s, True)
    lay = Image.new("RGBA", img.size, (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
    bb = dl.textbbox((cx, cy), text, font=f, anchor="mm")
    dl.rectangle([bb[0] - 22, bb[1] - 18, bb[2] + 22, bb[3] + 18], outline=col + (255,), width=int(10 * s))
    dl.text((cx, cy), text, font=f, fill=col + (255,), anchor="mm")
    lay = lay.rotate(rot, center=(cx, cy))
    img.paste(lay, (0, 0), lay)

def label(d, x, y, text, size=44, col=WHITE):
    if size < 2: return
    d.text((x, y), text, font=font(size), fill=col, anchor="mm", stroke_width=5, stroke_fill=BLACK)

def arrow(d, x0, y0, x1, y1, col=(255, 220, 60), w=10):
    d.line([(x0, y0), (x1, y1)], fill=col, width=w)
    a = math.atan2(y1 - y0, x1 - x0); L = 34
    d.polygon([(x1, y1), (x1 - L * math.cos(a - 0.45), y1 - L * math.sin(a - 0.45)), (x1 - L * math.cos(a + 0.45), y1 - L * math.sin(a + 0.45))], fill=col)

def pop(now, t0, d=0.18): return ease((now - t0) / d) if now >= t0 else 0.0

def caption(img, now):
    cur = None
    for i, w in enumerate(WORDS):
        if w["s"] <= now and (i + 1 == len(WORDS) or now < WORDS[i + 1]["s"]): cur = (i, w)
    if not cur or now > cur[1]["e"] + 0.6: return
    i, w = cur; txt = w["w"]
    if len(txt) <= 3 and i + 1 < len(WORDS) and WORDS[i + 1]["s"] - w["s"] < 0.35: txt += " " + WORDS[i + 1]["w"]
    p = 1.0 + 0.12 * clamp(1 - (now - w["s"]) / 0.1)
    ImageDraw.Draw(img).text((W // 2, int(H * 0.70)), txt, font=font(76 * p), fill=WHITE, anchor="mm", stroke_width=7, stroke_fill=BLACK)

def frame(now):
    si = max(i for i in range(len(SCENES)) if STARTS[i] <= now)
    t = now - STARTS[si]; d0 = STARTS[si + 1] - STARTS[si]
    img = FN[SCENES[si][1]](now, t, d0); caption(img, now); return img

if PREVIEW:
    only = sys.argv[3].split(",") if sys.argv[3] != "all" else None
    for i, (k, n) in enumerate(SCENES):
        if only and n not in only: continue
        frame(min(STARTS[i] + 0.7 * (STARTS[i + 1] - STARTS[i]), DUR - 0.01)).save(f"{OUT}_{i:02d}.jpg", quality=85)
    sys.exit()

# ---------------- audio ----------------
SR = 44100; N = int(DUR * SR) + SR; mix = np.zeros(N)
for f, off in data["files"]:
    f = os.path.join(HERE, "r", os.path.basename(f))
    with wave.open(f) as wv: a = np.frombuffer(wv.readframes(wv.getnframes()), np.int16) / 32768.0
    s = int(off * SR); mix[s:s + len(a)] += a
rng = np.random.default_rng(1)
def add(sig, t, g=1.0):
    s = int(t * SR); e = min(N, s + len(sig)); mix[s:e] += sig[:e - s] * g
def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=0.005, r=None): x = tt(d); r = r or d; return np.minimum(1, x / a) * np.exp(-x / (r / 4))
def noise(d): return rng.standard_normal(int(d * SR))
def lowpass(x, k=40): return np.convolve(x, np.ones(k) / k, mode="same")
def ding(f0, d=0.6, g=0.12): x = tt(d); return (np.sin(2 * np.pi * f0 * x) + 0.4 * np.sin(2 * np.pi * f0 * 2.7 * x)) * env(d, 0.002, d) * g
def murmur(d, g=0.06):
    x = tt(d); fade = np.minimum(1, np.minimum(x / 0.4, (d - x) / 0.4)); return lowpass(noise(d), 60) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * x)) * fade * g * 3
# jaunty plucked bed (stops at the cut)
beat = 60 / 120; notes = [196, 247, 294, 247, 220, 262, 330, 262]
for k, b in enumerate(np.arange(0.2, T["cutit"], beat / 2)):
    add(ding(notes[k % 8], 0.3, 0.035), b)
    if k % 2 == 0: add(np.sin(2 * np.pi * 98 * tt(0.25)) * env(0.25) * 0.06, b)
for a_, b_ in [("he", "yousee"), ("so", "crowd"), ("allsafe2", "above")]: add(murmur(T[b_] - T[a_]), T[a_])
for k in range(4): add(lowpass(noise(0.05), 4) * env(0.05) * 0.15, T["yousee"] + 0.2 + k * 0.3)        # hooves
add(np.sin(2 * np.pi * (220 + 40 * np.sin(2 * np.pi * 2 * tt(1.0))) * tt(1.0)) * env(1.0, 0.05, 1.2) * 0.05, T["because"] + 0.3)  # creak
add(noise(0.25) * env(0.25, 0.001, 0.12) * 0.8, T["snap1"]); add(lowpass(noise(0.8), 30) * env(0.8, 0.005, 0.7) * 1.0, T["snap1"] + 0.15)
add(lowpass(noise(0.12), 8) * env(0.12) * 0.8, T["1854"]); add(lowpass(noise(0.12), 8) * env(0.12) * 0.8, T["workers"])
for k in range(3): add(ding(2400 + 300 * k, 0.15, 0.03), T["elisha"] + 0.4 + k * 0.4)                    # metal clinks
add(ding(1760, 0.6, 0.06), T["says"] + 0.6)
for k in range(5): add(np.sin(2 * np.pi * (300 - 70 * (k % 3)) * tt(0.12)) * env(0.12, 0.005, 0.2) * 0.1, T["nobody"] + 0.1 + k * 0.2)
for k in range(int((T["cutit"] - T["then"]) / 0.05)): add(lowpass(noise(0.04), 3) * env(0.04) * (0.04 + 0.08 * k / 60), T["then"] + 0.3 + k * 0.05)  # drumroll
scr = np.sin(2 * np.pi * (900 + 200 * np.sin(2 * np.pi * 7 * tt(1.3))) * tt(1.3)) * env(1.3, 0.05, 1.4) * 0.05 + murmur(1.3, 0.1)
add(scr, T["crowd"] + 0.3)
add(lowpass(noise(0.1), 2) * env(0.1, 0.001, 0.06) * 1.2, T["snaps"] + 0.25)                             # thwack
add(noise(0.3) * env(0.3, 0.001, 0.1) * 0.6, T["snaps"] + 0.3)
clunk = (np.sin(2 * np.pi * 140 * tt(0.4)) + lowpass(noise(0.4), 10)) * env(0.4, 0.001, 0.3) * 0.5
add(clunk, T["drops"] + 0.4)
# applause
app = np.zeros(int(4.0 * SR))
for k in range(400):
    s = int(rng.uniform(0, 3.6) * SR); c = noise(0.02) * env(0.02, 0.0005, 0.02) * 0.25; app[s:s + len(c)] += c[:len(app) - s]
add(app * np.minimum(1, np.linspace(4, 0, len(app))), T["allsafe2"] - 0.6)
for k in range(8): add(lowpass(noise(0.03), 2) * env(0.03) * 0.25, T["snapped"] + k * 0.06)          # ratchet clicks
add(ding(1320, 1.0, 0.08), T["jammed"]); add(ding(880, 1.5, 0.08), T["cities"]); add(ding(1320, 1.5, 0.06), T["cities"] + 0.4)

mix = mix / max(1e-6, np.abs(mix).max()) * 0.92
WAV = OUT.replace(".mp4", ".wav")
with wave.open(WAV, "wb") as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix * 32767).astype(np.int16).tobytes())

p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                      "-i", "-", "-i", WAV, "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium",
                      "-crf", "19", "-pix_fmt", "yuv420p", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100",
                      "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT], stdin=subprocess.PIPE)
nf = int(DUR * FPS)
for i in range(nf):
    p.stdin.write(frame(i / FPS).tobytes())
    if i % 300 == 0: print("frame", i, "/", nf, flush=True)
p.stdin.close(); p.wait(); print("done")
