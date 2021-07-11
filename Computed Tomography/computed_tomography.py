
from numpy import array, dot, nditer, linspace, vstack, matmul, uint8
from math import sqrt, cos, sin, tan, floor, ceil, radians
from PIL import Image
from time import time

def projection_hyperplane(XPoint, A, b):
    """Finds the orthogonal projection X of XPoint on the hyperplane formed by the equation dot(A, X) = b,
    where XPoint, X, and A are vectors in n-space and b is a scalar."""

    projectionFactor = (b - dot(XPoint, A)) / dot(A, A)
    projectionX = XPoint + projectionFactor*A
    return projectionX


def projection_iterates(initialX, matrixA, vectorB, iterations, returnMultipleIterates:bool = False):
    """Iterates the vector initialX in n-space by orthogonally projecting it onto the M hyperplanes represented by
    each equation of the system (matrixA)(X) = vectorB. Returns a set of M iterate vectors obtained from the final
    iteration of applying the procedure described."""

    # test whether the sizes of the inputs are valid
    vectorDimension = initialX.shape[0]
    numberOfEquations = matrixA.shape[0]
    isValidInput = (vectorDimension == matrixA.shape[1]) and (numberOfEquations == vectorB.shape[0])

    if not isValidInput:
        raise Exception(f"Expected matrixA to have size {numberOfEquations} x {vectorDimension} and vectorB to have"
                        f" size {numberOfEquations} x 1.")


    currentX = initialX
    recentIterates = []

    zeroRow = [0]*vectorDimension
    isZeroRow = lambda row: sum(row == zeroRow) == vectorDimension

    isLastIteration = False
    for p in range(iterations):
        if p == iterations - 1:
            isLastIteration = True
        for k in range(numberOfEquations):
            A = matrixA[k]
            if isZeroRow(A):
                continue

            b = vectorB[k]
            newX = projection_hyperplane(currentX, A, b)
            if isLastIteration:
                recentIterates.append(newX)
            currentX = newX

    if not returnMultipleIterates:
        return currentX
    else:
        return recentIterates


class beam:
    """Beam objects represent the X-ray beams used to scan the object"""
    def __init__(self, centralAngle, translationAngle, inclination, beamWidth):

        # angles start at the left-hand side; positive angles go clockwise
        # angles are measured in degrees
        # the central angle is the angle of the middle beam in a scanner
        # the translation angle is how far this beam is from the middle beam
        # the beam width tells how thick the beam is relative to a pixel
        # the inclination is the angle between the beam's direction to the middle beam's direction

        self.centralAngle = centralAngle
        self.translationAngle = translationAngle
        self.inclination = inclination
        self.beamWidth = beamWidth
        self.set_angle()

    def set_angle(self):
        # angles relative to the center of the circle where the beams originate
        self.overallAngle = self.centralAngle + self.translationAngle
        self.overallInclination = self.centralAngle + self.inclination

    def set_central_angle(self, newAngle):
        # use this function when changing the central angle of the beam
        self.centralAngle = newAngle
        self.set_angle()


class beam_array_parallel:
    def __init__(self, numberOfBeams, spacingAngle, beamWidth, centralAngle):
        self.numberOfBeams = numberOfBeams
        self.beamWidth = beamWidth
        self.centralAngle = centralAngle

        # distribute the translation angles in two cases: odd or even number of beams
        translationAngles = []
        n = numberOfBeams
        q, r = n // 2, n % 2
        if r == 1:
            translationAngles = [k * spacingAngle for k in range(-q, q+1)]
        else:
            translationAngles = [(k-q+1/2)*spacingAngle for k in range(0, n)]

        # create the beam objects
        self.beamArray = [beam(centralAngle, T, 0, beamWidth) for T in translationAngles]

    def set_central_angle(self, newAngle):
        self.centralAngle = newAngle
        for bm in self.beamArray:
            bm.set_central_angle(newAngle)


