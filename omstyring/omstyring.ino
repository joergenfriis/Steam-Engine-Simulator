/*
Arduino I2C slave
Til måling på omstyringen.
Der returneres et byte med omstyringens stilling.

Register:
Status:            1 byte    read
Omstyring:         1 byte    read  

Programmet læser omstyringens stilling ved hjælp af spændingsfaldet 
over et skydepotentiometer.

Endvidere styrer det en stepmotor, der bestemmer visningen
på en skala over omstyringens stilling. Stepmotoren aktiverer
en microswitch i den ene yderstilling. Stepmotoren kører med 1/4 step.

Joergen Friis 30.06.2017
*/

#include<Wire.h>
#define SLAVE_ADDRESS    0x29    //slave address, any number from 0x01 to 0x7F. 0x er bare et præfix, der i C fortæller compileren, at de efterfølgende nummer er hexadecimalt.
#define REG_MAP_SIZE     2

#define ANALOG_INPUT_PIN A1
#define MOTOR_STEP_PIN 3
#define MOTOR_DIR_PIN 2 
#define MOTOR_STOP_PIN 6

/***** Global Variables ******/

byte registerMap[REG_MAP_SIZE];          // Her reserveres plads til registeret i lageret

int maxStep = 400;      // Her regnes med at stepmotoren har 200*4 step på en omgang.
int minInput = 190;
int maxInput = 820;
int stilling = 0;
int hysterese = 50;

const int numReadings = 25;    // nu større værdi, jo mere udjævnet signal
int readings[numReadings];    // her gemmes værdierne fra det analoge input
int readIndex = 0;            // index af den aktuelle måling
int total = 0;                // den løbende total
int average = 0;              // gennemsnittet af målingerne

void setup()
{
  Wire.begin(SLAVE_ADDRESS);
  Wire.onRequest(requestEvent);  // Kalder funktionen requestEvent når masteren anmoder om data fra slaven
  Serial.begin(9600);            // for debugging
  
  pinMode(ANALOG_INPUT_PIN, INPUT);
  pinMode(MOTOR_STEP_PIN, OUTPUT);
  pinMode(MOTOR_DIR_PIN, OUTPUT);
  pinMode(MOTOR_STOP_PIN, INPUT);
  
  for (int thisReading = 0; thisReading < numReadings; thisReading++)
  {
    readings[thisReading] = 0;
  }
  
  while (digitalRead(MOTOR_STOP_PIN) == HIGH)
  {
    digitalWrite(MOTOR_DIR_PIN,LOW);
    singleStepMotor();
  }
  registerMap[0] = 0;
  registerMap[1] = 0; 
}

void loop()
{  
  delay(10);
  
  total = total - readings[readIndex];    // subtract the last reading
  Serial.print(analogRead(ANALOG_INPUT_PIN));
  Serial.print("\t");
  readings[readIndex] = analogRead(ANALOG_INPUT_PIN);  // aflæs sensoren
  total = total + readings[readIndex];    // adder målingen til totalen
  readIndex = readIndex + 1;              // ryk til næste position i arrayet
  if (readIndex >= numReadings)
  {
    readIndex = 0;
  }
  average = total / numReadings;          // beregn gennemsnittet af målingerne
  
  int input = average;
  Serial.print(input);
  Serial.print("\t");
  
  if (registerMap[1] != input)
  {
    registerMap[0] = 1;
    registerMap[1] = input;
  }
  else
  {
    registerMap[0] = 0;
  }
  
  if (registerMap[0] != 0)
  {
    int nyStilling = map(input,minInput,maxInput,0,maxStep);
    Serial.println(nyStilling);
    if ((nyStilling > (stilling + hysterese)) || (nyStilling < (stilling - hysterese)))
    {
      if (nyStilling > stilling)
      {
        digitalWrite(MOTOR_DIR_PIN, HIGH);
        stilling += 1;
      }
      else
      {
        digitalWrite(MOTOR_DIR_PIN, LOW);
        stilling -= 1;
      }
      singleStepMotor();
    }
  }
}

void requestEvent()
{
  byte buffer[2];             //Vi definerer en midlertidig buffer indeholdende 2 bytes
  buffer[0] = registerMap[0];
  buffer[1] = registerMap[1]; //og fylder indholdet af de relevante celler i registeret ned i bufferen
  Wire.write(buffer,2);
}

void singleStepMotor()
{
  digitalWrite(MOTOR_STEP_PIN, HIGH);
  delay(5);
  digitalWrite(MOTOR_STEP_PIN, LOW);
  delay(5);
}

