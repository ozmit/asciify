import os
import sys
import cv2 # type: ignore
import numpy as np # type: ignore

maxHeight = 150
maxWidth = 200
palettes = [
    ' .#',
    ' .:-=+*#%@',
    '  .,_-+=:;|/([?rxuvtfjaomwqpdbWM#&%@'
]


dirpath = os.path.dirname(__file__)
cwd = os.getcwd()
imgpath = ''
try:
    imgpath = os.path.join(cwd, sys.argv[1])
except:
    print('Usage:\npython ascii.py [image path]')
    sys.exit()

if not os.path.exists(imgpath):
    print('Invalid path')
    sys.exit()

img = cv2.imread(imgpath)
height, width, channels = img.shape

def map(a, b, offset=0):
    return ( (1/b) * a ) + offset 

def img2txt(image, palette):
    out = ''

    for y in range(height):
        for x in range(width):
            px = image[y][x]

            value = map(np.average(px), 255)

            chari = int(value * (len(palette)-1))
            out += palette[chari]

        out += '\n'

    return out

if width > maxWidth or height > maxHeight:
    img = cv2.resize(img, (maxWidth, maxHeight), interpolation= cv2.INTER_CUBIC)
    height, width, channels = img.shape

print(img2txt(img, palettes[2]))