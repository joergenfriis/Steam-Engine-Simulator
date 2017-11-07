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

print("Starter testprogram.")

print("Slukker alle relæer")
powernet.RelayAlloff()
time.sleep(1)

print("Tænder for strøm til relæ 9")
powernet.Relay9on()
time.sleep(1)



print("Test sluttet")
