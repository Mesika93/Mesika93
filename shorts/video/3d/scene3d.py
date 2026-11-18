"""Build the Broughton bridge world in Blender and render background plates.
usage: bvenv/bin/python scene3d.py -- OUTDIR shot1 [shot2 ...] [--test]
"""
import bpy, bmesh, math, random, sys, os, json, time
from mathutils import Vector, Euler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common3d import *

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]; TEST = "--test" in argv
SHOTS_WANTED = [a for a in argv[1:] if not a.startswith("--")]
A = os.path.join(HERE, "assets")
FPS = 30
W_OUT, H_OUT = 720, 1280

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
rnd = random.Random(7)

# ---------------- materials ----------------
def node(nt, kind, **kw):
    n = nt.nodes.new(kind)
    for k, v in kw.items(): setattr(n, k, v)
    return n

def sock(n, ident, out=False):
    for s in (n.outputs if out else n.inputs):
        if s.identifier == ident or s.name == ident: return s
    raise KeyError(ident)

def pbr(name, tex, scale=1.0, tint=None, rough_mul=1.0, metal=0.0, bump=1.0):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree
    bsdf = nt.nodes["Principled BSDF"]
    tc = node(nt, "ShaderNodeTexCoord"); mp = node(nt, "ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (scale, scale, scale)
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    def img(suffix, color=True):
        n = node(nt, "ShaderNodeTexImage"); n.projection = "BOX"; n.projection_blend = 0.25
        n.image = bpy.data.images.load(os.path.join(A, f"{tex}_{suffix}.jpg"), check_existing=True)
        if not color: n.image.colorspace_settings.name = "Non-Color"
        nt.links.new(mp.outputs["Vector"], n.inputs["Vector"]); return n
    d = img("diff")
    col = d.outputs["Color"]
    if tint:
        mx = node(nt, "ShaderNodeMix", data_type="RGBA", blend_type="MULTIPLY")
        sock(mx, "Factor").default_value = 1.0
        nt.links.new(col, sock(mx, "A_Color")); sock(mx, "B_Color").default_value = (*tint, 1)
        col = sock(mx, "Result_Color", out=True)
    nt.links.new(col, bsdf.inputs["Base Color"])
    r = img("rough", False)
    if rough_mul != 1.0:
        mm = node(nt, "ShaderNodeMath", operation="MULTIPLY"); mm.inputs[1].default_value = rough_mul
        nt.links.new(r.outputs["Color"], mm.inputs[0]); nt.links.new(mm.outputs[0], bsdf.inputs["Roughness"])
    else:
        nt.links.new(r.outputs["Color"], bsdf.inputs["Roughness"])
    n = img("nor", False); nm = node(nt, "ShaderNodeNormalMap"); nm.inputs["Strength"].default_value = bump
    nt.links.new(n.outputs["Color"], nm.inputs["Color"]); nt.links.new(nm.outputs["Normal"], bsdf.inputs["Normal"])
    bsdf.inputs["Metallic"].default_value = metal
    return m

def flat(name, color, rough=0.5, metal=0.0, emit=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1); b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = (*color, 1); b.inputs["Emission Strength"].default_value = emit
    return m

M_WOOD = pbr("wood", "brown_planks_05", 0.5, tint=(0.55, 0.38, 0.24))
M_STONE = pbr("stone", "castle_brick_07", 0.35, tint=(0.95, 0.88, 0.78))
M_COBBLE = pbr("cobble", "cobblestone_floor_01", 0.3)
M_GRASS = pbr("grass", "aerial_grass_rock", 0.05, tint=(0.75, 0.85, 0.6))
M_ROOF = pbr("roof", "clay_roof_tiles_02", 0.3)
M_IRON = pbr("iron", "rust_coarse_01", 0.8, tint=(0.35, 0.3, 0.28), metal=0.6, rough_mul=0.8)
M_GLASS = flat("glass", (0.05, 0.07, 0.09), 0.08, 0.3)
M_FRAME = flat("frame", (0.85, 0.83, 0.78), 0.6)
M_LEAF = flat("leaf", (0.09, 0.22, 0.06), 0.8)
M_LEAF2 = flat("leaf2", (0.15, 0.28, 0.07), 0.8)
M_TRUNK = flat("trunk", (0.18, 0.11, 0.06), 0.9)
M_FOAM = flat("foam", (0.9, 0.95, 1.0), 0.35)
M_RED = flat("flag", (0.6, 0.03, 0.04), 0.7)
PLASTERS = [pbr(f"plaster{i}", "grey_plaster", 0.25, tint=c) for i, c in
            enumerate([(1.0, 0.85, 0.7), (0.85, 0.55, 0.45), (0.95, 0.92, 0.85), (0.75, 0.6, 0.5), (0.9, 0.78, 0.55)])]

def water_mat():
    m = bpy.data.materials.new("water"); m.use_nodes = True; nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.02, 0.06, 0.05, 1); b.inputs["Roughness"].default_value = 0.12
    tc = node(nt, "ShaderNodeTexCoord"); mp = node(nt, "ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (0.25, 0.08, 1)
    nz = node(nt, "ShaderNodeTexNoise", noise_dimensions="4D"); nz.inputs["Scale"].default_value = 3.0
    nz.inputs["Detail"].default_value = 6
    bp = node(nt, "ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.45
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], nz.inputs["Vector"])
    nt.links.new(nz.outputs["Fac"], bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])
    return m, nz
