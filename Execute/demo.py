# demo.py
#
# Modul, der demonstrerer nogle af simulatorens funktioner,
# uden at modtage brugerinput.
#
# Joergen Friis 10.01.2018
#
#*****************************************************************************

import pygame
import time
import powernet
import model
import IRremote
import servo

def demo():

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
    

    pygame.mixer.init()     # Afspil reallyd fra maskinrummet paa Bjoern
    pygame.mixer.music.load("Sound/dampmaskine.mp3")
    pygame.mixer.music.play()

    servo.maskintelegraf_FF()
    model.ModelRun(100,0) # Styr modellen saa den foelger kommandoerne paa reallyden

    time.sleep(42)
    time.sleep(170)

    servo.maskintelegraf_HF()
    time.sleep(3)
    model.ModelRun(60,0)
    time.sleep(19)
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(30, 0)
    time.sleep(40)
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(103)
    servo.maskintelegraf_LB()
    time.sleep(3)
    model.ModelRun(30, 100)
    time.sleep(16)
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(42)
    servo.maskintelegraf_LB()
    time.sleep(3)
    model.ModelRun(20, 100)
    time.sleep(17)
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(35)
    servo.maskintelegraf_LB()
    time.sleep(3)
    model.ModelRun(20, 100)
    time.sleep(24)
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(109)
    servo.maskintelegraf_LB()
    time.sleep(3)
    model.ModelRun(20, 100)
    time.sleep(25)
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(28)
    servo.maskintelegraf_HB()
    time.sleep(3)
    model.ModelRun(40, 100)
    time.sleep(24)
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(67)
    servo.maskintelegraf_LB()
    time.sleep(3)
    model.ModelRun(20, 100)
    time.sleep(14)
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(225)
    servo.maskintelegraf_FS()
    time.sleep(3)
    model.ModelRun(0, 50)
    time.sleep(35)

    model.ModelStop()

    pygame.mixer.music.stop()

    IRremote.TVonOff()

    powernet.Relay5off()
    time.sleep(1)
    powernet.Relay6off()


