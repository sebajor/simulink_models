import calandigital as calan
import numpy as np
from numpy.linalg import eigh
import time
import matplotlib.pyplot as plt

###
### Author: Sebastian Jorquera
###

roach_ip = '192.168.1.18'
boffile = 'eigen_test.bof.gz'

n = 16
seed = 10
read_size = n*(n+1)/2
iters = 100

np.set_printoptions(precision=3)
##
##start test
##

def meas_test(roach):
    roach.write_int('rst',1)
    roach.write_int('rst',0)
    time.sleep(0.1)
    start = time.time()
    bram_data = np.frombuffer(roach.read('dout', read_size*2), '>h')/2.**15
    aux = bram_data[::-1].tolist()    ##order backwards becouse pop takes the last one

    matrix = np.zeros([n,n])
    for i in range(n):
        for j in range(i,n):
            matrix[i,j] = aux.pop()
    eigval, eigvec = eigh(matrix, UPLO='U')
    end = time.time()
    elapsed = (end-start)*1000
    print('Read+solve eigen problem took %.3f ms' %((end-start)*1000))
    return eigval, eigvec, elapsed 

    


roach = calan.initialize_roach(roach_ip, boffile=boffile, upload=1)

roach.write_int('rst',1)
roach.write_int('seed', seed)
roach.write_int('read_size', read_size)

roach.write_int('rst',0)

roach.write_int('en',1)
time.sleep(1)

print('Done signal: %i' %roach.read_int('done'))
test_time = np.zeros(iters)
for i in range(iters):
    eigval, eigvec, elapsed = meas_test(roach)
    test_time[i] = elapsed

plt.plot(test_time)
plt.xlabel('Iteration')
plt.ylabel('ms')
plt.title('PC time for reading and solving eigen problem')
plt.grid()
plt.tight_layout()
plt.savefig('pc_time.png')
plt.close()
