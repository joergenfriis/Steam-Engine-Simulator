# sikkerhedsventil.py
#
# modul, der aabner sikkerhedsventilen kortvarigt
#
# Slaveadresse 0x39
#
# Programmet sender 0 eller 1 til Arduinoen, Ved 1 aabnes
# sikkerhedsventilen i 1 sekund. ved 0 lukkes sikkerhedsventilen.
#
# Joergen Friis 21.12.2017
#
###############################################################################

import smbus
import time
import sys

bus = smbus.SMBus(1)

def sikkerhedsventilOn():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x39,0,[1]) # send 1 til arduinoen
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            #print("Unexpected error:", sys.exc_info() [0])
            # wait a second for the retry
            time.sleep(1)
    if not Success:
        Print("Sikkerhedsventil on failed after 30 retries")
    #if Success:
        #print("Sikkerhedsventil on")
    return -1
 

def sikkerhedsventilOff():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x39,0,[0]) # send 0 til arduinoen
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            #print("Unexpected error:", sys.exc_info() [0])
            # wait a second for the retry
            time.sleep(1)
    if not Success:
        Print("Sikkerhedsventil off failed after 30 retries")
    #if Success:
        #print("Sikkerhedsventil off")
    return -1
