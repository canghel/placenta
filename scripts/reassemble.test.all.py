# now reassemble all the averages for the overlapping squares

### PREAMBLE ##################################################################

import cv2
import os
import numpy as np
from os import listdir
from os.path import isfile, join
import fnmatch
import re
import sys, traceback
import matplotlib.pyplot as plt

# datetime
import datetime
now = datetime.datetime.now()

# useful math functions
from sklearn.metrics import matthews_corrcoef
from sklearn import preprocessing
import scipy.misc

# useful math functions
from sklearn.metrics import matthews_corrcoef
from sklearn import preprocessing
import scipy.misc
import numpy as np

### PATHS #####################################################################

pathTraces = "/home/Documents/placenta/data/Traces/Pre-processed/"
#pathTest = "/home/Documents/placenta/pytorch-CycleGAN-and-pix2pix/results/placenta_pix2pix/2017-10-23-test_latest/images"
pathTest = "/home/Documents/placenta/pytorch-CycleGAN-and-pix2pix/results/2017-08-20-placenta_pix2pix/test_latest/images/"
pathOutput = "/home/Documents/placenta/data/2017-10-24-Reconstructed"

### FIND FILENAME STEM FOR EACH PLACENTA #####################################

threshValue = 200;

testFiles = fnmatch.filter(os.listdir(pathTest), '*_Trans_0_fake_B.png');

# get the unique files that were processed
fileStem = np.unique([re.sub('_Part_[0-9]*_Angle_[0-9]*_Trans_0_fake_B.png', '', x) for x in testFiles])
# number of full placentas in the test dataset
numFullTest = len(fileStem);

translationValue = [64, 128, 192]

