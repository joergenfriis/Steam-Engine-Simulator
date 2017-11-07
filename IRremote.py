# IRremote.py
#
# modul, der styrer fjernsynet bag kooejet.
#
# Slaveadressen er 0x42
#
# Programmet sender et heltal til Arduinoen. Tallet angiver hvilken
# funktion, der trykkes på på fjernbetjeningen:
#
# 1: On/Off
# 2: Right Arrow
# 3: OK
# 4: Pause
#********************************************************************
# Joergen Friis 24.07.2017
#********************************************************************
import smbus
import time
import sys

bus = smbus.SMBus(1)

def TVonOff():
    Success = False
    caught_exception = None
    for _ in range (3):
        try:
            bus.write_i2c_block_data(0x42,0,[1])
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after three retries")
    if Success:
        print("TV On/Off")
    return -1

def TVrightArrow():
    Success = False
    caught_exception = None
    for _ in range (3):
        try:
            bus.write_i2c_block_data(0x42,0,[2])
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after three retries")
    if Success:
        print("TV Right arrow")
    return -1

def TVok():
    Success = False
    caught_exception = None
    for _ in range (3):
        try:
            bus.write_i2c_block_data(0x42,0,[3])
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after three retries")
    if Success:
        print("TV OK")
    return -1

def TVpause():
    Success = False
    caught_exception = None
    for _ in range (3):
        try:
            bus.write_i2c_block_data(0x42,0,[4])
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Failed after three retries")
    if Success:
        print("TV Pause")
    return -1
