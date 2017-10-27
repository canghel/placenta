# move the training, test and val preprocessed files into different directories
# for both photos and traces

### PREAMBLE ##################################################################

import os
from os import listdir
from os.path import isfile, join
import fnmatch
import re

### PATHS #####################################################################

pathPhotos = "../../../data/photos/preprocessed"
pathTraces = "../../../data/traces/preprocessed"

### GET NAMES OF FILES ########################################################

# actually... better not to sort
# but sorted in previous work up till now, when moved them using bash commands
traceFiles = [f for f in listdir(pathTraces) if isfile(join(pathTraces, f))]
traceFiles = sorted(traceFiles, key=str.lower)
photoFiles = [f for f in listdir(pathPhotos) if isfile(join(pathPhotos, f))]
photoFiles = sorted(photoFiles, key=str.lower)

# sanity check
print("Check if trace files and photo files are the same names")
print(traceFiles==photoFiles)

numFiles = len(photoFiles);

### OBTAIN A MASK #############################################################

for jj in range(0, numFiles):
	if (jj < 121):
		os.rename(os.path.join(pathTraces, traceFiles[jj]), os.path.join(pathTraces+'/train', traceFiles[jj]))
		os.rename(os.path.join(pathPhotos, photoFiles[jj]), os.path.join(pathPhotos+'/train', photoFiles[jj]))
	elif (jj >= 121 and jj < 161):
		os.rename(os.path.join(pathTraces, traceFiles[jj]), os.path.join(pathTraces+'/val', traceFiles[jj]))
		os.rename(os.path.join(pathPhotos, photoFiles[jj]), os.path.join(pathPhotos+'/val', photoFiles[jj]))
	elif (jj >=161 and jj < 201):
		os.rename(os.path.join(pathTraces, traceFiles[jj]), os.path.join(pathTraces+'/test', traceFiles[jj]))
		os.rename(os.path.join(pathPhotos, photoFiles[jj]), os.path.join(pathPhotos+'/test', photoFiles[jj]))