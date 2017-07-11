# load photo and tracing files
# crop to only have the placenta area
# make tracing bw 

### PREAMBLE ##################################################################

import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
import scipy.ndimage

### PATHS #####################################################################

pathPhotos = "./photos"
pathTraces = "./traces"

### GET NAMES OF FILES ########################################################

traceFiles = [f for f in listdir(pathTraces) if isfile(join(pathTraces, f))]
photoFiles = [f for f in listdir(pathPhotos) if isfile(join(pathPhotos, f))]

numFiles = len(photoFiles);

### CROP FILES ################################################################

# load one file
jj = 1;

for jj in range(0, numFiles-1):
    
    print('--- Working on file '+str(jj+1)+' --------------------------------')
    filenameStem = traceFiles[jj]
    filenameStem = filenameStem.split('.')[0]
    print(filenameStem)

    # load a tracing
    traceImagePath = os.path.join(pathTraces, traceFiles[jj])
    traceImage = cv2.imread(traceImagePath)

    # process tracing to get an image of the edges
    traceBW = cv2.cvtColor(traceImage, cv2.COLOR_BGR2GRAY) # change to grayscale
    ret,traceBW = cv2.threshold(traceBW,250,255,cv2.THRESH_BINARY)
    gray = cv2.bilateralFilter(traceBW, 10, 10, 20)
    edged = cv2.Canny(gray, 30, 200)

    plt.imshow(traceBW, 'gray')
    plt.xticks([]), plt.yticks([])
    plt.show()

    # get contours of the edges
    tempImg, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    cnt = contours[0]

    # find bounding rectange
    x,y,w,h = cv2.boundingRect(cnt)

    # crop contoured trace
    #croppedTrace = edged[y:y+h,x:x+w]
    photoImagePath = os.path.join(pathPhotos, photoFiles[jj])
    photoImage = cv2.imread(photoImagePath)

    croppedPhoto = photoImage[y:y+h,x:x+w];
    cv2.imwrite(os.path.join(pathPhotos,filenameStem+'-cropped.png'), croppedPhoto)

    tempImg, contours2, hierarchy = cv2.findContours(traceBW.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    gray = cv2.bilateralFilter(tempImg, 10, 10, 20)
    croppedTrace = cv2.drawContours(gray, [contours2[0]], -1, (0, 255, 0), 10)
    croppedTrace = croppedTrace[y:y+h,x:x+w];
    cv2.imwrite(os.path.join(pathTraces,filenameStem+'-cropped.png'), croppedTrace)

    # plt.imshow(edged, 'gray')
    # plt.xticks([]), plt.yticks([])
    # plt.show()