mccResults = []
# loop over files
for ii in range(0, numFullTest):
	print('--- Working on file '+str(ii+1)+' --------------------------------')
	# load the average for translation 0
	output = cv2.imread(os.path.join(pathOutput, 'AverageTrans0', fileStem[ii]+'_recon_avg.png'));
	traceImage = cv2.imread(os.path.join(pathTraces, fileStem[ii]));
	# load each of the tranlation values (smaller) reconstructions too
	outputTrans64 = cv2.imread(os.path.join(pathOutput, 'AverageTrans64', fileStem[ii]+'_recon_avg.png'));
	outputTrans128 = cv2.imread(os.path.join(pathOutput, 'AverageTrans128', fileStem[ii]+'_recon_avg.png'));
	outputTrans192 = cv2.imread(os.path.join(pathOutput, 'AverageTrans192', fileStem[ii]+'_recon_avg.png'));

	# get the number of rows and columns of smaller (translated) images
	nofr = np.int(np.ceil(traceImage.shape[0]/256));
	nofc = np.int(np.ceil(traceImage.shape[1]/256));	

	### AVERAGE 4 OVERLAPPING IMAGES ##############################################
	# !!! 
	# !!! pretty sure some indices are off by one here :P
	# !!!

	# the innermost rectangle is covered by 4 images that are averages
	rStart = 191;
	rEnd = 256*nofr - 192 - 1;
	cStart = 191;
	cEnd = 256*nofc - 192 - 1;

	rr = outputTrans64.shape[0]
	cc = outputTrans64.shape[1]

	# output[rStart:rEnd,cStart:cEnd,:].shape
	# outputTrans192[0:(rr-128), 0:(cc-128),:].shape
	# outputTrans64[0:(rr-128), 0:cc,:].shape
	# outputTrans128[0:(rr-64), 0:(cc-64),:].shape

	output[rStart:rEnd,cStart:cEnd,:] = (output[rStart:rEnd,cStart:cEnd,:]/4 +
		outputTrans192[0:(rr-128), 0:(cc-128),:]/4 +
		outputTrans64[128:rr, 128:cc,:]/4 + 
		outputTrans128[64:(rr-64), 64:(cc-64),:]/4)

	# test = np.ones((output[rStart:rEnd,cStart:cEnd,:].shape))*255

	# test = (test/4 +
	# 	outputTrans192[0:(rr-128), 0:(cc-128),:]/4 +
	# 	outputTrans64[128:rr, 128:cc,:]/4 + 
	# 	outputTrans128[64:(rr-64), 64:(cc-64),:]/4)

	# cv2.imwrite(os.path.join(pathOutput, 'Average', 'test.png'), output);
	# cv2.imwrite(os.path.join(pathOutput, 'Average', 'test2.png'), test);

	### AVERAGE 3 OVERLAPPING IMAGES ##############################################

	# left rectangle --------------------------------------------------------------
	rStart = 128;
	rEnd = 256*nofr-192;
	cStart = 128;
	cEnd = 192;

	output[rStart:rEnd,cStart:cEnd,:] = (output[rStart:rEnd,cStart:cEnd,:]/3 +
		outputTrans128[0:(rr-64), 0:64,:]/3 +
		outputTrans64[64:rr, 64:128,:]/3)
	# cv2.imwrite(os.path.join(pathOutput, 'Average', 'test.png'), output);

	# test = np.ones((output[rStart:rEnd,cStart:cEnd,:].shape))*255

	# test = (test/3 +
	# 	outputTrans128[0:(rr-64), 0:64,:]/3 +
	# 	outputTrans64[64:rr, 64:128,:]/3)

	# cv2.imwrite(os.path.join(pathOutput, 'Average', 'test2.png'), test);

	# right rectangle -------------------------------------------------------------
	rStart = 192;
	rEnd = 256*nofr - 128;
	cStart = 256*nofc - 192;
	cEnd = 256*nofc - 128;

	output[rStart:rEnd,cStart:cEnd,:] = (output[rStart:rEnd,cStart:cEnd,:]/3 +
		outputTrans128[64:rr, (cc-64):cc,:]/3 +
		outputTrans192[0:(rr-64), (cc-128):(cc-64),:]/3)
	# cv2.imwrite(os.path.join(pathOutput, 'Average', 'test.png'), output);

	# test = np.ones((output[rStart:rEnd,cStart:cEnd,:].shape))*255

	# test = (test/3 +
	# 	outputTrans128[64:rr, (cc-64):cc,:]/3 +
	# 	outputTrans192[0:(rr-64), (cc-128):(cc-64),:]/3)

	# cv2.imwrite(os.path.join(pathOutput, 'Average', 'test.png'), test);

	# bottom rectangle ------------------------------------------------------------
	rStart = 256*nofr - 192;
	rEnd = 256*nofr - 128;
	cStart = 192;
	cEnd = 256*nofc - 192;

	output[rStart:rEnd,cStart:cEnd,:] = (output[rStart:rEnd,cStart:cEnd,:]/3 +
		outputTrans128[(rr-64):rr, 64:(cc-64),:]/3 +
		outputTrans192[(rr-128):(rr-64), 0:(cc-128),:]/3)
	# cv2.imwrite(os.path.join(pathOutput, 'Average', 'test.png'), output);

	# test = np.ones((output[rStart:rEnd,cStart:cEnd,:].shape))*255

	# test = (test/3 +
	# 	outputTrans128[(rr-64):rr, 64:(cc-64),:]/3 +
	# 	outputTrans192[(rr-128):(rr-64), 0:(cc-128),:]/3)

	# cv2.imwrite(os.path.join(pathOutput, 'Average', 'test2.png'), test);


	# top rectangle ---------------------------------------------------------------
	rStart = 128;
	rEnd = 192;
	cStart = 192;
	cEnd = 256*nofc - 192;

	output[rStart:rEnd,cStart:cEnd,:] = (output[rStart:rEnd,cStart:cEnd,:]/3 +
		outputTrans128[0:64, 64:(cc-64),:]/3 +
		outputTrans64[64:128, 128:cc,:]/3)
	# cv2.imwrite(os.path.join(pathOutput, 'Average', 'test.png'), output);

	test = np.ones((output[rStart:rEnd,cStart:cEnd,:].shape))*255

	# test = (test/3 + 
	# 	outputTrans128[0:64, 64:(cc-64),:]/3 +
	# 	outputTrans64[64:128, 128:cc,:]/3)

	# cv2.imwrite(os.path.join(pathOutput, 'Average', 'test3.png'), test);

	hist,bins = np.histogram(output.ravel(),256,[0,256])
	plt.hist(output.ravel(),256,[0,256]);
	fig = plt.gcf()
	fig.savefig('/home/Documents/placenta/data/'+now.strftime("%Y-%m-%d")+'pixel-values-8-20-new-test.png')
	# plt.close(fig)

	# output = cv2.threshold(output, threshValue, 255, cv2.THRESH_BINARY);
	outputFilename = fileStem[ii]+'_recon_avg.png'
	cv2.imwrite(os.path.join(pathOutput, 'Average', outputFilename), output[0:traceImage.shape[0], 0:traceImage.shape[1],:]);

	# cutoff
	output=output[0:traceImage.shape[0], 0:traceImage.shape[1],:]
	fakeThresh, fakeImageBW = cv2.threshold(output, 200, 255, cv2.THRESH_BINARY)
	realThresh, realImageBW = cv2.threshold(traceImage, 250, 255, cv2.THRESH_BINARY)

	# binarize the images
	fakeImageBW[fakeImageBW==0] = 1
	fakeImageBW[fakeImageBW==255] = 0;
	realImageBW[realImageBW==0] = 1;
	realImageBW[realImageBW==255] = 0;
	# lb = preprocessing.LabelBinarizer()
	# lb.fit(realImageBW)
	# realImageBin = lb.transform(realImageBW)
	# lb.fit(fakeImageBW)
	# fakeImageBin = lb.transform(fakeImageBW)

	# calculate MCC 
	mccResults.append(matthews_corrcoef(realImageBW.ravel(), fakeImageBW.ravel()))

