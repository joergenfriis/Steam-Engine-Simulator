# demo.py
#
# Program, der demonstrerer nogle af simulatorens funktioner,
# uden at modtage brugerinput.
#
# Joergen Friis 24.07.2017
#
#*****************************************************************************

import pygame
import time
import powernet
import model
import IRremote

while True:

    print("Demoprogram starter")

    model.ModelStop()

    model.ModelReset()

    powernet.RelayAlloff()

    time.sleep(15)

    powernet.Relay5on()     # Taend for lydanlaeg
    time.sleep(1)
    powernet.Relay6on()     # Taend for TV skaerm
    time.sleep(10)

    IRremote.TVonOff()      # Start filmen
    time.sleep(5)
    IRremote.TVrightArrow()
    time.sleep(1)
    IRremote.TVrightArrow()
    time.sleep(1)
    IRremote.TVok()
    time.sleep(1)
    IRremote.TVok()
    time.sleep(1)
    IRremote.TVrightArrow()
    time.sleep(1)
    IRremote.TVrightArrow()
    time.sleep(1)
    IRremote.TVrightArrow()
    time.sleep(1)
    IRremote.TVok()
    

    pygame.mixer.init()     # Afspil reallyd fra maskinrummet på Bjoern
    pygame.mixer.music.load("Sound/dampmaskine.mp3")
    pygame.mixer.music.play()

    model.ModelRun(255,255) # Styr modellen saa den foelger kommandoerne paa reallyden

    time.sleep(42)
    time.sleep(173)

    model.ModelRun(150,255)
    time.sleep(22)
    model.ModelRun(75, 255)
    time.sleep(43)
    model.ModelRun(50, 255)
    time.sleep(106)
    model.ModelRun(75, 0)
    time.sleep(19)
    model.ModelRun(50, 255)
    time.sleep(45)
    model.ModelRun(50, 0)
    time.sleep(20)
    model.ModelRun(50, 255)
    time.sleep(38)
    model.ModelRun(50, 0)
    time.sleep(27)
    model.ModelRun(50, 255)
    time.sleep(112)
    model.ModelRun(50, 0)
    time.sleep(28)
    model.ModelRun(50, 255)
    time.sleep(31)
    model.ModelRun(100, 0)
    time.sleep(27)
    model.ModelRun(50, 255)
    time.sleep(70)
    model.ModelRun(50, 0)
    time.sleep(17)
    model.ModelRun(50, 255)
    time.sleep(228)
    model.ModelRun(0, 127)
    time.sleep(35)

    model.ModelStop()

    pygame.mixer.music.stop()

    IRremote.TVonOff()

    powernet.Relay5off()
    time.sleep(1)
    powernet.Relay6off()

    print("Demoprogram genstarter")

