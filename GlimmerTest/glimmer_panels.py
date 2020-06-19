import bpy
from bpy.types import PropertyGroup, UIList, Panel, Operator
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    StringProperty,
    PointerProperty,

)

from GlimmerTest.glimmer_funcs import validateRenderSettings, SetRenderBlock, AddNew

class Glimmer_PT_Panel(Panel):
    bl_idname = "Glimmer_PT_Panel"
    bl_label = "Glimmer SVR"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Glimmer SVR"
    #bl_category = "Tool"

    def draw(self,context):

        layout = self.layout
        scene = context.scene

        settings = context.scene.svr_settings
        mylist = context.scene.my_list
        variationSettings = context.scene.my_variations


        #print(variationSettings.items())
        box = layout.box()
        box.row().prop(settings,"workDir",text="Work Directory")
        box.row().operator('glimmer.load_names_csv',text="Load CSV File")
        box.row().prop(settings,"csvFile",text="CSV File Path")
        layout.separator()

        box = layout.box()
        box.row().prop(settings, "nameEnum", text= "Pet")
        box.row().prop(settings, "colorsEnum", text= "Color")
        if settings.isSkill is True:
            box.row().prop(settings, "skillsEnum", text = "Skill")
        else:
            box.row().prop(settings, "actionsEnum", text = "Action")


        row = box.row()
        row.prop(settings, "isSkill", text = "Render As Skill?")

        layout.separator()
        layout.row().operator("render.multirender", text="Multi Render", icon='OBJECT_DATAMODE')
        layout.separator()
        layout.row().operator("temp.test", text="Test Enum Gen")

        #Action Prop List Area
        box = layout.box()
        box.row().label(text= "Action Prop List")
        row = box.row()
        if scene.list_index >= 0 and scene.my_list:
            if settings.isSkill is True:
                for item in scene.my_list[settings.skillsEnum].prop_list:
                    row = box.row()
                    row.label=(scene.my_list[settings.skillsEnum].name)
                    row.prop(item, "prop", text="Prop Object:")
            else:
                for item in scene.my_list[settings.actionsEnum].prop_list: 
                    row = box.row()
                    row.label(text= scene.my_list[settings.actionsEnum].name)
                    row.prop(item, "prop", text="Prop Object:")
        #Do Work on Action Prop List
        row = box.row()
        new = row.operator('my_list.new_item', text='NEW')
        if settings.isSkill is True:
            new.string = settings.skillsEnum
        else:
            new.string = settings.actionsEnum

        delete = row.operator('my_list.delete_item', text='REMOVE')
        if settings.isSkill is True:
            delete.string = settings.skillsEnum
        else:
            delete.string = settings.actionsEnum 
        #row.operator('my_list.move_item', text='UP').direction = 'UP'
        #row.operator('my_list.move_item', text='DOWN').direction = 'DOWN'
            
        
        
        layout.separator()

        #Variation Panel Area
        layout.row().label(text= "Variation Panel")
        row = layout.row()
        row.alignment = "EXPAND"
        row.operator('collections.add_variation', text = "Add", icon= 'PLUS')
        row.operator('collections.delete_variation', text =  "Delete", icon= 'REMOVE')
        #Iterator value for checking and adding items.
        iterator = 0
        for item in variationSettings:
            
            box = layout.box()          
            box.row().prop(item, 'colorsEnum')
            box.row().prop(item, 'material')
            box.row().prop(item, 'mesh')                   
            row = box.row() 

            new = row.operator('prop_list.new_item', text='NEW')
            new.index = iterator

            remove = row.operator('prop_list.delete_item', text='REMOVE')
            remove.index = iterator 

            
            if item.list_index >= 0 and item.prop_list:
                for prop in item.prop_list: 
                    box.row().prop(prop, "prop", text="Prop Object:")

            layout.separator()
            iterator = iterator + 1            
        
        #layout.row().prop(settings,"scaleValue",text="Scale Amount")
        #row = layout.row()
        #row.operator('object.scale_object',text="Scale Object")
        #row.operator('object.unscale_object',text="Unscale Object")

        dns = bpy.app.driver_namespace
        dns_pet_names = dns.get("pet_names")
        for name in dns_pet_names:
            layout.row().label(text=name)
        

###############################

def enum_members_from_type(rna_type, prop_str):
    prop = rna_type.bl_rna.properties[prop_str]
    return [e.identifier for e in prop.enum_items]


def enum_members_from_instance(rna_item, prop_str):
    return enum_members_from_type(type(rna_item), prop_str)

class Temp_Action(bpy.types.Operator):
    bl_idname = "temp.test"
    bl_label = "My Class Name"
    bl_description = "Description that shows in blender tooltips"
    bl_options = {"REGISTER"}

    def execute(self, context):

        enum = enum_members_from_instance(bpy.context.scene.svr_settings, "skillsEnum")
        
        for name in enum:
            new = bpy.context.scene.my_list.add()
            new.name = name
            new.prop_list.add()
            print(name)

        enum = enum_members_from_instance(bpy.context.scene.svr_settings, "actionsEnum")

        for name in enum:
            new = bpy.context.scene.my_list.add()
            new.name = name
            new.prop_list.add()
            print(name)

        return {"FINISHED"}


class ActionListItem(PropertyGroup):
    bl_idname = "collection.propitem"
    bl_label = "Pointer property group, used to hold prop info."
    name : StringProperty(name="name")
    prop : PointerProperty(name="prop", type= bpy.types.Object)   

class Glimmer_UL_ActionList(UIList):
    """Demo UIList.""" 
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index): 
        # We could write some code to decide which icon to use here... 
        custom_icon = 'OBJECT_DATAMODE' 
        # Make sure your code supports all 3 layout types 
        if self.layout_type in {'DEFAULT', 'COMPACT'}: 
            layout.label(text = item.name, icon = custom_icon) 
        elif self.layout_type in {'GRID'}: 
            layout.alignment = 'CENTER' 
            layout.label("", icon = custom_icon) 

class LIST_OT_NewItemProp(Operator): 
    """Add a new item to the list.""" 
    bl_idname = "prop_list.new_item" 
    bl_label = "Add a new item"

    index : bpy.props.IntProperty(name='index')

    def execute(self, context): 
        context.scene.my_variations[self.index].prop_list.add() 
        return{'FINISHED'}

class LIST_OT_DeleteItemProp(Operator): 
    """Delete the selected item from the list.""" 
    bl_idname = "prop_list.delete_item" 
    bl_label = "Deletes an item" 

    index : bpy.props.IntProperty(name='index')
        
    def execute(self, context): 
        my_list = context.scene.my_variations[self.index].prop_list
        index = context.scene.my_variations[self.index].list_index

        my_list.remove(0) 
        #context.scene.my_variations[self.index].list_index = min(max(0, index - 1), len(my_list) - 1) 
    
        return{'FINISHED'}

class LIST_OT_NewItem(Operator): 
    """Add a new item to the list.""" 
    bl_idname = "my_list.new_item" 
    bl_label = "Add a new item"

    string : bpy.props.StringProperty()

    def execute(self, context): 
        context.scene.my_list[self.string].prop_list.add() 
        return{'FINISHED'}

class LIST_OT_DeleteItem(Operator): 
    """Delete the selected item from the list.""" 
    bl_idname = "my_list.delete_item" 
    bl_label = "Deletes an item" 

    string : bpy.props.StringProperty()
 
        
    def execute(self, context): 
        my_list = context.scene.my_list[self.string].prop_list

        my_list.remove(0) 
        #context.scene.list_index = min(max(0, index - 1), len(my_list) - 1) 
    
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