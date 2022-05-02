%% Author:   Sebastian Jorquera

acc_len = 64;
sim_len = (2*acc_len+10)*512;
model_name = 'basic_sim';
filename = 'tone.hdf5';

rfi_shift = 7;


%%read the file and generate the inputs
adc0 = h5read(filename, '/adc0');
adc1 = h5read(filename, '/adc1');
adc3 = h5read(filename, '/adc3');

%set accumulation len
set_param(strcat(model_name, '/Constant'),'const', int2str(acc_len));

%get fft inputs
[fft0_re0, fft0_im0, fft0_re1, fft0_im1, fft0_re2, fft0_im2, ...
    fft0_re3, fft0_im3] = fft_inputs(adc0);

[fft1_re0, fft1_im0, fft1_re1, fft1_im1, fft1_re2, fft1_im2, ...
    fft1_re3, fft1_im3] = fft_inputs(adc1);

[fft3_re0, fft3_im0, fft3_re1, fft3_im1, fft3_re2, fft3_im2, ...
    fft3_re3, fft3_im3] = fft_inputs(adc3);

%create the sync signal for the fft
sync = zeros(512,1);
sync(end) = 1;
sync_fft0.time = [];                sync_fft3.time = [];
sync_fft0.signals.values = sync;    sync_fft3.signals.values = sync;
sync_fft0.dimensions = 1;           sync_fft3.dimensions=1;


%start simulation
disp('Simulation running!');
simulation = sim(model_name, 'StartTime','0','StopTime',int2str(sim_len-1));

%end simulation and read the outputs
disp('Reading outputs');
beam_re = [];
beam_im = [];
rfi_re = [];
rfi_im = [];
for i=(0:1:3)
    aux = strcat('beam_re',int2str(i));
    dout = simulation.get(aux).Data(:);
    beam_re = [beam_re, dout];
    aux = strcat('beam_im',int2str(i));
    dout = simulation.get(aux).Data(:);
    beam_im = [beam_im, dout];
    aux = strcat('rfi_re',int2str(i));
    dout = simulation.get(aux).Data(:);
    rfi_re = [rfi_re, dout];
    aux = strcat('rfi_im',int2str(i));
    dout = simulation.get(aux).Data(:);
    rfi_im = [rfi_im, dout];
end
rfi = rfi_re+1i*rfi_im;
beam = beam_re+1i*beam_im;
%deinterleave data
disp('Deinterleave data');
beam_data = deinterleave_data(beam, 2048);
rfi_data = deinterleave_data(rfi, 2048);


dout_frames = size(beam_data);
avg_rfi = mean(abs(rfi_data)')';
avg_beam = mean(abs(beam_data)')';

%gold values
gold_rfi = abs(adc3.r(1:dout_frames(2),:)+1i*adc3.i(1:dout_frames(2),:))/2^(15-rfi_shift);
avg_rfi_gold = mean(gold_rfi);
gold_beam = adc0.r(1:dout_frames(2),:)+adc1.r(1:dout_frames(2),:)+ ...
    1i*(adc0.i(1:dout_frames(2),:)+adc1.i(1:dout_frames(2),:));
avg_beam_gold = mean(abs(gold_beam))/2^(15-rfi_shift);


figure;
subplot(121);
plot(avg_rfi);
plot(avg_rfi_gold, 'r');
legend('rtl', 'gold');
title('RFI convertion output');
subplot(122);
plot(avg_rfi-avg_rfi_gold');
title('RFI convertion Error');

disp(strcat('Max error RFI :', num2str(max(abs(avg_rfi-avg_rfi_gold')))))

figure;
subplot(121);
plot(avg_beam);
plot(avg_beam_gold, 'r');
legend('rtl', 'gold');
title('Beam convertion output');
subplot(122);
plot(avg_rfi-avg_rfi_gold');
title('Beam convertion Error');

disp(strcat('Max error Beam :', num2str(max(abs(avg_beam-avg_beam_gold')))))


%% Accumulation
corr_dout = [];
pow_dout = [];
for i=(0:1:3)
   aux = strcat('pow', int2str(i)); 
   dout = simulation.get(aux).Data(:);
   pow_dout = [pow_dout, dout];
   aux = strcat('corr', int2str(i)); 
   dout = simulation.get(aux).Data(:);
   corr_dout = [corr_dout, dout];
end


corr_data = deinterleave_data(corr_dout, 2048);
pow_data = deinterleave_data(pow_dout, 2048);




