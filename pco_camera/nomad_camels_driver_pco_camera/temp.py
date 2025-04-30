import imageio.v3 as imageio
import numpy as np
import os

img = imageio.imread('nomad_camels_driver_pco_camera/Fuji_san_by_amaral.png', mode='F')
img_array = np.array(img)

print(img_array.shape)
print(img_array.min())


current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)

print("Current file path:", current_file_path)
print("Directory containing the file:", current_dir)

print(img_array.dtype, img.dtype)
