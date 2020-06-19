import bpy
import csv
from bpy_extras.io_utils import ImportHelper
from moviepy.editor import *

from bpy.types import Operator
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    CollectionProperty
) 
from . glimmer_funcs import gatherData, newRender, validateRenderSettings, SetRenderBlock, newRender, emptyRender, CreateDirectories
from . glimmer_panels import ActionListItem

pet_name = ""
pet_names = []
gifs = []
sections = ["colors", "actions", "skills"]

class Glimmer_OT_LoadNamesCsv(Operator, ImportHelper): 
    bl_idname = "glimmer.load_names_csv" 
    bl_label = "Load a CSV file with pet, color, and action names." 
    
    def execute(self, context): 
        settings = context.scene.svr_settings
        settings.csvFile = self.filepath
        dns = bpy.app.driver_namespace
        #dns_pet_names = dns.get("pet_names")
        #dns_pets = dns.get("pets")
        pets = {}
        with open(self.filepath, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            c_row = 0
            c_sec = 0 #section - [ "colors", "actions", "skills"]
            for row in spamreader:
                c_col = 0 #column
                for item in row:
                    if c_row == 1:
                        pet_names.append(item)                                            
                    elif c_row == 2:
                        for name in pet_names:
                            pets[name] = {}
                            for s in sections:
                                pets[name][s] = []                                
                    elif c_row > 2:
                        if (item == "-standard actions-"):
                            c_sec = 1
                        elif (item == "-skill actions-"):
                            c_sec = 2
                        else:
                            pets[pet_names[c_col]][sections[c_sec]].append(item)
                            c_col += 1
                c_row += 1
        for name in pet_names:
            print(name)
            print("COLORS:")
            enum = []
            for color in pets[name]["colors"]:
                enum.append(color)
            #bpy.types.Scene.svr_settings.colorsEnum = bpy.props.EnumProperty(items= enum)
            print("ACTIONS:")
            for action in pets[name]["actions"]:
                print(action)
            print("SKILLS:")
            for skill in pets[name]["skills"]:
                print(skill)
        
        dns["pet_names"] =  pet_names
        dns["pets"] = pets

        return {'FINISHED'}


class SVR_ActionPropList(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name= "Name")
    prop_list : bpy.props.CollectionProperty(type = ActionListItem)

class Glimmer_OT_LoadCsvFile(Operator, ImportHelper): 
    bl_idname = "glimmer.load_csv_file" 
    bl_label = "Load a CSV file." 
    
    def execute(self, context): 
        settings = context.scene.svr_settings
        settings.csvFile = self.filepath

        dns = bpy.app.driver_namespace
        pet_actions = dns.get("pet_actions")
        with open(self.filepath, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            c_row = 0
            for row in spamreader:
                c_col = 0
                for item in row:
                    if c_row == 0:
                        if c_col in (0,5,8):
                            pet_names.append(item)
                            if c_col == 0:
                                pet_name = "hummingbird" # hell with it, this is all temporary

                    if c_row >= 12 and c_row <= 81:
                        if c_col in (0,5,8):
                            gifs.append(item)
                            if c_col == 0:
                                action_name = item[len(pet_names[0])+1 : len(item)-4]
                                pet_actions.append(action_name)
                                print("('" + action_name + "',\"" + action_name  + "\", \"\")")

                    c_col += 1
                c_row += 1
        temp = 0
        return {'FINISHED'}

class Glimmer_OT_MultiRender(Operator):
    bl_idname = "render.multirender"
    bl_label = "Multi Render"
    bl_description = "Render Three Times!"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scn = context.scene
        settings = context.scene.svr_settings
        validateRenderSettings(settings, context)

        CreateDirectories()

        for item in scn.my_variations:
            if settings.isSkill is True:
                                         
                for ob in bpy.context.scene.objects:
                    if ob.hide_render == False:
                        if ob.type != 'LIGHT':
                            ob.hide_render = True
                            
                string1 =  settings.workDir + "mp4/" + settings.nameEnum + item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum + "-base.jpeg"
                gif1 = settings.workDir + "gif/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum + "-empty.gif"
                scn.render.filepath = string1

                #Enable objects from the hide list.
                emptyRender(item.mesh, item.material)

                clip = ImageClip(string1)
                clip.duration = 0.1
                clip.write_gif(gif1,fps = 24, program="ffmpeg")
                clip.close

                item.mesh.hide_render = False

                #First Render Loop
                string1 = settings.workDir + "mp4/" + settings.nameEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum + "-base.mp4"
                gif1L = settings.workDir + "gif/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum + "-left.gif"
                gif1R = settings.workDir + "gif/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum + "-right.gif"

                scn.render.filepath = string1
                newRender(item.mesh, item.material)

                myclip = VideoFileClip(string1)
                myclip.write_gif(gif1L, program="ffmpeg")

                myclip = myclip.fx( vfx.mirror_x)                
                myclip.write_gif(gif1R, program="ffmpeg")
                myclip.close

            else:

                for ob in bpy.context.scene.objects:
                    if ob.hide_render == False:
                        if ob.type != 'LIGHT':
                            ob.hide_render = True
                item.mesh.hide_render = False            
                #First Render Loop
                string1 = settings.workDir + "mp4/" + settings.nameEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum + ".mp4"
                gif1 = settings.workDir + "gif/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum + ".gif"
                scn.render.filepath = string1
                newRender(item.mesh, item.material)
                myclip = VideoFileClip(string1)
                myclip.write_gif(gif1, fps = 24, program= "ffmpeg", opt = "None")
                myclip.close
                    
        return {"FINISHED"}

class Glimmer_OT_AddVariation(bpy.types.Operator):
    bl_idname = "collections.add_variation"
    bl_label = "Add Variation"
    bl_description = "Adds a new Variation into the tool."
    bl_options = {"REGISTER", "UNDO"}  

    def execute(self, context):
        new_var = context.scene.my_variations.add()
        new_var.name = "Default Name"
        new_var.colorsEnum = bpy.types.Scene.svr_settings.colorsEnum
        return{'FINISHED'}
       
class Glimmer_OT_DeleteVariation(bpy.types.Operator):
    bl_idname = "collections.delete_variation"
    bl_label = "Delete Variation"
    bl_description = "Removes the last Variation in the pool."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        index = len(context.scene.my_variations) - 1
        if index >= 0:
            context.scene.my_variations.remove(index)
            
        return{'FINISHED'}

#########################################

class Glimmer_OT_ScaleObject(bpy.types.Operator):
    bl_idname = "object.scale_object"
    bl_label = "Scale Object"
    bl_description = "Scale selected object to scale_value."
    bl_options = {"REGISTER"}  

    @classmethod
    def poll(cls, context):
        return context.object.select_get()

    def execute(self, context):
        settings = context.scene.svr_settings
        s = settings.scaleValue
        sourceName = context.object.name

        for obj in bpy.data.objects:
            print(obj.name)
        source = bpy.data.objects[sourceName]
        bpy.ops.transform.resize(value=(s,s,s))
        return {'FINISHED'}

class Glimmer_OT_UnScaleObject(bpy.types.Operator):
    bl_idname = "object.unscale_object"
    bl_label = "Unscale Object"
    bl_description = "Scale selected object to inverse of scale_value."

    @classmethod
    def poll(cls, context):
        return context.object.select_get()

    def execute(self, context):
        settings = context.scene.svr_settings
        s = settings.scaleValue
        sourceName = context.object.name
        for obj in bpy.data.objects:
            print(obj.name)
        source = bpy.data.objects[sourceName]
        bpy.ops.transform.resize(value=(1.0/s,1.0/s,1.0/s))
        return {'FINISHED'}
