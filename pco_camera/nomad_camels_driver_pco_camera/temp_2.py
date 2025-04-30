import matplotlib.pyplot as plt
import pco

with pco.Camera() as cam:
    cam.record(mode="sequence")
    cam.exposure_time = 0.1
    print(cam.configuration)
    image, meta = cam.image()

    plt.imshow(image, cmap='gray')
    plt.show()