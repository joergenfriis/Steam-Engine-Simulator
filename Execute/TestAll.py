# TestAll.py
#
# Program til testning af de enkelte komponenter i simulatoren.
#
#***************************************************************************

import time
import powernet
import transport
import servo
import model
import vejecelle
import flowmaaler
import omstyring
import skueglasOlie
import skueglasKedel
import primaerluft
import sekundaerLuft
import roegroer
import ventiler
import sikkerhedsventil
import IRremote
import programvalg
import servoTryk
import servoTemp

print("Starter testprogram.")

# print(omstyring.Read_omstyring())
# servoTryk.vis(1,0)
# servoTemp.vis(300)
skueglasOlie.reset()
# sikkerhedsventil.sikkerhedsventilOff()
# transport.TransportStop()
# powernet.RelayAlloff()
# time.sleep(5)
# powernet.Relay3on()

skueglasKedel.set(50)

# IRremote.TVonOff()



print("Test sluttet")
