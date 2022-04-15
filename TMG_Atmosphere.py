from asyncio.windows_events import NULL
import bpy, sys, os
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, PointerProperty
from bpy.types import Operator, Header


class TMG_Atmosphere_Properties(bpy.types.PropertyGroup):
    atmosphere_enabled : bpy.props.BoolProperty(name='Atmosphere', default=True)
    atmosphere_color :  bpy.props.FloatVectorProperty(name="Color", size=4, subtype='COLOR_GAMMA', default=(0.8, 0.8, 0.8, 1), min=0, max=1)
    atmosphere_density : bpy.props.FloatProperty(name='Density', default=0.01, soft_min=0.0, soft_max=1.0)
    atmosphere_absorption : bpy.props.FloatProperty(name='Absorption', default=0.0, soft_min=0.0, soft_max=1.0)

    sun_enabled : bpy.props.BoolProperty(name='Enabled', default=True)
    sun_color :  bpy.props.FloatVectorProperty(name="Color", size=3, subtype='COLOR_GAMMA', default=(0.8, 0.8, 0.8), min=0, max=1)
    sun_energy : bpy.props.FloatProperty(name='Sun Energy', default=4.0, soft_min=0.0, soft_max=10.0)

    area1_enabled : bpy.props.BoolProperty(name='Enabled', default=True)
    area1_color :  bpy.props.FloatVectorProperty(name="Color", size=3, subtype='COLOR_GAMMA', default=(0.8, 0.8, 0.8), min=0, max=1)
    area1_energy : bpy.props.FloatProperty(name='Area1 Energy', default=100.0, soft_min=0.0, soft_max=100.0)
    area1_type : bpy.props.EnumProperty(name='Type', default='AREA', description='Light type',
    items=[
    ('NONE', 'None', ''),
    ('AREA', 'Area', ''),
    ('SPOT', 'Spot', ''),
    ('POINT', 'Point', ''),
    ('SUN', 'Sun', '')])

    area2_enabled : bpy.props.BoolProperty(name='Enabled', default=True)
    area2_color :  bpy.props.FloatVectorProperty(name="Color", size=3, subtype='COLOR_GAMMA', default=(0.8, 0.8, 0.8), min=0, max=1)
    area2_energy : bpy.props.FloatProperty(name='Area2 Energy', default=70.0, soft_min=0.0, soft_max=100.0)
    area2_type : bpy.props.EnumProperty(name='Type', default='AREA', description='Light type',
    items=[
    ('NONE', 'None', ''),
    ('AREA', 'Area', ''),
    ('SPOT', 'Spot', ''),
    ('POINT', 'Point', ''),
    ('SUN', 'Sun', '')])

    area3_enabled : bpy.props.BoolProperty(name='Enabled', default=True)
    area3_color :  bpy.props.FloatVectorProperty(name="Color", size=3, subtype='COLOR_GAMMA', default=(0.8, 0.8, 0.8), min=0, max=1)
    area3_energy : bpy.props.FloatProperty(name='Area3 Energy', default=50.0, soft_min=0.0, soft_max=100.0)
    area3_type : bpy.props.EnumProperty(name='Type', default='AREA', description='Light type',
    items=[
    ('NONE', 'None', ''),
    ('AREA', 'Area', ''),
    ('SPOT', 'Spot', ''),
    ('POINT', 'Point', ''),
    ('SUN', 'Sun', '')])

    control_circle : bpy.props.BoolProperty(name='Control Circle', default=True)
    focus : bpy.props.BoolProperty(name='Focus', default=True)
    camera : bpy.props.BoolProperty(name='Camera', default=True)
    floor : bpy.props.BoolProperty(name='Floor', default=True)
    suzanne : bpy.props.BoolProperty(name='Suzanne', default=True)


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

        layout.operator("tmg_atmosphere.add", icon='SCENE_DATA')
        layout.operator("tmg_atmosphere.set_scene_settings", icon='SCENE')

            