M_WATER, WATER_NOISE = water_mat()

# ---------------- geometry helpers ----------------
def obj_from(name, verts, faces, mat, loc=(0, 0, 0)):
    me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces); me.update()
    me.materials.append(mat)
    o = bpy.data.objects.new(name, me); o.location = loc; sc.collection.objects.link(o); return o

def box_vf(x0, y0, z0, x1, y1, z1, off=0):
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    return v, [tuple(i + off for i in q) for q in f]

def box(name, a, b, mat):
    v, f = box_vf(*a, *b); return obj_from(name, v, f, mat)

def multi_box(name, boxes, mat, loc=(0, 0, 0)):
    V, F = [], []
    for a, b in boxes:
        v, f = box_vf(*a, *b, off=len(V)); V += v; F += f
    return obj_from(name, V, F, mat, loc)

def shade_smooth(o):
    for p in o.data.polygons: p.use_smooth = True

# ---------------- world ----------------
w = bpy.data.worlds.new("sky"); sc.world = w; w.use_nodes = True
nt = w.node_tree; bg = nt.nodes["Background"]
env = node(nt, "ShaderNodeTexEnvironment"); env.image = bpy.data.images.load(os.path.join(A, "sky.hdr"))
mp = node(nt, "ShaderNodeMapping"); tc = node(nt, "ShaderNodeTexCoord")
mp.inputs["Rotation"].default_value = (0, 0, math.radians(200))
nt.links.new(tc.outputs["Generated"], mp.inputs["Vector"]); nt.links.new(mp.outputs["Vector"], env.inputs["Vector"])
nt.links.new(env.outputs["Color"], bg.inputs["Color"]); bg.inputs["Strength"].default_value = 1.0

sun_d = bpy.data.lights.new("sun", "SUN"); sun_d.energy = 3.2; sun_d.angle = math.radians(1.5)
sun_d.color = (1.0, 0.95, 0.88)
sun = bpy.data.objects.new("sun", sun_d); sc.collection.objects.link(sun)
sun.rotation_euler = Euler((math.radians(52), 0, math.radians(-30)))

# terrain
def smooth(t): t = clamp(t); return t * t * (3 - 2 * t)
BANK = 5.4
def terrain_h(x, y):
    d = abs(x)
    h = -2.5 + (BANK + 2.5) * smooth((d - 15) / 8)
    if d > 23:
        hill = smooth((d - 50) / 60) * (14 + 6 * math.sin(y * 0.03 + x * 0.01)) + \
               1.2 * math.sin(x * 0.11 + 1.3) * math.sin(y * 0.09) * smooth((d - 30) / 20)
        h += hill
    h += smooth((y - 90) / 80) * 10 * smooth((d - 10) / 30)   # far hills upstream
    return h
