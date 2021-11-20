from temperature_distributions.cls_gradient import gradient

grayscaleGradient = gradient((0, 0, 0), (255, 255, 255))
thermalGradient = gradient((0, 0, 0), (56, 36, 123), (121, 44, 138), (190, 39, 132), (232, 81, 72),
                           (238, 125, 31), (249, 176, 12), (255, 229, 60), (255, 255, 255))