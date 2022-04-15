from asyncio.windows_events import NULL
import bpy, sys, os
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, PointerProperty
from bpy.types import Operator, Header


## Parent Circle
## Focus Empty
## Camera
## Sun
## Area Light #1
## Area Light #2
## Area Light #3
## Ground Plane
## Suzanne Head


class TMG_Atmosphere_Properties(bpy.types.PropertyGroup):
    test : bpy.props.FloatProperty(name='Diffuse Max', default=1.0, soft_min=0.0, soft_max=1.0)

    atmosphere_color :  bpy.props.FloatVectorProperty(name="Color", size=4, subtype='COLOR_GAMMA', default=(0.8, 0.8, 0.8, 1), min=0, max=1)
    atmosphere_density : bpy.props.FloatProperty(name='Density', default=0.01, soft_min=0.0, soft_max=1.0)
    atmosphere_absorption : bpy.props.FloatProperty(name='Absorption', default=0.0, soft_min=0.0, soft_max=1.0)

    sun_energy : bpy.props.FloatProperty(name='Sun Energy', default=4.0, soft_min=0.0, soft_max=10.0)
    area1_energy : bpy.props.FloatProperty(name='Area1 Energy', default=100.0, soft_min=0.0, soft_max=100.0)
    area2_energy : bpy.props.FloatProperty(name='Area2 Energy', default=70.0, soft_min=0.0, soft_max=100.0)
    area3_energy : bpy.props.FloatProperty(name='Area3 Energy', default=50.0, soft_min=0.0, soft_max=100.0)

    control_circle : bpy.props.BoolProperty(name='Control Circle', default=True)
    focus : bpy.props.BoolProperty(name='Focus', default=True)
    effects_world : bpy.props.BoolProperty(name='World', default=True)
    sun : bpy.props.BoolProperty(name='Sun', default=True)
    three_point : bpy.props.BoolProperty(name='3 Point', default=True)
    atmosphere : bpy.props.BoolProperty(name='Atmosphere', default=True)
    camera : bpy.props.BoolProperty(name='Camera', default=True)
    floor : bpy.props.BoolProperty(name='Floor', default=True)
    suzanne : bpy.props.BoolProperty(name='Suzanne', default=False)
    pass  


def get_ob():
    return bpy.context.active_object


def set_position(ob, x, y, z):
    ob.location[0] = x
    ob.location[1] = y
    ob.location[2] = z


def set_rotation(ob, x, y, z):
    ob.rotation_euler[0] = x
    ob.rotation_euler[1] = y
    ob.rotation_euler[2] = z


# Get material
def get_material(_name):
    mat = bpy.data.materials.get(_name)
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name=_name)
    mat.use_nodes = True
    return mat


# Assign it to object
def assign_material(ob, mat):
    if ob.data.materials:
        # assign to 1st material slot
        ob.data.materials[0] = mat
    else:
        # no slots
        ob.data.materials.append(mat)


# Get Node In Material
def get_node(ob):
    return ob.material_slots[0].material


# Remove Node In Material
def remove_node(mat, name):
    if mat.node_tree.nodes.get(name):
        node =  mat.node_tree.nodes[name]
        mat.node_tree.nodes.remove( node )
        print( "Removed: ", name )
    else:
        print( "Node Not Found: ", name )
        

# Check If Node In Material
def check_node(mat, name):
    if mat.node_tree.nodes.get(name):
        return True
        print( "Check True: ", name )
    return False
        

# Add Shader Node
def add_shader_node(mat, type, name, pos):
    check = check_node(mat, name)
    if check == False:
        node = mat.node_tree.nodes.new(type)
        node.location = (pos[0], pos[1])
        

# Set Shader Node Value
def set_shader_value(mat, name, input, value):
    check = check_node(mat, name)
    if check == True:
        mat.node_tree.nodes[name].inputs[input].default_value = value


# Link Shader Node
def link_shader_nodes(mat, node_a, node_b, output, input):
    check_a = check_node(mat, node_a)
    check_b = check_node(mat, node_b)
    if check_a == True and check_b == True:
        mat.node_tree.links.new( mat.node_tree.nodes[node_a].outputs[output], mat.node_tree.nodes[node_b].inputs[input] ) 


class TMG_Atmosphere_Panel(bpy.types.Panel):
    bl_idname = 'tmg_atmosphere_panel'
    bl_category = 'TMG Atmosphere'
    bl_label = 'Atmosphere'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        layout = self.layout

        layout.operator("tmg_atmosphere.add")

            
class TMG_Atmosphere_Panel_Properties(bpy.types.Panel):
    bl_idname = 'tmg_atmosphere_panel_properties'
    bl_category = 'TMG Atmosphere'
    bl_label = 'Properties'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
        
    def draw(self, context):
        scene = context.scene
        tmg_atmosphere_vars = scene.tmg_atmosphere_vars
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.
        

