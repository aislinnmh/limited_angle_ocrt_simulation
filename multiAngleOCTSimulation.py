import numpy as np
import tensorflow as tf
import cv2
from scipy.fftpack import fft, fftshift, ifft, ifftshift
import scipy.io
import scipy.interpolate
import scipy.ndimage
import os
from time import time

class angularOCTSim2D:

    def __init__(self, sampleID, saveFolder, wavelength, NA, Ascans, zpixels, depth, lateralFOV):

        self.sampleID= sampleID
        self.saveFolder = saveFolder

        self.R = np.load(sampleID + 'R.npy') # reflectivity/structure of sample
        self.RI = np.load(sampleID + 'RI.npy') # refractive index map of sample
        # self.RI = np.pad(self.RI,((0,500),(1000,1000)),'constant', constant_values = (1,1))
        [self.umpp_x, self.umpp_z] = np.load(sampleID + '_umpp.npy') # microns per initial pixel
        [self.zdim_i, self.xdim_i] = self.R.shape

        sigblurRI = 5 #um
        blurRI = scipy.ndimage.gaussian_filter(self.RI,sigma = (sigblurRI/self.umpp_z,sigblurRI/self.umpp_x)) # will need to add rotated version later
        self.dndz = ((blurRI - scipy.ndimage.shift(blurRI, (1,0))) + (scipy.ndimage.shift(blurRI, (-1,0)) - blurRI))/2
        self.dndx = ((blurRI - scipy.ndimage.shift(blurRI, (0,1))) + (scipy.ndimage.shift(blurRI, (0,-1)) - blurRI))/2

        # OCT Parameters
        self.w = wavelength # nm
        self.na = NA
        self.Ascans = Ascans
        self.zpixels = zpixels
        self.depth = depth # mm
        self.lateralFOV = lateralFOV # mm

        # Ray propagation helpers
        self.step = 1
        self.nwsig = 0.006

    def setParameters(self, angles):
        # OCT Parameters
        # 
        
        # Rotation Matrices 
        rotmats = list()
        for a in angles:
            a *= np.pi/180 # Convert to radians
            a = a.astype(np.float32)
            rotmats.append(np.array([[np.cos(a), -np.sin(a)],
                                    [np.sin(a), np.cos(a)]]))
        rotmats = np.rollaxis(np.dstack(rotmats), 2, 0).astype(np.float32)
        self.rotmats = tf.constant(rotmats, name='rotationMatrices')

        # helpers for refraction

    def getRI(self,z,x):
        return self.RI[np.round(z.numpy()).astype(int),np.round(x.numpy()).astype(int)]

    def getRIderivatives(self,z,x):
        # dndx = self.RI[np.round(z.numpy()).astype(int),np.round(x.numpy()+1).astype(int)] - self.RI[np.round(z.numpy()).astype(int),np.round(x.numpy()).astype(int)]
        # dndz = self.RI[np.round(z.numpy()+1).astype(int),np.round(x.numpy()).astype(int)] - self.RI[np.round(z.numpy()).astype(int),np.round(x.numpy()).astype(int)]
        dndx = self.dndx[np.round(z.numpy()).astype(int),np.round(x.numpy()).astype(int)]
        dndz = self.dndz[np.round(z.numpy()).astype(int),np.round(x.numpy()).astype(int)]
        return dndz, dndx
    
    def getXZderivatives(self,z0,x0):
        dxdz1 = x0[:,1]

        [dndz, dndx] = self.getRIderivatives(z0,x0[:,0])
        n = self.getRI(z0,x0[:,0])

        dxdz2 = 1. / n * (dndx * (1 + dxdz1 ** 2) - dndz * dxdz1)

        derivs = tf.stack([dxdz1, dxdz2], 1)
        return derivs

    def step_rk4(self,xz0,dummy):
        # Propagate ray through sample's RI distribution one step, adpated version of rk4_step_opl() and rayeq_opl() in OCRT.py
        # xz0 = current position
        # dummy: tf.scan requires passing a second argument, not actually needed

        z0 = xz0[:,0] # pixel
        x0 = xz0[:,1:3] # starts with 0 for 2nd, gradient 

        # Get current RI  and dXdz derivative 
        n = self.getRI(z0,x0[:,0])

        # Define step size with index and derivative at the current step
        h = self.step / n
        hstack = tf.stack([h,h], 1)
        half_h = h * .5

        # Runge-Kutta, perform to get first deriv and second deriv at once
        k1 = self.getXZderivatives(z0,x0)

        z2 = z0 + half_h
        x2 = x0 + hstack*(k1 / 2)
        k2 = self.getXZderivatives(z2,x2)

        z3 = z2
        x3 = x0 + hstack*(k2/2)
        k3 = self.getXZderivatives(z3,x3)

        z4 = z0 + h
        x4 = x0 + hstack*k3
        k4 = self.getXZderivatives(z4,x4)

        xnew = x0 + (k1 + 2. * k2 + 2 * k3 + k4) / 6.
        znew = z4

        xznew = tf.concat([tf.expand_dims(znew,1),xnew],1)
        return xznew


    def propagateRays(self):
        # Propagate rays through sample's RI distribution, adpated version of integrate_scan_opl() in OCRT.py

        x0 = np.arange(200,self.xdim_i-200,1)

        z0 = np.zeros((len(x0),))
        dxdz0 = np.zeros((len(x0),))
        xz0 = tf.stack([z0,x0,dxdz0],1)

        dummy = tf.ones((self.zdim_i),) # Controls how many z steps will be performed

        paths = tf.scan(self.step_rk4, dummy, xz0, swap_memory=True)

        paths = paths[:,:,0:2] # throw out dxdz
        # Ends up as zpix x xpix x axes, where axis 1 is real zpos and 2 is real xpos

        return paths