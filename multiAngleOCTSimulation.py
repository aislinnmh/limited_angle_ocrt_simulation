import numpy as np
import tensorflow as tf
import scipy.ndimage
import os
from PIL import Image

class angularOCTSim2D:

    def __init__(self, sampleID, saveFolder):

        self.sampleID= sampleID
        self.saveFolder = saveFolder

        self.R = np.load(sampleID + 'R.npy') # reflectivity/structure of sample
        self.RI = np.load(sampleID + 'RI.npy') # refractive index map of sample
        [self.umpp_x, self.umpp_z] = np.load(sampleID + '_umpp.npy') # microns per initial pixel
        [self.xdim_i, self.zdim_i] = self.R.shape

    def setParameters(self, angles, Ascans, zpixels, depth, lat_FOV, ax_res, lat_res, mu_t):

        self.angles = angles
        self.Ascans = Ascans
        self.zpixels = zpixels
        self.depth = depth
        self.lat_FOV = lat_FOV
        self.ax_res = ax_res
        self.lat_res = lat_res
        self.mu_t = mu_t 

    def rotate(self):

        R = Image.fromarray(self.R)
        [m,n] = self.R.shape
        rotated = np.zeros((len(self.angles),m,n))
        for i in range(len(self.angles)):
            a = self.angles[i]
            rotatedR = R.rotate(a)
            rotated[i,:,:] = rotatedR

        self.Rstack = rotated
        return rotated
    
    def createPSF(self): 

        # Convert FWHM of gaussian to its sigma = FWHM / 2.35482, then to pixels
        xsig = self.lat_res/2.35482
        zsig = self.ax_res/2.35482
        xsig = xsig/self.umpp_x
        zsig = zsig/self.umpp_z

        Lfactor = 5
        xdim_kernel = round(xsig*Lfactor)
        zdim_kernel = round(zsig*Lfactor)

        x = np.array(range(xdim_kernel))
        xmu = round(len(x)/2)
        x = 1/(xsig*np.sqrt(2*np.pi))*np.exp(-0.5*((x-xmu)**2)/(xsig*82))
        x = np.expand_dims(x,axis=1)
        xpsf = tf.tile(x,[1,zdim_kernel])

        z = np.array(range(zdim_kernel))
        zmu = round(len(z)/2)
        z = 1/(zsig*np.sqrt(2*np.pi))*np.exp(-0.5*((z-zmu)**2)/(zsig*82))
        z = np.expand_dims(z,axis=0)
        zpsf = tf.tile(z,[xdim_kernel,1])

        psf = tf.multiply(xpsf,zpsf)
        # psf = np.expand_dims(psf,axis=0)

        return psf
    
    def convolvePSF(self):

        psf = self.createPSF()
        psf = np.expand_dims(psf,axis=0)
        print(psf.shape)

        # print(Rstack.shape)

        convolved = scipy.ndimage.convolve(self.Rstack, psf)

        self.Rstack = convolved
        return convolved
    
    def attenuate(self):

        z = np.array(range(self.zdim_i))
        z = z * self.umpp_z / 1000 # mm
        attenuation = np.exp(-1 * self.mu_t * z) # CHECK TYPE OF ATTEN
        z = np.expand_dims(z,axis=0)
        z = tf.tile(z,[self.xdim_i,1])
        z = np.expand_dims(z,axis=0)
        z = tf.tile(z,[len(self.angles),1,1])

        attenuated = tf.multiply(self.Rstack, attenuation)

        self.Rstack = attenuated
        return attenuated
    
    def resample(self):
        
        resampled = np.zeros((len(self.angles),self.Ascans,self.zpixels))
        Rstack = np.array(self.Rstack, dtype=float)
        print(resampled.shape)

        for i in range(len(self.angles)):
            R = Image.fromarray(Rstack[i,:,:])
            resampledR = R.resize((self.zpixels,self.Ascans))
            resampled[i,:,:] = resampledR

        self.Rstack = resampled
        return resampled
    
    def getUMDims(self):
        
        umpp_x_new = self.xdim_i * self.umpp_x  / self.Ascans
        umpp_z_new = self.zdim_i * self.umpp_z  / self.zpixels

        return umpp_x_new, umpp_z_new
