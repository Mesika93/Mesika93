"""The Great Diamond Hoax (1872): desert field + San Francisco bank. Still plates only.
usage: ../bvenv/bin/python scene_d.py -- OUTDIR shot1 [shot2 ...] [--test]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blib import *

rnd = random.Random(3)
def smooth(t): t = clamp(t); return t * t * (3 - 2 * t)

# ---------------- materials ----------------
M_GROUND = pbr("ground", "dry_ground_rocks", 0.12, tint=(1.0, 0.86, 0.7))
M_MESA = pbr("mesa", "dry_riverbed_rock", 0.03, tint=(1.0, 0.62, 0.42))
M_SAND = pbr("sand", "gravelly_sand", 2.5, tint=(1.0, 0.85, 0.68))
M_SNOW = pbr("snow", "snow_02", 0.3)
M_ROCK = pbr("rock", "dry_riverbed_rock", 0.3, tint=(0.8, 0.62, 0.5))
M_FLOOR = pbr("floor", "wood_floor_worn", 0.35, tint=(0.75, 0.55, 0.38))
M_WALL = pbr("wall", "painted_plaster_wall", 0.3, tint=(0.62, 0.72, 0.6))
M_LEATHER = pbr("leather", "brown_leather", 1.0, tint=(0.25, 0.45, 0.25))
M_VELVET = flat("velvet", (0.02, 0.03, 0.12), 0.95)
M_DESK = pbr("desk", "wood_floor_worn", 0.6, tint=(0.42, 0.22, 0.12), rough_mul=0.6)
M_SAGE = flat("sage", (0.1, 0.14, 0.06), 0.9)
M_SAGE2 = flat("sage2", (0.16, 0.17, 0.09), 0.9)
M_CANVAS = flat("canvas", (0.85, 0.8, 0.68), 0.85)
M_DARK = flat("dark", (0.03, 0.025, 0.02), 1.0)
M_BRASS = flat("brass", (0.8, 0.58, 0.25), 0.25, 1.0)
M_GOLD = flat("gold", (1.0, 0.72, 0.28), 0.18, 1.0)
M_IRON = flat("iron", (0.12, 0.12, 0.13), 0.4, 0.8)
M_BILL = flat("bill", (0.45, 0.55, 0.38), 0.8)
M_BAND = flat("band", (0.85, 0.8, 0.6), 0.7)
M_BURLAP = pbr("burlap", "hessian_230", 2.0, tint=(0.9, 0.75, 0.55), bump=2.0)
M_WINDOW = flat("window", (1.0, 0.93, 0.8), 0.5, emit=6.0)
M_LAMP = flat("lamp", (1.0, 0.8, 0.5), 0.5, emit=12.0)
M_TRIM = flat("trim", (0.22, 0.12, 0.07), 0.5)

def gem_mat(name, col, ior, rough=0.02):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["IOR"].default_value = ior; b.inputs["Transmission Weight"].default_value = 1.0
    try: b.inputs["Coat Weight"].default_value = 0.3
    except Exception: pass
    return m
M_DIAMOND = gem_mat("diamond", (1, 1, 1), 2.42)
M_RAW = gem_mat("raw", (0.95, 0.95, 0.9), 2.42, rough=0.18)
M_RUBY = gem_mat("ruby", (0.9, 0.04, 0.1), 1.77)
M_SAPPH = gem_mat("sapph", (0.08, 0.2, 0.95), 1.77)
M_EMER = gem_mat("emer", (0.05, 0.8, 0.3), 1.58)
M_LENS = gem_mat("lens", (1, 1, 1), 1.5)

# ---------------- meshes ----------------
def ico_mesh(name, sub, deform=0.0, seed=0):
    r = random.Random(seed)
    bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=sub, radius=1.0)
    for v in bm.verts: v.co *= 1 + deform * (r.random() - 0.5)
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free(); return me

def octa_mesh(name, seed):
    r = random.Random(seed)
    v = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1.15), (0, 0, -1.15)]
    v = [(a * r.uniform(.85, 1.15), b * r.uniform(.85, 1.15), c * r.uniform(.85, 1.15)) for a, b, c in v]
    f = [(0, 2, 4), (2, 1, 4), (1, 3, 4), (3, 0, 4), (2, 0, 5), (1, 2, 5), (3, 1, 5), (0, 3, 5)]
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.update(); return me

def hexprism_mesh(name):  # ruby / sapphire / emerald crystal
    v = []
    for z in (-1, 1):
        for k in range(6): a = k * math.pi / 3; v.append((math.cos(a) * 0.55, math.sin(a) * 0.55, z))
    v += [(0, 0, -1.25), (0, 0, 1.25)]
    f = [(k, (k + 1) % 6, 6 + (k + 1) % 6, 6 + k) for k in range(6)]
    f += [((k + 1) % 6, k, 12) for k in range(6)] + [(6 + k, 6 + (k + 1) % 6, 13) for k in range(6)]
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.update(); return me

def brilliant_mesh(name):
    n = 16; v = []; f = []
    for k in range(n): a = 2 * math.pi * k / n; v.append((math.cos(a), math.sin(a), 0))          # girdle 0..15
    for k in range(8): a = 2 * math.pi * k / 8 + math.pi / 8; v.append((0.55 * math.cos(a), 0.55 * math.sin(a), 0.42))  # table 16..23
    v.append((0, 0, -0.95))  # culet 24
    f.append(tuple(range(16, 24)))
    for k in range(8):
        g0, g1, g2 = 2 * k, 2 * k + 1, (2 * k + 2) % n
        t0, t1 = 16 + k, 16 + (k + 1) % 8
        f.append((g0, g1, t0)); f.append((g1, g2, t1, t0))
    for k in range(n): f.append(((k + 1) % n, k, 24))
    me = bpy.data.meshes.new(name); me.from_pydata(v, [], f); me.update(); return me

ROCK_MES = [ico_mesh(f"rock{i}", 2, 0.5, i) for i in range(4)]
for m in ROCK_MES: m.materials.append(M_ROCK)
SAGE_MES = [ico_mesh(f"sage{i}", 2, 0.6, 10 + i) for i in range(3)]
for i, m in enumerate(SAGE_MES): m.materials.append(M_SAGE if i % 2 else M_SAGE2)
RAW_MES = [octa_mesh(f"raw{i}", i) for i in range(5)]
for m in RAW_MES: m.materials.append(M_RAW)
HEX = {c: hexprism_mesh(f"hex_{c}") for c in ("ruby", "sapph", "emer")}
HEX["ruby"].materials.append(M_RUBY); HEX["sapph"].materials.append(M_SAPPH); HEX["emer"].materials.append(M_EMER)
BRIL = brilliant_mesh("bril"); BRIL.materials.append(M_DIAMOND)

def inst(me, loc, scale, rot=(0, 0, 0), smooth=False):
    o = bpy.data.objects.new(me.name, me); sc.collection.objects.link(o)
    o.location = loc; o.scale = scale if isinstance(scale, tuple) else (scale,) * 3; o.rotation_euler = rot
    if smooth: shade_smooth(o)
    return o

def rrot(): return (rnd.uniform(0, 6.3), rnd.uniform(0, 6.3), rnd.uniform(0, 6.3))

# ---------------- world (desert) ----------------
w = bpy.data.worlds.new("sky"); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes["Background"]
env = node(nt, "ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(os.path.join(A, "desert.hdr"))
mp = node(nt, "ShaderNodeMapping"); tc = node(nt, "ShaderNodeTexCoord")
mp.inputs["Rotation"].default_value = (0, 0, math.radians(120))
nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
nt.links.new(env.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 0.9
sun_d = bpy.data.lights.new("sun", "SUN"); sun_d.energy = 4.0; sun_d.angle = math.radians(1.0)
sun_d.color = (1.0, 0.9, 0.78)
sun = bpy.data.objects.new("sun", sun_d); sc.collection.objects.link(sun)
sun.rotation_euler = Euler((math.radians(58), 0, math.radians(-35)))

# terrain: flat basin with gentle swell, mesas in the distance
def terrain_h(x, y):
    r = math.hypot(x, y)
    h = 0.35 * math.sin(x * 0.07) * math.sin(y * 0.05 + 1) * smooth((r - 45) / 30)
    h += 6 * smooth((r - 120) / 120)
    h += 4 * smooth((r - 300) / 100)
    return h
N = 200; SZ = 1100.0
verts = [(-SZ / 2 + SZ * i / N, -SZ / 2 + SZ * j / N) for j in range(N + 1) for i in range(N + 1)]
verts = [(x, y, terrain_h(x, y)) for x, y in verts]
faces = [(j * (N + 1) + i, j * (N + 1) + i + 1, (j + 1) * (N + 1) + i + 1, (j + 1) * (N + 1) + i) for j in range(N) for i in range(N)]
terr = obj_from("terrain", verts, faces, M_GROUND); shade_smooth(terr)

def mesa(cx, cy, rad, hgt, seed):
    r = random.Random(seed); n = 28; V = []; F = []
    rads = [rad * (0.75 + 0.35 * r.random()) for _ in range(n)]
    levels = [(-2, 1.25), (hgt * 0.55, 1.08), (hgt * 0.9, 1.0), (hgt, 0.97)]
    for z, s in levels:
        for k in range(n):
            a = 2 * math.pi * k / n; rr = rads[k] * s * (1 + 0.05 * r.random())
            V.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr, z))
    for l in range(len(levels) - 1):
        for k in range(n): F.append((l * n + k, l * n + (k + 1) % n, (l + 1) * n + (k + 1) % n, (l + 1) * n + k))
    F.append(tuple(range(3 * n, 4 * n)))
    obj_from(f"mesa{seed}", V, F, M_MESA)
for k, (cx, cy, rad, hgt) in enumerate([(-90, 230, 60, 55), (60, 260, 45, 70), (170, 190, 50, 40), (-200, 150, 55, 45),
                                         (230, 60, 40, 50), (-20, 330, 70, 60), (-260, -40, 50, 35), (120, -260, 60, 45)]):
    mesa(cx * 1.9, cy * 1.9, rad * 1.3, hgt * 0.9, k)

# scatter: sagebrush, rocks, snow patches
placed = 0
while placed < 2200:
    x = rnd.uniform(-160, 160); y = rnd.uniform(-60, 200)
    if math.hypot(x - 0, y - 0) < 2.5 or math.hypot(x - 30, y - 4) < 2.5: continue
    if abs(x - 0.0) < 1.3 and -6 < y < 2: continue
    s = rnd.uniform(0.25, 0.7)
    inst(rnd.choice(SAGE_MES), (x, y, terrain_h(x, y) + s * 0.35), (s, s, s * 0.65), smooth=True); placed += 1
for _ in range(500):
    x = rnd.uniform(-120, 120); y = rnd.uniform(-40, 160); s = rnd.uniform(0.08, 0.6)
    if math.hypot(x, y) < 1.5: continue
    inst(rnd.choice(ROCK_MES), (x, y, terrain_h(x, y) + s * 0.1), (s, s * 0.8, s * 0.5), rrot(), smooth=True)
snow_me = ico_mesh("snowp", 2, 0.3, 99); snow_me.materials.append(M_SNOW)
for _ in range(160):
    x = rnd.uniform(-150, 150); y = rnd.uniform(-30, 200)
    if math.hypot(x, y) < 5 or math.hypot(x - 30, y - 4) < 4: continue
    s = rnd.uniform(0.8, 4.0); inst(snow_me, (x, y, terrain_h(x, y) - 0.02), (s, s * rnd.uniform(.5, 1.2), 0.06), (0, 0, rnd.uniform(0, 3)), smooth=True)

# camp: tents up the valley
def tent(x, y, rot, s=1.0):
    V = [(-1.4, -1.6, 0), (1.4, -1.6, 0), (1.4, 1.6, 0), (-1.4, 1.6, 0), (0, -1.6, 2.1), (0, 1.6, 2.1)]
    V = [(a * s, b * s, c * s) for a, b, c in V]
    F = [(0, 3, 5, 4), (1, 4, 5, 2), (0, 4, 1), (3, 2, 5)]
    o = obj_from("tent", V, F, M_CANVAS, (x, y, terrain_h(x, y))); o.rotation_euler = (0, 0, rot)
for x, y, r in [(-6, 22, 0.3), (-1, 26, -0.2), (5, 21, 0.5), (12, 27, 0.1), (-12, 30, 0.8)]:
    tent(x, y, r)

# ---- set A: anthill with salted diamond (origin) ----
def anthill(cx, cy, rad, hgt, seed):
    r = random.Random(seed); n = 36; rings = 9; V = [(cx, cy, hgt)]; F = []
    for j in range(1, rings + 1):
        rr = rad * j / rings
        for k in range(n):
            a = 2 * math.pi * k / n; q = rr * (1 + 0.08 * math.sin(a * 5 + seed) + 0.04 * r.random())
            z = hgt * (1 - (j / rings) ** 1.6) + 0.012 * r.random()
            V.append((cx + math.cos(a) * q, cy + math.sin(a) * q, z))
    for k in range(n): F.append((0, 1 + k, 1 + (k + 1) % n))
    for j in range(rings - 1):
        for k in range(n):
            a0 = 1 + j * n; a1 = 1 + (j + 1) * n
            F.append((a0 + k, a1 + k, a1 + (k + 1) % n, a0 + (k + 1) % n))
    o = obj_from("anthill", V, F, M_SAND); shade_smooth(o); return o
anthill(0, 0, 0.75, 0.32, 1)
hole = inst(ico_mesh("hole", 2), (0.0, 0.0, 0.318), (0.045, 0.045, 0.012)); hole.data.materials.append(M_DARK)
# stick hole + jammed diamond
def ah_z(x, y, rad=0.75, hgt=0.32): return hgt * (1 - min(1, math.hypot(x, y) / rad) ** 1.6)
stick_hole = inst(ico_mesh("shole", 2), (0.2, -0.12, ah_z(0.2, -0.12) - 0.006), (0.02, 0.02, 0.008), (0.45, 0, 0)); stick_hole.data.materials.append(M_DARK)
inst(RAW_MES[0], (0.13, -0.17, ah_z(0.13, -0.17) + 0.018), 0.03, (0.4, 0.2, 0.7))
inst(RAW_MES[1], (-0.25, -0.3, ah_z(-0.25, -0.3) + 0.012), 0.022, (1.0, 0.3, 0.2))
# a second anthill nearby
anthill(-1.8, 1.2, 0.6, 0.25, 2)

# ---- set B: mixed gems in a patch of dirt (x=30) ----
GX, GY = 30.0, 4.0
anthill(GX, GY, 1.2, 0.05, 5)
for k, (dx, dy, kind) in enumerate([(0, 0, "raw"), (0.07, 0.05, "ruby"), (-0.06, 0.04, "sapph"), (0.04, -0.07, "emer"),
                                    (-0.1, -0.04, "ruby"), (0.12, -0.02, "raw"), (-0.02, 0.11, "emer"), (0.1, 0.1, "sapph"),
                                    (-0.13, 0.09, "raw"), (0.02, -0.14, "ruby")]):
    z = GZ = 0.05
    if kind == "raw": inst(RAW_MES[k % 5], (GX + dx, GY + dy, GZ + 0.012), 0.016, rrot())
    else: inst(HEX[kind], (GX + dx, GY + dy, GZ + 0.008), (0.013, 0.013, 0.018), (math.radians(80), 0, rnd.uniform(0, 3)))
# cut diamond lying among raw ones
CX, CY = GX + 0.6, GY - 0.3
inst(BRIL, (CX, CY, 0.05 + 0.02), 0.03, (math.radians(-25), math.radians(10), 0.3))
inst(RAW_MES[2], (CX - 0.07, CY + 0.04, 0.062), 0.018, rrot())
inst(RAW_MES[3], (CX + 0.06, CY + 0.06, 0.062), 0.014, rrot())

# ---------------- bank interior (y = 1000) ----------------
BY = 1000.0; DY = BY + 2.0; DZ = 0.82
def room():
    multi_box("bankfloor", [((-8, BY - 8, -0.2), (8, BY + 8, 0))], M_FLOOR)
    multi_box("bankwalls", [((-8.2, BY + 8, 0), (8.2, BY + 8.3, 6)), ((-8.3, BY - 8, 0), (-8, BY + 8, 6)),
                            ((8, BY - 8, 0), (8.3, BY + 8, 6)), ((-8.2, BY - 8.3, 0), (8.2, BY - 8, 6))], M_WALL)
    multi_box("ceil", [((-8.3, BY - 8.3, 6), (8.3, BY + 8.3, 6.3))], M_TRIM)
    multi_box("wainscot", [((-8, BY + 7.85, 0), (8, BY + 8, 1.2)), ((-8, BY - 8, 0), (-7.85, BY + 8, 1.2)),
                           ((7.85, BY - 8, 0), (8, BY + 8, 1.2))], M_TRIM)
    for x in (-5.5, -1.8, 1.8, 5.5):   # tall windows on back wall
        multi_box("win", [((x - 0.8, BY + 7.95, 1.6), (x + 0.8, BY + 7.99, 5.2))], M_WINDOW)
        multi_box("winframe", [((x - 0.9, BY + 7.9, 1.5), (x + 0.9, BY + 7.95, 1.6)), ((x - 0.9, BY + 7.9, 5.2), (x + 0.9, BY + 7.95, 5.3)),
                               ((x - 0.04, BY + 7.9, 1.6), (x + 0.04, BY + 7.95, 5.2)), ((x - 0.8, BY + 7.9, 3.35), (x + 0.8, BY + 7.95, 3.45))], M_TRIM)
    for x in (-3.6, 3.6):   # columns
        bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.35, depth=6, location=(x, BY + 4.5, 3))
        c = bpy.context.object; c.data.materials.append(M_WALL); shade_smooth(c)
    # safe on the right
    multi_box("safe", [((5.2, BY + 6.0, 0), (7.2, BY + 7.6, 2.4))], M_IRON)
    bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.28, depth=0.08, location=(6.2, BY + 5.97, 1.4), rotation=(math.radians(90), 0, 0))
    bpy.context.object.data.materials.append(M_BRASS)
    # counter on the left
    multi_box("counter", [((-7.8, BY - 2, 0), (-6.6, BY + 6, 1.15)), ((-7.9, BY - 2, 1.15), (-6.5, BY + 6, 1.25))], M_DESK)
    # interior light
    for x, y in ((-3, BY + 1), (3, BY + 1), (0, BY - 4)):
        L = bpy.data.lights.new("pt", "POINT"); L.energy = 900; L.color = (1.0, 0.82, 0.6); L.shadow_soft_size = 0.6
        o = bpy.data.objects.new("pt", L); o.location = (x, y, 5.2); sc.collection.objects.link(o)
    a = bpy.data.lights.new("winarea", "AREA"); a.energy = 2500; a.size = 14; a.color = (1.0, 0.95, 0.85)
    o = bpy.data.objects.new("winarea", a); o.location = (0, BY + 7.5, 3.4); o.rotation_euler = (math.radians(-90), 0, 0); sc.collection.objects.link(o)
room()
M_RUG = flat("rug", (0.16, 0.03, 0.03), 0.95)
multi_box("rug", [((-2.4, BY - 0.5, 0), (2.4, BY + 4.5, 0.015))], M_RUG)
M_PAINT = [flat(f"paint{i}", c, 0.6) for i, c in enumerate([(0.3, 0.22, 0.12), (0.12, 0.2, 0.25), (0.35, 0.3, 0.15)])]
for k, x in enumerate((-7.95, 7.95)):
    for j, y in enumerate((BY - 3, BY + 1.5)):
        sgn = 1 if x < 0 else -1
        multi_box("frame", [((x, y - 0.9, 2.0), (x + sgn * 0.08, y + 0.9, 3.6))], M_BRASS)
        multi_box("canvas", [((x + sgn * 0.08, y - 0.78, 2.12), (x + sgn * 0.1, y + 0.78, 3.48))], M_PAINT[(k + j) % 3])
for x in (-1.0, 1.0):   # chairs
    multi_box("chair", [((x - 0.25, DY + 1.0, 0), (x + 0.25, DY + 1.5, 0.48)), ((x - 0.25, DY + 1.4, 0.48), (x + 0.25, DY + 1.5, 1.2))], M_LEATHER)
bpy.ops.mesh.primitive_torus_add(major_radius=0.9, minor_radius=0.05, location=(0, BY + 1, 4.6))
bpy.context.object.data.materials.append(M_BRASS)
for k in range(8):
    a = k * math.pi / 4
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(0.9 * math.cos(a), BY + 1 + 0.9 * math.sin(a), 4.7))
    bpy.context.object.data.materials.append(M_LAMP)
# desk
DY = BY + 2.0; DZ = 0.82
multi_box("desk", [((-1.6, DY - 0.8, 0.75), (1.6, DY + 0.8, DZ - 0.02)), ((-1.5, DY - 0.7, 0), (-0.7, DY + 0.7, 0.75)),
                   ((0.7, DY - 0.7, 0), (1.5, DY + 0.7, 0.75))], M_DESK)
multi_box("deskleather", [((-1.45, DY - 0.65, DZ - 0.02), (1.45, DY + 0.65, DZ))], M_LEATHER)
# desk lamp
bpy.ops.mesh.primitive_cylinder_add(vertices=24, radius=0.12, depth=0.03, location=(1.15, DY + 0.4, DZ + 0.015)); bpy.context.object.data.materials.append(M_BRASS)
bpy.ops.mesh.primitive_cylinder_add(vertices=12, radius=0.015, depth=0.45, location=(1.15, DY + 0.4, DZ + 0.24)); bpy.context.object.data.materials.append(M_BRASS)
bpy.ops.mesh.primitive_cone_add(vertices=24, radius1=0.2, radius2=0.08, depth=0.16, location=(1.15, DY + 0.4, DZ + 0.5)); bpy.context.object.data.materials.append(M_LEATHER)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(1.15, DY + 0.4, DZ + 0.44)); bpy.context.object.data.materials.append(M_LAMP)
# sack of diamonds (left of desk)
SX, SY = -0.55, DY - 0.05
sack_me = ico_mesh("sack", 4, 0.05, 4); sack_me.materials.append(M_BURLAP)
for v in sack_me.vertices:
    if v.co.z > 0.3: f = 1 - 0.75 * (v.co.z - 0.3) / 0.7; v.co.x *= f; v.co.y *= f
inst(sack_me, (SX, SY, DZ + 0.2), (0.2, 0.18, 0.21), (0, 0.15, 0.3), smooth=True)
bpy.ops.mesh.primitive_torus_add(major_radius=0.06, minor_radius=0.012, location=(SX + 0.03, SY, DZ + 0.39))
bpy.context.object.data.materials.append(M_BURLAP)
bpy.ops.mesh.primitive_cone_add(vertices=10, radius1=0.05, radius2=0.11, depth=0.1, location=(SX + 0.035, SY, DZ + 0.44))
o = bpy.context.object; o.data.materials.append(M_BURLAP)
for v in o.data.vertices:
    if v.co.z > 0: v.co.x += 0.02 * math.sin(v.co.y * 90); v.co.z += 0.015 * math.cos(v.co.x * 70)
for k in range(46):  # spill
    a = rnd.uniform(-1.1, 0.4); rr = 0.2 + abs(rnd.gauss(0, 0.16))
    x = SX + 0.1 + math.cos(a) * rr; y = SY + math.sin(a) * rr * 0.8
    m = RAW_MES[k % 5] if k % 9 else HEX["ruby"]
    s = rnd.uniform(0.018, 0.032)
    inst(m, (x, y, DZ + s * 0.9), s if m in RAW_MES else (s * .8, s * .8, s), rrot())
# velvet tray + loupe (right side of desk)
VX, VY = 0.45, DY - 0.1
multi_box("tray", [((VX - 0.22, VY - 0.15, DZ), (VX + 0.22, VY + 0.15, DZ + 0.025))], M_VELVET)
for k, (dx, dy) in enumerate([(-0.1, -0.05), (0.0, 0.04), (0.1, -0.03), (-0.05, 0.08), (0.12, 0.08)]):
    inst(RAW_MES[k], (VX + dx, VY + dy, DZ + 0.04), 0.016, rrot())
bpy.ops.mesh.primitive_torus_add(major_radius=0.045, minor_radius=0.008, location=(VX - 0.02, VY - 0.07, DZ + 0.065), rotation=(math.radians(20), 0, 0))
bpy.context.object.data.materials.append(M_BRASS)
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.042, depth=0.006, location=(VX - 0.02, VY - 0.07, DZ + 0.065), rotation=(math.radians(20), 0, 0))
bpy.context.object.data.materials.append(M_LENS)
# money: second desk (x = +4) stacks of gold coins & bills
MX, MY = 4.2, BY + 1.0
multi_box("desk2", [((MX - 1.4, MY - 0.7, 0.75), (MX + 1.4, MY + 0.7, DZ)), ((MX - 1.3, MY - 0.6, 0), (MX + 1.3, MY + 0.6, 0.75))], M_DESK)
coin_me = bpy.data.meshes.new("coin")
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=32, radius1=0.03, radius2=0.03, depth=0.004); bm.to_mesh(coin_me); bm.free()
coin_me.materials.append(M_GOLD)
for sx in range(-6, 7):
    for sy in range(-3, 4):
        if rnd.random() < 0.25: continue
        x = MX + sx * 0.085 + rnd.uniform(-.01, .01); y = MY + sy * 0.085 + rnd.uniform(-.01, .01)
        n = rnd.randint(6, 28)
        for k in range(n):
            inst(coin_me, (x + rnd.uniform(-.003, .003), y + rnd.uniform(-.003, .003), DZ + 0.002 + k * 0.0043), 1.0, (0, 0, rnd.uniform(0, 6)))
for k in range(10):
    x = MX + rnd.uniform(-1.1, 1.1); y = MY + rnd.choice([-0.55, 0.5]) + rnd.uniform(-.05, .05)
    h = rnd.randint(1, 3)
    for j in range(h):
        o = multi_box("bills", [((-0.08, -0.035, 0), (0.08, 0.035, 0.03))], M_BILL, (x, y, DZ + j * 0.03))
        o.rotation_euler = (0, 0, rnd.uniform(-.3, .3))
        multi_box("band", [((-0.012, -0.036, -0.001), (0.012, 0.036, 0.031))], M_BAND, (x, y, DZ + j * 0.03)).rotation_euler = o.rotation_euler

# ---------------- shots ----------------
SHOTS = {
    # name: (loc, target, lens, dof)
    "anthill": ((0.9, -2.6, 0.75), (0.0, 0.0, 0.5), 24, None),
    "antmacro": ((0.3, -0.62, 0.5), (0.15, -0.15, 0.25), 55, 4.0),
    "wide": ((2.0, -14.0, 1.9), (0.0, 30.0, 3.5), 22, None),
    "field": ((6.0, -6.5, 1.65), (2.0, 4.0, 1.0), 28, None),
    "trail": ((-25.0, -10.0, 1.5), (-5.0, 40.0, 3.0), 24, None),
    "gems": ((GX + 0.02, GY - 0.3, 0.5), (GX, GY + 0.01, 0.05), 45, 5.6),
    "cut": ((CX + 0.06, CY - 0.22, 0.2), (CX, CY, 0.07), 60, 4.0),
    "bank": ((-0.6, BY - 4.2, 1.6), (0.0, BY + 3.0, 1.5), 24, None),
    "sack": ((SX + 0.38, SY - 1.1, DZ + 0.6), (SX + 0.12, SY - 0.1, DZ + 0.13), 30, 5.6),
    "velvet": ((VX + 0.08, VY - 0.55, DZ + 0.42), (VX + 0.02, VY + 0.01, DZ + 0.03), 40, 5.6),
    "money": ((MX - 0.3, MY - 1.6, DZ + 0.75), (MX, MY, DZ + 0.05), 35, 8.0),
}

os.makedirs(OUT, exist_ok=True)
camfile = os.path.join(OUT, "cams.json")
cams = json.load(open(camfile)) if os.path.exists(camfile) else {}
for name in SHOTS_WANTED:
    loc, target, lens, dof = SHOTS[name]
    place_cam(loc, target, lens, dof)
    bpy.context.view_layer.update()
    mi = cam.matrix_world.inverted()
    sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
    sc.cycles.samples = 24 if TEST else 96
    cams[name] = {"mi": [list(r) for r in mi], "lens": lens, "sensor_h": 24.0, "res": [1080, 1920], "still": True}
    json.dump(cams, open(camfile, "w"), indent=1)
    d = os.path.join(OUT, name); os.makedirs(d, exist_ok=True)
    sc.render.filepath = os.path.join(d, "still.png")
    t0 = time.time(); bpy.ops.render.render(write_still=True); print(name, "still", round(time.time() - t0, 1), "s", flush=True)
print("ALL DONE", flush=True)
