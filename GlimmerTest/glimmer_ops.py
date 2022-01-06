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
    CollectionProperty,
    PointerProperty
) 
from . glimmer_funcs import (
    AddActionsCollectionCallback,
    AddSkillsCollectionCallback,
    LoadCSVFile,
    PNGTestRender,
    SetupCompositeSystem,
    gatherData,
    newRender,
    validateRenderSettings,
    SetRenderBlock,
    newRender,
    newAvatarRender,
    PNGTestRender,
    emptyRender,
    marathonEmptyRender,
    CreateDirectories,
    AddActionActionPropsFromCollectionCallback,
    AddSkillActionPropsFromCollectionCallback,
    AddActionEnviroPropsFromCollectionCallback,
    AddSkillEnviroPropsFromCollectionCallback,
    MeshFilter,
    CameraFilter,
    RigFilter
)
from . glimmer_panels import ActionListItem, EnviroListItem, EnviroListItem 

gifs = []

def SetFrameStart(self, context):
    context.scene.frame_start = self.floor

def SetFrameEnd(self, context):
    context.scene.frame_end = self.ceiling

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
        #LoadCSVFile         
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
            actionProp = bpy.context.scene.my_action_list.add() #Create Action Prop
            actionProp.name = name

            enviroProp = bpy.context.scene.my_enviro_list.add() #Create Skill Prop
            enviroProp.name = name

            frameRange = bpy.context.scene.frame_range_list.add() #Create Frame List
            frameRange.name = name
            frameRange.floor = 1
            frameRange.ceiling = 60

            cameraPointer = bpy.context.scene.my_camera_list.add()
            cameraPointer.name = name

            petAction = bpy.context.scene.pet_action.add()
            petAction.name = name   

        enum = AddSkillActionPropsFromCollectionCallback()

        for name in enum:
                actionProp = bpy.context.scene.my_action_list.add() #Create Action Prop
                actionProp.name = name

                enviroProp = bpy.context.scene.my_enviro_list.add() #Create Skill Prop
                enviroProp.name = name

                frameRange = bpy.context.scene.frame_range_list.add() #Create Frame List
                frameRange.name = name
                frameRange.floor = 1
                frameRange.ceiling = 60

                cameraPointer = bpy.context.scene.my_camera_list.add()
                cameraPointer.name = name

                petAction = bpy.context.scene.pet_action.add()
                petAction.name = name
                
        CreateDirectories()
        SetupCompositeSystem()
        return {'FINISHED'}

class SVR_ActionPropList(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name= "Name")
    prop_list : bpy.props.CollectionProperty(type = ActionListItem)

class SVR_EnviroPropList(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name= "Name")
    prop_list : bpy.props.CollectionProperty(type = EnviroListItem)

class SVR_FrameRangeList(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name="Name")
    #range_list : bpy.props.CollectionProperty(type = FrameRange)
    name : StringProperty(name="name")
    floor : IntProperty(name="floor", update= SetFrameStart)
    ceiling : IntProperty(name="ceiling", update= SetFrameEnd)

class SVR_CameraList(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name="Name")
    camera : PointerProperty(name="camera", type= bpy.types.Object, poll= CameraFilter)

class SVR_PetActionList(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name="Name")
    action : PointerProperty(name="action", type= bpy.types.Action)

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

    #RENDER LOOP MAP
    #Special Animations: Mistreated, Avatar and Icon Require special setups/render info. (May include Marathon and Juggle as they will have to load things in.)
    #Action Animations: Normal animations for the pet's render. (Now pulling all info from the scene settings.) Renders .PNG's and then converts them into .GIF format afterwards.
    #Skill Animations (save Juggle and Marathon): Sets the correct render settings for the skill animations and does a whole bunch of modifying to them afterwards to make the 3 gifs for each anim.

    def execute(self, context):
        scn = context.scene
        settings = context.scene.svr_settings
        
        SetCamera()

        SetFrameRange()

        validateRenderSettings(settings, context)

        for item in scn.my_variations:
            SetPetAction(item)
            if settings.actionsEnum == "mistreated" and settings.isSkill is False:
                RenderMistreated(self, context, item)  

            elif settings.actionsEnum == "icon" and settings.isSkill is False:
                RenderIcon(self, context, item)

            elif settings.actionsEnum == "avatar" and settings.isSkill is False:
                RenderAvatar(self, context, item)

            elif settings.isSkill is True:
                RenderSkill(self, context, item)

            elif settings.isSkill is False and settings.actionsEnum != "mistreated" and settings.actionsEnum != "avatar" and settings.actionsEnum != "icon":
                RenderAction(self, context, item)   

        return {"FINISHED"}

