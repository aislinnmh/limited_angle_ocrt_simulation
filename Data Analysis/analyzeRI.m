max_angles = [90, 60, 30, 18, 90, 90];
intervals = [6, 6, 6, 6, 18, 30];

sample_id = 'mouse_vas_deferens1';

RI_data = {};
RI_data.max_angles = [180, max_angles,0];
RI_data.intervals = [6,intervals,0];
tube_RI_list = [];
sample_RI_list =[];

%% Full result

save_directory = ['c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/saved_models_and_variables/'];

RI = load([save_directory sample_id '_result.mat']).RI;
RI = imrotate(RI,-90);

    % x left-right, z up-down
    RI = imrotate(RI,-90);

% crop to focus on sample
ystart = 88;
xoff = 44;
RI = RI(ystart:end, xoff:256-xoff);

f = figure(1);
imshow(RI,[min(RI,[],'all') max(RI,[],'all')])
colormap(jet)
colorbar


% Choose ROI
 title('Choose Tube ROI')

 roi = drawrectangle;
 xmin = roi.Position(1);
 xmin1=xmin
 ymin = roi.Position(2);
 ymin1=ymin
 width = roi.Position(3);
 height = roi.Position(4);
 width1 = width;
 height1 = height;


 ymax = ymin + height;
 xmax = xmin + width;

 f = figure(1);
 btemp = RI;
 w = 1;

title('Choose Sample ROI')

 roi = RI(ymin:ymax,xmin:xmax);
 btemp(ymin-w:ymin+w,xmin-w:xmax+w) = 0;
 btemp(ymax-w:ymax+w,xmin-w:xmax+w) = 0;
 btemp(ymin-w:ymax+w,xmin-w:xmin+w) = 0;
 btemp(ymin-w:ymax+w,xmax-w:xmax+w) = 0;

roi2 = drawrectangle;
 xmin = roi2.Position(1);
 xmin2 = xmin
 ymin = roi2.Position(2);
 ymin2 = ymin
 width = roi2.Position(3);
 height = roi2.Position(4);
  width2 = width;
 height2 = height;

 ymax = ymin + height;
 xmax = xmin + width;

 roi2 = RI(ymin:ymax,xmin:xmax);
 btemp(ymin-w:ymin+w,xmin-w:xmax+w) = 0;
 btemp(ymax-w:ymax+w,xmin-w:xmax+w) = 0;
 btemp(ymin-w:ymax+w,xmin-w:xmin+w) = 0;
 btemp(ymin-w:ymax+w,xmax-w:xmax+w) = 0;

f=figure(3);
imshow(btemp,[min(RI,[],'all') max(RI,[],'all')])
colormap(jet)
colorbar
title(['0\circ'],'fontsize',16)

saveas(f,[save_directory sample_id '_RIROI.png'])

%% Calculate RIs
tubeRI = mean(roi,'all');
sampleRI = mean(roi2,'all');
tube_RI_list = [tube_RI_list tubeRI];
sample_RI_list = [sample_RI_list sampleRI];

%% Limited 
for i = 1:length(max_angles)

max_angle = max_angles(i);
interval = intervals(i);

n_RIs = round(max_angle/interval)*2+1;
anglename = [num2str(max_angle) '-' num2str(interval) '-' num2str(max_angle)];

save_directory = ['c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/saved_models_and_variables/' anglename '/'];

result = load([save_directory sample_id '_result.mat']);
RI = result.RI;

RI = RI;
    % x left-right, z up-down
    RI = imrotate(RI,-90);
RI = RI(xoff:256-xoff,ystart:end);
    f = figure(1);
    imshow(RI,[min(RI,[],'all') max(RI,[],'all')])
    colormap(jet)
    colorbar
     
    % Choose ROI
     % roi = drawrectangle;
     % xmin = roi.Position(1)
     % ymin = roi.Position(2)
     % width = roi.Position(3)
     % height = roi.Position(4)
     
     xmin = xmin1
     ymin = ymin1

     ymax = ymin + height1;
     xmax = xmin + width1;

f = figure(1);
 btemp = RI;
 w = 1;
 roi = RI(ymin:ymax,xmin:xmax);
 btemp(ymin-w:ymin+w,xmin-w:xmax+w) = 0;
 btemp(ymax-w:ymax+w,xmin-w:xmax+w) = 0;
 btemp(ymin-w:ymax+w,xmin-w:xmin+w) = 0;
 btemp(ymin-w:ymax+w,xmax-w:xmax+w) = 0;


 xmin = xmin2
     ymin = ymin2

     ymax = ymin + height2;
     xmax = xmin + width2;
      roi2 = RI(ymin:ymax,xmin:xmax);
 btemp(ymin-w:ymin+w,xmin-w:xmax+w) = 0;
 btemp(ymax-w:ymax+w,xmin-w:xmax+w) = 0;
 btemp(ymin-w:ymax+w,xmin-w:xmin+w) = 0;
 btemp(ymin-w:ymax+w,xmax-w:xmax+w) = 0;

