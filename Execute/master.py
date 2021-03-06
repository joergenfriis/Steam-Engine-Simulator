# master.py
#
# Hovedprogram, der vaelger det relevante underprogram paa baggrund
# afprogramvaelgerens stilling
#
# Joergen Friis 04.09.2018
#
##############################################################################

import pygame
import time
import subprocess
import simulator
import demo
import programvalg
import powernet
import model
import servoTryk
import servoTemp
import sikkerhedsventil
import transport
import skueglasOlie
import skueglasKedel
import servo



while True:
    print("Starter program nummer ",programvalg.read())
    while programvalg.read() == 0:
        print("Lukker alt ned")
        sikkerhedsventil.sikkerhedsventilOff()
        transport.TransportStop()
        model.ModelStop()
        servoTryk.vis(1,0)
        servoTemp.vis(50)
        skueglasOlie.set(50)
        skueglasKedel.set(60)
        servo.maskintelegraf_FS()
        if (pygame.mixer.get_init != None):
            pygame.mixer.quit()
        powernet.RelayAlloff()
        time.sleep(5)
        # Her skal indsaettes noget kode, der kopierer klokkeslaet samt de
        # initiale tilstandsvaerdier ud i en tilstandsfil paa SD kortet
        subprocess.call(["sudo","shutdown","-h","now"])
        
            
    while programvalg.read() == 1:
        print("Starter demoprogram")
        if programvalg.read() == 1:
            demo.demo()
            
    while programvalg.read() in [2,3,4]:
        print("Starter simulatorprogram")
        simulator.start(programvalg.read())
            
