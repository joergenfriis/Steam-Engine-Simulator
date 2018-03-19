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
# Joergen Friis 19.03.2018
#***************************************************************************

import smbus
import time
import sys

bus = smbus.SMBus(1)

def vis(vacuum,tryk):
    if tryk > 10:
        tryk = 10
    if vacuum > 1:
        vacuum = 1
    tryk = int(180 - 18 * tryk)
    vacuum = int(180 - 180 * vacuum)
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


