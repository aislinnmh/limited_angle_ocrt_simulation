from multiAngleOCTSimulation import angularOCTSim2D
import numpy as np
from matplotlib import pyplot as plt

# This simulation accounts for:
# - angled acquisition
# - nominal PSF of the OCT system
# - axial attenuation
#
# Assumptions made in this simulation:
# - ignoring refraction (minimal, for poin scatterers)
# - ignoring depth of field (keeping PSF constant throughout FOV)
# - orientation = x (up/down) by z (left/right) to match data sampling in OCRT.py
sampleID = 'phantom'
saveFolder = 'Simulated Dataset'
oct = angularOCTSim2D(sampleID, saveFolder)

# Angular Sampling Parameters (degrees)
minAngle = -18
maxAngle = 18
interval = 6
angles = np.arange(minAngle,maxAngle+interval,interval)
print(angles)

# OCT Parameters (matched to the sample data)
# wavelength = 820 # nm
Ascans = 500
zpixels = 2048
depth = 2.22 # mm
lat_FOV = 1.5 # mm
ax_res = 1.2 # um
lat_res  = 8.5 # um
mu_t = 1 # mm^-1 # FIX

# CHECK RESOLUTION conversions, check sampling, check mu

oct.setParameters(angles, Ascans, zpixels, depth, lat_FOV, ax_res, lat_res, mu_t)
oct.rotate()
# result = oct.convolvePSF() 
oct.attenuate()
result = oct.resample()

[umpp_x,umpp_z] = oct.getUMDims()

# Show maps
plt.figure(figsize=(24,10))
plt.subplot(1,2,1)
f = plt.imshow(result[0,:,:], extent = [0,zpixels*umpp_z/1000,0,Ascans*umpp_x/1000]) 
cbar = plt.colorbar(f, fraction=0.046, pad=0.04)
plt.subplot(1,2,2)
f = plt.imshow(result[len(angles)-1,:,:], extent = [0,zpixels*umpp_z/1000,0,Ascans*umpp_x/1000]) 
cbar = plt.colorbar(f, fraction=0.046, pad=0.04)
plt.show()
print('plotted')

# Save
# anglename = str(maxAngle) + '-' + str(interval) + '-' + str(maxAngle)
# data_directory = 'c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Datasets/' + anglename + '/'  
# np.save(data_directory + sampleID + '_data.mat', result)

