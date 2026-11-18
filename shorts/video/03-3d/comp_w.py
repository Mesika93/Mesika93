"""Abraham Wald / survivorship bias: 2D characters over Blender plates.
usage: python3 comp_d.py PLATES OUT.mp4 | python3 comp_d.py PLATES PREFIX scene,scene|all"""
import sys, os, json, math, random, re, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

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
WORDS = data["words"]; DUR = data["dur"] + 0.2
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())
NW = [norm(w["w"]) for w in WORDS]
def find(phrase, after=0):
    p = [norm(x) for x in phrase.split()]
    for i in range(after, len(NW)):
        if NW[i:i + len(p)] == p: return i
    raise SystemExit("not found: " + phrase)
def wt(phrase, after=0): return WORDS[find(phrase, after)]["s"]
T = {"he": 0.0}
for k, ph in [("yousee", "you see"), ("1943", "1943"), ("armor", "armor is heavy"), ("little", "a little"), ("officers", "the officers have"),
              ("count", "count the bullet"), ("wings", "wings full"), ("tail", "tail full"), ("body", "body like"), ("swiss", "swiss cheese"),
              ("engines", "engines almost"), ("almost", "almost clean"), ("sowhen", "so when"), ("armeng", "armor the engines"),
              ("laughs", "laughs"), ("blind", "are you blind"), ("never", "never get hit"), ("but", "but wald"), ("where", "where are the planes"),
              ("silence", "silence"), ("limped", "bombers hit in the wings"), ("nevermade", "bombers hit in the engines"),
              ("holes", "the holes weren't"), ("survive", "survive"), ("missing", "the missing holes"), ("realmap", "real map"),
              ("called", "it's called"), ("bias", "bias")]:
    T[k] = wt(ph)
SCENES = [("he", "s_hook"), ("yousee", "s_sky"), ("armor", "s_armor"), ("officers", "s_plan"), ("wings", "s_wing"), ("tail", "s_tail"),
          ("body", "s_body"), ("engines", "s_engine"), ("sowhen", "s_wald"), ("blind", "s_blind"), ("but", "s_question"),
          ("limped", "s_limp"), ("nevermade", "s_never"), ("holes", "s_map"), ("called", "s_bias")]
STARTS = [T[k] for k, _ in SCENES] + [DUR]
HOLES = json.load(open(os.path.join(HERE, "holes.json")))
FZ = 2.8; BY = 1000.0

def hole_pts(cam, kinds, side=None, up_only=False):
    out = []
    for k, x, y, z in HOLES:
        if k not in kinds: continue
        if side == "+x" and x < 0.05: continue
        if up_only and k == "body" and z < FZ + 0.4: continue
        px, py = proj(cam, (x, y, z))
        if 0 < px < PW and 0 < py < PH: out.append((px, py))
    return out

def red_dots(d, pts, now, t0, r=16, per=0.02):
    for k, (x, y) in enumerate(pts):
        a = pop(now, t0 + k * per, 0.12)
        if a <= 0: continue
        rr = r * (1 + 0.6 * (1 - a))
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(230, 30, 35), outline=(255, 255, 255), width=3)

def ring_marks(d, pts, now, t0, r=34, per=0.06, col=(255, 60, 50)):
    for k, (x, y) in enumerate(pts):
        a = pop(now, t0 + k * per, 0.15)
        if a <= 0: continue
        rr = r * (1.8 - 0.8 * a)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], outline=col, width=7)

def counter(d, now, t0, n, label_txt, y=430, col=(255, 80, 70)):
    if now < t0: return
    k = int(min(n, (now - t0) * 40))
    label(d, 540, y, f"{label_txt}: {k}", 84, col)

def smoke(d, pts, now, seed=0, col=(40, 40, 40)):
    rr = random.Random(seed)
    for k, (x, y) in enumerate(pts):
        r = 18 + 4 * k + 6 * math.sin(now * 3 + k)
        g = int(40 + 3 * k)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(g, g, g))

def flak(d, now, seed=1):
    rr = random.Random(seed)
    for k in range(10):
        x = rr.uniform(80, 1000); y = rr.uniform(150, 1100); ph = (now * 0.8 + rr.random()) % 1.0
        if ph < 0.12:
            r = 15 + 250 * ph
            d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 200, 90))
            r *= 0.5; d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 245, 210))