class TMG_Atmosphere_Panel_Properties(bpy.types.Panel):
    bl_idname = 'tmg_atmosphere_panel_properties'
    bl_category = 'TMG Atmosphere'
    bl_label = 'Properties'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
        
    def draw(self, context):
        layout = self.layout
        

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

        layout.prop(tmg_atmosphere_vars, 'sun_enabled', text='Sun')
        box = layout.box()
        col = box.column(align=True)
        col.prop(tmg_atmosphere_vars, 'sun_color')
        col.prop(tmg_atmosphere_vars, 'sun_energy', text='Energy')
        col.enabled = tmg_atmosphere_vars.sun_enabled

        layout.prop(tmg_atmosphere_vars, 'area1_enabled', text='Area_1')
        box = layout.box()
        col = box.column(align=True)
        col.prop(tmg_atmosphere_vars, 'area1_type')
        col.prop(tmg_atmosphere_vars, 'area1_color')
        col.prop(tmg_atmosphere_vars, 'area1_energy', text='Energy')
        col.enabled = tmg_atmosphere_vars.area1_enabled

        layout.prop(tmg_atmosphere_vars, 'area2_enabled', text='Area_2')
        box = layout.box()
        col = box.column(align=True)
        col.prop(tmg_atmosphere_vars, 'area2_type')
        col.prop(tmg_atmosphere_vars, 'area2_color')
        col.prop(tmg_atmosphere_vars, 'area2_energy', text='Energy')
        col.enabled = tmg_atmosphere_vars.area2_enabled

        layout.prop(tmg_atmosphere_vars, 'area3_enabled', text='Area_3')
        box = layout.box()
        col = box.column(align=True)
        col.prop(tmg_atmosphere_vars, 'area3_type')
        col.prop(tmg_atmosphere_vars, 'area3_color')
        col.prop(tmg_atmosphere_vars, 'area3_energy', text='Energy')
        col.enabled = tmg_atmosphere_vars.area3_enabled


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

        layout.prop(tmg_atmosphere_vars, 'atmosphere_enabled', text='Atmosphere')
        box = layout.box()
        col = box.column(align=False)
        col.prop(tmg_atmosphere_vars, 'atmosphere_color')
        col.prop(tmg_atmosphere_vars, 'atmosphere_density')
        col.prop(tmg_atmosphere_vars, 'atmosphere_absorption')
        col.enabled = tmg_atmosphere_vars.atmosphere_enabled


class TMG_Atmosphere_Panel_Properties_Effects_View_Settings(bpy.types.Panel):
    bl_idname = "tmg_atmosphere_panel_properties_effects_view_settings"
    bl_label = "View Settings"
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
        col = box.column(align=True)
        col.prop(scene.view_settings, 'view_transform')
        col.prop(scene.view_settings, 'look')


