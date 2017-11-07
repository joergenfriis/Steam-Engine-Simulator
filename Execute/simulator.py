import smbus
import time
bus = smbus.SMBus(1)

# Dette er adressen, som arduinoslaven er sat op til
address = 0x50

def writeNumber(value):
    bus.write_i2c_block_data(address,0,value)
    # bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

def readNumber():
    # number = bus.read_byte(address)
    number = bus.read_i2c_block_data(address,1)
    return number


while True:
    #var = input("Enter 1-9:")   #input funktionen genererer altid en str
    #var = int(var)              #derfor skal den laves om til int

    var = [32,2]
    if not var:
        continue

    writeNumber(var)
    print("RPI: Hi Arduino, I send you",var)
    # sleep one second
    time.sleep(1)

    number = readNumber()
    print ("Arduino: Hej RPI, jeg modtog et array", number)
    print ()

