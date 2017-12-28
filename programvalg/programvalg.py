# programvalg.py
#
# modul, der aflaeser programvaelgerens stilling
#
# Slave adresse 0x41
# Der laeses en byte fra slaven med vaerdien:
# 1: Demo mode
# 2: Exhibition mode
# 3: Realistic mode
# 4: Exhibition mode with commando bridge
#
# Joergen Friis 28.12.2017
#
#*****************************************************************************

import smbus
import time
import sys

bus = smbus.SMBus(1)

def read():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            data = bus.read_i2c_block_data(0x41, 0)
            Success = True
            break
        except:
            print("Unexpected error: ",sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        programvalg = data[1]
        print("Programvalg = ",programvalg)
    return programvalg
