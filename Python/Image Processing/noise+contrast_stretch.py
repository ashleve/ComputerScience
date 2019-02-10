# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import os
import warnings
import numpy as np
import skimage as skimg
from skimage import io
from skimage import color
from skimage import exposure
import pydicom as dicom
import cv2
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import matplotlib.image as mpimg
import matplotlib.patches as patches
from skimage.util import img_as_ubyte
from skimage.util import img_as_float32


from skimage import transform as tf
from skimage import data

def lowpass_filter(dname, fname):
    fname = dname+fname
    img=io.imread(fname)
    img= img_as_float32(img)
    img = add_noise("s&p", img)
    if img.ndim>2:
        img=color.rgb2gray(img)
    
    #sigma -> jak szybko gasna
    #mode reflect -> odbija sie symetrycznie na 2 strone
    #granice obrazu sa odbiciem symetrycznym
    #imflt.gaussian - > inne pixele gasna odnosnie odleglosci od srodka pixela
    img=imflt.gaussian(img, sigma=2, mode='reflect')
    #img2 = imflt.median(img,mph.disk(2))
    
    fig, (ax,ax2)= plt.subplots(1,2)
    ax.imshow(img, cmap="gray")
    ax.set_title('original')
    ax2.imshow(img2, cmap="gray")
    ax2.set_title('noisy')
    ax.axis('off')
    ax2.axis('off')
    fig.tight_layout()
    plt.show(block=False)
    
    



def contrast_stretch():
    
    img = data.moon()
    p2, p98 = np.percentile(img, (2,58))
    #img2 = exposure.rescale_intesity(img, in_range=(p2,p98))
    
    
    img2 = (img.astype(np.float32)-p2)*255/(p98-p2)
    img2[img2<0]=0; img2[img2>255]=255
    img2=img2.astype(np.uint8)
    
    fig, (ax,ax2)= plt.subplots(1,2)
    ax.imshow(img, cmap="gray")
    ax2.imshow(img2, cmap="gray")


    #Display_histogram
    img2=img_as_float32(img2)
    img=img_as_float32(img)
    fig, ax = plt.subplots()
    #img.ravel() -> splaszczenie obrazu wielowymiarowego
    ax.hist(img2.ravel(), bins= 256, histtype="bar", color='blue')
    ax.ticklabel_format(axis='y', style = 'scientific', scilimits=(0,0))
    ax.set_xlim(0,1)
    ax.grid(True)
    
    #dystrybuatna
    fig,ax = plt.subplots()
    cdf, bins = exposure.cumulative_distribution(img2,256)
    ax.plot(bins,cdf,'r')
    ax.grid(True)
    
    

def add_noise(noise_type, image):
    
    if noise_type=="gauss":
        shp = image.shape
        mean = 0
        var = 0.01
        sigma = var**0.5
        gauss = np.random.normal(mean,sigma,shp)
        #gauss = gauss.reshape(shp)
        noisy = image+gauss
        return noisy
    elif noise_type =="uniform":
        k=1
        if image.ndim == 2:
            row,col = image.shape
            noisy = np.random.rand(row,col)
        else:
            row,col,chan = image.shape
            noisy = np.random.rand(row,col,chan)
        noisy = image + k*noisy
        return noisy
    elif noise_type =="s&p":
        s_vs_p = 0.5
        amount = 0.4
        out = np.copy(image) #kopiowanie obrazu#
        
        #Salt mode
        num_salt = np.ceil(amount * image.size * s_vs_p)
        coords = [np.random.randint(0,i-1, int(num_salt)) for i in image.shape]
        out[coords]= 1
        
        #Pepper mode
        num_pepper = np.ceil(amount * image.size *(1. - s_vs_p))
        coords = [np.random.randint(0,i-1, int(num_pepper)) for i in image.shape]
        out[coords]= 0
        return out
    elif noise_type =="poisson":
        PEAK=20
        noisy = (image+np.random.poisson(PEAK*image))/PEAK
        return noisy
    elif noise_type =="speckle":
        if image.ndim==2:
            row,col = image.shape
            noise= np.random.randn(row,col)
        else:
            row,col,chan = image.shape
            noise=np.random.randn(row,col,chan)
        noisy = image + image*0.2*noise
        return noisy
    
def test_noise(ntype, fname):
    img = io.imread(fname)
    img = img_as_float32(img)
    img2 = add_noise(ntype,img)
    
    fig, (ax,ax2)= plt.subplots(1,2)
    ax.imshow(img, cmap="gray")
    ax.set_title('original')
    ax2.imshow(img2, cmap="gray")
    ax2.set_title('noisy')
    ax.axis('off')
    ax2.axis('off')
    fig.tight_layout()
    plt.show(block=False)
    

def main():
    warnings.filterwarnings("ignore")
    data_dir = "C:\\Users\\student\Desktop\\images-20181017\\input1\\"
    #test_noise('speckle', data_dir + 'coins.png')
    #contrast_stretch()
    lowpass_filter(data_dir, 'coins.png')
    
if __name__ == "__main__":
    main()