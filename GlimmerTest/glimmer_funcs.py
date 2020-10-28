import bpy
import os


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

    SetRenderBlock(True)
    bpy.ops.render.render(animation=True)

def PNGTestRender(object, material):
    if object.data.materials:
            object.data.materials[0] = material
    else:
            object.data.materials.append(material)
    bpy.context.scene.render.use_file_extension = True
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.image_settings.color_mode = "RGB"
    bpy.ops.render.render(animation=True)
    SetRenderBlock(False)

def emptyRender(object, material):
    if object.data.materials:
            object.data.materials[0] = material
    else:
            object.data.materials.append(material)
    bpy.context.scene.render.use_file_extension = True
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.image_settings.color_mode = "RGB"
    bpy.context.scene.frame_set(1)
    bpy.ops.render.render(write_still= True)
    SetRenderBlock(False)

def marathonEmptyRender(object, material):
    if object.data.materials:
            object.data.materials[0] = material
    else:
            object.data.materials.append(material)
    bpy.context.scene.render.use_file_extension = True
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.image_settings.color_mode = "RGB"
    bpy.context.scene.render.film_transparent = True
    bpy.ops.render.render(animation=True)


def validateRenderSettings(self, context):
    if self.actionsEnum == "avatar" and self.isSkill is False:
        bpy.context.scene.render.resolution_x = 100
        bpy.context.scene.render.resolution_y = 268
        SetRenderBlock(True)
    elif self.actionsEnum == "icon" and self.isSkill is False:
        bpy.context.scene.render.resolution_x = 37
        bpy.context.scene.render.resolution_y = 30
        SetRenderBlock(False)
    elif self.isSkill is True:
        bpy.context.scene.render.resolution_x = 232
        bpy.context.scene.render.resolution_y = 346
        SetRenderBlock(False)
    else:
        bpy.context.scene.render.resolution_x = 464
        bpy.context.scene.render.resolution_y = 346
        SetRenderBlock(False)        


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



def CreateDirectories():
    settings = bpy.context.scene.svr_settings
    path = settings.workDir + "gif"

    #try:
        #os.makedirs(path)
    #except OSError:
        #print ("Creation of the directory %s failed" % path)
    #else:
        #print ("Successfully created the directory %s" % path)
        
    #path = settings.workDir + "mp4"

    #try:
        #os.makedirs(path)
    #except OSError:
        #print ("Creation of the directory %s failed" % path)
    #else:
        #print ("Successfully created the directory %s" % path)

    colorEnum = PopColors()
    for color in colorEnum:
        path = settings.workDir + "mp4\\" + settings.nameEnum + "\\" + color
        try:
            os.makedirs(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s" % path)
        
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

def AddActionPropsFromCollectionCallback():
    items = []
    settings = bpy.context.scene.svr_settings
    dns = bpy.app.driver_namespace
    pets = dns.get("pets")
    for action in pets[settings.nameEnum]["actions"]:
        items.append(action)
    return items

def AddSkillPropsFromCollectionCallback():
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

def AddEnviroPropsFromCollectionCallback():
    items = []
    #settings = bpy.context.scene.svr_settings
    dns = bpy.app.driver_namespace
    enviroProp = dns.get("enviro")
    for prop in enviroProp:
        items.append(prop)
    return items