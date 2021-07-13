
# Temperature Distribution of  Rectangular Region specified Temperatures along each side
from temperature_distributions import *
from PIL import Image
from time import time

R = temp_distribution_rectangle(width=40,
                                height=40,
                                temp_up=5,
                                temp_left=0,
                                temp_down=20,
                                temp_right=10)

t1 = time()
Rdist = R.generate_temp_distribution_jacobi(1000)
t2 = time()
timeElapsed = t2 - t1
print(f"Time taken to generate distribution: {timeElapsed:.2f} s")

Rcolors = array_to_color_array(Rdist, thermalGradient)
Rimage = Image.fromarray(Rcolors)
Rimage.save("output_images/01_square_region.png")








