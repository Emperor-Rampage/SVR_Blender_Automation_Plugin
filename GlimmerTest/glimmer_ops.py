import bpy
import csv
import xml.etree.ElementTree as ET
from bpy_extras.io_utils import ImportHelper
from moviepy.editor import *

from bpy.types import Operator
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    StringProperty
) 

from . glimmer_funcs import gatherData, newRender, validateRenderSettings, SetRenderBlock, newRender, emptyRender

pet_name = ""
pet_names = []
colors = []
actions = []
skills = []
gifs = []

class Glimmer_OT_LoadXMLFile(Operator, ImportHelper):
    bl_idname = "glimmer.load_xml_file" 
    bl_label = "Load an XML file." 

    def execute(self, context):
        settings = context.scene.svr_settings
        settings.xmlFile = self.filepath

        root = ET.fromstring(settings.xmlFile)

        for animal in root.findall('animal'):
            bpy.context.scene.svr_settings.nameEnum.append((animal.attrib, animal.attrib, animal.attrib))

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

class Glimmer_OT_NewMultiRender(Operator):
    bl_idname = "render.newmultirender"
    bl_label = "Multi Render"
    bl_description = "Render Three Times!"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        scn = context.scene
        mysettings = context.scene.svr_settings
        validateRenderSettings(mysettings,scn)

        for item in scn.my_variations:
            if mysettings.isSkill is True:
                #Empty Render Loop TO-DO
                    #Walk through all objects in the scene.
                    #Turn the render visibility off on objects that need to be turned off, and gather the ones that are turned off.
                    #Render out one empty framed .mp4 of the background.
                    #Convert the .mp4 to a .gif.
                    #Save once for each variation, giving it the '-empty.gif' ending tag.
                    #Close the clip and re-enable all the objects that were turned off during the walk.
                    #DONE.
                                         
                for ob in bpy.context.scene.objects:
                    if ob.hide_render == False:
                        if ob.type != 'LIGHT':
                            ob.hide_render = True
                            
                string1 = "C:/work/mp4/" + mysettings.nameEnum + item.colorsEnum + "/" + mysettings.nameEnum + item.colorsEnum + "-" + mysettings.actionsEnum + "-base.jpeg"
                gif1 = "C:/work/gif/" + mysettings.nameEnum + item.colorsEnum + "-" + mysettings.actionsEnum + "-empty.gif"
                scn.render.filepath = string1

                #Enable objects from the hide list.
                emptyRender(item.mesh, item.material)

                clip = ImageClip(string1)
                clip.duration = 0.1
                clip.write_gif(gif1,fps = 24, program="ffmpeg")
                clip.close

                item.mesh.hide_render = False

                #First Render Loop
                string1 = "C:\work\mp4\\" + mysettings.nameEnum + "\\" + mysettings.nameEnum + item.colorsEnum + "-" + mysettings.actionsEnum + "-base.mp4"
                gif1L = "C:\work\gif\\" + mysettings.nameEnum + item.colorsEnum + "-" + mysettings.actionsEnum + "-left.gif"
                gif1R = "C:\work\gif\\" + mysettings.nameEnum + item.colorsEnum + "-" + mysettings.actionsEnum + "-right.gif"

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
                string1 = "C:\work\mp4\\" + mysettings.nameEnum + "\\" + mysettings.nameEnum + item.colorsEnum + "-" + mysettings.actionsEnum + ".mp4"
                gif1 = "C:\work\gif\\" + mysettings.nameEnum + item.colorsEnum + "-" + mysettings.actionsEnum + ".gif"
                scn.render.filepath = string1
                newRender(item.mesh, item.material)
                myclip = VideoFileClip(string1)
                myclip.write_gif(gif1, fps = 24, program= "ffmpeg", opt = "None")
                myclip.close
                    
        return {"FINISHED"}

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
        pet = context.active_object
        mysettings = context.scene.my_settings
        DefaultMat = gatherData("DefaultMat")
        MaterialVar2 = gatherData("MaterialVar2")
        MaterialVar3 = gatherData("MaterialVar3")
        validateRenderSettings(mysettings,scn)                 

        if mysettings.isSkill is True:
            #Empty Render Loop TO-DO
                #Walk through all objects in the scene.
                #Turn the render visibility off on objects that need to be turned off, and gather the ones that are turned off.
                #Render out one empty framed .mp4 of the background.
                #Convert the .mp4 to a .gif.
                #Save once for each variation, giving it the '-empty.gif' ending tag.
                #Close the clip and re-enable all the objects that were turned off during the walk.
                #DONE.
            
            #First Render Loop
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

            #Second Render Loop
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

            #Third Render Loop
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
            string1 = "C:\work\mp4\r" + mysettings.petName + "\r" + mysettings.petName + mysettings.petColor1 + "-" + mysettings.animationName + ".mp4"
            gif1 = "C:\work\gif\r" + mysettings.petName + mysettings.petColor1 + "-" + mysettings.animationName + ".gif"
            scn.render.filepath = string1
            newRender(pet, DefaultMat)
            myclip = VideoFileClip(string1)
            myclip.write_gif(gif1, fps = 24, program= "ffmpeg", opt = "None")
            myclip.close
            

            #Second Render Loop
            string2 = "C:\work\mp4\r" + mysettings.petName + "\r" + mysettings.petName + mysettings.petColor2 + "-" + mysettings.animationName + ".mp4"
            gif2 = "C:\work\r" + mysettings.petName + mysettings.petColor2 + "-" + mysettings.animationName + ".gif"
            scn.render.filepath = string2
            newRender(pet, MaterialVar2)
            myclip = VideoFileClip(string2)
            myclip.write_gif(gif2, fps = 24, program= "ffmpeg", opt = "None")
            myclip.close

            #Third Render Loop
            string3 = "C:\work\mp4\r" + mysettings.petName + "\r" + mysettings.petName  + mysettings.petColor3 + "-" + mysettings.animationName + ".mp4"
            gif3 = "C:\work\gif\r"  + mysettings.petName + "\r"+ mysettings.petName + mysettings.petColor3 + "-" + mysettings.animationName + ".gif"
            scn.render.filepath = string3
            newRender(pet, MaterialVar3)
            myclip = VideoFileClip(string3)
            myclip.write_gif(gif3, fps = 24, program= "ffmpeg", opt = "None")
            myclip.close()
        
        return {'FINISHED'}

class Glimmer_OT_AddVariation(bpy.types.Operator):
    bl_idname = "collections.add_variation"
    bl_label = "Add Variation"
    bl_description = "Adds a new Variation into the tool."
    bl_options = {"REGISTER", "UNDO"}  

    def execute(self, context):
        new_var = context.scene.my_variations.add()
        new_var.name = "Default Name"
        return{'FINISHED'}
       
class Glimmer_OT_DeleteVariation(bpy.types.Operator):
    bl_idname = "collections.delete_variation"
    bl_label = "Delete Variation"
    bl_description = "Removes the last Variation in the pool."
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        index = len(context.scene.my_variations) - 1
        if index >= 0:
            remove_var = context.scene.my_variations.remove(index)
            return{'FINISHED'}
        return{'FAILED'}

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
