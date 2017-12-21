/*
slave, der styrer sikkerhedsventilen
slave 0x39

Joergen Friis 21.12.2017
***************************************************************/

#include <Wire.h>

#define SLAVE_ADDRESS 0x39
#define REG_MAP_SIZE 1
#define MAX_SEND_BYTES 1

/***** Global Variables *****/

byte registerMap[REG_MAP_SIZE];
byte nyBesked = 0;

int ventilPin = 2;

const int dropSize = 1000;  //antal milisekunder ventilen er aaben

/***** Setup *****/

void setup()
{
  //Serial.begin(9600);
  
  pinMode(ventilPin, OUTPUT);
  
  digitalWrite(ventilPin, LOW);
  
  registerMap[0] = 0;
  
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
}

void loop()
{
  if (nyBesked == 1)
  {
    //Serial.println(registerMap[1]);
    if (registerMap[1] == 1) executeDrop(dropSize,0);
  }
}

void delayExact(int timeMs, int timeUs)
{
  if (timeMs >0)
  {
    delay(timeMs);
  }
  if (timeUs > 0)
  {
    delayMicroseconds(timeUs);
  }
}

void executeDrop(int timeOn, int timeDelay)
{
   if (timeDelay > 0)
  {
   delayExact(timeDelay, 0);
  } 
  digitalWrite(ventilPin, HIGH);
  delayExact(timeOn, 0);
  digitalWrite(ventilPin, LOW);
}

void receiveEvent(int byteCount)
{
  for (int i = 0; i < byteCount; i++)
  {
    byte c = Wire.read();
    registerMap[i] = c;
    nyBesked = 1;
  }
}
  
