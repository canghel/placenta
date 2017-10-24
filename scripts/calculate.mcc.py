# mcc coefficient between true and fake B
# Kara already has a Matlab function to do this

### PREAMBLE ##################################################################

# images
import cv2

# input output and string matching
import os
from os import listdir
from os.path import isfile, join
import re
import fnmatch

# useful math functions
from sklearn.metrics import matthews_corrcoef
from sklearn import preprocessing
import scipy.misc
import numpy as np

# plotting things
import matplotlib.pyplot as plt
from matplotlib import cm
import plotly.plotly as py
# not quite sure what pandas are yet
import pandas as pd

# datetime
import datetime
now = datetime.datetime.now()

### PATHS #####################################################################

trainValOrTest = 'test';
if (trainValOrTest=="test"):
	pathReal = "/home/Documents/placenta/data/testTraces";
	pathFake = "/home/Documents/placenta/data/2017-10-19-Reconstructed/CroppedAverage/"
else:
	pathReal = "/home/Documents/placenta/data/Traces/Pre-processed";
	pathFake = "/home/Documents/placenta/data/2017-10-19-Reconstructed"+trainValOrTest.capitalize()+"/CroppedAverage/"

fakeFiles = fnmatch.filter(os.listdir(pathFake), '*_recon_avg.png');
realFiles = [re.sub("_recon_avg.png", "", x) for x in fakeFiles]

print('--- Dataset: '+trainValOrTest);

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
	
	# checked where to have a cutoff for black and white
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

print('--- Results summary -----------------------------------')
print('Min:'+str(np.min(mccResults)))
print('Mean:'+str(np.mean(mccResults)))
print('Median:'+str(np.median(mccResults)))
print('Max:'+str(np.max(mccResults)))
print('Mean results check:'+str(np.mean(mccResultsCheck)))
print('------------------------------------------------------')


### SAVE RESULTS TO FILE ######################################################

np.savetxt('/home/Documents/placenta/data/'+str(now.strftime("%Y-%m-%d"))+'-'+trainValOrTest+'MCCValues.txt', mccResults)

### PLOT A HISTOGRAM OF RESULTS ###############################################

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
fig.savefig('/home/Documents/placenta/data/'+str(now.strftime("%Y-%m-%d"))+'-'+trainValOrTest+'-MCCValuesHist.png', bbox_inches="tight")
# plt.close(fig)

# plot a histogram of mccResults
# plt.hist(mccResults)
# plt.title("MCC Values for Test Placenta Images")
# plt.xlabel("Value")
# plt.ylabel("Frequency")
# fig = plt.gcf()
# fig.savefig('/home/Documents/placenta/data/'+now.strftime("%Y-%m-%d")+'-'+trainValOrTest+'MCCValuesHist-2.png')
# plt.close(fig)

### PLOT A BOXPLOT OF RESULTS #################################################

# ooh, I should really do train, test, validation...

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
fig.savefig('/home/Documents/placenta/data//'+now.strftime("%Y-%m-%d")+'-testMCCValuesBoxPlot.png', bbox_inches="tight")