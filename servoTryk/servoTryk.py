# servoTryk.py
#
# modul, der styrer manometre for damptryk og kondensatorvacuum.
#
# Slaveadressen er 0x43
#
# Programmet sendet to heltal til Arduinoen:
# Foerste tal angiver hvor mange grader motoren i vacuummeteret skal dreje.
# Andet tal angiver hvor mange grader motoren i kedelomanometeret skal dreje.
#
# Naar manometrene er kalibreret aendres programmerne, saadan at de variable
# angiver trykket.
#
#***************************************************************************
# Joergen Friis 24.01.2018
#***************************************************************************

import smbus
import time
import sys

bus = smbus.SMBus(1)

def vis(vacuum,tryk):
    tryk = int(1.6 * tryk + 60)
    vacuum = int(22 * vacuum + 80)
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x43,0,[vacuum,tryk])
            Success = True
            break
        except:
            #print("Unexpected error:", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Servo tryk failed after 30 retries")
    #if Success:
        #print("Vacuum = ",vacuum,", tryk = ",tryk)
    return -1


