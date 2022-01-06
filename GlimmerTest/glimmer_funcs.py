import bpy
import os
from bpy_extras.io_utils import ImportHelper
import csv

def RigFilter(self, object):
    return object.type == "ARMATURE"
def MeshFilter(self, object):
    return object.type == "MESH" or object.type == "LIGHT"
def CameraFilter(self, object):
    return object.type == "CAMERA"

def AddNew(ActionList):
    ActionList.add()

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

def newAvatarRender(object, material):
    if object.data.materials:
            object.data.materials[0] = material
    else:
            object.data.materials.append(material)

    SetRenderBlock()
    bpy.context.scene.use_nodes = False
    bpy.context.scene.render.film_transparent = True
    bpy.ops.render.render(animation=True)
    bpy.context.scene.use_nodes = True

def PNGTestRender(object, material):
    if object.data.materials:
            object.data.materials[0] = material
    else:
            object.data.materials.append(material)
    SetRenderBlock()
    bpy.ops.render.render(animation=True)

def emptyRender(object, material):
    if object.data.materials:
            object.data.materials[0] = material
    else:
            object.data.materials.append(material)
    SetRenderBlock()
    bpy.context.scene.frame_set(1)
    bpy.ops.render.render(write_still= True)

def marathonEmptyRender(object, material):
    if object.data.materials:
            object.data.materials[0] = material
    else:
            object.data.materials.append(material)
    SetRenderBlock()
    bpy.context.scene.render.film_transparent = True
    bpy.ops.render.render(animation=True)

def validateRenderSettings(self, context):
    SetRenderBlock()
    tree = bpy.context.scene.node_tree
    if self.actionsEnum == "avatar" and self.isSkill is False:
        bpy.context.scene.render.resolution_x = 100
        bpy.context.scene.render.resolution_y = 268
    elif self.actionsEnum == "icon" and self.isSkill is False:
        bpy.context.scene.render.resolution_x = 37
        bpy.context.scene.render.resolution_y = 30
    elif self.isSkill is True:
        if self.skillsEnum == "marathon" or self.skillsEnum == "marathonfail":
            #LoadMarathonBackground()
            bpy.context.scene.use_nodes = True
            bpy.data.scenes['Scene'].node_tree.nodes['Mix'].inputs[0].default_value = 1.0          
        elif self.skillsEnum == "juggle" or self.skillsEnum == "jugglefail":
            #LoadJuggleBackground()
            bpy.context.scene.use_nodes = True
            bpy.data.scenes['Scene'].node_tree.nodes['Mix'].inputs[0].default_value = 0.0
        bpy.context.scene.render.resolution_x = 232
        bpy.context.scene.render.resolution_y = 346
    else:
        bpy.context.scene.render.resolution_x = 464
        bpy.context.scene.render.resolution_y = 346       

def SetupCompositeSystem():
    getfilepath = bpy.context.preferences.addons[__package__.split(".")[0]].preferences.filepath
    bpy.context.scene.use_nodes = True
    tree = bpy.context.scene.node_tree
    if os.path.exists(getfilepath):
        mov = bpy.data.movieclips.load(getfilepath + "/MarathonBG.mp4", check_existing=True)
        img = bpy.data.images.load(getfilepath + "/JuggleBG.jpg", check_existing=True)
        # clear default nodes
        for node in tree.nodes:
            tree.nodes.remove(node)

        # create input image node
        image_node = tree.nodes.new(type='CompositorNodeImage')
        image_node.image = img
        image_node.location = 0,0
        # create movie input node
        movie_node = tree.nodes.new(type='CompositorNodeMovieClip')
        movie_node.clip = mov
        movie_node.location = 400,0
        # View Layer Node
        layer_node = tree.nodes.new(type='CompositorNodeRLayers')
        layer_node.location = 0,400
        # Mix node
        mix_node = tree.nodes.new(type='CompositorNodeMixRGB')
        mix_node.location = 400,200
        # Alpha Over Node
        alpha_node = tree.nodes.new(type='CompositorNodeAlphaOver')
        alpha_node.location = 400,400
        # create output node
        comp_node = tree.nodes.new('CompositorNodeComposite')   
        comp_node.location = 800,0

        # link nodes
        links = tree.links
        links.new(image_node.outputs[0], mix_node.inputs[1])
        links.new(movie_node.outputs[0], mix_node.inputs[2])
        links.new(mix_node.outputs[0], alpha_node.inputs[1])
        links.new(layer_node.outputs[0], alpha_node.inputs[2])
        links.new(alpha_node.outputs[0], comp_node.inputs[0])              

def SetRenderBlock():
    bpy.context.scene.render.use_file_extension = True
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.image_settings.color_mode = "RGBA"
    bpy.context.scene.render.film_transparent = False

