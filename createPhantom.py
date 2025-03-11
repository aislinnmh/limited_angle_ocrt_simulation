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

def createGrids():
    emptyOCT = np.zeros((ydim, xdim))
    emptyRI = np.ones((ydim, xdim))
    return emptyOCT, emptyRI

def createTube(tubeOCT, tubeRI, od, id, R, RI, iRI):
    # tubeOCT, tubeRI = current phantom structure and RI map
    # od = outer diameter in mm
    # id = inner diameter in mm
    # R = OCT Reflectivity of surface (10^R)
    # RI = refractive index of tube
    # iRI = refractive index of solution inside tube

    orad = od/2
    irad = id/2

    # Create grid of distances from center in mm
    x = (np.arange(xdim)-np.floor(xdim/2)) * umpp_x/1000 # pixels --> centered --> mm
    y = (np.arange(ydim)-np.floor(ydim/2)) * umpp_y/1000 # pixels --> centered --> mm
    xgrid, ygrid = np.meshgrid(x,y)
    d = xgrid**2 + ygrid**2
    
    # Add RI signal
    mask = (d>=irad) * (d<=orad)     # Mask tube area
    tubeRI[mask] = RI
    mask = (d<irad)                  # Mask inside of tube
    tubeRI[mask] = iRI

    # Add reflection of OCT as the surfaces of the tube
    tol = 0.001
    mask = (abs(d-orad)<=tol) | (abs(d-irad)<=tol)     # Mask tube surface
    tubeOCT[mask] = 10**R

    return tubeOCT, tubeRI

def fillMaskWithReflectors(OCT, mask, Rmin, Rmax, coverage):
    # OCT = current phantom structure 
    # Rmin = Minimum OCT Reflectivity of surface (10^Rmin)
    # Rmax = Maximum OCT Reflectivity of surface (10^Rmax)
    # coverage = density of scatterer packing (% / 100)

    [rows,cols] = np.where(mask) # Convert mask to a list of indices
    nMask = len(rows) # Total points in the mask
    random_points = random.sample(range(nMask), round(nMask*coverage)) # Which points contain reflectors
    R_options = np.logspace(Rmin,Rmax,100,base=10) # Possible reflectivities
    Rs = np.zeros_like(rows)
    random_Rs = random.choices(R_options, k= round(nMask*coverage)) # Randomly apply R values within range
    Rs[random_points] = random_Rs
    OCT[rows,cols] = Rs

    return OCT

def createCenterCircle(circleOCT, circleRI, d , Rmin, Rmax, coverage, RI):
    # circleOCT, circleRI = current phantom structure and RI map
    # d = diameter in mm
    # Rmin = Minimum OCT Reflectivity of circle (10^Rmin)
    # Rmax = Maximum OCT Reflectivity of circle (10^Rmax)
    # coverage = density of scatterer packing (% / 100)
    # RI = refractive index

    rad = d/2

    # Create grid of distances from center in mm
    x = (np.arange(xdim)-np.floor(xdim/2)) * umpp_x/1000 # pixels --> centered --> mm
    y = (np.arange(ydim)-np.floor(ydim/2)) * umpp_y/1000 # pixels --> centered --> mm
    xgrid, ygrid = np.meshgrid(x,y)
    d = np.sqrt(xgrid**2 + ygrid**2)

    mask = (d<rad)                  # Mask area of circle
   
    # Add RI signal
    circleRI[mask] = RI

    # Add OCT scatterers randomly, densely packed within area
    circleOCT = circleOCT + fillMaskWithReflectors(circleOCT, mask, Rmin, Rmax, coverage)

    return circleOCT, circleRI

def keepWithin2Pi(theta):
    if theta >= 2*np.pi:
        theta = theta - 2*np.pi
    if theta < 0:
        theta = theta + 2*np.pi
    return theta