imshow(btemp,[min(RI,[],'all') max(RI,[],'all')])
colormap(jet)
colorbar

% title([num2str(max_angle) '\circ to -' num2str(max_angle) '\circ in ' num2str(interval) '\circ intervals'],'fontsize',16)
saveas(f,[save_directory sample_id '_RIROI.png'])

tubeRI = mean(roi,'all');
sampleRI = mean(roi2,'all');
tube_RI_list = [tube_RI_list tubeRI];
sample_RI_list = [sample_RI_list sampleRI];
end

%%
RI_data.tube_RI = tube_RI_list;
RI_data.sample_RI = sample_RI_list;


%% Plot
RILimitedRange = [];
RILimitedSampling = [];
for i = 1:length(RI_data.tube_RI)
    if RI_data.intervals(i) == 6 
        n = round(RI_data.max_angles(i)/RI_data.intervals(i))*2+1;
        data = [RI_data.max_angles(i) RI_data.intervals(i) RI_data.tube_RI(i) RI_data.sample_RI(i) n];
        RILimitedRange = [RILimitedRange; data];
    end
    if RI_data.max_angles(i) == 90 || RI_data.max_angles(i) == 180
        n = round(RI_data.max_angles(i)/RI_data.intervals(i))*2+1;
        data = [RI_data.max_angles(i) RI_data.intervals(i) RI_data.tube_RI(i) RI_data.sample_RI(i) n];
        RILimitedSampling = [RILimitedSampling; data];
    end
end
%%
f = figure('Position',[100 100 500 400]);
gt = RILimitedRange(1,3);
hold on
plot([0 380],[gt gt],'k--','linewidth',0.5,'color',[0.3 0.3 0.3])
% plot(RILimitedRange(1,1)*2,RILimitedRange(1,3),'*k','markersize',10,'linewidth',2);
plot(RILimitedRange(:,1)*2,RILimitedRange(:,3),'--','linewidth',2,'color',[0 0.5 0.8]);
plot(RILimitedRange(:,1)*2,RILimitedRange(:,3),'.k','linewidth',2,'markersize',20);
legend('Ground Truth','fontsize',14,'location','southeast')
% legend('Ground Truth','Fully Sampled OCRT','fontsize',14,'location','southeast')
hold off
ax = gca;
ax.FontSize = 18;
ylabel('Estimated RI','fontsize',20,'fontweight','bold')
xlabel('Total Angular Sampling Range (\circ)','fontsize',20,'fontweight','bold')
xticks([0 60 120 180 360])
ylim([1 1.8])
xlim([0 380])


title({'Effect of angular range on estimated tube RI','given constant 6\circ interval'},'fontsize',16)

save_directory = ['c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Results/' sample_id];
saveas(f,[save_directory '_limited_range_plot_tube.png'])
%%

f = figure('Position',[100 100 500 400]);
hold on
plot([0 380],[gt gt],'k--','linewidth',0.5,'color',[0.3 0.3 0.3])
plot(RILimitedSampling(:,2),RILimitedSampling(:,3),'--','linewidth',2,'color',[0.8 0.4 0.2]);
plot(RILimitedSampling(:,2),RILimitedSampling(:,3),'.k','linewidth',2,'markersize',20);
legend(['Ground Truth'],'fontsize',14,'location','southeast')
hold off
ax = gca;
ax.FontSize = 18;
set(gca,'xdir','reverse')

ylabel('Estimated RI','fontsize',20,'fontweight','bold')
xlabel('Angular Sampling Interval (\circ)','fontsize',20,'fontweight','bold')
xticks([6:6:30])
xlim([0 36])
ylim([1 1.8])

title({'Effect of angular interval on estimated tube RI','given constant 180\circ range'},'fontsize',16)

save_directory = ['c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Results/' sample_id];
saveas(f,[save_directory '_limited_sampling_plot_tube.png'])

%%

f = figure('Position',[100 100 500 400]);
hold on
plot(RILimitedRange(:,5),RILimitedRange(:,3),'-.','linewidth',2,'color',[0 0.5 0.8]);
plot(RILimitedSampling(:,5),RILimitedSampling(:,3),'--','linewidth',2,'color',[0.8 0.4 0.2]);
% plot([31 31],[0 80],'k:','linewidth',1.5)
plot(RILimitedRange(2,5),RILimitedRange(2,3),'k^','linewidth',2,'markersize',10);
plot(RILimitedRange(1,5),RILimitedRange(1,3),'kdiamond','markersize',10,'linewidth',2)
plot([0 380],[gt gt],'k--','linewidth',0.5,'color',[0.3 0.3 0.3])
plot(RILimitedRange(3:end,5),RILimitedRange(3:end,3),'.k','linewidth',2,'markersize',20);
plot(RILimitedSampling(3:end,5),RILimitedSampling(3:end,3),'.k','linewidth',2,'markersize',20);
legend('Increasing Angular Range','Decreasing Angular Interval','180\circ Range, 6\circ Interval Sampling','Fully Sampled OCRT','Ground Truth','fontsize',12,'location','southeast')

