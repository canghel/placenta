function cropandrotate(filename, imgdir)
%========================================================================== 
% Syntax
%       cropandrotate(filename, imgdir)
%==========================================================================
% Input
%   filename - grayscale or color image from the file specified by the 
%              string FILENAME. FILENAME must be in the current directory, 
%              in a directory on the MATLAB path, or include a full or 
%              relative path to a file.
%   imgdir   - directory in which the sub-images are saved.
%
% Output
%   For each images, saves sub-images of size 256 x 256, each rotated by 0, 
%   90, 180 and 270 degres.
%==========================================================================
% Reference : imrotate, imwrite
% Author   	: Karamatou Yacoubou Djima
% Created	: Jul 31, 2017 at 12:36
% Revised	: Jul 31, 2017 at 12:36
%==========================================================================

% imgdir = '/Users/kyacouboudjima/Dropbox (Amherst College)/Research/Projects/WAMB/placenta-traces/CroppedforNN/';

% Initialize variables and parameters
img = imread(filename);
[n,m,~] = size(img);
nofr = floor(n/256);
nofc = floor(m/256);
imgnum = 1;
alpha = [90,180,270]; % Rotation angles

% Crop and rotate images
for i = 1:nofr
    for j = 1:nofc
        % Crop a 256x256 sub-image from img
        subimg = img(1+(i-1)*256:i*256, 1+(j-1)*256:256*j,:);
        subimgname = strcat(imgdir,filename,'_Part_',num2str(imgnum),...
           '_Angle_','0','.png');      
        imwrite(subimg,subimgname,'png'); 
        %  Rotate the first 256x256 sub-image by angle defined by alpha
        for k = 1:3
            sumimgrot = imrotate(subimg,alpha(k));
            subimgname = strcat(imgdir,filename,'_Part_',num2str(imgnum),...
               '_Angle_',num2str(alpha(k)),'.png');
            imwrite(sumimgrot,subimgname,'png');
        end
        imgnum = imgnum + 1;
    end
end

end
