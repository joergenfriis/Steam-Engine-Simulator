/*
Arduino I2C slave
til aflæsning af hovedafbryderens stilling.
Der returneres et byte med omstyringens stilling.

Register:
Kontakt:    1 byte  read

Programmet læser hovedkontaktens stilling ud fra
24 V DC spændingen på den sluttede kontakt.

Joergen Friis 11.03.2017
*/

#include<Wire.h>
#define SLAVE_ADDRESS    0x43
#define REG_MAP_SIZE     2

#define KONTAKT_A  2
#define KONTAKT_B  3
#define KONTAKT_C  4
#define KONTAKT_D  5

/***** Global Variables *****/

byte registerMap[REG_MAP_SIZE];

void setup()
{
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(requestEvent);
  // Serial.begin(9600);  // for debugging
  
  pinMode(KONTAKT_A, INPUT);
  pinMode(KONTAKT_B, INPUT);
  pinMode(KONTAKT_C, INPUT);
  pinMode(KONTAKT_D, INPUT);
  
  registerMap[0] = 0;
  
}

void loop()
{
  delay(10);
  
  if      (digitalRead(KONTAKT_A) == HIGH) registerMap[0] = 1;
  else if (digitalRead(KONTAKT_B) == HIGH) registerMap[0] = 2;
  else if (digitalRead(KONTAKT_C) == HIGH) registerMap[0] = 3;
  else if (digitalRead(KONTAKT_D) == HIGH) registerMap[0] = 4;
  else registerMap[0] = 0;
  
  // Serial.println(registerMap[0]);
}
  
void requestEvent()
{
  byte buffer[1];             //Vi definerer en midlertidig buffer indeholdende 1 byte
  buffer[0] = registerMap[0]; //og fylder indholdet af de relevante celler i registeret ned i bufferen
  Wire.write(buffer,1);
}
  
  
