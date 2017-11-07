/*
Arduino I2C slave
Transportbånd styring
Styring af frekvensomformer vha af 0-10 V spænding
produceret vha PWM på Arduinoens ben D3.
Kredsen måler også motortemperaturen vhja A0 og slukker for motoren,
hvis temperaturen bliver for høj.
Endvidere styres et relæ, der tænder og slukker for motoren.

Der modtages en byte med en værdi mellem 0 og 255 til styring af frekvensen (motorhastigheden),
og en byte: 0 eller 1 til styring af sluk/tænd relæet.

Joergen Friis 01.02.2017
*/

#include<Wire.h>
#define SLAVE_ADDRESS   0x32
#define REG_MAP_SIZE    2
#define MAX_SEND_BYTES  2

/***** Global Variables *****/

byte registerMap[REG_MAP_SIZE];
byte nyBesked = 0;

int styringssignal = 3;
int relaysignal = 4;
int varmesensor = 0;

void setup()
{
  pinMode(styringssignal, OUTPUT);
  pinMode(relaysignal, OUTPUT);
  pinMode(varmesensor,INPUT);
  
  digitalWrite(relaysignal, LOW);
  analogWrite(styringssignal, 0);      // giver frekvensomformeren besked på at motoren skal stå stille
  
  Serial.begin(9600);    // For debugging
  
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
}

void loop()
{
  delay(100);
  if (nyBesked == 1)
  {
    nyBesked = 0;
    digitalWrite(relaysignal, registerMap[1]);
    analogWrite(styringssignal, registerMap[2]);
  }
}
  
void receiveEvent(int byteCount)
{
  for (int i = 0; i < byteCount; i++)
  {byte c =Wire.read();
  registerMap[i] = c;
  nyBesked = 1;
  Serial.println(registerMap[i]);  // for debugging
  }
}
    
