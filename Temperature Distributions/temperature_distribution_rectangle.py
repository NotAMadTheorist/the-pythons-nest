
# Temperature Distribution of  Rectangular Region specified Temperatures along each side
from math import floor
from numpy import array, zeros, linspace, vectorize, uint8, matmul
from random import choice
from PIL import Image

class temp_distribution_rectangle:
    def __init__(self, width, height, temp_up, temp_left, temp_down, temp_right):
        """Setup information about the rectangle such as width, height, and boundary temperatures"""
        # Note that the unknown cells are in the rectangle with corners (1, 1) and (NX, NY)
        # All other cells in the grid have constant boundary temperatures

        self.NX = width
        self.NY = height
        self.TU = temp_up
        self.TL = temp_left
        self.TD = temp_down
        self.TR = temp_right
        self.directions = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def random_direction(self):
        """returns one of the four directions on the plane"""
        return choice(self.directions)

    def give_temperature(self, x, y):
        """returns a set edge temperature if (x, y) is at an edge; otherwise, it returns None"""
        if x == 0:
            return self.TL

        elif x == self.NX+1:
            return self.TR

        elif y == 0:
            return self.TU

        elif y == self.NY+1:
            return self.TD

        else:
            return None

    def generate_temp_array(self):
        """creates an (NX+2) x (NY+2) array that has the edge temperatures at each of the four edges of the
        array and zeroes everywhere else"""

        tempArr = zeros((self.NY+2, self.NX+2))
        for i in range(self.NX+2):
            tempArr[0][i] = self.TU
            tempArr[-1][i] = self.TD

        for i in range(self.NY+2):
            tempArr[i][0] = self.TL
            tempArr[i][-1] = self.TR

        return tempArr

    def generate_temp_distribution_random_walk(self, iterations):
        '''Generate the temperature distribution for the rectangle using a Monte Carlo random walk.'''

        # for each iteration, loop over each cell and perform a random walk
        tempSumArr = self.generate_temp_array()
        for i in range(iterations):
            for x0 in range(1, self.NX+1):
                for y0 in range(1, self.NY+1):
                    initialCell = (x0, y0)

                    # generate random walk until it hits the edge of the rectangle
                    x, y = initialCell
                    edgeTemp = None
                    while True:
                        direction = self.random_direction()
                        x += direction[0]
                        y += direction[1]
                        edgeTemp = self.give_temperature(x, y)
                        if type(edgeTemp) != type(None):
                            break

                    # for the initial cell, update n and the temperature sum
                    tempSumArr[y0][x0] += edgeTemp

        # compute temperature = sum of temperatures / n
        tempArr = self.generate_temp_array()
        for x in range(1, self.NX+1):
            for y in range(1, self.NY+1):
                tempArr[y][x] = tempSumArr[y][x] / iterations

        return tempArr

    def generate_jacobi_iterator(self, returnMandB:bool = False):
        """generate a function T(n+1) = (M*T(n) + B)/4 for generating the temperature distribution of the rectangle
        using the Jacobi Iteration method;
        M is a matrix containing information on cells with unknown temperatures adjacent to a selected cell, and
        B is a vector containing information on boundary temperatures adjacent to the selected cell"""

        matrixM = []
        emptyRow = [0]*self.NX*self.NY
        vectorB = []

        indexOfPixel = lambda x, y: (y-1)*self.NX + (x-1)

        for y in range(1, self.NY+1):
            for x in range(1, self.NX+1):
                adjacentPixels = [(x + x0, y + y0) for x0, y0 in self.directions]

                edgeTemps = []
                unknownIndices = []
                for a, b in adjacentPixels:
                    edgeTemp = self.give_temperature(a, b)
                    if type(edgeTemp) == type(None):
                        unknownIndices.append(indexOfPixel(a, b))
                    else:
                        edgeTemps.append(edgeTemp)

                constantB = sum(edgeTemps)
                vectorB.append(constantB)

                rowM = emptyRow.copy()
                for i in unknownIndices:
                    rowM[i] = 1
                matrixM.append(rowM)

        matrixM = array(matrixM)
        vectorB = array(vectorB)

        func = lambda vectorT: (matmul(matrixM, vectorT) + vectorB)/4

        if returnMandB:
            return func, matrixM, vectorB
        else:
            return func




        # for each cell, get the four cells adjacent to it
        # test self.give_temperature - if it gives a number that cell becomes a constant to sum in B
        # otherwise, add to the matrix M

    def generate_temp_distribution_jacobi(self, iterations):
        """generate a temperature distribution using the Jacobi Iteration method using the following formula:
                T(n+1) = (M*T(n) + B)/4
                T is a vector containing the approximate temperatures of each cell
                M is a matrix containing information on cells with unknown temperatures adjacent to a selected cell, and
                B is a vector containing information on boundary temperatures adjacent to the selected cell"""

        vectorT = array([0]*self.NX*self.NY)
        iterator = self.generate_jacobi_iterator()
        for i in range(iterations):
            vectorT = iterator(vectorT)

        vectorT = vectorT.reshape((self.NY, self.NX))

        return vectorT


class gradient:
    """a class which can translate percentages to color values that correspond to a linear gradient"""

    def __init__(self, *RGBColors):
        """create a gradient by specifying certain colors (RGB triples) that are evenly spaced in the gradient"""
        self.RGBColors = tuple(array(color) for color in RGBColors)
        self.numberOfColors = len(RGBColors)
        self.percentageLimits = tuple(linspace(0, 1, self.numberOfColors))

    def percentColor(self, percentage):
        """converts a percentage (a float 0 to 1) to an RGB triple corresponding to a color in the gradient"""

        if not (0 <= percentage <= 1):
            raise Exception("expected percentage to be from 0 to 1")

        index = 1
        for i in range(1, self.numberOfColors):
            index = i
            if percentage <= self.percentageLimits[i]:
                break

        lowerColor, upperColor = self.RGBColors[index - 1], self.RGBColors[index]
        lowerPercent, upperPercent = self.percentageLimits[index - 1], self.percentageLimits[index]
        miniPercentage = (percentage - lowerPercent) / (upperPercent - lowerPercent)

        blendedColor = vectorize(floor)((1-miniPercentage)*lowerColor + miniPercentage*upperColor)

        return blendedColor


def arrayToColorArray(originalArr, gradientObj):
    """converts a two-dimensional array into an array of RGB triples according to a range determined by the
    minimum and maximum values of the array and the specified gradient"""

    flatArr = originalArr.flatten()
    minX, maxX = min(flatArr), max(flatArr)

    percentArr = (originalArr - minX) / (maxX - minX)
    colorFunc = lambda percent: gradientObj.percentColor(percent)

    colorArr = []
    for i in range(percentArr.shape[0]):
        colorArr.append([])
        for j in range(percentArr.shape[1]):
            colorArr[i].append(colorFunc(percentArr[i][j]))
    colorArr = array(colorArr, dtype=uint8)

    return colorArr


R = temp_distribution_rectangle(40, 40, 5, 0, 20, 10)
Rdist = R.generate_temp_distribution_jacobi(1000)

grayscaleGradient = gradient((0, 0, 0), (255, 255, 255))
thermalGradient = gradient((0, 0, 0), (56, 36, 123), (121, 44, 138), (190, 39, 132), (232, 81, 72),
                           (238, 125, 31), (249, 176, 12), (255, 229, 60), (255, 255, 255))

Rcolors = arrayToColorArray(Rdist, thermalGradient)
Rimage = Image.fromarray(Rcolors)
Rimage.show()
Rimage.save("temperature_distribution.png")

print(Rdist)








