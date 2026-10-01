"""Machu Picchu v3 - composicion como la foto: angular abierto, Huayna al fondo,
andenes robustos empotrados, ruinas sin techo, loma de guardian en primer plano."""
import bpy, math, time, random
from mathutils import Vector

t0 = time.time()
random.seed(7)
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

scene = bpy.context.scene
coll = scene.collection

# ---------- materiales ----------
def mat(name, rgb, rough=0.95, alpha=1.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    bsdf.inputs['Base Color'].default_value = (*rgb, 1.0)
    bsdf.inputs['Roughness'].default_value = rough
    if alpha < 1.0:
        try:
            bsdf.inputs['Alpha'].default_value = alpha
            m.blend_method = 'BLEND'
            m.shadow_method = 'NONE'
        except Exception:
            pass
    return m

M_STONE = mat('Stone', (0.45, 0.40, 0.33), 1.0)
M_GRASS = mat('Grass', (0.19, 0.38, 0.13), 1.0)
M_PLAZA = mat('Plaza', (0.32, 0.50, 0.20), 1.0)
M_ROCK  = mat('Rock',  (0.44, 0.42, 0.38))
M_DARK  = mat('Dark',  (0.07, 0.06, 0.05), 1.0)
M_FAR   = mat('Far',   (0.42, 0.52, 0.60), 1.0)
M_MIST  = mat('Mist',  (0.92, 0.94, 0.96), 1.0, alpha=0.08)

def mesh_obj(name, verts, faces, materials, loc=(0, 0, 0), smooth=False):
    if not isinstance(materials, list):
        materials = [materials]
    me = bpy.data.meshes.new(name + '_mesh')
    me.from_pydata(verts, [], faces)
    me.update()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    for m in materials:
        ob.data.materials.append(m)
    coll.objects.link(ob)
    return ob

def box(name, sx, sy, sz, loc, material, rot_z=0.0, cx=0.0, cy=0.0):
    x, y = sx / 2, sy / 2
    v = [(-x, -y, 0), (x, -y, 0), (x, y, 0), (-x, y, 0),
         (-x, -y, sz), (x, -y, sz), (x, y, sz), (-x, y, sz)]
    f = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
         (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    ob = mesh_obj(name, v, f, material, loc)
    if rot_z:
        c, s = math.cos(rot_z), math.sin(rot_z)
        ob.rotation_euler = (0, 0, rot_z)
        lx, ly, lz = loc
        ox, oy = lx - cx, ly - cy
        ob.location = (cx + ox * c - oy * s, cy + ox * s + oy * c, lz)
    return ob

# ---------- terreno (loma del guardian util al sur) ----------
PX, PY = 36.0, 20.0

def base_h(x, y):
    dx = max(0.0, abs(x) - PX)
    dy = max(0.0, abs(y) - PY)
    d = math.hypot(dx, dy)
    h = -0.55 * (d ** 1.22) if d > 0 else 0.0
    m = min(1.0, d / 25.0)
    h += m * (2.2 * math.sin(x * 0.11) * math.cos(y * 0.13)
              + 1.1 * math.sin(x * 0.31 + 1.7) * math.sin(y * 0.27 + 0.6))
    return h

def blend_flat(h, x, y, cx, cy, r, hf):
    dist = math.hypot(x - cx, y - cy)
    if dist >= r:
        return h
    w = 1.0 - dist / r
    w = w * w * (3 - 2 * w)
    return h * (1 - w) + hf * w

def terrain_h(x, y):
    h = base_h(x, y)
    h = blend_flat(h, x, y, 18, 112, 55, -18)    # asiento del Huayna
    h = blend_flat(h, x, y, -95, -25, 65, -28)
    ky = max(0.0, min(1.0, (-25 - y) / 15.0))     # solo al sur del recinto
    h += 60.0 * math.exp(-(((x - 5) ** 2) + ((y + 70) ** 2)) / (35 ** 2)) * ky
    return max(h, -70.0)

N, EXT = 76, 210.0
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
terrain = mesh_obj('Terrain', verts, faces, [M_GRASS, M_ROCK], smooth=True)
for p in terrain.data.polygons:
    if p.normal.z < 0.55:
        p.material_index = 1
print(f'terreno: {len(verts)} verts')

# ---------- montanas (verde abajo, roca arriba por altura) ----------
def craggy_cone(name, r, h, loc, rock_z, seg=30, crag=0.22, seed=0.0):
    v = []
    for i in range(seg):
        a = 2 * math.pi * i / seg
        rr = r * (1 + crag * math.sin(3 * a + seed) * math.cos(2 * a - seed)
                  + 0.5 * crag * math.sin(7 * a + seed * 2))
        v.append((rr * math.cos(a), rr * math.sin(a), 0))
    v.append((0, 0, h))
    f = [(i, (i + 1) % seg, seg) for i in range(seg)]
    f.append(tuple(reversed(range(seg))))
    ob = mesh_obj(name, v, f, [M_GRASS, M_ROCK], loc, smooth=True)
    for p in ob.data.polygons:
        wz = p.center.z + loc[2]
        if wz > rock_z or p.normal.z < 0.35:
            p.material_index = 1
    return ob

craggy_cone('HuaynaPicchu', 50, 95, (18, 112, -20), rock_z=28, seed=1.3)  # pico z=75
craggy_cone('CerroOeste', 58, 66, (-95, -25, -28), rock_z=15, seed=4.1)
craggy_cone('FondoNorte', 80, 60, (-30, 150, -30), rock_z=25, seed=2.2)

for i, (x, y, r, h) in enumerate([(-160, 60, 90, 70), (150, 120, 100, 80), (40, 230, 110, 75)]):
    cv = [(r * math.cos(2 * math.pi * k / 20), r * math.sin(2 * math.pi * k / 20), 0)
          for k in range(20)] + [(0, 0, h)]
    cf = [(k, (k + 1) % 20, 20) for k in range(20)]
    mesh_obj(f'Lejos_{i}', cv, cf, M_FAR, (x, y, -25))

# ---------- neblina ----------
box('Niebla1', 30, 0.5, 4, (-8, 98, 40), M_MIST, rot_z=0.3, cx=-8, cy=98)
box('Niebla2', 24, 0.5, 3, (34, 100, 48), M_MIST, rot_z=-0.25, cx=34, cy=100)

# ---------- plaza ----------
box('Plaza', 20, 11, 0.25, (9, 1, -0.05), M_PLAZA)

# ---------- andenes robustos: tapa = max del terreno + muros empotrados ----------
def terraces(prefix, n, horiz_dir, start, step, length, ref, wall_h=6.0):
    for i in range(n):
        if horiz_dir == 'S':
            y_f = start - i * step
            xs = [ref - length / 2, ref, ref + length / 2]
            top = max(terrain_h(x, y_f + 0.3) for x in xs +
                      [terrain_h(x, y_f + 3.1) for x in xs]) + 0.4
            box(f'{prefix}M_{i}', length, 0.8, wall_h, (ref, y_f, top - wall_h), M_STONE)
            box(f'{prefix}T_{i}', length, 2.8, 1.2, (ref, y_f + 1.7, top - 1.2), M_GRASS)
        elif horiz_dir == 'W':
            x_f = start - i * step
            top = max(terrain_h(x_f + 0.3, ref - length / 2),
                      terrain_h(x_f + 0.3, ref),
                      terrain_h(x_f + 0.3, ref + length / 2),
                      terrain_h(x_f + 3.1, ref)) + 0.4
            box(f'{prefix}M_{i}', 0.8, length, wall_h, (x_f, ref, top - wall_h), M_STONE)
            box(f'{prefix}T_{i}', 2.8, length, 1.2, (x_f + 1.7, ref, top - 1.2), M_GRASS)
        else:
            x_f = start + i * step
            top = max(terrain_h(x_f - 0.3, ref - length / 2),
                      terrain_h(x_f - 0.3, ref),
                      terrain_h(x_f - 0.3, ref + length / 2),
                      terrain_h(x_f - 3.1, ref)) + 0.4
            box(f'{prefix}M_{i}', 0.8, length, wall_h, (x_f, ref, top - wall_h), M_STONE)
            box(f'{prefix}T_{i}', 2.8, length, 1.2, (x_f - 1.7, ref, top - 1.2), M_GRASS)

terraces('SurA', 3, 'S', -23, 3.2, 36, 0.0, wall_h=3.4)   # borde del recinto
# (SurB eliminado: el primer plano queda como loma de pasto con muros, igual que la foto)
terraces('Oes', 5, 'W', -39, 3.2, 26, -2.0)
terraces('Est', 6, 'E', 39, 3.2, 26, 0.0)

# ---------- ruinas sin techo ----------
def ruin(name, cx, cy, w=5.0, d=4.0, h=1.7, rot=0.0, l_shape=False):
    t = 0.55
    c, s = math.cos(rot), math.sin(rot)
    def put(nm, ox, oy, sx, sy, hh):
        box(nm, sx, sy, hh, (cx + ox * c - oy * s, cy + ox * s + oy * c, 0),
            M_STONE, rot_z=rot, cx=cx, cy=cy)
    put(f'{name}_N', 0, d / 2, w, t, h + random.uniform(-0.3, 0.3))
    put(f'{name}_S', -w / 4, -d / 2, w / 2 - 0.5, t, h + random.uniform(-0.3, 0.3))
    put(f'{name}_S2', w / 4 + 0.5, -d / 2, w / 2 - 0.5, t, h + random.uniform(-0.3, 0.3))
    if not l_shape:
        put(f'{name}_E', w / 2, 0, t, d, h + random.uniform(-0.4, 0.2))
    put(f'{name}_O', -w / 2, 0, t, d, h + random.uniform(-0.3, 0.3))
    put(f'{name}_P', 0, -d / 2, 1.0, t + 0.06, 0.9)

k = 0
for row_y, x0, x1, r0 in [(9.5, -2, 26, 0.06), (2.5, -6, 24, -0.05), (-4.5, -2, 20, 0.1)]:
    x = x0
    while x < x1:
        w = random.uniform(4.2, 5.6)
        ruin(f'R{k}', x + random.uniform(-0.6, 0.6), row_y + random.uniform(-0.8, 0.8),
             w=w, d=random.uniform(3.6, 4.6), h=random.uniform(1.5, 2.1),
             rot=r0 + random.uniform(-0.08, 0.08), l_shape=(k % 4 == 0))
        x += w + random.uniform(1.2, 2.4)
        k += 1
for i, (x, y) in enumerate([(-28, 6), (-22, -2), (-29, -8), (-16, -10), (-33, -1)]):
    ruin(f'RO{i}', x, y, w=4.5, d=3.8, h=1.7, rot=random.uniform(-0.3, 0.3))

# ---------- Templo del Sol + Intihuatana ----------
def cylinder(name, r, h, loc, material, seg=26):
    v = [(r * math.cos(2 * math.pi * i / seg), r * math.sin(2 * math.pi * i / seg), 0)
         for i in range(seg)]
    v += [(vx, vy, h) for vx, vy, _ in v]
    f = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    f.append(tuple(range(seg - 1, -1, -1)))
    f.append(tuple(range(seg, 2 * seg)))
    return mesh_obj(name, v, f, material, loc)

cylinder('TemploSol', 4.0, 2.6, (-19, -3, 0), M_STONE)
for j, ang in enumerate([0.5, 2.2, 4.0]):
    box(f'TempVent_{j}', 0.7, 0.7, 0.9,
        (-19 + 3.92 * math.cos(ang), -3 + 3.92 * math.sin(ang), 1.2), M_DARK)

box('Inti_base', 7, 7, 1.0, (-27, 13, 0), M_STONE)
box('Inti_mid', 4.6, 4.6, 1.0, (-27, 13, 1.0), M_STONE)
box('Inti_top', 2.6, 2.6, 0.9, (-27, 13, 2.0), M_STONE)
piedra = box('Inti_piedra', 0.8, 0.8, 2.0, (-27, 13, 3.7), M_ROCK)
piedra.rotation_euler = (0.06, 0.1, 0.3)

# ---------- sendero + muros del primer plano ----------
for i in range(6):
    box(f'Sendero_{i}', 2.0, 1.3, 0.18, (-6 + i * 2.6, -12 - i * 2.2, 0.02), M_STONE)
box('MuroFG1', 14, 0.8, 1.4, (-14, -52, terrain_h(-14, -52)), M_STONE, rot_z=0.25, cx=-14, cy=-52)
box('MuroFG2', 10, 0.8, 1.2, (20, -58, terrain_h(20, -58)), M_STONE, rot_z=-0.2, cx=20, cy=-58)

# ---------- sol + cielo ----------
sun = bpy.data.lights.new('Sol', 'SUN')
sun.energy = 2.0
sun.color = (1.0, 0.96, 0.90)
sun_obj = bpy.data.objects.new('Sol', sun)
sun_obj.rotation_euler = (1.0, 0.05, 1.05)
coll.objects.link(sun_obj)

world = scene.world or bpy.data.worlds.new('World')
scene.world = world
world.use_nodes = True
bg = next(n for n in world.node_tree.nodes if n.type == 'BACKGROUND')
bg.inputs['Color'].default_value = (0.60, 0.74, 0.89, 1.0)
bg.inputs['Strength'].default_value = 0.6

# ---------- camara gran angular ----------
cam_data = bpy.data.cameras.new('VistaMP')
cam_data.lens = 24
cam = bpy.data.objects.new('VistaMP', cam_data)
coll.objects.link(cam)
cam.location = (28, -98, 30)
d = Vector((18, 0, 8)) - cam.location
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
scene.camera = cam

# ---------- render ----------
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = '/tmp/opencode/machu2.png'
bpy.ops.render.render(write_still=True)

print(f'objetos: {len(bpy.data.objects)} | render OK en {time.time()-t0:.1f}s')
