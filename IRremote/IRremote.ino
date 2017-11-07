// This sketch will send out a Nikon D50 trigger signal (probably works with most Nikons)
// See the full tutorial at http://www.ladyada.net/learn/sensors/ir.html
// this code is public domain, please enjoy!
//
//modified by Joergen Friis to send on/off and other signals to Blaupunkt TV
//
//I den færdige veresion skal programmet modtage ordrene til hvad der skal sendes over I2C bussen,
//sådan at Arduino loopet læser om der er kommet en ny besked, og hvis det er tilfældet, 
//så sender den det relevante IR-remote signal til TVet.
 
int IRledPin =  13;    // LED connected to digital pin 13
 
// The setup() method runs once, when the sketch starts
 
void setup()   {                
  // initialize the IR digital pin as an output:
  pinMode(IRledPin, OUTPUT);      
 
  Serial.begin(9600);
}
 
void loop()                     
{
  Serial.println("Sending IR signal");
 
  SendBlaupunktONOFF();
 
  delay(30*1000); 
  
  SendBlaupunktRIGHTARROW();
  delay(5*1000);
  SendBlaupunktRIGHTARROW();
  delay(5*1000);
  SendBlaupunktOK();
  delay(5*1000);
  SendBlaupunktOK();
  delay(5*1000);
  SendBlaupunktRIGHTARROW();
  delay(5*1000);
  SendBlaupunktRIGHTARROW();
  delay(5*1000);
  SendBlaupunktRIGHTARROW();
  delay(5*1000);
  SendBlaupunktOK();
  delay(30*1000);
  SendBlaupunktPAUSE();
  delay(10*1000);
  SendBlaupunktPAUSE();
  delay(10*1000);
  SendBlaupunktONOFF();
  delay(30*1000);
  
}
 
// This procedure sends a 38KHz pulse to the IRledPin 
// for a certain # of microseconds. We'll use this whenever we need to send codes
void pulseIR(long microsecs) {
  // we'll count down from the number of microseconds we are told to wait
 
  cli();  // this turns off any background interrupts
 
  while (microsecs > 0) {
    // 38 kHz is about 13 microseconds high and 13 microseconds low
   digitalWrite(IRledPin, HIGH);  // this takes about 3 microseconds to happen
   delayMicroseconds(10);         // hang out for 10 microseconds, you can also change this to 9 if its not working
   digitalWrite(IRledPin, LOW);   // this also takes about 3 microseconds
   delayMicroseconds(10);         // hang out for 10 microseconds, you can also change this to 9 if its not working
 
   // so 26 microseconds altogether
   microsecs -= 26;
  }
 
  sei();  // this turns them back on
}
 
void SendBlaupunktONOFF() {
  // This is the code for my Blaupunkt TV, for others use the tutorial
  // to 'grab' the proper code from the remote
  
  Serial.println("Sending ON/OFF");
 
  pulseIR(8760);
  delayMicroseconds(4433);
  pulseIR(520);
  delayMicroseconds(573);
  pulseIR(527);
  delayMicroseconds(573);
  pulseIR(533);
  delayMicroseconds(560);
  pulseIR(520);
  delayMicroseconds(580);
  pulseIR(520);
  delayMicroseconds(567);
  pulseIR(540);
  delayMicroseconds(553);
  pulseIR(533);
  delayMicroseconds(567);
  pulseIR(527);
  delayMicroseconds(567);
  pulseIR(533);
  delayMicroseconds(1660);
  pulseIR(527);
  delayMicroseconds(1673);
  pulseIR(527);
  delayMicroseconds(1667);
  pulseIR(540);
  delayMicroseconds(1660);
  pulseIR(527);
  delayMicroseconds(1667);
  pulseIR(527);
  delayMicroseconds(1673);
  pulseIR(533);
  delayMicroseconds(1660);
  pulseIR(527);
  delayMicroseconds(573);
  pulseIR(533);
  delayMicroseconds(560);
  pulseIR(527);
  delayMicroseconds(1667);
  pulseIR(533);
  delayMicroseconds(567);
  pulseIR(520);
  delayMicroseconds(1667);
  pulseIR(547);
  delayMicroseconds(553);
  pulseIR(520);
  delayMicroseconds(580);
  pulseIR(520);
  delayMicroseconds(573);
  pulseIR(533);
  delayMicroseconds(560);
  pulseIR(527);
  delayMicroseconds(1667);
  pulseIR(540);
  delayMicroseconds(553);
  pulseIR(527);
  delayMicroseconds(1673);
  pulseIR(533);
  delayMicroseconds(567);
  pulseIR(520);
  delayMicroseconds(1667);
  pulseIR(540);
  delayMicroseconds(1660);
  pulseIR(527);
  delayMicroseconds(1667);
  pulseIR(527);
  delayMicroseconds(1673);
  pulseIR(533);
  delayMicroseconds(40227);
  pulseIR(8753);
  delayMicroseconds(2233);
  pulseIR(533);
}

