f = 20;
phase = 10;

DFT_channels = 2048;
DFT_len = 4096;
acc_len = 8;
t = [0:1:DFT_len*acc_len-1];
sig0 = 0.5*sin(2*pi*f/DFT_len*t);
sig1 = 0.2*sin(2*pi*f/DFT_len*t+deg2rad(phase));


%reshape signals to take 
sig0 = reshape(sig0, [DFT_len, acc_len]);
sig1 = reshape(sig1, [DFT_len, acc_len]);
sig0 = transpose(sig0);
sig1 = transpose(sig1);

spec0 = fft(sig0, DFT_len, 2)/1025;
spec1 = fft(sig1, DFT_len, 2)/1025;

%reorder the spectrums
spec0_1 = reshape(transpose(spec0(:, 1:DFT_channels)), [1, DFT_channels*acc_len]);
spec1_1 = reshape(transpose(spec1(:, 1:DFT_channels)), [1, DFT_channels*acc_len]);

spec0_ord = reshape(spec0_1, [4,DFT_channels*acc_len/4]);
spec1_ord = reshape(spec1_1, [4,DFT_channels*acc_len/4]);


%ffts outputs
adc0_ch0_re = real(spec0_ord(1,:));
adc0_ch0_im = imag(spec0_ord(1,:));

adc0_ch1_re = real(spec0_ord(2,:));
adc0_ch1_im = imag(spec0_ord(2,:));

adc0_ch2_re = real(spec0_ord(3,:));
adc0_ch2_im = imag(spec0_ord(3,:));

adc0_ch3_re = real(spec0_ord(4,:));
adc0_ch3_im = imag(spec0_ord(4,:));



adc1_ch0_re = real(spec1_ord(1,:));
adc1_ch0_im = imag(spec1_ord(1,:));

adc1_ch1_re = real(spec1_ord(2,:));
adc1_ch1_im = imag(spec1_ord(2,:));

adc1_ch2_re = real(spec1_ord(3,:));
adc1_ch2_im = imag(spec1_ord(3,:));

adc1_ch3_re = real(spec1_ord(4,:));
adc1_ch3_im = imag(spec1_ord(4,:));


%sync signal
sync= zeros(size(adc0_ch0_re));
for i = 1:(acc_len-1)
    sync(i*DFT_channels/4) = 1; %check!
end

%now we need to add some zero samples at the begining
%timeseries(din);
sync_zero = zeros([1,514]);
sync_zero(514) = 1;   %first sync signal check!
zero_trail = zeros([1,514]);

sync_in = timeseries([sync_zero, sync]);
adc0_ch0_re = timeseries([zero_trail, adc0_ch0_re]);
adc0_ch0_im = timeseries([zero_trail, adc0_ch0_im]);
adc0_ch1_re = timeseries([zero_trail, adc0_ch1_re]);
adc0_ch1_im = timeseries([zero_trail, adc0_ch1_im]);
adc0_ch2_re = timeseries([zero_trail, adc0_ch2_re]);
adc0_ch2_im = timeseries([zero_trail, adc0_ch2_im]);
adc0_ch3_re = timeseries([zero_trail, adc0_ch3_re]);
adc0_ch3_im = timeseries([zero_trail, adc0_ch3_im]);

adc1_ch0_re = timeseries([zero_trail, adc1_ch0_re]);
adc1_ch0_im = timeseries([zero_trail, adc1_ch0_im]);
adc1_ch1_re = timeseries([zero_trail, adc1_ch1_re]);
adc1_ch1_im = timeseries([zero_trail, adc1_ch1_im]);
adc1_ch2_re = timeseries([zero_trail, adc1_ch2_re]);
adc1_ch2_im = timeseries([zero_trail, adc1_ch2_im]);
adc1_ch3_re = timeseries([zero_trail, adc1_ch3_re]);
adc1_ch3_im = timeseries([zero_trail, adc1_ch3_im]);


