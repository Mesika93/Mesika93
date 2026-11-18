import json, math, random, subprocess, sys, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 720, 1280
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

