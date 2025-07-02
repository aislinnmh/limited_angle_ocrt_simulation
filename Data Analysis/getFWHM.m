
function [fwhm_x,fwhm_z,psf_x,psf_z] = getFWHM(bscan,lat_FOV,ax_FOV,max_angle,interval)

[zpixels Ascans] = size(bscan);
umpp_x = lat_FOV/Ascans*1000;
umpp_z = ax_FOV/zpixels*1000;

anglename = [num2str(max_angle) '-' num2str(interval) '-' num2str(max_angle)];
save_dir = ['C:/Users/bundr/Documents/Research/Robotic OCRT/Limited Angle Project/Results/' anglename '/'];

% average multiple next

bscan = rescale(bscan);
[j,i] = find(islocalmax(bscan,'MinProminence',0.8)); % row, col
length(i)

% map = zeros(zpixels,Ascans);
% for k = 1:length(i)
%     map(j(k),i(k))=1;
% end
% imshow(map)

% FWHM Lateral
zbeadi = unique(i);
% create an array with all detected beads centered
center = Ascans/2+1;
centered_stack = [];
for k = 1:length(zbeadi)
    zi = zbeadi(k);
    line = squeeze(bscan(:,zi));

    maximum = max(line);
    beadj = find(line==maximum);
    beadj = beadj(1); % only one bead per line if encountered
    
    diff = center-beadj;
    centered = circshift(line,diff);
    centered_stack = [centered_stack centered];
end
combinedPSF = mean(centered_stack,2);
w = 10;
psf = combinedPSF(center-w:center+w);
psf = psf - min(psf);
f1 = figure(1);
clf(1)
% Fit to gaussian
f = fit((1:length(psf)).',psf,'gauss1','Exclude', (psf<0.15))
if max_angle==0
    f = fit((1:length(psf)).',psf,'gauss1','Exclude', (psf<0.2) + (psf>=0.9))
end
hold on
plot(psf,'.k')
plot(f)
legend('','','location','northeastoutside')
hold off
sigma = f.c1;
fwhm_x = sigma * 2.35482 * umpp_x
psf_x = psf;


saveas(f1, [save_dir 'psf_x.png'])


% FWHM Axial
xbeadj = unique(j);
% create an array with all detected beads centered
center = zpixels/2+1;
centered_stack = [];
for k = 1:length(xbeadj)
    xj = xbeadj(k);
    line = squeeze(bscan(xj,:)).';

    maximum = max(line);
    beadi = find(line==maximum);
    beadi = beadi(1); % only one bead per line if encountered

    diff = center-beadi;
    centered = circshift(line,diff);
    centered_stack = [centered_stack centered];
end
combinedPSF = mean(centered_stack,2);
w = 10;
psf = combinedPSF(center-w:center+w);
psf = psf - min(psf);
f2 = figure(2);
% Fit to gaussian
f = fit((1:length(psf)).',psf,'gauss1','Exclude', (psf<0.14))
clf(2)
hold on
plot(psf,'.k')
plot(f)
legend('','','location','northeastoutside')
hold off
sigma = f.c1;
fwhm_z = sigma * 2.35482 * umpp_z
psf_z = psf;

saveas(f2, [save_dir 'psf_z.png'])
end