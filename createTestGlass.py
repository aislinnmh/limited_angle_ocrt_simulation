import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import random
import cv2
import skimage


# Set parameters
xdim = 2000 # pixels in X
ydim = 2000 # pixels in y
umpp_x = 1 # microns per pixel in x
umpp_y = 1 # microns per pixel in y   

emptyOCT = np.zeros((ydim, xdim))
emptyRI = np.ones((ydim, xdim))
RI = emptyRI

for i in range(ydim):
    for j in range(xdim):
        if (i > 0.2*j + 500) & (j>1000):
            RI[i,j] = 1.5
        if (i > 0.2*1000+500) & (j<=1000):
            RI[i,j] = 1.5
        if (i > 0.2*j + 1000) & (j>1000):
            RI[i,j] = 1
        if (i > 0.2*1000+1000) & (j<=1000):
            RI[i,j] = 1  

np.save('testglassR',emptyOCT)
np.save('testglassRI',RI)
np.save('testglass_umpp',(umpp_x,umpp_y))

plt.figure()
plt.imshow(RI)
plt.show()