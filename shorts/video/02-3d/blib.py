"""Build the Broughton bridge world in Blender and render background plates.
usage: bvenv/bin/python scene3d.py -- OUTDIR shot1 [shot2 ...] [--test]
"""
import bpy, bmesh, math, random, sys, os, json, time
from mathutils import Vector, Euler
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

argv = sys.argv[sys.argv.index("--") + 1:]
OUT = argv[0]; TEST = "--test" in argv
SHOTS_WANTED = [a for a in argv[1:] if not a.startswith("--")]
HERE = os.path.dirname(os.path.abspath(__file__)); A = os.path.join(HERE, "..", "assets")
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
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

cam_d = bpy.data.cameras.new("cam"); cam_d.sensor_fit = "VERTICAL"; cam_d.sensor_height = 24.0
cam = bpy.data.objects.new("cam", cam_d); sc.collection.objects.link(cam); sc.camera = cam

def place_cam(loc, target, lens, dof=None):
    cam.location = loc
    d = Vector(target) - Vector(loc); cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cam_d.lens = lens; cam_d.clip_start = 0.05; cam_d.clip_end = 1000
    cam_d.dof.use_dof = bool(dof)
    if dof: cam_d.dof.focus_distance = d.length; cam_d.dof.aperture_fstop = dof

# render settings
sc.render.engine = "CYCLES"; cy = sc.cycles
cy.device = "CPU"; cy.use_denoising = True
try: cy.denoiser = "OPENIMAGEDENOISE"
except Exception: pass
cy.max_bounces = 8; cy.diffuse_bounces = 2; cy.glossy_bounces = 3; cy.transmission_bounces = 6
cy.use_adaptive_sampling = True; cy.adaptive_threshold = 0.05
sc.render.use_persistent_data = True
sc.render.image_settings.file_format = "PNG"
for v, look in (("AgX", "AgX - Medium High Contrast"), ("AgX", "Medium High Contrast")):
    try: sc.view_settings.view_transform = v; sc.view_settings.look = look; break
    except Exception: pass

