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
    ("presetIdOffsetShake","int32"),
    ("motionID","int32"),
    ("weaponDependent","int32"),
    #<name="Bitflags", bgcolor=0xB0FFFF, comment="Settings for various weapon tricks"> 
    ("globalEPV" ,"int32"),#<name="Global EFX", bgcolor=0x00FFFF> 
    ("pendantPos" ,"float[3]"),#<name="Pendant Position", bgcolor=0x3030FF, comment="On weapon, NOT room rack"> 
    ("pendantRot" ,"float[3]"),#<name="Pendant Rotation", bgcolor=0x7070FF, comment="On weapon, NOT room rack"> 
    ("pendantScale" ,"float"),#<name="Pendant Scale", bgcolor=0xB0B0FF, comment="On weapon, NOT room rack"> 
    ("attachPendantToMain" ,"byte"),
    ("useEmissiveFactor" ,"byte"),
    ("useSecondaryEmitColor" ,"byte"),
    ("usePartsSwitchDelay" ,"byte"),
    ("useChainSwitchDelay" ,"byte"),#<bgcolor=0x000000> 
    #First one moves the pendant from the quiver/sheathe to the main weapon
])

def stupidEvwp(evwpArray):
    evwpArray[1],evwpArray[2]=evwpArray[2],evwpArray[1]
    return
    
class Evwp(PyCStruct):
    defaultProperties = {"ibBytes":0x18091001,
                "magic":"EVWP",
                "version":0x0d}
    fields = evwpStruct
    properties = OrderedDict([("presetIdOffsetShake","Offset Shake Type"),("motionID","LMT"),
                  ("weaponDependent","Weapon Utility Value"),("globalEPV","EPV"),
                  ("attachPendantToMain","Pendant on Main"),("useEmissiveFactor","Disable Emissive"),("useSecondaryEmitColor","Disable Secondary Emit Color"),
                  ("usePartsSwitchDelay","Viscon Switch Delay"),("useChainSwitchDelay","Physics Switch Delay"),
                  ])#
    def __init__(self,dataPath = None):
        if dataPath is not None:
            with open(dataPath,"rb") as inf:
                data = FileLike(inf.read())
                super().__init__(data)
                return
        super().__init__()
        return
    def retardationToggle(self):
        for stupid in [self.sheathPos,self.sheathRot]:
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
    fieldSets = {field:{} for field in evwpStruct}
    with open("Bit Flags.json","w") as outf: 
        for evwpf in chunkPath.rglob("*.evwp"):
            evFile = Evwp(evwpf)
            for field in fieldSets:
                datum = getattr(evFile,field)
                datum = tuple(datum) if isIter(datum) else datum
                if datum not in fieldSets[field]:
                    fieldSets[field][datum] = []
                fieldSets[field][datum].append(evwpf)
        outf.write('{')
        for field in fieldSets:
            outf.write('"'+str(field)+'":{\n')
            values = fieldSets[field]
            for value in values:
                outf.write('\t"'+str(value)+'":{\n')
                pathings = values[value]
                for path in pathings:
                    outf.write('\t\t"'+str(path)+",\n")
                outf.write('\t},\n')
            outf.write('},\n')
        outf.write('}\n')
        #print(fieldSets["unknBytes"])
        