hold off
ax = gca;
ax.FontSize = 18;
ylabel('Estimated RI','fontsize',20,'fontweight','bold')
xlabel('Total # of Angular Samples','fontsize',20,'fontweight','bold')
xlim([0 68])
ylim([1 1.8])
title({'Effect of total angular samples on tube RI'},'fontsize',14)

save_directory = ['c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Results/' sample_id];
saveas(f,[save_directory '_RI_combined_plot_tube.png'])
%%
f = figure('Position',[100 100 500 400]);
gt = RILimitedRange(1,4);
hold on
plot([0 380],[gt gt],'k--','linewidth',0.5,'color',[0.3 0.3 0.3])
% plot(RILimitedRange(1,1)*2,RILimitedRange(1,4),'diamondk','markersize',10,'linewidth',2);
plot(RILimitedRange(:,1)*2,RILimitedRange(:,4),'--','linewidth',2,'color',[0 0.5 0.8]);
plot(RILimitedRange(:,1)*2,RILimitedRange(:,4),'.k','linewidth',2,'markersize',20);
legend(['Ground Truth'],'fontsize',14,'location','southeast')
hold off
ax = gca;
ax.FontSize = 18;
ylabel('Estimated RI','fontsize',20,'fontweight','bold')
xlabel('Total Angular Sampling Range (\circ)','fontsize',20,'fontweight','bold')
xticks([0 60 120 180 360])
xlim([0 380])
ylim([1 1.5])

title({'Effect of angular range on estimated sample RI','given constant 6\circ interval'},'fontsize',16)

save_directory = ['c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Results/' sample_id];
saveas(f,[save_directory '_limited_range_plot_sample.png'])
%%
f = figure('Position',[100 100 500 400]);
hold on
plot([0 380],[gt gt],'k--','linewidth',0.5,'color',[0.3 0.3 0.3])
plot(RILimitedSampling(2:end,2),RILimitedSampling(2:end,4),'--','linewidth',2,'color',[0.8 0.4 0.2]);
plot(RILimitedSampling(2:end,2),RILimitedSampling(2:end,4),'.k','linewidth',2,'markersize',20);
legend(['Ground Truth'],'fontsize',14,'location','southeast')
hold off
ax = gca;
ax.FontSize = 18;
set(gca,'xdir','reverse')

ylabel('Estimated RI','fontsize',20,'fontweight','bold')
xlabel('Angular Sampling Interval (\circ)','fontsize',20,'fontweight','bold')
xticks([6:6:30])
xlim([0 36])
ylim([1 1.5])

title({'Effect of angular interval on estimated sample RI','given constant 180\circ range'},'fontsize',16)

save_directory = ['c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Results/' sample_id];
saveas(f,[save_directory '_limited_sampling_plot_sample.png'])

%%

f = figure('Position',[100 100 500 400]);
hold on
plot(RILimitedRange(:,5),RILimitedRange(:,4),'-.','linewidth',2,'color',[0 0.5 0.8]);
plot(RILimitedSampling(:,5),RILimitedSampling(:,4),'--','linewidth',2,'color',[0.8 0.4 0.2]);
plot(RILimitedRange(2,5),RILimitedRange(2,4),'k^','linewidth',2,'markersize',10);
% plot([31 31],[0 80],'k:','linewidth',1.5)
plot(RILimitedRange(1,5),RILimitedRange(1,4),'diamondk','markersize',10,'linewidth',2)
plot([0 380],[gt gt],'k--','linewidth',0.5,'color',[0.3 0.3 0.3])

plot(RILimitedRange(3:end,5),RILimitedRange(3:end,4),'.k','linewidth',2,'markersize',20);
plot(RILimitedSampling(3:end,5),RILimitedSampling(3:end,4),'.k','linewidth',2,'markersize',20);

legend('Increasing Angular Range','Decreasing Angular Interval','180\circ Range, 6\circ Interval Sampling','Fully Sampled OCRT','Ground Truth','fontsize',12,'location','southeast')

hold off
ax = gca;
ax.FontSize = 18;
ylabel('Estimated RI','fontsize',20,'fontweight','bold')
xlabel('Total # of Angular Samples','fontsize',20,'fontweight','bold')
xlim([0 68])
ylim([1 1.5])
title({'Effect of total angular samples on sample RI'},'fontsize',14)

save_directory = ['c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Results/' sample_id];
saveas(f,[save_directory '_RI_combined_plot_sample.png'])