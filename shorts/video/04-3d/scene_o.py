"""Elisha Otis safety elevator (1854): NY street, construction site, workshop, Crystal Palace tower, mechanism.
usage: ../bvenv/bin/python scene_o.py -- OUTDIR shot1 [shot2 ...] [--test]
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "p2"))
from blib import *
HERE = os.path.dirname(os.path.abspath(__file__))
rnd = random.Random(8)
def lerp(a, b, t): return a + (b - a) * t

# ---------------- materials ----------------
M_BRICK = pbr("brick", "red_brick_03", 0.3, tint=(0.95, 0.8, 0.72))
M_BRICK2 = pbr("brick2", "red_brick_03", 0.3, tint=(0.75, 0.62, 0.55))
M_COBBLE = pbr("cobble", "cobblestone_floor_01", 0.3, tint=(0.8, 0.75, 0.68))
M_STONE = pbr("stone", "castle_brick_07", 0.4, tint=(0.95, 0.9, 0.8))
M_WOOD = pbr("wood", "brown_planks_05", 0.6, tint=(0.62, 0.45, 0.3))
M_WOODD = pbr("woodd", "brown_planks_05", 0.6, tint=(0.4, 0.27, 0.17))
M_TILES = pbr("tiles", "checkered_pavement_tiles", 0.25, tint=(0.9, 0.85, 0.75))
M_PLASTER = pbr("plaster", "painted_plaster_wall", 0.3, tint=(0.8, 0.72, 0.6))
M_FLOOR = pbr("floor", "wood_floor_worn", 0.35, tint=(0.6, 0.45, 0.3))
M_IRON = flat("iron", (0.08, 0.09, 0.1), 0.45, 0.8)
M_IRONW = flat("ironw", (0.75, 0.75, 0.72), 0.5, 0.3)      # white-painted cast iron (Crystal Palace)
M_BRASS = flat("brass", (0.8, 0.58, 0.25), 0.25, 1.0)
M_STEEL = flat("steel", (0.55, 0.56, 0.58), 0.3, 1.0)
M_ROPE = flat("rope", (0.55, 0.45, 0.3), 0.9)
M_GLASS = flat("glassd", (0.03, 0.04, 0.05), 0.08, 0.3)
M_FRAME = flat("frame", (0.85, 0.82, 0.75), 0.6)
M_AWN = [flat(f"awn{i}", c, 0.8) for i, c in enumerate([(0.5, 0.08, 0.08), (0.1, 0.25, 0.15), (0.15, 0.2, 0.45)])]
M_FLAG = [flat(f"flag{i}", c, 0.8) for i, c in enumerate([(0.7, 0.05, 0.06), (0.9, 0.88, 0.82), (0.08, 0.15, 0.5), (0.85, 0.65, 0.1)])]
M_LAMP = flat("lamp", (1.0, 0.85, 0.6), 0.5, emit=10.0)
M_DARK = flat("dark", (0.02, 0.02, 0.02), 0.9)

def roof_glass():
    m = bpy.data.materials.new("roofglass"); m.use_nodes = True; nt = m.node_tree
    out = nt.nodes["Material Output"]; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.82, 0.8, 0.75, 1); b.inputs["Roughness"].default_value = 0.5
    tc = node(nt, "ShaderNodeTexCoord"); br = node(nt, "ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = 1.0; br.inputs["Mortar Size"].default_value = 0.04
    br.inputs["Brick Width"].default_value = 1.2; br.inputs["Row Height"].default_value = 2.4
    br.offset = 0.0
    tr = node(nt, "ShaderNodeBsdfTransparent"); mx = node(nt, "ShaderNodeMixShader")
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"]); nt.links.new(br.outputs["Fac"], mx.inputs["Fac"])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(b.outputs[0], mx.inputs[2])
    tr.inputs["Color"].default_value = (0.92, 0.95, 1.0, 1)
    nt.links.new(mx.outputs[0], out.inputs["Surface"]); return m
M_ROOF = roof_glass()

def tower_mat():
    m = bpy.data.materials.new("towerwin"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]; tc = node(nt, "ShaderNodeTexCoord"); br = node(nt, "ShaderNodeTexBrick")
    br.inputs["Scale"].default_value = 0.6; br.inputs["Mortar Size"].default_value = 0.12
    br.inputs["Brick Width"].default_value = 1.0; br.inputs["Row Height"].default_value = 1.6; br.offset = 0.0
    br.inputs["Color1"].default_value = (0.08, 0.12, 0.18, 1); br.inputs["Color2"].default_value = (0.12, 0.17, 0.24, 1)
    br.inputs["Mortar"].default_value = (0.7, 0.68, 0.62, 1)
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"]); nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.25; b.inputs["Metallic"].default_value = 0.3; return m
M_TOWER = tower_mat()

# ---------------- world ----------------
w = bpy.data.worlds.new("sky"); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes["Background"]
env = node(nt, "ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(os.path.join(A, "sky.hdr"))
mp = node(nt, "ShaderNodeMapping"); tc = node(nt, "ShaderNodeTexCoord")
mp.inputs["Rotation"].default_value = (0, 0, math.radians(140))
nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
nt.links.new(env.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 1.0
sun_d = bpy.data.lights.new("sun", "SUN"); sun_d.energy = 3.4; sun_d.angle = math.radians(1.5); sun_d.color = (1.0, 0.93, 0.82)
sun = bpy.data.objects.new("sun", sun_d); sc.collection.objects.link(sun)
sun.rotation_euler = Euler((math.radians(50), 0, math.radians(-50)))

GROUPS = {}
def grp(name, o):
    GROUPS.setdefault(name, []).append(o); return o

def cyl(name, p0, p1, r, mat, verts=12):
    p0, p1 = Vector(p0), Vector(p1); d = p1 - p0
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=d.length, location=(p0 + p1) / 2)
    o = bpy.context.object; o.rotation_euler = d.to_track_quat("Z", "Y").to_euler(); o.data.materials.append(mat); o.name = name
    return o

# ================= NY STREET (origin) =================
multi_box("street", [((-6, -80, -0.2), (6, 120, 0.0))], M_COBBLE)
multi_box("walks", [((-9, -80, -0.2), (-6, 120, 0.15)), ((6, -80, -0.2), (9, 120, 0.15))], M_STONE)
FLOOR_H = 3.3
def building(x0, x1, y0, y1, floors, side, mat):
    multi_box("bld", [((x0, y0, 0), (x1, y1, floors * FLOOR_H))], mat)
    multi_box("cornice", [((x0 - side * 0.35 if side < 0 else x0, y0 - 0.2, floors * FLOOR_H - 0.3),
                           (x1 + 0.35 if side < 0 else x1, y1 + 0.2, floors * FLOOR_H + 0.25))], M_STONE)
    face = x1 if side < 0 else x0   # facade faces the street
    nwin = max(2, int((y1 - y0) / 2.6))
    for f in range(1, floors):
        z = f * FLOOR_H + 0.9
        for k in range(nwin):
            y = y0 + (k + 0.5) * (y1 - y0) / nwin
            fx = face + (0.03 if side < 0 else -0.03)
            multi_box("win", [((fx - 0.05, y - 0.55, z), (fx + 0.05, y + 0.55, z + 1.7))], M_GLASS)
            multi_box("lintel", [((fx - 0.12, y - 0.7, z + 1.7), (fx + 0.12, y + 0.7, z + 1.95)),
                                 ((fx - 0.1, y - 0.65, z - 0.15), (fx + 0.1, y + 0.65, z))], M_STONE)
    # shop front
    fx = face + (0.03 if side < 0 else -0.03)
    multi_box("shop", [((fx - 0.06, y0 + 0.6, 0.3), (fx + 0.06, y1 - 0.6, 2.6))], M_GLASS)
    aw = rnd.choice(M_AWN); s = 1 if side < 0 else -1
    o = multi_box("awning", [((0, y0 + 0.4, -0.05), (1.8, y1 - 0.4, 0.05))], aw, (face, 0, 2.9))
    o.rotation_euler = (0, math.radians(15) * (1 if side < 0 else -1), 0)
    if side > 0: o.location = (face - 1.8 * math.cos(math.radians(15)), 0, 2.9 + 0.45); o.rotation_euler = (0, math.radians(-15), 0)
LOWB = []
for side in (-1, 1):
    y = -70.0
    while y < 110:
        wdt = rnd.uniform(7, 11)
        if side > 0 and 14 < y + wdt / 2 < 32: y = 32; continue          # construction gap
        fl = rnd.choice([4, 5, 5, 6])
        x0, x1 = (-20, -9) if side < 0 else (9, 20)
        before = len(sc.objects)
        building(x0, x1, y, y + wdt - 0.15, fl, side, rnd.choice([M_BRICK, M_BRICK2, M_BRICK, M_PLASTER]))
        LOWB.extend(list(sc.objects)[before:])
        y += wdt
multi_box("endblock", [((-25, 118, 0), (25, 130, 19))], M_BRICK2)
# lamp posts
for y in range(-60, 110, 18):
    for x in (-6.6, 6.6):
        cyl("post", (x, y, 0.15), (x, y, 3.8), 0.07, M_IRON)
        multi_box("lampbox", [((x - 0.22, y - 0.22, 3.8), (x + 0.22, y + 0.22, 4.3))], M_GLASS)
        multi_box("lampcap", [((x - 0.3, y - 0.3, 4.3), (x + 0.3, y + 0.3, 4.4))], M_IRON)
# carriage
multi_box("cart", [((-4.2, 6, 0.9), (-2.6, 9.5, 2.0))], M_WOODD)
for yy in (6.5, 9.0):
    for xx in (-4.25, -2.55):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.6, minor_radius=0.06, location=(xx, yy, 0.65), rotation=(0, math.radians(90), 0))
        bpy.context.object.data.materials.append(M_WOODD)
# skyscrapers (skyline state) occupy the same blocks
TALL = []
for side in (-1, 1):
    y = -70.0
    while y < 110:
        wdt = rnd.uniform(14, 22); h = rnd.uniform(70, 190)
        x0, x1 = (-34, -9) if side < 0 else (9, 34)
        TALL.append(multi_box("tall", [((x0, y, 0), (x1, y + wdt - 1.0, h))], M_TOWER))
        TALL.append(multi_box("tallcap", [((x0 + 2, y + 2, h), (x1 - 2, y + wdt - 3, h + 6))], M_TOWER))
        y += wdt
for o in TALL: o.hide_render = True

# ---- construction site with a rope hoist (x 9..20, y 15..31) ----
SX, SY = 13.5, 23.0
multi_box("dirt", [((9, 14, -0.1), (20, 32, 0.08))], M_WOODD)
for dx in (-2.5, 2.5):
    for dy in (-2.5, 2.5):
        cyl("pole", (SX + dx, SY + dy, 0), (SX + dx, SY + dy, 14), 0.12, M_WOODD, 8)
for z in (4, 8, 12):
    multi_box("scaf", [((SX - 2.6, SY - 2.6, z), (SX + 2.6, SY - 2.3, z + 0.25)), ((SX - 2.6, SY + 2.3, z), (SX + 2.6, SY + 2.6, z + 0.25))], M_WOOD)
multi_box("beam", [((SX - 3.0, SY - 0.2, 14), (SX + 3.0, SY + 0.2, 14.4))], M_WOODD)
bpy.ops.mesh.primitive_torus_add(major_radius=0.35, minor_radius=0.08, location=(SX, SY, 13.7), rotation=(math.radians(90), 0, 0))
bpy.context.object.data.materials.append(M_IRON)
# half-built brick wall behind
multi_box("halfwall", [((18.5, 15, 0), (20, 31, 7.5))], M_BRICK)
HOIST_OK, HOIST_FALL = [], []
def hoist_platform(z, tilt=0.0, grp_list=None):
    o = multi_box("hplat", [((-1.3, -1.3, 0), (1.3, 1.3, 0.18))], M_WOOD, (SX, SY, z)); o.rotation_euler = (tilt, tilt * 0.4, 0); grp_list.append(o)
    for k, (dx, dy, s) in enumerate([(-0.5, -0.4, 0.7), (0.5, 0.3, 0.6), (-0.3, 0.6, 0.5)]):
        c = multi_box("crate", [((-s / 2, -s / 2, 0), (s / 2, s / 2, s))], M_WOODD, (SX + dx, SY + dy, z + 0.18)); grp_list.append(c)
hoist_platform(7.5, 0, HOIST_OK)
HOIST_OK.append(cyl("hrope", (SX, SY, 7.7), (SX, SY, 13.6), 0.04, M_ROPE, 8))
# fallen state
o = multi_box("hplat", [((-1.3, -1.3, 0), (1.3, 1.3, 0.18))], M_WOOD, (SX, SY, 0.1)); o.rotation_euler = (0.12, -0.08, 0.3); HOIST_FALL.append(o)
for k in range(6):
    s = rnd.uniform(0.4, 0.75)
    c = multi_box("crate", [((-s / 2, -s / 2, 0), (s / 2, s / 2, s))], M_WOODD, (SX + rnd.uniform(-3, 3), SY + rnd.uniform(-3.5, 2), 0.05))
    c.rotation_euler = (rnd.uniform(-0.3, 0.3), rnd.uniform(-0.3, 0.3), rnd.uniform(0, 3)); HOIST_FALL.append(c)
HOIST_FALL.append(cyl("hrope2", (SX, SY, 13.6), (SX + 0.4, SY - 0.3, 6.0), 0.04, M_ROPE, 8))
for o in HOIST_FALL: o.hide_render = True

# ================= WORKSHOP (y = 1500) =================
WY = 1500.0
multi_box("wfloor", [((-6, WY - 5, -0.2), (6, WY + 5, 0))], M_FLOOR)
multi_box("wwalls", [((-6.2, WY + 5, 0), (6.2, WY + 5.3, 4)), ((-6.3, WY - 5, 0), (-6, WY + 5, 4)), ((6, WY - 5, 0), (6.3, WY + 5, 4)),
                     ((-6.2, WY - 5.3, 0), (6.2, WY - 5, 4))], M_BRICK2)
multi_box("wceil", [((-6.3, WY - 5.3, 4), (6.3, WY + 5.3, 4.3))], M_WOODD)
multi_box("bench", [((-2.5, WY + 2.5, 0.85), (2.5, WY + 4.0, 0.95)), ((-2.4, WY + 2.6, 0), (-2.2, WY + 3.9, 0.85)), ((2.2, WY + 2.6, 0), (2.4, WY + 3.9, 0.85))], M_WOODD)
multi_box("shelf", [((-5.9, WY - 3, 1.6), (-5.5, WY + 3, 1.68)), ((-5.9, WY - 3, 2.5), (-5.5, WY + 3, 2.58))], M_WOOD)
for k in range(9):   # gears on the wall and bench
    r = rnd.uniform(0.15, 0.45)
    bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=r, depth=0.06, location=(-5.8, WY - 2.5 + k * 0.6, 1.9 + (k % 2) * 0.8), rotation=(0, math.radians(90), 0))
    bpy.context.object.data.materials.append(M_BRASS if k % 2 else M_STEEL)
for k in range(4):
    bpy.ops.mesh.primitive_torus_add(major_radius=0.12 + 0.05 * k, minor_radius=0.025, location=(1.0 + k * 0.35, WY + 3.0, 0.98))
    bpy.context.object.data.materials.append(M_BRASS)
# model tower on bench
MX, MYW = -0.8, WY + 3.2
for dx in (-0.25, 0.25):
    multi_box("mpost", [((MX + dx - 0.025, MYW - 0.025, 0.95), (MX + dx + 0.025, MYW + 0.025, 1.9))], M_WOOD)
multi_box("mtop", [((MX - 0.32, MYW - 0.04, 1.9), (MX + 0.32, MYW + 0.04, 1.95))], M_WOOD)
multi_box("mplat", [((MX - 0.2, MYW - 0.15, 1.3), (MX + 0.2, MYW + 0.15, 1.33))], M_WOOD)
cyl("mrope", (MX, MYW, 1.33), (MX, MYW, 1.9), 0.006, M_ROPE, 6)
L = bpy.data.lights.new("wl", "POINT"); L.energy = 600; L.color = (1.0, 0.8, 0.55); L.shadow_soft_size = 0.3
o = bpy.data.objects.new("wl", L); o.location = (0.5, WY + 2.2, 2.6); sc.collection.objects.link(o)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, location=(0.5, WY + 2.2, 2.6)); bpy.context.object.data.materials.append(M_LAMP)
L = bpy.data.lights.new("wl2", "AREA"); L.energy = 400; L.size = 4; L.color = (0.85, 0.9, 1.0)
o = bpy.data.objects.new("wl2", L); o.location = (0, WY - 3, 3.8); sc.collection.objects.link(o)

# ================= CRYSTAL PALACE (y = 500) =================
CY = 500.0; HW, HL, HH = 22.0, 40.0, 12.0
multi_box("hfloor", [((-HW, CY - HL, -0.2), (HW, CY + HL, 0))], M_TILES)
for x in (-HW, HW):   # side walls: glass with iron frames
    o = multi_box("hwall", [((x - 0.05, CY - HL, 0), (x + 0.05, CY + HL, HH))], M_ROOF)
multi_box("hend", [((-HW, CY + HL - 0.05, 0), (HW, CY + HL + 0.05, HH))], M_ROOF)
# barrel vault roof
rings = []
for k in range(2):
    y = CY - HL + 2 * HL * k
    rings.append([(HW * math.cos(a), y, HH + HW * 0.55 * math.sin(a)) for a in [i * math.pi / 28 for i in range(29)]])
V = [p for r in rings for p in r]; F = [(k, k + 1, 29 + k + 1, 29 + k) for k in range(28)]
obj_from("vault", V, F, M_ROOF)
for x in (-18, -9, 9, 18):   # columns + arches
    for y in range(int(CY - HL + 4), int(CY + HL), 8):
        if abs(x) < 4 and abs(y - CY) < 6: continue
        cyl("col", (x, y, 0), (x, y, HH), 0.22, M_IRONW, 16)
for y in range(int(CY - HL + 4), int(CY + HL), 8):
    pts = [(HW * math.cos(a), y, HH + HW * 0.55 * math.sin(a)) for a in [i * math.pi / 28 for i in range(29)]]
    for a_, b_ in zip(pts[:-1], pts[1:]): cyl("rib", a_, b_, 0.12, M_IRONW, 8)
    if abs(y - CY) > 6: cyl("tie", (-HW, y, HH), (HW, y, HH), 0.1, M_IRONW, 8)
for k in range(12):   # hanging flags
    x = -16 + k * 3.0; y = CY + rnd.uniform(-20, 25); m = M_FLAG[k % 4]
    if abs(x) < 6 and abs(y - CY) < 10: y = CY + 14 + k
    multi_box("flag", [((x - 0.7, y - 0.02, HH - 4.5), (x + 0.7, y + 0.02, HH - 0.5))], m)
for k in range(10):   # exhibit stands
    x = rnd.choice([-1, 1]) * rnd.uniform(8, 18); y = CY + rnd.uniform(-30, 32)
    multi_box("stand", [((x - 1.5, y - 1.0, 0), (x + 1.5, y + 1.0, 0.9))], M_WOODD)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.5, depth=1.2, location=(x, y, 1.5)); bpy.context.object.data.materials.append(M_BRASS)
# ---- the tower ----
TZ = 9.0   # platform height
TOP = 13.5
for dx in (-1.6, 1.6):
    for dy in (-1.1, 1.1):
        multi_box("tpost", [((dx - 0.12, CY + dy - 0.12, 0), (dx + 0.12, CY + dy + 0.12, TOP))], M_WOODD)
for z in (3.0, 6.0):
    for dy in (-1.1, 1.1):
        multi_box("tbrace", [((-1.6, CY + dy - 0.06, z), (1.6, CY + dy + 0.06, z + 0.14))], M_WOODD)
multi_box("ttop", [((-2.0, CY - 1.3, TOP), (2.0, CY + 1.3, TOP + 0.35))], M_WOODD)
# guide rails with ratchet teeth (inner faces at x = +-1.45)
for s in (-1, 1):
    multi_box("rail", [((s * 1.45 - 0.07, CY - 0.12, 0.2), (s * 1.45 + 0.07, CY + 0.12, TOP))], M_WOOD)
    for k in range(int(TOP / 0.25)):
        z = 0.3 + k * 0.25
        V = [(s * 1.38, CY - 0.1, z), (s * 1.38, CY + 0.1, z), (s * 1.38, CY + 0.1, z + 0.2), (s * 1.38, CY - 0.1, z + 0.2),
             (s * 1.27, CY - 0.1, z + 0.2), (s * 1.27, CY + 0.1, z + 0.2)]
        F = [(0, 1, 2, 3), (3, 2, 5, 4), (0, 3, 4), (1, 5, 2), (0, 4, 5, 1)]
        obj_from("tooth", V, F, M_IRON)
bpy.ops.mesh.primitive_torus_add(major_radius=0.45, minor_radius=0.09, location=(0, CY, TOP - 0.35), rotation=(math.radians(90), 0, 0))
bpy.context.object.data.materials.append(M_IRON)
# platform
multi_box("plat", [((-1.25, CY - 1.0, TZ), (1.25, CY + 1.0, TZ + 0.2))], M_WOOD)
multi_box("platrail", [((-1.25, CY - 1.0, TZ + 0.2), (-1.18, CY + 1.0, TZ + 1.1)), ((1.18, CY - 1.0, TZ + 0.2), (1.25, CY + 1.0, TZ + 1.1)),
                       ((-1.25, CY - 1.0, TZ + 1.05), (1.25, CY - 0.94, TZ + 1.12))], M_WOODD)
for dx in (-1.2, 1.2): multi_box("hanger", [((dx - 0.05, CY - 0.05, TZ + 0.2), (dx + 0.05, CY + 0.05, TZ + 2.3))], M_IRON)
multi_box("crossbar", [((-1.3, CY - 0.1, TZ + 2.3), (1.3, CY + 0.1, TZ + 2.45))], M_IRON)
for k, (dx, dy, s) in enumerate([(-0.75, 0.55, 0.55), (0.7, 0.5, 0.5)]):
    multi_box("pcrate", [((dx - s / 2, CY + dy - s / 2, TZ + 0.2), (dx + s / 2, CY + dy + s / 2, TZ + 0.2 + s))], M_WOODD)
bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.28, depth=0.7, location=(0.75, CY - 0.5, TZ + 0.55)); bpy.context.object.data.materials.append(M_WOODD)
# wagon spring + pawls: two states
def leaf_spring(arch, name):
    pts = []
    for k in range(17):
        u = k / 16; x = -1.1 + 2.2 * u; z = TZ + 2.5 + arch * math.sin(math.pi * u)
        pts.append((x, z))
    V, F = [], []
    for i, (x, z) in enumerate(pts):
        for dy, dz in ((-0.09, 0), (0.09, 0), (0.09, 0.06), (-0.09, 0.06)): V.append((x, CY + dy, z + dz))
    for i in range(16):
        a = i * 4; b = a + 4
        for k in range(4): F.append((a + k, a + (k + 1) % 4, b + (k + 1) % 4, b + k))
    return obj_from(name, V, F, M_STEEL)
SPRING_A = [leaf_spring(0.55, "springA"), leaf_spring(0.48, "springA2")]
SPRING_B = [leaf_spring(0.08, "springB"), leaf_spring(0.02, "springB2")]
PAWL_A = [multi_box("pawlA", [((s * 1.12 - 0.08, CY - 0.08, TZ + 2.45), (s * 1.12 + 0.08, CY + 0.08, TZ + 2.75))], M_IRON) for s in (-1, 1)]
PAWL_B = []
for s in (-1, 1):
    o = multi_box("pawlB", [((-0.07, -0.08, 0), (0.07, 0.08, 0.32))], M_IRON, (s * 1.24, CY, TZ + 2.4)); o.rotation_euler = (0, s * math.radians(-60), 0)
    PAWL_B.append(o)
ROPE_OK = [cyl("rope", (0, CY, TZ + 2.5 + 0.55), (0, CY, TOP - 0.35), 0.05, M_ROPE, 10)]
ROPE_CUT = [cyl("ropeup", (0, CY, TOP - 0.9), (0, CY, TOP - 0.35), 0.05, M_ROPE, 10),
            cyl("ropedn", (0.15, CY, TZ + 3.0), (0.05, CY, TZ + 4.3), 0.05, M_ROPE, 10)]
for o in SPRING_B + PAWL_B + ROPE_CUT: o.hide_render = True
for x, y in ((-10, CY - 15), (10, CY - 15), (0, CY + 15)):
    L = bpy.data.lights.new("hl", "AREA"); L.energy = 3000; L.size = 10; L.color = (1.0, 0.97, 0.9)
    o = bpy.data.objects.new("hl", L); o.location = (x, y, HH + 8); sc.collection.objects.link(o)

STATE = {"low": True, "fall": False, "cut": False, "mech": "A"}
def apply_state(st):
    for o in LOWB: o.hide_render = not st["low"]
    for o in TALL: o.hide_render = st["low"]
    for o in HOIST_OK: o.hide_render = st["fall"]
    for o in HOIST_FALL: o.hide_render = not st["fall"]
    for o in ROPE_OK: o.hide_render = st["cut"]
    for o in ROPE_CUT: o.hide_render = not st["cut"]
    a = st["mech"] == "A"
    for o in SPRING_A + PAWL_A: o.hide_render = not a
    for o in SPRING_B + PAWL_B: o.hide_render = a

# ---------------- shots ----------------
SHOTS = {
    # name: (loc, target, lens, dof, state overrides)
    "towerlow": ((5.0, CY - 13.0, 1.6), (0.0, CY, 8.5), 22, None, {}),
    "street": ((-1.5, -32.0, 1.7), (1.0, 20.0, 4.5), 24, None, {}),
    "streetup": ((0.0, -30.0, 1.5), (0.5, 20.0, 15.0), 20, None, {}),
    "skyline": ((0.0, -30.0, 1.5), (0.5, 20.0, 15.0), 20, None, {"low": False}),
    "site": ((1.5, 11.0, 1.7), (SX, SY, 6.5), 24, None, {}),
    "fall": ((1.5, 11.0, 1.7), (SX, SY, 2.0), 24, None, {"fall": True}),
    "shop": ((1.5, WY - 3.8, 1.7), (-0.5, WY + 3.0, 1.3), 26, None, {}),
    "bench": ((-0.2, WY + 1.9, 1.55), (MX, MYW, 1.45), 40, 4.0, {}),
    "hall": ((3.0, CY - 36.0, 1.7), (0.0, CY, 6.0), 22, None, {}),
    "ropetop": ((1.2, CY - 2.8, TZ + 3.6), (0.0, CY, TZ + 3.9), 32, None, {}),
    "ropecut": ((1.2, CY - 2.8, TZ + 3.6), (0.0, CY, TZ + 3.9), 32, None, {"cut": True}),
    "platform": ((3.2, CY - 5.0, TZ + 1.8), (0.0, CY, TZ + 1.6), 30, None, {}),
    "mechA": ((1.6, CY - 8.5, TZ + 3.3), (0.0, CY, TZ + 2.4), 30, None, {}),
    "mechB": ((1.6, CY - 8.5, TZ + 3.3), (0.0, CY, TZ + 2.4), 30, None, {"mech": "B", "cut": True}),
}

os.makedirs(OUT, exist_ok=True)
camfile = os.path.join(OUT, "cams.json")
cams = json.load(open(camfile)) if os.path.exists(camfile) else {}
for name in SHOTS_WANTED:
    loc, target, lens, dof, ov = SHOTS[name]
    st = dict(STATE); st.update(ov); apply_state(st)
    place_cam(loc, target, lens, dof)
    bpy.context.view_layer.update()
    mi = cam.matrix_world.inverted()
    sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
    sc.cycles.samples = 24 if TEST else 80
    cams[name] = {"mi": [list(r) for r in mi], "lens": lens, "sensor_h": 24.0, "res": [1080, 1920], "still": True}
    json.dump(cams, open(camfile, "w"), indent=1)
    d = os.path.join(OUT, name); os.makedirs(d, exist_ok=True)
    sc.render.filepath = os.path.join(d, "still.png")
    t0 = time.time(); bpy.ops.render.render(write_still=True); print(name, "still", round(time.time() - t0, 1), "s", flush=True)
print("ALL DONE", flush=True)
