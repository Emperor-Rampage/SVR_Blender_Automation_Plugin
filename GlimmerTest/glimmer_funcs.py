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

def emptyRender(object, material):
    if object.data.materials:
            object.data.materials[0] = material
    else:
            object.data.materials.append(material)
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.image_settings.color_mode = "RGB"
    bpy.context.scene.frame_set(1)
    bpy.ops.render.render(write_still= True)
    SetRenderBlock()

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

def CreateDirectories():
    settings = bpy.context.scene.svr_settings
    path = settings.workDir + "gif"

    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)
        
    path = settings.workDir + "mp4"

    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)
    else:
        print ("Successfully created the directory %s" % path)

def AddItemsFromCollectionCallback(self, context):
    items = []
    scene = context.scene
    for item in scene.my_items.values():
        items.append((item.some_str, item.some_str, ""))
    return items

def AddNamesCollectionCallback(self, context):
    items = []
    dns = bpy.app.driver_namespace
    pet_names = dns.get("pet_names")
    for name in pet_names:
        items.append((name, name, ""))
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
