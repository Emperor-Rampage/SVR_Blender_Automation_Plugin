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

class ObjectMoveX(bpy.types.Operator):
    bl_idname = "render.multirender"
    bl_label = "Multi Render"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}

    pet = bpy.context.active_object
    DefaultMat = bpy.data.materials.get("DefaultMat")
    if DefaultMat is None:
        DefaultMat = bpy.data.materials.new(name="DefaultMat")

    MaterialVar2 = bpy.data.materials.get("MaterialVar2")
    if MaterialVar2 is None:
        MaterialVar2 = bpy.data.materials.new(name="MaterialVar2")

    MaterialVar3 = bpy.data.materials.get("MaterialVar3")
    if MaterialVar3 is None:
        MaterialVar3 = bpy.data.materials.new(name="MaterialVar3")

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        if pet.data.materials:
            pet.data.materials[0] = DefaultMat
        else:
            pet.data.materials.append(DefaultMat)
        bpy.ops.render.render()

        if pet.data.materials:
            pet.data.materials[0] = MaterialVar2
        else:
            pet.data.materials.append(MaterialVar2)
        bpy.ops.render.render()

        if pet.data.materials:
            pet.data.materials[0] = MaterialVar3
        else:
            pet.data.materials.append(MaterialVar3)
        bpy.ops.render.render()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ObjectMoveX)

def unregister():
    bpy.utils.unregister_class(ObjectMoveX)

if __name__ == "__main__":
    register()