class Glimmer_OT_RenderAll(bpy.types.Operator):
    bl_idname = "render.renderall"
    bl_label = "Render All"
    bl_description = "Renders each animation sequencially."
    bl_options = {"REGISTER"}

    def execute(self, context):
        scn = context.scene
        settings = context.scene.svr_settings

        enum = AddActionActionPropsFromCollectionCallback()
        skillsenum = AddSkillActionPropsFromCollectionCallback()

        settings.isSkill = False

        for action in enum:
            settings.actionsEnum = action
            SetCamera()

            SetFrameRange()

            validateRenderSettings(settings, context)



            for item in scn.my_variations:
                SetPetAction(item)
                if settings.actionsEnum == "mistreated" and settings.isSkill is False:
                    RenderMistreated(self, context, item)  

                elif settings.actionsEnum == "icon" and settings.isSkill is False:
                    RenderIcon(self, context, item)

                elif settings.actionsEnum == "avatar" and settings.isSkill is False:
                    RenderAvatar(self, context, item)

                elif settings.isSkill is True:
                    RenderSkill(self, context, item)

                elif settings.isSkill is False and settings.actionsEnum != "mistreated" and settings.actionsEnum != "avatar" and settings.actionsEnum != "icon":
                    RenderAction(self, context, item)

        settings.isSkill = True
        for skill in skillsenum:
            settings.skillsEnum = skill
            SetCamera()

            SetFrameRange()

            validateRenderSettings(settings, context)

            for item in scn.my_variations:
                SetPetAction(item)

                if settings.actionsEnum == "mistreated" and settings.isSkill is False:
                    RenderMistreated(self, context, item)  

                elif settings.actionsEnum == "icon" and settings.isSkill is False:
                    RenderIcon(self, context, item)

                elif settings.actionsEnum == "avatar" and settings.isSkill is False:
                    RenderAvatar(self, context, item)

                elif settings.isSkill is True:
                    RenderSkill(self, context, item)

                elif settings.isSkill is False and settings.actionsEnum != "mistreated" and settings.actionsEnum != "avatar" and settings.actionsEnum != "icon":
                    RenderAction(self, context, item)   

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



def SetCamera():
    scn = bpy.context.scene
    settings = scn.svr_settings

    if settings.isSkill is True:
        cam = scn.my_camera_list[settings.skillsEnum].camera
    else:
        cam = scn.my_camera_list[settings.actionsEnum].camera

    if cam is not None:
        scn.camera = cam
    else:
        print("ERROR: Cannot set Camera! Make sure it's set in the SVR Tool!")

def SetFrameRange():
    scn = bpy.context.scene
    settings = scn.svr_settings

    if settings.isSkill is True:
        floor = scn.frame_range_list[settings.skillsEnum].floor
        ceiling = scn.frame_range_list[settings.skillsEnum].ceiling
    else:
        floor = scn.frame_range_list[settings.actionsEnum].floor
        ceiling = scn.frame_range_list[settings.actionsEnum].ceiling

    if floor is not None and ceiling is not None:
        scn.frame_start = floor
        scn.frame_end = ceiling
    else:
        print("ERROR: Cannot set frame range! Check start and end frame numbers for this animation!") 

def SetPetAction(item):
    scn = bpy.context.scene
    settings = scn.svr_settings

    if settings.isSkill is True:
        petAction = scn.pet_action[settings.skillsEnum].action
    else:
        petAction = scn.pet_action[settings.actionsEnum].action

    if petAction is not None:
        if item.rig.animation_data is None:
            item.rig.animation_data_create()
        item.rig.animation_data.action = petAction

def SetPropAction(item):    
    propAction = item.action
   
    if propAction is not None:
        if item.rig is not None:
            if item.rig.animation_data is None:
                item.rig.animation_data_create()
                item.rig.animation_data.action = propAction
        else:
            item.prop.animation_data_create()
            item.prop.animation_data.action = propAction
        
def hideObjects():
    for ob in bpy.context.scene.objects:
        if ob.hide_render == False:
            if ob.type is not 'LIGHT':
                ob.hide_render = True

def Un_HideEnviroProps(settings):
    if settings.isSkill is True:
        for ob in bpy.context.scene.my_enviro_list[settings.skillsEnum].prop_list:
            if ob: 
                ob.prop.hide_render = False
    else:
        for ob in bpy.context.scene.my_enviro_list[settings.actionsEnum].prop_list:
            if ob: 
                ob.prop.hide_render = False

def RenderIcon(self, context, item):
    scn = context.scene
    settings = scn.svr_settings
    hideObjects()
    Un_HideEnviroProps(settings)
    for ob in bpy.context.scene.my_action_list[settings.actionsEnum].prop_list:
       ob.prop.hide_render = False

    #unhide the pet mesh
    item.mesh.hide_render = False

    string1 = settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum + "/" + settings.nameEnum + item.colorsEnum
    gif1 = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + ".gif"
    scn.render.filepath = string1

    checkAndDeleteOldPNG(constructFilePath(self,context,item))

    emptyRender(item.mesh, item.material)

    vid = imageio.imread(string1 + ".png")
    imageio.imwrite(gif1, vid, fps=30)

def RenderMistreated(self, context, item):
    scn = context.scene
    settings = scn.svr_settings

    #Render Mistreated animation.
        #Hide everything.
        #Check the Enviornment Props list
        #Render single frame gif.

    hideObjects()
    Un_HideEnviroProps(settings)

    string1 = constructActionOutputStringPNG(self,context,item) 
    gif1 = constructActionOutputStringGIF(self, context, item)
    scn.render.filepath = string1

    checkAndDeleteOldPNG(constructFilePath(self,context,item))

    emptyRender(item.mesh, item.material)

    vid = imageio.imread(string1 + ".png")
    imageio.imwrite(gif1, vid, fps=30) 

