"""Abraham Wald / survivorship bias: airfield, bomber with bullet holes, sky, briefing room. Still plates.
usage: ../bvenv/bin/python scene_w.py -- OUTDIR shot1 [shot2 ...] [--test]
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "p2"))
from blib import *
HERE = os.path.dirname(os.path.abspath(__file__))
rnd = random.Random(5)

# ---------------- materials ----------------
M_CONC = pbr("conc", "concrete_floor_worn_001", 0.12, tint=(0.72, 0.7, 0.64))
M_GRASS = pbr("grass", "aerial_grass_rock", 0.04, tint=(0.7, 0.8, 0.55))
M_SHEET = pbr("sheet", "concrete_floor_worn_001", 0.1, tint=(0.55, 0.56, 0.52), metal=0.6, rough_mul=0.7)
def olive():
    m = pbr("olive", "concrete_floor_worn_001", 0.25, tint=(0.36, 0.38, 0.17), metal=0.25, rough_mul=0.8, bump=0.3)
    return m
M_OD = olive()
M_GREYB = pbr("belly", "blue_metal_plate", 0.6, tint=(0.75, 0.75, 0.72), metal=0.5)
M_GLASS = flat("glass", (0.05, 0.08, 0.1), 0.05, 0.5)
M_BLACK = flat("blk", (0.02, 0.02, 0.02), 0.6)
M_HOLE = flat("hole", (0.005, 0.005, 0.005), 1.0)
M_RIM = flat("rim", (0.42, 0.4, 0.37), 0.45, 1.0)
M_TIRE = flat("tire", (0.03, 0.03, 0.03), 0.8)
M_PROP = flat("prop", (0.03, 0.03, 0.03), 0.4, 0.5)
M_STAR = flat("star", (0.9, 0.9, 0.9), 0.6)
M_BLUE = flat("blue", (0.05, 0.1, 0.35), 0.6)
M_FLAK = flat("flak", (0.06, 0.06, 0.06), 1.0)
M_WALL = pbr("wall", "painted_plaster_wall", 0.3, tint=(0.75, 0.72, 0.6))
M_FLOOR = pbr("floor", "wood_floor_worn", 0.35, tint=(0.6, 0.45, 0.3))
M_BOARD = flat("board", (0.06, 0.12, 0.08), 0.85)
M_DESK = pbr("desk", "wood_floor_worn", 0.6, tint=(0.42, 0.22, 0.12), rough_mul=0.6)
M_WINDOW = flat("window", (1.0, 0.95, 0.85), 0.5, emit=5.0)
M_MAP = flat("map", (0.75, 0.68, 0.5), 0.8)
M_LAMP = flat("lamp", (1.0, 0.85, 0.6), 0.5, emit=10.0)
M_TRIM = flat("trim", (0.2, 0.13, 0.08), 0.5)

# ---------------- world ----------------
w = bpy.data.worlds.new("sky"); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes["Background"]
env = node(nt, "ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(os.path.join(A, "clouds.hdr"))
mp = node(nt, "ShaderNodeMapping"); tc = node(nt, "ShaderNodeTexCoord")
mp.inputs["Rotation"].default_value = (0, 0, math.radians(60))
nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
nt.links.new(env.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 1.0
sun_d = bpy.data.lights.new("sun", "SUN"); sun_d.energy = 3.5; sun_d.angle = math.radians(1.5); sun_d.color = (1.0, 0.94, 0.85)
sun = bpy.data.objects.new("sun", sun_d); sc.collection.objects.link(sun)
sun.rotation_euler = Euler((math.radians(45), 0, math.radians(-40)))

# ---------------- bomber ----------------
def loft(name, rings, mat, cap=True):
    """rings: list of lists of (x,y,z) with equal counts"""
    n = len(rings[0]); V = [p for r in rings for p in r]; F = []
    for j in range(len(rings) - 1):
        for k in range(n): F.append((j * n + k, j * n + (k + 1) % n, (j + 1) * n + (k + 1) % n, (j + 1) * n + k))
    if cap: F.append(tuple(range(n))[::-1]); F.append(tuple(range((len(rings) - 1) * n, len(rings) * n)))
    o = obj_from(name, V, F, mat); shade_smooth(o); return o

def fus_r(y):
    # nose at +11.5, tail at -11
    if y > 8: return 1.15 * math.sqrt(max(0.0, 1 - ((y - 8) / 3.6) ** 2)) + 0.02
    if y > -3: return 1.15
    return 1.15 - 0.9 * ((-3 - y) / 8) ** 1.3

FZ = 2.8          # fuselage axis height when parked
WZ = 2.55         # wing height
def wing_pts(side, span, root_c, tip_c, y_le_root, sweep, z0, thick):
    """returns rings for a wing as loft along x"""
    rings = []
    for k in range(9):
        u = k / 8; x = side * (1.1 + (span - 1.1) * u); c = lerp(root_c, tip_c, u)
        yle = y_le_root - sweep * u; th = thick * lerp(1, 0.45, u); z = z0 + 0.35 * u
        prof = [(0, 0), (0.03, 0.6), (0.15, 0.95), (0.4, 1.0), (0.7, 0.6), (1.0, 0.05), (0.7, -0.35), (0.4, -0.5), (0.15, -0.45), (0.03, -0.3)]
        ring = [(x, yle - c * a, z + th * b) for a, b in prof]
        if side < 0: ring = ring[::-1]
        rings.append(ring)
    return rings

def lerp(a, b, t): return a + (b - a) * t

ENG_X = [-8.6, -4.2, 4.2, 8.6]
def bomber(ox, oy, oz, holes=True, rot=0.0, gear=True):
    objs = []
    rings = []
    for k in range(41):
        y = 11.5 - 22.5 * k / 40; r = fus_r(y)
        zc = FZ + (0.25 * ((-3 - y) / 8) if y < -3 else 0)
        ring = [(r * math.cos(a), y, zc + r * 1.05 * math.sin(a)) for a in [i * 2 * math.pi / 24 for i in range(24)]]
        rings.append(ring)
    objs.append(loft("fus", rings, M_OD))
    objs.append(loft("wingR", wing_pts(1, 15.8, 5.6, 2.0, 4.6, 1.6, WZ, 0.55), M_OD))
    objs.append(loft("wingL", wing_pts(-1, 15.8, 5.6, 2.0, 4.6, 1.6, WZ, 0.55), M_OD))
    for side in (1, -1):   # horizontal stabilizers
        rr = []
        for k in range(5):
            u = k / 4; x = side * (0.6 + 5.2 * u); c = lerp(3.2, 1.3, u); yle = -7.6 - 1.2 * u
            prof = [(0, 0), (0.1, 0.8), (0.4, 1.0), (1.0, 0.0), (0.4, -0.7), (0.1, -0.6)]
            ring = [(x, yle - c * a, FZ + 0.4 + 0.18 * b) for a, b in prof]
            rr.append(ring if side > 0 else ring[::-1])
        objs.append(loft("stab", rr, M_OD))
    rr = []   # vertical fin
    for k in range(6):
        u = k / 5; z = FZ + 0.8 + 4.0 * u; c = lerp(6.5, 1.6, u); yle = -4.5 - 5.0 * u ** 0.8
        prof = [(0, 0), (0.1, 1), (0.4, 1.2), (1.0, 0), (0.4, -1.2), (0.1, -1)]
        rr.append([(0.16 * b * (1 - 0.5 * u), yle - c * a, z) for a, b in prof])
    objs.append(loft("fin", rr, M_OD))
    # cockpit glass + nose
    o = box("cockpit", (-0.75, 6.2, FZ + 0.85), (0.75, 7.6, FZ + 1.3), M_GLASS); objs.append(o)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.62, location=(0, 11.0, FZ)); o = bpy.context.object
    o.scale = (1, 0.9, 1); o.data.materials.append(M_GLASS); shade_smooth(o); objs.append(o)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.55, location=(0, 1.0, FZ + 1.15)); o = bpy.context.object  # top turret
    o.data.materials.append(M_GLASS); shade_smooth(o); objs.append(o)
    # engines
    for ex in ENG_X:
        ylead = 4.6 - 1.6 * (abs(ex) - 1.1) / 14.7 + 0.3; zc = WZ + 0.35 * (abs(ex) - 1.1) / 14.7 + 0.1
        rr = []
        for k in range(9):
            y = ylead + 1.2 - 5.0 * k / 8; rad = 0.72 * (1 - 0.6 * (k / 8) ** 2)
            if k == 0: rad = 0.55
            rr.append([(ex + rad * math.cos(a), y, zc + rad * math.sin(a)) for a in [i * 2 * math.pi / 20 for i in range(20)]])
        objs.append(loft("nacelle", rr, M_OD))
        bpy.ops.mesh.primitive_cone_add(vertices=16, radius1=0.3, depth=0.5, location=(ex, ylead + 1.45, zc), rotation=(math.radians(-90), 0, 0))
        o = bpy.context.object; o.data.materials.append(M_BLACK); objs.append(o)
        for b in range(3):
            a = b * 2 * math.pi / 3 + ex
            o = box("blade", (-0.11, -0.03, 0.0), (0.11, 0.03, 1.85), M_PROP); o.location = (ex, ylead + 1.35, zc)
            o.rotation_euler = (0, a, 0); objs.append(o)
        if gear and abs(ex) < 5:
            o = box("strut", (-0.1, -0.1, 0.6), (0.1, 0.1, zc - 0.4), M_BLACK); o.location = (ex, ylead - 0.8, 0); objs.append(o)
            bpy.ops.mesh.primitive_torus_add(major_radius=0.45, minor_radius=0.2, location=(ex, ylead - 0.8, 0.65), rotation=(0, math.radians(90), 0))
            o = bpy.context.object; o.data.materials.append(M_TIRE); shade_smooth(o); objs.append(o)
    if gear:
        bpy.ops.mesh.primitive_torus_add(major_radius=0.22, minor_radius=0.1, location=(0, -8.6, 0.32), rotation=(0, math.radians(90), 0))
        o = bpy.context.object; o.data.materials.append(M_TIRE); objs.append(o)
        o = box("tstrut", (-0.06, -0.06, 0.3), (0.06, 0.06, 1.9), M_BLACK); o.location = (0, -8.6, 0); objs.append(o)
    # insignia (white star on blue disc) on fuselage sides
    for s in (1, -1):
        bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=0.75, depth=0.02, location=(s * 1.16, -5.0, FZ), rotation=(0, math.radians(90), 0))
        o = bpy.context.object; o.data.materials.append(M_BLUE); objs.append(o)
        V = []
        for k in range(10):
            r = 0.68 if k % 2 == 0 else 0.27; a = math.pi / 2 + k * math.pi / 5
            V.append((s * 1.18, -5.0 + r * math.cos(a), FZ + r * math.sin(a)))
        V.append((s * 1.18, -5.0, FZ)); F = [(10, k, (k + 1) % 10) if s > 0 else (10, (k + 1) % 10, k) for k in range(10)]
        objs.append(obj_from("star", V, F, M_STAR))
    hole_list = []
    if holes:
        hr = random.Random(21)
        def hole(p, normal):
            nx, ny, nz = normal
            bpy.ops.mesh.primitive_cylinder_add(vertices=10, radius=hr.uniform(0.05, 0.09), depth=0.04, location=p)
            o = bpy.context.object; o.data.materials.append(M_HOLE)
            o.rotation_euler = Vector(normal).to_track_quat("Z", "Y").to_euler(); objs.append(o)
            bpy.ops.mesh.primitive_torus_add(major_radius=0.095, minor_radius=0.016, location=p)
            o = bpy.context.object; o.data.materials.append(M_RIM); o.rotation_euler = Vector(normal).to_track_quat("Z", "Y").to_euler(); objs.append(o)
        # wings (top surface), avoid engine nacelles
        cnt = 0
        while cnt < 70:
            side = hr.choice((-1, 1)); u = hr.uniform(0.0, 0.95); x = side * (1.1 + 14.7 * u)
            if any(abs(x - ex) < 1.0 for ex in ENG_X): continue
            c = lerp(5.6, 2.0, u); yle = 4.6 - 1.6 * u; y = yle - c * hr.uniform(0.15, 0.8)
            z = WZ + 0.35 * u + 0.55 * lerp(1, 0.45, u) * 0.92
            hole((x, y, z), (0, 0, 1)); hole_list.append(("wing", x, y, z)); cnt += 1
        for _ in range(48):   # fuselage
            y = hr.uniform(-6.5, 5.5); a = hr.uniform(-0.6, 2.0) * hr.choice((1, -1)) + (0 if hr.random() < 0.5 else math.pi)
            r = fus_r(y) * 1.0; zc = FZ + (0.25 * ((-3 - y) / 8) if y < -3 else 0)
            p = (r * math.cos(a), y, zc + r * 1.05 * math.sin(a))
            if math.hypot(p[0] - 1.16, (p[1] + 5) * 1) < 0.9 or math.hypot(p[0] + 1.16, (p[1] + 5)) < 0.9: continue
            hole(p, (math.cos(a), 0, math.sin(a))); hole_list.append(("body", *p))
        for _ in range(26):   # tail stabilizers
            side = hr.choice((-1, 1)); u = hr.uniform(0.05, 0.9); x = side * (0.6 + 5.2 * u)
            c = lerp(3.2, 1.3, u); y = -7.6 - 1.2 * u - c * hr.uniform(0.15, 0.7)
            hole((x, y, FZ + 0.4 + 0.18 * 0.9), (0, 0, 1)); hole_list.append(("tail", x, y, FZ + 0.56))
        for _ in range(8):    # fin
            u = hr.uniform(0.1, 0.8); z = FZ + 0.8 + 4.0 * u; y = -4.5 - 5.0 * u ** 0.8 - lerp(6.5, 1.6, u) * hr.uniform(0.2, 0.6)
            hole((0.15 * (1 - 0.5 * u), y, z), (1, 0, 0)); hole_list.append(("tail", 0.15, y, z))
    root = bpy.data.objects.new("bomber_root", None); sc.collection.objects.link(root)
    for o in objs: o.parent = root
    root.location = (ox, oy, oz); root.rotation_euler = (0, 0, rot)
    return root, hole_list

_, HOLES = bomber(0, 0, 0, holes=True)
json.dump(HOLES, open(os.path.join(HERE, "holes.json"), "w"))

# ---------------- airfield ----------------
multi_box("apron", [((-60, -60, -0.3), (60, 60, 0.0))], M_CONC)
obj_from("grassland", [(-600, -600, -0.05), (600, -600, -0.05), (600, 600, -0.05), (-600, 600, -0.05)], [(0, 1, 2, 3)], M_GRASS)
def quonset(cx, cy, length, rad):
    rings = []
    for k in range(2):
        y = cy - length / 2 + length * k
        rings.append([(cx + rad * math.cos(a), y, rad * math.sin(a)) for a in [i * math.pi / 24 for i in range(25)]])
    V = [p for r in rings for p in r]; F = [(k, k + 1, 25 + k + 1, 25 + k) for k in range(24)]
    obj_from("hangar", V, F, M_SHEET)
    obj_from("hback", rings[0], [tuple(range(25))], M_SHEET)
    bk = [(cx + rad * 0.98 * math.cos(a), cy + length / 2 - 0.3, rad * 0.98 * math.sin(a)) for a in [i * math.pi / 24 for i in range(25)]]
    obj_from("hdark", bk, [tuple(range(25))], M_BLACK)
quonset(-38, 30, 40, 13)
quonset(30, 45, 30, 10)
for k in range(5):   # parked bombers far away (no holes)
    bomber(-70 + k * 34, 95, 0, holes=False, rot=math.radians(180 + rnd.uniform(-8, 8)))
# fuel drums & crates near the plane
drum_me = bpy.data.meshes.new("drum"); bm = bmesh.new()
bmesh.ops.create_cone(bm, cap_ends=True, segments=20, radius1=0.3, radius2=0.3, depth=0.9); bm.to_mesh(drum_me); bm.free()
drum_me.materials.append(flat("drumc", (0.2, 0.25, 0.15), 0.6, 0.3))
for k in range(7):
    o = bpy.data.objects.new("drum", drum_me); sc.collection.objects.link(o); o.location = (-12 + (k % 4) * 0.65, -6 + (k // 4) * 0.65, 0.45)
multi_box("crate", [((10, -9, 0), (11.2, -7.8, 1.0)), ((10.3, -9.2, 1.0), (11.0, -8.4, 1.6))], M_DESK)

# ---------------- sky (z = 3000) ----------------
SKYZ = 3000.0
for k, (x, y, z, r) in enumerate([(0, 0, 0, 0.0), (-28, -22, 6, 0.05), (26, -26, -4, -0.04), (-50, -50, 2, 0.02), (52, -55, 8, 0.0)]):
    root, _ = bomber(x, 200 + y, SKYZ + z, holes=False, gear=False, rot=0)
    root.rotation_euler = (0, r, 0)
flak_me = ico_mesh = None
bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
for v in bm.verts: v.co *= 1 + 0.25 * (rnd.random() - 0.5)
flak_me = bpy.data.meshes.new("flak"); bm.to_mesh(flak_me); bm.free(); flak_me.materials.append(M_FLAK)
for k in range(30):
    x = rnd.uniform(-90, 90); y = rnd.uniform(150, 420); z = SKYZ + rnd.uniform(-25, 35)
    if abs(x) < 12 and y < 230: continue
    for j in range(4):
        o = bpy.data.objects.new("flak", flak_me); sc.collection.objects.link(o)
        s = rnd.uniform(1.5, 3.2); o.location = (x + rnd.uniform(-2, 2), y + rnd.uniform(-2, 2), z + rnd.uniform(-1.5, 1.5)); o.scale = (s, s, s)
        for p in flak_me.polygons: p.use_smooth = True

# ---------------- briefing room (y = 1000) ----------------
BY = 1000.0
multi_box("bfloor", [((-7, BY - 6, -0.2), (7, BY + 6, 0))], M_FLOOR)
multi_box("bwalls", [((-7.2, BY + 6, 0), (7.2, BY + 6.3, 4.5)), ((-7.3, BY - 6, 0), (-7, BY + 6, 4.5)),
                     ((7, BY - 6, 0), (7.3, BY + 6, 4.5)), ((-7.2, BY - 6.3, 0), (7.2, BY - 6, 4.5))], M_WALL)
multi_box("bceil", [((-7.3, BY - 6.3, 4.5), (7.3, BY + 6.3, 4.8))], M_TRIM)
multi_box("board", [((-3.0, BY + 5.95, 1.0), (3.0, BY + 6.0, 3.2))], M_BOARD)
multi_box("bframe", [((-3.1, BY + 5.9, 0.92), (3.1, BY + 5.98, 1.0)), ((-3.1, BY + 5.9, 3.2), (3.1, BY + 5.98, 3.28)),
                     ((-3.1, BY + 5.9, 1.0), (-3.0, BY + 5.98, 3.2)), ((3.0, BY + 5.9, 1.0), (3.1, BY + 5.98, 3.2))], M_TRIM)
multi_box("map", [((4.0, BY + 5.95, 1.3), (6.4, BY + 6.0, 3.1))], M_MAP)
multi_box("mapframe", [((3.9, BY + 5.9, 1.2), (6.5, BY + 5.97, 3.2))], M_TRIM)
for x in (-6.98, 6.98):
    multi_box("win", [((x - 0.02, BY - 3.5, 1.3), (x + 0.02, BY - 1.5, 3.4)), ((x - 0.02, BY + 0.5, 1.3), (x + 0.02, BY + 2.5, 3.4))], M_WINDOW)
multi_box("table", [((-2.5, BY + 0.5, 0.75), (2.5, BY + 2.3, 0.82)), ((-2.3, BY + 0.7, 0), (-2.1, BY + 0.9, 0.75)), ((2.1, BY + 0.7, 0), (2.3, BY + 0.9, 0.75)),
                    ((-2.3, BY + 1.9, 0), (-2.1, BY + 2.1, 0.75)), ((2.1, BY + 1.9, 0), (2.3, BY + 2.1, 0.75))], M_DESK)
for k in range(6):   # scattered photos/papers on table
    o = multi_box("paper", [((-0.15, -0.2, 0), (0.15, 0.2, 0.004))], flat(f"pap{k}", (0.85, 0.83, 0.75), 0.8), (-1.8 + k * 0.7, BY + 1.4 + rnd.uniform(-.3, .3), 0.82))
    o.rotation_euler = (0, 0, rnd.uniform(-0.5, 0.5))
for x, y in ((-2.5, BY - 1), (2.5, BY - 1), (0, BY + 3)):
    L = bpy.data.lights.new("pt", "POINT"); L.energy = 700; L.color = (1.0, 0.85, 0.65); L.shadow_soft_size = 0.5
    o = bpy.data.objects.new("pt", L); o.location = (x, y, 4.1); sc.collection.objects.link(o)
    bpy.ops.mesh.primitive_cone_add(vertices=20, radius1=0.35, radius2=0.08, depth=0.3, location=(x, y, 4.25)); bpy.context.object.data.materials.append(M_TRIM)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(x, y, 4.1)); bpy.context.object.data.materials.append(M_LAMP)

# ---------------- shots ----------------
SHOTS = {
    # name: (loc, target, lens, dof)
    "apron": ((21.0, 28.0, 2.0), (-1.0, -1.0, 3.2), 30, None),
    "front": ((-6.0, 26.0, 2.2), (0.0, 0.0, 2.6), 24, None),
    "sky": ((6.0, 118.0, SKYZ - 5.0), (0.0, 195.0, SKYZ + 3.0), 34, None),
    "skyempty": ((14.0, 150.0, SKYZ - 6.0), (60.0, 330.0, SKYZ + 25.0), 30, None),
    "wing": ((10.5, 6.5, 6.0), (11.0, 1.5, 2.6), 30, None),
    "tail": ((5.5, -15.5, 5.6), (0.0, -9.0, 3.4), 28, None),
    "body": ((8.5, -1.0, 3.6), (0.0, -2.0, 2.9), 24, None),
    "engine": ((-7.0, 6.5, 7.0), (-4.2, 2.6, 2.9), 28, None),
    "top": ((0.0, 0.5, 52.0), (0.0, 0.5, 0.0), 24, None),
    "room": ((0.0, BY - 4.8, 1.7), (0.0, BY + 3.0, 1.6), 24, None),
}

os.makedirs(OUT, exist_ok=True)
camfile = os.path.join(OUT, "cams.json")
cams = json.load(open(camfile)) if os.path.exists(camfile) else {}
for name in SHOTS_WANTED:
    loc, target, lens, dof = SHOTS[name]
    place_cam(loc, target, lens, dof)
    if name == "top": cam.rotation_euler = (0, 0, math.radians(0))
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
