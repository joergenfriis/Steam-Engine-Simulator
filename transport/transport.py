# transport.py
#
# Modul, der styrer den arduino,
# som styrer frekvensomformeren, og dermed transportbåndet.
#
# Slaveadresdse 0x32
#
# Programmet sender en streng med 2 bytes til arduinoen.
# Første byte kan være 0 eller 1 for hhv slukket og tændt motor.
# Andet byte er et tal mellem 0 og 255, der angiver motorens hastighed.
#
# Testet 02.02.2017 Jørgen Friis
#**************************************************************************

import smbus

bus = smbus.SMBus(1)

def TransportStop():
    bus.write_i2c_block_data(0x32,0,[0,0])
    return -1

def TransportGo(speed):
    bus.write_i2c_block_data(0x32,0,[1,speed])
    return -1