def createIrregularShapes(blobsOCT, blobsRI, n, seedDim, Rmin, Rmax, coverage, RI, iRI, displayOn=False):
    # n = # of shapes
    # seedDim = rough size of region around each random point in which to create blobs
    # blobOCT, blobRI = current phantom structure and RI map
    # Rmin = Minimum OCT Reflectivity of blob (10^Rmin)
    # Rmax = Maximum OCT Reflectivity of blob (10^Rmax)
    # coverage = density of scatterer packing (% / 100)
    # RI = refractive index 
    # iRI = refractive index inside tube (background)
    # displayOn = whether to show intermediate blob creation parameters, for fine tuning and debugging

    # Find where not air, tube, or circle, is free space for the blobs
    freeSpacesMask = (blobsRI==iRI)
    freeSpacesMask.dtype='uint8'
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(seedDim*2),int(seedDim*2)))
    freeSpacesMask = cv2.morphologyEx(freeSpacesMask, cv2.MORPH_ERODE, kernel)
    freeSpacesMask.dtype='bool'
    # plt.figure(figsize=(16,8))
    # plt.imshow(freeSpacesMask) 
    # plt.colorbar()

    # Create angles array
    x = (np.arange(xdim)-np.floor(xdim/2)) * umpp_x/1000 # pixels --> centered --> mm
    y = (np.arange(ydim)-np.floor(ydim/2)) * umpp_y/1000 # pixels --> centered --> mm
    xgrid, ygrid = np.meshgrid(x,y)
    theta = np.arctan(ygrid/xgrid)
    theta[:,0:int(np.ceil(xdim/2))] = theta[:,0:int(np.ceil(xdim/2))] + np.pi
    theta = theta + np.pi/2

    mask = np.zeros((ydim,xdim))
    theta1 = -1
    
    # Add blobs to image
    for i in range(n):
        # Choose acceptable ranges for blob angle seed based on n
        thetamin = 2*np.pi/n * i
        thetamax = thetamin + 2*np.pi/n
        angleMask = (theta>thetamin) * (theta<thetamax)

        if theta1 >= 0: 
            # Don't let a blob appear across from the last blob
            thetaAcross = theta1 + np.pi
            thetaAcross = keepWithin2Pi(thetaAcross)
            blockThetaMin = thetaAcross - np.pi/8
            blockThetaMin= keepWithin2Pi(blockThetaMin)
            blockThetaMax = thetaAcross + np.pi/8
            blockThetaMax = keepWithin2Pi(blockThetaMax)
            if blockThetaMin > blockThetaMax:
                blockMask1 = (theta>blockThetaMin) | (theta<blockThetaMax)
            else:   
                blockMask1 = (theta>blockThetaMin) * (theta<blockThetaMax)

            # Don't let a blob appear close to the last blob
            blockThetaMin = theta1 - np.pi/8
            blockThetaMin= keepWithin2Pi(blockThetaMin)
            blockThetaMax = theta1 + np.pi/8
            blockThetaMax = keepWithin2Pi(blockThetaMax)
            if blockThetaMin > blockThetaMax:
                blockMask2 = (theta>blockThetaMin) | (theta<blockThetaMax)
            else:   
                blockMask2 = (theta>blockThetaMin) * (theta<blockThetaMax)
            angleMask = angleMask * ~blockMask1 * ~blockMask2

        # Choose a location to seed a blob
        eligibleMask = angleMask * freeSpacesMask
        [rows,cols] = np.where(eligibleMask) # Convert mask to a list of indices
        nMask = len(rows) # Total points in the mask
        random_point = random.sample(range(nMask), 1) # Which point to seed
        seedy = rows[random_point][0]
        seedx = cols[random_point][0]

        # Calculate the angle chosen 
        theta1 = theta[seedy,seedx]

        # Generate blobs
        noise = np.random.randint(0, 255, (seedDim*2,seedDim*2)).astype(np.uint8)
        blur = cv2.GaussianBlur(noise, (seedDim+1,seedDim+1), seedDim/16, borderType=0)
        stretch = skimage.exposure.rescale_intensity(blur, in_range='image', out_range=(0,255)).astype(np.uint8)
        thresh = cv2.threshold(stretch, 240, 255, cv2.THRESH_BINARY)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(seedDim/4),int(seedDim/4)))
        result = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        result = cv2.morphologyEx(result, cv2.MORPH_CLOSE, kernel)
        mask[seedy-seedDim:seedy+seedDim, seedx-seedDim:seedx+seedDim] = result

        if displayOn:
            plt.figure(figsize=(16,8))
            plt.subplot(1,5,1)
            plt.imshow(eligibleMask) 
            plt.colorbar()
            plt.subplot(1,5,2)
            plt.imshow(stretch)
            plt.colorbar() 
            plt.subplot(1,5,3)
            plt.imshow(thresh) 
            plt.colorbar()
            plt.subplot(1,5,4)
            plt.imshow(result) 
            plt.colorbar()
            plt.subplot(1,5,5)
            plt.imshow(mask) 
            plt.colorbar()
            plt.show()

    mask = mask>0
    # mask = mask*freeSpacesMask
    blobsRI[mask] = RI

    blobsOCT = blobsOCT + fillMaskWithReflectors(blobsOCT, mask, Rmin, Rmax, coverage)

    return blobsOCT, blobsRI

