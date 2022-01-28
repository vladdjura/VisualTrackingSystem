import numpy as np
import sys
import pandas as pd
import cv2

def frameByFrame(img):
    cv2.imshow('frame', img)
    cv2.waitKey(25)
    cv2.destroyAllWindows()

# show image    
def show(img):
    cv2.imshow('frame', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
# draw vertical and horizontal lines for creating parking mask
def liner(x_, y_, w_, h_, img, color = 'b', size = 6):
    colors = {
        'b' : (255, 0, 0),
        'g' : (0, 255, 0),
        'r' : (0, 0, 255)
    }
    color = colors[color]
    return cv2.line(img, (x_,y_), (w_, h_), color, size)

# returns parking space as numpy array
def extractor(img):
    pixels = []
    rows, cols, _ = img.shape
    switch = 0
    for row in range(rows):
        for col in range(cols):
            pixel = img[row,col]
            if (pixel == np.array([0,255, 0])).all():
                switch+=1
            elif switch == 1:
                pixels.append(pixel)
        switch = 0
    return np.array(pixels)

# transforms image into black & white
def gray(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray

space_nums = [(1, 985, 760, 3, 4),(3, 1140, 760, 3, 4),(5, 830, 760, 3, 4)]

# draw numbers on spaces
def space_ids(img, space_nums):
    for space in space_nums:
        font = cv2.FONT_HERSHEY_SIMPLEX
        org = (space[1], space[2])
        fontScale = space[3]
        color = (0, 0, 255)
        thickness = space[4]
        img = cv2.putText(img, str(space[0]), org, font, 
                           fontScale, color, thickness, cv2.LINE_AA)
   

paths = ['C:\\Users\\Vladislav\\Desktop\\12_2_2021 10_01_42 AM (UTC-05_00)Video1.mov',
         'C:\\Users\\Vladislav\\Desktop\\12_2_2021 10_01_42 AM (UTC-05_00)Video_2.mov',
         'C:\\Users\\Vladislav\\Desktop\\12_2_2021 10_01_42 AM (UTC-05_00)moving 0007.mov'
         ''
         ]

# returns 
def qualifier(space_num = 1):
    space = img[mask == space_num]
    if np.var(space) > 1000:
        print('Space is occupied')
    else:
        print('Parking space is unoccupied')

        
# create mask for given parking space        
def masker(mask, img, frame, space_number = 1, park_row = 0):
    rows = [range(590,860), range(278,390)][park_row]
    cols = img.shape[1]

    for row in rows:
        color = 'mixed'
        switch = 0
        for col in range(cols):
            if switch == 2:
                mask[row,col] = 1
            if np.array_equal(frame[row][col], np.array([0,255,0])):
                state = 'green'
            else:
                state = 'mixed'
            if state != color:
                switch += 1
                color = state
            if switch == 3:
                break
    return mask

