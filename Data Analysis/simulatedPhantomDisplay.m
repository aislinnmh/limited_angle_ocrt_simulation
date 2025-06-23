clear;clc;

load_directory = 'C:/Users/DEL-AIProjects/Documents/GitHub/limited_angle_ocrt_local_saves/Datasets/90-6-90/';
sample_id = 'phantom';
data = load([load_directory sample_id '_data.mat']).Bscans;
%% 
