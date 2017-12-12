# vejecelle.py
#
# Modul, der styrer den Arduino, der aflaeser og resetter vejecellerne
# under transportbaandet.
#
# Slaveadresse 0x31
#
# Programmet sender et byte til Arduinoen, der styrer reset, og det modtager
# et int fra arduinoen med den vejede masse i gram.
#
# Joergen Friis 12.12.2017
#
#****************************************************************************
import smbus
import time
import sys

bus = smbus.SMBus(1)

def Reset_vejecelle():
     # Try up to 30 times on a faliure
    Success = False
    caught_exception = None
    for _ in range(30):
        try:
            bus.write_i2c_block_data(0x31,0,[1,0,0])
            Success = True
            break
        except:
            print("Unexpected error: ", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Vejecelle resat")
    return -1



def Read_vejecelle():
    # Try up to 30 times on a faliure
    Success = False
    caught_exception = None
    for _ in range(30):
        try:
            bus.read_i2c_block_data(0x31,0)
            Success = True
            break
        except:
            print("Unexpected error: ", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        reset = data[0]
        msb = data[1]
        lsb = data[2]
        masse = msb * 256 + lsb
        print("Vejecelle viser: ",masse," gram")
    return masse
