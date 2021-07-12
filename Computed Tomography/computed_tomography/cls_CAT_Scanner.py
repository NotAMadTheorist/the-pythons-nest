from computed_tomography.cls_pixel_grid import *
from computed_tomography.func_projection_iterates import *
from numpy import nditer, linspace, matmul, uint8
from PIL import Image
from math import ceil
from time import time


class CAT_Scanner:
    def __init__(self, imageObj, beamArray, doConvertToGrayscale: bool = True):
        self.image = imageObj
        self.beamArray = beamArray
        self.beamArray.set_central_angle(0)
        self.imageWidth, self.imageHeight = self.image.size
        self.numberOfPixels = self.imageWidth * self.imageHeight
        self.pixelGrid = pixel_grid(self.imageWidth, self.imageHeight)
        self.pixelDensityArr = self.to_pixel_densities(self.image, doConvertToGrayscale)

        self.matrixA = array([])
        self.matrixB = array([])
        self.isScanned = False

    def change_image(self, newImageObj, doConvertToGrayscale: bool = True):
        self.image = newImageObj
        self.imageWidth, self.imageHeight = self.image.size
        self.numberOfPixels = self.imageWidth * self.imageHeight
        self.pixelGrid = pixel_grid(self.imageWidth, self.imageHeight)
        self.pixelDensityArr = self.to_pixel_densities(self.image, doConvertToGrayscale)
        self.matrixA = array([])
        self.matrixB = array([])
        self.isScanned = False

    def change_beam_array(self, newBeamArray):
        self.beamArray = newBeamArray
        self.beamArray.set_central_angle(0)

    def to_pixel_densities(self, imageObj, doConvertToGrayscale):
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
        print(f"Time taken to scan image:  {timeTaken} s")
        self.isScanned = True

    def to_color_values(self, arrayObj):
        funcToGrayscaleValue = lambda x: ceil(255*(10-x) / 10)
        funcToColorRGB = lambda g: [g, g, g]

        colorValuesFlat = []
        for x in nditer(arrayObj):
            colorValue = funcToColorRGB(funcToGrayscaleValue(x))
            colorValuesFlat.append(colorValue)
        colorValues = array(colorValuesFlat, uint8).reshape((self.imageHeight, self.imageWidth, 3))

        return colorValues

    def reconstruct_image(self, iterations):
        if not self.isScanned:
            raise Exception("image has not yet been scanned; call CAT_Scanner.scan(n) to scan the image")

        initialVectorX = array([0.0]*self.numberOfPixels)
        vectorOriginalX = self.pixelDensityArr.flatten()

        time1 = time()
        vectorApproxX = projection_iterates(initialVectorX, self.matrixA, self.vectorB, iterations, False)
        time2 = time()

        timeTaken = round(time2 - time1, 3)
        print(f"Time taken to reconstruct image:  {timeTaken} s")

        colorsRGBX = self.to_color_values(vectorApproxX)
        reconstructedImage = Image.fromarray(colorsRGBX)

        return reconstructedImage
