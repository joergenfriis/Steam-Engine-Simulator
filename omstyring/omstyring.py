# omstyring.py
#
# modul, der styrer Arduino slaven paa omstyringshaandtaget.
#
# Slaveadresse er 0x29
#
# Programmet laeser en streng med 2 bytes fra Arduinoen:
# Byte 0 indeholder 0, hvis stillingen af omstyringshaandtaget ikke  er aendret,
# og 1, hvis haandtaget er blevet flyttet.
# Byte 1 indeholder et tal mellem 0 og 100, der angiver omstyringshaandtagets stilling.
# 0 er fuld kraft frem og 100 er fuld kraft bak,
#
# Joergen Friis 26.01.2018
#
#######################################################################################

import smbus
import time
import sys

bus = smbus.SMBus(1)

def Read_omstyring():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range(30):
        try:
            data = bus.read_i2c_block_data(0x29, 0)
            Success = True
            break
        except:
            print("Unexpected error: ",sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        status = data[0]
        omstyring = data[1]
        print('Omstyring read = ',omstyring)
    return omstyring
    
