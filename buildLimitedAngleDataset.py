import scipy.io
import numpy as np
import os

data_directory = 'c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Datasets/180-6-180/'
# sample_id = 'mouse_vas_deferens1'  
sample_id = 'point_phantom'
filename = data_directory + sample_id + '_data.mat'
data = scipy.io.loadmat(filename)

# FOR SAMPLES
# center_angle_i = 15 # Arbitrarily define one angle as central within the original range (Here, 90 degrees from that at 0)
# max_angles = 90, 60, 30, 18, 90, 90
# intervals = 6, 6, 6, 6, 18, 30

# FOR PHANTOM
center_angle_i = 90
max_angles = 90, 60, 30, 18, 90, 90
intervals = 6, 6, 6, 6, 18, 30

subsampledData = data.copy()
Bscans = data['Bscans']
[n_bscans,pixels,Ascans] = Bscans.shape

for i in range(len(max_angles)):
    max_angle = max_angles[i]
    interval = intervals[i]
    n_onesided = int(max_angle/interval)
    n_bscans = n_onesided*2 + 1

    subsampledBscans = np.zeros((n_bscans,pixels,Ascans))
    # Grab B-scans - Dimensions are angle x pixels x Ascans
    for j in range(n_bscans):
        i_interval = int(interval/6)
        angle_i = (center_angle_i - n_onesided*i_interval) + j*i_interval
        subsampledBscans[j,:,:] = Bscans[angle_i,:,:]

    subsampledData['Bscans'] = subsampledBscans

    anglename = str(max_angle) + '-' + str(interval) + '-' + str(max_angle)
    data_directory = 'c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Datasets/' + anglename + '/'
    os.mkdir(data_directory)
    filename = data_directory + sample_id + '_data.mat'
    scipy.io.savemat(filename, subsampledData)


# add appropriate inputs to ocrt code, any changes needed