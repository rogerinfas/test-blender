"""Machu Picchu estilizado low-poly. Solo data-API (sin bpy.ops salvo render)."""
import bpy, math, time
from mathutils import Vector

t0 = time.time()

# ---------- limpieza ----------
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

scene = bpy.context.scene
coll = scene.collection

# ---------- materiales ----------
def mat(name, rgb, rough=0.9):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    bsdf.inputs['Base Color'].default_value = (*rgb, 1.0)
    bsdf.inputs['Roughness'].default_value = rough
    return m

M_STONE  = mat('Stone',  (0.43, 0.41, 0.38))
M_GRASS  = mat('Grass',  (0.24, 0.44, 0.17), 1.0)
M_PLAZA  = mat('Plaza',  (0.33, 0.53, 0.24), 1.0)
M_THATCH = mat('Thatch', (0.46, 0.33, 0.18), 1.0)
M_ROCK   = mat('Rock',   (0.45, 0.44, 0.42))
M_DARK   = mat('Dark',   (0.07, 0.055, 0.05), 1.0)
M_PATH   = mat('Path',   (0.62, 0.60, 0.55))

def mesh_obj(name, verts, faces, material, loc=(0, 0, 0)):
    me = bpy.data.meshes.new(name + '_mesh')
    me.from_pydata(verts, [], faces)
    me.update()
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    ob.data.materials.append(material)
    coll.objects.link(ob)
    return ob

