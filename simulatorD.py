# simulatorD.py
#
# Hovedprogram til at drive maskinrumssimulatoren alene i pædagogisk mode.
#
#**************************************************************************

import time
import powernet

# Tænd for strøm til Lydanlæg:
powernet.Relay5on()
time.sleep(1)

# Tænd for strøm til TV skærm i koøje:
powernet.Relay6on()
time.sleep(1)

# Meld simulator klar:
powernet.Relay10on()
time.sleep(1)



