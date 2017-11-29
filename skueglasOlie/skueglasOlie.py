# skueglasOlie.py
#
# Modul, der styrer den Arduino, der regulerer vaeskestanden i skueglasset med olie.
#
# Slave adresse 0x38
#
# Programmet sender et heltal til Arduinoen:
# 0-100 angiver hvor mange % glasset skal vaere fyldt.
# 110 angiver at glasset skal fyldes yderligere 1 %
# 111 angiver at glasset skal draenes for 1 %
# 112 angiver at skueglasset skal resettes til 0 %
#
# Joegen Friis 29.11.2017
#****************************************************************************

import smbus
import time
import sys

bus = smbus.SMBus(1)

def set(niveau):
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x38,0,[niveau]) # send niveau til arduinoen
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0])
            # wait a second for the retry
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Skueglas olie ",niveau," %")
    return -1


def plus1():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x38,0,[110]) # send 110 til arduinoen
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0])
            # wait a second for the retry
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Skueglas olie plus 1 %")
    return -1

def minus1():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x38,0,[111]) # send 111 til arduinoen
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0])
            # wait a second for the retry
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Skueglas olie minus 1 %")
    return -1

def reset():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x38,0,[112]) # send 112 til arduinoen
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0])
            # wait a second for the retry
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Skueglas olie resat")
    return -1
