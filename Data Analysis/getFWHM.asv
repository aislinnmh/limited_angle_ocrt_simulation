% function [fwhm_x,fwhm_z,psf_x,psf_z] = getFWHM(bscan,lat_FOV,ax_FOV)
% 
% [zpixels Ascans] = size(bscan)
% umpp_x = lat_FOV/Ascans*1000;
% umpp_z = ax_FOV/zpixels*1000;
% 
% 
% % average multiple next
% bscan = rescale(bscan);
% [j,i] = find(bscan>0.6); % row, col
% length(i)
% 
% % map = zeros(zpixels,Ascans);
% % for k = 1:length(i)
% %     map(j(k),i(k))=1;
% % end
% % imshow(map)
% 
% % FWHM Lateral
% zbeadi = unique(i);
% % create an array with all detected beads centered
% center = Ascans/2+1;
% centered_stack = [];
% for k = 1:length(zbeadi)
%     zi = zbeadi(k);
%     line = squeeze(bscan(:,zi));
% 
%     maximum = max(line);
%     beadj = find(line==maximum);
%     beadj = beadj(1); % only one bead per line if encountered
% 
%     diff = center-beadj;
%     centered = circshift(line,diff);
%     centered_stack = [centered_stack centered];
% end
% combinedPSF = mean(centered_stack,2);
% figure(1)
% plot(combinedPSF(center-20:center+20))
% halfmax = max(combinedPSF)/2;
% tol = 0.1;
% halfmax_js = find(abs(combinedPSF-halfmax)<=tol);
% if length(halfmax_js) < 2
%     tol = 0.15;
%     halfmax_js = find(abs(combinedPSF-halfmax)<=tol);
% end
% if length(halfmax_js)>2
%     temp = zeros(1,2);
%     temp(1) = mean(halfmax_js(halfmax_js<center));
%     temp(2) = mean(halfmax_js(halfmax_js>center));
%     halfmax_js = temp;
% end
% fwhm_x = (halfmax_js(2)-halfmax_js(1))*umpp_x;
% psf_x = combinedPSF;
% 
% 
% 
% % FWHM Axial
% xbeadj = unique(j);
% % create an array with all detected beads centered
% center = zpixels/2+1;
% centered_stack = [];
% for k = 1:length(xbeadj)
%     xj = xbeadj(k);
%     line = squeeze(bscan(xj,:)).';
% 
%     maximum = max(line);
%     beadi = find(line==maximum);
%     beadi = beadi(1); % only one bead per line if encountered
% 
%     diff = center-beadi;
%     centered = circshift(line,diff);
%     centered_stack = [centered_stack centered];
% end
% combinedPSF = mean(centered_stack,2);
% figure(2)
% plot(combinedPSF(center-20:center+20))
% halfmax = max(combinedPSF)/2;
% tol = 0.1;
% halfmax_is = find(abs(combinedPSF-halfmax)<=tol);
% if length(halfmax_is) < 2
%     tol = 0.15;
%     halfmax_is = find(abs(combinedPSF-halfmax)<=tol);
% end
% if length(halfmax_is)>2
%     temp = zeros(1,2);
%     temp(1) = mean(halfmax_is(halfmax_is<center));
%     temp(2) = mean(halfmax_is(halfmax_is>center));
%     halfmax_is = temp;
% end
% fwhm_z = (halfmax_is(2)-halfmax_is(1))*umpp_x;
% psf_z = combinedPSF;
% 
% end


function [fwhm_x,fwhm_z,psf_x,psf_z] = getFWHM(bscan,lat_FOV,ax_FOV)

[zpixels Ascans] = size(bscan);
umpp_x = lat_FOV/Ascans*1000;
umpp_z = ax_FOV/zpixels*1000;


% average multiple next
bscan = rescale(bscan);
[j,i] = find(bscan>0.6); % row, col
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
psf = combinedPSF(center-15:center+15);
figure(1)
plot(psf,'.k')
% Fit to gaussian
f = fit(1:length(psf),psf,'gauss1')


% 
% % FWHM Axial
% xbeadj = unique(j);
% % create an array with all detected beads centered
% center = zpixels/2+1;
% centered_stack = [];
% for k = 1:length(xbeadj)
%     xj = xbeadj(k);
%     line = squeeze(bscan(xj,:)).';
% 
%     maximum = max(line);
%     beadi = find(line==maximum);
%     beadi = beadi(1); % only one bead per line if encountered
% 
%     diff = center-beadi;
%     centered = circshift(line,diff);
%     centered_stack = [centered_stack centered];
% end
% combinedPSF = mean(centered_stack,2);
% figure(2)
% plot(combinedPSF(center-20:center+20))


end