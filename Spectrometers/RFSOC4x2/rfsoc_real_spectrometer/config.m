model_name = 'rfsoc_spectrometer';
fft_size = 12;

pfb_taps = 3;
pfb_inwidth = 16;
pfb_outwidth = 18;

pow_add_lat = 2;
pow_mult_lat = 3;

%the power is calculated full scale then you could reduce it
pow_shift = 1;  %left shift
pow_resize = 20;
pow_point = 15;

acc_out = 32;   %only could be 8,16,32,64,128 to match the brams

%latencies
pfb_add_lat = 1;
pfb_mult_lat = 2;
pfb_bram_lat = 3;
pfb_fanout_lat = 2;
pfb_convert_lat = 1;

fft_add_lat = 1;
fft_mult_lat = 2;
fft_bram_lat = 3;
fft_input_lat = 2;
fft_convert_lat = 3;

pre_power_lat = 2;
post_power_lat = 1;
pre_bram_lat = 2;

%% 
fft_vals =          {7,8,9,10,11,12,13,14,15,16,17};
unscramble_values = [2,5,3, 7, 4, 9, 5,11, 6,13, 7];
reorder_vals = containers.Map(fft_vals, unscramble_values);
%%

%write pfb and ffts
disp('Update pfbs');
for i=[0:1:3]
    pfb_name = strcat(model_name, '/pfb_fir_real',int2str(i));
    set_param(pfb_name, 'PFBSize', int2str(fft_size));
    set_param(pfb_name, 'TotalTaps', int2str(pfb_taps));
    set_param(pfb_name, 'BitWidthOut', int2str(pfb_outwidth));
    set_param(pfb_name, 'BitWidthIn', int2str(pfb_inwidth));
    set_param(pfb_name,'add_latency', int2str(pfb_add_lat));
    set_param(pfb_name, 'mult_latency', int2str(pfb_mult_lat));
    set_param(pfb_name, 'bram_latency', int2str(pfb_bram_lat));
    set_param(pfb_name, 'fan_latency', int2str(pfb_fanout_lat));
    set_param(pfb_name, 'conv_latency', int2str(pfb_convert_lat));
end

disp('Update ffts');
for i=[0:1:3]
    fft_name = strcat(model_name, '/fft_wideband_real', int2str(i));
    set_param(fft_name,'FFTSize', int2str(fft_size));
    set_param(fft_name,'input_bit_width', int2str(pfb_outwidth));
    set_param(fft_name,'bin_pt_in', int2str(pfb_outwidth-1));
    set_param(fft_name,'add_latency', int2str(fft_add_lat));
    set_param(fft_name,'mult_latency', int2str(fft_mult_lat));
    set_param(fft_name,'bram_latency', int2str(fft_bram_lat));
    set_param(fft_name,'conv_latency', int2str(fft_convert_lat));
    set_param(fft_name,'input_latency', int2str(fft_input_lat));
end

%fft shift value
const_name = strcat(model_name, '/Constant6');
set_param(const_name, 'n_bits', '32');
set_param(const_name, 'const', int2str(2^(fft_size)-1));

%pre,post power delay
disp('Update pre-post power delay');
for i=[0:1:3]
    name = strcat(model_name, '/pre_power_delay', int2str(i));
    set_param(name, 'delay', int2str(pre_power_lat));
    name = strcat(model_name, '/post_power_delay', int2str(i));
    set_param(name, 'delay', int2str(post_power_lat));
end

%power
disp('Update powers');
for i=[0:1:3]
    name = strcat(model_name, '/power', int2str(i));
    set_param(name,'din_width', int2str(pfb_outwidth))
    set_param(name,'add_lat', int2str(pow_add_lat))
    set_param(name,'mult_lat', int2str(pow_mult_lat))
end


%convert power output
disp('Convert the output power');
for i=[0:1:3]
    pow_conv_name = strcat(model_name, '/power_convert', int2str(i));
    set_param(pow_conv_name, 'shift_val', int2str(pow_shift));
    set_param(pow_conv_name, 'conv_width', int2str(pow_resize));
    set_param(pow_conv_name, 'conv_point', int2str(pow_point));
end

%accumultors
disp('Update accumulators');
for i=[0:1:3]
    name = strcat(model_name, '/accs', int2str(i));
    set_param(name, 'vector_len',int2str(2^(fft_size-1-3)));
    set_param(name, 'dout_width',int2str(acc_out));
    set_param(name, 'dout_point',int2str(pow_point));
end

%brams
if acc_out == 32
   bram_addr =  max([fft_size-3, 10]);
elseif acc_out == 64
   bram_addr = max([fft_size-3, 9]);
elseif acc_out == 16
   bram_addr = max([fft_size-3, 11]);
else
    bram_addr = fft_size-3;
end


disp('Update brams');
for i=[0:1:3]
    adc = strcat(model_name, '/adc', int2str(i));
    for j=[0:1:3]
        name = strcat(adc, '_', int2str(j));
        set_param(name, 'addr_width',int2str(bram_addr));
        set_param(name, 'data_width', int2str(acc_out));
    end
end

%update bram counter
for i=[0:1:3]
    name = strcat(model_name, '/counter', int2str(i));
    set_param(name, 'n_bits', int2str(fft_size-3));
end

%acclen_ctrl
for i=[0:1:3]
    name = strcat(model_name, '/acc_cntrl', int2str(i));
    set_param(name, 'chan_bits', int2str(fft_size-3));
end

%sync stuffs
disp('Update sync stuffs');

sync_gen_name = strcat(model_name, '/sync_gen');
set_param(sync_gen_name, 'fft_size', int2str(2^fft_size));
set_param(sync_gen_name, 'fft_simult_inputs', '8');
set_param(sync_gen_name, 'pfb_fir_taps', int2str(pfb_taps));
reorder_vec = strcat('[2,2,',int2str(reorder_vals(fft_size)),']');       %always check the reorder!!
set_param(sync_gen_name, 'reorder_vec', reorder_vec);

%finally update the model
disp('Update the whole model with ctrl+D');
%set_param(model_name, 'SimulationCommand', 'update');

