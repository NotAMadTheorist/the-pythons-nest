class beam:
    """A class representing the X-ray beams that are used to scan the object"""

    def __init__(self, centralAngle, translationAngle, inclination, beamWidth):
        """Create an X-ray beam with a specified width (1 unit = 1 pixel) and angular position and whose point of
        origin is positioned along the circumcircle of the image.

        Angles used to position the beam are measured in degrees and the positive direction goes clockwise.

        List of Angles:
         - Central Angle -- the middle angle relative to the beam array; is 0 degrees if the beam array is positioned
         directly to the left of the center of the image
         - Translation Angle -- angle between central angle and the radius to the point of origin for the beam
         - Inclination -- direction of the beam relative to the central angle; is 0 degrees if the beam is parallel
         to the central angle of its respective beam array"""

        self.centralAngle = centralAngle
        self.translationAngle = translationAngle
        self.inclination = inclination
        self.beamWidth = beamWidth
        self.set_angle()

    def set_angle(self):
        """Update the beam's overall angle and inclination relative to the center of the image, rather than the beam
        array which the beam belongs to."""

        self.overallAngle = self.centralAngle + self.translationAngle
        self.overallInclination = self.centralAngle + self.inclination

    def set_central_angle(self, newAngle):
        """Change the central angle of the beam; used whenever the beam array is rotated around the image."""

        self.centralAngle = newAngle
        self.set_angle()

    def __repr__(self):
        return f"beam(centralAngle = {self.centralAngle:.1f}" \
               f"     translationAngle = {self.translationAngle:.1f}" \
               f"     inclination = {self.inclination:.1f}" \
               f"     beamWidth = {self.beamWidth:.2f})"