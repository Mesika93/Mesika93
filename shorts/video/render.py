import json, math, random, subprocess, sys, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

R1 = sys.argv[1]; OUT = sys.argv[2]
PREVIEW = len(sys.argv) > 3
W, H, FPS = 720, 1280, 30
data = json.load(open(f"{R1}/words.json"))
WORDS = data["words"]; DUR = data["dur"] + 0.6
norm = lambda s: re.sub(r"[^a-z0-9']", "", s.lower())
NW = [norm(w["w"]) for w in WORDS]

def find(phrase, after=0):
    p = [norm(x) for x in phrase.split()]
    for i in range(after, len(NW)):
        if NW[i:i+len(p)] == p: return i
    raise SystemExit("not found: " + phrase)

def wt(phrase, after=0):
    return WORDS[find(phrase, after)]["s"]

FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 76)
FONT_S = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 56)
FONT_XS = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 26)

BLACK = (20, 20, 20); WHITE = (250, 250, 248)
RED = (190, 30, 40); GOLD = (220, 180, 60)

def lerp(a, b, t): return a + (b - a) * t
def lerpc(a, b, t): return tuple(int(lerp(x, y, t)) for x, y in zip(a, b))
def clamp(x, a=0, b=1): return max(a, min(b, x))
def ease(t): t = clamp(t); return t * t * (3 - 2 * t)

