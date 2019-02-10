import cv2
import skimage.io as io
import numpy as np
import matplotlib.pyplot as plt
import skimage.segmentation as sgm
import skimage.color as color
import skimage.filters as imflt
from skimage.util import img_as_ubyte


class ImageSegmantation():

    def show(self, ax, img, text=""):
        ax.imshow(img, cmap="gray")
        ax.axis("off")
        ax.set_title(text)

    def task1(self):

        img = io.imread("lungs_lesion.bmp")
        markers = io.imread("lungs_lesion_seeds1.bmp")

        for B in range(0, 100001, 5000):
            print(B)

            rw = sgm.random_walker(img, markers, beta=B)

            fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
            self.show(ax1, img, "original")
            self.show(ax2, markers, "markers")
            self.show(ax3, rw, "random_walker")
            plt.show()

    def task2(self):

        img = io.imread("apples.jpg")

        green = img[:, :, 1]
        blue = img[:, :, 2]
        img1 = color.rgb2gray(img)
        img1 = img_as_ubyte(img1)

        ret, img1 = cv2.threshold(img1, 230, 255, cv2.THRESH_BINARY)
        img1[img1 != 0] = 127
        img1[np.logical_and(blue < 28, green < 28)] = 255
        rw = sgm.random_walker(color.rgb2gray(img), img1, beta=10000)

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
        self.show(ax1, img, "original")
        self.show(ax2, img1, "seeds")
        self.show(ax3, rw, "random_walker")
        plt.show()

    def task3(self):

        image = io.imread("cat.jpg")

        fig, ax = plt.subplots(1, 3)

        # kot
        points = np.linspace(0, 2*np.pi, 700)
        x = 480 + 340*np.cos(points)
        y = 140 + 160*np.sin(points)
        ellipse = np.transpose(np.array([x, y]))
        contour = sgm.active_contour(
            image, ellipse, alpha=0.20, beta=5000, gamma=0.001)

        self.show(ax[0], image, "cat with active_contour")
        ax[0].plot(ellipse[:, 0], ellipse[:, 1], "--r", lw=2)
        ax[0].plot(contour[:, 0], contour[:, 1], "-b", lw=2)

        # motyl
        points2 = np.linspace(0, 2*np.pi, 700)
        x2 = 110 + 50*np.cos(points2)
        y2 = 135 + 50*np.sin(points2)
        ellipse2 = np.transpose(np.array([x2, y2]))
        contour2 = sgm.active_contour(
            image, ellipse2, alpha=1, beta=0, gamma=0.01)

        self.show(ax[1], image, "butterfly with active_contour")
        ax[1].plot(ellipse2[:, 0], ellipse2[:, 1], "--r", lw=1)
        ax[1].plot(contour2[:, 0], contour2[:, 1], "-b", lw=1)

        # gaussian
        points3 = np.linspace(0, 2*np.pi, 700)
        x3 = 460 + 320*np.cos(points3)
        y3 = 140 + 140*np.sin(points3)
        ellipse3 = np.transpose(np.array([x, y]))
        contour3 = sgm.active_contour(imflt.gaussian(
            image, 3), ellipse3, alpha=0.205, beta=0, gamma=0.001)

        self.show(ax[2], image, "cat with gaussian")
        ax[2].plot(ellipse3[:, 0], ellipse3[:, 1], "--r", lw=1)
        ax[2].plot(contour3[:, 0], contour3[:, 1], "-b", lw=1)

        plt.show()

    def task4(self):

        img = io.imread("objects1.jpg")
        # img = io.imread("objects2.jpg")
        # img = io.imread("objects3.jpg")
        image = color.rgb2gray(img)

        # szum
        PEAK = 50
        image = (image+np.random.poisson(PEAK*image))/PEAK

        iteration = 100
        s = sgm.chan_vese(image, max_iter=iteration)

        fig, (ax1, ax2) = plt.subplots(1, 2)
        self.show(ax1, image, "image")
        self.show(ax2, s, "max_iter: " + str(iteration))
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
        elif option == 4:
            imseg.task4()


if __name__ == "__main__":
    main()
