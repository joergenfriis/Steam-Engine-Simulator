/*
Program, der aflaeser stillingen af 6 ventiler:
1: Damp ind
2: Damp ud
3: Kondensator ind
4: Kondensator ud
5: Kedelvand ind
6: Kedelvand ud

Arduino slave 0x36

Der sendes 6 vaerdier til masteren.

Register:
registerMap[0]: Damp ind, 0-100 %
registerMap[1]: Damp ud, 0-100 %
registerMap[2]: Kondensator ind, 0-100 %
registerMap[3]: Kondensator ud, 0-100 %
registerMap[4]: Kedelvand ind, 0-100 %
registerMap[5]: Kedelvand ud, 0-100 %

Joergen Friis 19.12.2017
*/

#include <Wire.h>
#define Slave_ADDRESS 0x36
#define REG_MAP_SIZE 6
#define MAX_SEND_BYTES 6

byte registerMap[REG_MAP_SIZE];

const int numReadings = 100; // antal maalinger i gennemsnittet

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

int readingsF[numReadings];
int readIndexF = 0;
int totalF = 0;
int averageF = 0;

int Amin = 200;
int Amax = 800;
int Bmin = 200;
int Bmax = 800;
int Cmin = 200;
int Cmax = 800;
int Dmin = 200;
int Dmax = 800;
int Emin = 200;
int Emax = 800;
int Fmin = 200;
int Fmax = 800;


void setup()
{
  Wire.begin(Slave_ADDRESS);
  Wire.onRequest(requestEvent);
  
  Serial.begin(9600);
  
  for (int i = 0; i < REG_MAP_SIZE; i++)
  {
    registerMap[i] = 0;
  }
  
  pinMode(A0, INPUT);  //damp ind         (A)
  pinMode(A1, INPUT);  //damp ud          (B)
  pinMode(A2, INPUT);  //kondensator ind  (C)
  pinMode(A3, INPUT);  //kondensator ud   (D)
  pinMode(A6, INPUT);  //kedelvand ind    (E)
  pinMode(A7, INPUT);  //kedelvand ud     (F)
  
  for (int i = 0; i < numReadings; i++)
  {
    readingsA[i] = 0;
    readingsB[i] = 0;
    readingsC[i] = 0;
    readingsD[i] = 0;
    readingsE[i] = 0;
    readingsF[i] = 0;
  }
}

void loop()
{
  delay(10);
   
  totalA = totalA - readingsA[readIndexA];
  readingsA[readIndexA] = analogRead(A0);
  totalA = totalA + readingsA[readIndexA];
  readIndexA = readIndexA + 1;
  if (readIndexA >= numReadings) readIndexA = 0;
  averageA = totalA / numReadings;
  Serial.print("averageA before mapping: ");
  Serial.println(averageA);
  averageA = map(averageA, Amin, Amax, 0, 100);
  Serial.print("averageA after mapping: ");
  Serial.println(averageA);
  registerMap[0] = averageA;
  
  totalB = totalB - readingsB[readIndexB];
  readingsB[readIndexB] = analogRead(A1);
  totalB = totalB + readingsB[readIndexB];
  readIndexB = readIndexB + 1;
  if (readIndexB >= numReadings) readIndexB = 0;
  averageB = totalB / numReadings;
  Serial.print("averageB before mapping: ");
  Serial.println(averageB);
  averageB = map(averageB, Bmin, Bmax, 0, 100);
  Serial.print("averageB after mapping: ");
  Serial.println(averageB);
  registerMap[1] = averageB;

  totalC = totalC - readingsC[readIndexC];
  readingsC[readIndexC] = analogRead(A2);
  totalC = totalC + readingsC[readIndexC];
  readIndexC = readIndexC + 1;
  if (readIndexC >= numReadings) readIndexC = 0;
  averageC = totalC / numReadings;
  Serial.print("averageC before mapping: ");
  Serial.println(averageC);
  averageC = map(averageC, Cmin, Cmax, 0, 100);
  Serial.print("averageC after mapping: ");
  Serial.println(averageC);
  registerMap[2] = averageC;

  totalD = totalD - readingsD[readIndexD];
  readingsD[readIndexD] = analogRead(A3);
  totalD = totalD + readingsD[readIndexD];
  readIndexD = readIndexD + 1;
  if (readIndexD >= numReadings) readIndexD = 0;
  averageD = totalD / numReadings;
  Serial.print("averageD before mapping: ");
  Serial.println(averageD);
  averageD = map(averageD, Dmin, Dmax, 0, 100);
  Serial.print("averageD after mapping: ");
  Serial.println(averageD);
  registerMap[3] = averageD;

  totalE = totalE - readingsE[readIndexE];
  readingsE[readIndexE] = analogRead(A6);
  totalE = totalE + readingsE[readIndexE];
  readIndexE = readIndexE + 1;
  if (readIndexE >= numReadings) readIndexE = 0;
  averageE = totalE / numReadings;
  Serial.print("averageE before mapping: ");
  Serial.println(averageE);
  averageE = map(averageE, Emin, Emax, 0, 100);
  Serial.print("averageE after mapping: ");
  Serial.println(averageE);
  registerMap[4] = averageE;

  totalF = totalF - readingsF[readIndexF];
  readingsF[readIndexF] = analogRead(A7);
  totalF = totalF + readingsF[readIndexF];
  readIndexF = readIndexF + 1;
  if (readIndexF >= numReadings) readIndexF = 0;
  averageF = totalF / numReadings;
  Serial.print("averageF before mapping: ");
  Serial.println(averageF);
  averageF = map(averageF, Fmin, Fmax, 0, 100);
  Serial.print("averageF after mapping: ");
  Serial.println(averageF);
  Serial.println();
  registerMap[5] = averageF; 
}


void requestEvent()
{
 byte buffer[6];
 for (int i = 0; i<6;i++)
 {
   buffer[i] = registerMap[i];
 }
 Wire.write(buffer,6);
}


