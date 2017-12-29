/*
servo slave
slave  0x43

Kontrollerer to servomotorer: damptryk og kondensator vacuum

RegisterMap:
0: tryk (0-100)
1: vacuum (09-100)

Joergen Friis 27.12.2017
*/

#include <Servo.h>
#include <Wire.h>
#define SLAVE_ADDRESS 0x43
#define REG_MAP_SIZE 3
#define MAX_SEND_BYTES 3

byte registerMap[REG_MAP_SIZE];

Servo dampServo;
Servo kondensServo;

int tryk = 50;
int vacuum = 0;


void setup()
{
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
  
  Serial.begin(9600);
  
  dampServo.attach(10);
  kondensServo.attach(9);
  
  registerMap[0] = 0;
  registerMap[1] = 0;
  registerMap[2] = 50;
}

void loop()
{
  delay(3000);
  tryk = registerMap[2];
  Serial.print("Tryk = ");
  Serial.println(tryk);
  dampServo.write(tryk);
  delay(15);
  
  vacuum = registerMap[1];
  //vacuum = map(vacuum, 0, 100, 0, 180);
  Serial.print("Vacuum = ");
  Serial.println(vacuum);
  Serial.println();
  kondensServo.write(vacuum);
  delay(15);
}

void receiveEvent(int byteCount)
{
  for (int i = 0; i < byteCount; i++)
  {
    byte c = Wire.read();
    registerMap[i] = c;
  }
}

