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
from matplotlib import cm
# not quite sure what pandas are yet
import pandas as pd

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
import scipy.stats
import numpy as np

### FIND FILENAME STEM FOR EACH PLACENTA #####################################

threshFake = 200;
threshReal = 250;

testFiles = fnmatch.filter(os.listdir(pathTest), '*_Trans_0_fake_B.png');

# get the unique files that were processed
fileStem = np.unique([re.sub('_Part_[0-9]*_Angle_[0-9]*_Trans_0_fake_B.png', '', x) for x in testFiles])
fileStem = sorted(fileStem, key=str.lower)
# number of full placentas in the test dataset
numFullTest = len(fileStem);

translationValue = [64, 128, 192]

mccResultsTrans0 = []
mccResults = []
sensitivity = []
specificity = []
precision = []
F1score = []
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

	### MCC FOR TRANSLATION 0 FILES ###############################################

	outputTrans0=output[0:traceImage.shape[0], 0:traceImage.shape[1],:]
	fakeThreshTrans0, fakeImageBWTrans0 = cv2.threshold(outputTrans0, threshFake, 255, cv2.THRESH_BINARY)
	realThresh, realImageBW = cv2.threshold(traceImage, threshReal, 255, cv2.THRESH_BINARY)
	# binarize the images
	fakeImageBWTrans0[fakeImageBWTrans0==0] = 1
	fakeImageBWTrans0[fakeImageBWTrans0==255] = 0;
	realImageBW[realImageBW==0] = 1;
	realImageBW[realImageBW==255] = 0;

	mccResultsTrans0.append(matthews_corrcoef(realImageBW.ravel(), fakeImageBWTrans0.ravel()))


	### AVERAGE 4 OVERLAPPING IMAGES ##############################################

	# the innermost rectangle is covered by 4 images that are averages
	rStart = 192;
	rEnd = 256*nofr - 192;
	cStart = 192;
	cEnd = 256*nofc - 192;

	rr = outputTrans64.shape[0]
	cc = outputTrans64.shape[1]

	output[rStart:rEnd,cStart:cEnd,:] = (output[rStart:rEnd,cStart:cEnd,:]/4 +
		outputTrans192[0:(rr-128), 0:(cc-128),:]/4 +
		outputTrans64[128:rr, 128:cc,:]/4 + 
		outputTrans128[64:(rr-64), 64:(cc-64),:]/4)


	### AVERAGE 3 OVERLAPPING IMAGES ##############################################

	# left rectangle --------------------------------------------------------------
	rStart = 128;
	rEnd = 256*nofr-192;
	cStart = 128;
	cEnd = 192;

	output[rStart:rEnd,cStart:cEnd,:] = (output[rStart:rEnd,cStart:cEnd,:]/3 +
		outputTrans128[0:(rr-64), 0:64,:]/3 +
		outputTrans64[64:rr, 64:128,:]/3)

	# right rectangle -------------------------------------------------------------
	rStart = 192;
	rEnd = 256*nofr - 128;
	cStart = 256*nofc - 192;
	cEnd = 256*nofc - 128;

	output[rStart:rEnd,cStart:cEnd,:] = (output[rStart:rEnd,cStart:cEnd,:]/3 +
		outputTrans128[64:rr, (cc-64):cc,:]/3 +
		outputTrans192[0:(rr-64), (cc-128):(cc-64),:]/3)


	# bottom rectangle ------------------------------------------------------------
	rStart = 256*nofr - 192;
	rEnd = 256*nofr - 128;
	cStart = 192;
	cEnd = 256*nofc - 192;

	output[rStart:rEnd,cStart:cEnd,:] = (output[rStart:rEnd,cStart:cEnd,:]/3 +
		outputTrans128[(rr-64):rr, 64:(cc-64),:]/3 +
		outputTrans192[(rr-128):(rr-64), 0:(cc-128),:]/3)


	# top rectangle ---------------------------------------------------------------
	rStart = 128;
	rEnd = 192;
	cStart = 192;
	cEnd = 256*nofc - 192;

	output[rStart:rEnd,cStart:cEnd,:] = (output[rStart:rEnd,cStart:cEnd,:]/3 +
		outputTrans128[0:64, 64:(cc-64),:]/3 +
		outputTrans64[64:128, 128:cc,:]/3)

	# hist,bins = np.histogram(output.ravel(),256,[0,256])
	# plt.hist(output.ravel(),256,[0,256]);
	# fig = plt.gcf()
	# fig.savefig(os.path.join(pathOutput, str(now.strftime("%Y-%m-%d"))+'pixel-vals.png'))

	outputFilename = fileStem[ii]+'_recon_avg.png'
	cv2.imwrite(os.path.join(pathOutput, 'Average', outputFilename), output[0:traceImage.shape[0], 0:traceImage.shape[1],:]);

	# cutoff
	output=output[0:traceImage.shape[0], 0:traceImage.shape[1],:]
	fakeThresh, fakeImageBW = cv2.threshold(output, threshFake, 255, cv2.THRESH_BINARY)
	realThresh, realImageBW = cv2.threshold(traceImage, threshReal, 255, cv2.THRESH_BINARY)

	outputFilenameBinarized = fileStem[ii]+'_recon_avg_binarized.png'
	cv2.imwrite(os.path.join(pathOutput, 'Average', outputFilenameBinarized), fakeImageBW);

	# binarize the images
	fakeImageBW[fakeImageBW==0] = 1
	fakeImageBW[fakeImageBW==255] = 0;
	realImageBW[realImageBW==0] = 1;
	realImageBW[realImageBW==255] = 0;

	# calculate MCC 
	TP = len(np.intersect1d(np.where(realImageBW.ravel()==1), np.where(fakeImageBW.ravel()==1)));
	TN = len(np.intersect1d(np.where(realImageBW.ravel()==0), np.where(fakeImageBW.ravel()==0)));
	FP = len(np.intersect1d(np.where(realImageBW.ravel()==0), np.where(fakeImageBW.ravel()==1)));
	FN = len(np.intersect1d(np.where(realImageBW.ravel()==1), np.where(fakeImageBW.ravel()==0)));
	sensitivity.append(TP/(TP+FN))
	specificity.append(TN/(TN+FP))
	precision.append(TP/(TP+FP))
	F1score.append(2*TP/(2*TP+FP+FN))
	mccResults.append(matthews_corrcoef(realImageBW.ravel(), fakeImageBW.ravel()))