void SendBlaupunktOK() {
  // This is the code for my Blaupunkt TV, for others use the tutorial
  // to 'grab' the proper code from the remote
  
  Serial.println("Sending OK");
 
  pulseIR(8780);
  delayMicroseconds(4413);
   pulseIR(547);
  delayMicroseconds(547);
  pulseIR(547);
  delayMicroseconds(553);
  pulseIR(520);
  delayMicroseconds(580);
  pulseIR(547);
  delayMicroseconds(540);
  pulseIR(553);
  delayMicroseconds(547);
  pulseIR(527);
  delayMicroseconds(573);
  pulseIR(547);
  delayMicroseconds(547);
  pulseIR(547);
  delayMicroseconds(547);
  pulseIR(527);
  delayMicroseconds(1660);
  pulseIR(560);
  delayMicroseconds(1647);
  pulseIR(547);
  delayMicroseconds(1640);
  pulseIR(533);
  delayMicroseconds(1673);
  pulseIR(547);
  delayMicroseconds(1640);
  pulseIR(567);
  delayMicroseconds(1640);
  pulseIR(527);
  delayMicroseconds(1673);
  pulseIR(547);
  delayMicroseconds(547);
  pulseIR(533);
  delayMicroseconds(567);
  pulseIR(547);
  delayMicroseconds(1640);
  pulseIR(527);
  delayMicroseconds(567);
  pulseIR(553);
  delayMicroseconds(1653);
  pulseIR(527);
  delayMicroseconds(1660);
  pulseIR(553);
  delayMicroseconds(547);
  pulseIR(527);
  delayMicroseconds(1680);
  pulseIR(540);
  delayMicroseconds(547);
  pulseIR(527);
  delayMicroseconds(1647);
  pulseIR(580);
  delayMicroseconds(547);
  pulseIR(527);
  delayMicroseconds(1647);
  pulseIR(560);
  delayMicroseconds(553);
  pulseIR(520);
  delayMicroseconds(573);
  pulseIR(547);
  delayMicroseconds(1633);
  pulseIR(547);
  delayMicroseconds(567);
  pulseIR(547);
  delayMicroseconds(1640);
  pulseIR(540);
  delayMicroseconds(40233);
  pulseIR(8773);
  delayMicroseconds(2213);
  pulseIR(547);
}


