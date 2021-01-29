from typing import Type
import bpy
import csv
from bpy_extras.io_utils import ImportHelper
from moviepy.editor import *
import imageio
from numpy import fliplr

from bpy.types import Operator
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    CollectionProperty
) 
from . glimmer_funcs import PNGTestRender, gatherData, newRender, validateRenderSettings, SetRenderBlock, newRender, newAvatarRender, PNGTestRender, emptyRender, marathonEmptyRender, CreateDirectories, AddActionActionPropsFromCollectionCallback, AddSkillActionPropsFromCollectionCallback, AddActionEnviroPropsFromCollectionCallback, AddSkillEnviroPropsFromCollectionCallback
from . glimmer_panels import ActionListItem, EnviroListItem, ActionPointer, CameraPointer, EnviroListItem, FrameRange

gifs = []

class MyItem(bpy.types.PropertyGroup):
    @classmethod
    def register(cls):
        bpy.types.Scene.my_items = bpy.props.CollectionProperty(type=MyItem)

    @classmethod
    def unregister(cls):
        del bpy.types.Scene.my_items

    some_str : bpy.props.StringProperty(
        name = "asdf",
        default = ""
    )

class MY_OT_add_item(bpy.types.Operator):
    ''' add item to bpy.context.scene.my_items '''
    bl_label = "add item"
    bl_idname = "my.add_item"

    def execute(self, context):
        # create a new item, assign its properties
        item = bpy.context.scene.my_items.add()
        item.some_str = "asdf" + str(len(bpy.context.scene.my_items))
        return {'FINISHED'}

class Glimmer_OT_LoadNamesCsv(Operator, ImportHelper): 
    bl_idname = "glimmer.load_names_csv" 
    bl_label = "Load a CSV file with pet, color, and action names." 
    
    def execute(self, context): 
        settings = context.scene.svr_settings
        settings.csvFile = self.filepath
        sections = ["colors", "actions", "skills"]
        pet_names = []
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
            #print(name)
            #print("COLORS:")
            enum = []
            for color in pets[name]["colors"]:
                enum.append(color)
            #print("ACTIONS:")
            for action in pets[name]["actions"]:
                print(action)
            #print("SKILLS:")
            for skill in pets[name]["skills"]:
                print(skill)
        
        dns = bpy.app.driver_namespace
        dns["pet_names"] =  pet_names
        dns["pets"] = pets

        enum = AddActionActionPropsFromCollectionCallback()
        
        for name in enum:
            new = bpy.context.scene.my_action_list.add()
            new.name = name
        

        enum = AddSkillActionPropsFromCollectionCallback()

        for name in enum:
            new = bpy.context.scene.my_action_list.add()
            new.name = name


        enum = AddActionEnviroPropsFromCollectionCallback()
        
        for name in enum:
            new = bpy.context.scene.my_enviro_list.add()
            new.name = name

        enum = AddSkillEnviroPropsFromCollectionCallback()
        
        for name in enum:
            new = bpy.context.scene.my_enviro_list.add()
            new.name = name

        return {'FINISHED'}


class SVR_ActionPropList(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name= "Name")
    prop_list : bpy.props.CollectionProperty(type = ActionListItem)

class SVR_EnviroPropList(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name= "Name")
    prop_list : bpy.props.CollectionProperty(type = EnviroListItem)

class SVR_FrameRangeList(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name="name")
    range_list : bpy.props.CollectionProperty(type = FrameRange)

class SVR_CameraList(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name="name")
    camera_list : bpy.props.CollectionProperty(type = CameraPointer)

