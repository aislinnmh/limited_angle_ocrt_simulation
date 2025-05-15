import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import random

def createGrids(xdim,ydim,umpp_x,umpp_y):
    emptyOCT = np.zeros((ydim, xdim))
    emptyRI = np.ones((ydim, xdim))
    return emptyOCT, emptyRI

def keepWithin2Pi(theta):
    if theta >= 2*np.pi:
        theta = theta - 2*np.pi
    if theta < 0:
        theta = theta + 2*np.pi
    return theta

def createPointScatterers(pointsOCT,n,d,R,xdim,ydim,umpp_x,umpp_y):
    # n = # of points
    # d = diameter in mm
    # pointsOCT, pointsRI = current phantom structure and RI map
    # R = OCT Reflectivity
    # RI = refractive index
    # iRI = refractive index inside tube (background)

    rad = d/2

    mask = np.zeros((ydim,xdim))

    maxDist = ydim/2 * 0.8 # don't want it at edge
    eligibleDists = []
    for i in range(1,n):
        eligibleDists.append(maxDist/i)
    print(eligibleDists)

    cenx = int(xdim/2) + 1
    ceny = int(ydim/2) + 1

    for i in range(n):

        if i == 0:
            # Make one scatterer at center
            x = cenx
            y = ceny
        else: 
            # Place other scatterers randomly but evenly around

            # Split possible locations evenly by angle
            interval = int(180/(n-1))
            eligibleAngles = range(i*interval + 5,(i+1)*interval - 5)
            angle = random.sample(eligibleAngles, 1)

            # Choose a distance from center, evenly spaced intervals
            dist = random.sample(eligibleDists, 1)
            eligibleDists.remove(dist[0])

            x = np.cos(angle[0]/180*np.pi)*dist[0] + cenx
            y = np.sin(angle[0]/180*np.pi)*dist[0] + ceny
            print(angle[0])
            print(dist)

        # Create grid of distances from center in mm
        x = (np.arange(xdim)-x) * umpp_x/1000 # pixels --> centered --> mm
        y = (np.arange(ydim)-y) * umpp_y/1000 # pixels --> centered --> mm
        xgrid, ygrid = np.meshgrid(x,y)
        d = np.sqrt(xgrid**2 + ygrid**2)

        pointMask = (d<rad).astype(int)                  # Mask area of circle
        mask = mask + pointMask

    mask = mask.astype(bool)
    pointsOCT[mask] = R

    return pointsOCT

if __name__ == "__main__":

    # Set parameters
    xdim = 2000 # pixels in X
    ydim = 2000 # pixels in y
    umpp_x = 1 # microns per pixel in x
    umpp_y = 1 # microns per pixel in y
    
    [phantomStructure, phantomRI] = createGrids(xdim,ydim,umpp_x,umpp_y)

    iRI = 1
    phantomRI[:,:] = 1.33

    # Add sub-beam size scatterers to phantom, center and two off-center
    n=3
    d = 0.01 #mm
    R = 1e5
    phantomStructure = createPointScatterers(phantomStructure, 3, 0.01, 1e5, xdim, ydim, umpp_x, umpp_y)

    # Show maps
    plt.figure(figsize=(24,10))
    plt.subplot(1,2,1)
    f = plt.imshow(phantomStructure,norm=LogNorm(vmin=1e2,vmax=1e6),extent = [0,xdim*umpp_x/1000,0,ydim*umpp_y/1000]) 
    plt.title('Reflectivity', fontsize=24)
    cbar = plt.colorbar(f, fraction=0.046, pad=0.04)
    plt.xlabel('mm',fontsize=18)
    plt.ylabel('mm',fontsize=18)
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    cbar.ax.tick_params(labelsize = 16)
    plt.subplot(1,2,2)
    f = plt.imshow(phantomRI,extent = [0,xdim*umpp_x/1000,0,ydim*umpp_y/1000]) 
    plt.title('Refractive Index', fontsize=24)
    cbar = plt.colorbar(f, fraction=0.046, pad=0.04)
    plt.xlabel('mm',fontsize=18)
    plt.ylabel('mm',fontsize=18)
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    cbar.ax.tick_params(labelsize = 16)
    plt.suptitle('Simulated Phantom', fontsize=32, fontweight='bold')
    plt.savefig('Simulated Phantom')
    plt.show()

    # Save phantom OCT/structure and RI map
    np.save('phantomR',phantomStructure)
    np.save('phantomRI',phantomRI)
    np.save('phantom_umpp',(umpp_x,umpp_y))

