# servoTemp.py
#
# modul, der styrer roeggastermometer.
#
# Slaveadressen er 0x44
#
# Programmet sendet et heltal til Arduinoen:
# Tallet angiver hvor mange grader motoren i termometeret skal dreje.
# 
#
# Naar termometeret er kalibreret aendres programmet, saadan at den variable
# angiver temperaturen.
#
#***************************************************************************
# Joergen Friis 19.03.2018
#***************************************************************************

import smbus
import time
import sys

bus = smbus.SMBus(1)

def vis(temp):
    if temp > 600:
        temp = 600
    temp = int(100 - 0.167 * temp)
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x44,0,[temp])
            Success = True
            break
        except:
            #print("Unexpected error:", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Servo temp vis failed after 30 retries")
    #if Success:
        #print("Temperatur = ",temp)
    return -1


