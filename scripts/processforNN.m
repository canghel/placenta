processforNN

Files = dir('*.*');

for k = 1:length(Files)
   FileNames = Files(k).name;
   [~,~,ext] = fileparts(FileNames);
   c = strcmp(ext,'.png');
   if c == 1
       cropandrotate(FileNames)
   else
   end
end

