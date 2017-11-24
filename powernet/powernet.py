# powernet.py
#
# Modul, der styrer den arduino,
# som styrer  stroemforsyningen til simulatorens forskellige dele.
#
# Slaveadresse 0x10
#
# Programmet sender et heltal til arduinoen. Tallet angiver hvilket relae,
# der skal taendes eller slukkes.
#
# Relae nummer, taend-kode, sluk-kode, funktion:
# 2,            1,          2           Transportbaand
# 3,            3,          4           Roegmaskine
# 4,            7,          8           Varmeblaeser
# 5,            9,          10          Lydanlaeg
# 6,            5,           6          TV skaerm kooeje i maskinrum
# 7,            19,         20          Ventilation
# 8,            17,         18          Skibsbro 230 V AC
# 9,            11,         12          Roegmaskine aktivering
# 10,           13,         14          Simulator klar: 24 V DC
# 11,           15,         16          Skibsbro 24 + 12 V DC
#*************************************************************************
# Joergen Friis 16.11.2017
#*************************************************************************
import smbus
import time
import sys

bus = smbus.SMBus(1)

def Relay2on():
    # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[1]) # send 1 til arduinoen
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0])
            # wait a second for the retry
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 2 on")
    return -1

def Relay2off():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[2]) # send 2 til arduinoen
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 2 off")
    return -1

def Relay3on():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[3])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 3 on")
    return -1

def Relay3off():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[4])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 3 off")
    return -1

def Relay4on():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[7])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 4 on")
    return -1

def Relay4off():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[8])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 4 off")
    return -1

def Relay5on():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[9])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 5 on")
    return -1

def Relay5off():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[10])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 5 off")
    return -1

def Relay6on():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[5])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 6 on")
    return -1

def Relay6off():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[6])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 6 off")
    return -1

def Relay7on():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[19])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 7 on")
    return -1

def Relay7off():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[20])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 7 off")
    return -1

def Relay8on():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[17])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 8 on")
    return -1

def Relay8off():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[18])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 8 off")
    return -1

def Relay9on():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[11])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 9 on")
    return -1

def Relay9off():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[12])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 9 off")
    return -1

def Relay10on():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[13])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 10 on")
    return -1

def Relay10off():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[14])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 10 off")
    return -1

def Relay11on():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[15])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 11 on")
    return -1

def Relay11off():
     # Try up to 30 times on a failure
    Success = False
    caught_exception = None
    for _ in range (30):
        try:
            bus.write_i2c_block_data(0x10,0,[16])
            # if we get here, we succeeded, so break out of the loop
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0]) 
            time.sleep(1)
    if not Success:
        print("Failed after 30 retries")
    if Success:
        print("Relay 11 off")
    return -1


def RelayAlloff():
    Relay2off()
    time.sleep(1)
    Relay3off()
    time.sleep(1)
    Relay4off()
    time.sleep(1)
    Relay5off()
    time.sleep(1)
    Relay6off()
    time.sleep(1)
    Relay7off()
    time.sleep(1)
    Relay8off()
    time.sleep(1)
    Relay9off()
    time.sleep(1)
    Relay10off()
    time.sleep(1)
    Relay11off()
    print("All relays off")

    
