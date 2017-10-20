# get the file sizes and check if a file size is very small, move a portion
# of them out of the folder
# i.e. move a lot of the blank squares from training
# since NN doesn't learn anything from them

### OPTIONS TO CHANGE #########################################################

trainOrVal = "val"
thresholdFileSize =  10240 # inspect file sizes that are smaller than this size
probToMove = 0.8 # move them out of the folder with this probability

### PREAMBLE ##################################################################

import os
import os.path
import fnmatch
import re
import numpy as np
import random

### PATHS #####################################################################


pathFiles = "/home/Documents/placenta/pytorch-CycleGAN-and-pix2pix/datasets/placenta/"+trainOrVal
pathRemovedFiles = "/home/Documents/placenta/pytorch-CycleGAN-and-pix2pix/datasets/placenta/old/blankSquares/"+trainOrVal

### GET ALL FILES ###########################################################

allFiles = fnmatch.filter(os.listdir(pathFiles), '*.png');
fileStem = np.unique([re.sub('_Part_[0-9]*_Angle_[0-9]*.png', '', x) for x in allFiles]);

numPlacentas = len(fileStem);
numFiles = len(allFiles);

print("The number of placentas is", numPlacentas);

### FIND FILENAME STEM FOR EACH PLACENTA #####################################

random.seed(100);

numNearlyBlank = 0;
for jj in range(0, numFiles):
	# load the trace image of that placenta
	fileSize = os.path.getsize(os.path.join(pathFiles, allFiles[jj]))
	# consider only files smaller than the give file size
	if (fileSize < thresholdFileSize):
		print(fileSize);
		# count the number of files that are under the threshold size
		numNearlyBlank = numNearlyBlank + 1;
		# draw a 0 or 1 flag with given probably about whether to move file 
		moveFlag = np.random.binomial(1, probToMove);
		print(moveFlag);
		# move the file if flag is 1
		if (moveFlag):
			os.rename(os.path.join(pathFiles, allFiles[jj]), os.path.join(pathRemovedFiles, allFiles[jj]))