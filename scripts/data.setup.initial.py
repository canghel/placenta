### PREAMBLE ##################################################################

import numpy as np
import cv2
import os
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt
import scipy.ndimage

### PATHS #####################################################################

pathPhotos = "./photos"
pathTraces = "./traces"
pathSkeletons = "./skeletons"

### GET NAMES OF FILES ########################################################

traceFiles = [f for f in listdir(pathTraces) if isfile(join(pathTraces, f))]
photoFiles = [f for f in listdir(pathPhotos) if isfile(join(pathPhotos, f))]
skelFiles =  [f for f in listdir(pathSkeletons) if isfile(join(pathSkeletons, f))]

numFiles = len(photoFiles);

# load photo and tracing files
# crop to only have the placenta area
# make tracing bw 
### CROP FILES ################################################################

# load one file
# for jj in range(0, numFiles):
jj = 0
print('--- Working on file '+str(jj+1)+' --------------------------------')
#filenameStem = traceFiles[jj]
#filenameStem = filenameStem.split('.')[0]
# print(filenameStem)

# load a tracing
#traceImagePath = os.path.join(pathTraces, traceFiles[jj])
traceImagePath = './T000-BN0013990_fetalsurface_fixed_ruler_lights_filter_12_0130-dd.png'
traceImage = cv2.imread(traceImagePath)

# the perimeter indices have rgb code (0, 255, 0)
perimIndices = np.where(np.all(traceImage == [0, 255, 0], axis=-1))
coords = np.column_stack((perimIndices[1], perimIndices[0]))

mask = np.zeros((traceImage.shape[0], traceImage.shape[1]))
cv2.fillConvexPoly(mask, coords, 1)
#mask = mask.astype(np.bool)
plt.imshow(mask)
plt.xticks([]), plt.yticks([])
plt.show()

cv2.imwrite('maskmaybe1.png', 255*(1-mask));