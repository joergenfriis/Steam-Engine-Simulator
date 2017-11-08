# simulatorD.py
#
# Hovedprogram til at drive maskinrumssimulatoren alene i pædagogisk mode.
#
#**************************************************************************

import time
import powernet
import transport
import servo
import model

# Nulstil alle servomotorer:
servo.servoNulstil()
time.sleep(1)

# Stop dampmaskinemodellen:
model.ModelStop()
time.sleep(1)

# Tænd for strøm til Lydanlæg:
powernet.Relay5on()
time.sleep(1)

# Tænd for strøm til TV skærm i koøje:
powernet.Relay6on()
time.sleep(1)

# Tænd for strøm til transportbånd,
# start båndet og kør 1,5 m frem, så det er tomt.
powernet.Relay2on()
time.sleep(5)       # Der skal være tid til at frekvensomformeren starter
#  transport.TransportGo(127)
time.sleep(5)       # Den rigtige pauselængde skal findes
# transport.TransportStop()
time.sleep(1)

# Meld simulator klar:
powernet.Relay10on()
time.sleep(1)

# test af røggastemperatur:
servo.smokeTemp(300)
time.sleep(1)

# test af kedeltryk:
servo.kedelTryk(5)
time.sleep(1)

# test af kondensatortryk:
servo.kondensatorTryk(1)
time.sleep(1)

# test af dampmaskinemodel:
# print('test af dampmaskinemodel')
# model.ModelRun(0,0)
# time.sleep(5)
# model.ModelRun(0,50)
# time.sleep(5)
# model.ModelRun(255,50)
# time.sleep(5)

# Stop dampmaskinemodellen:
model.ModelStop()
time.sleep(1)

# 0-stil alle relæer:
powernet.RelayAlloff()

# 0-stil alle servomotorer
servo.servoNulstil()

# Sluttekst:

print('Program sluttet')
