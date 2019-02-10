import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage as ndi
import matplotlib.image as mimg
from skimage import img_as_ubyte, img_as_float32, img_as_float64
import skimage.morphology as mph
import skimage.filters as imflt
import skimage.feature as feature
import skimage.segmentation as sgm
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.filters import try_all_threshold


class ImageSegmantation():

    def show(self, ax, img, text = ""):
        ax.axis("off")
        ax.imshow(img, cmap="gray")
        ax.set_title(text)

    def task1(self):
        img = cv2.imread("brain_tumor.bmp", 0)
    
        # 1
        ret, thresh = cv2.threshold(img ,227, 255, cv2.THRESH_BINARY)
    
        # 2
        # a)
        # ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) 
        # b)
        # fig, ax = try_all_threshold(img, figsize=(10, 8), verbose=False)

        # 3
        # a)
        # thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 2559, 1)
        # b)
        # thresh = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 2559, 1)
    
        fig, (ax1, ax2)=plt.subplots(1,2)
        self.show(ax1, img, "brain")
        self.show(ax2, thresh, "tumor")
        plt.show()
    
    
    def task2(self):
        img = cv2.imread("gears.bmp")
        img = rgb2gray(img)

        img1=feature.canny(img, sigma=1.6, low_threshold=0.001*255, high_threshold=0.0005*255)

        # ret,thresh = cv2.threshold(img, 127, 255, 0)
        # img1, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # img2 = mph.remove_small_holes(img1,10000,2)

        # img1 = 255 - img1

        # img1 = imflt.sobel(img)
        # img1 = imflt.prewitt(img)
       
        # img1 = imflt.apply_hysteresis_threshold(img , 20 , 30)

        img2 = ndi.binary_fill_holes(img1)
        fig, (ax1, ax2, ax3) = plt.subplots(1,3)
        self.show(ax1, img)
        self.show(ax2, img1)
        self.show(ax3, img2)
        plt.show()
    

    def task3(self):
            img1 = img_as_float64(mimg.imread("fish.bmp"))
            imgray = rgb2gray(img1)
    
            # Method 1
            # img2=sgm.watershed(imgray, markers=300, watershed_line=True)

            # Method 2
            # img2 = sgm.slic(imgray, n_segments=30, compactness=0.3, sigma=20)

            # Method 3
            # img2 = sgm.quickshift(img1, kernel_size=5, max_dist=15, ratio=0.05)
            
            # Method 4
            img2 = sgm.felzenszwalb(imgray, scale=200, sigma=1, min_size=100)
            

            img3 = sgm.mark_boundaries(img1,img2)

            fg, (ax1, ax2, ax3) = plt.subplots(1,3)
            self.show(ax1, img1, "original")
            self.show(ax2, img2, "markers")
            self.show(ax3, img3, "with segmentation")
            plt.show()



def main():
    imseg = ImageSegmantation()

    while(1):
        option = input("Podaj numer zadania: ")
        option = int(option)

        if option == 1:
            imseg.task1()
        elif option == 2:
            imseg.task2()
        elif option == 3:
            imseg.task3()
    

if __name__ == "__main__":
    main()