def chalk_board(img, lines, now, t0, size=62):
    """write chalk text on the briefing-room board (projected)"""
    if now < t0: return
    (x0, y0), (x1, y1) = proj("room", (-2.85, BY + 5.94, 3.1)), proj("room", (2.85, BY + 5.94, 1.1))
    d = ImageDraw.Draw(img); n = len(lines)
    chars_shown = int((now - t0) * 28)
    for j, ln in enumerate(lines):
        if chars_shown <= 0: break
        txt = ln[:chars_shown]; chars_shown -= len(ln)
        yy = y0 + (y1 - y0) * (j + 0.6) / (n + 0.2)
        d.text(((x0 + x1) / 2, yy), txt, font=font(size), fill=(235, 238, 230), anchor="mm")

# ---------------- scenes ----------------
def s_hook(now, t, d0):
    img = still("engine"); d = ImageDraw.Draw(img)
    ex, ey = proj("engine", (-4.2, 3.2, 3.4))
    if t > 0.9:
        k = pop(now, 0.9, 0.25)
        d.ellipse([ex - 170 * k, ey - 110 * k, ex + 170 * k, ey + 110 * k], outline=(80, 230, 110), width=10)
        label(d, 540, 420, "ARMOR HERE?", int(84 * k), (80, 230, 110))
    guy(d, 200, 1980, 230, who="wald", eyes="glasses", brows="calm", mouth="flat", arm_r=35, arm_l=-70, look=1)
    guy(d, 900, 2000, 215, who="colonel", brows="angry", mouth="o", eyes="big", arm_l=-120, arm_r=-60, look=-1)
    return cam2d(img, 1.0 + 0.06 * t / d0, 0.5, 0.5)

def s_sky(now, t, d0):
    img = still("sky"); d = ImageDraw.Draw(img)
    flak(d, now)
    k = pop(now, T["1943"], 0.2)
    if k: stamp(img, "1943", now, T["1943"], 540, 380, 130, (240, 240, 230), -6)
    return cam2d(img, 1.0 + 0.08 * t / d0, 0.5, 0.5, shake=5 if (now * 0.8) % 1.0 < 0.1 else 1, t=now)

def s_armor(now, t, d0):
    img = still("apron"); d = ImageDraw.Draw(img)
    hands, (fx, fy, R) = put(d, "apron", 15.0, 20.5, 0.0, who="crew", brows="worried", mouth="open", eyes="big",
                             arm_l=90 + 6 * math.sin(now * 20), arm_r=90 - 6 * math.sin(now * 20), hop=-abs(math.sin(now * 5)) * 4)
    hx = (hands[0][0] + hands[1][0]) / 2; hy = min(hands[0][1], hands[1][1])
    d.rectangle([hx - 2.0 * R, hy - 1.1 * R, hx + 2.0 * R, hy], fill=(120, 122, 125), outline=BLACK, width=4)
    d.text((hx, hy - 0.55 * R), "ARMOR", font=font(0.55 * R), fill=BLACK, anchor="mm")
    for j in range(3):
        yy = fy - 3.0 * R + ((now * 200 + j * 40) % 90)
        d.ellipse([fx + 0.9 * R + j * 12, yy, fx + 1.1 * R + j * 12, yy + 0.3 * R], fill=(150, 200, 255))
    if now >= T["little"]:
        stamp(img, "TOO HEAVY", now, T["little"] + 0.2, 540, 420, 100, RED, -8)
    return cam2d(img, 1.15, 0.47, 0.6)

def s_plan(now, t, d0):
    img = still("room"); d = ImageDraw.Draw(img)
    chalk_board(img, ["COUNT THE HOLES", "WINGS  |||| ||||", "TAIL   |||| |||", "BODY   |||| ||||"], now, T["count"], 54)
    put(d, "room", -1.4, BY + 4.3, 0.0, who="colonel", brows="calm", mouth="smug", arm_r=40, arm_l=-70, look=1)
    put(d, "room", 1.7, BY + 4.0, 0.0, who="officer", brows="calm", mouth="flat", arm_r=-30, arm_l=-120, look=-1)
    return cam2d(img, 1.12 + 0.05 * t / d0, 0.5, 0.42)

