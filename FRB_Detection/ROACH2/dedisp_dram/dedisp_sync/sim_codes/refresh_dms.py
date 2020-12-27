import numpy as np
import frbd_64ch_600mhz as frb


accs = np.array(frb.compute_accs())
dm = frb.DMs

fclk = 150.*10**6
n_addr = 2**10
n_chann = 64
parallel = 4

refresh_rate = n_addr*accs/fclk*n_chann/parallel

for i in range(len(accs)):
    print("DM=%i \t refresh rate: %.4f"%(dm[i], refresh_rate[i]))


