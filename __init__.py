# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 19:38:35 2020

@author: AsteriskAmpersand
"""


content=bytes("","UTF-8")
bl_info = {
    "name": "MHW EVWP Importer",
    "category": "Import-Export",
    "author": "AsteriskAmpersand (Code), Silvris & Statyk(Structure)",
    "location": "File > Import-Export > EVWP/MHW",
    "version": (1,0,0)
}
 
import bpy
from .operators.evwp import Evwp
from .operators.evwpimport import ImportEVWP
from .operators.evwpimport import menu_func_import as evwp_import
from .operators.evwpexport import ExportEVWP
from .operators.evwpexport import menu_func_export as evwp_export
from .operators.evwppanel import EVWPTools
from .operators.evwptools import (resetAlignmentEVWP, alignSheathEVWP, alignSmithEVWP, alignRoomEVWP)

from bpy.props import (StringProperty, IntProperty, FloatProperty, 
                       IntVectorProperty, FloatVectorProperty, BoolVectorProperty)
def propTypeMap(propType):
    if "int" in propType or "byte" in propType:
        if "[" in propType:
            size = int(propType.replace("]","").split("[")[1])
            def vecProp(vecType):
                def PropertyMaker(**kwargs):
                    return vecType(size = size, **kwargs)
                return PropertyMaker
            if "int" in propType:                
                return vecProp(IntVectorProperty)
            if "byte" in propType:
                return vecProp(BoolVectorProperty)
        return IntProperty
    if "float" in propType:
        if "[" in propType:
            return FloatVectorProperty
        return FloatProperty
    if "string" in propType:
        return StringProperty

classes = [ImportEVWP,ExportEVWP,
           EVWPTools,
           resetAlignmentEVWP, alignSheathEVWP, 
           alignSmithEVWP, alignRoomEVWP
           ]

importFunctions = [evwp_import,
                   ] 
exportFunctions = [evwp_export,
                   ] 

def register():
    for cl in classes:
        bpy.utils.register_class(cl)
    for iF in importFunctions:
        bpy.types.INFO_MT_file_import.append(iF)
    for iF in exportFunctions:
        bpy.types.INFO_MT_file_export.append(iF)
    for prop in Evwp.properties:
        blenderProperty = propTypeMap(Evwp.fields[prop])(name=Evwp.properties[prop])
        setattr(bpy.types.Scene,"evwp_%s"%prop,blenderProperty)
    
def unregister():
    for cl in classes:
        bpy.utils.unregister_class(cl)
    for iF in importFunctions:
        bpy.types.INFO_MT_file_import.remove(iF)
    for iF in exportFunctions:
        bpy.types.INFO_MT_file_export.remove(iF)   
    for prop in Evwp.properties:
        blenderProperty = propTypeMap(Evwp.fields[prop])(name=Evwp.properties[prop])
        delattr(bpy.types.Scene,"evwp_%s"%prop,blenderProperty)
        
if __name__ == "__main__":
    try:
        unregister()
    except:
        pass
    register()
