import math
import bpy

# Parametros de diseno (editables)
rotor_radio_mm = 50
rotor_anchura_mm = 20
angulos_sectores = [(0, 120), (120, 240), (240, 360)]
radio_imanes = [50, 40, 30]  # mm
altura_imanes_mm = 5
bobinas_fase = 12
bobinas_radio_mm = 60
stator_od_mm = 75
stator_id_mm = 50

# Limpiar escena
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Colecciones
def get_or_create_collection(nombre):
    col = bpy.data.collections.get(nombre)
    if not col:
        col = bpy.data.collections.new(nombre)
        bpy.context.scene.collection.children.link(col)
    return col

coleccion_rotor = get_or_create_collection("BSLC_Rotor")
coleccion_estator = get_or_create_collection("BSLC_Estator")
coleccion_ejes = get_or_create_collection("BSLC_Ejes")

# Materiales
def crear_material(nombre, color, tipo='PRINCIPLED'):
    mat = bpy.data.materials.get(nombre)
    if not mat:
        mat = bpy.data.materials.new(name=nombre)
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = color
            if tipo == 'METAL':
                bsdf.inputs['Metallic'].default_value = 1.0
                bsdf.inputs['Roughness'].default_value = 0.2
            elif tipo == 'COBRE':
                bsdf.inputs['Base Color'].default_value = (0.9, 0.6, 0.2, 1.0)
                bsdf.inputs['Metallic'].default_value = 1.0
                bsdf.inputs['Roughness'].default_value = 0.3
    return mat

mat_iman = crear_material("Iman_NdFeB_N52", (0.1, 0.1, 0.3, 1.0), tipo='METAL')
mat_rotor = crear_material("Rotor_Estructura", (0.3, 0.3, 0.3, 1.0))
mat_bobina = crear_material("Bobina_Cobre", (0.9, 0.6, 0.2, 1.0), tipo='COBRE')
mat_eje = crear_material("Eje_Acero", (0.6, 0.6, 0.65, 1.0), tipo='METAL')

# Rotor - Nucleo
bpy.ops.mesh.primitive_cylinder_add(
    radius=rotor_radio_mm / 1000,
    depth=rotor_anchura_mm / 1000,
    location=(0, 0, 0)
)
rotor = bpy.context.active_object
rotor.name = "Rotor_Nucleo"
rotor.data.materials.append(mat_rotor)
coleccion_rotor.objects.link(rotor)
bpy.context.scene.collection.objects.unlink(rotor)

# Rotor - Imanes (simplificados)
for i, (ang_ini, ang_fin) in enumerate(angulos_sectores):
    radio_eff = radio_imanes[i] / 1000
    altura = altura_imanes_mm / 1000
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radio_eff,
        depth=altura,
        location=(0, 0, rotor_anchura_mm / 2000)
    )
    iman = bpy.context.active_object
    iman.name = f"Iman_Sector_{i+1}"
    iman.data.materials.append(mat_iman)
    coleccion_rotor.objects.link(iman)
    bpy.context.scene.collection.objects.unlink(iman)

# Eje central
bpy.ops.mesh.primitive_cylinder_add(
    radius=4 / 1000,
    depth=(rotor_anchura_mm + 20) / 1000,
    location=(0, 0, 0)
)
eje = bpy.context.active_object
eje.name = "Eje_Central"
eje.data.materials.append(mat_eje)
coleccion_ejes.objects.link(eje)
bpy.context.scene.collection.objects.unlink(eje)

# Estator - Anillo base
stator_od = stator_od_mm / 1000
stator_id = stator_id_mm / 1000
bpy.ops.mesh.primitive_torus_add(
    major_radius=(stator_od + stator_id) / 2,
    minor_radius=(stator_od - stator_id) / 2,
    major_segments=64,
    minor_segments=16
)
estator = bpy.context.active_object
estator.name = "Estator_Base"
estator.data.materials.append(mat_rotor)
coleccion_estator.objects.link(estator)
bpy.context.scene.collection.objects.unlink(estator)

# Estator - Bobinas simplificadas
for i in range(bobinas_fase):
    ang_deg = i * 360 / bobinas_fase
    ang_rad = math.radians(ang_deg)
    radio_m = bobinas_radio_mm / 1000
    x = radio_m * math.cos(ang_rad)
    y = radio_m * math.sin(ang_rad)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=6 / 1000,
        minor_radius=2 / 1000,
        major_segments=12,
        minor_segments=8
    )
    bobina = bpy.context.active_object
    bobina.name = f"Bobina_{i+1}"
    bobina.location = (x, y, 0)
    bobina.data.materials.append(mat_bobina)
    coleccion_estator.objects.link(bobina)
    bpy.context.scene.collection.objects.unlink(bobina)

print("Modelado BSLC Blender completado.")
