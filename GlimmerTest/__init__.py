# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "Glimmer Multirender",
    "author" : "Chris Calef, Conner Lindsley",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (1, 2, 1),
    "location" : "",
    "warning" : "",
    "category" : "Rendering"
}

import bpy
import subprocess

from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    CollectionProperty,
    PointerProperty
) 

from . glimmer_panels import (
    Glimmer_PT_Panel, 
    Glimmer_UL_ActionList, 
    ActionListItem,
    EnviroListItem,
    #FrameRange,
    #ActionPointer,
    #CameraPointer, 
    LIST_OT_NewItem, 
    LIST_OT_DeleteItem, 
    LIST_OT_MoveItem, 
    LIST_OT_NewItemProp, 
    LIST_OT_DeleteItemProp,
    LIST_OT_NewEnviroProp,
    LIST_OT_DeleteEnviroItem

)

from . glimmer_ops import (
    Glimmer_OT_LoadNamesCsv, 
    Glimmer_OT_LoadCsvFile, 
    Glimmer_OT_MultiRender, 
    Glimmer_OT_ScaleObject, 
    Glimmer_OT_UnScaleObject, 
    Glimmer_OT_AddVariation, 
    Glimmer_OT_DeleteVariation,
    SVR_ActionPropList, 
    SVR_EnviroPropList,
    #SVR_CameraList, 
    SVR_FrameRangeList,
    #SVR_PetActionList
)
from . glimmer_funcs import (
    validateRenderSettings, 
    AddNamesCollectionCallback,
    AddColorsCollectionCallback,
    AddActionsCollectionCallback,
    AddSkillsCollectionCallback
)

#myTestArray = ["test string one","test string two"]

class SVR_Settings(bpy.types.PropertyGroup):
    workDir : bpy.props.StringProperty(name = "Work Directory", default = "C:\\work\\")
    csvFile : StringProperty(name="CSV Filename")
    isSkill : BoolProperty(name="isSkill:", description="Set Render Mode to skill.", update= validateRenderSettings)

    # Make the Camera and Action Set be a Collection Property, and have a bank of them for each action/skill then use a callback to determine which goes where.
    #action : bpy.props.PointerProperty(name="Action", type= bpy.types.Action)
    
    nameEnum: EnumProperty(
        name="Name:",
        description="Main animal name.",
        items = AddNamesCollectionCallback
    )

    colorsEnum: EnumProperty(
        name="Colors:",
        description="Pet Colors.",
        items = AddColorsCollectionCallback,
        update= validateRenderSettings
    )

    actionsEnum: EnumProperty(
        name="Actions:",
        description="Pet Actions.",
        items = AddActionsCollectionCallback,
        update= validateRenderSettings
    )
    
    skillsEnum: EnumProperty(
        name="Skills:",
        description="Pet Skills.",
        items = AddSkillsCollectionCallback,
        update= validateRenderSettings
    )


class SVR_VariationSettings(bpy.types.PropertyGroup):
    colorsEnum: EnumProperty(
        name="Colors:",
        description="Color Variations.",
        items = AddColorsCollectionCallback
    )
    material : bpy.props.PointerProperty(name="MaterialProperty", type= bpy.types.Material)
    mesh : bpy.props.PointerProperty(name="MeshProperty", type= bpy.types.Mesh)
    rig : bpy.props.PointerProperty(name="ArmatureProperty", type= bpy.types.Armature)
    prop_list : bpy.props.CollectionProperty(type = ActionListItem)
    list_index : bpy.props.IntProperty(name = "Index for my_action_list", default = 0)

classes = (
    SVR_Settings,
    ActionListItem,
    EnviroListItem,
    SVR_VariationSettings,
    SVR_ActionPropList,
    SVR_EnviroPropList,
    SVR_FrameRangeList,
    #SVR_CameraList,
    #SVR_PetActionList,
    Glimmer_OT_LoadNamesCsv,
    Glimmer_OT_LoadCsvFile,
    Glimmer_OT_MultiRender,
    Glimmer_OT_ScaleObject,
    Glimmer_OT_UnScaleObject,
    Glimmer_PT_Panel,
    Glimmer_UL_ActionList,
    Glimmer_OT_AddVariation,
    Glimmer_OT_DeleteVariation,
    LIST_OT_NewItem,
    LIST_OT_NewItemProp,
    LIST_OT_DeleteItem,
    LIST_OT_DeleteItemProp,
    LIST_OT_NewEnviroProp,
    LIST_OT_DeleteEnviroItem,
    LIST_OT_MoveItem
    )

def register():

    #py_exec = bpy.app.binary_path_python

    # ensure pip is installed & update
    #subprocess.call([str(py_exec), "-m", "ensurepip", "--user"])
    #subprocess.call([str(py_exec), "-m", "pip", "install", "--upgrade", "pip"])

    # install dependencies using pip
    # dependencies such as 'numpy' could be added to the end of this command's list
    #subprocess.call([str(py_exec),"-m", "pip", "install", "--user", "imageio"])
    #subprocess.call([str(py_exec),"-m", "pip", "install", "--user", "moviepy"])

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.svr_settings = bpy.props.PointerProperty(type = SVR_Settings)
    bpy.types.Scene.my_action_list = CollectionProperty(type = SVR_ActionPropList)
    bpy.types.Scene.my_enviro_list = CollectionProperty(type = SVR_EnviroPropList)  
    bpy.types.Scene.my_variations = CollectionProperty(type = SVR_VariationSettings)
    #bpy.types.Scene.my_camera_list = CollectionProperty(type = SVR_CameraList)
    #bpy.types.Scene.frame_range = CollectionProperty(type = SVR_FrameRangeList)
    #bpy.types.Scene.pet_action = CollectionProperty(type = SVR_PetActionList)
    bpy.types.Scene.list_index = IntProperty(name = "Index for my_action_list", default = 0)
    bpy.types.Scene.enviro_index = IntProperty(name = "Index for my_enivro_list", default = 0)
        
    #Well this is weird but it appears that globals are a little weird in blender addons, this is _one_ way to do it.
    dns = bpy.app.driver_namespace
    dns["pet_names"] = []
    dns["pets"] =  {}
    #dns["enviro"] = []

    
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.enviro_index    
    del bpy.types.Scene.list_index
    #del bpy.types.Scene.pet_action
    #del bpy.types.Scene.frame_range
    #del bpy.types.Scene.my_camera_list
    del bpy.types.Scene.my_variations 
    del bpy.types.Scene.my_enviro_list
    del bpy.types.Scene.my_action_list
    del bpy.types.Scene.svr_settings