# ---------------- character ----------------
def person(d, x, y, R, outfit="soldier", walk=0.0, arm_l=-60, arm_r=-120, brows="calm",
           mouth="flat", face=WHITE, flip=False, hop=0.0, musket=False):
    y = y - hop
    lw = max(2, int(R * 0.09))
    hip = y - 1.35 * R; neck = y - 2.35 * R; hc = y - 3.15 * R
    sw = math.sin(walk) * 0.38 * R
    for s in (1, -1):
        d.line([(x + s * 0.18 * R, hip), (x + s * 0.18 * R + s * sw, y)], fill=BLACK, width=lw)
        d.ellipse([x + s * 0.18 * R + s * sw - 0.16 * R, y - 0.08 * R, x + s * 0.18 * R + s * sw + 0.2 * R, y + 0.08 * R], fill=BLACK)
    col = {"soldier": RED, "general": (40, 50, 110), "civ1": (70, 110, 70), "civ2": (130, 90, 60),
           "civ3": (120, 60, 120), "civ4": (60, 90, 140)}.get(outfit, RED)
    tw = 0.5 * R
    shoulder = neck + 0.15 * R
    for ang, sx in ((arm_l, -1), (arm_r, 1)):
        a = math.radians(ang)
        ex = x + sx * tw * 0.9 + math.cos(a) * 1.0 * R * (1 if sx > 0 else 1)
        ey = shoulder - math.sin(a) * 1.0 * R
        d.line([(x + sx * tw * 0.9, shoulder), (ex, ey)], fill=BLACK, width=lw)
        d.ellipse([ex - 0.09 * R, ey - 0.09 * R, ex + 0.09 * R, ey + 0.09 * R], fill=WHITE, outline=BLACK, width=max(1, lw // 2))
        if musket and sx > 0:
            d.line([(ex - 0.1 * R, ey + 0.4 * R), (ex + 0.15 * R, ey - 1.6 * R)], fill=(90, 60, 30), width=lw + 2)
    d.rounded_rectangle([x - tw, neck, x + tw, hip + 0.05 * R], radius=int(0.15 * R), fill=col, outline=BLACK, width=lw)
    if outfit == "soldier":
        d.line([(x - tw + 3, neck + 4), (x + tw - 3, hip - 4)], fill=WHITE, width=lw + 1)
        d.line([(x + tw - 3, neck + 4), (x - tw + 3, hip - 4)], fill=WHITE, width=lw + 1)
    if outfit == "general":
        for s in (-1, 1):
            d.rectangle([x + s * tw - 0.18 * R, neck - 0.05 * R, x + s * tw + 0.18 * R, neck + 0.12 * R], fill=GOLD, outline=BLACK)
        for k in range(3):
            d.ellipse([x - 0.3 * R + k * 0.18 * R, neck + 0.35 * R, x - 0.18 * R + k * 0.18 * R, neck + 0.5 * R], fill=GOLD)
    # head
    hr = 0.82 * R
    d.ellipse([x - hr, hc - hr, x + hr, hc + hr], fill=face, outline=BLACK, width=lw)
    if outfit == "general":
        for s in (-1, 1):
            d.chord([x + s * hr * 0.98 - 0.25 * R, hc - 0.1 * R, x + s * hr * 0.98 + 0.25 * R, hc + 0.6 * R], 0, 360, fill=(150, 150, 150), outline=BLACK)
    f = -1 if flip else 1
    ex1, ex2 = x - 0.28 * R + f * 0.08 * R, x + 0.28 * R + f * 0.08 * R
    ey = hc - 0.05 * R
    for exx in (ex1, ex2):
        d.ellipse([exx - 0.07 * R, ey - 0.07 * R, exx + 0.07 * R, ey + 0.07 * R], fill=BLACK)
    by = ey - 0.25 * R
    for exx, s in ((ex1, -1), (ex2, 1)):
        if brows == "angry": d.line([(exx - s * 0.15 * R, by - 0.08 * R), (exx + s * 0.15 * R, by + 0.06 * R)], fill=BLACK, width=lw)
        elif brows == "worried": d.line([(exx - s * 0.15 * R, by + 0.06 * R), (exx + s * 0.15 * R, by - 0.08 * R)], fill=BLACK, width=lw)
        elif brows == "calm": d.line([(exx - 0.14 * R, by), (exx + 0.14 * R, by)], fill=BLACK, width=lw)
    my = hc + 0.38 * R; mx = x + f * 0.06 * R
    if mouth == "flat": d.line([(mx - 0.18 * R, my), (mx + 0.18 * R, my)], fill=BLACK, width=lw)
    elif mouth == "smile": d.arc([mx - 0.25 * R, my - 0.2 * R, mx + 0.25 * R, my + 0.12 * R], 20, 160, fill=BLACK, width=lw)
    elif mouth == "open": d.ellipse([mx - 0.17 * R, my - 0.12 * R, mx + 0.17 * R, my + 0.2 * R], fill=(120, 20, 30), outline=BLACK, width=lw)
    elif mouth == "shout": d.ellipse([mx - 0.24 * R, my - 0.15 * R, mx + 0.24 * R, my + 0.3 * R], fill=(120, 20, 30), outline=BLACK, width=lw)
    elif mouth == "frown": d.arc([mx - 0.22 * R, my, mx + 0.22 * R, my + 0.3 * R], 200, 340, fill=BLACK, width=lw)
    top = hc - hr
    if outfit == "soldier":
        d.polygon([(x - 0.5 * R, top + 0.2 * R), (x + 0.5 * R, top + 0.2 * R), (x + 0.42 * R, top - 0.7 * R), (x - 0.42 * R, top - 0.7 * R)], fill=BLACK)
        d.rectangle([x - 0.5 * R, top + 0.08 * R, x + 0.5 * R, top + 0.2 * R], fill=GOLD)
        d.ellipse([x - 0.12 * R, top - 0.95 * R, x + 0.12 * R, top - 0.7 * R], fill=WHITE, outline=BLACK)
    elif outfit == "general":
        d.chord([x - 1.0 * R, top - 0.55 * R, x + 1.0 * R, top + 0.55 * R], 180, 360, fill=BLACK)
        d.ellipse([x - 0.1 * R, top - 0.62 * R, x + 0.1 * R, top - 0.42 * R], fill=GOLD)
    elif outfit in ("civ1", "civ4"):
        d.rectangle([x - 0.42 * R, top - 0.75 * R, x + 0.42 * R, top + 0.1 * R], fill=BLACK)
        d.rectangle([x - 0.65 * R, top + 0.02 * R, x + 0.65 * R, top + 0.14 * R], fill=BLACK)
    elif outfit == "civ3":
        d.chord([x - hr * 1.1, top - 0.1 * R, x + hr * 1.1, hc + 0.2 * R], 180, 360, fill=(230, 200, 120), outline=BLACK, width=lw)

# ---------------- backgrounds ----------------
def sky(img, top=(120, 160, 200), bot=(215, 225, 230)):
    a = np.zeros((H, W, 3), np.uint8)
    for c in range(3): a[:, :, c] = np.linspace(top[c], bot[c], H)[:, None]
    img.paste(Image.fromarray(a))

TX0, TX1, DECK, TTOP = 40, 680, 760, 420
def deck_dy(x, amp, phase):
    u = clamp((x - TX0) / (TX1 - TX0))
    return amp * math.sin(math.pi * u) * math.sin(phase)

def bridge_bg(seed=1):
    img = Image.new("RGB", (W, H)); sky(img); d = ImageDraw.Draw(img)
    d.polygon([(0, 640), (150, 560), (330, 610), (520, 540), (720, 600), (720, 900), (0, 900)], fill=(110, 140, 110))
    d.polygon([(0, 700), (200, 650), (450, 690), (720, 660), (720, 900), (0, 900)], fill=(90, 120, 90))
    d.rectangle([0, 880, W, H], fill=(60, 90, 120))
    rnd = random.Random(seed)
    for _ in range(60):
        yy = rnd.randint(890, H); xx = rnd.randint(0, W)
        d.line([(xx, yy), (xx + rnd.randint(20, 70), yy)], fill=(110, 140, 170), width=3)
    d.polygon([(0, 820), (90, 800), (110, 900), (0, 930)], fill=(120, 110, 90))
    d.polygon([(720, 820), (630, 800), (610, 900), (720, 930)], fill=(120, 110, 90))
    return img

def draw_bridge(d, amp=0, phase=0, collapse=0.0, jitter=0.0):
    rnd = random.Random(int(phase * 100))
    for tx in (TX0, TX1):
        d.rectangle([tx - 28, TTOP, tx + 28, 900], fill=(150, 140, 120), outline=BLACK, width=3)
        d.rectangle([tx - 36, TTOP - 20, tx + 36, TTOP + 6], fill=(130, 120, 100), outline=BLACK, width=3)
    pts = []; n = 40
    for i in range(n + 1):
        x = TX0 + (TX1 - TX0) * i / n
        sag = (DECK - 70 - TTOP) * (1 - (2 * i / n - 1) ** 2)
        y = TTOP + sag + deck_dy(x, amp * 0.5, phase)
        if collapse > 0: y += collapse * 400 * math.sin(math.pi * i / n) ** 2
        pts.append((x + rnd.uniform(-jitter, jitter), y + rnd.uniform(-jitter, jitter)))
    if collapse < 0.35:
        d.line(pts, fill=BLACK, width=6)
    else:
        d.line(pts[:12], fill=BLACK, width=6); d.line(pts[-12:], fill=BLACK, width=6)
    for i in range(2, n - 1, 3):
        x, cy = pts[i]
        dy = DECK + deck_dy(x, amp, phase) + collapse * 500 * math.sin(math.pi * i / n) ** 2
        if collapse < 0.2 or i < 8 or i > n - 8:
            d.line([(x, cy), (x, dy)], fill=(50, 50, 50), width=2)
    # deck
    if collapse <= 0:
        seg = [(x, DECK + deck_dy(x, amp, phase)) for x in np.linspace(TX0 - 30, TX1 + 30, 50)]
        d.line(seg, fill=(90, 60, 35), width=18); d.line([(x, y + 9) for x, y in seg], fill=BLACK, width=3)
        d.line([(x, y - 9) for x, y in seg], fill=BLACK, width=3)
    else:
        mid = (TX0 + TX1) / 2
        for side in (-1, 1):
            ang = collapse * 1.1
            x0 = TX0 if side < 0 else TX1
            L = mid - TX0
            ex = x0 - side * L * math.cos(ang) * -1 if False else x0 + (-side) * L * math.cos(ang)
            ey = DECK + L * math.sin(ang) * (1 if side else 1)
            ex = x0 + (mid - x0) * math.cos(ang); ey = DECK + abs(mid - x0) * math.sin(ang)
            d.line([(x0, DECK), (ex, min(ey, 1000))], fill=(90, 60, 35), width=18)

def promenade_bg():
    img = Image.new("RGB", (W, H)); sky(img, (140, 180, 215), (230, 230, 220)); d = ImageDraw.Draw(img)
    rnd = random.Random(3); x = -20
    while x < W:
        w = rnd.randint(90, 150); h = rnd.randint(250, 420)
        c = rnd.choice([(170, 120, 100), (190, 170, 140), (150, 110, 90), (200, 190, 170)])
        d.rectangle([x, 700 - h, x + w, 700], fill=c, outline=BLACK, width=3)
        for wy in range(700 - h + 30, 680, 70):
            for wx in range(x + 15, x + w - 25, 40):
                d.rectangle([wx, wy, wx + 20, wy + 34], fill=(90, 110, 140), outline=BLACK, width=2)
        d.polygon([(x - 5, 700 - h), (x + w // 2, 700 - h - 50), (x + w + 5, 700 - h)], fill=(100, 60, 50), outline=BLACK)
        x += w
    for fx in (110, 360, 610):
        d.line([(fx, 380), (fx, 700)], fill=BLACK, width=4)
        d.polygon([(fx, 380), (fx + 70, 400), (fx, 420)], fill=RED, outline=BLACK)
    d.rectangle([0, 700, W, H], fill=(150, 140, 130))
    for yy in range(710, H, 34):
        off = 0 if (yy // 34) % 2 else 25
        for xx in range(-25 + off, W, 50):
            d.rounded_rectangle([xx, yy, xx + 46, yy + 30], radius=8, fill=(165, 155, 145), outline=(120, 110, 100))
    return img

def planks_bg():
    img = Image.new("RGB", (W, H), (110, 75, 45)); d = ImageDraw.Draw(img)
    for i, yy in enumerate(range(0, H, 140)):
        c = (120 + (i % 3) * 8, 80 + (i % 2) * 6, 48)
        d.rectangle([0, yy, W, yy + 134], fill=c, outline=BLACK, width=4)
        for xx in (40, W - 40):
            d.ellipse([xx - 10, yy + 57, xx + 10, yy + 77], fill=(70, 70, 70), outline=BLACK, width=2)
        rnd = random.Random(i)
        for _ in range(4):
            gy = yy + rnd.randint(20, 110); gx = rnd.randint(0, W - 200)
            d.line([(gx, gy), (gx + rnd.randint(80, 220), gy + rnd.randint(-4, 4))], fill=(90, 60, 35), width=2)
    return img

def chains_bg():
    img = Image.new("RGB", (W, H)); sky(img, (110, 130, 160), (190, 190, 190))
    return img.filter(ImageFilter.GaussianBlur(4))

def news_bg():
    img = Image.new("RGB", (W, H), (100, 65, 40)); d = ImageDraw.Draw(img)
    for yy in range(0, H, 22): d.line([(0, yy), (W, yy + 6)], fill=(90, 58, 35), width=3)
    return img

def blueprint_bg():
    img = Image.new("RGB", (W, H), (25, 60, 120)); d = ImageDraw.Draw(img)
    for x in range(0, W, 40): d.line([(x, 0), (x, H)], fill=(45, 85, 150), width=1)
    for y in range(0, H, 40): d.line([(0, y), (W, y)], fill=(45, 85, 150), width=1)
    return img

BG = {"bridge": bridge_bg(), "prom": promenade_bg(), "planks": planks_bg(), "chains": chains_bg(),
      "news": news_bg(), "blue": blueprint_bg()}
BG["prom_blur"] = BG["prom"].filter(ImageFilter.GaussianBlur(6))

# ---------------- timeline ----------------
T = {}
T["ordered"] = 0.0
T["middle"] = wt("right in the middle")
T["yousee"] = wt("you see")
T["left1"] = wt("left"); T["right"] = wt("right", find("left")); T["left2"] = wt("left", find("left") + 1)
T["crowds"] = wt("the crowds loved")
T["sowhen"] = wt("so when the young")
T["break"] = wt("break step")
T["general"] = wt("the general turns")
T["mob"] = wt("are you trying")
T["stumble"] = wt("the soldiers stumble")
T["ducks"] = wt("ducks")
T["news"] = wt("the newspapers call")
T["next"] = wt("next sunday")
T["halfway"] = wt("and halfway across")
T["hum"] = wt("hum")
T["bounce"] = wt("then bounce")
T["every"] = wt("every step pushes")
T["cheers"] = wt("the crowd cheers")
T["bolts"] = wt("then the bolts")
T["popping"] = wt("popping")
T["folds"] = wt("and the whole bridge folds")
T["rhythm"] = wt("every bridge has")
T["match"] = wt("match it with")
T["apart"] = WORDS[-1]["s"]
SCENES = [("ordered", "s_order"), ("middle", "s_wide"), ("yousee", "s_parade"), ("left1", "s_boots"),
          ("crowds", "s_crowd"), ("sowhen", "s_officer"), ("general", "s_purple"), ("mob", "s_nose"),
          ("stumble", "s_ducks"), ("news", "s_news"), ("next", "s_proud"), ("halfway", "s_hum"),
          ("every", "s_swing"), ("cheers", "s_crowd2"), ("bolts", "s_bolts"), ("folds", "s_collapse"),
          ("rhythm", "s_diagram")]

def soldiers_on_bridge(d, t, amp=0, phase=0, chaos=False, lead=None, R=26, step=6.0, n=7, xoff=0, hopk=0.0, scared=False):
    for k in range(n):
        x = 150 + k * 62 + xoff
        rnd = random.Random(k)
        if chaos:
            wph = t * step * (0.6 + rnd.random()) + k
            hop = abs(math.sin(t * 7 + k)) * 10
            yy = DECK - 10 + deck_dy(x, amp, phase)
            person(d, x + math.sin(t * 3 + k) * 8, yy, R, walk=wph, hop=hop, arm_l=rnd.choice([-30, 20, 60]),
                   arm_r=rnd.choice([-150, 160, 120]), brows="worried", mouth="open" if k % 2 else "flat", musket=True)
        else:
            wph = t * step
            yy = DECK - 10 + deck_dy(x, amp, phase)
            hop = max(0, -deck_dy(x, amp, phase) * hopk)
            person(d, x, yy, R, walk=wph, hop=hop, brows="worried" if scared else "calm",
                   mouth="open" if scared else "flat", musket=True)
    if lead:
        x = 150 + n * 62 + xoff
        person(d, x, DECK - 10 + deck_dy(x, amp, phase), R * 1.15, outfit="general", walk=t * step,
               brows=lead, mouth="smile" if lead == "calm" else "open", arm_r=-100, arm_l=-80)

def cam(img, z, cx, cy, shake=0.0, t=0):
    if shake:
        cx += math.sin(t * 53) * shake; cy += math.cos(t * 41) * shake
    if z == 1 and not shake: return img
    w, h = W / z, H / z
    x0 = clamp(cx - w / 2, 0, W - w); y0 = clamp(cy - h / 2, 0, H - h)
    return img.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BILINEAR)

def s_order(t, d0):
    img = BG["bridge"].copy(); d = ImageDraw.Draw(img); draw_bridge(d)
    for k in range(6): person(d, 130 + k * 55, DECK - 10, 26, musket=True)
    person(d, 520, DECK - 10, 30, arm_r=60 + 20 * ease(t / 0.5), brows="calm", mouth="open" if t < 1.5 else "flat", flip=True)
    return cam(img, lerp(2.4, 2.8, t / d0), 430, 640)

def s_wide(t, d0):
    img = BG["bridge"].copy(); d = ImageDraw.Draw(img); draw_bridge(d)
    for k in range(6): person(d, 130 + k * 55, DECK - 10, 26, musket=True)
    person(d, 520, DECK - 10, 30, arm_r=80, flip=True)
    return cam(img, lerp(1.6, 1.15, ease(t / d0)), 360, 700)

def s_parade(t, d0):
    img = BG["prom"].copy(); d = ImageDraw.Draw(img)
    for k, o in enumerate(["civ1", "civ3", "civ2", "civ4", "civ1", "civ3", "civ2"]):
        person(d, 40 + k * 105, 820, 30, outfit=o, arm_r=-120 + 70 * math.sin(t * 6 + k), mouth="smile")
    for k in range(5):
        x = -200 + t * 90 + k * 130
        person(d, x, 1120, 46, walk=t * 6, musket=True, hop=abs(math.sin(t * 6)) * 6)
    return cam(img, 1.05, 360, 800)

def s_boots(t, d0):
    img = BG["planks"].copy(); d = ImageDraw.Draw(img)
    beats = [T["left1"], T["right"], T["left2"]]
    now = T["left1"] + t
    for i, (bx, b) in enumerate(zip((230, 490, 230), beats)):
        if i == 2 and now < beats[2]: continue
        if i == 0 and now >= beats[2]: continue
        k = (now - b)
        yb = 760 if k >= 0.12 else lerp(200, 760, clamp(k / 0.12)) if k >= 0 else 200
        if k < 0: yb = 300
        d.rectangle([bx - 30, -10, bx + 30, yb - 60], fill=(230, 230, 225), outline=BLACK, width=5)
        d.rounded_rectangle([bx - 70, yb - 80, bx + 90, yb + 40], radius=40, fill=BLACK)
        d.rectangle([bx - 30, yb - 120, bx + 30, yb - 60], fill=RED, outline=BLACK, width=4)
    sh = 10 if any(0 <= now - b < 0.15 for b in beats) else 0
    return cam(img, 1.0 + (0.04 if sh else 0), 360, 640, shake=sh, t=t)

def s_crowd(t, d0, cheer=True):
    img = BG["prom_blur"].copy(); d = ImageDraw.Draw(img)
    for k, (o, x) in enumerate(zip(["civ3", "civ1", "civ2", "civ4"], [110, 290, 470, 640])):
        hop = abs(math.sin(t * 7 + k)) * 25
        person(d, x, 1200 - (k % 2) * 40, 72, outfit=o, hop=hop, arm_l=40 + 30 * math.sin(t * 9 + k),
               arm_r=140 - 30 * math.sin(t * 9 + k), mouth="open", brows="worried" if False else "none")
    return cam(img, lerp(1.0, 1.08, t / d0), 360, 760)

def s_crowd2(t, d0): return s_crowd(t, d0)

def s_officer(t, d0):
    img = BG["bridge"].copy(); d = ImageDraw.Draw(img); draw_bridge(d)
    img = cam(img, 2.0, 360, 600).filter(ImageFilter.GaussianBlur(3)); d = ImageDraw.Draw(img)
    shouting = T["sowhen"] + t >= T["break"]
    person(d, 360, 1250, 150, arm_r=70 if shouting else -110, arm_l=-60, brows="angry" if shouting else "calm",
           mouth="shout" if shouting else "flat")
    return cam(img, 1.0 + (0.06 if shouting else 0), 360, 640, shake=8 if shouting and (T["sowhen"] + t - T["break"]) < 0.5 else 0, t=t)

def s_purple(t, d0):
    img = BG["bridge"].copy(); img = cam(img, 2.2, 360, 600).filter(ImageFilter.GaussianBlur(4)); d = ImageDraw.Draw(img)
    face = lerpc(WHITE, (150, 60, 140), ease(t / max(0.4, d0 * 0.8)))
    person(d, 360, 1350, 190, outfit="general", face=face, brows="angry", mouth="frown", arm_l=-80, arm_r=-100)
    return cam(img, lerp(1.0, 1.25, ease(t / d0)), 360, 560)

def s_nose(t, d0):
    img = BG["bridge"].copy(); img = cam(img, 2.2, 360, 600).filter(ImageFilter.GaussianBlur(4)); d = ImageDraw.Draw(img)
    lean = ease(t / 0.6) * 40
    person(d, 170, 1300, 120, arm_r=-110, brows="calm", mouth="flat")
    person(d, 560 - lean, 1330, 135, outfit="general", face=(150, 60, 140), brows="angry",
           mouth="shout" if int(t * 8) % 2 else "open", flip=True, arm_l=150, arm_r=-100)
    return cam(img, 1.05, 360, 700, shake=3, t=t)

def s_ducks(t, d0):
    img = BG["bridge"].copy(); d = ImageDraw.Draw(img); draw_bridge(d)
    soldiers_on_bridge(d, t, chaos=True, xoff=-60)
    if T["stumble"] + t >= T["ducks"]:
        for k in range(3):
            bx = 150 + k * 140 + t * 20; by = DECK - 120 - k * 15
            d.text((bx, by - 100), "QUACK", font=FONT_XS, fill=WHITE, stroke_width=3, stroke_fill=BLACK)
    return cam(img, 1.7, 360, 680)

def s_news(t, d0):
    img = BG["news"].copy()
    p = Image.new("RGBA", (560, 760), (238, 230, 205, 255)); d = ImageDraw.Draw(p)
    d.rectangle([0, 0, 559, 759], outline=BLACK, width=4)
    d.text((280, 50), "THE MANCHESTER", font=FONT_XS, fill=BLACK, anchor="mm")
    d.text((280, 90), "DAILY COURIER", font=FONT_XS, fill=BLACK, anchor="mm")
    d.line([(20, 120), (540, 120)], fill=BLACK, width=3)
    d.text((280, 175), "THE DUCK", font=FONT_S, fill=BLACK, anchor="mm")
    d.text((280, 240), "BRIGADE", font=FONT_S, fill=BLACK, anchor="mm")
    d.rectangle([60, 290, 500, 600], outline=BLACK, width=3, fill=(225, 218, 190))
    person(d, 280, 570, 70, walk=0.9, brows="worried", mouth="flat", musket=True)
    hc = 570 - 3.15 * 70
    d.polygon([(280 + 30, hc + 20), (280 + 100, hc + 35), (280 + 30, hc + 50)], fill=(240, 150, 30), outline=BLACK)
    for yy in range(630, 740, 22): d.line([(40, yy), (520, yy)], fill=(120, 120, 120), width=6)
    k = ease(t / 0.7)
    p = p.rotate(lerp(380, 6, k), expand=True, resample=Image.BICUBIC)
    s = lerp(0.2, 1.0, k); p = p.resize((max(1, int(p.width * s)), max(1, int(p.height * s))))
    img.paste(p, (360 - p.width // 2, 620 - p.height // 2), p)
    return cam(img, lerp(1.0, 1.1, t / d0), 360, 600)

def s_proud(t, d0):
    img = BG["bridge"].copy(); d = ImageDraw.Draw(img); draw_bridge(d)
    soldiers_on_bridge(d, t, lead="calm", n=5, xoff=-60 + t * 12)
    return cam(img, lerp(1.9, 1.6, t / d0), 400, 660)

def s_hum(t, d0):
    now = T["halfway"] + t
    img = BG["bridge"].copy(); d = ImageDraw.Draw(img)
    amp = 0 if now < T["hum"] else 6 * clamp((now - T["hum"]) / 1.0)
    if now >= T["bounce"]: amp = 22
    ph = now * 2 * math.pi * 1.6
    draw_bridge(d, amp, ph, jitter=amp * 0.15)
    soldiers_on_bridge(d, now, amp, ph, lead="calm", n=5, xoff=40)
    z = 1.9 if now < T["hum"] else 2.6
    return cam(img, z, 300 if now < T["hum"] else 330, 560 if now >= T["hum"] else 660, shake=amp * 0.3, t=t)

def s_swing(t, d0):
    now = T["every"] + t
    img = BG["bridge"].copy(); d = ImageDraw.Draw(img)
    amp = lerp(25, 70, clamp(t / d0)); ph = now * 2 * math.pi * 1.6
    draw_bridge(d, amp, ph)
    soldiers_on_bridge(d, now, amp, ph, lead="worried", n=5, xoff=40, hopk=0.6, scared=True)
    return cam(img, 1.2, 360, 700)

def s_bolts(t, d0):
    now = T["bolts"] + t
    img = BG["chains"].copy(); d = ImageDraw.Draw(img)
    sh = 6 + 8 * clamp(t / d0)
    pops = [T["popping"] + i * 0.35 for i in range(3)]
    for i in range(9):
        cx = 60 + i * 80; cy = 200 + i * 105
        jx = math.sin(now * 40 + i) * sh; jy = math.cos(now * 37 + i) * sh
        if i % 2: d.ellipse([cx - 70 + jx, cy - 34 + jy, cx + 70 + jx, cy + 34 + jy], outline=(60, 60, 65), width=22)
        else: d.ellipse([cx - 34 + jx, cy - 70 + jy, cx + 34 + jx, cy + 70 + jy], outline=(75, 75, 80), width=22)
    for i, p in enumerate(pops):
        bx, by = 200 + i * 160, 480 + i * 140
        if now < p:
            d.regular_polygon((bx, by, 34), 6, fill=(150, 150, 155), outline=BLACK)
        else:
            k = now - p
            fx, fy = bx + k * 900 * (1 if i % 2 else -1), by - k * 700 + 900 * k * k
            d.regular_polygon((fx, fy, 34), 6, rotation=k * 900, fill=(150, 150, 155), outline=BLACK)
            if k < 0.12:
                d.ellipse([bx - 70, by - 70, bx + 70, by + 70], fill=(255, 230, 120))
    flash = any(0 <= now - p < 0.08 for p in pops)
    return cam(img, 1.08 if flash else 1.0, 360, 640, shake=sh + (14 if flash else 0), t=t)

def s_collapse(t, d0):
    img = BG["bridge"].copy(); d = ImageDraw.Draw(img)
    c = ease(clamp((t - 0.2) / 1.6))
    draw_bridge(d, 0 if c > 0 else 40, 0, collapse=c, jitter=4)
    if c < 0.3:
        soldiers_on_bridge(d, t, 40, t * 10, lead="worried", n=5, xoff=40, scared=True)
    else:
        rnd = random.Random(5)
        for k in range(6):
            x = 180 + k * 70; y = DECK + (t - 0.6) * 500 + rnd.randint(0, 60)
            if y < 950: person(d, x, y, 24, arm_l=150, arm_r=30, brows="worried", mouth="open", musket=False)
    if t > 1.0:
        k = clamp((t - 1.0) / 1.5)
        rnd = random.Random(9)
        for i in range(70):
            a = rnd.uniform(math.pi * 1.05, math.pi * 1.95); v = rnd.uniform(250, 650)
            px = 360 + math.cos(a) * v * k * 1.0; py = 900 + math.sin(a) * v * k + 600 * k * k
            r = rnd.randint(8, 20) * (1 - k * 0.6)
            d.ellipse([px - r, py - r, px + r, py + r], fill=(210, 230, 245), outline=(120, 150, 180))
    return cam(img, 1.15, 360, 760, shake=10 if 0.2 < t < 2.5 else 0, t=t)

def s_diagram(t, d0):
    now = T["rhythm"] + t
    img = BG["blue"].copy(); d = ImageDraw.Draw(img)
    LC = (220, 235, 255)
    d.text((360, 170), "RESONANCE", font=FONT_S, fill=LC, anchor="mm")
    d.line([(80, 1060), (640, 1060)], fill=LC, width=5)
    for tx in (80, 640): d.rectangle([tx - 15, 980, tx + 15, 1150], outline=LC, width=4)
    amp = 10 + 110 * clamp((now - T["match"]) / max(0.5, T["apart"] - T["match"])) if now > T["match"] else 10
    pts = [(x, 1060 - amp * math.sin(math.pi * (x - 80) / 560) * math.sin(now * 2 * math.pi * 1.5)) for x in range(80, 641, 8)]
    d.line(pts, fill=(255, 210, 90), width=7)
    d.text((360, 1200), "bridge: 1.5 swings / sec", font=FONT_XS, fill=LC, anchor="mm")
    beat = (now * 1.5) % 1
    for i in range(6):
        bx = 120 + i * 95; on = now > T["match"] and i <= int((now - T["match"]) * 1.5) % 6
        d.rounded_rectangle([bx - 26, 360, bx + 34, 400], radius=14, fill=(255, 210, 90) if on else None, outline=LC, width=3)
        d.rectangle([bx - 12, 300, bx + 12, 362], outline=LC, width=3)
    d.text((360, 470), "boots: 1.5 steps / sec", font=FONT_XS, fill=LC, anchor="mm")
    return img

FN = {name: globals()[name] for _, name in SCENES}
starts = [T[k] for k, _ in SCENES] + [DUR]

def caption(img, now):
    cur = None
    for i, w in enumerate(WORDS):
        if w["s"] <= now and (i + 1 == len(WORDS) or now < WORDS[i + 1]["s"]):
            cur = (i, w)
    if not cur or now > cur[1]["e"] + 0.6: return
    i, w = cur
    txt = w["w"]
    if len(txt) <= 3 and i + 1 < len(WORDS) and WORDS[i + 1]["s"] - w["s"] < 0.35:
        txt += " " + WORDS[i + 1]["w"]
    d = ImageDraw.Draw(img)
    pop = 1.0 + 0.12 * clamp(1 - (now - w["s"]) / 0.1)
    f = FONT if pop < 1.01 else ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", int(76 * pop))
    d.text((W // 2, int(H * 0.70)), txt, font=f, fill=WHITE, anchor="mm", stroke_width=7, stroke_fill=BLACK)

def frame(now):
    si = max(i for i in range(len(SCENES)) if starts[i] <= now)
    t = now - starts[si]; d0 = starts[si + 1] - starts[si]
    img = FN[SCENES[si][1]](t, d0)
    caption(img, now)
    return img

if PREVIEW:
    for i, (k, n) in enumerate(SCENES):
        frame(min(starts[i] + 0.6 * (starts[i + 1] - starts[i]), DUR - 0.01)).save(f"{OUT}_{i:02d}.jpg", quality=80)
    sys.exit()

# ---------------- audio ----------------
SR = 44100
N = int(DUR * SR) + SR
mix = np.zeros(N)
import wave
for f, off in data["files"]:
    with wave.open(f) as wv:
        a = np.frombuffer(wv.readframes(wv.getnframes()), np.int16) / 32768.0
    s = int(off * SR); mix[s:s + len(a)] += a
rng = np.random.default_rng(1)
def add(sig, t, g=1.0):
    s = int(t * SR); e = min(N, s + len(sig)); mix[s:e] += sig[:e - s] * g
def tt(d): return np.arange(int(d * SR)) / SR
def env(d, a=0.005, r=None):
    x = tt(d); r = r or d; return np.minimum(1, x / a) * np.exp(-x / (r / 4))
def noise(d): return rng.standard_normal(int(d * SR))
def lowpass(x, k=40): return np.convolve(x, np.ones(k) / k, mode="same")
# music bed: low march drone + soft drum on beat until collapse
bed = np.zeros(N); x = np.arange(N) / SR
bed += 0.035 * np.sin(2 * np.pi * 55 * x) + 0.02 * np.sin(2 * np.pi * 82.4 * x)
for b in np.arange(0.3, T["folds"] + 1.0, 60 / 112):
    s = int(b * SR); k = lowpass(noise(0.12), 20) * env(0.12) * 0.12
    bed[s:s + len(k)] += k[:max(0, min(len(k), N - s))]
fade = np.ones(N); cut = int((T["folds"] + 1.2) * SR); fade[cut:] = np.exp(-(np.arange(N - cut)) / (SR * 0.3))
mix += bed * fade
add(np.sin(2 * np.pi * 2200 * tt(0.4) + 30 * np.sin(2 * np.pi * 6 * tt(0.4))) * env(0.4, 0.02, 0.6) * 0.18, 0.0)
for b in (T["left1"], T["right"], T["left2"]):
    add(lowpass(noise(0.25), 60) * env(0.25) * 1.6 + np.sin(2 * np.pi * 70 * tt(0.25)) * env(0.25) * 0.5, b)
for b in np.arange(T["break"], T["break"] + 0.6, 0.6): pass
q = tt(0.18); quack = np.sign(np.sin(2 * np.pi * (520 - 900 * q) * q)) * env(0.18, 0.01, 0.4) * 0.12
for k in range(3): add(quack, T["ducks"] + 0.05 + k * 0.28)
def cheer(d): return lowpass(noise(d), 8) * np.sin(np.pi * tt(d) / d) * 0.25
add(cheer(2.2), T["crowds"] - 0.2); add(cheer(2.6), T["cheers"] - 0.1)
add(np.sin(2 * np.pi * 48 * tt(4)) * np.minimum(1, tt(4) / 2) * 0.14, T["hum"])
creak = np.sin(2 * np.pi * (180 + 60 * np.sin(2 * np.pi * 3 * tt(0.7))) * tt(0.7)) * env(0.7, 0.05, 1.0) * 0.08
for k in range(4): add(creak, T["bounce"] + k * 0.62)
for i in range(3): add(noise(0.3) * env(0.3, 0.001, 0.15) * 0.7, T["popping"] + i * 0.35)
add(lowpass(noise(1.2), 6) * env(1.2, 0.01, 1.4) * 0.8, T["folds"] + 0.3); add(lowpass(noise(2.5), 150) * env(2.5, 0.2, 3) * 1.5, T["folds"] + 0.3)
add(lowpass(noise(2.0), 4) * np.sin(np.pi * tt(2.0) / 2.0) * 0.5, T["folds"] + 1.1)
mix = mix / max(1e-6, np.abs(mix).max()) * 0.92
pcm = (mix * 32767).astype(np.int16)
with wave.open(f"{OUT}.wav", "wb") as wv:
    wv.setnchannels(1); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes(pcm.tobytes())

# ---------------- video ----------------
p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
                      "-i", "-", "-i", f"{OUT}.wav", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                      "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", f"{OUT}.mp4"], stdin=subprocess.PIPE)
nf = int(DUR * FPS)
for i in range(nf):
    p.stdin.write(frame(i / FPS).tobytes())
p.stdin.close(); p.wait()
print("done", nf, "frames")
