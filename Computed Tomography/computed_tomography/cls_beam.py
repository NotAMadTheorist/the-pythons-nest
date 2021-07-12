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