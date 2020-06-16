import bpy
from bpy.types import PropertyGroup, UIList, Panel, Operator
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    StringProperty
) 



class Glimmer_PT_Panel(Panel):
    bl_idname = "Glimmer_PT_Panel"
    bl_label = "Glimmer SVR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Glimmer SVR"
    #bl_category = "Tool"

    def draw(self,context):
        pet = context.active_object
        settings = context.scene.svr_settings
        scene = context.scene

        layout = self.layout

        #layout.row().prop(settings, "isSkill", text = "Render as Skill?")
        layout.row().prop(settings, "petName", text = "Pet Name")
        layout.row().prop(settings, "petColor1", text = "Color 1")
        layout.row().prop(settings, "petColor2", text = "Color 2")
        layout.row().prop(settings, "petColor3", text = "Color 3")
        layout.row().prop(settings, "animationName", text = "Animation Title")
        layout.row().prop(settings, "actionsEnum", text = "Action")
        layout.row().prop(settings, "skillsEnum", text = "Skill")
        row = layout.row()
        row.prop(settings, "skillHandEnum", text = "Hand")
        row.prop(settings, "skillFail", text = "Fail")
        
        layout.row().operator("render.multirender", text="Multi Render", icon='OBJECT_DATAMODE')

        layout.row().template_list("Glimmer_UL_ActionList", "The_List", scene, "my_list", scene, "list_index")
        row = layout.row() 
        row.operator('my_list.new_item', text='NEW') 
        row.operator('my_list.delete_item', text='REMOVE') 
        row.operator('my_list.move_item', text='UP').direction = 'UP'
        row.operator('my_list.move_item', text='DOWN').direction = 'DOWN'

        row = layout.row()
        if scene.list_index >= 0 and scene.my_list: 
            item = scene.my_list[scene.list_index] 
            row = layout.row()
            row.prop(item, "name")
            row.prop(item, "color")

        layout.separator()

        layout.row().prop(settings,"workDir",text="Work Directory")
        layout.row().operator('glimmer.load_csv_file',text="Load CSV File")
        layout.row().prop(settings,"csvFile",text="CSV File Path")

        layout.separator()
        
        layout.row().prop(settings,"scaleValue",text="Scale Amount")
        row = layout.row()
        row.operator('object.scale_object',text="Scale Object")
        row.operator('object.unscale_object',text="Unscale Object")
        

###############################

#class Glimmer_PT_VariationPanel(bpy.types.Panel):
#    bl_label = "Variation Panel"
#    bl_idname = "OBJECT_PT_variation_panel"
#    bl_space_type = "VIEW_3D"
#    bl_region_type = 'UI'

variations = {
    1 : {'name' : 'Default', 'material' : 'Default Mat'},
}


###############################

class ActionListItem(PropertyGroup):
    name: StringProperty( name="Name", description="A name for this item", default="Untitled") 
    random_prop: StringProperty( name="color", description="Color", default="")

class Glimmer_UL_ActionList(UIList):
    """Demo UIList.""" 
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index): 
        # We could write some code to decide which icon to use here... 
        custom_icon = 'OBJECT_DATAMODE' 
        # Make sure your code supports all 3 layout types 
        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            layout.label(item.name, icon = custom_icon) 
        elif self.layout_type in {'GRID'}: 
            layout.alignment = 'CENTER' 
            layout.label("", icon = custom_icon) 


class LIST_OT_NewItem(Operator): 
    """Add a new item to the list.""" 
    bl_idname = "my_list.new_item" 
    bl_label = "Add a new item" 
    def execute(self, context): 
        context.scene.my_list.add() 
        return{'FINISHED'}

class LIST_OT_DeleteItem(Operator): 
    """Delete the selected item from the list.""" 
    bl_idname = "my_list.delete_item" 
    bl_label = "Deletes an item" 

    @classmethod 
    def poll(cls, context): 
        return context.scene.my_list 
        
    def execute(self, context): 
        my_list = context.scene.my_list
        index = context.scene.list_index

        my_list.remove(index) 
        context.scene.list_index = min(max(0, index - 1), len(my_list) - 1) 
    
        return{'FINISHED'}

class LIST_OT_MoveItem(Operator):
    """Move an item in the list."""
    bl_idname = "my_list.move_item"
    bl_label = "Move an item in the list"

    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""), ('DOWN', 'Down', "")))
    
    @classmethod
    def poll(cls, context):
        return context.scene.my_list
    
    def move_index(self):
        """ Move index of an item render queue while clamping it. """
        index = bpy.context.scene.list_index
        list_length = len(bpy.context.scene.my_list) - 1 # (index starts at 0)
        new_index = index + (-1 if self.direction == 'UP' else 1)
        bpy.context.scene.list_index = max(0, min(new_index, list_length))

    def execute(self, context):
        my_list = context.scene.my_list
        index = context.scene.list_index
        neighbor = index + (-1 if self.direction == 'UP' else 1)
        my_list.move(neighbor, index)
        self.move_index()
        return{'FINISHED'}

###############################