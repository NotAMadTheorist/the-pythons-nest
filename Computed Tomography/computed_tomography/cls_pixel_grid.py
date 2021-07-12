from math import sqrt, sin, cos, tan, radians, floor
from numpy import array, vstack

class pixel_grid:
    def __init__(self, imageWidth:int, imageHeight:int):
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