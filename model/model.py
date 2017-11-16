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
# 16.11.2017 Joergen Friis
#******************************************************************

import smbus

bus = smbus.SMBus(1)

def ModelStop():
    # Try up to 3 times on a faliure
    Success = False
    caught_exception = None
    for _ in range (3):
        try:
            bus.write_i2c_block_data(0x52, 0, [0,127,0])
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        Print("Failed after 3 retries")
    if Success:
        print('model stop')
    return -1

def ModelRun(energi,gear):
    # Try up to 3 times on a faliure
    Success = False
    caught_exception = None
    for _ in range (3):
        try:
            bus.write_i2c_block_data(0x52, 0, [energi,gear,0])
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        Print("Failed after 3 retries")
    if Success:
        print('model run, energi= {} og gear = {}'.format(energi,gear))
    return -1

def ModelReset():
    # Try up to 3 times on a faliure
    Success = False
    caught_exception = None
    for _ in range (3):
        try:
            bus.write_i2c_block_data(0x52, 0, [0,127,1])
            Success = True
            break
        except:
            print("Unexpected error:", sys.exc_info() [0])
            time.sleep(1)
    if not Success:
        Print("Failed after 3 retries")
    if Success:
        print('model reset')
    return -1