print('--- Results summary -----------------------------------')
print('Min:'+str(np.min(mccResults)))
print('Mean:'+str(np.mean(mccResults)))
print('Median:'+str(np.median(mccResults)))
print('Max:'+str(np.max(mccResults)))
print('------------------------------------------------------')

### PLOTS #####################################################################

plt.figure(figsize=(12, 12))  
  
ax = plt.subplot(111)  
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)  
  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  
  
plt.xticks(fontsize=18) 
plt.yticks(fontsize=18)  
  
plt.xlabel("MCC Value", fontsize=22)  
plt.ylabel("Frequency", fontsize=22)  
  
plt.hist(mccResults, color="#3F5D7D", edgecolor="k")  

fig = plt.gcf()
fig.savefig('/home/Documents/placenta/data/'+str(now.strftime("%Y-%m-%d"))+'-test-averaged-MCCValuesHist-8-20-new-test.png', bbox_inches="tight")

# initialize dataframe
df = pd.DataFrame({'MCC': mccResults, 'group': 'Test dataset'})
group = 'group'
column = 'MCC'
grouped = df.groupby(group)

names, vals, xs = [], [] ,[]

for i, (name, subdf) in enumerate(grouped):
    names.append(name)
    vals.append(subdf[column].tolist())
    xs.append(np.random.normal(i+1, 0.04, subdf.shape[0]))

plt.figure(figsize=(12, 12))  
plt.boxplot(vals, labels=names)
plt.xticks(fontsize=18) 
plt.yticks(fontsize=18) 
plt.ylim([0.66,0.835])
ngroup = len(vals)
clevels = np.linspace(0., 1., ngroup)

for x, val, clevel in zip(xs, vals, clevels):
    plt.scatter(x, val, c=cm.prism(clevel), alpha=0.4)

fig = plt.gcf()
fig.savefig('/home/Documents/placenta/data//'+now.strftime("%Y-%m-%d")+'-test-averaged-MCCValuesBoxPlot-8-20-new-test.png', bbox_inches="tight")


plt.figure(figsize=(12, 12))  
plt.scatter(mccResults,mccResultsAveraged)
plt.plot([0.65, 0.86], [0.65, 0.86], ls="--", c=".3")
plt.xlabel("MCC", fontsize=22)  
plt.ylabel("MCC Overlapping average", fontsize=22)  
fig2 = plt.gcf()
fig2.savefig('/home/Documents/placenta/data//'+now.strftime("%Y-%m-%d")+'-averaged-non-averaged.png', bbox_inches="tight")