class pixel_grid:
    def __init__(self, imageWidth, imageHeight):
        self.imageWidth = imageWidth
        self.imageHeight = imageHeight
        self.numberOfPixels = self.imageWidth * self.imageHeight

        # Here, the origin (0, 0) is at the top-left corner of the image
        # The x-axis goes to the right and the y-axis goes down

        self.minX, self.minY = 0, 0
        self.maxX, self.maxY = imageWidth, imageHeight

        # center and radius
        self.centerX, self.centerY = imageWidth/2, imageHeight/2
        self.minRadius = sqrt(imageWidth**2 + imageHeight**2)/2

        # setup pixel coordinates
        pixels = []
        pixelsList = []
        for i in range(imageHeight):
            pixelRow = []
            for j in range(imageWidth):
                pixelRow.append((j, i))
                pixelsList.append((j, i))
            pixels.append(pixelRow)
        self.pixels = pixels
        self.pixelsList = pixelsList

    def coefficient_list_center_line(self, beamObj):

        # First find where the line passes through in the circle centered about the image's center with
        # a radius equal to half the length of the diagonal of the image
        x0 = self.centerX - self.minRadius*cos(radians(beamObj.overallAngle))
        y0 = self.centerY - self.minRadius*sin(radians(beamObj.overallAngle))

        # Then assign x and y coordinates that describe each line in the grid
        gridX = [float(x) for x in range(self.minX, self.maxX + 1)]
        gridY = [float(y) for y in range(self.minY, self.maxY + 1)]
        nIntercepts = len(gridX)

        # Next, get the slope of the line by using the beam's overall inclination, and get all the points where
        # the line crosses any of the grid lines even those outside the image using the equation of the line
        i = beamObj.overallInclination
        isVertical = False
        if i % 90 != 0:
            m = tan(radians(i))
            getY = lambda x: round(y0 + m * (x-x0), 4)
            getX = lambda y: round(x0 + (y - y0)/m, 4)
            interceptY = [getY(x) for x in gridX]
            interceptX = [getX(y) for y in gridY]
        elif i % 180 == 0:
            interceptY = [y0]*nIntercepts
            interceptX = []
        else:
            interceptX = [x0]*nIntercepts
            interceptY = []
            isVertical = True
        interceptPointsA = list(zip(gridX, interceptY))
        interceptPointsB = list(zip(interceptX, gridY))



        # Next, only keep those intercepts that are within the image, remove any repeated intercepts and
        # sort the intercepts according to either y-coordinate (if the line is vertical) or x-coordinate
        # in all other cases
        interceptPointsA = [(x, y) for x, y in interceptPointsA if self.minY <= y <= self.maxY]
        interceptPointsB = [(x, y) for x, y in interceptPointsB if self.minX <= x <= self.maxX]
        interceptPoints = interceptPointsA
        interceptPoints.extend(interceptPointsB)
        interceptPoints = list(set(interceptPoints))
        if isVertical:
            interceptPoints.sort(key = lambda point: point[1])
        else:
            interceptPoints.sort(key = lambda point: point[0])

        # update the number of intercepts remaining
        nIntercepts = len(interceptPoints)

        # if there are any remaining intercepts, the line crosses the image
        if nIntercepts != 0:

            # Then for each pair of consecutive intercepts within the image, we take the length of the segment
            # (or distance) between them, which becomes a coefficient, and use the midpoint of the segment to
            # assign which pixel as this coefficient.
            aDistances = []
            pixelsIntercepted = []
            x1, y1 = interceptPoints[0]
            for i in range(0, nIntercepts - 1):
                x2, y2 = interceptPoints[i + 1]
                distance = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                aDistances.append(distance)

                midpoint = ((x1 + x2)/2, (y1 + y2)/2)
                pixelIntercepted = (floor(midpoint[0]), floor(midpoint[1]))
                pixelsIntercepted.append(pixelIntercepted)
                x1, y1 = x2, y2
            pixelInterceptedCoefficients = dict(zip(pixelsIntercepted, aDistances))

            # Finally, assemble the coefficient list which becomes a row in the linear system to be solved
            # during the scan and assemble an array representing the coefficients of each pixel in the grid
            coefficientList = []
            coefficientPixels = self.pixels.copy()
            for i in range(self.imageHeight):
                for j in range(self.imageWidth):
                    pixel = (j, i)
                    if pixel in pixelsIntercepted:
                        aValue = pixelInterceptedCoefficients[pixel]
                        coefficientList.append(aValue)
                        coefficientPixels[i][j] = aValue
                    else:
                        coefficientList.append(0.0)
                        coefficientPixels[i][j] = 0.0

        else:
            # If there are no remaining intercepts, the line does not cross the image and there are no
            # intercepts within the image.

            # Therefore, the row is simply the zero row

            coefficientList = []
            coefficientPixels = self.pixels.copy()
            for i in range(self.imageHeight):
                for j in range(self.imageWidth):
                    coefficientList.append(0.0)
                    coefficientPixels[i][j] = 0.0

        coefficientList = array(coefficientList)
        return coefficientList

    def coefficient_array_center_line(self, beamArrayObj):
        # create a coefficient array where each row is simply the row of coefficients for each beam in the
        # beam array
        coefficientArray = vstack(tuple(self.coefficient_list_center_line(beamObj) for beamObj in
                                        beamArrayObj.beamArray))

        return coefficientArray


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


initialImage = Image.open('CT_image_megaman.jpg')
beamArray = beam_array_parallel(90, 1, 1, 0)

CT = CAT_Scanner(initialImage, beamArray, True)
CT.scan(100)
reconstructedImage = CT.reconstruct_image(6)
reconstructedImage.save('CT_image_megaman_new.jpg')