print('--- Results summary -----------------------------------')
print('Min:'+str(np.min(mccResults)))
print('Mean:'+str(np.mean(mccResults)))
print('Median:'+str(np.median(mccResults)))
print('Max:'+str(np.max(mccResults)))
print(scipy.stats.describe(sensitivity))
print(scipy.stats.describe(specificity))
print(scipy.stats.describe(precision))
print(scipy.stats.describe(F1score))
print('------------------------------------------------------')

### SAVE RESULTS TO FILE ######################################################

np.savetxt(pathOutput+str(now.strftime("%Y-%m-%d"))+'-averaged-MCC-values-'+filenameSuffix+'.txt', mccResults)
np.savetxt(pathOutput+str(now.strftime("%Y-%m-%d"))+'-trans0-MCC-values-'+filenameSuffix+'.txt', mccResultsTrans0)

### PLOTS #####################################################################

# histogram of averaged mcc values --------------------------------------------
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
fig.savefig(pathOutput+str(now.strftime("%Y-%m-%d"))+'-averaged-MCCValuesHist-'+filenameSuffix+'.png', bbox_inches="tight")

# box plot of averaged mcc values ---------------------------------------------

# initialize dataframe
df = pd.DataFrame({'MCC': mccResultsTrans0, 'group': 'Test dataset'})
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
plt.ylim([0.65,0.86])
ngroup = len(vals)
clevels = np.linspace(0., 1., ngroup)

for x, val, clevel in zip(xs, vals, clevels):
    plt.scatter(x, val, c=cm.prism(clevel), alpha=0.4)

fig = plt.gcf()
fig.savefig(pathOutput+now.strftime("%Y-%m-%d")+'-trans0-MCCValuesBoxPlot-'+filenameSuffix+'.png', bbox_inches="tight")

# box plot of averaged mcc values ---------------------------------------------

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
plt.ylim([0.65,0.86])
ngroup = len(vals)
clevels = np.linspace(0., 1., ngroup)

for x, val, clevel in zip(xs, vals, clevels):
    plt.scatter(x, val, c=cm.prism(clevel), alpha=0.4)

fig = plt.gcf()
fig.savefig(pathOutput+now.strftime("%Y-%m-%d")+'-averaged-MCCValuesBoxPlot-'+filenameSuffix+'.png', bbox_inches="tight")

# histogram of averaged F1 score ----------------------------------------------

plt.figure(figsize=(12, 12))  
  
ax = plt.subplot(111)  
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)  
  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  
  
plt.xticks(fontsize=18) 
plt.yticks(fontsize=18)  
  
plt.xlabel("F1 score", fontsize=22)  
plt.ylabel("Frequency", fontsize=22)  
  
plt.hist(F1score, color="#3F5D7D", edgecolor="k")  

fig = plt.gcf()
fig.savefig(pathOutput+str(now.strftime("%Y-%m-%d"))+'-averaged-F1score-'+filenameSuffix+'.png', bbox_inches="tight")

# histogram of averaged precision ---------------------------------------------

plt.figure(figsize=(12, 12))  
  
ax = plt.subplot(111)  
ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False)  
  
ax.get_xaxis().tick_bottom()  
ax.get_yaxis().tick_left()  
  
plt.xticks(fontsize=18) 
plt.yticks(fontsize=18)  
  
plt.xlabel("Precision", fontsize=22)  
plt.ylabel("Frequency", fontsize=22)  
  
plt.hist(precision, color="#3F5D7D", edgecolor="k")  

fig = plt.gcf()
fig.savefig(pathOutput+str(now.strftime("%Y-%m-%d"))+'-averaged-precision-'+filenameSuffix+'.png', bbox_inches="tight")