class TMG_Atmosphere_Panel_Properties_Objects(bpy.types.Panel):
    bl_idname = "tmg_atmosphere_panel_properties_objects"
    bl_label = "Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "tmg_atmosphere_panel_properties"
    bl_options = {"DEFAULT_CLOSED"}
        
    def draw(self, context):
        scene = context.scene
        tmg_atmosphere_vars = scene.tmg_atmosphere_vars
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        box = layout.box()
        col = box.column(align=False)
        # row = col.row(align=True)  

        col.prop(tmg_atmosphere_vars, 'control_circle')
        col.prop(tmg_atmosphere_vars, 'focus')
        col.prop(tmg_atmosphere_vars, 'camera')
        col.prop(tmg_atmosphere_vars, 'sun')
        col.prop(tmg_atmosphere_vars, 'three_point')
        col.prop(tmg_atmosphere_vars, 'atmosphere')
        col.prop(tmg_atmosphere_vars, 'floor')
        col.prop(tmg_atmosphere_vars, 'suzanne')


class TMG_Atmosphere_Panel_Properties_Lights(bpy.types.Panel):
    bl_idname = "tmg_atmosphere_panel_properties_lights"
    bl_label = "Lights"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "tmg_atmosphere_panel_properties"
    bl_options = {"DEFAULT_CLOSED"}
        
    def draw(self, context):
        scene = context.scene
        tmg_atmosphere_vars = scene.tmg_atmosphere_vars
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        box = layout.box()
        col = box.column(align=False)
        # row = col.row(align=True)  

        col.prop(tmg_atmosphere_vars, 'sun_energy')
        col.prop(tmg_atmosphere_vars, 'area1_energy')
        col.prop(tmg_atmosphere_vars, 'area2_energy')
        col.prop(tmg_atmosphere_vars, 'area3_energy')


class TMG_Atmosphere_Panel_Properties_Atmosphere(bpy.types.Panel):
    bl_idname = "tmg_atmosphere_panel_properties_atmosphere"
    bl_label = "Atmosphere"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = "tmg_atmosphere_panel_properties"
    bl_options = {"DEFAULT_CLOSED"}
        
    def draw(self, context):
        scene = context.scene
        tmg_atmosphere_vars = scene.tmg_atmosphere_vars
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        box = layout.box()
        col = box.column(align=False)
        # row = col.row(align=True)  

        col.prop(tmg_atmosphere_vars, 'atmosphere_color')
        col.prop(tmg_atmosphere_vars, 'atmosphere_density')
        col.prop(tmg_atmosphere_vars, 'atmosphere_absorption')

        