def createPointScatterers(pointsOCT,pointsRI,n,d,R,RI,iRI):
    # n = # of points
    # d = diameter in mm
    # pointsOCT, pointsRI = current phantom structure and RI map
    # R = OCT Reflectivity
    # RI = refractive index
    # iRI = refractive index inside tube (background)

    rad = d/2

    # Find where not air, tube, circle, or blob is free space for the point scatterers
    freeSpacesMask = (pointsRI==iRI)
    freeSpacesMask.dtype='uint8'
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(int(100),int(100)))
    freeSpacesMask = cv2.morphologyEx(freeSpacesMask, cv2.MORPH_ERODE, kernel)
    freeSpacesMask.dtype='bool'
    # plt.figure(figsize=(16,8))
    # plt.imshow(freeSpacesMask) 
    # plt.colorbar()

    # Choose locations of points
    [rows,cols] = np.where(freeSpacesMask) # Convert mask to a list of indices
    nMask = len(rows) # Total points in the mask
    random_points = random.sample(range(nMask), n) # Which points 

    mask = np.zeros((ydim,xdim))

    for i in range(n):
        y = rows[random_points][i]
        x = cols[random_points][i]
        
        # Create grid of distances from center in mm
        x = (np.arange(xdim)-x) * umpp_x/1000 # pixels --> centered --> mm
        y = (np.arange(ydim)-y) * umpp_y/1000 # pixels --> centered --> mm
        xgrid, ygrid = np.meshgrid(x,y)
        d = np.sqrt(xgrid**2 + ygrid**2)

        pointMask = (d<rad).astype(int)                  # Mask area of circle
        mask = mask + pointMask

    mask = mask.astype(bool)
    pointsOCT[mask] = R
    pointsRI[mask] = RI

    return pointsOCT, pointsRI

def fillTubeBackground(phantomStructure, phantomRI, Rmin, Rmax, coverage, iRI):
    # pointsOCT, pointsRI = current phantom structure and RI map
    # R = OCT Reflectivity
    # Rmin = Minimum OCT Reflectivity of tube background (10^Rmin)
    # Rmax = Maximum OCT Reflectivity of tube background (10^Rmax)
    # coverage = density of scatterer packing (% / 100)
    # RI = refractive index 
    # iRI = refractive index inside tube background

    mask = (phantomRI==iRI)
    phantomStructure = phantomStructure + fillMaskWithReflectors(phantomStructure, mask, Rmin, Rmax, coverage)

    return phantomStructure, phantomRI



if __name__ == "__main__":

    [phantomStructure, phantomRI] = createGrids()

    # Add the sample outer tube to the phantom
    iRI = 1.33
    [phantomStructure, phantomRI] = createTube(phantomStructure, phantomRI, od=1.8, id=1.4, R=4, RI=1.5, iRI=iRI)

    # Add a solid circle to the phantom center
    [phantomStructure, phantomRI] = createCenterCircle(phantomStructure, phantomRI, d=0.2, Rmin=3, Rmax=3.5, coverage=0.9, RI=1.43)

    # Add irregular shapes
    [phantomStructure, phantomRI] = createIrregularShapes(phantomStructure, phantomRI, n=2, seedDim=200, Rmin=2, Rmax=3, coverage=0.7, RI=1.38, iRI=iRI, displayOn=False)

    # Add sub-beam size scatterers to phantom
    [phantomStructure, phantomRI] = createPointScatterers(phantomStructure, phantomRI, n=8, d=0.01, R=1e5, RI=1.47, iRI=iRI)

    # Fill in background inside tube with OCT scatterers
    [phantomStructure, phantomRI] = fillTubeBackground(phantomStructure, phantomRI, Rmin=-1, Rmax=0, coverage=0.7, iRI=iRI)

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

