import cv2
import skimage.io as io
import numpy as np
import skimage.filters as flt
import matplotlib.pyplot as plt
import skimage.measure as msr
from skimage import feature
from scipy import ndimage as ndi
from skimage.morphology import binary_opening, binary_closing
from skimage.morphology import disk



def Zad2_a():
    img = io.imread("coins.png")
    img = color.rgb2gray(img)
    thresh = flt.threshold_otsu(img)
    img_tmp = np.array(img)

    img[img_tmp >= thresh] = 1
    img[img_tmp < thresh] = 0

    img2 = img
    img = ndi.binary_fill_holes(img)

    plt.imshow(img, cmap="gray")
    plt.show()

    img = msr.label(img)
    list = msr.regionprops(img)
    surface_areas = []
    for j, i in enumerate(list):
        surface_areas.append(i.area)

    mean = sum(surface_areas)/len(surface_areas)

    big = 0
    small = 0
    for i in surface_areas:
        if i >= mean:
            big += 1
        else:
            small += 1

    print("większy nominał: ", big)
    print("mniejszy nominał: ", small)



def Zad2_b():
    img = io.imread("coins.png")
    img = color.rgb2gray(img)

    img = feature.canny(img, sigma=2.5)
    img = ndi.binary_fill_holes(img)

    plt.imshow(img, cmap="gray")
    plt.show()

    img = msr.label(img)
    lista = msr.regionprops(img)
    area = 0
    for j, i in enumerate(lista):
        area += i.area

    print(area)



def Zad3():
    img = io.imread("planes.png")
    img = color.rgb2gray(img)
    img = 255 - img
    plt.imshow(img, cmap="gray")
    plt.show()
    img = ndi.binary_fill_holes(img)
    
    img = msr.label(img)
    list = msr.regionprops(img)

    planes = 0
    for j, i in enumerate(list):
        if i.area < 43000 and i.area > 42000:
            planes += 1

    print(planes)




def main():
    Zad3()



if __name__ == "__main__":
    main()