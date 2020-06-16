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
    "name" : "Glimmer_SVR_Automation",
    "author" : "Conner Lindsley, Chris Calef",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Render"
}

import bpy
import os, sys
import imageio
from moviepy.editor import *

enum_menu_items = [
                ('OPT1','Option 1','',1),
                ('OPT2','Option 2','',2),
                ('OPT3','Option 3','',3),
                ('OPT4','Option 4','',4),
                ]

def gatherData(string):
    DefaultMat = bpy.data.materials.get(string)
    if DefaultMat is None:
        DefaultMat = bpy.data.materials.new(name=string)
    return DefaultMat

def newRender(object, material):
    if object.data.materials:
            object.data.materials[0] = material
    else:
            object.data.materials.append(material)
    bpy.ops.render.render(animation=True)

def validateRenderSettings(self, context):
    if self.isSkill is True:
        bpy.context.scene.render.resolution_x = 232
        bpy.context.scene.render.resolution_y = 346
    else:
        bpy.context.scene.render.resolution_x = 464
        bpy.context.scene.render.resolution_y = 346        
    SetRenderBlock()

def SetRenderBlock():
    bpy.context.scene.render.use_file_extension = False
    bpy.context.scene.render.image_settings.file_format = "FFMPEG"
    bpy.context.scene.render.image_settings.color_mode = "RGB"
    bpy.context.scene.render.ffmpeg.format = "MPEG4"
    bpy.context.scene.render.ffmpeg.codec = "MPEG4"
    bpy.context.scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
    bpy.context.scene.render.ffmpeg.ffmpeg_preset = "GOOD"
    bpy.context.scene.render.ffmpeg.gopsize = 18
    bpy.context.scene.render.ffmpeg.audio_codec = "NONE"


class MySettings(bpy.types.PropertyGroup):
    isSkill : bpy.props.BoolProperty(name = "isSkill", 
                description = "Boolean that confirms if the current animations is supposed to be a skill animation or not.", 
                default = False, 
                update = validateRenderSettings,
                )
    petName : bpy.props.StringProperty(name = "Pet Type", default = "PetName")
    petColor1 : bpy.props.StringProperty(name = "Default Color Name", default = "Color1")
    petColor2 : bpy.props.StringProperty(name = "Variation 1 Color Name", default = "Color2")
    petColor3 : bpy.props.StringProperty(name = "Variation 2 Color Name", default = "Color3")
    animationName : bpy.props.StringProperty(name = "Animation Title", default = "DefaultAnimation")

class SetMaterialDefault(bpy.types.Operator):
    bl_idname = "material.set"
    bl_label = "Set Material"
    
    def execute(self, context):
        pet = bpy.context.active_object
        pet.active_material = gatherData("DefaultMat")

class CustomMenu(bpy.types.Menu):
    """Demo custom menu"""
    # example menu from Templates->Python->ui_menu.py
    bl_label = "Custom Menu"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("wm.open_mainfile")
        layout.operator("wm.save_as_mainfile").copy = True

        layout.operator("object.shade_smooth")

        layout.label(text = "Hello world!", icon = 'WORLD_DATA')

        # use an operator enum property to populate a sub-menu
        layout.operator_menu_enum("object.select_by_type",
                                  property="type",
                                  text="Select All by Type...",
                                  )

        # call another menu
        layout.operator("wm.call_menu", text="Unwrap").name = "VIEW3D_MT_uv_map"

class VariationSettingItem(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name = "Variation Name", default = "Default")
    meshName: bpy.props.StringProperty(name = "Mesh Name", default = "Default")
    materialName: bpy.props.StringProperty(name = "Material Name", default = "Default")

variations = {
    1 : {'name' : 'Default Name', 'material' : 'Default Mat', 'model' : 'Default Model'},
    2 : {'name' : 'Default Name', 'material' : 'Default Mat', 'model' : 'Default Model'},
    3 : {'name' : 'Default Name', 'material' : 'Default Mat', 'model' : 'Default Model'}
}

