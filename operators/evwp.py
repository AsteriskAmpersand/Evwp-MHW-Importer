# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 11:39:55 2020

@author: aguevara
"""

from pathlib import Path
from collections import OrderedDict

try:
    from ..common.Cstruct import PyCStruct
    from ..common.FileLike import FileLike
except:
    import sys
    sys.path.append(r"C:\Users\AsteriskAmpersand\AppData\Roaming\Blender Foundation\Blender\2.79\scripts\addons\Evwp-MHW-Importer\common")
    from Cstruct import PyCStruct
    from FileLike import FileLike

evwpStruct = OrderedDict([
    ("ibBytes" ,"uint32"),#<bgcolor=0x000000,format=hex> 
    ("magic" ,"char[4]"),#<bgcolor=0x000000> 
    ("version" ,"uint32"),#<comment="All files I've seen has it as 13", bgcolor=0x000000> 
    ("roomPos" ,"float[3]"),#<name="Room Rack Weapon Position", bgcolor=0xFF3030, comment="Bedroom rack display"> 
    ("roomRot" ,"float[3]"),#<name="Room Rack Weapon Rotation", bgcolor=0xFF7070, comment="Bedroom rack display"> 
    ("roomScale" ,"float"),#<name="Room Rack Weapon Scale", bgcolor=0xFFB0B0, comment="Bedroom rack display"> 
    ("smithPos" ,"float[3]"),#<bgcolor=0x000000> 
    ("smithRot" ,"float[3]"),
    ("smithScale" ,"float"),
    ("sheathPos" ,"float[3]"),#<name="Sheathed Weapon Position", bgcolor=0x30FF30> 
    ("sheathRot" ,"float[3]"),#<name="Sheathed Weapon Rotation", bgcolor=0x70FF70> 
    ("sheathScale", "float"),
    ("witcherUnkn","int32"),
    ("secondaryBoneBehaviour","int32"),
    ("weebUnkn","int32"),
    #<name="Bitflags", bgcolor=0xB0FFFF, comment="Settings for various weapon tricks"> 
    ("globalEFX" ,"int32"),#<name="Global EFX", bgcolor=0x00FFFF> 
    ("pendantPos" ,"float[3]"),#<name="Pendant Position", bgcolor=0x3030FF, comment="On weapon, NOT room rack"> 
    ("pendantRot" ,"float[3]"),#<name="Pendant Rotation", bgcolor=0x7070FF, comment="On weapon, NOT room rack"> 
    ("pendantScale" ,"float"),#<name="Pendant Scale", bgcolor=0xB0B0FF, comment="On weapon, NOT room rack"> 
    ("unknBytes" ,"byte[5]"),#<bgcolor=0x000000> 
])

def stupidEvwp(evwpArray):
    evwpArray[1],evwpArray[2]=evwpArray[2],evwpArray[1]
    return
    
class Evwp(PyCStruct):
    defaultProperties = {"ibBytes":0x18091001,
                "magic":"EVWP",
                "version":0x0d}
    fields = evwpStruct
    properties = OrderedDict([("witcherUnkn","Witcher Unk"),("secondaryBoneBehaviour","Alt Bone Enum"),
                  ("weebUnkn","Weeb Unk"),("globalEFX","EPV"),
                  ("unknBytes","Flags")])#
    def __init__(self,dataPath = None):
        if dataPath is not None:
            with open(dataPath,"rb") as inf:
                data = FileLike(inf.read())
                super().__init__(data)
                return
        super().__init__()
        return
    def retardationToggle(self):
        for stupid in [self.smithRot,self.smithPos,self.roomPos,self.roomRot,
                      self.sheathPos,self.sheathRot]:
            stupidEvwp(stupid)
    def marshall(self,data):
        super().marshall(data)
        self.retardationToggle()
        return self
    def serialize(self):
        self.retardationToggle()
        data = super().serialize()
        self.retardationToggle()
        return data
        
    
if __name__ in "__main__":
    from pathlib import Path
    def isIter(data):
        try:
            iter(data)
            return True
        except:
            return False
    chunkPath = Path(r"E:\MHW\chunkG0")
    fieldSets = {field:set() for field in evwpStruct}
    with open("Bit Flags.txt","w") as outf: 
        for evwpf in chunkPath.rglob("*.evwp"):
            evFile = Evwp(evwpf)
            for field in fieldSets:
                datum = getattr(evFile,field)
                fieldSets[field].add(tuple(datum) if isIter(datum) else datum)
            if evFile.unkn2[4] != 0:
                print("%s - %s"%(evwpf.stem,list(evFile.unkn2)))
    
        