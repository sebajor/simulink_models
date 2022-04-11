import argparse
import numpy as np
import calandigital as calan
import time

parser = argparse.ArgumentParser(
    description="intialize roach")

parser.add_argument("-i", "--ip", dest="ip", default=None,
    help="ROACH IP address.")
parser.add_argument("-b", "--boffile", dest="bof",
    help="Boffile to load into the FPGA.")

parser.add_argument("-u", "--upload", dest="upload", action="store_true",
    help="If used, upload .bof from PC memory (ROACH2 only).")

def main():
    args = parser.parse_args()
    roach = calan.initialize_roach(args.ip, boffile=args.bof, upload=args.upload)
    time.sleep(1)
    roach.write_int('cnt_rst',3)
    time.sleep(1)
    roach.write_int('cnt_rst',0)
    roach.write_int('snap_trig',1)

if __name__  == '__main__':
    main()

