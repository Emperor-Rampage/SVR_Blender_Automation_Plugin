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

def gatherData(string):
    DefaultMat = bpy.data.materials.get(string)
    if DefaultMat is None:
        DefaultMat = bpy.data.materials.new(name=string)
    return DefaultMat
  

class MultiRender(bpy.types.Operator):
    bl_idname = "render.multirender"
    bl_label = "Multi Render"
    bl_description = "RenderThree Times!"
    bl_options = {"REGISTER"}  

    @classmethod
    def poll(cls, context):
        return True 
 
    def execute(self, context):
        scn = bpy.context.scene
        pet = bpy.context.active_object
        DefaultMat = gatherData("DefaultMat")
        MaterialVar2 = gatherData("MaterialVar2")
        MaterialVar3 = gatherData("MaterialVar3")
        scn.render.filepath = "C:\work\work1"
        if pet.data.materials:
            pet.data.materials[0] = DefaultMat
        else:
            pet.data.materials.append(DefaultMat)
        bpy.ops.render.render(animation=True)

        scn.render.filepath = "C:\work\work2"

        if pet.data.materials:
            pet.data.materials[0] = MaterialVar2
        else:
            pet.data.materials.append(MaterialVar2)
        bpy.ops.render.render(animation=True)

        scn.render.filepath = "C:\work\work3"

        if pet.data.materials:
            pet.data.materials[0] = MaterialVar3
        else:
            pet.data.materials.append(MaterialVar3)
        bpy.ops.render.render(animation=True)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(MultiRender)

def unregister():
    bpy.utils.unregister_class(MultiRender)

if __name__ == "__main__":
    register()