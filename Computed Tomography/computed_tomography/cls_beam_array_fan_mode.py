from computed_tomography.cls_beam import *
from numpy import linspace

class beam_array_fan_mode:
    """A class representing a beam array that is rotated around an image in a fan-mode CT scan.
    Here, beams originate from the same point but are aimed at different angles."""

    def __init__(self, numberOfBeams, spreadAngle, beamWidth, centralAngle = 0):
        """Create a fan-mode beam array given a number of beams, the spread angle for the beams' directions, and
        a beam width (1 unit = 1 pixel)."""

        self.numberOfBeams = numberOfBeams
        self.beamWidth = beamWidth
        self.centralAngle = centralAngle
        self.spreadAngle = spreadAngle
        inclinationAngles = linspace(-spreadAngle / 2, spreadAngle / 2, numberOfBeams)

        # create the beam objects
        self.beamArray = [beam(centralAngle, 0, I, beamWidth) for I in inclinationAngles]

    def set_central_angle(self, newAngle):
        """Change the central angle of the beam array; corresponds to rotating the beam array"""

        self.centralAngle = newAngle
        for bm in self.beamArray:
            bm.set_central_angle(newAngle)

    def __repr__(self):
        return f"beam_array_fan_mode(numberOfBeams={self.numberOfBeams}," \
               f"                    spreadAngle={self.spreadAngle}," \
               f"                    beamWidth={self.beamWidth}," \
               f"                    centralAngle={self.centralAngle}"