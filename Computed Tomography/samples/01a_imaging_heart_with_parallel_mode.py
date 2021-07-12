from computed_tomography import *
from PIL import Image

# open the image of a heart emoji (16 px x 15 px)
myHeart = Image.open("CT_images_before/heart.jpg")

# setup a parallel beam array with 60 beams, each with a width of 1 pixel, spread over 60 degrees around the center
# of the image
beamArray = beam_array_parallel(numberOfBeams=60,
                                spreadAngle=60,
                                beamWidth=1)

# setup the CAT Scanner and connect it to the heart image and the beam array
CT = CAT_Scanner(imageObj=myHeart,
                 beamArray=beamArray,
                 doConvertToGrayscale= True)

# scan the heart image by rotating the beam array in 100 evenly spaced directions circling the image
# since we have 60 beams, we will have a total of 60*100 = 6,000 beams to analyze
CT.scan(numberOfDirections=100)

# reconstruct a grayscale map of the image by applying an iterative projection algorithm 6 times
# this is the step that will always take the longest time
scannedHeart = CT.reconstruct_image(iterations=6)

# the time required to reconstruct the image scales with the number of pixels in the image, the number of beams,
# and the number of directions by which the image is scanned

# save the image
scannedHeart.save("CT_images_after/heart_new.jpg")