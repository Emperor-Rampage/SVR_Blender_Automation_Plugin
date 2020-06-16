import bpy
import csv
from bpy_extras.io_utils import ImportHelper

from bpy.types import Operator
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    StringProperty
) 

from . glimmer_funcs import gatherData, newRender, validateRenderSettings, SetRenderBlock

pet_name = ""
pet_names = []
colors = []
actions = []
skills = []
gifs = []

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



class Glimmer_OT_MultiRender(bpy.types.Operator):
    bl_idname = "render.multirender"
    bl_label = "Multi Render"
    bl_description = "Render Three Times!"
    bl_options = {"REGISTER"}  

    @classmethod
    def poll(cls, context):
        return True 
    
    def execute(self, context):
        scn = context.scene
        pet = context.active_object        
        settings = context.scene.svr_settings
        DefaultMat = gatherData("DefaultMat")
        MaterialVar2 = gatherData("MaterialVar2")
        MaterialVar3 = gatherData("MaterialVar3")
        validateRenderSettings(mysettings,scn)
        #do a bunch of work here...
        return {'FINISHED'}


#########################################


class Glimmer_OT_SetMaterialDefault(bpy.types.Operator):
    bl_idname = "material.set"
    bl_label = "Set Material"
    
    def execute(self, context):
        pet = context.active_object
        pet.active_material = gatherData("DefaultMat")



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

        ## TEMP, testing #######
        dns = bpy.app.driver_namespace
        pet_names = dns.get("pet_names")
        pet_colors = dns.get("pet_colors")
        pet_actions = dns.get("pet_actions")
        pet_skills = dns.get("pet_skills")
        print("Scaling the " + sourceName + ", pet names[0]: " + pet_names[0] + " pet actions: " + str(len(pet_actions)))
        ########################

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
