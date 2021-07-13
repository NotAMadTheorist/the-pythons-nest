from numpy import array, linspace, vectorize
from math import floor

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