from computed_tomography.cls_beam import *
from numpy import linspace

class beam_array_parallel:
    """A class representing a beam array that is rotated around an image in a parallel-mode CT scan.
    Here, beams are aimed in the same direction but originate from different points along the circumcircle of the
    image to be scanned."""

    def __init__(self, numberOfBeams, spreadAngle, beamWidth, centralAngle = 0):
        """Create a parallel-mode beam array given a number of beams, the spread angle for the beams' positions, and
        a beam width (1 unit = 1 pixel)."""

        self.numberOfBeams = numberOfBeams
        self.beamWidth = beamWidth
        self.centralAngle = centralAngle
        self.spreadAngle = spreadAngle
        translationAngles = linspace(-spreadAngle/2, spreadAngle/2, numberOfBeams)

        # create the beam objects
        self.beamArray = [beam(centralAngle, T, 0, beamWidth) for T in translationAngles]

    def set_central_angle(self, newAngle):
        """Change the central angle of the beam array; corresponds to rotating the beam array"""

        self.centralAngle = newAngle
        for bm in self.beamArray:
            bm.set_central_angle(newAngle)

    def __repr__(self):
        return f"beam_array_parallel(numberOfBeams={self.numberOfBeams}," \
               f"                    spreadAngle={self.spreadAngle}," \
               f"                    beamWidth={self.beamWidth}," \
               f"                    centralAngle={self.centralAngle}"