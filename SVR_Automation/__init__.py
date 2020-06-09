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
    "category" : "Generic"
}

import bpy


class ObjectMoveX(bpy.types.Operator):
    bl_idname = "my_operator.my_class_name"
    bl_label = "My Class Name"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        scene = context.scene
        for obj in scene.objects:
            obj.location.x +=10
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ObjectMoveX)

def unregister():
    bpy.utils.unregister_class(ObjectMoveX)
