"""Tecla mecanica: placa de aluminio + switch + keycap, con animacion de pulsacion."""
import bpy, math, time
import mathutils

t0 = time.time()
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)

scene = bpy.context.scene
coll = scene.collection

# ---------- materiales ----------
def mat(name, rgb, rough=0.6, metallic=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = next(n for n in m.node_tree.nodes if n.type == 'BSDF_PRINCIPLED')
    bsdf.inputs['Base Color'].default_value = (*rgb, 1.0)
    bsdf.inputs['Roughness'].default_value = rough
    try:
        bsdf.inputs['Metallic'].default_value = metallic
    except Exception:
        pass
    return m

M_PLATE   = mat('Aluminio', (0.82, 0.83, 0.85), 0.4, 0.6)
M_HOUSING = mat('Housing',  (0.12, 0.12, 0.13), 0.7)
M_STEM    = mat('Stem',     (0.95, 0.45, 0.10), 0.5)
M_CAP     = mat('Keycap',   (0.05, 0.45, 0.50), 0.45)
M_GROUND  = mat('Ground',   (0.60, 0.59, 0.58), 0.9)

def mesh_obj(name, verts, faces, material, loc=(0, 0, 0), smooth=False):
    me = bpy.data.meshes.new(name + '_mesh')
    me.from_pydata(verts, [], faces)
    me.update()
    if smooth:
        for p in me.polygons:
            p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    ob.location = loc
    ob.data.materials.append(material)
    coll.objects.link(ob)
    return ob

def box_c(name, sx, sy, sz, center, material):
    """Caja centrada en `center`."""
    x, y, z = sx / 2, sy / 2, sz / 2
    cx, cy, cz = center
    v = [(cx - x, cy - y, cz - z), (cx + x, cy - y, cz - z),
         (cx + x, cy + y, cz - z), (cx - x, cy + y, cz - z),
         (cx - x, cy - y, cz + z), (cx + x, cy - y, cz + z),
         (cx + x, cy + y, cz + z), (cx - x, cy + y, cz + z)]
    f = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
         (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
    return mesh_obj(name, v, f, material)

def cylinder(name, r, h, center, material, seg=24):
    cx, cy, cz = center
    v = [(cx + r * math.cos(2 * math.pi * i / seg),
          cy + r * math.sin(2 * math.pi * i / seg), cz - h / 2) for i in range(seg)]
    v += [(vx, vy, cz + h / 2) for vx, vy, _ in v]
    f = [(i, (i + 1) % seg, seg + (i + 1) % seg, seg + i) for i in range(seg)]
    f.append(tuple(range(seg - 1, -1, -1)))
    f.append(tuple(range(seg, 2 * seg)))
    return mesh_obj(name, v, f, material, smooth=True)

# ---------- suelo ----------
box_c('Suelo', 200, 200, 0.2, (0, 0, -0.175), M_GROUND)

# ---------- placa de aluminio con agujero para el switch ----------
plate = box_c('Placa', 4.0, 4.0, 0.15, (0, 0, 0), M_PLATE)
cutter = box_c('Cutter', 1.5, 1.5, 0.5, (0, 0, 0), M_HOUSING)
boolean = plate.modifiers.new('Agujero', 'BOOLEAN')
boolean.operation = 'DIFFERENCE'
boolean.object = cutter
coll.objects.unlink(cutter)
bpy.data.objects.remove(cutter, do_unlink=True)

# ---------- switch: base + vastago en cruz ----------
box_c('SwitchBase', 1.3, 1.3, 0.35, (0, 0, 0.25), M_HOUSING)
stem = cylinder('Vastago', 0.26, 0.55, (0, 0, 0.55), M_STEM)
box_c('CruzA', 0.55, 0.18, 0.30, (0, 0, 0.80), M_STEM)
box_c('CruzB', 0.18, 0.55, 0.30, (0, 0, 0.80), M_STEM)

# ---------- keycap trapezoidal con bordes redondeados ----------
bw, tw, h = 1.8, 1.32, 1.05
z0 = 0.62
v = [(-bw / 2, -bw / 2, z0), (bw / 2, -bw / 2, z0),
     (bw / 2, bw / 2, z0), (-bw / 2, bw / 2, z0),
     (-tw / 2, -tw / 2, z0 + h), (tw / 2, -tw / 2, z0 + h),
     (tw / 2, tw / 2, z0 + h), (-tw / 2, tw / 2, z0 + h)]
f = [(0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1),
     (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)]
keycap = mesh_obj('Keycap', v, f, M_CAP)
bevel = keycap.modifiers.new('Borde', 'BEVEL')
bevel.width = 0.05
bevel.segments = 2

# ---------- animacion: 3 pulsaciones (baja 0.4 y vuelve) ----------
moviles = [keycap, stem,
           bpy.data.objects['CruzA'], bpy.data.objects['CruzB']]
base_z = {o.name: o.location.z for o in moviles}
DOWN, HOLD_UP = -0.4, 0.0

def press(f_down0, f_down1, f_up0, f_up1):
    for f, z in [(f_down0 - 6, HOLD_UP), (f_down1, DOWN),
                 (f_up0, DOWN), (f_up1, HOLD_UP)]:
        for o in moviles:
            o.location.z = base_z[o.name] + z
            o.keyframe_insert(data_path='location', frame=f)

press(10, 15, 21, 29)
press(40, 45, 51, 59)
press(70, 75, 81, 89)

scene.frame_start = 1
scene.frame_end = 90
scene.render.fps = 30

# ---------- luces / camara ----------
sun = bpy.data.lights.new('Sol', 'SUN')
sun.energy = 2.0
sun_obj = bpy.data.objects.new('Sol', sun)
sun_obj.rotation_euler = (0.9, 0.0, -0.5)
coll.objects.link(sun_obj)

world = scene.world or bpy.data.worlds.new('World')
scene.world = world
world.use_nodes = True
bg = next(n for n in world.node_tree.nodes if n.type == 'BACKGROUND')
bg.inputs['Color'].default_value = (0.75, 0.82, 0.90, 1.0)
bg.inputs['Strength'].default_value = 0.6

cam_data = bpy.data.cameras.new('Camara')
cam_data.lens = 50
cam = bpy.data.objects.new('Camara', cam_data)
coll.objects.link(cam)
cam.location = (4.6, -6.0, 4.2)
d = mathutils.Vector((0, 0, 0.6)) - cam.location
cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
scene.camera = cam

# ---------- stills de verificacion: arriba y presionada ----------
scene.render.resolution_x = 960
scene.render.resolution_y = 540
scene.render.resolution_percentage = 100
scene.render.film_transparent = False
scene.render.image_settings.file_format = 'PNG'
scene.frame_current = 1
scene.render.filepath = '/home/roger/Escritorio/keyboard/tecla_up.png'
bpy.ops.render.render(write_still=True)
scene.frame_current = 15
scene.render.filepath = '/home/roger/Escritorio/keyboard/tecla_down.png'
bpy.ops.render.render(write_still=True)

print(f'objetos: {len(bpy.data.objects)} | fov OK en {time.time()-t0:.1f}s')
