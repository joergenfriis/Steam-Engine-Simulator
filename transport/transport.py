# transport.py
#
# Modul, der styrer den arduino,
# som styrer frekvensomformeren, og dermed transportbaandet.
#
# Slaveadresse 0x32
#
# Programmet sender en streng med 2 bytes til arduinoen.
# Foerste byte kan vaere 0 eller 1 for hhv slukket og taendt motor.
# Andet byte er et tal mellem 0 og 255, der angiver motorens hastighed.
#
# 23.01.2018 Joergen Friis
#**************************************************************************

import smbus
import sys
import time

bus = smbus.SMBus(1)

def TransportStop():
    # Try up to 30 times on a faliure
    Success = False
    caught_exception = None
    for _ in range(30):
        try:
            bus.write_i2c_block_data(0x32,0,[0,0])
            Success = True
            break
        except:
            #print("Unexpected error: ", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Transportbaand stop failed after 30 retries")
    #if Success:
        #print("Transportbaand stoppet")
    return -1

def TransportGo(speed):
    # Try up to 30 times on a faliure
    Success = False
    caught_exception = None
    for _ in range(30):
        try:
            bus.write_i2c_block_data(0x32,0,[1,speed])
            Success = True
            break
        except:
            #print("Unexpected error: ", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Transportbaand go failed after 30 retries")
    #if Success:
        #print("Transportbaand koerer. Speed = ",speed)
    return -1
