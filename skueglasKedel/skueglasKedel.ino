/****************************************************************
 Program til styring af vaeskestanden i skueglas.
 Med anvendelse af Pololu DRV 8825

 Slave nr 0x38 Skueglas for smoereolie.
 Modtager 1 byte fra Masteren med den oenskede vaeskestand i procent.
 Tallet 110 er reserveret til + 1 %
 Tallet 111 er reserveret til - 1 %
 Tallet 112 er reserveret til reset.
 
 Pumpen har 200 step paa en omdrejning, hvilket svarer til XX cm på skueglasset.

 Joergen Friis 29/11-2017
****************************************************************/

#include <Wire.h>
#define Slave_ADDRESS 0x38
#define REG_MAP_SIZE 1

//Konstanter

const int stepPrCm = 100;  // skal fastsaettes eksperimentelt.
const int glasHoejde = 37;
const int startFyldning = 50;
const int limit = 500;

// Navngivning af input og output på Arduinoen
// Digitale I/O pins

const int motorRetning = 2;
const int motorStep = 3;

// Analoge I/O pins

const int irRead = 0;

// Globale Variable

byte registerMap[REG_MAP_SIZE];
int hoejde = 0;
int stepPrProcent = int(glasHoejde * stepPrCm/100);


// Initialisering af programmet

void setup()
{
  Wire.begin(Slave_ADDRESS);
  Wire.onReceive(receiveEvent);
  
  for (int i = 0; i < 1; i++)
  {
    registerMap[i] = 0;
  }
  
  pinMode(motorRetning, OUTPUT);
  pinMode(motorStep, OUTPUT);
  
  pinMode(irRead, INPUT);
  
  reset();
  vaeske(50);
}

// Afvikling af programmet
void loop()
{
  int niveau = registerMap[0];
  if (niveau < 101) vaeske(niveau);
  if (niveau = 110) vaeske(hoejde+1);
  if (niveau = 111) vaeske(hoejde-1);
  if (niveau = 112) reset();
}

// Funktioner

void singleStep()
{
  digitalWrite(motorStep, HIGH);
  delay(5);
  digitalWrite(motorStep, LOW);
  delay(5);
}

void reset()
{
   while (analogRead(irRead) < limit)  // der pumpes væske over i reservoir røret til lysstrålen brydes.
  {
    digitalWrite(motorRetning, HIGH);
    singleStep();
  }
  
  hoejde = 0;
}

void vaeske(int niveau)
{
  if (niveau != hoejde)
  {
    if (niveau > hoejde)
    {
      digitalWrite(motorRetning, HIGH);
      for (int i = 0; i < ((niveau-hoejde)*stepPrProcent); i++)
      {
        singleStep(); 
      }
    }
    if (niveau < hoejde)
    {
      digitalWrite(motorRetning, LOW);
      for (int i = 0; i < ((hoejde-niveau)*stepPrProcent); i++)
      {
        singleStep();
      }
    }
    hoejde = niveau;
  }
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
