#include <PinChangeInt.h>

uint8_t pinChLA;
uint8_t pinChLB;
volatile uint8_t * portChLA;
volatile uint8_t * portChLB;
volatile uint8_t maskChLA;
volatile uint8_t maskChLB;
volatile int countL;

uint8_t pinChRA;
uint8_t pinChRB;
volatile uint8_t * portChRA;
volatile uint8_t * portChRB;
volatile uint8_t maskChRA;
volatile uint8_t maskChRB;
volatile int countR;

void encoderInitL(int chAPin, int chBPin)
{
  pinChLA = chAPin;
  pinChLB = chBPin;
  portChLA=portInputRegister(digitalPinToPort(chAPin));
  portChLB=portInputRegister(digitalPinToPort(chBPin));
  maskChLA = digitalPinToBitMask(chAPin);
  maskChLB = digitalPinToBitMask(chBPin);
  pinMode(pinChLA, INPUT);
  pinMode(pinChLB, INPUT);
  digitalWrite(pinChLA, HIGH); //pullup
  digitalWrite(pinChLB, HIGH); //pullup
  PCintPort::attachInterrupt(pinChLA, &intEncLA, CHANGE);
  PCintPort::attachInterrupt(pinChLB, &intEncLB, CHANGE);
}
  
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
  PCintPort::attachInterrupt(pinChRA, &intEncRA, CHANGE);
  PCintPort::attachInterrupt(pinChRB, &intEncRB, CHANGE);
}

int encoderReadL()
{
  int temp = countL;
  countL = 0;
  return temp;
}

void intEncLA()
{   //aka if chA == chB
  if (((*portChLA & maskChLA) == 0) == ((*portChLB & maskChLB) == 0))
    countL++;
  else
    countL--;
}

void intEncLB()
{  //aka if chA == chB
  if (((*portChLA & maskChLA) == 0) == ((*portChLB & maskChLB) == 0))
    countL--;
  else
    countL++;
}

int encoderReadR()
{
  int temp = countR;
  countR = 0;
  return temp;
}

void intEncRA()
{   //aka if chA == chB
  if (((*portChRA & maskChRA) == 0) == ((*portChRB & maskChRB) == 0))
    countR++;
  else
    countR--;
}

void intEncBR()
{  //aka if chA == chB
  if (((*portChRA & maskChRA) == 0) == ((*portChRB & maskChRB) == 0))
    countR--;
  else
    countR++;
}
