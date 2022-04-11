%%  Author: Sebastian Jorquera
model_name = 'preliminar';
bw = 600;           %mhz


%spectrometer params
fft_pow_shift = 13;
fft_pow_width = 20;
fft_pow_point = 19;

%spectrometers acc
fft_pow_acc_width = 32; %should match the bram size



%fft conversion (before centrosym)
fft_delay = 0;
fft_shift = 0;
fft_conv_width = 18;
fft_conv_point = 17;


%correlator
corr_din_width = fft_conv_width+1;
corr_din_point = fft_conv_point;
corr_vect_len = 512;
corr_acc_width = 20;
corr_acc_point = 16;
corr_dout_width = 32;





%%
disp('Configure spectrometer parameters');
for i=(0:1:1)
    name = strcat(model_name, '/power_convert', int2str(i));
    set_param(name, 'shift_val', int2str(fft_pow_shift));
    set_param(name, 'conv_width', int2str(fft_pow_width));
    set_param(name, 'conv_point', int2str(fft_pow_point));
end

disp('Configure spectrometer accumulators');
for i=(0:1:7)
    name = strcat(model_name, '/simpel_bram_vacc_0_', int2str(i));
    set_param(name, 'n_bits', int2str(fft_pow_acc_width));
    set_param(name, 'bin_pt', int2str(fft_pow_point));
end

disp('Configure spectrometer brams');
for i=(0:1:3)
    name = strcat(model_name, 'dout0_a0_', int2str(i));
    set_param(name, 'data_width', int2str(fft_pow_acc_width));
end

for i=(0:1:3)
    name = strcat(model_name, 'dout0_c0_', int2str(i));
    set_param(name, 'data_width', int2str(fft_pow_acc_width));
end


%%centrosymmetric stuffs

disp('Set the fft convertion and delay');
name = strcat(model_name, '/fft0_delay');
set_param(name, 'lat', int2str(fft_delay));

name = strcat(model_name, '/fft1_delay');
set_param(name, 'lat', int2str(fft_delay));

name = strcat(model_name, '/fft0_conv');
set_param(name, 'shift_val', int2str(fft_shift));
set_param(name, 'conv_width', int2str(fft_conv_width));
set_param(name, 'conv_point', int2str(fft_conv_point));

name = strcat(model_name, '/fft1_conv');
set_param(name, 'shift_val', int2str(fft_shift));
set_param(name, 'conv_width', int2str(fft_conv_width));
set_param(name, 'conv_point', int2str(fft_conv_point));


disp('Set centrosymmetric parameters');
for i=(0:1:3)
    name = strcat(model_name, '/centrosym', int2str(i));
    set_param(name, 'din_width', int2str(fft_conv_width));
    set_param(name, 'din_point', int2str(fft_conv_point));
end


disp('Configuring accumulators');
for i=(0:1:3)
    name = strcat(model_name, '/correlator', int2str(i));
    set_param(name, 'din_width', int2str(corr_din_width));
    set_param(name, 'din_point', int2str(corr_din_point));
    set_param(name, 'vector_len', int2str(corr_vect_len));
    set_param(name, 'acc_width', int2str(corr_acc_width));
    set_param(name, 'acc_point', int2str(corr_acc_point));
    set_param(name, 'dout_width', int2str(corr_dout_width));
end


