from multiAngleOCTSimulation import angularOCTSim2D
import numpy as np
from matplotlib import pyplot as plt
import scipy.io


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
mu_t = depth/2 # mm^-1 # Arbitrary bu realistic - no falloff info given

# CHECK RESOLUTION conversions, check sampling, check mu

oct.setParameters(angles, Ascans, zpixels, depth, lat_FOV, ax_res, lat_res, mu_t)
oct.rotate()
# oct.convolvePSF() 
oct.attenuate() 
result = oct.resample()
# print(result.shape)

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
anglename = str(maxAngle) + '-' + str(interval) + '-' + str(maxAngle)
# data_directory = 'c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Datasets/'   
data_directory = 'c:/Users/William Bundrant/OneDrive/Documents/Aislinn/GitHub/Datasets/'
filename = data_directory + sampleID + '_data.mat'

data = {}
data['Bscans'] = result
data['basename'] = 'phantom'
data['Bscan_dims'] = [zpixels,Ascans]
xzcoords = np.zeros((len(angles),Ascans,2))
xzcoords[:,:,0] = np.tile(np.linspace(0,1,Ascans),(len(angles),1))
data['xzcoords'] = xzcoords
data['tweaks'] = np.zeros((len(angles),2))
data['window'] = np.ones((128,128)).astype(np.int64)
data['L'] = 1
data['radii'] = 0
data['mindists'] = np.zeros((128,128))
# Just taken from a sample arbitrarily
data['center'] = [0.4985, 0.3402] 
data['weights'] = np.ones((zpixels,Ascans)) * 2.364e-7



scipy.io.savemat(filename, data)
