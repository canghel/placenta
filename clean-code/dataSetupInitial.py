# Preprocess files:
# - create a white mask around the placenta
# - erase the perimeter from the trace pictures
# - make traces black and white
#
# - !!! NOTE !!! One of the traces, T-BN1273150 does not come out well (inverse
#   black and white) and it has to be processed by and

# Reminder to self:
# 0 = black
# 255 = white

### PREAMBLE ##################################################################

import numpy as np
import cv2
import os
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt
import scipy.ndimage

### PATHS #####################################################################

pathPhotos = "../../../data/photos/raw-photos"
pathTraces = "../../../data/traces/raw-traces"

pathPhotosProcessed = "../../../data/photos/preprocessed"
pathTracesProcessed = "../../../data/traces/preprocessed"

### GET NAMES OF FILES ########################################################

traceFiles = [f for f in listdir(pathTraces) if isfile(join(pathTraces, f))]
photoFiles = [f for f in listdir(pathPhotos) if isfile(join(pathPhotos, f))]

numFiles = len(photoFiles);

### OBTAIN A MASK #############################################################

# load each file
for jj in range(0, numFiles):
    
    print('--- Working on file '+str(jj+1)+' --------------------------------')
    filenameStem = traceFiles[jj]
    filenameStem = filenameStem.split('.')[0]
    print(filenameStem)

    # load a tracing
    traceImagePath = os.path.join(pathTraces, traceFiles[jj])
    traceImage = cv2.imread(traceImagePath)

    # the perimeter indices have rgb code (0, 255, 0)
    perimIndices = np.where(np.all(traceImage == [0, 255, 0], axis=-1))
    coords = np.column_stack((perimIndices[1], perimIndices[0]))

    mask = np.zeros((traceImage.shape[0], traceImage.shape[1]))
    cv2.fillConvexPoly(mask, coords, 1)
    mask = 255*(1-mask)

    # cv2.imwrite('mask1.png', mask);
    perimMask = np.zeros((traceImage.shape[0], traceImage.shape[1]));
    perimMask[perimIndices] = 255;
    perimMask = cv2.threshold(perimMask, 1, 255, cv2.THRESH_BINARY_INV)[1]

    ### COLOUR REGION OUTSIDE IMAGES CONTOUR WHITE ###############################

    # load photo image
    photoImagePath = os.path.join(pathPhotos, photoFiles[jj])
    photoImage = cv2.imread(photoImagePath)

    # make the outside of the photo be white
    img = photoImage.copy()
    photoImageClean = np.ones_like(img)*255 
    photoImageClean[:,:,0][mask==0]=img[:,:,0][mask==0]
    photoImageClean[:,:,1][mask==0]=img[:,:,1][mask==0]
    photoImageClean[:,:,2][mask==0]=img[:,:,2][mask==0]

    # load trace as grayscale
    traceImagePath = os.path.join(pathTraces, traceFiles[jj])
    traceBWImage = cv2.imread(traceImagePath, cv2.IMREAD_GRAYSCALE)
    # obtain the minimum nonzero grayscale value
    grayscaleValues = np.unique(traceBWImage);
    minGrayscaleValue = min(grayscaleValues[1:len(grayscaleValues)]);
    # make trace black and white
    traceBWImage = cv2.threshold(traceBWImage, minGrayscaleValue-1, 255, cv2.THRESH_BINARY_INV)[1]

    # make the outside of the trace white and make trace black and white
    traceImageClean = traceBWImage.copy()
    traceImageClean[perimMask==0]=255;

    ### CROP ###################################################################

    x = min(perimIndices[0]) 
    y = min(perimIndices[1])
    w = max(perimIndices[0])-x
    h = max(perimIndices[1])-y

    # crop
    photoImageCropped = photoImageClean[x:x+w,y:y+h]
    traceImageCropped = traceImageClean[x:x+w,y:y+h]

    ### SAVE ###################################################################

    # write to file
    cv2.imwrite(os.path.join(pathPhotosProcessed, traceFiles[jj]), photoImageCropped);
    cv2.imwrite(os.path.join(pathTracesProcessed, traceFiles[jj]), traceImageCropped);