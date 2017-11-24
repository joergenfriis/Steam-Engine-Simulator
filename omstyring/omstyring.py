# omstyring.py
#
# modul, der styrer Arduino slaven paa omstyringshaandtaget.
#
# Slaveadresse er 0x29
#
# Programmet laeser en streng med 2 bytes fra Arduinoen:
# Byte 0 indeholder 0, hvis stillingen af omstyringshaandtaget ikke  er aendret,
# og 1, hvis haandtaget er blevet flyttet.
# Byte 1 indeholder et tal mellem 0 og 255, der angiver omstyringshaandtagets stilling.
# 0 er fuld kraft frem og 255 er fuld kraft bak,
#
# Joergen Friis 15.11.2017
#
#######################################################################################

import smbus
import time

bus = smbus.SMBus(1)

def Read_omstyring():
    print('Omstyring read')
    data = bus.read_i2c_block_data(0x29, 0)
    status = data[0]
    omstyring = data[1]
    return omstyring
    