def holes_scene(cam, kinds, now, t, d0, t0, txt, side=None, z=1.0, cy=0.5):
    img = still(cam); d = ImageDraw.Draw(img)
    pts = hole_pts(cam, kinds, side)
    ring_marks(d, pts, now, t0 + 0.2, 30, 0.05)
    counter(d, now, t0 + 0.2, len(pts) * 3 + 7, txt)
    return cam2d(img, z + 0.06 * t / d0, 0.5, cy)

def s_wing(now, t, d0): return holes_scene("wing", ("wing",), now, t, d0, T["wings"], "WINGS")
def s_tail(now, t, d0): return holes_scene("tail", ("tail",), now, t, d0, T["tail"], "TAIL")
def s_body(now, t, d0):
    img = holes_scene("body", ("body",), now, t, d0, T["body"], "BODY", side="+x")
    if now >= T["swiss"]:
        d = ImageDraw.Draw(img); k = pop(now, T["swiss"], 0.2)
        x, y, r = 560, 330, 110 * k        # cheese wedge icon
        d.polygon([(x - r, y + r * 0.5), (x + r, y + r * 0.5), (x + r * 0.2, y - r * 0.6)], fill=(250, 210, 70), outline=BLACK)
        for (a, b) in ((-0.3, 0.2), (0.3, 0.25), (0.05, -0.1)): d.ellipse([x + a * r - 12 * k, y + b * r - 12 * k, x + a * r + 12 * k, y + b * r + 12 * k], fill=(200, 150, 30))
    return img

def s_engine(now, t, d0):
    img = still("engine"); d = ImageDraw.Draw(img)
    ex, ey = proj("engine", (-4.2, 3.2, 3.4))
    pts = hole_pts("engine", ("wing", "body"))
    for x, y in pts: d.ellipse([x - 22, y - 22, x + 22, y + 22], outline=(255, 60, 50), width=5)
    if now >= T["almost"]:
        k = pop(now, T["almost"], 0.25)
        d.ellipse([ex - 190 * k, ey - 120 * k, ex + 190 * k, ey + 120 * k], outline=(80, 230, 110), width=10)
        label(d, 540, 430, "ENGINES: 0", 92, (80, 230, 110))
    return cam2d(img, 1.0 + 0.15 * ease(t / d0), 0.45, 0.45)

def s_wald(now, t, d0):
    img = still("room", 6); d = ImageDraw.Draw(img)
    lg = now >= T["laughs"]; say = T["armeng"] <= now < T["laughs"] + 0.2
    guy(d, 300, 1760, 210, who="wald", eyes="glasses", brows="calm", mouth="open" if say and int(now * 8) % 2 else "flat",
        arm_r=70 if say else -60, arm_l=-70, look=1)
    guy(d, 790, 1790 - (abs(math.sin(now * 14)) * 30 if lg else 0), 225, who="colonel", mouth="laugh" if lg else "flat",
        eyes="closed" if lg else "dot", brows="up", arm_l=-110 if not lg else 60, arm_r=-70 if not lg else 120, look=-1)
    if now >= T["armeng"]: label(d, 330, 820, "ARMOR THE", 64, (80, 230, 110)); label(d, 330, 900, "ENGINES", 80, (80, 230, 110))
    if lg:
        for k in range(3): label(d, 790 + 170 * math.cos(k * 2.1 + now * 2), 700 + 60 * k + 15 * math.sin(now * 9 + k), "HA", 72, WHITE)
    return cam2d(img, 1.0, 0.5, 0.5, shake=4 if lg else 0, t=now)

def s_blind(now, t, d0):
    img = still("room", 11); d = ImageDraw.Draw(img)
    guy(d, 560, 2480, 430, who="colonel", mouth="open" if int(now * 7) % 2 else "frown", brows="angry", eyes="big",
        arm_l=-100, arm_r=60 + 15 * math.sin(now * 12), look=-0.3)
    return cam2d(img, 1.0 + 0.08 * t / d0, 0.5, 0.5, shake=7, t=now)