def RenderAvatar(self, context, item):
    scn = context.scene
    settings = scn.svr_settings

    hideObjects()

    #Unhide variation props and pet.
    item.mesh.hide_render = False
    for ob in item.prop_list:
        ob.prop.hide_render = False

    Un_HideEnviroProps(settings)

    for ob in bpy.context.scene.my_action_list[settings.actionsEnum].prop_list:
       ob.prop.hide_render = False

    string1 = constructActionOutputStringPNG(self,context,item) 
    gif1 = constructActionOutputStringGIF(self, context, item)
    scn.render.filepath = string1

    checkAndDeleteOldPNG(constructFilePath(self,context,item))

    newAvatarRender(item.mesh, item.material)

    images = []
    for file_name in os.listdir(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum):
        if file_name.endswith('.png'):
            file_path = os.path.join(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum, file_name)
            images.append(imageio.imread(file_path))
    imageio.mimsave(gif1, images, fps=30)

def RenderSkill(self, context, item):
    scn = context.scene
    settings = scn.svr_settings

   #Turn off all props and meshes and only enable the ones we want.
    for ob in bpy.context.scene.objects:
        if ob.hide_render == False:
            if ob.type != 'LIGHT':
                ob.hide_render = True

    #for ob in bpy.context.scene.my_enviro_list[settings.actionsEnum].prop_list:
    #    if ob: 
    #        ob.prop.hide_render = False
    
    Un_HideEnviroProps(settings)
                
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


    item.mesh.hide_render = False
    for ob in item.prop_list:
        ob.prop.hide_render = False
    for ob in bpy.context.scene.my_action_list[settings.skillsEnum].prop_list:
        ob.prop.hide_render = False
        SetPropAction(ob)

    #First Render Loop
    string1 = settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.skillsEnum  + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum 
    gif1 = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum + "-left.gif"
    gif2 = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum + "-right.gif"

    scn.render.filepath = string1
    
    checkAndDeleteOldPNG(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.skillsEnum)

    if settings.skillsEnum == "marathon" or settings.skillsEnum == "marathonfail" or settings.skillsEnum == "jugglefail" or settings.skillsEnum == "juggle":
        marathonEmptyRender(item.mesh, item.material)
    else:
        PNGTestRender(item.mesh, item.material)
    
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

def RenderAction(self, context, item):
    
    scn = context.scene
    settings = scn.svr_settings

    #Turn off all props and meshes and only enable the ones we want.
    for ob in bpy.context.scene.objects:
        if ob.hide_render == False:
            if ob.type != 'LIGHT':
                ob.hide_render = True

    item.mesh.hide_render = False
    #for ob in bpy.context.scene.my_enviro_list[settings.actionsEnum].prop_list: 
    #    ob.prop.hide_render = False
    Un_HideEnviroProps(settings)
    for ob in item.prop_list:
        if ob is not 'NONETYPE':
            ob.prop.hide_render = False
    for ob in bpy.context.scene.my_action_list[settings.actionsEnum].prop_list:
        if ob is not 'NONETYPE':
            ob.prop.hide_render = False
            SetPropAction(ob)

    #First Render Loop
    #string1 = settings.workDir + "mp4/" + settings.nameEnum + "/" + item.colorsEnum + "/"+ item.colorsEnum + "-" + settings.actionsEnum + ".mp4"
    string1 = settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum 
    gif1 = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum + ".gif"
    scn.render.filepath = string1

    checkAndDeleteOldPNG(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum)

    PNGTestRender(item.mesh, item.material)

    images = []
    for file_name in os.listdir(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum):
        if file_name.endswith('.png'):
            file_path = os.path.join(settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum, file_name)
            images.append(imageio.imread(file_path))
    imageio.mimsave(gif1, images, fps=30)

def constructFilePath(self,context, item):
    settings = context.scene.svr_settings

    string = settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum
    return string

def constructActionOutputStringPNG(self, context, item):
    settings = context.scene.svr_settings

    string = settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.actionsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum
    return string

def constructActionOutputStringGIF(self, context, item):
    settings = context.scene.svr_settings
    string = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.actionsEnum + ".gif"
    return string

def constructSkillnOutputStringPNG(self, context, item):
    settings = context.scene.svr_settings

    string = settings.workDir + "png/" + settings.nameEnum + "/" + item.colorsEnum + "/" + settings.skillsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum
    return string

def constructSkillOutputStringGIF(self, context, item):
    settings = context.scene.svr_settings
    string = settings.workDir + "gif/" + settings.nameEnum + "/"+ item.colorsEnum + "/" + settings.nameEnum + item.colorsEnum + "-" + settings.skillsEnum + ".gif"
    return string

def checkAndDeleteOldPNG(string):
    if os.path.exists(string):
        for file_name in os.listdir(string):
            if file_name.endswith('.png'):
                os.remove(os.path.join(string, file_name))

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
