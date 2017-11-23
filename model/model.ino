/**********************************************************************************************************************************
Arduino I2C slave
til styring af model-dampmaskinen.
Register:
Der modtages 3 bytes: 
1. byte er et tal mellem 0 og 100, der angiver hvor meget energi motoren tilføres
2. byte er et tal mellem 0 og 100, der angiver stillingen på gangskiftet. 255 er fuld kraft frem.
3. byte er 0 eller 1. 1 angiver at modellen skal resettes.

Denne udgave, ver.2, benytter en servomotor til bevægelse af gangskiftet.
servomotoren styres direkte fra Python programmet med programlinjen servo.gangskifte(stilling), hvor stilling er 
0 for fuld frem og 100 for fuld bak. 50 er neutral.

Jørgen Friis 23.08.2017
************************************************************************************************************************************/

#include <Wire.h>
#define SLAVE_ADDRESS 0x52
#define REG_MAP_SIZE 3
#define MAX_SEND_BYTES 3

/***** Global Variables *****/

byte registerMap[REG_MAP_SIZE];

// Navngivning af input og output på Ardinoen
// Digitale I/O pins:

const int irPower = 2;            // Spænding til at drive IR dioden i sensoren på hovedaksen
const int lysLtBund = 9;
const int lysLtTop = 6;
const int lysHtBund = 10;
const int lysHtTop = 5;
const int direction_main = 11;    // 11 Hovedaksel HIGH er mod uret set fra propellen
const int step_main = 12;          // 12 stepmotoren (Motor 1) er indstillet til 1/8 step


// Analoge I/O pins:

const int irRead = 0;              // analog input pin for IR-sensor  
                                    // analog input 4 er I2C (SDA)
                                    // analog input 5 er I2C (SCL)
                                    
                                    
                                    
// Andre konstanter


// Variable ************************************************************************************

int stepPosMain = 0;        // den aktuelle step position for hovedaksen
int limit = 500;              // grænsen for hvornår IR-sensoren detekterer hullet i blændeskiven
int IRinput = 0;

float hastighed = 0;            // hastighed afhænger af den tilførte energi og af stillingen på omstyringen
                              // Hvis omstyringen står i midten (stepMax/2) er hastighed = 0 uanset den tilførte energi.
                              // Hastighed varierer mellem -40 og +40 rpm.
                              
long previousMillis_main = 0;      // lagrer klokkeslettet for sidst en steppuls var sendt til hovedmotoren
long interval_main = 0;            // antal millisekunder mellem hvert step på hovedmotoren
int mainMotorState = LOW;

int HtNederst[200];
int HtOverst[200];
int LtNederst[200];
int LtOverst[200];
int counter;

int omstyrVal = 0;              // en værdi mellem 0 og 255, der angiver omstyringshåndtagets stilling. 
                                // 0 er fuld kraft bak, 127 er neutral og 255 er fuld kraft frem.

int energiVal = 0;              // et tal mellem 0-255 der angiver hvor meget energi motoren tilføres.

int resetVal = 0;              // hvis = 1 skal modellen resettes.

//  **************************************************************************************************




void setup()
{    
  Wire.begin(SLAVE_ADDRESS);
  Wire.onReceive(receiveEvent);
  
  pinMode(direction_main,OUTPUT);
  pinMode(step_main,OUTPUT);
  pinMode(irPower,OUTPUT);        // supply 5 volts to photodiode
  pinMode(irRead, INPUT);

  
  slukLys();
  
  // Nulstil RegMap:
  
  registerMap[1] = 0;
  registerMap[2] = 50;      // neutral stilling af gangskifte
  registerMap[3] = 0;
  
  resetEvent();
  stepPosMain = 0;
  
  // Beregning af lysstyrker for de enkelte step på hovedaksen:

  memset(HtNederst, 0, sizeof(HtNederst));    //0-stilling af arrays
  memset(HtOverst, 0, sizeof(HtOverst));
  memset(LtNederst, 0, sizeof(LtNederst));
  memset(LtOverst, 0, sizeof(LtOverst));

  for (counter=0; counter<50; counter++)
  {
    HtNederst[counter] = int(-sin(counter*PI/100 - PI/2) * 255);
    LtOverst[counter] = int(sin(counter*PI/100) * 255);
  }
  
  for (counter=50; counter<100; counter++)
  {
    HtOverst[counter] = int(sin(counter*PI/100 - PI/2) * 255);
    LtOverst[counter] = int(sin(counter*PI/100) * 255);
  }
  
  for (counter=100; counter<150; counter++)
  {
    HtOverst[counter] = int(sin(counter*PI/100 - PI/2) * 255);
    LtNederst[counter] = int(-sin(counter*PI/100) * 255);
  }
  
  for (counter=150; counter<200; counter++)
  {
    HtNederst[counter] = int(-sin(counter*PI/100 - PI/2) * 255);
    LtNederst[counter] = int(-sin(counter*PI/100) * 255);
  }
}


