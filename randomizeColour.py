import bpy
import random

colours = ["glassR","glassG","glassB"]

mats = bpy.data.materials


for obj in bpy.data.collections['generatedPegs'].objects:
    obj.material_slots[0].material = mats[colours[random.randint(0, len(colours)-1)]]