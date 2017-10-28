# This script does to things:
# - crop non-overlapping 256x256 pixel squares for the photos and traces of 
#   training and validation placentas (and testing but that's not used in
#   in the GAN)
# - crop overlapping for testing and for reconstruction of training and 
#   validation in order to compare averaged vs. non-averaged images


def cropRotateOverlap(filename, inputdir, outputdir, overlap=True):
	### PREAMBLE ##############################################################

	import cv2
	import os
	import numpy as np
	from os import listdir
	from os.path import isfile, join
	import fnmatch
	import re
	import sys, traceback

	### READ IN FILE AND EXTEND IT TO MULTIPLE OF 256 PIXELS ##################

	img = cv2.imread(os.path.join(inputdir, filename));
	# size of image
	n = img.shape[0]
	m = img.shape[1]

	# number of rows and number of columns
	nofr = np.int(np.ceil(n/256));
	nofc = np.int(np.ceil(m/256));

	# create blank (white) image whose height and width are multiples of 256 pixels
	newimg = np.ones((nofr*256, nofc*256, 3))*255
	# Set the top left corner to match the image loaded
	newimg[0:n,0:m,:] = img;

	angles = ['Angle_0', 'Angle_90', 'Angle_180', 'Angle_270']

	# translation is 0 at this point
	# loop over rows and columns
	for rr in range(0, nofr):
		for cc in range(0, nofc):

			# create blank (white) image that's 256 by 256
			output = np.ones((256, 256, 3))*255
			# get the number of the part
			part = nofc*rr + cc + 1;
			# get the start and end indices of the image
			rStart = 256*rr;
			rEnd = 256*(rr+1);
			cStart = 256*cc;
			cEnd = 256*(cc+1);

			output = newimg[rStart:rEnd,cStart:cEnd,:];
			
			for jj in range(0, 4):
				if (overlap):
					outputFile = filename+'_Part_'+str(part)+'_'+angles[jj]+'_Trans_0.png'
				else:
					outputFile = filename+'_Part_'+str(part)+'_'+angles[jj]+'.png'
				output = np.rot90(output, jj);
				cv2.imwrite(os.path.join(outputdir, outputFile), output);

	if (overlap):
		translationValue = [64, 128, 192]
		# now do the same thing, but with the translation
		for ii in range(0, 3):
			for rr in range(0, (nofr-1)):
				for cc in range(0, (nofc-1)):

					# create blank (white) image that's 256 by 256
					output = np.ones((256, 256, 3))*255
					# get the number of the part
					part = (nofc-1)*rr + cc + 1;
					# get the start and end indices of the image
					rStart = 256*rr + translationValue[ii]; # if rr is 0 will start at 65th value, say
					rEnd = 256*(rr+1) + translationValue[ii];
					cStart = 256*cc + translationValue[ii];
					cEnd = 256*(cc+1) + translationValue[ii];

					rStart

					output = newimg[rStart:rEnd,cStart:cEnd,:];
					
					for jj in range(0, 4):
						outputFile = filename+'_Part_'+str(part)+'_'+str(angles[jj])+'_Trans_'+str(translationValue[ii])+'.png'
						print(jj)
						print(angles[jj])
						output = np.rot90(output, jj);
						cv2.imwrite(os.path.join(outputdir, outputFile), output);


### CALL THE FUNCTION #########################################################

import os
from os import listdir
from os.path import isfile, join
import fnmatch
import re
 
# ### CROP FOR NN, NON-OVERLAPPING ##############################################

# photoOrTrace = ['traces', 'photos'];
# dataset = ['train', 'val', 'test']

# # loop over photos or loop over traces
# for ii in range(0,2):
# 	# loop over the three datasets
# 	for jj in range(0,3):
# 		print('--- Working on '+dataset[jj]+' files ----------------------')
# 		inputdir = '/home/Documents/placenta/data/'+photoOrTrace[ii]+'/preprocessed/'+dataset[jj];
# 		outputdir =  '/home/Documents/placenta/data/'+photoOrTrace[ii]+'/croppedForNN/'+dataset[jj];

# 		print(inputdir)
# 		print(outputdir)

# 		## GET THE FILENAMES FOR TEST PHOTOS TO PROCESS ########################## 

# 		inputFiles = fnmatch.filter(os.listdir(inputdir), '*.png');

# 		for file in inputFiles:
# 			print(file)
# 			cropRotateOverlap(file, inputdir, outputdir, False)

### CROP FOR NN, OVERLAPPING #####################################################

dataset = ['train', 'val', 'test']

# loop over the three datasets
for jj in range(0,3):
	print('--- Working on '+dataset[jj]+' files ----------------------')
	inputdir = '/home/Documents/placenta/data/photos/preprocessed/'+dataset[jj];
	outputdir =  '/home/Documents/placenta/data/photos/croppedOverlapping/'+dataset[jj];

	print(inputdir)
	print(outputdir)

	## GET THE FILENAMES FOR TEST PHOTOS TO PROCESS ########################## 

	inputFiles = fnmatch.filter(os.listdir(inputdir), '*.png');

	for file in inputFiles:
		print(file)
		cropRotateOverlap(file, inputdir, outputdir, True)