# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:41:00 2020

@author: aguevara
"""
import bpy

def checkIsStarType(candidateStarType):
    return candidateStarType.type == "EMPTY" and "Type" in candidateStarType
def checkStarType(typing):
    return lambda x: checkIsStarType(x) and x["Type"]==typing

def getStarTypeNode(startype):
    candidates = []
    for obj in bpy.context.scene.objects:
        if checkStarType(startype)(obj):
                candidates.append(obj)
    if len(candidates)<1:
        raise ValueError("No Candidate Empty Found for %s"%startype)
    if len(candidates)>1:
        raise ValueError("Too Many Candidates Empty Found for %s:\n\t"%startype+'\n\t'.join(
                map(lambda x: x.name,candidates)))
    return candidates[0]

class alignOp(bpy.types.Operator):
    def execute(self, context):
        target = self.target
        for obj in bpy.context.scene.objects: 
            if obj.type == "MESH" or checkStarType("EVWP_Pendant")(obj):
                constraint = self.addEVWPConstraint(obj)
                constraint.target = target                
        return {"FINISHED"}
    @staticmethod
    def addEVWPConstraint(obj):
        cons = obj.constraints
        if "EVWP Position" not in cons:
            con = cons.new("CHILD_OF")
            con.name = "EVWP Position"
        else:
            con = cons["EVWP Position"]
        return con

class starAlignOp(alignOp):
    def execute(self,context):
        self.target = getStarTypeNode(self.starType)
        return super().execute(context)
        
    @classmethod
    def poll(cls, context):
        check = checkStarType(cls.starType)
        return any((check(obj) for obj in bpy.context.scene.objects))

class resetAlignmentEVWP(alignOp):
    bl_idname = 'evwp_tools.align_reset'
    bl_label = "Reset Weapon Alignment"
    bl_description = 'Reset Weapon Alignment'
    bl_options = {"REGISTER", "UNDO"}    
    target = None

class alignSheathEVWP(starAlignOp):
    bl_idname = 'evwp_tools.align_sheath'
    bl_label = "Align to Sheathed Position"
    bl_description = "Align to Sheathed Position"
    bl_options = {"REGISTER", "UNDO"}    
    starType = "EVWP_Sheath"

class alignSmithEVWP(starAlignOp):
    bl_idname = 'evwp_tools.align_smith'
    bl_label = "Align to Smith Table Position"
    bl_description = "Align to Smith Table Position"
    bl_options = {"REGISTER", "UNDO"}    
    starType = "EVWP_Smith"

class alignRoomEVWP(starAlignOp):
    bl_idname = 'evwp_tools.align_room'
    bl_label = "Align to Bedroom Rack Position"
    bl_description = "Align to Bedroom Rack Position"
    bl_options = {"REGISTER", "UNDO"}    
    starType = "EVWP_Room"