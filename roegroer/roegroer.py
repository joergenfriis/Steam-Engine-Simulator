# roegroer.py
#
# modul, der aflaeser aabningen i fen roegroer.
#
# Slaveadresse er 0x35
#
# Programmet laeser en streng med 5 byte fra Arduinoen.
# Vaerdien er mellem 0 og 100, og angiver hvor mange procvent det enkelte
# roer er aabent.
#
# Joergen Friis 13.12.2017
#
##############################################################################

import smbus
import time
import sys

bus = smbus.SMBus(1)

def Read_roegroer():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            data = bus.read_i2c_block_data(0x35, 0)
            Success = True
            break
        except:
            print("Unexpected error: ",sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        roer = data
        print("Roer 1 = ",roer[0]," %")
        print("Roer 2 = ",roer[1]," %")
        print("Roer 3 = ",roer[2]," %")
        print("Roer 4 = ",roer[3]," %")
        print("Roer 5 = ",roer[4]," %")
    return roer

def Test_roegroer():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            data = bus.read_i2c_block_data(0x35, 0)
            Success = True
            break
        except:
            print("Unexpected error: ",sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        roer = data
        print("Roer 1 = ",roer[0]," mm")
    return roer


    
    
