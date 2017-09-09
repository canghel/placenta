% processforNN

% Files = dir('*.*');
% 
% for k = 1:length(Files)
%    FileNames = Files(k).name;
%    [~,~,ext] = fileparts(FileNames);
%    c = strcmp(ext,'.png');
%    if c == 1
%        cropandrotate(FileNames)
%    else
%    end
% end

% Files = dir('*.*');
addpath(pwd);
Files = dir('/Users/user/Documents/Data/placenta/TestPhotos/*.*');
inputdir = '/Users/user/Documents/Data/placenta/TestPhotos/';
imgdir = '/Users/user/Documents/Data/placenta/TestPhotosCroppedForNN/';

oldFolder = cd(inputdir);

for k = 1:length(Files)
   FileNames = Files(k).name;
   [~,~,ext] = fileparts(FileNames);
   c = strcmp(ext,'.png');
   if c == 1
       cropandrotateLarge(FileNames, imgdir)
   else
   end
end

cd(oldFolder);

