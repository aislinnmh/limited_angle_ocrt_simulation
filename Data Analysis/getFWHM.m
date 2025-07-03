
function [fwhm_x,fwhm_z,psf_x,psf_z] = getFWHM(bscan,lat_FOV,ax_FOV,max_angle,interval)

[zpixels Ascans] = size(bscan);
umpp_x = lat_FOV/Ascans*1000;
umpp_z = ax_FOV/zpixels*1000;

anglename = [num2str(max_angle) '-' num2str(interval) '-' num2str(max_angle)];
save_dir = ['C:/Users/bundr/Documents/Research/Robotic OCRT/Limited Angle Project/Results/' anglename '/'];

% average multiple next

bscan = rescale(bscan);
[j,i] = find(islocalmax(bscan,'MaxNumExtrema',20,'FlatSelection','center','MinProminence',0.8)); % row, col
length(i)

% map = zeros(zpixels,Ascans);
% for k = 1:length(i)
%     map(j(k),i(k))=1;
% end
% imshow(map)

% FWHM Lateral
zbeadi = unique(i);
fwhm_xs =[];

for k = 1:length(zbeadi)
    zi = zbeadi(k);
    line = squeeze(bscan(:,zi));

    maximum = max(line);
    beadj = find(line==maximum);
    beadj = beadj(1); % only one bead per line if encountered
    
    if beadj >10 && beadj <1014
        w=10;
        psf = line(beadj-w:beadj+w);
        psf = psf - min(psf);
        f = fit((1:length(psf)).',psf,'gauss1','Exclude', (psf<0.1));
        if max_angle==0
            f = fit((1:length(psf)).',psf,'gauss1','Exclude', (psf<0.1) + (psf>=0.9));
        end
        sigma = f.c1;
        fwhm_xs = [fwhm_xs sigma * 2.35482 * umpp_x];
    end
end

f1 = figure(1);
clf(1)

hold on
plot(psf,'.k')
plot(f)
legend('','','location','northeastoutside')
hold off
sigma = f.c1;
fwhm_x = mean(fwhm_xs);
psf_x = psf;


saveas(f1, [save_dir 'psf_x.png'])


% FWHM Axial
xbeadj = unique(j);
fwhm_zs =[];

for k = 1:length(zbeadi)
    xj = xbeadj(k);
    line = squeeze(bscan(xj,:)).';

    maximum = max(line);
    beadi = find(line==maximum);
    beadi = beadi(1); % only one bead per line if encountered
    
    if beadi >10 && beadi <1014
        w=10;
        psf = line(beadi-w:beadi+w);
        psf = psf - min(psf);
        f = fit((1:length(psf)).',psf,'gauss1','Exclude', (psf<0));
        sigma = f.c1;
        fwhm_zs = [fwhm_zs sigma * 2.35482 * umpp_z];
    end
end

f2 = figure(2);
clf(2)

hold on
plot(psf,'.k')
plot(f)
legend('','','location','northeastoutside')
hold off
sigma = f.c1;
fwhm_z = mean(fwhm_zs);
psf_z = psf;

end