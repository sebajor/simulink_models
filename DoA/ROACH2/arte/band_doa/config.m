%always check the fft/unscramble to set the reorder 
%parameter in the sync_gen! we set a dictionary like obj to save some
%sync values

model_name = 'spec4in';

%parameters
bw = 600;  %mhz
fft_size = 12;

pfb_taps = 3;
pfb_inwidth = 8;
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

%% 
fft_vals =          {7,8,9,10,11,12,13,14,15,16,17};
unscramble_values = [2,5,3, 7, 4, 9, 5,11, 6,13, 7];
reorder_vals = containers.Map(fft_vals, unscramble_values);
%%

disp(['This bw needs a fpga clk:', num2str(bw/4)]);

%write adc clock and fpga clock
disp('Writing adc and fpga clocks');
adc0_name = strcat(model_name, '/asiaa_adc5g0');
adc1_name = strcat(model_name, '/asiaa_adc5g1');
xsg_name = strcat(model_name, '/XSG_core_config');

set_param(adc0_name, 'adc_clk_rate', num2str(2*bw));
set_param(adc1_name, 'adc_clk_rate', num2str(2*bw));
set_param(xsg_name, 'clk_rate', num2str(bw/4));



%write pfb and ffts
disp('Update pfbs');
pfb0_name = strcat(model_name, '/pfb_fir_real0');
pfb1_name = strcat(model_name, '/pfb_fir_real1');
pfb2_name = strcat(model_name, '/pfb_fir_real2');
pfb3_name = strcat(model_name, '/pfb_fir_real3');

pfb = {pfb0_name, pfb1_name, pfb2_name, pfb3_name};


for i = [1:1:4]
    set_param(pfb{i}, 'PFBSize', int2str(fft_size));
    set_param(pfb{i}, 'TotalTaps', int2str(pfb_taps));
    set_param(pfb{i}, 'BitWidthOut', int2str(pfb_outwidth));
    set_param(pfb{i}, 'BitWidthIn', int2str(pfb_inwidth));
    set_param(pfb{i},'add_latency', int2str(pfb_add_lat));
    set_param(pfb{i}, 'mult_latency', int2str(pfb_mult_lat));
    set_param(pfb{i}, 'bram_latency', int2str(pfb_bram_lat));
    set_param(pfb{i}, 'fan_latency', int2str(pfb_fanout_lat));
    set_param(pfb{i}, 'conv_latency', int2str(pfb_convert_lat));
end

disp('Update FFTs');
fft0_name = strcat(model_name, '/fft_wideband_real0');
fft1_name = strcat(model_name, '/fft_wideband_real1');
fft2_name = strcat(model_name, '/fft_wideband_real2');
fft3_name = strcat(model_name, '/fft_wideband_real3');
ffts = {fft0_name, fft1_name, fft2_name, fft3_name};

for i = [1:1:4]
    set_param(ffts{i},'FFTSize', int2str(fft_size));
    set_param(ffts{i},'input_bit_width', int2str(pfb_outwidth));
    set_param(ffts{i},'bin_pt_in', int2str(pfb_outwidth-1));
    set_param(ffts{i},'add_latency', int2str(fft_add_lat));
    set_param(ffts{i},'mult_latency', int2str(fft_mult_lat));
    set_param(ffts{i},'bram_latency', int2str(fft_bram_lat));
    set_param(ffts{i},'conv_latency', int2str(fft_convert_lat));
    set_param(ffts{i},'input_latency', int2str(fft_input_lat));
end

%fft shift value
const_name = strcat(model_name, '/Constant1');
set_param(const_name, 'n_bits', '32');
set_param(const_name, 'const', int2str(2^(fft_size)-1));

const_name = strcat(model_name, '/Constant10');
set_param(const_name, 'n_bits', '32');
set_param(const_name, 'const', int2str(2^(fft_size)-1));

const_name = strcat(model_name, '/Constant3');
set_param(const_name, 'n_bits', '32');
set_param(const_name, 'const', int2str(2^(fft_size)-1));

const_name = strcat(model_name, '/Constant5');
set_param(const_name, 'n_bits', '32');
set_param(const_name, 'const', int2str(2^(fft_size)-1));

%fft power
disp('Update power blocks');
for i = [1:1:16]
   pow_name =  strcat(model_name, '/power',int2str(i));
   set_param(pow_name,'BitWidth', int2str(pfb_outwidth))
   set_param(pow_name,'add_latency', int2str(pow_add_lat))
   set_param(pow_name,'mult_latency', int2str(pow_mult_lat))
end

%set the correspondant delay to sync the power
set_param(strcat(model_name, '/pipeline72'), 'latency', int2str(pow_add_lat+pow_mult_lat));
set_param(strcat(model_name, '/pipeline90'), 'latency', int2str(pow_add_lat+pow_mult_lat));
set_param(strcat(model_name, '/pipeline103'), 'latency', int2str(pow_add_lat+pow_mult_lat));
set_param(strcat(model_name, '/pipeline122'), 'latency', int2str(pow_add_lat+pow_mult_lat));


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
for i = [0:1:15]
   acc_name = strcat(model_name, '/simple_bram_vacc_0_', int2str(i));
   set_param(acc_name, 'vec_len', int2str(2^(fft_size-1-3)));
   set_param(acc_name, 'n_bits', int2str(acc_out));
   set_param(acc_name, 'bin_pt', int2str(pow_point));
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
for i = [0:1:3]
   bram_name = strcat(model_name, '/dout_0a_', int2str(i));
   set_param(bram_name, 'addr_width', int2str(bram_addr));
   set_param(bram_name, 'data_width', int2str(acc_out));

   bram_name = strcat(model_name, '/dout_0c_', int2str(i));
   set_param(bram_name, 'addr_width', int2str(bram_addr));
   set_param(bram_name, 'data_width', int2str(acc_out));

   bram_name = strcat(model_name, '/dout_1a_', int2str(i));
   set_param(bram_name, 'addr_width', int2str(bram_addr));
   set_param(bram_name, 'data_width', int2str(acc_out)); 


   bram_name = strcat(model_name, '/dout_1c_', int2str(i));
   set_param(bram_name, 'addr_width', int2str(bram_addr));
   set_param(bram_name, 'data_width', int2str(acc_out)); 
end

%update bram counter 
set_param(strcat(model_name, '/Counter1'), 'n_bits', int2str(fft_size-3));
set_param(strcat(model_name, '/Counter2'), 'n_bits', int2str(fft_size-3));
set_param(strcat(model_name, '/Counter3'), 'n_bits', int2str(fft_size-3));
set_param(strcat(model_name, '/Counter4'), 'n_bits', int2str(fft_size-3));

%acclen_ctrl
for i=[0:1:3]
    acc_ctrl_name = strcat(model_name, '/acc_cntrl',int2str(i));
    set_param(acc_ctrl_name, 'chan_bits', int2str(fft_size-3));
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
