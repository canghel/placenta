# crop and rotate

def cropRotateOverlay(filename, inputdir, outputdir):
	### PREAMBLE ##################################################################

	import cv2
	import os
	import numpy as np
	from os import listdir
	from os.path import isfile, join
	import fnmatch
	import re
	import sys, traceback

	### READ IN FILE AND EXTEND IT TO MULTIPLE OF 256 PIXELS ######################

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
				outputFile = filename+'_Part_'+str(part)+'_'+angles[jj]+'_Trans_0.png'
				output = np.rot90(output, jj);
				cv2.imwrite(os.path.join(outputdir, outputFile), output);

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
				rStart = 256*rr + translationValue[ii]-1;
				rEnd = 256*(rr+1) + translationValue[ii]-1;
				cStart = 256*cc + translationValue[ii]-1;
				cEnd = 256*(cc+1) + translationValue[ii]-1;

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
 
### PATHS #####################################################################

inputdir = '/home/Documents/placenta/data/testPhotos/Pre-processed/';
outputdir =  '/home/Documents/placenta/data/testPhotos/CroppedForNNOverlapping';

### GET THE FILENAMES FOR TEST PHOTOS TO PROCESS ############################## 

testFiles = fnmatch.filter(os.listdir(inputdir), '*.png');

for file in testFiles:
	print(file)
	cropRotateOverlay(file, inputdir, outputdir)