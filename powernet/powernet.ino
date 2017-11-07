/*
Arduino I2C slave
til styring af strømforsyningstavlen.
Der modtages et int (2 bytes) med tænd eller sluksignal for et enkelt relæ.

Register:
relæstilling:  1 byte  write  (tal mellem 1 og 20)

Jørgen Friis 30.01.17
*/

#include <Wire.h>
#define SLAVE_ADDRESS   0x10
#define REG_MAP_SIZE    1
#define MAX_SEND_BYTES  1

/***** Global Variables *****/

byte registerMap[REG_MAP_SIZE];
byte nyBesked = 0;

int relay2 = 2;
int relay3 = 3;
int relay4 = 5;
int relay5 = 6;
int relay6 = 7;
int relay7 = 8;
int relay8 = 9;
int relay9 = 4;
int relay10 = 10;
int relay11 = 11;



void setup() {
  pinMode(relay2,OUTPUT);
  pinMode(relay3,OUTPUT);
  pinMode(relay4,OUTPUT);
  pinMode(relay5,OUTPUT);
  pinMode(relay6,OUTPUT);
  pinMode(relay7,OUTPUT);
  pinMode(relay8,OUTPUT);
  pinMode(relay9,OUTPUT);
  pinMode(relay10,OUTPUT);
  pinMode(relay11,OUTPUT);

  digitalWrite(relay2,LOW);
  digitalWrite(relay3,LOW);
  digitalWrite(relay4,LOW);
  digitalWrite(relay5,LOW);
  digitalWrite(relay6,LOW);
  digitalWrite(relay7,LOW);
  digitalWrite(relay8,LOW);
  digitalWrite(relay9,LOW);
  digitalWrite(relay10,LOW);
  digitalWrite(relay11,LOW);

  Serial.begin(9600);   // for debugging

  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);

  Serial.println("Ready!");  // for debugging
}

void loop() {
  delay(100);
  if (nyBesked == 1)
    {
      nyBesked = 0;
      switch(registerMap[1])
      {
        case 1:
          digitalWrite(relay2,HIGH);
          break;
        case 2:
          digitalWrite(relay2,LOW);
          break;
        case 3:
          digitalWrite(relay3,HIGH);
          break;
        case 4:
          digitalWrite(relay3,LOW);
          break;
        case 5:
          digitalWrite(relay9,HIGH);
          break;
        case 6:
          digitalWrite(relay9,LOW);
          break;
        case 7:
          digitalWrite(relay4,HIGH);
          break;
        case 8:
          digitalWrite(relay4,LOW);
          break;
        case 9:
          digitalWrite(relay5,HIGH);
          break;
        case 10:
          digitalWrite(relay5,LOW);
          break;
        case 11:
          digitalWrite(relay6,HIGH);
          break;
        case 12:
          digitalWrite(relay6,LOW);
          break;
        case 13:
          digitalWrite(relay7,HIGH);
          break;
        case 14:
          digitalWrite(relay7,LOW);
          break;
        case 15:
          digitalWrite(relay8,HIGH);
          break;
        case 16:
          digitalWrite(relay8,LOW);
          break;
        case 17:
          digitalWrite(relay10,HIGH);
          break;
        case 18:
          digitalWrite(relay10,LOW);
          break;
        case 19:
          digitalWrite(relay11,HIGH);
          break;
        case 20:
          digitalWrite(relay11,LOW);
          break;
      }
    }
}

void receiveEvent(int byteCount)
{
  for (int i = 0; i < byteCount; i++)
    {byte c = Wire.read();
    registerMap[i] = c;
    nyBesked = 1;
    Serial.println(registerMap[1]);   // for debugging
    }
}

