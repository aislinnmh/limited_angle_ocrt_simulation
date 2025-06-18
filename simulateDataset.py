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
minAngle = -90
maxAngle = 90
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
mu_t = depth/1.5 # mm^-1 # Arbitrary but realistic - no falloff info given

oct.setParameters(angles, Ascans, zpixels, depth, lat_FOV, ax_res, lat_res, mu_t)
oct.rotate()
oct.convolvePSF() 
oct.attenuate() 
result = oct.resample()

[umpp_x,umpp_z] = oct.getUMDims()

# Show maps
plt.figure(figsize=(24,10))
plt.subplot(1,2,1)
# f = plt.imshow(oct.R, extent = [0,zpixels*umpp_z/1000,0,Ascans*umpp_x/1000]) # original phantom, for testing
f = plt.imshow(result[0,:,:], extent = [0,zpixels*umpp_z/1000,0,Ascans*umpp_x/1000]) 
cbar = plt.colorbar(f, fraction=0.046, pad=0.04)
plt.subplot(1,2,2)
f = plt.imshow(result[len(angles)-1,:,:], extent = [0,zpixels*umpp_z/1000,0,Ascans*umpp_x/1000]) 
cbar = plt.colorbar(f, fraction=0.046, pad=0.04)
plt.show()
print('plotted')

# Save
anglename = str(maxAngle) + '-' + str(interval) + '-' + str(maxAngle) + '/'
data_directory = 'c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Datasets/'   
# data_directory = 'c:/Users/William Bundrant/OneDrive/Documents/Aislinn/GitHub/Datasets/'
filename = data_directory + anglename + sampleID + '_data.mat'

data = {}
result = np.transpose(result,(0,2,1))
# LOG, scale to similar rnage as sample
result = result/100
result[result<=0.5] = 0.5
result = np.log(result)
result = result/2

data['Bscans'] = result
data['basename'] = 'phantom'
data['Bscan_dims'] = [zpixels,Ascans]
xzcoords = np.zeros((len(angles),Ascans,2))
xzcoords[:,:,0] = np.tile(np.linspace(0,1,Ascans),(len(angles),1))
data['xzcoords'] = xzcoords
data['tweaks'] = np.zeros((len(angles),2))
data['window'] = np.ones((128,128)).astype(np.int64)
data['L'] = 0.664
data['center'] = [0.5,0.5] 
data['radii'] = 0 # no tube

# Just taken from a sample in order to work
sample_data = scipy.io.loadmat('C:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Datasets/90-6-90/mouse_vas_deferens1_data.mat')
data['mindists'] = sample_data['mindists'] # kernel
data['weights'] = np.ones((1,zpixels,Ascans)) * 2.918e-7

scipy.io.savemat(filename, data)
