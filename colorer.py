import cv2
import numpy as np

image = cv2.imread('C:/Users/Vladislav/Desktop/rit-paw-crop.png', -1)

rows, cols, _ = image.shape
print(rows,cols)
cells = rows*cols
# reshaping image from 3d to 2d (one row with RGB pixels)
pixels = np.reshape(image, (cells, -1))
# unique colors, index of their first appearance, frequency
color, index, count = np.unique(pixels, axis = 0, return_counts = True, return_index = True)

for i in color:
    print(i)