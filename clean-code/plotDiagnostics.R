# plot diagonistic plots
# - a box plot of train, val and test before and after averaging the 
#   overlapping squares

### PREAMBLE ##################################################################

library(BoutrosLab.plotting.general);

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
	inputFile = file.path(pathOutput, 'reconstructed-train', '2017-10-27-trans0-MCC-values-train.txt'),
	dataset = 'train',
	averaged = FALSE);
mccResults <- concatenateData(mccResults,
	inputFile = file.path(pathOutput,'reconstructed-train', '2017-10-27-averaged-MCC-values-train.txt'),
	dataset = 'train',
	averaged = TRUE);
# val
mccResults <- concatenateData(mccResults,
	inputFile = file.path(pathOutput, 'reconstructed-val', '2017-10-27-trans0-MCC-values-val.txt'),
	dataset = 'val',
	averaged = FALSE);
mccResults <- concatenateData(mccResults,
	inputFile = file.path(pathOutput,'reconstructed-val', '2017-10-27-averaged-MCC-values-val.txt'),
	dataset = 'val',
	averaged = TRUE);
# test
mccResults <- concatenateData(mccResults,
	inputFile = file.path(pathOutput, 'reconstructed-test', '2017-10-27-trans0-MCC-values-test.txt'),
	dataset = 'test',
	averaged = FALSE);
mccResults <- concatenateData(mccResults,
	inputFile = file.path(pathOutput,'reconstructed-test', '2017-10-27-averaged-MCC-values-test.txt'),
	dataset = 'test',
	averaged = TRUE);
colnames(mccResults) = c("MCC", "Dataset", "Reconstruction");
mccResults = as.data.frame(mccResults);
mccResults$MCC = as.numeric(as.character(mccResults$MCC));
mccResults$Category = as.factor(paste0(mccResults$Dataset, "-", mccResults$Reconstruction));

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

#colorPalette <- c('gray70', 'gray70', 'gray50', 'gray50', 'gray20', 'gray20')

colors <- recode.vector(
    mccResults$Reconstruction,
    list(
        'gray70' = 'non-avg',
        'gray20' = 'avg'
        )
    );

create.boxplot(
    file = file.path(pathOutput, generate.filename("MCC", "boxplot", "png")),
    formula =  MCC ~ Order, 
    data = mccResults,
    xaxis.cex = 0.8,
    yaxis.cex = 1,
    xlab.cex = 1,
    ylab.cex = 1.3,
    ylab.label = 'MCC',
    add.stripplot = TRUE,
    points.col = colors, #colorPalette[as.numeric(mccResults$Order)],
    points.alpha = 1,
    resolution = 1000,
    xaxis.lab = rep(c("non-avg", "avg"), 3), 
    xlab.label = c(" Train                         Val                         Test"),
    ylimits = c(0.65, 0.87),
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