void loop() 
{
  unsigned long currentMillis = millis();            // currentMillis sættes til det antal millisekunder der er gået 
                                                       // siden programmet startede.
    energiVal = registerMap[1];
    omstyrVal = registerMap[2];
    resetVal  = registerMap[3];
    hastighed = ((energiVal*5.0)/100.0)*((omstyrVal - 50.0) / 50.0);  // mellem -20 og +20 omdr/min
    
    if(resetVal !=0)
    {
      resetEvent();
      registerMap[3] = 0;
      stepPosMain = 0;
    }
 
    // Her styres motorhastigheden på hovedmotoren
    if(hastighed != 0)
    { 
      if(hastighed > 0)
      {
        digitalWrite(direction_main, HIGH);    // positive hastigheder kører den ene vej rundt
      }
      else
      {
        digitalWrite(direction_main, LOW);      // negative hastigheder kører den anden vej rundt
      }
        
      interval_main = abs(int((60*1000)/((hastighed * 1600)+1)));    // de 1600 er antal step pr omdrejning på hovedmotoren
                                                                      // +1 for at undgå at dividere med 0
    
      if(currentMillis - previousMillis_main > interval_main)
      {
        previousMillis_main = currentMillis;
      
        if(mainMotorState == LOW)
        {
          mainMotorState = HIGH;
          if (hastighed > 0) stepPosMain +=1;
          if (hastighed < 0) stepPosMain -=1;
          if(stepPosMain == 1600) stepPosMain = 0;
          if (stepPosMain < 0) stepPosMain = 1600 + stepPosMain;
        }
        else
        {
          mainMotorState = LOW;
        }
                
        digitalWrite(step_main, mainMotorState);   
   
        // her styres lyset i cylinderne.  
        if (hastighed > 0)
        { 
          analogWrite(lysHtTop, HtOverst[int(stepPosMain/8)]);
          analogWrite(lysHtBund, HtNederst[int(stepPosMain/8)]);
          analogWrite(lysLtTop, LtOverst[int(stepPosMain/8)]);
          analogWrite(lysLtBund, LtNederst[int(stepPosMain/8)]); 
        }
        else
        {
          analogWrite(lysHtTop, HtNederst[int(stepPosMain/8)]);
          analogWrite(lysHtBund, HtOverst[int(stepPosMain/8)]);
          analogWrite(lysLtTop, LtNederst[int(stepPosMain/8)]);
          analogWrite(lysLtBund, LtOverst[int(stepPosMain/8)]); 
        } 
      }
    }
    
    if (hastighed == 0) slukLys();
}


void singleStepMain()
{
  digitalWrite(step_main, HIGH);
  delay(5);
  digitalWrite(step_main, LOW);
  delay(5);
}

void receiveEvent(int byteCount)
{
  for (int i = 0; i < byteCount; i++)
  {
    byte c = Wire.read();
    registerMap[i] = c;
  }
}

void slukLys()
{
  // Sluk lyset i alle cylindre:
  analogWrite(lysHtTop,0);
  analogWrite(lysHtBund,0);
  analogWrite(lysLtTop,0);
  analogWrite(lysLtBund,0);
}
  

void resetEvent()
{
  
  // Nulstil hovedaksen:
  
  digitalWrite(irPower, HIGH);
  digitalWrite(direction_main, HIGH);
  
  while (true) 
    {
      IRinput = analogRead(irRead);
      
      if (IRinput > limit)
      {
        singleStepMain();
      }
      else
      {
        break;
      }
    }
    
    for (int i = 0; i < 10; i++)    // Her justeres toppunktet i forhold til det punkt hvor IR lyset brydes.
    {
      singleStepMain();
    }
    
    slukLys();
}