void SendBlaupunktRIGHTARROW() {
  // This is the code for my Blaupunkt TV, for others use the tutorial
  // to 'grab' the proper code from the remote
  
  Serial.println("Sending ->");
 
  pulseIR(8793);
  delayMicroseconds(4393);
  pulseIR(553);
  delayMicroseconds(540);
  pulseIR(560);
  delayMicroseconds(547);
  pulseIR(553);
  delayMicroseconds(540);
  pulseIR(533);
  delayMicroseconds(567);
  pulseIR(547);
  delayMicroseconds(547);
  pulseIR(547);
  delayMicroseconds(547);
  pulseIR(533);
  delayMicroseconds(560);
  pulseIR(547);
  delayMicroseconds(547);
  pulseIR(547);
  delayMicroseconds(1647);
  pulseIR(560);
  delayMicroseconds(1640);
  pulseIR(547);
  delayMicroseconds(1653);
  pulseIR(553);
  delayMicroseconds(1640);
  pulseIR(553);
  delayMicroseconds(1647);
  pulseIR(520);
  delayMicroseconds(1673);
  pulseIR(553);
  delayMicroseconds(1647);
  pulseIR(540);
  delayMicroseconds(560);
  pulseIR(547);
  delayMicroseconds(547);
  pulseIR(540);
  delayMicroseconds(553);
  pulseIR(547);
  delayMicroseconds(547);
  pulseIR(547);
  delayMicroseconds(1647);
  pulseIR(547);
  delayMicroseconds(1653);
  pulseIR(520);
  delayMicroseconds(573);
  pulseIR(547);
  delayMicroseconds(1660);
  pulseIR(540);
  delayMicroseconds(553);
  pulseIR(540);
  delayMicroseconds(1653);
  pulseIR(527);
  delayMicroseconds(1673);
  pulseIR(547);
  delayMicroseconds(1640);
  pulseIR(553);
  delayMicroseconds(567);
  pulseIR(540);
  delayMicroseconds(553);
  pulseIR(547);
  delayMicroseconds(1640);
  pulseIR(553);
  delayMicroseconds(553);
  pulseIR(553);
  delayMicroseconds(1660);
  pulseIR(547);
  delayMicroseconds(40227);
  pulseIR(8787);
  delayMicroseconds(2200);
  pulseIR(547);
}

void SendBlaupunktPAUSE() {
  // This is the code for my Blaupunkt TV, for others use the tutorial
  // to 'grab' the proper code from the remote
  
  Serial.println("Sending pause");
 
  pulseIR(8813);
  delayMicroseconds(4380);
  pulseIR(560);
  delayMicroseconds(540);
  pulseIR(553);
  delayMicroseconds(553);
  pulseIR(547);
  delayMicroseconds(533);
  pulseIR(560);
  delayMicroseconds(533);
  pulseIR(560);
  delayMicroseconds(533);
  pulseIR(560);
  delayMicroseconds(540);
  pulseIR(553);
  delayMicroseconds(540);
  pulseIR(560);
  delayMicroseconds(540);
  pulseIR(560);
  delayMicroseconds(1633);
  pulseIR(567);
  delayMicroseconds(1627);
  pulseIR(567);
  delayMicroseconds(1633);
  pulseIR(560);
  delayMicroseconds(1633);
  pulseIR(560);
  delayMicroseconds(1640);
  pulseIR(567);
  delayMicroseconds(1633);
  pulseIR(567);
  delayMicroseconds(1627);
  pulseIR(567);
  delayMicroseconds(533);
  pulseIR(567);
  delayMicroseconds(1627);
  pulseIR(567);
  delayMicroseconds(1640);
  pulseIR(547);
  delayMicroseconds(1647);
  pulseIR(560);
  delayMicroseconds(1627);
  pulseIR(567);
  delayMicroseconds(533);
  pulseIR(567);
  delayMicroseconds(540);
  pulseIR(553);
  delayMicroseconds(1633);
  pulseIR(567);
  delayMicroseconds(527);
  pulseIR(567);
  delayMicroseconds(527);
  pulseIR(567);
  delayMicroseconds(527);
  pulseIR(567);
  delayMicroseconds(533);
  pulseIR(567);
  delayMicroseconds(527);
  pulseIR(573);
  delayMicroseconds(1620);
  pulseIR(573);
  delayMicroseconds(1620);
  pulseIR(573);
  delayMicroseconds(567);
  pulseIR(560);
  delayMicroseconds(1633);
  pulseIR(567);
  delayMicroseconds(40207);
  pulseIR(8800);
  delayMicroseconds(2180);
  pulseIR(520);
}

