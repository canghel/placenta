# skeletonize
import os
from os import listdir
from os.path import isfile, join
from skimage.morphology import skeletonize, thin, medial_axis

from skimage import draw
from skimage.io import imread, imshow, imsave
from skimage.color import rgb2gray
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.cm as cm

pathColoredTraces = "./traces/colored-traces"
pathSkeletons = "./skeletons"
traceFiles = [f for f in listdir(pathColoredTraces) if isfile(join(pathColoredTraces, f))]
numFiles = len(traceFiles);

# load one file
for jj in range(0, numFiles-1):
    # jj = 0

    print('--- Working on file '+str(jj+1)+' --------------------------------')
    filenameStem = traceFiles[jj]
    filenameStem = filenameStem.split('.')[0]
    print(filenameStem)

    # # load a tracing
    traceImagePath = os.path.join(pathColoredTraces, traceFiles[jj])
    # load image from file
    # img_fname=os.path.join('images','mall1_2F_schema.png') 
    image=imread(traceImagePath)

    # # Change RGB color to gray 
    image=rgb2gray(image)
    # imsave('traceImg.png', image)

    out = abs(image*1-1);
    # imsave('outImg.png', out)

    out=np.where(out>np.mean(out),1.0,0.0)

    # imsave('outImg.png', out)
    # Change gray image to binary
    # out=np.where(out>np.mean(image),1.0,0.0)

    # imsave('out.png', image)

    # # Change gray image to binary
    # image=np.where(image<230,1.0,0.0)

    # image
    # # perform skeletonization
    # skeleton = skeletonize(out)

    skeleton = skeletonize(out)
    #skeletonmed = medial_axis(out)
    #thinned = thin(out)
    #thinned_partial = thin(out, max_iter=10)

    # skeleton = abs(skeleton*1-1);

    # plt.imshow(skeleton)
    # plt.xticks([]), plt.yticks([])
    # plt.show()

    # plt.imshow(thinned_partial)
    # plt.xticks([]), plt.yticks([])
    # plt.show()

    pathSkeletons

    skeletonPath = os.path.join(pathSkeletons, filenameStem+'.png')

    plt.imsave(skeletonPath, abs(skeleton-1), cmap=cm.gray)