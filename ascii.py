import os
import sys
import time
import cv2 # type: ignore
import numpy as np # type: ignore
ansi = '\x1b['

HEIGHT = input('Height: ')
WIDTH = input('Width: ')
if not HEIGHT:
    HEIGHT = 40
else:
    HEIGHT = int(HEIGHT)
if not WIDTH:
    WIDTH = 65
else:
    WIDTH = int(WIDTH)

palettes = [
    ' .#',
    ' .:-=+*#%@',
    '  .,_-+=:;|/([?rxuvtfjaomwqpdbWM#&%@'
]
pal = palettes[2]

dirpath = os.path.dirname(__file__)
cwd = os.getcwd()
imgpath = ''
try:
    imgpath = os.path.join(cwd, sys.argv[1])
except:
    print('python ascii.py [path]')
    sys.exit()

if not os.path.exists(imgpath):
    print('Invalid path')
    sys.exit()

img = cv2.imread(imgpath)
cap = cv2.VideoCapture(imgpath)

def map(a, b, offset=0):
    return ( (1/b) * a ) + offset 

def img2txt(image, palette=pal):
    out = ''#*HEIGHT*2

    for y in range(HEIGHT):
        for x in range(WIDTH):
            #print(x, len(image[y]))

            px = image[y][x]

            value = map(np.average(px), 255)

            chari = int(value * (len(palette)-1))
            out += palette[chari]

        out += '\n'

    return out

if not img is None:
    img = cv2.resize(img, (WIDTH, HEIGHT), interpolation= cv2.INTER_CUBIC)
    print(img2txt(img))
    sys.exit()
elif cap is None:
    print('Invalid file')
    sys.exit()

frameList = []
maxfps = 16
fps = cap.get(cv2.CAP_PROP_FPS)
skipFrame = 0
if fps > maxfps:
    skipFrame = np.ceil(fps/maxfps)
    fps = maxfps
    print(skipFrame, '      aa')
spf = 1/fps

fi = 0

while cap and cap.isOpened():
    ret, frame = cap.read()

    if skipFrame > 0 and not fi % skipFrame == 0:
        print('skipped ' + str(fi), end='\r')
        fi += 1
        continue
    if not ret:
        cap.release()
        break

    frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation= cv2.INTER_CUBIC)
    frameList.append(frame)
    fi += 1

#print(HEIGHT, len(frameList[0]))

fi = 0
for f in frameList:
    #if fi >= 10000:
    #    frameList = frameList[:fi-1]
    #    break
    frameList[fi] = img2txt(f)
    print(f'Processed {fi}       ', end='\r')
    fi+= 1

init = True
loop = True
if '.gif' in imgpath:
    loop = True

while loop or init:
    init = False
    for f in frameList:
        print(f, end='\r')
        time.sleep(spf)
        #sys.stdout.write(f'{ansi}{HEIGHT-1}A')
