# servo.py
#
# modul, der styrer servomotorerne
#
#**********************************************************************
from __future__ import division
import PCA9685 # Servo driver

pwm = PCA9685.PCA9685()
pwm.set_pwm_freq(60)    # Erfaringsvaerdipaa 60 Hz, der virker godt

servo1 = 0   # maskintelegraf
servo2 = 1   # røggastemperatur
servo3 = 2   # kondensatortryk
servo4 = 3   # kedeltryk
servo5 = 4   # gangskifte                                                                                                                    
servo1_min = 246  # svarer til 1 ms ved 60 Hz
servo1_max = 492  # svarer til 2 ms ved 60 Hz
servo2_min = 175 # testet
servo2_max = 240 # testet
servo3_min = 327 # testet
servo3_max = 390 # testet
servo4_min = 240 # testet
servo4_max = 290 # testet
servo5_min = 280 # testet
servo5_max = 430 # testet


def servoNulstil():
    pwm.set_pwm(servo1,0,servo1_min)
    pwm.set_pwm(servo2,0,servo2_min)
    pwm.set_pwm(servo3,0,servo3_min)
    pwm.set_pwm(servo4,0,servo4_min)
    pwm.set_pwm(servo5,0,int(servo_5min+(servo5_max-servo5_min)/2))
    
    

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
    step = int(stilling*((servo5_max-servo5_min)/255) + servo5_min)
    pwm.set_pwm(servo5, 0, step)
    
