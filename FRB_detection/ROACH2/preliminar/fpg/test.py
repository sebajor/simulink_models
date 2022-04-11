import calandigital as calan
import sys, time
import numpy as np
sys.path.append('codes/')
import control


###
np.random.seed(19)

adc0_delay = np.random.randint(2**20)
adc1_delay = np.random.randint(2**20)
adc2_delay = np.random.randint(2**20)
adc3_delay = np.random.randint(2**20)

acc_len = np.random.randint(2**20)
acc_len0 = np.random.randint(2**20)
acc_len1 = np.random.randint(2**20)
acc_len2 = np.random.randint(2**20)
acc_len3 = np.random.randint(2**20)

theta0 = np.random.randint(2**10)
theta1 = np.random.randint(2**10)
theta2 = np.random.randint(2**10)
theta3 = np.random.randint(2**10)


####
roach_ip = '192.168.1.18'
boffile = 'test.fpg'

roach = calan.initialize_roach(ip=roach_ip, boffile=boffile, upload=1)
time.sleep(1)

roach_control = control.roach_control(roach)

#set acc len
roach_control.set_accumulation(acc_len, num=0)
roach_control.set_accumulation(acc_len0, num=1, thresh=theta0)
roach_control.set_accumulation(acc_len1, num=2, thresh=theta1)
roach_control.set_accumulation(acc_len2, num=3, thresh=theta2)
roach_control.set_accumulation(acc_len3, num=4, thresh=theta3)

#set adc delay
roach_control.set_adc_latencies(0, adc0_delay)
roach_control.set_adc_latencies(1, adc1_delay)
roach_control.set_adc_latencies(2, adc2_delay)
#roach_control.set_adc_latencies(3, adc3_delay)

time.sleep(1)

##check the data
assert (roach.read_int('adc0_delay') == adc0_delay)
assert (roach.read_int('adc1_delay') == adc1_delay)
assert (roach.read_int('adc2_delay') == adc2_delay)
#assert (roach.read_int('adc_delay3') == adc_delay3)


assert (roach.read_int('acc_len') == acc_len)
assert (roach.read_int('acc_len0') == acc_len0)
assert (roach.read_int('acc_len1') == acc_len1)
assert (roach.read_int('acc_len2') == acc_len2)
assert (roach.read_int('acc_len3') == acc_len3)


assert (roach.read_int('theta0')//2**20 == theta0)
assert (roach.read_int('theta1')//2**20 == theta1)
assert (roach.read_int('theta2')//2**20 == theta2)
assert (roach.read_int('theta3')//2**20 == theta3)

print('Everything looks good :)')

