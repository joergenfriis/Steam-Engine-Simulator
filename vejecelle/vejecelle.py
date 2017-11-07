# vejecelle.py
#
# Modul, der styrer den Arduino, der aflæser og resetter vejecellerne
# under transpoprtbåndet.
#
# Slaveadresse 0x31
#
# Programmet sender et byte til Arduinoen, der styrer reset, og det modtager
# et int fra arduinoen med den vejede masse i gram.
#
#****************************************************************************
import smbus
import time

bus = smbus.SMBus(1)

def Reset_vejecelle():
    bus.write_i2c_block_data(0x31,0,[1, 0, 0])
    return -1

def Read_vejecelle():
    data = bus.read_i2c_block_data(0x31,0)
    reset = data[0]
    msb = data[1]
    lsb = data[2]
    masse = msb * 256 + lsb
    return masse
