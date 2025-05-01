from multiAngleOCTSimulation import angularOCTSim2D
import numpy as np
from matplotlib import pyplot as plt


# OCT Parameters
wavelength = 1050
NA = 0.1
Ascans = 1200
zpixels = 2048,
depth = 3
lateralFOV = 1.7

oct = angularOCTSim2D(sampleID = 'testglass', saveFolder = 'Simulated Dataset', wavelength = wavelength, NA = NA, Ascans = Ascans, zpixels = zpixels, depth = depth, lateralFOV = lateralFOV)

# Angular Sampling Parameters (degrees)
# minAngle = -180
# maxAngle = 179
minAngle = 0
maxAngle = 2
interval = 1 
angles = np.arange(minAngle,maxAngle+interval,interval)

oct.setParameters(angles = angles)

paths = oct.propagateRays()

paths = paths.numpy()
plt.figure()
for i in np.arange(0,1600,50):
    plt.plot(paths[:,i,1],paths[:,i,0])
plt.imshow(oct.RI)
plt.show()

# print(paths[950,:,1])

# rotate
# Refract ray trajectories  - makle into a big stack
# warp by rotated refraction - code within backproijection to trilinear interp from nearest coord
# Signal formation - inc beam size gaussian
# IFT
# Save

