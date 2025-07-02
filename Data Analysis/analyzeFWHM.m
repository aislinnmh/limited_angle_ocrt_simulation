
max_angle = 0;
interval = 6;
anglename = [num2str(max_angle) '-' num2str(interval) '-' num2str(max_angle)];

if max_angle == 0
    load_directory = ['c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Datasets/18-6-18/']
    result = load([load_directory sample_id '_data.mat']);
    bscan = squeeze(result.Bscans(4,:,:)).';
    bscan = imresize(bscan,[1024 1024]);
    lat_FOV = 1.5;
    ax_FOV = 2.22;
else
    save_directory = ['c:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/saved_models_and_variables/' anglename '/'];
    sample_id = 'phantom';
    result = load([save_directory sample_id '_result.mat']);
    bscan = result.recon;
    lat_FOV = 3;
    ax_FOV;
end

[fwhm_x,fwhm_z,psf_x,psf_z] = getFWHM(bscan,lat_FOV,ax_FOV);