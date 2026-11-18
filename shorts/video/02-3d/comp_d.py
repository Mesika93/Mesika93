"""The Great Diamond Hoax: 2D characters over Blender plates.
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
WORDS = data["words"]; DUR = data["dur"] + 0.25
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())
NW = [norm(w["w"]) for w in WORDS]
def find(phrase, after=0):
    p = [norm(x) for x in phrase.split()]
    for i in range(after, len(NW)):
        if NW[i:i + len(p)] == p: return i
    raise SystemExit("not found: " + phrase)
def wt(phrase, after=0): return WORDS[find(phrase, after)]["s"]
T = {"he": 0.0}
for k, ph in [("while", "while millionaires"), ("yousee", "you see"), ("sack", "with a sack"), ("tiffany", "tiffany's"),
              ("real", "real"), ("famous", "a famous"), ("everywhere", "diamonds everywhere"), ("bankers", "bankers poured"),
              ("sowhen", "so when"), ("laughs", "laughs"), ("son", "son"), ("but", "but clarence"), ("andhe", "and he finds"),
              ("pushed", "pushed into"), ("stick", "stick hole"), ("rubies", "rubies"), ("sapph", "sapphires"), ("emer", "emeralds"),
              ("nature", "nature never"), ("then", "then he picks"), ("marks", "marks from"), ("salted", "the field was"),
              ("king", "king sends"), ("telegram", "telegram"), ("dust", "turn to dust"), ("realg", "real gems"), ("fake", "fake ones")]:
    T[k] = wt(ph)
T["end"] = WORDS[-1]["e"]
SCENES = [("he", "s_hook"), ("while", "s_rich"), ("yousee", "s_prosp"), ("sack", "s_sack"), ("tiffany", "s_tiffany"),
          ("famous", "s_expert"), ("bankers", "s_money"), ("sowhen", "s_ask"), ("son", "s_son"), ("but", "s_goes"),
          ("andhe", "s_finds"), ("pushed", "s_macro"), ("rubies", "s_gems"), ("then", "s_cut"), ("salted", "s_salted"),
          ("king", "s_telegram"), ("dust", "s_dust"), ("realg", "s_diagram")]
STARTS = [T[k] for k, _ in SCENES] + [DUR]

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
         "jeweler": (90, 40, 60), "expert": (60, 75, 60), "rich1": (40, 40, 50), "rich2": (70, 40, 40)}
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
    if who in ("banker", "expert", "king", "rich1"):
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

# ---------------- scenes (draw in plate space 1080x1920) ----------------
BY = 1000.0; DY = BY + 2.0
def s_hook(now, t, d0):
    img = still("anthill"); d = ImageDraw.Draw(img)
    poke = math.sin(now * 9) * 6
    put(d, "anthill", -1.25, 1.5, 0.0, crouch=True, arm_r=-35 + poke, arm_l=-60, brows="raised", mouth="flat", who="king", prop="stick", look=1)
    return cam2d(img, 1.0 + 0.06 * t / d0, 0.45, 0.55)

def s_rich(now, t, d0):
    img = still("wide"); d = ImageDraw.Draw(img)
    for k, (x, y, who) in enumerate([(-1.6, 1.0, "rich1"), (-0.2, 1.8, "rich2"), (1.2, 0.8, "rich1"), (2.5, 2.2, "banker")]):
        put(d, "wide", x, y, 0.0, who=who, arm_r=50 + 20 * math.sin(now * 6 + k), arm_l=130, mouth="laugh", eyes="closed",
            hop=abs(math.sin(now * 7 + k)) * 10, prop="diamond" if k % 2 == 0 else None)
    pts = [proj("wide", (x, y, 0.05)) for x, y in [(-2, -1), (-1, 0), (0.5, -1.5), (2, -0.5), (3, 0.5), (-2.5, 1), (0.6, 3)]]
    glints(d, pts, now, 22)
    return cam2d(img, 1.1 + 0.1 * t / d0, 0.5, 0.55)

def s_prosp(now, t, d0):
    img = still("bank"); d = ImageDraw.Draw(img)
    put(d, "bank", 0.3, DY + 0.95, 0.0, who="banker", arm_l=-60, arm_r=-120, brows="up", mouth="o", eyes="big" if t > 1.5 else "dot")
    walk_x = lerp(-0.7, 0.0, ease(t / d0))
    for k, (dx, who) in enumerate([(0, "prosp1"), (0.9, "prosp2")]):
        put(d, "bank", walk_x - dx * 0.75, BY + 0.5 - dx * 0.6, 0.0, who=who, walk=now * 7 + k, brows="calm", mouth="smile" if k else "flat",
            hop=abs(math.sin(now * 7 + k)) * 6, arm_r=-110 + 20 * math.sin(now * 7), look=1)
    return cam2d(img, 1.12, 0.5, 0.58)

def s_sack(now, t, d0):
    img = still("sack"); d = ImageDraw.Draw(img)
    glints(d, [(700, 980), (860, 1060), (760, 1180), (920, 900), (640, 1100), (980, 1150), (820, 1300)], now, 40)
    return cam2d(img, 1.12 + 0.12 * t / d0, 0.72, 0.56)

def s_tiffany(now, t, d0):
    img = still("velvet", 3 if now < T["real"] else 6); d = ImageDraw.Draw(img)
    glints(d, [(560, 1050), (760, 1090), (880, 1000), (350, 980)], now, 34)
    jx = lerp(1300, 820, ease(t / 0.4))
    guy(d, jx, 2120, 300, who="jeweler", eyes="loupe", brows="up" if now < T["real"] else "calm",
        mouth="flat" if now < T["real"] else "smile", arm_l=-40, arm_r=-140, look=-1)
    if now >= T["real"]:
        stamp(img, "REAL", now, T["real"], 470, 560, 150, (40, 160, 70), -10)
    return cam2d(img, 1.0, 0.5, 0.5)

def s_expert(now, t, d0):
    img = still("field"); d = ImageDraw.Draw(img)
    ev = now >= T["everywhere"]
    put(d, "field", 2.3, 1.0, 0.0, who="expert", brows="up", mouth="open" if ev else "smile", eyes="big" if ev else "dot",
        arm_l=140 if ev else -40, arm_r=40 if ev else -150, prop=None if ev else "bag", hop=abs(math.sin(now * 8)) * 10 if ev else 0)
    rr = random.Random(4); pts = []
    for k in range(40 if ev else 6):
        pts.append(proj("field", (rr.uniform(-2, 6), rr.uniform(-2.5, 6), 0.02)))
    glints(d, pts, now, 30)
    return cam2d(img, 1.05 + 0.05 * t / d0, 0.5, 0.55)

def s_money(now, t, d0):
    img = still("money"); d = ImageDraw.Draw(img)
    glints(d, [(300, 1100), (520, 1000), (700, 1150), (850, 1050), (430, 1250), (640, 1320)], now, 36)
    k = pop(now, T["bankers"] + 0.6, 0.25)
    if k > 0: label(d, 540, 520, "$10,000,000", int(110 * (0.6 + 0.4 * k)), (120, 230, 120))
    return cam2d(img, 1.0 + 0.1 * t / d0, 0.5, 0.55)

def s_ask(now, t, d0):
    img = still("bank", 6); d = ImageDraw.Draw(img)
    lg = now >= T["laughs"]
    guy(d, 330, 1720, 200, who="king", arm_l=-50, arm_r=-30 if now < T["laughs"] else -130, brows="calm" if not lg else "worried", mouth="flat", look=1)
    guy(d, 760, 1760 - (abs(math.sin(now * 14)) * 30 if lg else 0), 215, who="banker", mouth="laugh" if lg else "smug",
        eyes="closed" if lg else "dot", brows="up", arm_l=-110 if not lg else 60, arm_r=-70 if not lg else 120, look=-1)
    if lg:
        for k in range(3):
            label(d, 760 + 170 * math.cos(k * 2.1 + now * 2), 760 + 60 * k + 15 * math.sin(now * 9 + k), "HA", 70, WHITE)
    return cam2d(img, 1.0, 0.5, 0.5, shake=4 if lg else 0, t=now)

def s_son(now, t, d0):
    img = still("bank", 10); d = ImageDraw.Draw(img)
    guy(d, 560, 2500, 420, who="banker", mouth="smug" if int(now * 6) % 2 else "open", brows="up", eyes="closed",
        arm_l=-100, arm_r=75 + 8 * math.sin(now * 10), look=-0.5)
    return cam2d(img, 1.0 + 0.08 * t / d0, 0.5, 0.5)

def s_goes(now, t, d0):
    img = still("trail"); d = ImageDraw.Draw(img)
    x = lerp(-24.6, -22.6, t / d0)
    put(d, "trail", x, -4.0, 0.0, who="king", walk=now * 6, arm_l=-80 + 20 * math.sin(now * 6), brows="angry", mouth="flat",
        prop="walkstick", hop=abs(math.sin(now * 6)) * 6, look=1)
    return cam2d(img, 1.05, 0.5, 0.55)

def s_finds(now, t, d0):
    img = still("field"); d = ImageDraw.Draw(img)
    put(d, "field", 2.8, 0.5, 0.0, who="king", crouch=True, brows="raised", mouth="o" if now > T["andhe"] + 1.3 else "flat",
        arm_r=-40, arm_l=-80, prop="diamond", look=1)
    k = pop(now, T["andhe"] + 1.6)
    if k: label(d, 690, 760, "?", int(160 * k), (255, 220, 60))
    return cam2d(img, 1.1 + 0.08 * t / d0, 0.55, 0.55)

def s_macro(now, t, d0):
    img = still("antmacro"); d = ImageDraw.Draw(img)
    az = lambda x, y: 0.32 * (1 - min(1, math.hypot(x, y) / 0.75) ** 1.6)
    dx, dy = proj("antmacro", (0.13, -0.17, az(0.13, -0.17) + 0.03)); hx, hy = proj("antmacro", (0.2, -0.12, az(0.2, -0.12)))
    glints(d, [(dx - 30, dy - 50)], now, 50)
    if now >= T["stick"]:
        k = pop(now, T["stick"], 0.25)
        d.ellipse([hx - 90 * k, hy - 60 * k, hx + 90 * k, hy + 60 * k], outline=(255, 220, 60), width=10)
        arrow(d, hx - 120, hy - 380, hx - 20, hy - 80)
        label(d, clamp(hx - 120, 250, 830), hy - 440, "STICK HOLE", 64, (255, 220, 60))
    return cam2d(img, 1.0 + 0.15 * t / d0, 0.5, 0.5)

def s_gems(now, t, d0):
    img = still("gems"); d = ImageDraw.Draw(img)
    GX, GY, GZ = 30.0, 4.0, 0.06
    items = [("RUBY", T["rubies"], (GX + 0.07, GY + 0.05), (220, 40, 50)), ("SAPPHIRE", T["sapph"], (GX - 0.06, GY + 0.04), (70, 120, 255)),
             ("EMERALD", T["emer"], (GX + 0.04, GY - 0.07), (40, 210, 100))]
    bad = now >= T["nature"]
    for k, (name, t0, (x, y), col) in enumerate(items):
        if now < t0: continue
        px, py = proj("gems", (x, y, GZ)); kk = pop(now, t0)
        lx, ly = clamp(px + (-200 if k == 1 else 200), 230, 850), clamp(py - 320 + 60 * k, 300, 1500)
        if bad: lx += 6 * math.sin(now * 40 + k)
        if not (0 < px < PW and 0 < py < PH): continue
        arrow(d, lx, ly + 40, px, py - 30, col=col, w=8)
        label(d, lx, ly, name, int(58 * kk), RED if bad else col)
    if bad:
        stamp(img, "NOT NATURAL", now, T["nature"] + 0.4, 540, 1500, 90, RED, 8)
    return cam2d(img, 1.0 + 0.08 * t / d0, 0.5, 0.5)

def s_cut(now, t, d0):
    img = still("cut"); d = ImageDraw.Draw(img)
    glints(d, [(400, 820), (720, 1000), (560, 1180)], now, 50)
    if now >= T["marks"]:
        k = pop(now, T["marks"], 0.25)
        for (x, y) in [(470, 900), (690, 860)]:
            d.ellipse([x - 110 * k, y - 110 * k, x + 110 * k, y + 110 * k], outline=(255, 220, 60), width=10)
        label(d, 540, 520, "CUT BY A", 70, (255, 220, 60)); label(d, 540, 610, "JEWELER", 90, (255, 220, 60))
    return cam2d(img, 1.0 + 0.1 * t / d0, 0.5, 0.5)

def s_salted(now, t, d0):
    img = still("field"); d = ImageDraw.Draw(img)
    # giant salt shaker sprinkling diamonds from the sky
    sx, sy = 640 + 30 * math.sin(now * 12), 470 + 20 * math.sin(now * 20)
    d.rounded_rectangle([sx - 130, sy - 260, sx + 130, sy + 120], radius=60, fill=(235, 240, 245), outline=BLACK, width=8)
    d.chord([sx - 130, sy + 30, sx + 130, sy + 230], 0, 180, fill=(170, 175, 185), outline=BLACK, width=8)
    for k in range(5): d.ellipse([sx - 70 + k * 30, sy + 150, sx - 58 + k * 30, sy + 162], fill=BLACK)
    rr = random.Random(9)
    for k in range(40):
        ph = (now * 1.4 + rr.random()) % 1.0
        x = sx + rr.uniform(-140, 140) * (0.3 + ph); y = sy + 220 + ph * 1300
        sparkle(d, x, y, 22, 1.0)
    put(d, "field", 1.0, -0.5, 0.0, who="king", brows="angry", mouth="flat", arm_r=50, arm_l=-60, look=1)
    stamp(img, "SALTED", now, T["salted"] + 0.6, 540, 1250, 150, RED, -14)
    return cam2d(img, 1.0, 0.5, 0.5, shake=6 if now > T["salted"] + 0.6 and now < T["salted"] + 0.9 else 0, t=now)

def s_telegram(now, t, d0):
    img = still("bank", 8); d = ImageDraw.Draw(img)
    pale = clamp((now - T["telegram"] - 0.4) / 0.8)
    face = tuple(int(lerp(a, b, pale)) for a, b in zip(WHITE, (175, 215, 165)))
    guy(d, 540, 2250, 380, who="banker", face=face, eyes="big" if pale > 0.3 else "dot", brows="worried" if pale > 0.3 else "calm",
        mouth="o" if pale > 0.3 else "flat", arm_l=-20, arm_r=-160, prop="telegram")
    # telegram text overlay
    k = pop(now, T["telegram"], 0.3)
    if k:
        x0, y0 = 220, 330
        d.rectangle([x0, y0, x0 + 640, y0 + 420], fill=(240, 230, 200), outline=BLACK, width=6)
        d.text((x0 + 320, y0 + 60), "WESTERN UNION", font=font(40, True), fill=(60, 50, 40), anchor="mm")
        for j, line in enumerate(["DIAMOND FIELD", "IS A FRAUD STOP", "IT WAS SALTED", "-- C. KING"]):
            d.text((x0 + 320, y0 + 140 + 70 * j), line, font=font(48), fill=BLACK, anchor="mm")
    if pale > 0.3:
        for j in range(3):
            yy = 1500 + ((now * 300 + j * 90) % 200)
            d.ellipse([360 + j * 150, yy, 385 + j * 150, yy + 40], fill=(150, 200, 255))
    return cam2d(img, 1.0, 0.5, 0.5)

def s_dust(now, t, d0):
    img = still("money"); k = clamp(t / 1.2)
    g = img.convert("L").convert("RGB"); img = Image.blend(img, g, k * 0.85)
    img = Image.blend(img, Image.new("RGB", img.size, (60, 50, 40)), k * 0.35)
    d = ImageDraw.Draw(img); rr = random.Random(2)
    for j in range(260):
        x0 = rr.uniform(150, 950); y0 = rr.uniform(900, 1400); dl = rr.uniform(0, 0.6)
        tt = max(0, t - dl)
        x = x0 + tt * rr.uniform(300, 900); y = y0 - tt * rr.uniform(100, 500) + 80 * tt * tt
        r = rr.uniform(3, 9)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(200, 175, 120) if j % 3 else (150, 140, 120))
    return cam2d(img, 1.0 + 0.05 * t / d0, 0.5, 0.55)

def s_diagram(now, t, d0):
    img = Image.new("RGB", (PW, PH), (120, 185, 230)); d = ImageDraw.Draw(img)
    GY = 760
    d.rectangle([0, GY, PW, PH], fill=(170, 120, 75))
    for k, c in enumerate([(150, 105, 65), (125, 88, 58), (100, 72, 52), (75, 58, 48)]):
        d.rectangle([0, GY + 180 + 230 * k, PW, PH], fill=c)
    # kimberlite pipe
    d.polygon([(470, GY), (610, GY), (575, PH), (505, PH)], fill=(60, 75, 90))
    for k in range(4):
        y = 1300 + k * 140; sparkle(d, 540 + (k % 2) * 20 - 10, y, 36, 0.6 + 0.4 * abs(math.sin(now * 3 + k)))
    rk = pop(now, T["realg"] + 0.3, 0.3)
    if rk:
        label(d, 820, 1660, "REAL", int(110 * rk), (120, 230, 140)); label(d, 820, 1770, "deep in rock", int(62 * rk), WHITE)
    # fake: lying on surface, right where you look
    fk = pop(now, T["fake"], 0.25)
    if fk:
        for k, x in enumerate((180, 260, 340, 790, 880)):
            sparkle(d, x, GY - 22, 34 * fk, 0.7 + 0.3 * abs(math.sin(now * 4 + k)))
        label(d, 280, 560, "FAKE", int(110 * fk), RED); label(d, 280, 665, "on the surface", int(56 * fk), WHITE)
        guy(d, 870, GY - 2, 70, who="banker", eyes="big", mouth="smile", arm_l=-40, arm_r=40, brows="up", look=-1)
    d.text((PW // 2, 300), "WHERE DIAMONDS HIDE", font=font(72, True), fill=(30, 40, 60), anchor="mm")
    return cam2d(img, 1.0, 0.5, 0.5)

FN = {n: globals()[n] for _, n in SCENES}

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
# western-ish bed: plucked bass + shaker until the reveal
x = np.arange(N) / SR; bed = np.zeros(N); beat = 60 / 100
notes = [110, 110, 146.8, 130.8, 110, 98, 110, 82.4]
for k, b in enumerate(np.arange(0.2, T["salted"], beat)):
    s = int(b * SR); n = ding(notes[k % 8], 0.45, 0.07); bed[s:s + len(n)] += n[:max(0, min(len(n), N - s))]
    sh = lowpass(noise(0.06), 3) * env(0.06) * 0.03; s2 = int((b + beat / 2) * SR); bed[s2:s2 + len(sh)] += sh[:max(0, min(len(sh), N - s2))]
mix += bed
for tm in (T["sack"] + 0.3, T["everywhere"], T["everywhere"] + 0.25, T["bankers"] + 0.6, T["stick"], T["marks"]):
    add(ding(1760, 0.5, 0.06), tm); add(ding(2637, 0.4, 0.04), tm)
add(lowpass(noise(0.12), 8) * env(0.12) * 0.9, T["real"])                    # stamp thunk
add(lowpass(noise(0.15), 8) * env(0.15) * 1.0, T["salted"] + 0.6)
add(lowpass(noise(0.12), 8) * env(0.12) * 0.7, T["nature"] + 0.4)
for k in range(3): add(np.sin(2 * np.pi * (300 - 80 * k) * tt(0.12)) * env(0.12, 0.005, 0.2) * 0.12, T["laughs"] + 0.1 + k * 0.18)
for k in range(10): add(np.sign(np.sin(2 * np.pi * 900 * tt(0.08 if k % 3 else 0.2))) * 0.03, T["telegram"] + 0.05 + k * 0.12)  # telegraph clicks
add(lowpass(noise(2.0), 30) * np.sin(np.pi * tt(2.0) / 2.0) * 0.5, T["dust"])                    # whoosh
sw = np.sin(2 * np.pi * (600 - 250 * tt(1.0)) * tt(1.0)) * env(1.0, 0.01, 1.2) * 0.08; add(sw, T["salted"] + 0.1)  # sad slide
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
