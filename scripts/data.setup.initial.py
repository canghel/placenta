# load photo and tracing files
# crop to only have the placenta area
# make tracing bw 

### PREAMBLE ##################################################################

import numpy as np
import cv2
import os
# confused why the top thing doesn't import listdir?
from os import listdir
from os.path import isfile, join
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

# load photo and tracing files
# crop to only have the placenta area
# make tracing bw 
### CROP FILES ################################################################

# load one file
jj = 1;

#for jj in range(0, numFiles-1):
    
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

# crop
photoImagePath = os.path.join(pathPhotos, photoFiles[jj])
photoImage = cv2.imread(photoImagePath)

plt.imshow(photoImage)
plt.xticks([]), plt.yticks([])
plt.show()

img = cv2.imread(photoImagePath, cv2.IMREAD_GRAYSCALE)
idx = 0 # The index of the contour that surrounds your object
mask = np.zeros_like(img) # Create mask where white is what we want, black otherwise
cv2.drawContours(mask, contours, idx, 255, -1) # Draw filled contour in mask
out = np.zeros_like(photoImage) # Extract out the object and place into output image
out = [255, 255, 255]
# note to self: have to change each of the RGB values

# Show the output image
cv2.imshow('Output', out)
cv2.waitKey(0)
cv2.destroyAllWindows()



# # make outside of the placenta contour completely white
# # from https://stackoverflow.com/questions/37912928/fill-the-outside-of-contours-opencv
# stencil = np.zeros(photoImage.shape).astype(photoImage.dtype)
# # plt.imshow(stencil, 'gray')
# # plt.xticks([]), plt.yticks([])
# # plt.show()
# colorWhite = [255, 255, 225]
# cv2.fillPoly(stencil, contours[1], colorWhite)

# #img = cv2.cvtColor(photoImage.copy(), cv2.COLOR_BGR2GRAY) # change to grayscale
# img = cv2.imread(photoImagePath, cv2.IMREAD_GRAYSCALE)
# thresh = 127
# img_bw = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
# cv2.imwrite('blackwhite.png', img_bw)

# plt.imshow(img_bw)
# plt.xticks([]), plt.yticks([])
# plt.show()

# idx = 0 # The index of the contour that surrounds your object
# mask = np.zeros_like(img_bw) # Create mask where white is what we want, black otherwise
# cv2.drawContours(mask, contours, idx, 255, -1) # Draw filled contour in mask

# out = np.zeros_like(img_bw) # Extract out the object and place into output image
# out[mask == 255] = img_bw[mask == 255]
# plt.imshow(out)
# plt.xticks([]), plt.yticks([])
# plt.show()
# # Show the output image
# # cv2.imshow('Output', out)
# # cv2.waitKey(0)
# # cv2.destroyAllWindows()


# # plt.imshow(stencil, 'gray')
# # plt.xticks([]), plt.yticks([])
# # plt.show()
# result = cv2.bitwise_and(photoImage, mask)
# # cv2.imwrite("result.jpg", result)

# plt.imshow(result)
# plt.xticks([]), plt.yticks([])
# plt.show()

#croppedPhoto = photoImage[y:y+h,x:x+w];
#cv2.imwrite(os.path.join(pathPhotos,filenameStem+'-cropped.png'), croppedPhoto)

#tempImg, contours2, hierarchy = cv2.findContours(traceBW.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#gray = cv2.bilateralFilter(tempImg, 10, 10, 20)
#croppedTrace = cv2.drawContours(gray, [contours2[0]], -1, (0, 255, 0), 10)
#croppedTrace = croppedTrace[y:y+h,x:x+w];
#cv2.imwrite(os.path.join(pathTraces,filenameStem+'-cropped.png'), croppedTrace)