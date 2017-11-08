# flowmaaler.py
#
# Modul, der styrer den Arduino, der aflæser og resetter
# flowmåleren på oliepumpen.
#
# Slaveadresse 0x51
#
# Programmet sender et byte til Arduinoen, der styurer reset, og det
# modtager et int fra Arduinoen med det gennemstrømmede volumen i liter.
#
#****************************************************************************
import smbus
import time

bus = smbus.SMBus(1)

def Reset_flowmaaler():
    bus.write_i2c_block_data(0x51,0,[1,0,0])
    return -1

def Read_flowmaaler():
    data = bus.read_i2c_block_data(0x51,0)
    reset = data[0]
    liter = data[1]
    return liter
