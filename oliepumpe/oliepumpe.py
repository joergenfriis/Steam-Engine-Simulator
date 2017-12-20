# oliepumpe.py
#
# Modul, der styrer den Arduino, der aflaeser og resetter
# flowmaaleren paa oliepumpen.
#
# Slaveadresse 0x51
#
# Programmet sender et byte til Arduinoen, der styrer reset, og det
# modtager et int fra Arduinoen med det gennemstroemmede volumen i liter.
#
# Joergen Friis 12.12.2017
#
#****************************************************************************
import smbus
import time
import sys

bus = smbus.SMBus(1)

def Reset_flowmaaler():
    # Try up to 30 times on a faliure
    Success = False
    caught_exception = None
    for _ in range(30):
        try:
            bus.write_i2c_block_data(0x51,0,[1,0])
            Success = True
            break
        except:
            print("Unexpected error: ", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Flowmaaler resat")
    return -1


def Read_flowmaaler():
    # Try up to 30 times on a faliure
    Success = False
    caught_exception = None
    for _ in range(30):
        try:
            bus.read_i2c_block_data(0x51,0)
            Success = True
            break
        except:
            print("Unexpected error: ", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        reset = data[0]
        liter = data[1]
        print("Flowmaaleren viser: ",liter)
    return liter