def box(name, sx, sy, sz, loc, material):
    x, y, z = sx / 2, sy / 2, sz / 2
    v = [(-x, -y, 0), (x, -y, 0), (x, y, 0), (-x, y, 0),
         (-x, -y, sz), (x, -y, sz), (x, y, sz), (-x, y, sz)]
    f = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
         (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return mesh_obj(name, v, f, material, loc)

# ---------- terreno: meseta + laderas + ruido ----------
PX, PY = 34.0, 17.0  # semi-ejes de la meseta plana

def terrain_h(x, y):
    dx = max(0.0, abs(x) - PX)
    dy = max(0.0, abs(y) - PY)
    d = math.hypot(dx, dy)
    h = -0.55 * (d ** 1.22) if d > 0 else 0.0
    # ruido suave que crece fuera de la meseta
    m = min(1.0, d / 25.0)
    h += m * (2.2 * math.sin(x * 0.11) * math.cos(y * 0.13)
              + 1.1 * math.sin(x * 0.31 + 1.7) * math.sin(y * 0.27 + 0.6))
    return max(h, -70.0)

N, EXT = 72, 190.0
verts, faces = [], []
for iy in range(N + 1):
    y = -EXT + 2 * EXT * iy / N
    for ix in range(N + 1):
        x = -EXT + 2 * EXT * ix / N
        verts.append((x, y, terrain_h(x, y)))
for iy in range(N):
    for ix in range(N):
        a = iy * (N + 1) + ix
        faces.append((a, a + 1, a + N + 2, a + N + 1))
terrain = mesh_obj('Terrain', verts, faces, M_GRASS)
print(f'terreno: {len(verts)} verts')

# ---------- montanas (conos): Huayna Picchu + Cerro Machu Picchu ----------
def cone(name, r, h, loc, material, seg=28):
    v = [(r * math.cos(2 * math.pi * i / seg), r * math.sin(2 * math.pi * i / seg), 0)
         for i in range(seg)] + [(0, 0, h)]
    apex = seg
    f = [(i, (i + 1) % seg, apex) for i in range(seg)]
    f.append(tuple(reversed(range(seg))))
    return mesh_obj(name, v, f, material, loc)

cone('HuaynaPicchu_low', 46, 50, (72, 42, -26), M_GRASS)
cone('HuaynaPicchu_top', 8.5, 13, (72, 42, 15), M_ROCK)
cone('CerroMachuPicchu', 58, 66, (-95, -25, -30), M_GRASS)
cone('CerroMachuPicchu_top', 24, 30, (-95, -25, 12), M_ROCK)
cone('FondoNorte', 70, 55, (-20, 130, -30), M_GRASS)

# ---------- plaza central (parche claro) ----------
box('Plaza', 26, 16, 0.25, (12, 0, -0.05), M_PLAZA)

# ---------- andenes: muro de piedra + cesped (ladera ESTE, bajan hacia +X) ----------
for i in range(8):
    x_wall = 35.0 + i * 3.6
    top = terrain_h(x_wall - 0.3, 0) + 0.8
    box(f'Muro_{i}', 0.8, 30, 4.0, (x_wall, 0, top - 4.0), M_STONE)
    box(f'Anden_{i}', 3.4, 30, 0.5, (x_wall - 2.0, 0, top - 0.5), M_GRASS)

# ---------- casas: muro piedra + techo paja a dos aguas + puerta/ventanas ----------
def gable_roof(name, w, d, h, loc, material):
    x, y = w / 2 * 1.12, d / 2 * 1.12
    v = [(-x, -y, 0), (x, -y, 0), (x, y, 0), (-x, y, 0),
         (0, -y, h), (0, y, h)]
    f = [(0, 1, 4), (3, 5, 2), (0, 4, 5, 3), (1, 2, 5, 4), (0, 3, 2, 1)]
    return mesh_obj(name, v, f, material, loc)

def house(name, x, y, w=4.2, d=3.2, wh=2.3):
    box(f'{name}_muro', w, d, wh, (x, y, 0), M_STONE)
    gable_roof(f'{name}_techo', w, d, 1.5, (x, y, wh), M_THATCH)
    box(f'{name}_puerta', 0.9, 0.12, 1.6, (x, y - d / 2 - 0.01, 0), M_DARK)  # cara sur
    box(f'{name}_vent1', 0.6, 0.12, 0.6, (x - 1.2, y - d / 2 - 0.01, 1.2), M_DARK)
    box(f'{name}_vent2', 0.6, 0.12, 0.6, (x + 1.2, y - d / 2 - 0.01, 1.2), M_DARK)

xs = [-27, -21, -15, -9, -3]
for i, x in enumerate(xs):
    house(f'CasaN_{i}', x, -8.5 + (i % 2) * 0.7)
    if i < 4:
        house(f'CasaS_{i}', x + 2.5, -2.5 - (i % 2) * 0.7)

# ---------- Templo del Sol: torre circular + ventanas ----------
def cylinder(name, r, h, loc, material, seg=26):
    v = [(r * math.cos(2 * math.pi * i / seg), r * math.sin(2 * math.pi * i / seg), 0)
         for i in range(seg)]
    v += [(vx, vy, h) for vx, vy, _ in v]
    f = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    f.append(tuple(range(seg - 1, -1, -1)))
    f.append(tuple(range(seg, 2 * seg)))
    return mesh_obj(name, v, f, material, loc)

cylinder('TemploSol', 4.4, 3.4, (-31, 5.5, 0), M_STONE)
for k, ang in enumerate([0.5, 2.2, 4.0]):
    wx, wy = -31 + 4.32 * math.cos(ang), 5.5 + 4.32 * math.sin(ang)
    box(f'TempVent_{k}', 0.7, 0.7, 0.9, (wx, wy, 1.7), M_DARK)

# ---------- Intihuatana ----------
box('Inti_base', 7, 7, 1.0, (-24, 7.5, 0), M_STONE)
box('Inti_mid', 4.6, 4.6, 1.0, (-24, 7.5, 1.0), M_STONE)
box('Inti_top', 2.6, 2.6, 0.9, (-24, 7.5, 2.0), M_STONE)
piedra = box('Inti_piedra', 0.8, 0.8, 2.0, (-24, 7.5, 3.7), M_ROCK)
piedra.rotation_euler = (0.06, 0.1, 0.3)

# ---------- sendero de piedra ----------
for i in range(5):
    box(f'Sendero_{i}', 2.2, 1.4, 0.18, (2 + i * 2.4, -4.5 + i * 1.6, 0.02), M_PATH)

# ---------- sol + cielo ----------
sun = bpy.data.lights.new('Sol', 'SUN')
sun.energy = 2.2
sun_obj = bpy.data.objects.new('Sol', sun)
sun_obj.rotation_euler = (0.95, 0.0, -0.35)
coll.objects.link(sun_obj)

world = scene.world or bpy.data.worlds.new('World')
scene.world = world
world.use_nodes = True
bg = next(n for n in world.node_tree.nodes if n.type == 'BACKGROUND')
bg.inputs['Color'].default_value = (0.55, 0.74, 0.94, 1.0)
bg.inputs['Strength'].default_value = 0.55

# ---------- camara (vista postal clasica) ----------
cam_data = bpy.data.cameras.new('VistaMP')
cam_data.lens = 40
cam = bpy.data.objects.new('VistaMP', cam_data)
coll.objects.link(cam)
cam.location = (58, -102, 38)
d = Vector((8, 10, 2)) - cam.location
q = d.to_track_quat('-Z', 'Y')
cam.rotation_euler = q.to_euler()
scene.camera = cam

# ---------- render ----------
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = '/tmp/opencode/machu.png'
bpy.ops.render.render(write_still=True)

print(f'objetos: {len(bpy.data.objects)} | render OK en {time.time()-t0:.1f}s')