class ButtonOperator(bpy.types.Operator):
    bl_idname =  'button.operation'
    bl_label = 'ButtonOperator'
    bl_description = 'Operator that runs the adding and subtracting of items into the variation enum.'
    bl_options = {'REGISTER', 'UNDO'}

    
    #def AddVariation(name, material, model):

class LayoutPanel(bpy.types.Panel):
    bl_label = "MultiRender"
    bl_idname = "OBJECT_PT_layout_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        #self.layout.operator("object.mode_set", text='Edit', icon='EDITMODE_HLT').mode='EDIT'
        pet = bpy.context.active_object
        mysettings = bpy.context.scene.my_settings

        layout.label(text = "Test Operators")
        layout.row().prop(mysettings, "isSkill", text = "Render as Skill?")
        layout.row().prop(mysettings, "petName", text = "Pet Name")
        layout.row().prop(mysettings, "petColor1", text = "Color 1")
        layout.row().prop(mysettings, "petColor2", text = "Color 2")
        layout.row().prop(mysettings, "petColor3", text = "Color 3")
        layout.row().prop(mysettings, "animationName", text = "Animation Title")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        #row.operator( "material.set", text="Set Default Mat", icon='OBJECT_DATAMODE')
        row.operator("render.multirender", text="Multi Render", icon='OBJECT_DATAMODE')

        for var in variations:
            layout.label(text = "Test Operators")
            row = layout.row(align=True)
            row.alignment = 'EXPAND'
            row.label(text = variations[var]['name'])
            row.label(text = variations[var]['material'])
            row.label(text = variations[var]['model'])

        buttonRow = layout.row(align=True)
        row.alignment = 'EXPAND'
        #row.operator()

        #row.operator("object.mode_set", text="Set Var 3", icon='OBJECT_DATAMODE').mode='TEXTURE_PAINT'

        #row = layout.row()
        #box = row.box()

        #row = box.row()
        #row.label(text = "Some menus", icon='LINENUMBERS_ON')

        #row = box.row()
        # add the custom menu defined above
        #box.menu(CustomMenu.bl_idname,text = 'My custom menu', icon='PREFERENCES')

        #row = box.row()
        # add a standard blender menu - the add menu
        #box.menu('VIEW3D_MT_mesh_add', text ='Add', icon='PLUS')

        #row = box.row()
        # add an enum property menu
        # this allows only certain values to be set for a property
        #box.prop_menu_enum(context.scene, 'test_enum', text='enum property', icon='ALIGN_LEFT')

