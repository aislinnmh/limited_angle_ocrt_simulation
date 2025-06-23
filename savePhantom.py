load_directory = 'C:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/data/'
filename = load_directory + 'phantomR.npy'

import scipy.io
import numpy as np

phantom = np.load(filename)

data = {}
data['phantom'] = phantom

scipy.io.savemat(load_directory + 'phantom.mat',data)