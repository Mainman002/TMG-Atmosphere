import bpy, sys, os

from . TMG_Atmosphere import *

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, PointerProperty
from bpy.types import Operator, Header


# GNU GENERAL PUBLIC LICENSE
# Version 3, 29 June 2007

# Thank you all that download, suggest, and request features
# As well as the whole Blender community. You're all epic :)


bl_info = {
    "name": "TMG_Atmosphere",
    "author": "Johnathan Mueller",
    "descrtion": "A panel to manage atmosphere and lighting effects",
    "blender": (2, 80, 0),
    "version": (0, 1, 1),
    "location": "View3D (ObjectMode) > Sidebar > TMG > Atmosphere Tab",
    "warning": "",
    "category": "Object"
}

classes = (
    ## Properties
    TMG_Atmosphere_Properties,

    ## Operators
    TMG_Atmosphere_Add,
    TMG_Atmosphere_Set_Scene_Settings,
    
    ## Atmosphere Panel
    OBJECT_PT_TMG_Atmosphere_Parent_Panel, 
    ATMO_PT_TMG_Atmosphere_Panel, 
    ATMO_PT_TMG_Atmosphere_Panel_Properties,
    ATMO_PT_TMG_Atmosphere_Panel_Properties_Objects,
    ATMO_PT_TMG_Atmosphere_Panel_Properties_Effects_View_Settings,
    ATMO_PT_TMG_Atmosphere_Panel_Properties_Effects_World,
    ATMO_PT_TMG_Atmosphere_Panel_Properties_Atmosphere,
    ATMO_PT_TMG_Atmosphere_Panel_Properties_Lights,
)

def register():
    for rsclass in classes:
        bpy.utils.register_class(rsclass)
        bpy.types.Scene.tmg_atmosphere_vars = bpy.props.PointerProperty(type=TMG_Atmosphere_Properties)

def unregister():
    for rsclass in classes:
        bpy.utils.unregister_class(rsclass)

if __name__ == "__main__":
    register()

