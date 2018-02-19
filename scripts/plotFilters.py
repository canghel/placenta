### PREAMBLE ##################################################################
import torch
import torch.nn as nn
import os

import numpy as np
import matplotlib.pyplot as plt
import cv2

# the path for the network to load
#pathNets = '/home/Documents/placenta/pytorch-CycleGAN-and-pix2pix/checkpoints/placenta_pix2pix/'
pathNets = '/home/Documents/placenta/pytorch-CycleGAN-and-pix2pix/checkpoints/facades_pix2pix'
fileToLoad = '10_net_G.pth'

### VISUALIZE FILTERS #########################################################
# load the network into the variable 'net'
net = torch.load(os.path.join(pathNets, fileToLoad))

## figuring out dimensions of filters, layers, etc.
for k, v in net.items():
	print(k)

#net["model.model.1.model.1.weight"]
#net["model.model.3.weight"].size()
#net["model.model.0.weight"].size()
#net["model.model.1.model.6.running_mean"].size()

#output = cv2.imread('/home/Documents/placenta/data/photos/preprocessed/train/T-BN0013990_fetalsurface_fixed_ruler_lights_filter_12_0130-dd.png')

# the filters are of size 3x4x4, and there are 64 of them
plt.figure()  
plt.imshow(np.floor((net["model.model.0.weight"][0,:,:,:])*255))
fig = plt.gcf()
fig.savefig("./test.png")

#+net["model.model.0.bias"][jj]
#+net["model.model.0.bias"][jj]

for jj in range(64):
	temp = np.floor((net["model.model.0.weight"][jj,:,:,:])*255);
	# print(sum(sum(sum(temp>0)<3)))
	# img = np.zeros((4,4,3))
	# img[:,:,0] = temp[0,:,:].numpy()
	# img[:,:,1] = temp[1,:,:].numpy()
	# img[:,:,2] = temp[2,:,:].numpy()
	img = np.zeros((4,4))
	img = temp[0,:,:].numpy()#-np.min(temp[0,:,:].numpy(), 0)
	#print(sum(sum(img>=0)))
	#img = temp[0,:,:].numpy()-np.min(temp[0,:,:].numpy(), 0)
	#plt.imshow(img, cmap=plt.get_cmap('gray'))
	plt.figure() #interpolation='none', 
	plt.imshow(img, vmin=-95, vmax=95, cmap='gray')
	# plt.colorbar()
	fig = plt.gcf()
	fig.savefig("./test"+str(jj)+".png")

print(net["model.model.0.weight"].size())

# for jj in range(64):
# 	temp = net["model.model.0.weight"][jj,:,:,:];
# 	x = np.zeros((4,4,3))
# 	x[:,:,0] = temp[0,:,:].numpy()
# 	x[:,:,1] = temp[1,:,:].numpy()
# 	x[:,:,2] = temp[2,:,:].numpy()
# 	x -= x.mean()
# 	x /= (x.std() + 1e-12)
# 	# x = (x - x.min()) / (x.max() - x.min())
# 	x *= 0.1
# 	#
# 	# clip to [0, 1]
# 	x += 0.5
# 	x = np.clip(x, 0, 1)
# 	#
# 	# convert to RGB array
# 	x *= 255
# 	#
# 	x = np.clip(x, 0, 255).astype('uint8')
# 	plt.figure() #interpolation='none', 
# 	plt.imshow(x)# , vmin=-95, vmax=95, cmap='gray')
# 	# plt.colorbar()
# 	fig = plt.gcf()
# 	fig.savefig("./test"+str(jj)+".png")

