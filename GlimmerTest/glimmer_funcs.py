import bpy

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
        context.scene.render.resolution_x = 232
        context.scene.render.resolution_y = 346
    else:
        context.scene.render.resolution_x = 464
        context.scene.render.resolution_y = 346        
    SetRenderBlock(context)

def SetRenderBlock(context):
    context.scene.render.use_file_extension = False
    context.scene.render.image_settings.file_format = "FFMPEG"
    context.scene.render.image_settings.color_mode = "RGB"
    context.scene.render.ffmpeg.format = "MPEG4"
    context.scene.render.ffmpeg.codec = "MPEG4"
    context.scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
    context.scene.render.ffmpeg.ffmpeg_preset = "GOOD"
    context.scene.render.ffmpeg.gopsize = 18
    context.scene.render.ffmpeg.audio_codec = "NONE"
