import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm
import random

def createGrids(xdim,zdim,umpp_x,umpp_z):
    emptyOCT = np.zeros((xdim, zdim))
    emptyRI = np.ones((xdim, zdim))
    return emptyOCT, emptyRI

def keepWithin2Pi(theta):
    if theta >= 2*np.pi:
        theta = theta - 2*np.pi
    if theta < 0:
        theta = theta + 2*np.pi
    return theta

def createPointScatterers(pointsOCT,n,d,R,xdim,zdim,umpp_x,umpp_z):
    # n = # of points
    # d = diameter in mm
    # pointsOCT = current phantom structure
    # R = OCT Reflectivity

    rad = d/2

    mask = np.zeros((xdim,zdim))

    if n <= 10:

        maxDist = xdim/2 * 0.8 # don't want it at edge
        eligibleDists = []
        for i in range(1,n):
            eligibleDists.append(maxDist/i)
        print(eligibleDists)

        cenx = int(xdim/2) + 1
        cenz = int(zdim/2) + 1

        for i in range(n):

            if i == 0:
                # Make one scatterer at center
                x = cenx
                z = cenz
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
                z = np.sin(angle[0]/180*np.pi)*dist[0] + cenz
                print(angle[0])
                print(dist)

            # Create grid of distances from center in mm
            x = (np.arange(xdim)-x) * umpp_x/1000 # pixels --> centered --> mm
            z = (np.arange(zdim)-z) * umpp_z/1000 # pixels --> centered --> mm
            xgrid, zgrid = np.meshgrid(z,x)
            d = np.sqrt(xgrid**2 + zgrid**2)

            pointMask = (d<rad).astype(int)                  # Mask area of circle
            mask = mask + pointMask

        mask = mask.astype(bool)
        pointsOCT[mask] = R

    else:

        eligibleMask = np.ones((xdim,zdim))


        cenx = int(xdim/2) + 1
        cenz = int(zdim/2) + 1

        # Only place beads within "tube"
        for i in range(xdim):
            for j in range(zdim):
                z = j - cenz
                x = i - cenx

                d = np.sqrt(x**2 + z**2)
                if d > (0.8*xdim/2):
                    eligibleMask[i,j] = 0

        for i in range(n):

            if i == 0:
                # Make one scatterer at center
                x = cenx
                z = cenz
            else: 
                # Place other scatterers randomly everywhere, but not too close to each other

                # Sample a random location
                eligibleXZ = np.argwhere(eligibleMask)
                eligibleI = range(len(eligibleXZ))
                I = random.sample(eligibleI, 1)
                XZ = eligibleXZ[I,:]

                x = XZ[0,0]
                z = XZ[0,1]

            # Create grid of distances from center in mm
            x = (np.arange(xdim)-x) * umpp_x/1000 # pixels --> centered --> mm
            z = (np.arange(zdim)-z) * umpp_z/1000 # pixels --> centered --> mm
            xgrid, zgrid = np.meshgrid(z,x)
            d = np.sqrt(xgrid**2 + zgrid**2)

            pointMask = (d<rad).astype(int)                  # Mask area of circle
            mask = mask + pointMask

            # Remove nearby pixels from potential locations
            nearbyMask = (d<(4*rad)).astype(int)
            eligibleMask = eligibleMask - nearbyMask

        mask = mask.astype(bool)
        pointsOCT[mask] = R

    return pointsOCT

if __name__ == "__main__":

    # Set parameters
    xdim = 6000 # pixels in X, 1.5 mm total 
    zdim = 8880 # pixels in z, 2.22 mm total
    umpp_x = 0.25 # microns per pixel in x
    umpp_z = 0.25 # microns per pixel in z
    
    [phantomStructure, phantomRI] = createGrids(xdim,zdim,umpp_x,umpp_z)

    iRI = 1
    phantomRI[:,:] = 1.35 # Modeling 2% wt/vol agarose

    # Add sub-beam size scatterers to phantom, center and two off-center
    n = 100
    d = 0.000560 #mm
    R = 1e5
    phantomStructure = createPointScatterers(phantomStructure, n, d, R, xdim, zdim, umpp_x, umpp_z)

    # Show maps (X by Z orientation)
    plt.figure(figsize=(24,10))
    plt.subplot(1,2,1)
    f = plt.imshow(phantomStructure,norm=LogNorm(vmin=1e2,vmax=1e6),extent = [0,zdim*umpp_z/1000,0,xdim*umpp_x/1000]) 
    plt.title('Reflectivity', fontsize=24)
    cbar = plt.colorbar(f, fraction=0.046, pad=0.04)
    plt.xlabel('mm',fontsize=18)
    plt.ylabel('mm',fontsize=18)
    plt.xticks(fontsize = 16)
    plt.yticks(fontsize = 16)
    cbar.ax.tick_params(labelsize = 16)
    plt.subplot(1,2,2)
    f = plt.imshow(phantomRI,extent = [0,zdim*umpp_z/1000,0,xdim*umpp_x/1000,]) 
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
    np.save('phantom_umpp',(umpp_x,umpp_z))

