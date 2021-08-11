import bpy
import neurokit2 as nk
import pandas as pd
import matplotlib.pyplot as plt
import math
import mathutils

emg = nk.emg_simulate(duration=10, sampling_rate=1000, burst_number=3)
cleaned = nk.emg_clean(emg, sampling_rate=1000)

amplitude = nk.emg_amplitude(cleaned)
fig = pd.DataFrame({"EMG": emg, "Amplitude": amplitude}).plot(subplots=True)

th = 0.15
state = False

obj = bpy.data.objects["Armature"]
arm = obj.data.bones["Bone"]
bpy.ops.object.mode_set(mode='POSE')
bpy.ops.anim.keyframe_clear_button(all=True)

bone = obj.pose.bones["Bone"]
bone.rotation_mode = 'XYZ'

axis = 'Z'

# initial position
f = 1
angle = 10
bone.rotation_euler.rotate_axis(axis, math.radians(angle))
bpy.ops.object.mode_set(mode='OBJECT')

bone.keyframe_insert(data_path='rotation_euler', frame = f)
f += 10

c = 0
o = 0

debug_closes = 0

for i, x in enumerate(amplitude[:-1]):
    if state == True and x < th:
        state = False   
        print(i,"|| Hand is opening: ",x)    
        
        f += o/100
        o = 0
        
        angle = 75
        bone.rotation_euler.rotate_axis(axis, math.radians(angle))
        bpy.ops.object.mode_set(mode='OBJECT')

        bone.keyframe_insert(data_path='rotation_euler', frame = f) 
        f += 5
    elif state == False and x > th:
        state = True
        print(i,"|| Hand is closing: ",x)
        
        f += c/100
        c = 0
        
        angle = -75
        bone.rotation_euler.rotate_axis(axis, math.radians(angle))
        bpy.ops.object.mode_set(mode='OBJECT')

        bone.keyframe_insert(data_path='rotation_euler', frame = f)
        f += 5
        
        debug_closes += 1
    elif state == True:
        print(i,"|| Hand is closed: ",x)
        c += 1
    elif state == False:
        print(i,"|| Hand is open: ",x)
        o += 1 
    
print("The number of times the hand has closed is: ",debug_closes)
fig
plt.show()
