# reassemble the training and validation ones, too
# for those, they will be smaller than the whole image (because of the way we
# cropped the small squares)

### PREAMBLE ##################################################################

import cv2
import os
import numpy as np
from os import listdir
from os.path import isfile, join
import fnmatch
import re
import sys, traceback

### PATHS #####################################################################

trainOrVal = "val"
pathTraces = "/home/Documents/placenta/data/Traces/Pre-processed/"
pathResults = "/home/Documents/placenta/pytorch-CycleGAN-and-pix2pix/results/placenta_pix2pix/2017-10-19-"+trainOrVal+"/images"
pathOutput = "/home/Documents/placenta/data/2017-10-19-Reconstructed"+trainOrVal.capitalize()

### FIND FILENAME STEM FOR EACH PLACENTA #####################################

resultFiles = fnmatch.filter(os.listdir(pathResults), '*fake_B.png');

# get the unique files that were processed
fileStem = np.unique([re.sub('_Part_[0-9]*_Angle_[0-9]*_fake_B.png', '', x) for x in resultFiles])
# number of full placentas in the test dataset
numFullResults = len(fileStem);

angles = ['Angle_0', 'Angle_90', 'Angle_180', 'Angle_270']

### RECONSTRUCT THE TRACE OUTPUT BY NN FOR EACH PLACENTA #####################
# get four traces for each angle
# plus an average trace

# loop over images (jj is index of the image of a whole placenta)
for jj in range(0, numFullResults):
	print('--- Working on file '+str(jj+1)+' --------------------------------')
	# load the trace image of that placenta
	traceImage = cv2.imread(os.path.join(pathTraces, fileStem[jj]))

	# number of rows and number of columns
	nofr = np.int(np.ceil(traceImage.shape[0]/256));
	nofc = np.int(np.ceil(traceImage.shape[1]/256));

	cv2.imwrite(os.path.join(pathOutput, 'CroppedTrace',  fileStem[jj]), traceImage[0:nofr*256, 0:nofc*256,:]);

	# loop over all the angles (aa is index of the angle)
	for aa in range(0, 4):
		angle = angles[aa];
		# create blank (white) image 
		output = np.ones_like(traceImage)*255

		# loop over rows and columns
		for rr in range(0, nofr):
			for cc in range(0, nofc):

				# get the number of the part
				part = nofc*rr + cc + 1;
				# this is the file and load the 256x256 part of the image
				fileToLoad = fileStem[jj]+'_Part_'+str(part)+'_'+angle+'_fake_B.png'
				subImage = cv2.imread(os.path.join(pathResults, fileToLoad));

				# need to save that image as part of the bigger image
				# with the correct row and column coordinates
				rStart = 256*rr;
				rEnd = 256*(rr+1);
				cStart = 256*cc;
				cEnd = 256*(cc+1);
				if (angle=='Angle_0'):
				    output[rStart:rEnd,cStart:cEnd,:] = subImage;
				elif (angle=='Angle_90'):
				    output[rStart:rEnd,cStart:cEnd,:] = np.rot90(subImage, 3);
				elif (angle=='Angle_180'):
				    output[rStart:rEnd,cStart:cEnd,:] = np.rot90(subImage, 2);
				elif (angle=='Angle_270'):
				    output[rStart:rEnd,cStart:cEnd,:] = np.rot90(subImage, 1);

		# save output to file
		outputFile = fileStem[jj]+'_recon_'+angle+'.png'
		cv2.imwrite(os.path.join(pathOutput, 'ByAngle',  outputFile), output);

		# keep a record of the average trace
		# easier to divide each by 4 than average at the end
		temp = cv2.threshold(output, 250, 255, cv2.THRESH_BINARY);
		if (angle=='Angle_0'):
			averageTrace = output/4;
		else:
			averageTrace = averageTrace +  (output/4);

	# save the average trace
	averageTrace = np.around(averageTrace).astype(int)
	averageFile = fileStem[jj]+'_recon_avg.png'
	cv2.imwrite(os.path.join(pathOutput, 'Average', averageFile), averageTrace);
	cv2.imwrite(os.path.join(pathOutput, 'CroppedAverage', averageFile), averageTrace[0:nofr*256, 0:nofc*256,:]);