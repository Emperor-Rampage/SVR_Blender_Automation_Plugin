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
    "name" : "GlimmerTest",
    "author" : "Chris Calef",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}

import bpy
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    CollectionProperty,
    PointerProperty
) 

from . glimmer_ops import Glimmer_OT_LoadCsvFile, Glimmer_OT_MultiRender,Glimmer_OT_NewMultiRender, Glimmer_OT_ScaleObject, Glimmer_OT_UnScaleObject, Glimmer_OT_AddVariation, Glimmer_OT_DeleteVariation
from . glimmer_panels import Glimmer_PT_Panel, Glimmer_UL_ActionList, ActionListItem, LIST_OT_NewItem, LIST_OT_DeleteItem, LIST_OT_MoveItem, LIST_OT_NewItemNew
from . glimmer_funcs import validateRenderSettings, SetRenderBlock


myTestArray = ["test string one","test string two"]

class SVR_Settings(bpy.types.PropertyGroup):
    workDir : bpy.props.StringProperty(name = "Work Directory", default = "C:\\work\\")
    csvFile : StringProperty(name="CSV Filename")
    isSkill: BoolProperty(name="isSkill:", description="Set Render Mode to skill.", update= validateRenderSettings)    
    
    nameEnum: EnumProperty(
        name="Name:",
        description="Main animal name.",
        #items=[('hummingbird',"Hummingbird","")
        #]
        items= []
    )

    skillsEnum: EnumProperty(
        name="Skills:",
        description="Pet Skills.",
        items=[('singing',"Singing", ""),
                ('knitting',"Knitting", ""),
                ('bubbles',"Bubbles", ""),
                ('hiding',"Hiding", ""),
                ('hypnotize',"Hypnotize", ""),
                ('juggle',"Juggle", ""),
                ('marathon',"Marathon", ""),
                ('singingfail',"Singing Fail", ""),
                ('knittingfail',"Knitting Fail", ""),
                ('bubblesfail',"Bubbles Fail", ""),
                ('hidingfail',"Hiding Fail", ""),
                ('hypnotizefail',"Hypnotize Fail", ""),
                ('jugglefail',"Juggle Fail", ""),
                ('marathonfail',"Marathon Fail", ""),
                ('',"", ""),
        ]
    )

    actionsEnum: EnumProperty(
        name="Actions:",
        description="Pet Actions.",
        items=[ ('idle',"Idle", ""),
                ('happy',"Happy", ""),
                ('sad',"Sad", ""),
                ('hungry',"Hungry", ""),
                ('starving',"Starving", ""),
                ('sick',"Sick", ""),
                ('ill',"Ill", ""),
                ('bad',"Bad", ""),
                ('afraid',"Afraid", ""),
                ('lazy',"Lazy", ""),
                ('tired',"Tired", ""),
                ('sleep',"Sleep", ""),
                ('outshape',"Out of Shape", ""),
                ('inclass',"In Class", ""),
                ('inclassdone',"In Class Done", ""),
                ('inclasspickup',"In Class Pickup", ""),
                ('mistreated',"Mistreated", ""),
                ('petwater',"Pet Water", ""),
                ('basicfeed',"Basic Feed", ""),
                ('premiumfeed',"Premium Feed", ""),
                ('worms',"Worms", ""),
                ('lollipop',"Lollipop", ""),
                ('pettreat',"Pet Treat", ""),
                ('weights',"Weights", ""),
                ('ropejumpning',"Rope Jumping", ""),
                ('position',"Position", ""),                
                ('avatar',"Avatar", ""),
                ('',"", ""),
        ]
    )

class SVR_VariationSettings(bpy.types.PropertyGroup):
    colorsEnum: EnumProperty(
        name="Colors:",
        description="Color Variations.",
        items=[ ('green',"Green",""),
        ('magenta', "Magenta",""),
        ('orange', "Orange",""),
        ]
    )
    material : bpy.props.PointerProperty(name="MaterialProperty", type= bpy.types.Material)
    mesh : bpy.props.PointerProperty(name="MeshProperty", type= bpy.types.Object)
    prop_list : bpy.props.CollectionProperty(type = ActionListItem)
    list_index : bpy.props.IntProperty(name = "Index for my_list", default = 0)

classes = (
    SVR_Settings,
    ActionListItem,
    SVR_VariationSettings,
    Glimmer_OT_LoadCsvFile,
    Glimmer_OT_MultiRender,
    Glimmer_OT_MultiRender,
    Glimmer_OT_ScaleObject,
    Glimmer_OT_UnScaleObject,
    Glimmer_PT_Panel,
    Glimmer_UL_ActionList,
    Glimmer_OT_AddVariation,
    Glimmer_OT_DeleteVariation,
    LIST_OT_NewItem,
    LIST_OT_NewItemNew,
    LIST_OT_DeleteItem,
    LIST_OT_MoveItem
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.svr_settings = bpy.props.PointerProperty(type = SVR_Settings)
    bpy.types.Scene.my_list = CollectionProperty(type = ActionListItem) 
    bpy.types.Scene.my_variations = CollectionProperty(type = SVR_VariationSettings)
    bpy.types.Scene.list_index = IntProperty(name = "Index for my_list", default = 0)
    bpy.types.Scene.object_list = PointerProperty(type = bpy.data.collections.items)
        
    #Well this is weird but it appears that globals are a little weird in blender addons, this is _one_ way to do it.
    dns = bpy.app.driver_namespace
    dns["pet_names"] = ["hummingbird","ostrich"]
    dns["pet_colors"] =  { "hummingbird" : ["green","magenta","orange"], "ostrich" : ["white","black"] }
    dns["pet_actions"] = []
    dns["pet_skills"] = []
    
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.svr_settings
    del bpy.types.Scene.my_list
    del bpy.types.Scene.my_variations 
    del bpy.types.Scene.list_index

