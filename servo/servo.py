# servo.py
#
# modul, der styrer servomotorerne
#
# Joergen Friis 20.12.2017
#
#**********************************************************************
from __future__ import division
import PCA9685 # Servo driver

pwm = PCA9685.PCA9685()
pwm.set_pwm_freq(60)    # Erfaringsvaerdi paa 60 Hz, der virker godt

servo1 = 0   # maskintelegraf
servo2 = 1   # roeggastemperatur
servo3 = 2   # kondensatortryk
servo4 = 3   # kedeltryk
servo5 = 4   # gangskifte                                                                                                                    
servo1_min = 135  # (135 svarer til 0 grader)
servo1_max = 590  # (369 svarer til 90 grader og 590 svarer til 180 grader)
servo2_min = 175 # testet
servo2_max = 240 # testet
servo3_min = 327 # testet
servo3_max = 390 # testet
servo4_min = 240 # testet
servo4_max = 290 # testet
servo5_min = 280 # testet Fuld kraft frem
servo5_max = 430 # testet Fuld kraft bak


def servoTest(drej):
    pwm.set_pwm(0, 0, drej)


def servoNulstil():
    pwm.set_pwm(servo1,0,int(servo1_min+(servo1_max-servo1_min)/2))
    pwm.set_pwm(servo2,0,servo2_min)
    pwm.set_pwm(servo3,0,servo3_min)
    pwm.set_pwm(servo4,0,servo4_min)
    pwm.set_pwm(servo5,0,int(servo5_min+(servo5_max-servo5_min)/2))
    

def maskintelegraf_FF():
    pwm.set_pwm(servo1, 0, 250)

def maskintelegraf_HF():
    pwm.set_pwm(servo1, 0, 285)

def maskintelegraf_LF():
    pwm.set_pwm(servo1, 0, 325)

def maskintelegraf_FS():
    pwm.set_pwm(servo1, 0, 369)

def maskintelegraf_LB():
    pwm.set_pwm(servo1, 0, 410)

def maskintelegraf_HB():
    pwm.set_pwm(servo1, 0, 450)

def maskintelegraf_FB():
    pwm.set_pwm(servo1, 0, 490)

    

def smokeTemp(temp):
    step = int(175 + 0.07666*temp)
    pwm.set_pwm(servo2, 0, step)

def kedelTryk(tryk):
    step = int(255 + 3.5*tryk)
    pwm.set_pwm(servo4, 0, step)

def kondensatorTryk(tryk):
    step = int(330 + 60*tryk)
    pwm.set_pwm(servo3, 0, step)

def gangskifte(stilling):
    step = int(stilling/100*(servo5_max-servo5_min) + servo5_min)
    pwm.set_pwm(servo5, 0, step)
    print("step: ",step)
    print("Gangskifte servo stilling: ",stilling)
    
