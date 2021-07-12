from computed_tomography.cls_pixel_grid import *
from computed_tomography.func_projection_iterates import *
from numpy import nditer, linspace, matmul, uint8
from PIL import Image
from math import ceil
from time import time


class CAT_Scanner:
    """A class which simulates a Computed Tomography (CT) scan on a given image with a constructed beam array."""

    def __init__(self, imageObj, beamArray, doConvertToGrayscale: bool = True):
        """Initialize a CAT Scanner on an image with a beam array."""

        # set the contained image, its width, height, and number of pixels
        self.image = imageObj
        self.imageWidth, self.imageHeight = self.image.size
        self.numberOfPixels = self.imageWidth * self.imageHeight

        # set the beam array at an angle of 0 degrees to the circumcircle of the image; that is, place the beam array
        # on the left side of the circumcircle
        self.beamArray = beamArray
        self.beamArray.set_central_angle(0)

        # set a pixel grid object, which helps in deciding which pixels are hit by each beam
        self.pixelGrid = pixel_grid(self.imageWidth, self.imageHeight)

        # pixel densities of the original image
        self.pixelDensityArr = self.to_pixel_densities(self.image, doConvertToGrayscale)

        # matrices A and B are used for computing the reconstructed image
        # matrix A contains information on which pixels are struck by each beam
        # matrix B tells how much of each beam is absorbed as it passes through the image
        self.matrixA = array([])
        self.matrixB = array([])

        # flag which is set to true once the image is already scanned
        self.isScanned = False

    def change_image(self, newImageObj, doConvertToGrayscale: bool = True):
        """Switches the image of the scanner to another chosen image object."""

        # initialize the scanner again but with the new image
        self.image = newImageObj
        self.imageWidth, self.imageHeight = self.image.size
        self.numberOfPixels = self.imageWidth * self.imageHeight
        self.pixelGrid = pixel_grid(self.imageWidth, self.imageHeight)
        self.pixelDensityArr = self.to_pixel_densities(self.image, doConvertToGrayscale)
        self.matrixA = array([])
        self.matrixB = array([])
        self.isScanned = False

    def change_beam_array(self, newBeamArray):
        """Switch the beam array used in the scan"""
        self.beamArray = newBeamArray
        self.beamArray.set_central_angle(0)

    def to_pixel_densities(self, imageObj, doConvertToGrayscale):
        """Converts an image to a grayscale image and returns an array consisting of pixel densities ranging from 0
        (white) to 10 (black)."""

        funcGrayscale = lambda r, g, b: ceil(0.2989 * r + 0.5870 * g + 0.1140 * b)
        funcScaleTo10 = lambda colorInt: 10 - 10 * colorInt / 255

        pixelRGBArr = array(imageObj)
        pixelDensityFlat = []

        r = 0
        red, green, blue = 0, 0, 0
        for colorPart in nditer(pixelRGBArr):
            color = int(colorPart)
            r += 1
            if r == 1:
                red = color
            elif r == 2:
                green = color
            elif r == 3:
                blue = color
                r = 0
                if doConvertToGrayscale:
                    pixelDensity = funcScaleTo10(funcGrayscale(red, green, blue))
                else:
                    pixelDensity = funcScaleTo10(red)
                pixelDensityFlat.append(pixelDensity)

        pixelDensityArr = array(pixelDensityFlat).reshape((self.imageHeight, self.imageWidth))
        return pixelDensityArr

    def scan(self, numberOfDirections):
        """Rotate the beam array around the image in a selected number of directions spaced evenly across the
        circumcircle of the image."""

        time1 = time()
        scanningAngles = linspace(0, 360, numberOfDirections+1)[:-1]
        submatricesA = []
        for scanAngle in scanningAngles:
            self.beamArray.set_central_angle(scanAngle)
            submatrixA = self.pixelGrid.coefficient_array_center_line(self.beamArray)
            submatricesA.append(submatrixA)

        self.matrixA = vstack(tuple(submatricesA))
        vectorX = self.pixelDensityArr.flatten()
        self.vectorB = matmul(self.matrixA, vectorX)
        time2 = time()

        timeTaken = round(time2 - time1, 3)
        print(f"Image successfully scanned in {timeTaken} s. \n")
        self.isScanned = True

    def to_color_values(self, arrayObj):
        """Translates an array of pixel densities into an array of equivalent RGB colors, ranging from white (0) to
        black (10)."""
        funcToGrayscaleValue = lambda x: ceil(255*(10-x) / 10)
        funcToColorRGB = lambda g: [g, g, g]

        colorValuesFlat = []
        for x in nditer(arrayObj):
            colorValue = funcToColorRGB(funcToGrayscaleValue(x))
            colorValuesFlat.append(colorValue)
        colorValues = array(colorValuesFlat, uint8).reshape((self.imageHeight, self.imageWidth, 3))

        return colorValues

    def reconstruct_image(self, iterations):
        """Reconstruct a grayscale version of the scanned image by using an iterative projection algorithm specified
        a number of iterations.

        NOTE:  This step may take a while to execute especially with images of size 30 x 30 pixels or larger."""

        if not self.isScanned:
            raise Exception("Image has not yet been scanned; call CAT_Scanner.scan(n) to scan the image")

        initialVectorX = array([0.0]*self.numberOfPixels)
        vectorOriginalX = self.pixelDensityArr.flatten()

        time1 = time()
        vectorApproxX = projection_iterates(initialVectorX, self.matrixA, self.vectorB, iterations, False)
        time2 = time()

        timeTaken = round(time2 - time1, 3)
        print(f"Image reconstructed in {timeTaken} s \n")

        colorsRGBX = self.to_color_values(vectorApproxX)
        reconstructedImage = Image.fromarray(colorsRGBX)

        return reconstructedImage

    def __repr__(self):
        return f"CAT_Scanner of {self.image}"
