/*
Program til at maale den frie distance i fem roegroer.

Arduino slave 0x35

Der sendes 5 vaerdier til masteren .

Register:
registerMap[0] er 0 hvis frontpladen er lukket og 1 hvis den er aaben.
registerMap[1-4] er 0-100: 0 hvis rensepinden er i bund og 100 hvis roeret er helt tomt.

Joergen Friis 20.12.2017
*/

#include <Wire.h>
#define Slave_ADDRESS 0x35
#define REG_MAP_SIZE 5
#define MAX_SEND_BYTES 5

#define trigPinA 2
#define echoPinA 3
#define trigPinB 4
#define echoPinB 5
#define trigPinC 6
#define echoPinC 7
#define trigPinD 8
#define echoPinD 9
#define trigPinE 10
#define echoPinE 11

#define distMinA 60    // anvendes til mapping af output til omraadet 0-100
#define distMaxA 700
#define distMinB 60    // anvendes til mapping af output til omraadet 0-100
#define distMaxB 700
#define distMinC 60    // anvendes til mapping af output til omraadet 0-100
#define distMaxC 700
#define distMinD 60    // anvendes til mapping af output til omraadet 0-100
#define distMaxD 700
#define distMinE 60    // anvendes til mapping af output til omraadet 0-100
#define distMaxE 700

byte registerMap[REG_MAP_SIZE];

const int numReadings = 100;

int readingsA[numReadings];
int readIndexA = 0;
int totalA = 0;
int averageA = 0;

int readingsB[numReadings];
int readIndexB = 0;
int totalB = 0;
int averageB = 0;

int readingsC[numReadings];
int readIndexC = 0;
int totalC = 0;
int averageC = 0;

int readingsD[numReadings];
int readIndexD = 0;
int totalD = 0;
int averageD = 0;

int readingsE[numReadings];
int readIndexE = 0;
int totalE = 0;
int averageE = 0;

void setup()
{
  Wire.begin(Slave_ADDRESS);
  Wire.onRequest(requestEvent);
  
  for (int i = 0; i < REG_MAP_SIZE; i++)
  {
    registerMap[i] = 0;
  }
  
  pinMode(trigPinA, OUTPUT);
  pinMode(echoPinA, INPUT);
  pinMode(trigPinB, OUTPUT);
  pinMode(echoPinB, INPUT);
  pinMode(trigPinC, OUTPUT);
  pinMode(echoPinC, INPUT);
  pinMode(trigPinD, OUTPUT);
  pinMode(echoPinD, INPUT);
  pinMode(trigPinE, OUTPUT);
  pinMode(echoPinE, INPUT);

  for (int i = 0; i < numReadings; i++)
  {
    readingsA[i] = 0;
    readingsB[i] = 0;
    readingsC[i] = 0;
    readingsD[i] = 0;
    readingsE[i] = 0;
  }
}

void loop()
{
  delay(10);
  
  long durationA,distanceA;
  long durationB,distanceB;
  long durationC,distanceC;
  long durationD,distanceD;
  long durationE,distanceE;
  
  totalA = totalA - readingsA[readIndexA];
  digitalWrite(trigPinA, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinA, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinA, LOW);
  durationA = pulseIn(echoPinA, HIGH);
  distanceA = durationA * 0.34/2+10;    // afstanden i mm
  readingsA[readIndexA] = distanceA;
  totalA = totalA + readingsA[readIndexA];
  readIndexA = readIndexA + 1;
  if (readIndexA >= numReadings)
  {
    readIndexA = 0;
  }
  averageA = totalA / numReadings;
  averageA = map(averageA, distMinA, distMaxA, 0, 100);
  registerMap[0] = averageA;
  
  totalB = totalB - readingsB[readIndexB];
  digitalWrite(trigPinB, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinB, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinB, LOW);
  durationB = pulseIn(echoPinB, HIGH);
  distanceB = durationB * 0.34/2+10;    // afstanden i mm
  readingsB[readIndexB] = distanceB;
  totalB = totalB + readingsB[readIndexB];
  readIndexB = readIndexB + 1;
  if (readIndexB >= numReadings)
  {
    readIndexB = 0;
  }
  averageB = totalB / numReadings;
  averageB = map(averageB, distMinB, distMaxB, 0, 100);
  registerMap[1] = averageB;

  totalC = totalC - readingsC[readIndexC];
  digitalWrite(trigPinC, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinC, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinC, LOW);
  durationC = pulseIn(echoPinC, HIGH);
  distanceC = durationC * 0.34/2+10;    // afstanden i mm
  readingsC[readIndexC] = distanceC;
  totalC = totalC + readingsC[readIndexC];
  readIndexC = readIndexC + 1;
  if (readIndexC >= numReadings)
  {
    readIndexC = 0;
  }
  averageC = totalC / numReadings;
  averageC = map(averageC, distMinC, distMaxC, 0, 100);
  registerMap[2] = averageC;

  totalD = totalD - readingsD[readIndexD];
  digitalWrite(trigPinD, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinD, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinD, LOW);
  durationD = pulseIn(echoPinD, HIGH);
  distanceD = durationD * 0.34/2+10;    // afstanden i mm
  readingsD[readIndexD] = distanceD;
  totalD = totalD + readingsD[readIndexD];
  readIndexD = readIndexD + 1;
  if (readIndexD >= numReadings)
  {
    readIndexD = 0;
  }
  averageD = totalD / numReadings;
  averageD = map(averageD, distMinD, distMaxD, 0, 100);
  registerMap[3] = averageD;

  totalE = totalE - readingsE[readIndexE];
  digitalWrite(trigPinE, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPinE, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPinE, LOW);
  durationE = pulseIn(echoPinE, HIGH);
  distanceE = durationE * 0.34/2+10;    // afstanden i mm
  readingsE[readIndexE] = distanceE;
  totalE = totalE + readingsE[readIndexE];
  readIndexE = readIndexE + 1;
  if (readIndexE >= numReadings)
  {
    readIndexE = 0;
  }
  averageE = totalE / numReadings;
  averageE = map(averageE, distMinE, distMaxE, 0, 100);
  registerMap[4] = averageE;
}

void requestEvent()
{
 byte buffer[5];
 for (int i = 0; i<5;i++)
 {
   buffer[i] = registerMap[i];
 }
 Wire.write(buffer,5);
}