class TMG_Atmosphere_Add(bpy.types.Operator):
    """Add atmosphere to scene"""

    bl_idname = "tmg_atmosphere.add"
    bl_label = "Add Atmosphere"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        tmg_atmosphere_vars = scene.tmg_atmosphere_vars

        ## Empty object properties
        control_circle = NULL
        focus_empty = NULL
        camera_ob = NULL
        suzanne = NULL
        ob = NULL

        ## Add Atmosphere Cube
        if tmg_atmosphere_vars.atmosphere:
            bpy.ops.mesh.primitive_cube_add(size=32, enter_editmode=False, align='WORLD', location=(0, 0, 8), scale=(2, 2, 1))
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            ob = get_ob()
            ob.name = "Atmosphere"
            ob.data.name = "Atmosphere"

            ## Materials for Atmosphere
            material = get_material("Atmosphere")
            assign_material( ob, material )
            remove_node( material, "Principled BSDF" )
            remove_node( material, "Material Output" )
            add_shader_node( material, "ShaderNodeOutputMaterial", "Material Output", [200, 0] )
            add_shader_node( material, "ShaderNodeVolumeScatter", "Volume Scatter", [0, 0] )
            set_shader_value( material, "Volume Scatter", 0, tmg_atmosphere_vars.atmosphere_color )
            set_shader_value( material, "Volume Scatter", 1, tmg_atmosphere_vars.atmosphere_density )
            set_shader_value( material, "Volume Scatter", 2, tmg_atmosphere_vars.atmosphere_absorption )
            link_shader_nodes(material, "Volume Scatter", "Material Output", 0, 1)

        ## Add Ground Plane
        if tmg_atmosphere_vars.floor:
            bpy.ops.mesh.primitive_plane_add(size=16, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            ob = get_ob()
            ob.name = "Ground"
            ob.data.name = "Ground"

        ## Add Control Circle
        if tmg_atmosphere_vars.control_circle:
            bpy.ops.curve.primitive_bezier_circle_add(radius=4, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            control_circle = get_ob()
            control_circle.show_in_front = True
            control_circle.name = "Lighting_Parent"

        ## Add Focus Empty
        if tmg_atmosphere_vars.focus:
            bpy.ops.object.empty_add(type='SPHERE', align='WORLD', location=(0, 0, 0.3), scale=(1, 1, 1))
            focus_empty = get_ob()
            focus_empty.name = "Focus"

            if control_circle:
                focus_empty.parent = control_circle
            set_position( focus_empty, 0, 4, 0.3 )

        ## Add Camera
        if tmg_atmosphere_vars.camera:
            bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(-0.1, -2.13, 1.71), rotation=(1.34424, 0.00822251, -0.019539), scale=(1, 1, 1))
            camera_ob = get_ob()
            bpy.context.scene.camera = camera_ob

            if control_circle:
                camera_ob.parent = control_circle

            if focus_empty:
                bpy.ops.object.constraint_add( type='TRACK_TO' )
                bpy.context.object.constraints["Track To"].target = focus_empty
                camera_ob.data.dof.focus_object = focus_empty
                
            ## Camera View Settings
            camera_ob.data.dof.use_dof = True
            camera_ob.data.lens = 61.87
            camera_ob.data.sensor_width = 50
            camera_ob.data.clip_start = 0.1
            camera_ob.data.clip_end = 1000
            camera_ob.data.passepartout_alpha = 0.98

            ## DOF Blur Effect
            bpy.context.scene.eevee.use_bokeh_high_quality_slight_defocus = True
            bpy.context.scene.eevee.use_bokeh_jittered = True
            bpy.context.object.data.dof.aperture_blades = 8

            ## ScreenSpace Effect
            bpy.context.scene.eevee.use_ssr_refraction = True
            bpy.context.scene.eevee.use_ssr_halfres = True
            bpy.context.scene.eevee.use_ssr = True

            ## AO Effect
            bpy.context.scene.eevee.use_gtao = True

            ## Bloom Effect
            bpy.context.scene.eevee.use_bloom = True


            ## Camera Local Position Offset
            bpy.ops.transform.translate(value=(1.86265e-09, 0, -3.11202), orient_axis_ortho='X', orient_type='LOCAL', orient_matrix=((0.999775, -0.0195371, -0.00822242), (0.0123994, 0.224424, 0.974413), (-0.0171919, -0.974296, 0.224616)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), mirror=False, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

        ## Add Suzanne
        if tmg_atmosphere_vars.suzanne:
            bpy.ops.mesh.primitive_monkey_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0.23), rotation=(0, 0, 0), scale=(1, 1, 1))
            suzanne = get_ob()
            bpy.ops.object.subdivision_set(level=2, relative=False)
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
            bpy.ops.object.convert(target='MESH')
            set_rotation( get_ob(), -0.785398, 0, 0.785398 )
            bpy.ops.object.shade_smooth()

            ## Materials for Suzanne
            material = get_material("Suzanne")
            assign_material( suzanne, material )
            remove_node( material, "Principled BSDF" )
            remove_node( material, "Material Output" )
            add_shader_node( material, "ShaderNodeOutputMaterial", "Material Output", [300, 0] )
            add_shader_node( material, "ShaderNodeBsdfPrincipled", "Principled BSDF", [0, 0] )
            set_shader_value( material, "Principled BSDF", 0, (0.765267, 0.546716, 0.455458, 1) )
            set_shader_value( material, "Principled BSDF", 1, 0.1 )
            set_shader_value( material, "Principled BSDF", 9, 0.55 )
            set_shader_value( material, "Principled BSDF", 16, 2.5 )
            set_shader_value( material, "Principled BSDF", 17, 0.103734 )
            link_shader_nodes(material, "Principled BSDF", "Material Output", 0, 0)

        ## Add Sun Light
        if tmg_atmosphere_vars.sun:
            bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 10), rotation=(0, 0.436332, -0.785398), scale=(1, 1, 1))
            if control_circle:
                get_ob().parent = control_circle
            bpy.context.object.data.energy = tmg_atmosphere_vars.sun_energy

        ## Add Area Light
        if tmg_atmosphere_vars.three_point:
            bpy.ops.object.light_add(type='AREA', radius=3, align='WORLD', location=(1, -1, 3), scale=(1, 1, 1))
            bpy.context.object.data.energy = bpy.context.object.data.energy = tmg_atmosphere_vars.area1_energy
            bpy.context.object.data.shape = 'DISK'
            bpy.context.object.data.use_contact_shadow = True

            if focus_empty:
                bpy.ops.object.constraint_add(type='TRACK_TO')
                bpy.context.object.constraints["Track To"].target = focus_empty

            if control_circle:
                get_ob().parent = control_circle

            ## Create Area Duplicates
            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(-6, 6, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
            bpy.context.object.data.energy = bpy.context.object.data.energy = tmg_atmosphere_vars.area2_energy

            bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(9, 1, 0), "orient_axis_ortho":'X', "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(True, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "view2d_edge_pan":False, "release_confirm":False, "use_accurate":False, "use_automerge_and_split":False})
            bpy.context.object.data.energy = bpy.context.object.data.energy = tmg_atmosphere_vars.area3_energy

        ## Set World Strength
        if tmg_atmosphere_vars.effects_world:
            if bpy.data.worlds.get( "World" ):
                bpy.data.worlds["World"].node_tree.nodes["Background"].inputs[1].default_value = 0.1

        return {'FINISHED'}