N = 140; S = 340.0
verts = [(-S / 2 + S * i / N, -S / 2 + S * j / N, 0) for j in range(N + 1) for i in range(N + 1)]
verts = [(x, y, terrain_h(x, y)) for x, y, _ in verts]
faces = [(j * (N + 1) + i, j * (N + 1) + i + 1, (j + 1) * (N + 1) + i + 1, (j + 1) * (N + 1) + i) for j in range(N) for i in range(N)]
terr = obj_from("terrain", verts, faces, M_GRASS); shade_smooth(terr)
water = obj_from("water", [(-200, -200, 0.3), (200, -200, 0.3), (200, 200, 0.3), (-200, 200, 0.3)], [(0, 1, 2, 3)], M_WATER)

# towers
for sx in (-1, 1):
    X = sx * SPAN
    multi_box(f"tower{sx}", [((X - 1.0, -4.0, -2.5), (X + 1.0, -2.0, TOWER_TOP)),
                             ((X - 1.0, 2.0, -2.5), (X + 1.0, 4.0, TOWER_TOP)),
                             ((X - 1.1, -4.2, TOWER_TOP - 2.0), (X + 1.1, 4.2, TOWER_TOP + 1.0)),
                             ((X - 1.3, -4.4, TOWER_TOP + 1.0), (X + 1.3, 4.4, TOWER_TOP + 1.4)),
                             ((X - 2.2, -5.0, -2.5), (X + 2.2, 5.0, 1.2))], M_STONE)
    # approach road
    x0, x1 = sorted((X, X + sx * 12))
    multi_box(f"approach{sx}", [((x0, -2.2, DECK_Z - 1.2), (x1, 2.2, DECK_Z + 0.12))], M_WOOD)
    multi_box(f"wall{sx}", [((x0, 2.15, DECK_Z), (x1, 2.4, DECK_Z + 0.9))], M_STONE)
    multi_box(f"wallN{sx}", [((x0, -2.4, DECK_Z), (x1, -2.15, DECK_Z + 0.9))], M_STONE)

# deck segments
SEG = 2.0
SEG_X = [-SPAN + SEG / 2 + i * SEG for i in range(int(2 * SPAN / SEG))]
seg_mesh = None; near_mesh = None; SEGS = []; NEAR = set()
for i, x in enumerate(SEG_X):
    if seg_mesh is None:
        o = multi_box("seg0", [((-1.0, -2.2, -0.25), (1.0, 2.2, 0.12)),
                               ((-0.95, 2.0, 0.12), (-0.8, 2.15, 1.15)),
                               ((-1.0, 1.99, 1.05), (1.0, 2.17, 1.18)), ((-1.0, 2.04, 0.55), (1.0, 2.14, 0.62))], M_WOOD)
        n = multi_box("near0", [((-0.95, -2.15, 0.12), (-0.8, -2.0, 1.15)),
                                ((-1.0, -2.17, 1.05), (1.0, -1.99, 1.18)), ((-1.0, -2.14, 0.55), (1.0, -2.04, 0.62))], M_WOOD)
        seg_mesh, near_mesh = o.data, n.data
    else:
        o = bpy.data.objects.new(f"seg{i}", seg_mesh); sc.collection.objects.link(o)
        n = bpy.data.objects.new(f"near{i}", near_mesh); sc.collection.objects.link(n)
    o.location = (x, 0, DECK_Z); n.location = (x, 0, DECK_Z); SEGS.append((o, n)); NEAR.add(n.name)

# chains (curves) + hangers
CHAIN_N = 45
def make_chain(name, y):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = 0.13; cu.bevel_resolution = 3
    sp = cu.splines.new("POLY"); sp.points.add(CHAIN_N - 1)
    o = bpy.data.objects.new(name, cu); o.data.materials.append(M_IRON); sc.collection.objects.link(o)
    return o
CHAINS = {y: make_chain(f"chain{y}", y) for y in (-2.6, 2.6)}
NEAR.add(CHAINS[-2.6].name)
hm = bpy.data.meshes.new("hanger")
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=8, radius1=0.04, radius2=0.04, depth=1.0); bm.to_mesh(hm); bm.free()
hm.materials.append(M_IRON)
HANGERS = []
for x in SEG_X[1:-1]:
    for y in (-2.45, 2.45):
        o = bpy.data.objects.new("h", hm); sc.collection.objects.link(o); HANGERS.append((o, x, y))
        if y < 0: NEAR.add(o.name)

