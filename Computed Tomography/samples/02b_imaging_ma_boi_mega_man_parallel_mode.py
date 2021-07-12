from computed_tomography import *
from PIL import Image

# Yes, I do not own this character, but come on I really like playing his classic platforming games!

# open the image of Mega Man's sprite (34 px x 40 px)
yeBoi = Image.open("CT_images_before/mega_man.jpg")

# setup a parallel beam array with 90 beams, each with a width of 1 pixel, spread over 30 degrees around the center
# of the image
beamArray = beam_array_parallel(numberOfBeams=90,
                                spreadAngle=30,
                                beamWidth=1)

# setup the CAT Scanner and connect it to the sprite and the beam array
CT = CAT_Scanner(imageObj=yeBoi,
                 beamArray=beamArray,
                 doConvertToGrayscale=True)

# scan the sprite by rotating the beam array in 100 evenly spaced directions circling the image
CT.scan(100)

# reconstruct a grayscale map of the image by applying an iterative projection algorithm 6 times
# this is the step that will always take the longest time
# this will take a while (wait 5 minutes or so)
scannedBoi = CT.reconstruct_image(iterations=6)


# the time required to reconstruct the image scales with the number of pixels in the image, the number of beams,
# and the number of directions by which the image is scanned

# save the image
scannedBoi.save("CT_images_after/mega_man_new2.jpg")
