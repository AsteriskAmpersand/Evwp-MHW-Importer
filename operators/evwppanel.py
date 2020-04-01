# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 23:04:20 2019
@author: AsteriskAmpersand
"""
import bpy
from .evwp import Evwp

class EVWPTools(bpy.types.Panel):
    bl_category = "MHW Tools"
    bl_idname = "panel.mhw_evwp"
    bl_label = "EVWP Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    # bl_category = "Tools"
    
    def draw(self, context):
        
        layout = self.layout
        #self.layout.label("CCL Capsule Tools")
        #self.layout.operator("ctc_tools.mesh_from_capsule", icon='MESH_CUBE', text="Mesh from Capsule")
        self.draw_buttons(context, layout)
        self.draw_data(context, layout)
        layout.separator()
        
    def draw_buttons(self,context,layout):
        col = layout.column(align = True)
        col.operator("evwp_tools.align_reset", icon='CONSTRAINT_DATA', 
                     text="Reset Position")
        col.operator("evwp_tools.align_sheath", icon='CONSTRAINT_DATA', 
                     text="Set on Sheath")
        col.operator("evwp_tools.align_smith", icon='CONSTRAINT_DATA', 
                     text="Set on Smith Table")
        col.operator("evwp_tools.align_room", icon='CONSTRAINT_DATA', 
                     text="Set on Beedroom Weapon Rack")        
    
    def draw_data(self,context,layout):
        for prop in Evwp.properties:
            blenderProp = "evwp_%s"%prop
            if hasattr(bpy.types.Scene,blenderProp):
                layout.prop(bpy.context.scene, blenderProp, text = Evwp.properties[prop])