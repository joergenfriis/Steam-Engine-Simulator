# ventiler.py
#
# modul, der aflaeser input fra de 6 ventilhaandtag
#
# slaveadresse 0x36
#
# programmet laeser en streng med 6 bytes fra arduinoen.
# alle med en vaerdi mellem 1 og 100, der angiver hvor
# meget den enkelte ventil er aabnet.
# 
# Joergen Friis 21.12.2017
#
##############################################################################

import smbus
import time
import sys

bus = smbus.SMBus(1)

def readKedelvandInd():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            data = bus.read_i2c_block_data(0x36, 0)
            Success = True
            break
        except:
            #print("Unexpected error: ",sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Read kedelvand ind failed after 30 retries")
    if Success:
        kedelvandInd = data[1]
        #print("Kedelvand Ind = ",kedelvandInd," %")
    return kedelvandInd

def readKedelvandUd():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            data = bus.read_i2c_block_data(0x36, 0)
            Success = True
            break
        except:
            #print("Unexpected error: ",sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Read kedelvand ud failed after 30 retries")
    if Success:
        kedelvandUd = data[0]
        #print("Kedelvand Ud = ",kedelvandUd," %")
    return kedelvandUd

def readKondensatorvandInd():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            data = bus.read_i2c_block_data(0x36, 0)
            Success = True
            break
        except:
            #print("Unexpected error: ",sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("kondensatorvand ind failed after 30 retries")
    if Success:
        kondensatorvandInd = data[3]
        #print("Kondensatorvand Ind = ",kondensatorvandInd," %")
    return kondensatorvandInd
    
def readKondensatorvandUd():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            data = bus.read_i2c_block_data(0x36, 0)
            Success = True
            break
        except:
            #print("Unexpected error: ",sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Read kondensatorvand ud failed after 30 retries")
    if Success:
        kondensatorvandUd = data[2]
        #print("Kondensatorvand Ud = ",kondensatorvandUd," %")
    return kondensatorvandUd

def readDampInd():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            data = bus.read_i2c_block_data(0x36, 0)
            Success = True
            break
        except:
            #print("Unexpected error: ",sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Read damp ind failed after 30 retries")
    if Success:
        dampInd = data[4]
        #print("Damp Ind = ",dampInd," %")
    return dampInd

def readDampUd():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            data = bus.read_i2c_block_data(0x36, 0)
            Success = True
            break
        except:
            #print("Unexpected error: ",sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        print("Read damp ud failed after 30 retries")
    if Success:
        dampUd = data[5]
        #print("Damp Ud = ",dampUd," %")
    return dampUd
