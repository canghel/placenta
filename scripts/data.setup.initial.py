# load photo and tracing files
# crop to only have the placenta area
# make tracing bw 

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
filenameStem = traceFiles[jj]
filenameStem = filenameStem.split('.')[0]
print(filenameStem)

# load a tracing
traceImagePath = os.path.join(pathTraces, traceFiles[jj])
traceImage = cv2.imread(traceImagePath)

# process tracing to get an image of the edges
traceBW = cv2.cvtColor(traceImage, cv2.COLOR_BGR2GRAY) # change to grayscale

# grrr erase the perimeter here!
traceColored = cv2.imread(traceImagePath)

blur_radius = 1.0
threshold = 50
# smooth the image (to remove small objects)
imgf = scipy.ndimage.gaussian_filter(tempImg3, blur_radius)
threshold = 50

# find connected components
labeled, nr_objects = scipy.ndimage.label(imgf > threshold) 
print("Number of objects is %d " % nr_objects)

plt.imsave('./out.png', labeled)
plt.imshow(labeled)

np.unique(labeled)

# ret,traceBW = cv2.threshold(traceBW,250,255,cv2.THRESH_BINARY)
# gray = cv2.bilateralFilter(traceBW, 10, 10, 20)
# edged = cv2.Canny(gray, 30, 200)

# plt.imshow(traceBW, 'gray')
# plt.xticks([]), plt.yticks([])
# plt.show()

# # get contours of the edges
# tempImg, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# contours = sorted(contours, key = cv2.contourArea, reverse = True)
# cnt = contours[0]

# # find bounding rectange
# x,y,w,h = cv2.boundingRect(cnt)

# # crop
# photoImagePath = os.path.join(pathPhotos, photoFiles[jj])
# photoImage = cv2.imread(photoImagePath)

# ### MAKE EVERYTHING OUTSIDE THE PLACENTA BLACK ############################

# img = cv2.imread(photoImagePath,0) # read the image in grayscale
# print(img.shape)

# idx = 1 # The index of the contour that surrounds your object
# mask = np.zeros_like(img) # Create mask where white is what we want, black otherwise
# print(mask.shape)
# cv2.drawContours(mask, contours, idx, 255, -1) # Draw filled contour in mask

# # a little hack to get the region inside the contour coloured black
# # and the outside coloured white
# # just having the option +1 instead of -1 in drawContours doesn't work
# # as then it's the contour *line* that is white
# mask[mask==0] = 3;
# mask[mask==255] = 0;
# mask[mask==3] = 255;

# # cv2.imwrite("mask.png", mask)

# # make the outside of the photo be white
# img = photoImage.copy()
# out = np.ones_like(img)*255 
# out[:,:,0][mask==0]=img[:,:,0][mask==0]
# out[:,:,1][mask==0]=img[:,:,1][mask==0]
# out[:,:,2][mask==0]=img[:,:,2][mask==0]

# # cv2.imwrite("out.png", out)

# # crop around the placenta
# croppedPhoto = out[y:y+h,x:x+w];
# cv2.imwrite(os.path.join(pathPhotos,filenameStem+'-cropped.png'), croppedPhoto)

# tempImg2, contours2, hierarchy = cv2.findContours(traceBW.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# gray = cv2.bilateralFilter(tempImg2, 10, 10, 20)
# print(gray.shape)
# out = np.ones_like(gray)*255 
# out[mask==0]=gray[mask == 0]
# croppedTrace = cv2.drawContours(out, [contours2[0]], -1, (0, 255, 0), 10)

# # find contours of the cropped trace
# tempImg3, contours3, hierarchy = cv2.findContours(croppedTrace ,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# mask3 = np.zeros_like(croppedTrace) # Create mask where white is what we want, black otherwise
# cv2.drawContours(mask3, contours3, 1, 255, 10)

# mask4 = np.zeros_like(croppedTrace) # Create mask where white is what we want, black otherwise
# cv2.drawContours(mask4, contours3, 1, 255, -10)

# #mask2 = cv2.drawContours(tempImg3, contours, 0, 225, 1) # Draw filled contour in mask
# # a little hack to get the region inside the contour coloured black
# # and the outside coloured white
# # just having the option +1 instead of -1 in drawContours doesn't work
# # as then it's the contour *line* that is white
# mask3[mask3==0] = 3;
# mask3[mask3==255] = 100;
# mask3[mask3==3] = 255;
# # cv2.imwrite('./mask3.png', mask3)

# mask4[mask4==0] = 3;
# mask4[mask4==255] = 100;
# mask4[mask4==3] = 255;
# # cv2.imwrite('./mask4.png', mask4)

# out = np.ones_like(croppedTrace)*255
# croppedTrace[mask4==0]=croppedTrace[mask4 == 0]
# croppedTrace2 = cv2.drawContours(croppedTrace, [contours3[0]], -1, (0, 255, 0))
# croppedTrace2[mask3==100] = 255;
# # cv2.imwrite("trace-bw-3.png", croppedTrace2);
# croppedTrace2 = croppedTrace2[y:y+h,x:x+w];
# cv2.imwrite(os.path.join(pathTraces,filenameStem+'-cropped.png'), croppedTrace2)

#     # tempImg3, contours3, hierarchy = cv2.findContours(croppedTrace ,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     # blur_radius = 1.0
#     # threshold = 50
#     # # smooth the image (to remove small objects)
#     # imgf = scipy.ndimage.gaussian_filter(tempImg3, blur_radius)
#     # threshold = 50

#     # # find connected components
#     # labeled, nr_objects = scipy.ndimage.label(imgf > threshold) 
#     # print("Number of objects is %d " % nr_objects)

#     # plt.imsave('./out.png', labeled)
#     # plt.imshow(labeled)

#     # np.unique(labeled)

#     # drop from bounding box?

#     # cv2.imwrite(os.path.join(pathTraces,filenameStem+'-cropped.png'), croppedTrace)

# # load a skeleton
# skelImagePath = os.path.join(pathSkeletons, traceFiles[jj])
# skelImage = cv2.imread(skelImagePath)
# croppedSkeleton = skelImage[y:y+h,x:x+w];
# cv2.imwrite(os.path.join(pathSkeletons,filenameStem+'-cropped.png'), croppedSkeleton)