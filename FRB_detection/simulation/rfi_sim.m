%% Author:   Sebastian Jorquera

acc_len = 64;
sim_len = (acc_len+10)*512;
model_name = 'rfi_sim_model';
filename = 'tone.hdf5';


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
out = [];
for i=(0:1:3)
    aux = strcat('dout',int2str(i));
    dout = simulation.get(aux).Data(:);
    out = [out, dout];
end

%deinterleave data
disp('Deinterleave data');
out_data = deinterleave_data(out, 2048);


