import numpy as np
import matplotlib.pyplot as plt
import struct
import ipdb


f = file('data', 'rb')
iters = 762
byte_chunk = 220*200*36
chunk = 220*200*9
last = np.zeros(9)
fail0 = []
fail1 = []
fail2 = []
last = np.zeros([3,3])
fail_acc = []
lost_pkt = []
for i in range(iters):
    #ipdb.set_trace()
    print(i)
    raw_data = f.read(byte_chunk)
    dat = np.array(struct.unpack(str(chunk)+'I', raw_data))
    dat = dat.reshape(chunk/9,3,3)
    err0 = np.sum(last-dat[0,:,:])
    if(err0!=-9*3):
        fail0.append(i)
    a0 = dat[:,:,0].flatten(); a1 = dat[:,:,1].flatten(); a2 = dat[:,:,2].flatten()
    b0 = np.diff(a0); b1 = np.diff(a1); b2 = np.diff(a2)
    c0 = np.sum(a0-a1); c1 = np.sum(a1-a2)
    err0 = np.where(b0!=1); err1 = np.where(b1!=1); err2 = np.where(b2!=1)
    if((len(err0[0])+len(err1[0])+len(err2[0]))!=0):
        fail1.append(i)
        fail_acc.append(len(err0[0]))
        lost_pkt.append(np.sum(a0[err0[0]+1]-a0[err0[0]]))
        print(err0)
        print(err1)
        print(err2)
    if(c0+c1 != chunk/3*2):
        fail2.append(i)
    last = dat[-1,:,:]

f.close()









