import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mimg
from skimage import img_as_ubyte
from skimage.color import rgb2gray
from skimage.morphology import binary_erosion, binary_dilation
from skimage.morphology import binary_opening, binary_closing
from skimage.morphology import square, rectangle, diamond, disk, star, octagon
from scipy.ndimage.morphology import binary_hit_or_miss


def show(ax, img, text=""):
    ax.axis("off")
    ax.imshow(img, cmap="gray")
    ax.set_title(text)


def task1():
    img = mimg.imread("bw1.bmp")

    new_img1 = binary_erosion(img, selem=square(width=30))
    new_img2 = binary_erosion(img, selem=rectangle(width=30, height=20))
    new_img3 = binary_erosion(img, selem=diamond(radius=5))
    new_img4 = binary_erosion(img, selem=disk(radius=15))
    new_img5 = binary_erosion(img, selem=star(a=10))
    new_img6 = binary_erosion(img, selem=octagon(m=10, n=20))
    new_img7 = binary_dilation(img,)

    fig, ax = plt.subplots(1, 8)
    show(ax[0], img, "original")
    show(ax[1], new_img1, "BE square")
    show(ax[2], new_img2, "BE rectangle")
    show(ax[3], new_img3, "BE diamond")
    show(ax[4], new_img4, "BE disk")
    show(ax[5], new_img5, "BE star")
    show(ax[6], new_img6, "BE octagon")
    show(ax[7], new_img2, "binary_dilation")
    plt.show()


def task2():
    img = mimg.imread("bw2.bmp")

    # domkniecie robi najpierw dylatacje potem erozje wiec usuwa wystajace elementy
    new_img = binary_closing(img, selem=disk(2.4))
    # otwarcie robi najpierw erosje potem dylatacje, usuwa rysy
    new_img = binary_opening(new_img, selem=disk(2))


    # alternatywa
    # new_img = binary_closing(img, selem=disk(2.4))
    # new_img= 1-new_img
    # new_img = binary_closing(img, selem=disk(2.4))
    # new_img=1-new_img

    fig, ax = plt.subplots(1, 2)
    show(ax[0], img, "before")
    show(ax[1], new_img, "after")
    plt.show()


def task3():
    img = mimg.imread("hm2.bmp")
    img = rgb2gray(img)
    new_img = 1-img

    new_img = binary_hit_or_miss(new_img, structure1=square(50))

    new_img = np.array(new_img, dtype=np.uint8)
    _, contours, hierarchy = cv2.findContours(
        new_img,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    number_of_squares = len(contours)
    print(number_of_squares)

    fig, ax = plt.subplots(1, 2)
    show(ax[0], img, "original")
    show(ax[1], new_img, "hit_or_miss")
    plt.show()


def task4():
    img = mimg.imread("x.png")
    img = rgb2gray(img)
    img = img_as_ubyte(img)

    ret, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)

    new_img = binary_opening(thresh, selem=disk(35))

    # fig, ax = plt.subplots(1, 3)
    # show(ax[0], img, "original")
    # show(ax[1], thresh, "thresh")
    # show(ax[2], new_img, "new_img")
    # plt.show()

    fig, ax = plt.subplots(1, 1)
    show(ax, new_img)
    plt.show()


def main():
    # task1()
    # task2()
    # task3()
    task4()


if __name__ == "__main__":
    main()
