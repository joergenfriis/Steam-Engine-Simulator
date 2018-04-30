# demo.py
#
# Modul, der demonstrerer nogle af simulatorens funktioner,
# uden at modtage brugerinput.
#
# Joergen Friis 30.04.2018
#
#*****************************************************************************

import pygame
import time
import powernet
import model
import IRremote
import servo
import programvalg
import skueglasOlie
import skueglasKedel
import servoTryk
import servoTemp

def demo():

    model.ModelStop()

    model.ModelReset()

    pygame.mixer.quit()

    powernet.RelayAlloff()

    time.sleep(15)

    powernet.Relay5on()     # Taend for lydanlaeg
    time.sleep(1)
    powernet.Relay6on()     # Taend for TV skaerm
    time.sleep(30)
    IRremote.TVonOff()
    time.sleep(10)
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

    if programvalg.read() != 1:
        return

    powernet.Relay10on()    # Taend forkontrollampe
    time.sleep(1)


    pygame.mixer.init()     # Afspil reallyd fra maskinrummet paa Bjoern
    pygame.mixer.music.load("Sound/dampmaskine.mp3")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play()

    servo.maskintelegraf_FF()
    skueglasOlie.set(50)
    skueglasKedel.set(70)
    servoTryk.vis(0.2,8)
    servoTemp.vis(300)
    model.ModelRun(100,0) # Styr modellen saa den foelger kommandoerne paa reallyden

    time.sleep(42)

    if programvalg.read() != 1:
        return
    
    time.sleep(170)

    if programvalg.read() != 1:
        return

    servo.maskintelegraf_HF()
    time.sleep(3)
    model.ModelRun(60,0)
    time.sleep(19)

    if programvalg.read() != 1:
        return
    
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(30, 0)
    time.sleep(40)

    if programvalg.read() != 1:
        return
    
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(103)

    if programvalg.read() != 1:
        return
    
    servo.maskintelegraf_LB()
    time.sleep(3)
    model.ModelRun(30, 100)
    time.sleep(16)
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(42)

    if programvalg.read() != 1:
        return
    
    servo.maskintelegraf_LB()
    time.sleep(3)
    model.ModelRun(20, 100)
    time.sleep(17)
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(35)

    if programvalg.read() != 1:
        return
    
    servo.maskintelegraf_LB()
    time.sleep(3)
    model.ModelRun(20, 100)
    time.sleep(24)

    if programvalg.read() != 1:
        return
    
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(109)

    if programvalg.read() != 1:
        return
    
    servo.maskintelegraf_LB()
    time.sleep(3)
    model.ModelRun(20, 100)
    time.sleep(25)

    if programvalg.read() != 1:
        return
    
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(28)

    if programvalg.read() != 1:
        return
    
    servo.maskintelegraf_HB()
    time.sleep(3)
    model.ModelRun(40, 100)
    time.sleep(24)

    if programvalg.read() != 1:
        return
    
    servo.maskintelegraf_LF()
    time.sleep(3)
    model.ModelRun(20, 0)
    time.sleep(67)

    if programvalg.read() != 1:
        return
    
    servo.maskintelegraf_LB()
    time.sleep(3)
    model.ModelRun(20, 100)
    time.sleep(14)
    servo.maskintelegraf_LF()
    time.sleep(3)

    if programvalg.read() != 1:
        return
    
    model.ModelRun(20, 0)
    time.sleep(225)

    if programvalg.read() != 1:
        return
    
    servo.maskintelegraf_FS()
    time.sleep(3)
    model.ModelRun(0, 50)
    time.sleep(35)

    model.ModelStop()

    pygame.mixer.music.stop()