#Attempt to create the directories for the output, using the given location in the tool.
def CreateDirectories():
    settings = bpy.context.scene.svr_settings
    path = settings.workDir + "gif"

    colorEnum = PopColors()
    for color in colorEnum:
        path = settings.workDir + "gif\\" + settings.nameEnum + "\\" + color
        try:
            os.makedirs(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s" % path)

        path = settings.workDir + "png\\" + settings.nameEnum + "\\" + color
        try:
            os.makedirs(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s" % path)

def AddActionActionPropsFromCollectionCallback():
    items = []
    settings = bpy.context.scene.svr_settings
    dns = bpy.app.driver_namespace
    pets = dns.get("pets")
    for action in pets[settings.nameEnum]["actions"]:
        items.append(action)
    return items

def AddSkillActionPropsFromCollectionCallback():
    items = []
    settings = bpy.context.scene.svr_settings
    dns = bpy.app.driver_namespace
    pets = dns.get("pets")
    for action in pets[settings.nameEnum]["skills"]:
        items.append(action)
    return items

def AddActionEnviroPropsFromCollectionCallback():
    items = []
    settings = bpy.context.scene.svr_settings
    dns = bpy.app.driver_namespace
    pets = dns.get("pets")
    for action in pets[settings.nameEnum]["actions"]:
        items.append(action)
    return items

def AddSkillEnviroPropsFromCollectionCallback():   
    items = []
    settings = bpy.context.scene.svr_settings
    dns = bpy.app.driver_namespace
    pets = dns.get("pets")
    for action in pets[settings.nameEnum]["skills"]:
        items.append(action)
    return items

def AddNamesCollectionCallback(self, context):
    items = []
    dns = bpy.app.driver_namespace
    pet_names = dns.get("pet_names")
    for name in pet_names:
        items.append((name, name, ""))
    return items

def PopColors():
    items = []
    settings = bpy.context.scene.svr_settings
    dns = bpy.app.driver_namespace
    pets = dns.get("pets")
    for color in pets[settings.nameEnum]["colors"]:
        items.append(color)
    return items

def AddColorsCollectionCallback(self, context):
    items = []
    settings = context.scene.svr_settings
    dns = bpy.app.driver_namespace
    pets = dns.get("pets")
    for color in pets[settings.nameEnum]["colors"]:
        items.append((color, color, ""))
    return items
    
def AddActionsCollectionCallback(self, context):
    items = []
    settings = context.scene.svr_settings
    dns = bpy.app.driver_namespace
    pets = dns.get("pets")
    for action in pets[settings.nameEnum]["actions"]:
        items.append((action, action, ""))
    return items
    
def AddSkillsCollectionCallback(self, context):
    items = []
    settings = context.scene.svr_settings
    dns = bpy.app.driver_namespace
    pets = dns.get("pets")
    for skill in pets[settings.nameEnum]["skills"]:
        items.append((skill, skill, ""))
    return items

def LoadCSVFile(self, context):
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


    

    return {'FINISHED'}

#########################################################################################

def LoadMarathonBackground():
    getfilepath = bpy.context.preferences.addons[__package__.split(".")[0]].preferences.filepath
    if os.path.exists(getfilepath):
        mov = bpy.data.movieclips.load(getfilepath + "/MarathonBG.mp4", check_existing=True)
        #mov.source = 'MOVIE'

        cam = bpy.context.scene.camera

        cam.data.show_background_images = True
        if len(cam.data.background_images) > 0:
            for background_image in cam.data.background_images:
                cam.data.background_images.remove(background_image)
        bg = cam.data.background_images.new()
        bg.clip = mov
        bg.source = "MOVIE_CLIP"
        bpy.context.scene.render.film_transparent = True

def LoadJuggleBackground():
    getfilepath = bpy.context.preferences.addons[__package__.split(".")[0]].preferences.filepath
    if os.path.exists(getfilepath):
        img = bpy.data.images.load(getfilepath + "/JuggleBG.jpg", check_existing=True)
        
        #img.source = 'IMAGE'

        cam = bpy.context.scene.camera

        cam.data.show_background_images = True
        if len(cam.data.background_images) > 0:
            for background_image in cam.data.background_images:
                cam.data.background_images.remove(background_image)
        bg = cam.data.background_images.new()
        bg.image = img
        bg.source = "IMAGE"
        bpy.context.scene.render.film_transparent = True

'''
def SetRenderBlock(avatar):
    if avatar == False:
        
        bpy.context.scene.render.use_file_extension = False
        bpy.context.scene.render.image_settings.file_format = "FFMPEG"
        bpy.context.scene.render.image_settings.color_mode = "RGB"
        bpy.context.scene.render.ffmpeg.format = "MPEG4"
        bpy.context.scene.render.ffmpeg.codec = "MPEG4"
        bpy.context.scene.render.ffmpeg.use_autosplit = False
        bpy.context.scene.render.ffmpeg.constant_rate_factor = "LOSSLESS"
        bpy.context.scene.render.ffmpeg.ffmpeg_preset = "GOOD"
        bpy.context.scene.render.ffmpeg.gopsize = 18
        bpy.context.scene.render.ffmpeg.audio_codec = "NONE"
        bpy.context.scene.render.film_transparent = False
    else:
        bpy.context.scene.render.use_file_extension = True
        bpy.context.scene.render.image_settings.file_format = "PNG"
        bpy.context.scene.render.image_settings.color_mode = "RGBA"
        bpy.context.scene.render.film_transparent = True
'''