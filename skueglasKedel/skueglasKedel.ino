/****************************************************************
 Program til styring af vaeskestanden i skueglas.
 Med anvendelse af Pololu DRV 8825

 Slave nr 0x37 Skueglas for kedelvand.
 Modtager 1 byte fra Masteren med den oenskede vaeskestand i procent.
 Tallet 110 er reserveret til + 1 %
 Tallet 111 er reserveret til - 1 %
 Tallet 112 er reserveret til reset.
 
 Pumpen har 200 step paa en omdrejning, hvilket svarer til XX cm på skueglasset.

 Joergen Friis 30/04-2018
****************************************************************/

#include <Wire.h>
#define Slave_ADDRESS 0x37
#define REG_MAP_SIZE 1

//Konstanter

const int stepPrMm = 10;  // skal fastsaettes eksperimentelt.
const int glasHoejde = 35;
const int startFyldning = 60;
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
int stepPrProcent = int(glasHoejde * stepPrMm);


// Initialisering af programmet

void setup()
{
  Wire.begin(Slave_ADDRESS);
  Wire.onReceive(receiveEvent);
  
  Serial.begin(9600);
  Serial.println("Setup begin");
  
  for (int i = 0; i < 1; i++)
  {
    registerMap[i] = 0;
  }
  
  pinMode(motorRetning, OUTPUT);
  pinMode(motorStep, OUTPUT);
  
  pinMode(irRead, INPUT);
  
  Serial.print("stepPrProcent = ");
  Serial.println(stepPrProcent);
  
  reset();
  //vaeske(startFyldning);
}

// Afvikling af programmet
void loop()
{
  delay(1000);
  Serial.print("Loop procedure, analogRead = ");
  Serial.println(analogRead(irRead));
  int niveau = registerMap[0];
  Serial.print("Niveau = ");
  Serial.println(niveau);
  Serial.print("Hoejde = ");
  Serial.println(hoejde);
  if (niveau < 101) vaeske(niveau);
  if (niveau == 110) vaeske(hoejde+1);
  if (niveau == 111) vaeske(hoejde-1);
  if (niveau == 112) reset();
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
  Serial.print("Reset procedure, analogRead = ");
  Serial.println(analogRead(irRead));
  while (analogRead(irRead) < limit)  // der pumpes væske over i reservoir røret til lysstrålen brydes.
  {
    Serial.println(analogRead(irRead));
    digitalWrite(motorRetning, HIGH);
    singleStep();
  }
  
 // while (analogRead(irRead) > limit)
 //{
 // digitalWrite(motorRetning, LOW);
 // singleStep();
  //}
  
  hoejde = 0;
}

void vaeske(int niveau)
{
  Serial.print("Vaeske procedure, niveau = ");
  Serial.println(niveau);
  Serial.print("                  hoejde = ");
  Serial.println(hoejde);
  if (niveau != hoejde)
  {
    if (niveau > hoejde)
    {
      digitalWrite(motorRetning, LOW);
      for (int i = 0; i < ((niveau-hoejde)*stepPrProcent); i++)
      {
        singleStep(); 
      }
    }
    if (niveau < hoejde)
    {
      digitalWrite(motorRetning, HIGH);
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