def s_question(now, t, d0):
    img = still("room"); d = ImageDraw.Draw(img)
    chalk_board(img, ["WHERE ARE THE", "PLANES THAT", "DIDN'T COME", "BACK?"], now, T["where"], 70)
    sil = now >= T["silence"]
    put(d, "room", -1.9, BY + 4.6, 0.0, who="wald", eyes="glasses", brows="calm", mouth="flat", arm_r=75, arm_l=-70, look=1)
    put(d, "room", 0.9, BY - 0.4, 0.0, who="colonel", brows="up" if sil else "angry", mouth="o" if sil else "frown", eyes="big" if sil else "dot",
        arm_l=-80, arm_r=-100, look=-1)
    put(d, "room", 2.2, BY + 0.2, 0.0, who="officer", brows="up" if sil else "calm", mouth="o" if sil else "flat", eyes="big" if sil else "dot", look=-1)
    if sil:
        k = pop(now, T["silence"] + 0.2, 0.3)
        label(d, 830, 700, "...", int(110 * k), WHITE)
    return cam2d(img, 1.1, 0.5, 0.45)

def s_limp(now, t, d0):
    img = still("top"); d = ImageDraw.Draw(img)
    red_dots(d, hole_pts("top", ("wing",), up_only=True), now, T["limped"] + 0.1, 13, 0.008)
    if now >= T["limped"] + 1.2:
        k = pop(now, T["limped"] + 1.2, 0.25)
        label(d, 540, 380, "MADE IT HOME", int(80 * k), (80, 230, 110))
    return cam2d(img, 1.15, 0.5, 0.48)

def s_never(now, t, d0):
    img = still("skyempty"); d = ImageDraw.Draw(img)
    # a bomber silhouette falling with a smoke trail from an engine
    u = clamp(t / 1.6)
    bx, by = lerp(380, 820, u), lerp(250, 1350, u ** 1.4)
    trail = [(lerp(380, 820, v), lerp(250, 1350, v ** 1.4) - 40) for v in [u * j / 14 for j in range(15)]]
    smoke(d, trail, now)
    ang = -30 - 50 * u
    sil = Image.new("RGBA", (360, 360), (0, 0, 0, 0)); sd = ImageDraw.Draw(sil)
    if t > 1.55: sil = None
    sd.ellipse([150, 40, 210, 330], fill=(30, 32, 28)); sd.polygon([(20, 170), (340, 170), (330, 205), (30, 205)], fill=(30, 32, 28))
    sd.polygon([(120, 300), (240, 300), (230, 320), (130, 320)], fill=(30, 32, 28))
    if sil is not None:
        sd.ellipse([150, 40, 210, 330], fill=(30, 32, 28)); sd.polygon([(20, 170), (340, 170), (330, 205), (30, 205)], fill=(30, 32, 28))
        sd.polygon([(120, 300), (240, 300), (230, 320), (130, 320)], fill=(30, 32, 28))
        sil = sil.rotate(ang, expand=False); img.paste(sil, (int(bx - 180), int(by - 180)), sil)
    if t > 1.5:
        k = pop(now, T["nevermade"] + 1.5, 0.15)
        for rr_, col in ((230, (90, 80, 70)), (200, (255, 120, 40)), (140, (255, 190, 70)), (70, (255, 245, 200))):
            rr_ *= k * (1 + 0.3 * clamp(t - 1.5)); d.ellipse([820 - rr_, 1380 - rr_ * 0.7, 820 + rr_, 1380 + rr_ * 0.7], fill=col)
        stamp(img, "NEVER CAME BACK", now, T["nevermade"] + 1.6, 540, 450, 80, RED, -6)
    return cam2d(img, 1.0, 0.5, 0.5, shake=8 if 1.5 < t < 1.9 else 0, t=now)

def s_map(now, t, d0):
    img = still("top"); d = ImageDraw.Draw(img)
    red_dots(d, hole_pts("top", ("wing", "tail", "body"), up_only=True), now, -10, 13)
    if now >= T["survive"] - 0.6:
        k = pop(now, T["survive"] - 0.6, 0.3)
        label(d, 540, 330, "SURVIVABLE HITS", int(70 * k), (255, 90, 80))
    if now >= T["missing"]:
        k = pop(now, T["missing"], 0.3)
        for ex in (-8.6, -4.2, 4.2, 8.6):
            px, py = proj("top", (ex, 3.4, 3.2))
            g = 0.6 + 0.4 * abs(math.sin(now * 5))
            d.ellipse([px - 75 * k, py - 120 * k, px + 75 * k, py + 120 * k], outline=(int(80 * g), int(230 * g), int(110 * g)), width=12)
        label(d, 540, 1560, "ARMOR HERE", int(96 * k), (80, 230, 110))
    return cam2d(img, 1.12 if now < T["missing"] else lerp(1.12, 1.3, ease((now - T["missing"]) / 1.5)), 0.5, 0.48)

