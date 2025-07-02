load_directory = 'C:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/data/';
filename = [load_directory 'phantom.mat'];

phantom = load(filename).phantom;
phantom(phantom>0) = log(phantom(phantom>0));
phantom = rescale(phantom);
[m n] = size(phantom); 

% need to resize in order to see tiny beads
scale = 0.1;
phantom = imresize(phantom,scale);
% phantom = rescale(phantom);

f = figure('Position',[50 50 800 800]);

phantom = imrotate(phantom,-90);

% imshow(phantom);
% imagesc(0:0.00025/scale:2.22,0:0.00025/scale:1.5,phantom)
imagesc(0:0.00025/scale:1.5,0:0.00025/scale:2.22,phantom)
axis image
colormap(flipud(gray))
% colorbar
title(['Original Phantom'],'fontsize',16)
saveas(f,[load_directory 'original_phantom.png'])

%%

load_directory = 'C:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Datasets/90-6-90/';
filename = [load_directory 'phantom_data.mat'];

bscans = load(filename).Bscans;
bscan1 = squeeze(bscans(1,:,:));
bscan2 = squeeze(bscans(16,:,:));
bscan3 = squeeze(bscans(31,:,:));

% phantom(phantom>0) = log(phantom(phantom>0));
% phantom = rescale(phantom);
% [m n] = size(phantom); 
x_mmpp = 1.5/500;
z_mmpp = 2.22/2048;

scale = 2;
bscan1 = imresize(bscan1,scale);
bscan2 = imresize(bscan2,scale);
bscan3 = imresize(bscan3,scale);


f = figure('Position',[50 50 1800 1000]);

bscan1 = imrotate(bscan1,90);
bscan2 = imrotate(bscan2,90);
bscan3 = imrotate(bscan3,90);


% subplot(1,3,1)
imagesc(0:z_mmpp/1000*scale:1.5,0:x_mmpp/1000*scale:2.22,bscan1.')
axis image
colormap(flipud(gray))
% colorbar
title(['-90\circ'],'fontsize',16)
saveas(f,[load_directory 'phantom_minus90.png'])

f = figure('Position',[50 50 1800 1000]);

% subplot(1,3,2)
imagesc(0:z_mmpp/1000*scale:1.5,0:x_mmpp/1000*scale:2.22,bscan2.')
axis image
colormap(flipud(gray))
% colorbar
title(['0\circ'],'fontsize',16)
saveas(f,[load_directory 'phantom_0.png'])

f = figure('Position',[50 50 1800 1000]);

% subplot(1,3,3)
imagesc(0:z_mmpp/1000*scale:1.5,0:x_mmpp/1000*scale:2.22,bscan3.')
axis image
colormap(flipud(gray))
% colorbar
title(['90\circ'],'fontsize',16)
saveas(f,[load_directory 'phantom_90.png'])
