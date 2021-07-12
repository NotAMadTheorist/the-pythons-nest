from computed_tomography.cls_beam import *
from numpy import linspace

class beam_array_fan_mode:
    def __init__(self, numberOfBeams, spreadAngle, beamWidth, centralAngle = 0):
        self.numberOfBeams = numberOfBeams
        self.beamWidth = beamWidth
        self.centralAngle = centralAngle
        inclinationAngles = linspace(-spreadAngle / 2, spreadAngle / 2, numberOfBeams)

        # create the beam objects
        self.beamArray = [beam(centralAngle, 0, I, beamWidth) for I in inclinationAngles]

    def set_central_angle(self, newAngle):
        self.centralAngle = newAngle
        for bm in self.beamArray:
            bm.set_central_angle(newAngle)