# clamp with bolts on the near chain (for the bolts close-up)
CLAMP_X = -14.0
clamp_o = multi_box("clamp", [((-0.32, -0.12, -0.35), (0.32, 0.0, 0.35))], M_IRON)
bolt_me = bpy.data.meshes.new("bolt"); bm = bmesh.new()
bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.11, radius2=0.11, depth=0.12); bm.to_mesh(bolt_me); bm.free()
bolt_me.materials.append(M_IRON)
BOLTS = []
for k, (bx, bz) in enumerate([(-0.18, 0.18), (0.18, 0.0), (-0.12, -0.2)]):
    o = bpy.data.objects.new(f"bolt{k}", bolt_me); sc.collection.objects.link(o)
    o.rotation_euler = (math.radians(90), 0, 0); BOLTS.append((o, bx, bz))
# close-up chain links near clamp
link_me = bpy.data.meshes.new("link"); bm = bmesh.new()
bmesh.ops.create_circle(bm, segments=4, radius=1)
bm.free()
bpy.ops.mesh.primitive_torus_add(major_radius=0.32, minor_radius=0.07, major_segments=24, minor_segments=8)
link_proto = bpy.context.object; link_proto.scale = (1.6, 1, 1); link_proto.data.materials.append(M_IRON)
shade_smooth(link_proto); link_proto.location = (0, 0, -100)
LINKS = []
for k in range(-5, 6):
    o = bpy.data.objects.new(f"lk{k}", link_proto.data); sc.collection.objects.link(o)
    o.scale = (1.6, 1, 1); LINKS.append((o, k))

