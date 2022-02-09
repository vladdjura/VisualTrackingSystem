import numpy as np
import sys
import pandas as pd
import cv2


# show image    
def show(img):
    try:
        cv2.imshow('frame', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except:
        raise ValueError("ValueError exception thrown")

        
# save image
def save(path, img):
    cv2.imwrite(path, img)

    
# draw vertical and horizontal lines for creating parking mask
def liner(x_, y_, w_, h_, img, color = 'b', size = 6):
    colors = {
        'b' : (255, 0, 0),
        'g' : (0, 255, 0),
        'r' : (0, 0, 255)
    }
    color = colors[color]
    return cv2.line(img, (x_,y_), (w_, h_), color, size)



# transforms image into black & white
def gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray


space_nums = [(1, 995, 760, 3, 4),(3, 1140, 760, 3, 4),(5, 838, 760, 3, 4),(7, 1284, 760, 3, 4), (9, 700, 760, 3, 4),
              (2, 1018, 350, 1, 4),(4, 1110, 350, 1, 4),(6, 924, 350, 1, 4),(8, 1194, 350, 1, 4), (10, 826, 350, 1, 4),
              (11, 1390, 760, 3, 4), (13, 540, 760, 3, 4), (14, 744, 350, 1, 4), (12, 1260, 350, 1, 4)]


# draw numbers on spaces
def space_ids(img, space_nums=space_nums):
    for space in space_nums:
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (space[1], space[2])
        fontScale = space[3]
        color = (0, 0, 255)
        thickness = space[4]
        img = cv2.putText(img, str(space[0]), org, font, 
                           fontScale, color, thickness, cv2.LINE_AA)
   

paths = ['C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)Video1.mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)Video_2.mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)moving 0007.mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0010 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0025 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0031 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0035 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0040 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0043 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0045 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0048 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0049 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0059 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0060 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0058 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0065 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0066 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0068 (Converted).mov',
         'C:/Users/Vladislav/Desktop/Videos/12_2_2021 10_01_42 AM (UTC-05_00)_0069 (Converted).mov',
         ]



