# mcc coefficient between true and fake B
# Kara already has a Matlab function to do this

### PREAMBLE ##################################################################

from sklearn.metrics import matthews_corrcoef
import cv2
import os
from os import listdir
from os.path import isfile, join
import re
import fnmatch
from sklearn import preprocessing

import scipy.misc
import numpy as np

### PATHS #####################################################################

#pathResults = "../../../pytorch-CycleGAN-and-pix2pix/results/placenta_pix2pix/2017-08-20-test_latest/images/"
## get list of fake files and of real files
#fakeFiles = [ff for file in sorted(os.listdir(pathResults)) for ff in re.findall("*fake_B.png", file)];
#realFiles = [re.sub("fake_B", "real_B", x) for x in fakeFiles]

pathReal = "/home/Documents/placenta/data/Reconstructed/CroppedTrace/";
pathFake = "/home/Documents/placenta/data/Reconstructed/CroppedAverage/"
fakeFiles = fnmatch.filter(os.listdir(pathFake), '*_recon_avg.png');
realFiles = [re.sub("_recon_avg.png", "", x) for x in fakeFiles]

numFiles = len(fakeFiles)
mccResults = []
mccResultsCheck = []
for jj in range(0, numFiles):
	print('--- Working on file '+str(jj+1)+' --------------------------------')
	
	# read in the images
	fakeImagePath = os.path.join(pathFake, fakeFiles[jj])
	fakeImage = scipy.misc.imread(fakeImagePath, mode="L");
	realImagePath = os.path.join(pathReal, realFiles[jj])
	realImage = scipy.misc.imread(realImagePath, mode="L");
	fakeImagePath = os.path.join(pathFake, fakeFiles[jj]);
	fakeImage = cv2.imread(fakeImagePath, cv2.IMREAD_GRAYSCALE);
	realImagePath = os.path.join(pathReal, realFiles[jj]);
	realImage = cv2.imread(realImagePath, cv2.IMREAD_GRAYSCALE);
	
	## checked where to have a cutoff for black and white
	## REVISIT: still not sure why initial (real) images weren't completely BW?
	# hist, bins = np.histogram(fakeImage.ravel(), 256, [0,256])
	# plt.hist(img.ravel(),256,[0,256]);
	fakeThresh, fakeImageBW = cv2.threshold(fakeImage, 250, 255, cv2.THRESH_BINARY)
	realThresh, realImageBW = cv2.threshold(realImage, 254, 255, cv2.THRESH_BINARY)

	# binarize the images
	fakeImageBW[fakeImageBW==0] = 1
	fakeImageBW[fakeImageBW==255] = 0;
	realImageBW[realImageBW==0] = 1;
	realImageBW[realImageBW==255] = 0;
	lb = preprocessing.LabelBinarizer()
	lb.fit(realImageBW)
	realImageBin = lb.transform(realImageBW)
	lb.fit(fakeImageBW)
	fakeImageBin = lb.transform(fakeImageBW)

	# calculate MCC 
	mccResults.append(matthews_corrcoef(realImageBin.ravel(), fakeImageBin.ravel()))
	# check manually
	TP = len(np.intersect1d(np.where(realImageBW.ravel()==1), np.where(fakeImageBW.ravel()==1)));
	TN = len(np.intersect1d(np.where(realImageBW.ravel()==0), np.where(fakeImageBW.ravel()==0)));
	FP = len(np.intersect1d(np.where(realImageBW.ravel()==0), np.where(fakeImageBW.ravel()==1)));
	FN = len(np.intersect1d(np.where(realImageBW.ravel()==1), np.where(fakeImageBW.ravel()==0)));
	mcc = (TP*TN-FP*FN)/np.sqrt(((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))+0.0);
	mccResultsCheck.append(mcc); 
