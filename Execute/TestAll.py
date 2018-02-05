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

servoTryk.vis(0.5,5)
servoTemp.vis(300)
sikkerhedsventil.sikkerhedsventilOff()
transport.TransportStop()
powernet.RelayAlloff()
skueglasOlie.set(50)
skueglasKedel.set(70)
time.sleep(5)
servo.maskintelegraf_FS()
time.sleep(5)


model.ModelStop()




print("Test sluttet")
