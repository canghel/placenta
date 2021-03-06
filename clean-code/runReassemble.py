# run the reassembling of test, val and train images

### TEST  #####################################################################

# # paths
# pathTraces = "/home/Documents/placenta/data/traces/preprocessed/test/"
# pathTest = "/home/Documents/placenta/pytorch-CycleGAN-and-pix2pix/results/placenta_pix2pix/2017-10-29-test_latest-test/images/"
# pathOutput = "/home/Documents/placenta/data/reconstructed-test/"
# filenameSuffix = "test"

# # call each script
# exec(open("./reassembleTranslation0.py").read(), globals())
# exec(open("./reassembleOverlapping.py").read(), globals())
# exec(open("./reassembleFinal.py").read(), globals())

### VALIDATION  ###############################################################

# paths
# pathTraces = "/home/Documents/placenta/data/traces/preprocessed/val/"
# pathTest = "/home/Documents/placenta/pytorch-CycleGAN-and-pix2pix/results/placenta_pix2pix/2017-10-29-test_latest-val/images/"
# pathOutput = "/home/Documents/placenta/data/reconstructed-val/"
# filenameSuffix = "val"

# # call each script
# exec(open("./reassembleTranslation0.py").read(), globals())
# exec(open("./reassembleOverlapping.py").read(), globals())
# exec(open("./reassembleFinal.py").read(), globals())

### TRAINING  #################################################################

# # paths
# pathTraces = "/home/Documents/placenta/data/traces/preprocessed/train/"
# pathTest = "/home/Documents/placenta/pytorch-CycleGAN-and-pix2pix/results/placenta_pix2pix/2017-10-29-test_latest-train/images/"
# pathOutput = "/home/Documents/placenta/data/reconstructed-train/"
# filenameSuffix = "train"

# # call each script
# exec(open("./reassembleTranslation0.py").read(), globals())
# exec(open("./reassembleOverlapping.py").read(), globals())
# exec(open("./reassembleFinal.py").read(), globals())


### UNC IMAGES ################################################################

# paths
# pathTraces = "/home/Documents/placenta-v2/data/multiscale-filter-img/traces/preprocessed"
# pathTest = "/home/Documents/placenta/pytorch-CycleGAN-and-pix2pix/results/placenta_pix2pix/2017-12-03-test_latest/images/"
# pathOutput = "/home/Documents/placenta-v2/data/multiscale-filter-img/reconstructed/"
# filenameSuffix = "UNC"

# paths
pathTraces = "/home/Documents/placenta-v2/data/Methodist/traces/preprocessed"
pathTest = "/home/Documents/placenta/pytorch-CycleGAN-and-pix2pix/results/placenta_pix2pix/test_latest/images/"
pathOutput = "/home/Documents/placenta-v2/data/Methodist/reconstructed/"
filenameSuffix = "Methodist"

# call each script
exec(open("./reassembleTranslation0.py").read(), globals())
exec(open("./reassembleOverlapping.py").read(), globals())
exec(open("./reassembleFinal.py").read(), globals())

# plt.close("all")