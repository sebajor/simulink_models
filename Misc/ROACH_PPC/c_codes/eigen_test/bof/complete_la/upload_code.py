import telnetlib
import time, os


def upload_code(roach_ip, filename):
    tn = telnetlib.Telnet(roach_ip, 7147)
    tn.write("?uploadbof 3000 " + filename + "\n")
    time.sleep(1)
    os.system("nc " + roach_ip + " 3000 < " + filename)
    print tn.read_very_eager()
    tn.close()

   
