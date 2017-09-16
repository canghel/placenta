# boxplot of mcc values for train, val and test
# question: validation set is only used for validation in cGAN?

### PREAMBLE ##################################################################

import numpy as np
# plotting things
import matplotlib.pyplot as plt
from matplotlib import cm
import plotly.plotly as py
# not quite sure what pandas are yet
import pandas as pd

### READ IN THE THREE MCC FILES ###############################################

mccTrain = np.loadtxt('/home/Documents/placenta/data/trainMCCValues.txt');
mccVal = np.loadtxt('/home/Documents/placenta/data/valMCCValues.txt');
mccTest = np.loadtxt('/home/Documents/placenta/data/testMCCValues.txt');

nTrain = len(mccTrain);
nVal = len(mccVal);
nTest = len(mccTest);

### PLOT A BOXPLOT OF RESULTS #################################################
# using code from: 
# https://stackoverflow.com/questions/29779079/adding-a-scatter-of-points-to-a-boxplot-using-matplotlib

# initialize dataframe
df = pd.DataFrame({'MCC': list(mccTrain) + list(mccVal) + list(mccTest), 'group': list(['1']*nTrain + ['2']*nVal + ['3']*nTest)})
group = 'group'
column = 'MCC'
grouped = df.groupby(group)

# i think this part makes the jitter
names, vals, xs = [], [] ,[]

for i, (name, subdf) in enumerate(grouped):
    names.append(name)
    vals.append(subdf[column].tolist())
    xs.append(np.random.normal(i+1, 0.04, subdf.shape[0]))

# create figure
plt.figure(figsize=(12, 9))
plt.boxplot(vals, labels=['Train']+['Val']+['Test'])
plt.xticks(fontsize=18) 
plt.yticks(fontsize=18)  
ngroup = len(vals)
# clevels = np.linspace(0., 1., ngroup)
clevels = [5, 1, 3];

for x, val, clevel in zip(xs, vals, clevels):
    #plt.scatter(x, val, c=cm.prism(clevel), alpha=0.4)
    plt.scatter(x, val, c=cm.Paired(clevel), alpha=0.4)

fig = plt.gcf()
fig.savefig('/home/Documents/placenta/data/MCCValuesBoxPlotPastel.png', bbox_inches="tight")