

class temp_distribution_image:
    def __init__(self, targetImage, boundaryTemperatures:list, boundaryColor=(255, 0, 0), cellColor=(0, 0, 0)):
        """Setup the temperature distribution given a target image object containing a map of the area and a list of
        boundary temperatures for every region in the image with color boundaryColor. The default boundary color
        is pure red (RGB = 255, 0, 0) and the default cell color is pure black (RGB = 0, 0, 0)."""

        self.targetImage = targetImage
        self.boundaryTemperatures = boundaryTemperatures
        self.boundaryColor = boundaryColor
        self.cellColor = cellColor


# pixels