# simulator.py
#
# Hovedprogram til drift af dampmaskinesimulatoren paa Det Gamle Vaerft.
#
# Joergen Friis 12.12.2017
#
#############################################################################

import time
import powernet
import transport
import servo
import model
import vejecelle
import flowmaaler
import omstyring
import skueglasOlie
import primaerluft

print("Starter simulatorprogram")

# Initiering af simulatoren ################################################

print("Initiering")

servo.servoNulstil() # Alle servoerne stilles i neutral stilling.
