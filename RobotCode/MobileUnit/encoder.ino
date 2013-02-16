#include <PinChangeInt.h>

uint8_t pinChLA;  //Left wheel, channel A pin
uint8_t pinChLB;  //Left wheel, channel B pin
volatile uint8_t * portChLA; //port of left ch A
volatile uint8_t * portChLB; //port of left ch B
volatile uint8_t maskChLA; //mask for that port that selects that pin
volatile uint8_t maskChLB; 
volatile int countL; //the count of the left encoder

uint8_t pinChRA; //same as above stuff, but for right wheel
uint8_t pinChRB;
volatile uint8_t * portChRA;
volatile uint8_t * portChRB;
volatile uint8_t maskChRA;
volatile uint8_t maskChRB;
volatile int countR;


//look up interrupt
int pinToInt( int pin )
{
  switch(pin)
  {
    case 2:
      return 0;
    case 3:
      return 1;
    case 21:
      return 2;
    case 20:
      return 3;
    case 19:
      return 4;
    case 18:
      return 5;
  }
  return -1;
}

//initializes the left wheel encoder
//tell it what pins to use
//If you swap the ch A and ch B pins, it will change the sign on the
// encoder count (as if it were going the opposite direction.
void encoderInitL(int chAPin, int chBPin)
{
  int intChLA = pinToInt(chAPin);
  int intChLB = pinToInt(chBPin);
  portChLA=portInputRegister(digitalPinToPort(chAPin)); //gets the port
  portChLB=portInputRegister(digitalPinToPort(chBPin));
  maskChLA = digitalPinToBitMask(chAPin); //gets the mask
  maskChLB = digitalPinToBitMask(chBPin);
  pinMode(pinChLA, INPUT);
  pinMode(pinChLB, INPUT);
  digitalWrite(pinChLA, HIGH); //pullup
  digitalWrite(pinChLB, HIGH); //pullup
  attachInterrupt(intChLA, &intEncLA, CHANGE);
  attachInterrupt(intChLB, &intEncLB, CHANGE);
}

//same as above, but for right wheel
void encoderInitR(int chAPin, int chBPin)
{  
  pinChRA = chAPin;
  pinChRB = chBPin;
  portChRA=portInputRegister(digitalPinToPort(chAPin));
  portChRB=portInputRegister(digitalPinToPort(chBPin));
  maskChRA = digitalPinToBitMask(chAPin);
  maskChRB = digitalPinToBitMask(chBPin);
  pinMode(pinChRA, INPUT);
  pinMode(pinChRB, INPUT);
  digitalWrite(pinChRA, HIGH); //pullup
  digitalWrite(pinChRB, HIGH); //pullup
  attachInterrupt(pinChRA, &intEncRA, CHANGE);
  attachInterrupt(pinChRB, &intEncRB, CHANGE);
}

//reads the current count on the left encoder and resets it to 0
int encoderReadL()
{
  int temp = countL;
  countL = 0;
  return temp;
}

//interrupt for left ch A
void intEncLA()
{   //aka if chA == chB
  if (((*portChLA & maskChLA) == 0) == ((*portChLB & maskChLB) == 0))
    countL++;
  else
    countL--;
}

//interrupt for left ch B
void intEncLB()
{  //aka if chA == chB
  if (((*portChLA & maskChLA) == 0) == ((*portChLB & maskChLB) == 0))
    countL--;
  else
    countL++;
}

//reads the current count on the right encoder and resets it to 0
int encoderReadR()
{
  int temp = countR;
  countR = 0;
  return temp;
}

//interrupt for rught ch A
void intEncRA()
{   //aka if chA == chB
  if (((*portChRA & maskChRA) == 0) == ((*portChRB & maskChRB) == 0))
    countR++;
  else
    countR--;
}

//interrupt for right ch B
void intEncRB()
{  //aka if chA == chB
  if (((*portChRA & maskChRA) == 0) == ((*portChRB & maskChRB) == 0))
    countR--;
  else
    countR++;
}
