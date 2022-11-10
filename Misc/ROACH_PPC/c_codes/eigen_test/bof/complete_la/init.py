import calandigital as calan
import numpy as np
from numpy import linalg as la
import time
import matplotlib.pyplot as plt


def PiMatrix(N):
    PiM = np.zeros((N, N))
    for i in range(N):
        PiM[i, N - i - 1] = 1
    return PiM

def QMatrix(N):
    QM = np.array(np.zeros((N, N)), dtype = np.complex)
    if N % 2 == 0:
        n = int(N / 2)
        QM[0:n, 0:n] = np.eye(n)
        QM[0:n, n::] = 1j * np.eye(n)
        QM[n::, 0:n] = PiMatrix(n)
        QM[n::, n::] = -1j * PiMatrix(n)
    else:
        n = int((N - 1) / 2)
        QM[0:n, 0:n] = np.eye(n)
        QM[0:n, n + 1::] = 1j * np.eye(n)
        QM[n, n] = np.sqrt(2)
        QM[n + 1::, 0:n] = PiMatrix(n)
        QM[n + 1::, n + 1::] = -1j * PiMatrix(n)
    return QM / np.sqrt(2)

def J1Matrix(N):
    J1 = np.zeros((N - 1, N))
    J1[0:N - 1, 0:N - 1] = np.eye(N - 1)
    return J1

def J2Matrix(N):
    J2 = np.zeros((N - 1, N))
    J2[0:N - 1, 1:N] = np.eye(N - 1)
    return J2

def K_subMu(N):
    K_subMu_r = np.array(np.zeros((N - 1, N)), dtype = np.complex)
    K_subMu_r = QMatrix(N - 1).conj().T.dot(J2Matrix(N).dot(QMatrix(N)))
    return K_subMu_r

def K_subNu(M):
    K_subNu_r = np.array(np.zeros((M - 1, M)), dtype = np.complex)
    K_subNu_r = QMatrix(M - 1).conj().T.dot(J2Matrix(M).dot(QMatrix(M)))
    return K_subNu_r

def Kmu1(N, M):
    return np.kron(np.eye(M), K_subMu(N).real)
def Kmu2(N, M):
    return np.kron(np.eye(M), K_subMu(N).imag)
def Knu1(N, M):
    return np.kron(K_subNu(M).real, np.eye(N))
def Knu2(N, M):
    return np.kron(K_subNu(M).imag, np.eye(N))


roach_ip = '192.168.1.18'
boffile = '../eigen_test.bof.gz'

n = 16
seed = 10
read_size = n*(n+1)/2
iters = 100

np.set_printoptions(precision=3)
sources = 5

##doa algebra
def doa_algebra(matrix, n_sources):
    eigval,eigvec = la.eigh(matrix, UPLO='U')
    Es = eigvec[:,-n_sources:]
    inv_x = la.pinv(np.matmul(Kmu1(4,4), Es))
    out_x = np.matmul(inv_x, np.matmul(Kmu2(4,4), Es))
    eigval_x, eigvec_x = la.eig(out_x)

    inv_y = la.pinv(np.matmul(Knu1(4,4), Es))
    out_y = np.matmul(inv_y, np.matmul(Knu2(4,4), Es))
    eigval_y, eigvec_y = la.eig(out_y)
    
    c_problem = out_x+1j*out_y
    out_eigval, out_eigvec = la.eig(c_problem)
    return eigval, eigvec,Es, out_x, out_y, out_eigval



###
### start test
###

def meas_test(roach, n_sources):
    roach.write_int('rst',1)
    roach.write_int('rst',0)
    time.sleep(0.1)
    start = time.time()
    bram_data = np.frombuffer(roach.read('dout', read_size*2), '>h')/2.**15
    aux = bram_data[::-1].tolist()  ##order backwards 
    matrix = np.zeros([n,n])
    for i in range(n):
        for j in range(i+1):
            matrix[j,i] = aux.pop() ##check, should be colmajor
    eigval, eigvec,Es, out_x, out_y, doa = doa_algebra(matrix, n_sources)
    end = time.time()
    elapsed = (end-start)*1000
    print("read+solve took %.3f ms"%elapsed)
    return eigval, eigvec,Es, out_x, out_y, doa, elapsed

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
    eigval, eigvec,Es, mu, nu,doa, elapsed = meas_test(roach, sources)
    test_time[i] = elapsed

plt.plot(test_time)
plt.xlabel('Iteration')
plt.ylabel('ms')
plt.title('PC time for reading and solving eigen problem')
plt.grid()
plt.tight_layout()
plt.savefig('pc_time.png')
plt.close()

