# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 12:06:04 2020

@author: aguevara
"""
from bpy_extras.io_utils import ImportHelper
from bpy.types import Operator
from bpy.props import (StringProperty, IntProperty, FloatProperty, 
                       IntVectorProperty, FloatVectorProperty, BoolVectorProperty)

from .evwp import Evwp
from mathutils import Matrix, Euler
from math import degrees, radians
import bpy

def transrotscale(trans,rot,scale):
    angle = list(map(radians,rot))
    print(angle)
    return Matrix.Translation(trans)*Euler(angle, "XYZ").to_matrix().to_4x4()*Matrix.Scale(scale,4)

class ImportEVWP(Operator, ImportHelper):
    bl_idname = "custom_import.import_mhw_evwp"
    bl_label = "Load MHW EVWP file (.evwp)"
    bl_options = {'REGISTER', 'PRESET', 'UNDO'}
        
    # ImportHelper mixin class uses this
    filename_ext = ".evwp"
    filter_glob = StringProperty(default="*.evwp", options={'HIDDEN'}, maxlen=255)
    
    @staticmethod
    def showMessageBox(message = "", title = "Message Box", icon = 'INFO'):
    
        def draw(self, context):
            self.layout.label(message)
    
        bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

    def displayErrors(self, errors):
        if errors:
            for _ in range(20):print()
            print("EVWP Import Errors:")
            print("#"*75)
            print("\n".join(errors))
            print("#"*75)
            message= "Import Process aborted due to error, check the reason in Window > Toggle_System_Console"
            self.showMessageBox(message, title = "Warnings and Error Log")
    
    def execute(self,context):
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except:
            pass
        self.ErrorMessages = []
        bpy.ops.object.select_all(action='DESELECT')
        try: evwp = Evwp(self.properties.filepath)
        except:
            self.ErrorMessages.append("Corrupted EVWP File couldn't be read.")
            self.missingFunctionBehaviour = "Abort"
            self.displayErrors(self.ErrorMessages)
            return {'FINISHED'}
        #self.prepareScene()
        self.createPendant(evwp.pendantPos,evwp.pendantRot,evwp.pendantScale)
        self.createSheathPosition(evwp.sheathPos,evwp.sheathRot,evwp.sheathScale)
        self.createUnknownPosition(evwp.smithPos,evwp.smithRot,evwp.smithScale)
        self.createRoomPosition(evwp.roomPos,evwp.roomRot,evwp.roomScale)
        self.writeProperties(evwp)
        self.displayErrors(self.ErrorMessages)
        return {'FINISHED'}
            
    @staticmethod   
    def createEmpty(name = "Empty"):
        o = bpy.data.objects.new( name, None )
        bpy.context.scene.objects.link( o )
        o.empty_draw_size = 1
        o.empty_draw_type = "PLAIN_AXES"
        o.show_x_ray = True
        o.show_bounds = False
        return o
    
    @staticmethod
    def createNode(name,pos,rot,scale):
        rep = ImportEVWP.createEmpty(name)
        rep["Type"] = "EVWP_%s"%name
        rep.rotation_euler = list(map(radians,rot))
        rep.scale = [scale,scale,scale]
        rep.location = pos
        return rep
    
    @staticmethod 
    def createPendant(pos,rot,scale):
        pendant = ImportEVWP.createNode("Pendant",pos,rot,scale)
        pendant.constraints.new("CHILD_OF").name = "EVWP Position"
        return pendant
    
    @staticmethod 
    def createUnknownPosition(pos,rot,scale):
        return ImportEVWP.createNode("Smith",pos,rot,scale)
       
    @staticmethod 
    def createRoomPosition(pos,rot,scale):
        return ImportEVWP.createNode("Room",pos,rot,scale)
        
    @staticmethod 
    def createSheathPosition(pos,rot,scale):
        return ImportEVWP.createNode("Sheath",pos,rot,1+scale)
    
    @staticmethod
    def writeProperties(evwp):
        for prop in evwp.properties:
            if "byte" in evwp.fields[prop]:
                setattr(bpy.context.scene,"evwp_%s"%prop,list(map(bool, getattr(evwp,prop))))
            else:
                setattr(bpy.context.scene,"evwp_%s"%prop,getattr(evwp,prop))
            #bpy.types.Scene
            #bpy.context.scene
            #bpy.context.scene["evwp_%s"%prop] = propTypeMap(evwp.fields[prop])(name=evwp.properties[prop],default = getattr(evwp,prop))
        #bpy.context.scene["evwp_bitflags"] = bitflags
        #bpy.context.scene["evwp_unknArray"] = unkn2
        return
    
def menu_func_import(self, context):
    self.layout.operator(ImportEVWP.bl_idname, text="MHW EVWP (.evwp)")