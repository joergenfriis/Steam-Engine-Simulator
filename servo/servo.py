# servo.py
#
# modul, der styrer servomotorerne
#
#**********************************************************************
from __future__ import division
import PCA9685 # Servo driver

pwm = PCA9685.PCA9685()
pwm.set_pwm_freq(60)    # Erfaringsværdi, der virker godt

servo1 = 0   # maskintelegraf
servo2 = 1   # røggastemperatur
servo3 = 2   # kondensatortryk
servo4 = 3   # kedeltryk

servo1_min = 150
servo1_max = 600
servo2_min = 175 # testet
servo2_max = 240 # testet
servo3_min = 327 # testet
servo3_max = 390 # testet
servo4_min = 240 # testet
servo4_max = 290 # testet


def servoNulstil():
    pwm.set_pwm(servo1,0,servo1_min)
    pwm.set_pwm(servo2,0,servo2_min)
    pwm.set_pwm(servo3,0,servo3_min)
    pwm.set_pwm(servo4,0,servo4_min)
    

def smokeTemp(temp):
    step = int(175 + 0.07666*temp)
    pwm.set_pwm(servo2, 0, step)

def kedelTryk(tryk):
    step = int(255 + 3.5*tryk)
    pwm.set_pwm(servo4, 0, step)

def kondensatorTryk(tryk):
    step = int(330 + 60*tryk)
    pwm.set_pwm(servo3, 0, step)
    
