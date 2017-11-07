# model.py
#
# modul, der styrer Arduino slaven paa dampmaskinemodellen.
#
# Slaveadresse er 0x52
#
# Programmet sender en streng med 3 bytes til Arduinoen.
# Foerste byte er et tal mellem 0 og 255, der angiver den tilfoerte energi.
# Andet byte er et tal mellem 0 og 255, der angiver omstyringens stilling.
# 127 er neutral stilling.
# Tredje byte er 0 eller 1. 1 angiver at modellen skal resettes.
#
# Testet 27.06.2017 Joergen Friis
#******************************************************************

import smbus

bus = smbus.SMBus(1)

def ModelStop():
    print('model stop')
    bus.write_i2c_block_data(0x52, 0, [0,127,0])
    return -1

def ModelRun(energi,gear):
    print('model run, energi= {} og gear = {}'.format(energi,gear))
    bus.write_i2c_block_data(0x52, 0, [energi,gear,0])
    return -1

def ModelReset():
    print('model reset')
    bus.write_i2c_block_data(0x52, 0, [0,127,1])
    return -1