class TMG_Atmosphere_Panel_Properties_Effects_World(bpy.types.Panel):
    bl_idname = "tmg_atmosphere_panel_properties_effects_world"
    bl_label = "World"
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
        col = box.column(align=True)
        if scene.world:
            col.prop(scene.world.node_tree.nodes["Background"].inputs[0], 'default_value', text="Color")
            col.prop(scene.world.node_tree.nodes["Background"].inputs[1], 'default_value', text='Energy')

        
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
        if tmg_atmosphere_vars.atmosphere_enabled:
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
            bpy.ops.object.camera_add(enter_editmode=False, align='WORLD', location=(-0.1, -2.13, 1.71), rotation=(1.34424, 0.00822251, -0.019539), scale=(1, 1, 1))
            camera_ob = get_ob()
            scene.camera = camera_ob

            if control_circle:
                camera_ob.parent = control_circle

            if focus_empty:
                bpy.ops.object.constraint_add( type='TRACK_TO' )
                bpy.context.object.constraints["Track To"].target = focus_empty
                camera_ob.data.dof.focus_object = focus_empty
                
            ## Camera View Settings
            camera_ob.data.dof.use_dof = True
            camera_ob.data.dof.aperture_blades = 8
            camera_ob.data.lens = 61.87
            camera_ob.data.sensor_width = 50
            camera_ob.data.clip_start = 0.1
            camera_ob.data.clip_end = 1000
            camera_ob.data.passepartout_alpha = 0.98

            ## Camera Local Position Offset
            bpy.ops.transform.translate(value=(1.86265e-09, 0, -3.11202), orient_type='LOCAL', orient_matrix=((0.999867, -0.016311, 2.32831e-10), (0.00365587, 0.224105, 0.974558), (-0.0158961, -0.974429, 0.224135)), orient_matrix_type='LOCAL', constraint_axis=(False, False, True), use_proportional_edit=False)

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
        if tmg_atmosphere_vars.sun_enabled:
            bpy.ops.object.light_add(type='SUN', radius=1, align='WORLD', location=(0, 0, 10), rotation=(0, 0.436332, -0.785398), scale=(1, 1, 1))
            if control_circle:
                get_ob().parent = control_circle
            bpy.context.object.data.color = tmg_atmosphere_vars.sun_color
            bpy.context.object.data.energy = tmg_atmosphere_vars.sun_energy

        ## Add Area Light_1
        if tmg_atmosphere_vars.area1_enabled and not tmg_atmosphere_vars.area1_type == 'NONE':
            light_type = tmg_atmosphere_vars.area1_type
            bpy.ops.object.light_add(type=light_type, radius=3, align='WORLD', location=(1, -1, 2.5), scale=(1, 1, 1))
            if light_type == "AREA":
                bpy.context.object.data.shape = 'DISK'
            bpy.context.object.data.color = tmg_atmosphere_vars.area1_color
            bpy.context.object.data.energy = tmg_atmosphere_vars.area1_energy
            bpy.context.object.data.use_contact_shadow = True

            if focus_empty:
                bpy.ops.object.constraint_add(type='TRACK_TO')
                bpy.context.object.constraints["Track To"].target = focus_empty

            if control_circle:
                get_ob().parent = control_circle

        ## Add Area Light_2
        if tmg_atmosphere_vars.area2_enabled and not tmg_atmosphere_vars.area2_type == 'NONE':
            light_type = tmg_atmosphere_vars.area2_type
            bpy.ops.object.light_add(type=light_type, radius=3, align='WORLD', location=(-5, 5.7, 2.5), scale=(1, 1, 1))
            if light_type == "AREA":
                bpy.context.object.data.shape = 'DISK'
            bpy.context.object.data.color = tmg_atmosphere_vars.area2_color
            bpy.context.object.data.energy = tmg_atmosphere_vars.area2_energy
            bpy.context.object.data.use_contact_shadow = True

            if focus_empty:
                bpy.ops.object.constraint_add(type='TRACK_TO')
                bpy.context.object.constraints["Track To"].target = focus_empty

            if control_circle:
                get_ob().parent = control_circle

        ## Add Area Light_3
        if tmg_atmosphere_vars.area3_enabled and not tmg_atmosphere_vars.area3_type == 'NONE':
            light_type = tmg_atmosphere_vars.area3_type
            bpy.ops.object.light_add(type=light_type, radius=3, align='WORLD', location=(4, 8, 2.5), scale=(1, 1, 1))
            if light_type == "AREA":
                bpy.context.object.data.shape = 'DISK'
            bpy.context.object.data.color = tmg_atmosphere_vars.area3_color
            bpy.context.object.data.energy = tmg_atmosphere_vars.area3_energy
            bpy.context.object.data.use_contact_shadow = True

            if focus_empty:
                bpy.ops.object.constraint_add(type='TRACK_TO')
                bpy.context.object.constraints["Track To"].target = focus_empty

            if control_circle:
                get_ob().parent = control_circle
        return {'FINISHED'}


class TMG_Atmosphere_Set_Scene_Settings(bpy.types.Operator):
    """Change blender scene rendering settings"""

    bl_idname = "tmg_atmosphere.set_scene_settings"
    bl_label = "Set Render Settings"
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

        ## View Look
        scene.view_settings.look = 'Medium High Contrast'

        ## DOF Blur Effect
        scene.eevee.use_bokeh_high_quality_slight_defocus = True
        scene.eevee.use_bokeh_jittered = True

        ## ScreenSpace Effect
        scene.eevee.use_ssr_refraction = True
        scene.eevee.use_ssr_halfres = True
        scene.eevee.use_ssr = True

        ## AO Effect
        scene.eevee.use_gtao = True

        ## Bloom Effect
        scene.eevee.use_bloom = True

        ## Set World Strength
        if scene.world:
            scene.world.node_tree.nodes["Background"].inputs[0].default_value = (0.8, 0.8, 0.8, 1)
            scene.world.node_tree.nodes["Background"].inputs[1].default_value = 0.1

        return {'FINISHED'}


