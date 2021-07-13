from random import choice
from numpy import zeros, array, matmul

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
