# plot diagonistic plots
# - a box plot of train, val and test before and after averaging the 
#   overlapping squares

### PREAMBLE ##################################################################

library(BoutrosLab.plotting.general);
library(scales)

### FUNCTIONS #################################################################

concatenateData <- function(results, inputFile, dataset, averaged){
	temp <- read.table(inputFile, quote="")$V1;
	numValues <- length(temp);
	if (averaged){
		temp <- cbind(temp, rep(dataset, numValues), rep('avg', numValues));
	} else {
		temp <- cbind(temp, rep(dataset, numValues), rep('non-avg', numValues));
	}
	results <- rbind(results, temp);
	return(results);
}

### LOAD MCC VALUES AND CREATE DATAFRAME ######################################

pathOutput <- '/home/Documents/placenta/data';

mccResults <- NULL;

# train
mccResults <- concatenateData(mccResults,
	inputFile = file.path(pathOutput, 'reconstructed-train', '2017-10-29-trans0-MCC-values-train.txt'),
	dataset = 'train',
	averaged = FALSE);
mccResults <- concatenateData(mccResults,
	inputFile = file.path(pathOutput,'reconstructed-train', '2017-10-29-averaged-MCC-values-train.txt'),
	dataset = 'train',
	averaged = TRUE);
# val
mccResults <- concatenateData(mccResults,
	inputFile = file.path(pathOutput, 'reconstructed-val', '2017-10-29-trans0-MCC-values-val.txt'),
	dataset = 'val',
	averaged = FALSE);
mccResults <- concatenateData(mccResults,
	inputFile = file.path(pathOutput,'reconstructed-val', '2017-10-29-averaged-MCC-values-val.txt'),
	dataset = 'val',
	averaged = TRUE);
# test
mccResults <- concatenateData(mccResults,
	inputFile = file.path(pathOutput, 'reconstructed-test', '2017-10-29-trans0-MCC-values-test.txt'),
	dataset = 'test',
	averaged = FALSE);
mccResults <- concatenateData(mccResults,
	inputFile = file.path(pathOutput,'reconstructed-test', '2017-10-29-averaged-MCC-values-test.txt'),
	dataset = 'test',
	averaged = TRUE);
colnames(mccResults) = c("MCC", "Dataset", "Reconstruction");
mccResults = as.data.frame(mccResults);
mccResults$MCC = as.numeric(as.character(mccResults$MCC));
mccResults$Category = as.factor(paste0(mccResults$Dataset, "-", mccResults$Reconstruction));

xyBounds <- c(0.625, 0.86)

### BOXPlOT CODE ##############################################################

mccResults$Order <- recode.vector(
    mccResults$Category,
    list(
        '1' = 'train-non-avg',
        '2' = 'train-avg',
        '3' = 'val-non-avg',
        '4' = 'val-avg',
        '5' = 'test-non-avg',
        '6' = 'test-avg'
        )
    );

colors <- recode.vector(
    mccResults$Reconstruction,
    list(
        'gray70' = 'non-avg',
        'gray20' = 'avg'
        )
    );

create.boxplot(
    file = file.path(pathOutput, "figures", generate.filename("MCC", "boxplot", "png")),
    formula =  MCC ~ Order, 
    data = mccResults,
    xaxis.cex = 0.8,
    yaxis.cex = 1,
    xlab.cex = 1,
    ylab.cex = 1.3,
    ylab.label = 'MCC',
    add.stripplot = TRUE,
    points.col = colors,
    points.alpha = 1,
    resolution = 1000,
    xaxis.lab = rep(c("Non-avg", "Avg"), 3), 
    xlab.label = c(" Train                         Val                         Test"),
    ylimits = xyBounds,
    main = NULL, 
    # draw rectangle
    add.rectangle = TRUE,
    ybottom.rectangle = -0.1, 
    ytop.rectangle = 1.1, 
    xleft.rectangle = seq(0.5, 7.5, 2),
    xright.rectangle = seq(1.5, 8.5, 2),
    col.rectangle = 'gray83',
    alpha.rectangle = 0.4
    );

### STATS TEST TO CHECK IF AVERAGING HELPED ###################################

wilcoxTest <- list()

# t.test(mccResults$MCC[mccResults$Category=="test-avg"], 
# 	mccResults$MCC[mccResults$Category=="test-non-avg"], paired=TRUE)
# t.test(mccResults$MCC[mccResults$Category=="val-avg"], 
# 	mccResults$MCC[mccResults$Category=="val-non-avg"], paired=TRUE)
# t.test(mccResults$MCC[mccResults$Category=="train-avg"], 
# 	mccResults$MCC[mccResults$Category=="train-non-avg"], paired=TRUE)

wilcoxTest[["test"]] <- wilcox.test(mccResults$MCC[mccResults$Category=="test-avg"], 
	mccResults$MCC[mccResults$Category=="test-non-avg"], paired=TRUE)
wilcoxTest[["val"]] <-  wilcox.test(mccResults$MCC[mccResults$Category=="val-avg"], 
	mccResults$MCC[mccResults$Category=="val-non-avg"], paired=TRUE)
wilcoxTest[["train"]] <- wilcox.test(mccResults$MCC[mccResults$Category=="train-avg"], 
	mccResults$MCC[mccResults$Category=="train-non-avg"], paired=TRUE)

print(wilcoxTest)

### SCATTERPLOT TO SHOW IMPROVEMENT ###########################################

scatterData <- data.frame(
    avg = mccResults$MCC[mccResults[,"Reconstruction"]=="avg"],
    nonavg = mccResults$MCC[mccResults[,"Reconstruction"]=="non-avg"],
    dataset = mccResults$Dataset[mccResults[,"Reconstruction"]=="non-avg"]
    );

# levels(scatterData$dataset) <- c("train", "val", "test")

scatterData$Order <- recode.vector(
    scatterData$dataset,
    list(
        '1' = 'train',
        '2' = 'val',
        '3' = 'test'
        )
    );

scatterData$Order <- as.factor(scatterData$Order)
levels(scatterData$Order) <- c("Train", "Val", "Test");

# sanity check
print("Check if dataset is correct in scatter.data")
print(identical(mccResults$Dataset[mccResults[,"Reconstruction"]=="non-avg"],
	mccResults$Dataset[mccResults[,"Reconstruction"]=="avg"]))

create.scatterplot(
    file = file.path(pathOutput, "figures", generate.filename("MCC", "scatterplot-dataset", "png")),
    height = 6, 
    width = 11,
    formula = avg ~ nonavg | Order,
    data = scatterData,
    main = NULL,
    xlab.label = "Non-averaged MCC",
    ylab.label = "Averaged MCC",
    # xat = seq(0, 16, 2),
    # yat = seq(0, 16, 2),
    xlimits = xyBounds,
    ylimits = xyBounds,
    xaxis.cex = 0.75,
    yaxis.cex = 0.75,
    xaxis.fontface = 1,
    yaxis.fontface = 1,
    xlab.cex = 1.3,
    ylab.cex = 1.3,
    pch = 19,
    col = scales::alpha('gray20', 0.5),
    # set up panel layout
    layout = c(3,1),
    resolution = 1000,
    # add xy line
    add.xyline = TRUE,
    xyline.lty = 3,
    xyline.col = 'grey',
    xyline.lwd = 2
    );