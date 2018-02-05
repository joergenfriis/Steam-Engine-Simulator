# model.py
#
# modul, der styrer Arduino slaven paa dampmaskinemodellen.
#
# Slaveadresse er 0x52
#
# Programmet sender en streng med 3 bytes til Arduinoen.
# Foerste byte er et tal mellem 0 og 100, der angiver den tilfoerte energi.
# Andet byte er et tal mellem 0 og 100, der angiver omstyringens stilling.
# 50 er neutral stilling.
# Tredje byte er 0 eller 1. 1 angiver at modellen skal resettes.
#
# 24.11.2017 Joergen Friis
#******************************************************************

import smbus
import time
import servo
import sys

bus = smbus.SMBus(1)

def ModelStop():
    # Try up to 30 times on a faliure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x52, 0, [0,50,0])
            Success = True
            break
        except:
            #print("Unexpected error:", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Model stop Failed after 30 retries")
    if Success:
        servo.gangskifte(50)
        time.sleep(10)
        #print('model stop')
    return -1

def ModelRun(energi,gear):
    # Try up to 30 times on a faliure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x52, 0, [energi,gear,0])
            Success = True
            break
        except:
            #print("Unexpected error:", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Model run failed after 30 retries")
    if Success:
        servo.gangskifte(gear)
        #print('model run, energi= {} og gear = {}'.format(energi,gear))
    return -1

def ModelReset():
    # Try up to 30 times on a faliure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x52, 0, [0,50,1])
            Success = True
            break
        except:
            #print("Unexpected error:", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Model reset failed after 30 retries")
    if Success:
        servo.gangskifte(50)
        time.sleep(10)
        #print('model reset')
    return -1
