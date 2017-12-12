# primaerluft.py
#
# modul, der aflaeser det primaere luftspjaelds stilling.
#
# Slaveadresse er 0x34
#
# Programmet laeser en streng med 1 byte fra Arduinoen.
# Vaerdien er mellem 0 og 100, og angiver hvor mange procent
# primaerluftspjaeldet er aabent.
#
# Joergen Friis 12.12.2017
#
################################################################################

import smbus
import time
import sys


bus = smbus.SMBus(1)

def Read_primaerluft():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            data = bus.read_i2c_block_data(0x34, 0)
            Success = True
            break
        except:
            print("Unexpected error: ",sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        primaerluft = data[0]
        print("Primaer luft = ",primaerluft," %")
    return primaerluft

            
    