class SVR_PetActionList(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name="name")
    action_list : bpy.props.CollectionProperty(type= ActionPointer)

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
    bl_description = "Render each variation with the current animation."
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
            if settings.actionsEnum == "mistreated" and settings.isSkill is False:
                #Render Mistreated animation.
                    #Hide everything.
                    #Check the Enviornment Props list
                    #Un-hide everything in that list.
                    #Render single frame gif for that one.
                for ob in bpy.context.scene.objects:
                    if ob.hide_render == False:
                        if ob.type != 'LIGHT':
                            ob.hide_render = True

                for ob in scn.my_enviro_list:
                    if ob: 
                        ob.prop.hide_render = False

                string1 =  settings.workDir + "mp4/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + "Empty" + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum + "-base"
                gif1 = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum + ".gif"
                scn.render.filepath = string1                
                emptyRender(item.mesh, item.material)

                vid = imageio.imread(string1 + ".png")
                imageio.imwrite(gif1, vid, fps=30)

                #clip = ImageClip(string1)
                #clip.duration = 0.1
                #clip.write_gif(gif1,fps = 30, program="ffmpeg")
                #clip.close
 
                        
            elif settings.actionsEnum == "icon" and settings.isSkill is False:

                for ob in bpy.context.scene.objects:
                    if ob.hide_render == False:
                        if ob.type != 'LIGHT':
                            ob.hide_render = True
                item.mesh.hide_render = False

                string1 =  settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum 
                gif1 = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + ".gif"
                scn.render.filepath = string1
                emptyRender(item.mesh, item.material)

                images = []
                for file_name in os.listdir(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum):
                    if file_name.endswith('.png'):
                        file_path = os.path.join(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum, file_name)
                        images.append(imageio.imread(file_path))
                imageio.mimsave(gif1, images, fps=30)

                #clip = ImageClip(string1)
                #clip.duration = 0.1
                #clip.write_gif(gif1,fps = 30, program="ffmpeg")
                #clip.close

            elif settings.actionsEnum == "avatar" and settings.isSkill is False:

                for ob in bpy.context.scene.objects:
                    if ob.hide_render == False:
                        if ob.type != 'LIGHT':
                            ob.hide_render = True
                item.mesh.hide_render = False
                string1 =  settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum 
                gif1 = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum + ".gif"
                scn.render.filepath = string1

                newAvatarRender(item.mesh, item.material)

                images = []
                for file_name in os.listdir(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum):
                    if file_name.endswith('.png'):
                        file_path = os.path.join(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum, file_name)
                        images.append(imageio.imread(file_path))
                imageio.mimsave(gif1, images, fps=30)

                #clip = ImageSequenceClip(settings.workDir + "png/" + settings.nameEnum + item.colorsEnum + "/", with_mask= True, set_duration=.01)
                #clip.duration = 0.1
                #clip.write_gif(gif1,fps = 30, program="ffmpeg")
                #clip.close


            elif settings.isSkill is True:
                #Add special setup for Marathon-empty, rendering out all the frames.
                                         
                for ob in bpy.context.scene.objects:
                    if ob.type != 'NONETYPE': 
                        if ob.hide_render == False:
                            if ob.type != 'LIGHT':
                                ob.hide_render = True

                for ob in scn.my_enviro_list:
                    if ob: 
                        ob.prop.hide_render = False
                            
                string1 =  settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.skillsEnum + "/" + "Empty" +"/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum + "-empty"
                gif1 = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum + "-empty.gif"
                scn.render.filepath = string1

                #Enable objects from the hide list.
                if settings.skillsEnum == "marathon" or settings.skillsEnum == "marathonfail" or settings.skillsEnum == "jugglefail" or settings.skillsEnum == "juggle":
                    marathonEmptyRender(item.mesh, item.material)
                else:
                    emptyRender(item.mesh, item.material)

                images = []
                for file_name in os.listdir(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.skillsEnum + "/" + "Empty"):
                    if file_name.endswith('.png'):
                        file_path = os.path.join(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.skillsEnum + "/" + "Empty", file_name)
                        images.append(imageio.imread(file_path))
                imageio.mimsave(gif1, images, fps=30)

                #clip = ImageClip(string1)
                #clip.duration = 0.1
                #clip.write_gif(gif1,fps = 30, program="ffmpeg")
                #clip.close

                item.mesh.hide_render = False
                for ob in item.prop_list:
                    ob.prop.hide_render = False
                for ob in bpy.context.scene.my_action_list[settings.skillsEnum].prop_list:
                    ob.prop.hide_render = False

                #First Render Loop
                string1 = settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.skillsEnum  + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum 
                #string2 = settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.skillsEnum  + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum 
                gif1 = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum + "-left.gif"
                gif2 = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum + "-right.gif"

                scn.render.filepath = string1
                #newRender(item.mesh, item.material)
                if settings.skillsEnum == "marathon" or settings.skillsEnum == "marathonfail" or settings.skillsEnum == "jugglingfail" or settings.skillsEnum == "juggling":
                    marathonEmptyRender(item.mesh, item.material)
                else:
                    PNGTestRender(item.mesh, item.material)
                #myclip = VideoFileClip(string1)
                #myclip = myclip.fx( vfx.mirror_x)
                #myclip.write_videofile(string2)

                images = []
                for file_name in os.listdir(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.skillsEnum):
                    if file_name.endswith('.png'):
                        file_path = os.path.join(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.skillsEnum, file_name)
                        images.append(imageio.imread(file_path))
                imageio.mimsave(gif1, images, fps=30)

                images = []
                for file_name in os.listdir(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.skillsEnum):
                    if file_name.endswith('.png'):
                        file_path = os.path.join(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.skillsEnum, file_name)
                        images.append(fliplr(imageio.imread(file_path)))
                imageio.mimsave(gif2, images, fps=30)

            elif settings.isSkill is False and settings.actionsEnum != "mistreated" and settings.actionsEnum != "avatar" and settings.actionsEnum != "icon":

                #Turn off all props and meshes and only enable the ones we want.
                for ob in bpy.context.scene.objects:
                    if ob.hide_render == False:
                        if ob.type != 'LIGHT':
                            ob.hide_render = True

                item.mesh.hide_render = False
                for ob in scn.my_enviro_list:
                    if ob: 
                        ob.prop.hide_render = False
                for ob in item.prop_list:
                    if ob: 
                        ob.prop.hide_render = False
                for ob in bpy.context.scene.my_action_list[settings.actionsEnum].prop_list:
                    if ob:
                        ob.prop.hide_render = False

                #First Render Loop
                #string1 = settings.workDir + "mp4/" + settings.nameEnum + "/" + item.colorsEnum + "/"+ item.colorsEnum + "-" + settings.actionsEnum + ".mp4"
                string1 = settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum 
                gif1 = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum + ".gif"
                scn.render.filepath = string1

                PNGTestRender(item.mesh, item.material)

                images = []
                for file_name in os.listdir(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum):
                    if file_name.endswith('.png'):
                        file_path = os.path.join(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum, file_name)
                        images.append(imageio.imread(file_path))
                imageio.mimsave(gif1, images, fps=30)

        return {"FINISHED"}

class Glimmer_OT_RenderAll(bpy.types.Operator):
    bl_idname = "render.renderall"
    bl_label = "Render All"
    bl_description = "Renders each animation sequencially."
    bl_options = {"REGISTER"}

    def execute(self, context):
        return{"FINISHED"}
    
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
