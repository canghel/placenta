# mcc coefficient between true and fake B

### PREAMBLE ##################################################################

from sklearn.metrics import matthews_corrcoef
import cv2
import os
from os import listdir
from os.path import isfile, join
import glob
import re

from sklearn import preprocessing

# import scipy.misc

### PATHS #####################################################################

pathResults = "../../../pytorch-CycleGAN-and-pix2pix/results/placenta_pix2pix/2017-08-20-test_latest/images/"
# get list of fake files and of real files
fakeFiles = [ff for file in sorted(os.listdir(pathResults)) for ff in re.findall("*fake_B.png", file)];
realFiles = [re.sub("fake_B", "real_B", x) for x in fakeFiles]

numFiles = len(fakeFiles)
mccResults = []
mccResultsCheck = []
for jj in range(0, numFiles):
	print('--- Working on file '+str(jj+1)+' --------------------------------')
	fakeImagePath = os.path.join(pathResults, fakeFiles[jj])
	fakeImage = scipy.misc.imread(fakeImagePath, mode="L");
	realImagePath = os.path.join(pathResults, realFiles[jj])
	realImage = scipy.misc.imread(realImagePath, mode="L");
	fakeImagePath = os.path.join(pathResults, fakeFiles[jj]);
	fakeImage = cv2.imread(fakeImagePath, cv2.IMREAD_GRAYSCALE);
	realImagePath = os.path.join(pathResults, realFiles[jj]);
	realImage = cv2.imread(realImagePath, cv2.IMREAD_GRAYSCALE);
	# hist, bins = np.histogram(fakeImage.ravel(), 256, [0,256])
	# plt.hist(img.ravel(),256,[0,256]);
	fakeThresh, fakeImageBW = cv2.threshold(fakeImage, 250, 255, cv2.THRESH_BINARY)
	realThresh, realImageBW = cv2.threshold(realImage, 254, 255, cv2.THRESH_BINARY)
	fakeImageBW[fakeImageBW==0] = 1
	fakeImageBW[fakeImageBW==255] = 0;
	realImageBW[realImageBW==0] = 1;
	realImageBW[realImageBW==255] = 0;
	lb = preprocessing.LabelBinarizer()
	lb.fit(realImageBW)
	realImageBin = lb.transform(realImageBW)
	lb.fit(fakeImageBW)
	fakeImageBin = lb.transform(fakeImageBW)
	mccResults.append(matthews_corrcoef(realImageBin.ravel(), fakeImageBin.ravel()))
	#
	TP = len(np.intersect1d(np.where(realImageBW.ravel()==1), np.where(fakeImageBW.ravel()==1)));
	TN = len(np.intersect1d(np.where(realImageBW.ravel()==0), np.where(fakeImageBW.ravel()==0)));
	FP = len(np.intersect1d(np.where(realImageBW.ravel()==0), np.where(fakeImageBW.ravel()==1)));
	FN = len(np.intersect1d(np.where(realImageBW.ravel()==1), np.where(fakeImageBW.ravel()==0)));
	mcc = (TP*TN-FP*FN)/np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN));
	mccResultsCheck.append(mcc); 
