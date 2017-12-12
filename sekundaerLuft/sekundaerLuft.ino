/*
Arduino slave 0x33, der maaler aabningen af sekundaer luft spjaeldet
Der sendes en vaerdi til masteren mellem 0 og 100.

Register:
registerMap[0] er aabningen af spjeldet i procent af fuldt aabent.

From bildr article: http://bildr.org/2012/08/rotary-encoder-arduino/

Joergen Friis 12.12.2017
*/

#include <Wire.h>
#define Slave_ADDRESS 0x33
#define REG_MAP_SIZE 1
#define MAX_SEND_BYTES 1

int encoderPin1 = 2;  //det skal vaere interrupt PIN nr 2 og 3
int encoderPin2 = 3;

volatile int lastEncoded = 0;
volatile long encoderValue = 0;

long lastencoderValue = 0;

int lastMSB = 0;
int lastLSB = 0;

byte registerMap[REG_MAP_SIZE];
int encoderMax = 600;  // Den eksperimentelt bestemte maksimale vaerdi for encoderen.
int aabning = 0;

void setup() {
Serial.begin (9600);

Wire.begin(Slave_ADDRESS);
Wire.onRequest(requestEvent);

registerMap[0] = 0;

pinMode(encoderPin1, INPUT);
pinMode(encoderPin2, INPUT);

digitalWrite(encoderPin1, HIGH); //turn pullup resistor on
digitalWrite(encoderPin2, HIGH); //turn pullup resistor on

//call updateEncoder() when any high/low changed seen
//on interrupt 0 (pin 2), or interrupt 1 (pin 3)
attachInterrupt(0, updateEncoder, CHANGE);
attachInterrupt(1, updateEncoder, CHANGE);

}

void loop()
{
  aabning = map(encoderValue, 0,encoderMax,0,100);
  registerMap[0] = aabning;

  Serial.println(encoderValue);
  delay(1000); //just here to slow down the output, and show it will work even during a delay
}

void updateEncoder()
{
  int MSB = digitalRead(encoderPin1); //MSB = most significant bit
  int LSB = digitalRead(encoderPin2); //LSB = least significant bit

  int encoded = (MSB << 1) |LSB; //converting the 2 pin value to single number 
  int sum = (lastEncoded << 2) | encoded; //adding it to the previous encoded value 
  if(sum == 0b1101 || sum == 0b0100 || sum == 0b0010 || sum == 0b1011) encoderValue ++; 
  if(sum == 0b1110 || sum == 0b0111 || sum == 0b0001 || sum == 0b1000) encoderValue --; 
  lastEncoded = encoded; //store this value for next time 
}

void requestEvent()
{
 byte buffer[1];
 buffer[0] = registerMap[0];
 Wire.write(buffer,1);
}