# town on right bank
bx = 0; y = -70.0
while y < 75:
    wdt = rnd.uniform(8, 12); hgt = rnd.uniform(9, 16); dep = 10; x0 = 41 + rnd.uniform(-1, 1.5)
    gz = terrain_h(x0, y) - 0.5
    box(f"house{bx}", (x0, y, gz), (x0 + dep, y + wdt - 0.3, gz + hgt), rnd.choice(PLASTERS))
    rv = [(x0 - 0.4, y - 0.3, gz + hgt), (x0 + dep + 0.4, y - 0.3, gz + hgt), (x0 + dep / 2, y - 0.3, gz + hgt + 4.5),
          (x0 - 0.4, y + wdt, gz + hgt), (x0 + dep + 0.4, y + wdt, gz + hgt), (x0 + dep / 2, y + wdt, gz + hgt + 4.5)]
    obj_from(f"roof{bx}", rv, [(0, 1, 2), (3, 5, 4), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], M_ROOF)
    wins, frames = [], []
    for fl in range(int((hgt - 2) // 3.2)):
        for c in range(int(wdt // 2.6)):
            wy = y + 1.3 + c * 2.6; wz = gz + 2.2 + fl * 3.2
            frames.append(((x0 - 0.12, wy - 0.1, wz - 0.1), (x0 + 0.02, wy + 1.1, wz + 1.75)))
            wins.append(((x0 - 0.18, wy, wz), (x0 - 0.05, wy + 1.0, wz + 1.65)))
    if wins:
        multi_box(f"wf{bx}", frames, M_FRAME); multi_box(f"wg{bx}", wins, M_GLASS)
    y += wdt; bx += 1
multi_box("promenade", [((22.5, -80, BANK - 1), (41, 80, BANK + 0.08))], M_COBBLE)
for fy in (-14, -4, 6, 16):
    multi_box(f"pole{fy}", [((36.5, fy, BANK), (36.65, fy + 0.15, BANK + 7))], M_TRUNK)
    obj_from(f"flag{fy}", [(36.55, fy + 0.15, BANK + 7), (36.55, fy + 2.4, BANK + 6.4), (36.55, fy + 0.15, BANK + 5.7)], [(0, 1, 2)], M_RED)
multi_box("quay", [((22.0, -80, -2), (23.2, 80, BANK + 0.6))], M_STONE)

# trees (instanced)
bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
for v in bm.verts: v.co *= 1 + 0.15 * math.sin(v.co.x * 5) * math.cos(v.co.y * 4)
crown_me = bpy.data.meshes.new("crown"); bm.to_mesh(crown_me); bm.free()
bm = bmesh.new(); bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=0.25, radius2=0.18, depth=1.0)
trunk_me = bpy.data.meshes.new("trunk"); bm.to_mesh(trunk_me); bm.free(); trunk_me.materials.append(M_TRUNK)
crown_me.materials.append(M_LEAF)
crown2 = crown_me.copy(); crown2.materials[0] = M_LEAF2
placed = 0
while placed < 260:
    x = rnd.uniform(-160, 160); y = rnd.uniform(-60, 160)
    if abs(x) < 25 or (x > 20 and x < 56 and y < 80): continue
    z = terrain_h(x, y); s = rnd.uniform(2.2, 4.0)
    t = bpy.data.objects.new("t", trunk_me); t.location = (x, y, z + s * 0.5); t.scale = (s * 0.5, s * 0.5, s * 1.2)
    c = bpy.data.objects.new("c", rnd.choice([crown_me, crown2])); c.location = (x, y, z + s * 1.7)
    c.scale = (s, s, s * rnd.uniform(1.0, 1.4)); sc.collection.objects.link(t); sc.collection.objects.link(c)
    shade_smooth(c); placed += 1

# splash particles
bm = bmesh.new(); bmesh.ops.create_icosphere(bm, subdivisions=2, radius=1.0)
drop_me = bpy.data.meshes.new("drop"); bm.to_mesh(drop_me); bm.free(); drop_me.materials.append(M_FOAM)
DROPS = []
r2 = random.Random(11)
for k in range(220):
    o = bpy.data.objects.new("d", drop_me); sc.collection.objects.link(o)
    DROPS.append((o, r2.uniform(-12, 12), r2.uniform(-3.5, 3.5), r2.uniform(-3, 3), r2.uniform(-2.5, 2.5),
                  r2.uniform(5, 13), r2.uniform(0.12, 0.45), r2.uniform(0.0, 0.6)))
for o in DROPS: o[0].data.polygons.foreach_set("use_smooth", [True] * len(o[0].data.polygons))
foam = obj_from("foam", [(math.cos(a) * 1, math.sin(a) * 1, 0.33) for a in [i * math.pi / 16 for i in range(32)]],
                [tuple(range(32))], M_FOAM)

# ---------------- per-time state ----------------
def collapse_seg(x, now, c):
    tf = now - T["folds"] - 0.15
    if abs(x) < 11:
        t0 = abs(x) * 0.035
        tt = max(0.0, tf - t0)
        z = max(-1.6, DECK_Z - 4.9 * tt * tt)
        r = random.Random(int(x * 10))
        return (x + r.uniform(-1, 1) * tt * 0.8, r.uniform(-1, 1) * tt * 1.2, z), (r.uniform(-0.4, 0.4) * tt, math.copysign(min(1.2, tt * 0.9), x), 0)
    th = math.radians(72) * ease((tf - 0.25) / 1.3)
    sx = 1 if x > 0 else -1; s = SPAN - abs(x)
    return (sx * (SPAN - s * math.cos(th)), 0, DECK_Z - s * math.sin(th)), (0, sx * th, 0)

def set_state(now):
    amp, f, c = bridge_state(now)
    for (o, n), x in zip(SEGS, SEG_X):
        if c > 0:
            loc, rot = collapse_seg(x, now, c)
        else:
            z = deck_z(x, now); slope = (deck_z(x + 0.5, now) - deck_z(x - 0.5, now))
            loc, rot = (x, 0, z), (0, -math.atan(slope), 0)
        o.location = loc; o.rotation_euler = rot; n.location = loc; n.rotation_euler = rot
    jit = 0.0
    if now >= T["bolts"] and c == 0: jit = 0.03 + 0.05 * clamp((now - T["bolts"]) / 2)
    r = random.Random(int(now * 1000))
    def cz(x):
        z = chain_z(x, now)
        if c > 0: z = max(0.6, z - c * 11 * math.sin(math.pi * (x + SPAN) / (2 * SPAN)) ** 2)
        return z
    for y, o in CHAINS.items():
        for i, p in enumerate(o.data.splines[0].points):
            x = -SPAN + 2 * SPAN * i / (CHAIN_N - 1)
            p.co = (x + r.uniform(-jit, jit), y + r.uniform(-jit, jit), cz(x) + r.uniform(-jit, jit), 1)
    for o, x, y in HANGERS:
        if c > 0.15 and abs(x) < 16: o.location = (0, 0, -100); continue
        top = cz(x); bot = deck_z(x, now) + 0.1 if c == 0 else collapse_seg(x, now, c)[0][2]
        o.location = (x, y, (top + bot) / 2); o.scale = (1, 1, max(0.05, top - bot))
    # clamp on near chain
    cy = -3.0 - 0.14; czz = cz(CLAMP_X)
    clamp_o.location = (CLAMP_X, cy + 0.12, czz)
    for k, (o, bx, bz) in enumerate(BOLTS):
        tp = now - POP_TIMES[k]
        if tp < 0:
            o.location = (CLAMP_X + bx, cy - 0.04, czz + bz); o.rotation_euler = (math.radians(90), 0, 0)
        else:
            o.location = (CLAMP_X + bx + (k - 1) * 1.2 * tp, cy - 0.04 - 6 * tp, czz + bz + 3.5 * tp - 4.9 * tp * tp)
            o.rotation_euler = (math.radians(90) + tp * 25, tp * 17, 0)
    for o, k in LINKS:
        x = CLAMP_X + k * 0.62
        o.location = (x, -2.6, cz(x)); o.rotation_euler = (math.radians(90) * (k % 2), math.atan2(cz(x + .3) - cz(x - .3), .6) * -1, 0)
    ts = now - T["folds"] - 0.9
    for o, x0, y0, vx, vy, vz, s, d in DROPS:
        t = ts - d * 0.4
        if t <= 0 or c == 0: o.location = (0, 0, -100); continue
        z = 0.3 + vz * t - 4.9 * t * t
        if z < 0.2: o.location = (0, 0, -100); continue
        o.location = (x0 + vx * t, y0 + vy * t - 1.0, z); o.scale = (s, s, s * 1.3)
    if c > 0 and ts > 0:
        k = clamp(ts / 2.0); foam.location = (0, 0, 0); foam.scale = (2 + 16 * k, 4 + 8 * k, 1)
    else:
        foam.location = (0, 0, -100)
    WATER_NOISE.inputs["W"].default_value = now * 0.25

# ---------------- cameras / shots ----------------
cam_d = bpy.data.cameras.new("cam"); cam_d.sensor_fit = "VERTICAL"; cam_d.sensor_height = 24.0
cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam

def place_cam(loc, target, lens, dof=None):
    cam.location = loc
    d = Vector(target) - Vector(loc); cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cam_d.lens = lens; cam_d.clip_start = 0.05; cam_d.clip_end = 1000
    cam_d.dof.use_dof = bool(dof)
    if dof: cam_d.dof.focus_distance = d.length; cam_d.dof.aperture_fstop = dof

SHOTS = {
    # name: (loc, target, lens, still?, dof)
    "order":  ((10.0, -6.5, 8.9), (1.5, 0.0, 7.6), 30, True, None),
    "wide":   ((-8.0, -52.0, 14.0), (0.0, 0.0, 6.0), 17, True, None),
    "parade": ((26.0, -14.0, 7.2), (40.0, -11.0, 9.5), 22, True, None),
    "crowd":  ((30.0, -14.0, 7.0), (40.0, -13.0, 8.6), 30, True, None),
    "boots":  ((0.4, -1.6, 8.3), (0.0, 0.5, 6.6), 26, True, None),
    "close":  ((-6.0, -6.5, 8.2), (-22.0, 1.0, 11.0), 40, True, None),
    "mid":    ((3.0, -18.0, 8.8), (0.0, 0.0, 7.8), 30, True, None),
    "news":   ((0.0, 199.0, 2.6), (0.0, 200.0, 0.0), 30, True, None),
    "hum":    ((7.5, -15.0, 9.0), (-2.0, 0.0, 8.6), 32, False, None),
    "swing":  ((-4.0, -48.0, 12.0), (0.0, 0.0, 6.5), 19, False, None),
    "bolts":  ((-13.0, -4.9, 0), (CLAMP_X, -2.7, 0), 45, False, 2.8),
    "collapse": ((4.0, -36.0, 9.5), (0.0, 0.0, 4.5), 21, False, None),
}
SHOT_RANGE = {"hum": scene_range("s_hum"), "swing": scene_range("s_swing"),
              "bolts": scene_range("s_bolts"), "collapse": scene_range("s_collapse")}
STILL_TIME = {"order": 0.5, "wide": 3.0, "parade": 6.0, "crowd": 11.0, "boots": 10.0, "close": 14.0,
              "mid": 25.0, "news": 26.0}

# newspaper table set
multi_box("table", [((-3, 197, -0.6), (3, 203, 0.0))], M_WOOD)

# render settings
sc.render.engine = "CYCLES"; cy = sc.cycles
cy.device = "CPU"; cy.use_denoising = True
try: cy.denoiser = "OPENIMAGEDENOISE"
except Exception: pass
cy.max_bounces = 4; cy.diffuse_bounces = 2; cy.glossy_bounces = 2; cy.transmission_bounces = 2
cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.05
sc.render.use_persistent_data = True
sc.render.image_settings.file_format = "PNG"
for v, look in (("AgX", "AgX - Medium High Contrast"), ("AgX", "Medium High Contrast")):
    try: sc.view_settings.view_transform = v; sc.view_settings.look = look; break
    except Exception: pass

FG = "--fg" in argv
if FG:
    for o in sc.objects:
        if o.type in ("MESH", "CURVE") and o.name not in NEAR and not o.name.startswith("wallN"):
            o.is_holdout = True
    sc.render.film_transparent = True
os.makedirs(OUT, exist_ok=True)
camfile = os.path.join(OUT, "cams.json")
cams = json.load(open(camfile)) if os.path.exists(camfile) else {}

for name in SHOTS_WANTED:
    loc, target, lens, still, dof = SHOTS[name]
    if name == "bolts":
        zc = chain_z(CLAMP_X, T["bolts"])
        loc = (loc[0], loc[1], zc + 0.25); target = (target[0], target[1], zc - 0.05)
    place_cam(loc, target, lens, dof)
    bpy.context.view_layer.update()
    mi = cam.matrix_world.inverted()
    if still:
        sc.render.resolution_x, sc.render.resolution_y = 1080, 1920
        cy.samples = 24 if TEST else 64
    else:
        sc.render.resolution_x, sc.render.resolution_y = W_OUT, H_OUT
        cy.samples = 8 if TEST else 16
    cams[name] = {"mi": [list(r) for r in mi], "lens": lens, "sensor_h": 24.0,
                  "res": [sc.render.resolution_x, sc.render.resolution_y], "still": still}
    if FG: cy.samples = 8
    elif True: json.dump(cams, open(camfile, "w"), indent=1)
    d = os.path.join(OUT, name); os.makedirs(d, exist_ok=True)
    if still:
        set_state(STILL_TIME[name]); sc.render.filepath = os.path.join(d, "fg.png" if FG else "still.png")
        t0 = time.time(); bpy.ops.render.render(write_still=True); print(name, "still", round(time.time() - t0, 1), "s", flush=True)
    else:
        a, b = SHOT_RANGE[name]
        frames = list(range(int(math.floor(a * FPS)), int(math.ceil(b * FPS)) + 1))
        if TEST: frames = frames[len(frames) // 2: len(frames) // 2 + 1]
        for fi in frames:
            p = os.path.join(d, f"{'fg' if FG else 'f'}{fi:05d}.png")
            if os.path.exists(p) and not TEST: continue
            if name == "bolts":
                zc = chain_z(CLAMP_X, fi / FPS)
                place_cam((-12.7, -5.7, zc + 0.35), (CLAMP_X, -2.7, zc - 0.02), 35, 4.0)
            set_state(fi / FPS); sc.render.filepath = p
            t0 = time.time(); bpy.ops.render.render(write_still=True)
            print(name, fi, round(time.time() - t0, 1), "s", flush=True)
print("ALL DONE", flush=True)
