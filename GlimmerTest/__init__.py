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
    CollectionProperty
) 

from . glimmer_ops import Glimmer_OT_LoadCsvFile, Glimmer_OT_MultiRender, Glimmer_OT_SetMaterialDefault,Glimmer_OT_ScaleObject, Glimmer_OT_UnScaleObject
from . glimmer_panels import Glimmer_PT_Panel, Glimmer_UL_ActionList, ActionListItem, LIST_OT_NewItem, LIST_OT_DeleteItem, LIST_OT_MoveItem
#Glimmer_PT_VariationPanel,

myTestArray = ["test string one","test string two"]

class SVR_Settings(bpy.types.PropertyGroup):
    workDir : bpy.props.StringProperty(name = "Work Directory", default = "C:\\work\\")
    petName : bpy.props.StringProperty(name = "Pet Type", default = "PetName")
    petColor1 : bpy.props.StringProperty(name = "Default Color Name", default = "Color1")
    petColor2 : bpy.props.StringProperty(name = "Variation 1 Color Name", default = "Color2")
    petColor3 : bpy.props.StringProperty(name = "Variation 2 Color Name", default = "Color3")
    animationName : bpy.props.StringProperty(name = "Animation Title", default = "DefaultAnimation")
    csvFile : StringProperty(name="CSV Filename")
    scaleValue : FloatProperty(name="Global scale value",default=1.0)
    skillFail: BoolProperty(name="SkillFail:", description="Pet Fails at Skill.")    
    skillHandEnum: EnumProperty(
        name="Skills:",
        description="Pet Skill Hand.",
        items=[ ('empty',"Empty", ""),
                ('right',"Right", ""),
                ('left',"Left", ""),
        ]
    )
    skillsEnum: EnumProperty(
        name="Skills:",
        description="Pet Skills.",
        items=[ ('singing',"Singing", ""),
                ('knitting',"Knitting", ""),
                ('bubbles',"Bubbles", ""),
                ('hiding',"Hiding", ""),
                ('hypnotize',"Hypnotize", ""),
                ('juggle',"Juggle", ""),
                ('marathon',"Marathon", ""),
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

classes = (
    SVR_Settings,
    Glimmer_OT_LoadCsvFile,
    Glimmer_OT_MultiRender,
    Glimmer_OT_SetMaterialDefault,
    Glimmer_OT_ScaleObject,
    Glimmer_OT_UnScaleObject,
    Glimmer_PT_Panel,
    Glimmer_UL_ActionList,
    #Glimmer_PT_VariationPanel,
    ActionListItem,
    LIST_OT_NewItem,
    LIST_OT_DeleteItem,
    LIST_OT_MoveItem
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.svr_settings = bpy.props.PointerProperty(type = SVR_Settings)
    bpy.types.Scene.my_list = CollectionProperty(type = ActionListItem) 
    bpy.types.Scene.list_index = IntProperty(name = "Index for my_list", default = 0)
        
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
    del bpy.types.Scene.list_index

