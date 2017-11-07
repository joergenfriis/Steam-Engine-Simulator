/*
Arduino I2C slave
Aflæsning af vejeceller.
Anvender A/D converter HX711

HX711.DOUT      pin #A0
HX711.PD_SCK    pin #A1

Register:
registerMap[0] er 0 for vejning og 1 for reset med tarering
registerMap[1] er msb for massen i gram af det vejede
registerMap[2] er lsb for massen i gram af det vejede

Joergen Friis 05.04.2017
*/

#include <Wire.h>
#include <HX711.h>
#define Slave_ADDRESS   0x31
#define REG_MAP_SIZE    3
#define MAX_SEND_BYTES  3

/***** Global Variables *****/

byte registerMap[REG_MAP_SIZE];
byte nyBesked = 0;

long tara = 0;
long skalering = 20.921;        // Eksperimentelt fastsat værdi
int masse = 0;

HX711 scale;

void setup()
{
  // Serial.begin(38400);          // For debugging
  
  Wire.begin(Slave_ADDRESS);
  Wire.onRequest(requestEvent);
  Wire.onReceive(receiveEvent);
  
  scale.begin(A0, A1);
  tara = scale.read_average(1000);
  
  for (int i = 0; i<3; i++)
  {
    registerMap[i] = 0;
  }
  
//  Serial.println("Ready!");
}

void loop()
{
  if (registerMap[0] > 0) 
  {
    tara = scale.read_average(1000);  // Nulstil vægten
    registerMap[0] = 0;
    Serial.println("Vaegten er nulstillet");
  }
  
  masse = int((scale.read_average(100) - tara)/skalering);
  masse = abs(masse);
  registerMap[1] = masse>>8;      // Indeholder det høje byte af int masse
  registerMap[2] = masse & 0xff;  // Indeholder det lave byte af int masse
  
 /* Serial.print("Masse paa baandet: \t");
  Serial.print(masse);
  Serial.print("\t regMap[0]: \t");
  Serial.print(registerMap[0]);
  Serial.print("\t regMap[1]: \t");
  Serial.print(registerMap[1]);
  Serial.print("\t regMap[2]: \t");
  Serial.println(registerMap[2]);*/
}

void requestEvent()
{
 byte buffer[3];
 buffer[0] = registerMap[0];
 buffer[1] = registerMap[1];
 buffer[2] = registerMap[2];
 Wire.write(buffer,3);
}

void receiveEvent(int byteCount)
{
 byte c = Wire.read();    // Den første byte, der modtages er ubrugelig
 for (int i = 0; i < byteCount-1; i++)
  {
    c = Wire.read();
    registerMap[i] = c;
  }
}

