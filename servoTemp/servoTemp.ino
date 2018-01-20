/*
servo slave
slave  0x43

Kontrollerer servomotor: roegtemperatur

RegisterMap:
0: temperatur (0-100)

Joergen Friis 20.01.2018
*/

#include <Servo.h>
#include <Wire.h>
#define SLAVE_ADDRESS 0x44
#define REG_MAP_SIZE 2
#define MAX_SEND_BYTES 2

byte registerMap[REG_MAP_SIZE];






Servo tempServo;

int temp = 100;


void setup()
{
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
  
  Serial.begin(9600);
  
  tempServo.attach(9);
  
  registerMap[0] = 0;
  registerMap[1] = 0;
}

void loop()
{
  delay(3000);
  temp = registerMap[1];
  Serial.print("Temp = ");
  Serial.println(temp);
  temp = map(temp, 0, 100, 0, 180);
  tempServo.write(temp);
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
