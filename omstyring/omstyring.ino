/*
Arduino I2C slave
Til måling på omstyringen.
Der returneres et byte med omstyringens stilling.

Register:
Status:            1 byte    read
Omstyring:         1 byte    read  

Programmet læser omstyringens stilling ved hjælp af spændingsfaldet 
over et potentiometer.


Joergen Friis 12.03.2018
*/

#include<Wire.h>
#define SLAVE_ADDRESS    0x29    //slave address, any number from 0x01 to 0x7F. 0x er bare et præfix, der i C fortæller compileren, at de efterfølgende nummer er hexadecimalt.
#define REG_MAP_SIZE     2

#define ANALOG_INPUT_PIN A1

/***** Global Variables ******/

byte registerMap[REG_MAP_SIZE];          // Her reserveres plads til registeret i lageret

const int numReadings = 2;    // nu større værdi, jo mere udjævnet signal
int stilling = 0;
int readings[numReadings];    // her gemmes værdierne fra det analoge input
int readIndex = 0;            // index af den aktuelle måling
int total = 0;                // den løbende total
int average = 0;              // gennemsnittet af målingerne

void setup()
{
  Serial.begin(9600);
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(requestEvent);  // Kalder funktionen requestEvent når masteren anmoder om data fra slaven
  
  pinMode(ANALOG_INPUT_PIN, INPUT);
  
  for (int thisReading = 0; thisReading < numReadings; thisReading++)
  {
    readings[thisReading] = 0;
  }
 
  registerMap[0] = 0;
  registerMap[1] = 0; 
}

void loop()
{  
  delay(10);
  
  total = total - readings[readIndex];    // subtract the last reading
 // Serial.println(analogRead(ANALOG_INPUT_PIN));
  stilling = map(analogRead(ANALOG_INPUT_PIN),398,620,0,100);   // aflaes og skaler aflaesningen af sensoren
  Serial.println(stilling);
  if (stilling < 0) stilling = 0;
  readings[readIndex] = stilling;  // gem aflaesningen
  total = total + readings[readIndex];    // adder målingen til totalen
  readIndex = readIndex + 1;              // ryk til næste position i arrayet
  if (readIndex >= numReadings)
  {
    readIndex = 0;
  }
  average = total / numReadings;          // beregn gennemsnittet af målingerne
  
  int input = average;
  
  if (registerMap[1] != input)
  {
    registerMap[0] = 1;
    registerMap[1] = input;
  }
  else
  {
    registerMap[0] = 0;
  }
}

void requestEvent()
{
  byte buffer[2];             //Vi definerer en midlertidig buffer indeholdende 2 bytes
  buffer[0] = registerMap[0];
  buffer[1] = registerMap[1]; //og fylder indholdet af de relevante celler i registeret ned i bufferen
  Wire.write(buffer,2);
}
