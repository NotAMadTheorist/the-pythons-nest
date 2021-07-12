from computed_tomography.cls_beam import *
from numpy import linspace

class beam_array_parallel:
    def __init__(self, numberOfBeams, spreadAngle, beamWidth, centralAngle = 0):
        self.numberOfBeams = numberOfBeams
        self.beamWidth = beamWidth
        self.centralAngle = centralAngle
        translationAngles = linspace(-spreadAngle/2, spreadAngle/2, numberOfBeams)

        # create the beam objects
        self.beamArray = [beam(centralAngle, T, 0, beamWidth) for T in translationAngles]

    def set_central_angle(self, newAngle):
        self.centralAngle = newAngle
        for bm in self.beamArray:
            bm.set_central_angle(newAngle)