def s_bias(now, t, d0):
    img = still("front"); d = ImageDraw.Draw(img)
    put(d, "front", -3.5, 18.0, 0.0, who="wald", eyes="glasses", brows="calm", mouth="smile", arm_r=-40, arm_l=-110)
    put(d, "front", -5.0, 19.5, 0.0, who="colonel", brows="worried", mouth="frown", arm_r=-80, arm_l=-100, look=1)
    k = pop(now, T["bias"] - 0.2, 0.25)
    if k:
        label(d, 540, 360, "SURVIVORSHIP", int(92 * k), (255, 220, 60)); label(d, 540, 470, "BIAS", int(130 * k), (255, 220, 60))
    return cam2d(img, 1.05 + 0.05 * t / d0, 0.5, 0.5)

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
def drone(d, g=0.05):
    x = tt(d); fade = np.minimum(1, np.minimum(x / 0.3, (d - x) / 0.3))
    return (np.sin(2 * np.pi * 62 * x + 0.3 * np.sin(2 * np.pi * 9 * x)) + 0.6 * np.sin(2 * np.pi * 93 * x) + 0.3 * lowpass(noise(d), 30)) * fade * g
def boom(g=0.8): return lowpass(noise(0.6), 25) * env(0.6, 0.003, 0.5) * g
# military snare bed until the reveal
beat = 60 / 108
for k, b in enumerate(np.arange(0.2, T["sowhen"], beat / 2)):
    if k % 4 in (0, 3) or k % 8 == 6: add(lowpass(noise(0.08), 3) * env(0.08) * (0.05 if k % 4 else 0.08), b)
for k, b in enumerate(np.arange(0.2, T["sowhen"], beat * 2)): add(np.sin(2 * np.pi * 55 * tt(0.4)) * env(0.4) * 0.12, b)
for a_, b_ in [("yousee", "armor"), ("limped", "holes")]: add(drone(T[b_] - T[a_]), T[a_])
for k in range(8): add(boom(0.5), T["yousee"] + 0.4 + k * (T["armor"] - T["yousee"]) / 8)
for key in ("wings", "tail", "body"):
    for k in range(18): add(np.sin(2 * np.pi * 1500 * tt(0.03)) * env(0.03) * 0.05, T[key] + 0.25 + k * 0.025 * 2)
# crickets for clean engines and silence
def crickets(d):
    x = tt(d); return np.sin(2 * np.pi * 4300 * x) * (np.sin(2 * np.pi * 18 * x) > 0.6) * (np.sin(2 * np.pi * 1.5 * x) > 0) * 0.04
add(crickets(T["sowhen"] - T["almost"]), T["almost"]); add(crickets(T["limped"] - T["silence"]), T["silence"])
add(lowpass(noise(0.12), 8) * env(0.12) * 0.9, T["1943"]); add(lowpass(noise(0.12), 8) * env(0.12) * 0.8, T["little"] + 0.2)
for k in range(3): add(np.sin(2 * np.pi * (300 - 80 * k) * tt(0.12)) * env(0.12, 0.005, 0.2) * 0.12, T["laughs"] + 0.1 + k * 0.18)
for k in range(30): add(lowpass(noise(0.03), 2) * env(0.03) * 0.04, T["where"] + k * 0.05)        # chalk scratches
sw = np.sin(2 * np.pi * (900 - 600 * tt(1.5)) * tt(1.5)) * env(1.5, 0.05, 2.0) * 0.08; add(sw, T["nevermade"])  # falling whistle
add(boom(1.0), T["nevermade"] + 1.5)
add(ding(1320, 1.0, 0.1), T["missing"]); add(ding(1760, 1.0, 0.08), T["missing"] + 0.15); add(ding(2640, 1.2, 0.07), T["bias"])

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
