%% Author: Sebastian Jorquera
function [fft_re0,fft_im0,fft_re1,fft_im1,fft_re2,fft_im2,fft_re3,fft_im3] = fft_inputs(din)

din_re = din.r';    din_re = din_re(:);
din_im = din.i';    din_im = din_im(:);

val0_re = din_re(1:4:end); val0_im = din_im(1:4:end);
val1_re = din_re(2:4:end); val1_im = din_im(2:4:end);
val2_re = din_re(3:4:end); val2_im = din_im(3:4:end);
val3_re = din_re(4:4:end); val3_im = din_im(4:4:end);

fft_re0.time=[]; fft_im0.time=[];
fft_re1.time=[]; fft_im1.time=[];
fft_re2.time=[]; fft_im2.time=[];
fft_re3.time=[]; fft_im3.time=[];

fft_re0.signals.values=(val0_re/2^15);   fft_im0.signals.values=(val0_im/2^15);
fft_re1.signals.values=(val1_re/2^15);   fft_im1.signals.values=(val1_im/2^15);
fft_re2.signals.values=(val2_re/2^15);   fft_im2.signals.values=(val2_im/2^15);
fft_re3.signals.values=(val3_re/2^15);   fft_im3.signals.values=(val3_im/2^15);

fft_re0.dimensions=1;       fft_im0.dimensions=1;
fft_re1.dimensions=1;       fft_im1.dimensions=1;
fft_re2.dimensions=1;       fft_im2.dimensions=1;
fft_re3.dimensions=1;       fft_im3.dimensions=1;


end
