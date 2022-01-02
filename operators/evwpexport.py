# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 12:06:04 2020

@author: aguevara
"""
from bpy_extras.io_utils import ExportHelper
from bpy.types import Operator
from bpy.props import StringProperty

from .evwp import Evwp
from .evwptools import getStarTypeNode
from mathutils import Matrix, Euler
from math import degrees, radians
import bpy

def transrotscale(trans,rot,scale):
    angle = list(map(radians,rot))
    print(angle)
    return Matrix.Translation(trans)*Euler(angle, "XYZ").to_matrix().to_4x4()*Matrix.Scale(scale,4)

def isIter(var):
    try:
        iter(var)
        return True
    except:
        return False

class ExportEVWP(Operator, ExportHelper):
    bl_idname = "custom_export.export_mhw_evwp"
    bl_label = "Save MHW EVWP file (.evwp)"
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
            message= "Export Process aborted due to error, check the reason in Window > Toggle_System_Console"
            self.showMessageBox(message, title = "Warnings and Error Log")
    
    def execute(self,context):
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except:
            pass
        self.ErrorMessages = []
        evwpData = {}
        self.loadGeometryData(evwpData)
        self.loadMetadata(evwpData)       
        if self.ErrorMessages:
            self.displayErrors(self.ErrorMessages)
            return{'CANCELLED'}
        self.writeData(evwpData)
        return {'FINISHED'}
    
    def loadGeometryData(self,evwpData):
        for starType in ["Sheath","Room","Pendant","Smith"]:
            try:
                nodeProps = self.decomposeNode(getStarTypeNode("EVWP_%s"%starType),starType)
                if starType == "Sheath":
                    nodeProps["sheathScale"] -= 1
                for prop in nodeProps:
                    evwpData[prop] = nodeProps[prop]
            except Exception as e:
                self.ErrorMessages.append("Failed to Find %s. %s"%(starType,e))
    def loadMetadata(self,evwpData):
        for prop in Evwp.properties:
            try:
                data = getattr(bpy.context.scene,"evwp_%s"%prop)
                evwpData[prop] = [i for i in data] if isIter(data) else data
            except:
                self.ErrorMessages.append("Missing Property %s"%prop)
    def writeData(self,evwpData):
        evwp = Evwp()
        evwp.construct(evwpData)
        with open(self.properties.filepath,"wb") as outf:
            outf.write(evwp.serialize())
    @staticmethod
    def decomposeNode(node,typeStr):
        pos,rot,scale= map(lambda x: x%(typeStr.lower()), ["%sPos","%sRot","%sScale"])
        return {pos:node.location,rot:list(map(degrees,node.rotation_euler)),scale:node.scale[0]}

def menu_func_export(self, context):
    self.layout.operator(ExportEVWP.bl_idname, text="MHW EVWP (.evwp)")