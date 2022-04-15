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
    "version": (0, 1, 0),
    "location": "View3D (ObjectMode) > Sidebar > TMG_Atmosphere Tab",
    "warning": "",
    "category": "Object"
}

classes = (
    ## Properties
    TMG_Atmosphere_Properties,

    ## Operators
    TMG_Atmosphere_Add,
    
    ## Atmosphere Panel
    TMG_Atmosphere_Panel, 
    TMG_Atmosphere_Panel_Properties,
    TMG_Atmosphere_Panel_Properties_Objects,
    TMG_Atmosphere_Panel_Properties_Atmosphere,
    TMG_Atmosphere_Panel_Properties_Lights,
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