class MultiRender(bpy.types.Operator):
    bl_idname = "render.multirender"
    bl_label = "Multi Render"
    bl_description = "Render Three Times!"
    bl_options = {"REGISTER"}  

    @classmethod
    def poll(cls, context):
        return True 

    def execute(self, context):

        scn = bpy.context.scene
        pet = bpy.context.active_object
        mysettings = bpy.context.scene.my_settings
        DefaultMat = gatherData("DefaultMat")
        MaterialVar2 = gatherData("MaterialVar2")
        MaterialVar3 = gatherData("MaterialVar3")
        validateRenderSettings(mysettings,scn)

        if mysettings.isSkill is True:
     
            string1 = "C:\work\mp4\\" + mysettings.petName + "\\ " + mysettings.petName + mysettings.petColor1 + "-" + mysettings.animationName + "-left.mp4"
            gif1L = "C:\work\gif\\" + mysettings.petName + mysettings.petColor1 + "-" + mysettings.animationName + "-left.gif"
            gif1R = "C:\work\gif\\" + mysettings.petName + mysettings.petColor1 + "-" + mysettings.animationName + "-right.gif"

            scn.render.filepath = string1
            newRender(pet, DefaultMat)

            myclip = VideoFileClip(string1)
            myclip.write_gif(gif1L, program="ffmpeg")

            mirroredClip = myclip.fx( vfx.mirror_x)
            myclip.close
            mirroredClip.write_gif(gif1R, program="ffmpeg")
            mirroredClip.close


            string2 = "C:\work\\" + mysettings.petName + mysettings.petColor2 + "-" + mysettings.animationName + "-left.mp4"
            gif2L = "C:\work\gif\\" + mysettings.petName + mysettings.petColor2 + "-" + mysettings.animationName + "-left.gif"
            gif2R = "C:\work\gif\\" + mysettings.petName + mysettings.petColor2 + "-" + mysettings.animationName + "-right.gif"

            scn.render.filepath = string2
            newRender(pet, MaterialVar2)
            myclip = VideoFileClip(string2)
            myclip.write_gif(gif2L, program="ffmpeg")

            mirroredClip = myclip.fx( vfx.mirror_x)
            myclip.close
            mirroredClip.write_gif(gif2R, program="ffmpeg")
            mirroredClip.close


            string3 = "C:\work\\" + mysettings.petName + mysettings.petColor3 + "-" + mysettings.animationName + "-left.mp4"

            gif3L = "C:\work\gif\\" + mysettings.petName + mysettings.petColor3 + "-" + mysettings.animationName + "-left.gif"
            gif3R = "C:\work\gif\\" + mysettings.petName + mysettings.petColor3 + "-" + mysettings.animationName + "-right.gif"

            newRender(pet, MaterialVar3)
            myclip = VideoFileClip(string3)
            myclip.write_gif(gif3L, program="ffmpeg")

            mirroredClip = myclip.fx( vfx.mirror_x)
            myclip.close
            mirroredClip.write_gif(gif3R, program="ffmpeg")
            mirroredClip.close

        else:
            #First Render Loop
            string1 = "C:\work\mp4\\" + mysettings.petName + "\\" + mysettings.petName + mysettings.petColor1 + "-" + mysettings.animationName + ".mp4"
            gif1 = "C:\work\\" + mysettings.petName + mysettings.petColor1 + "-" + mysettings.animationName + ".gif"
            scn.render.filepath = string1
            newRender(pet, DefaultMat)
            myclip = VideoFileClip(string1)
            myclip.write_videofile(string1)
            myclip.close

            myclip = VideoFileClip(string1)
            myclip.write_gif(gif1, fps = myclip.fps, program= "ffmepg", opt = "None")
            myclip.close
            

            #Second Render Loop
            string2 = "C:\work\mp4\\" + mysettings.petName + "\\ " + mysettings.petName + mysettings.petColor2 + "-" + mysettings.animationName + ".mp4"
            gif2 = "C:\work\gif\\"  + mysettings.petName + "\\ " + mysettings.petName + mysettings.petColor2 + "-" + mysettings.animationName + ".gif"
            scn.render.filepath = string2
            newRender(pet, MaterialVar2)
            myclip = VideoFileClip(string2)
            myclip.write_gif(gif2, fps = myclip.fps, program= "ffmpeg", opt = "None")
            

            #Third Render Loop
            string3 = "C:\work\mp4\\" + mysettings.petName + "\\ " + mysettings.petName  + mysettings.petColor3 + "-" + mysettings.animationName + ".mp4"
            gif3 = "C:\work\gif\\"  + mysettings.petName + "\\ "+ mysettings.petName + mysettings.petColor3 + "-" + mysettings.animationName + ".gif"
            scn.render.filepath = string3
            newRender(pet, MaterialVar3)
            myclip = VideoFileClip(string3)
            myclip.write_gif(gif3, fps = myclip.fps, program= "ffmpeg", opt = "None")
            myclip.close()
        
        pet.data.materials[0] = DefaultMat
        return {'FINISHED'}

classes = (
    MySettings,
    MultiRender,
    CustomMenu,
    LayoutPanel,
    SetMaterialDefault,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.test_enum = bpy.props.EnumProperty(items=enum_menu_items)
    bpy.types.Scene.my_settings = bpy.props.PointerProperty(type = MySettings)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.my_settings
    del bpy.types.Scene.test_enum


if __name__ == "__main__":
    register()