#include <PinChangeInt.h>

uint8_t pinChA;
uint8_t pinChB;
volatile uint8_t * portChA;
volatile uint8_t * portChB;
volatile uint8_t maskChA;
volatile uint8_t maskChB;
volatile int count;

void encoderInit(int chAPin, int chBPin)
{
  pinChA = chAPin;
  pinChB = chBPin;
  portChA=portInputRegister(digitalPinToPort(chAPin));
  portChB=portInputRegister(digitalPinToPort(chBPin));
  maskChA = digitalPinToBitMask(chAPin);
  maskChB = digitalPinToBitMask(chBPin);
  pinMode(pinChA, INPUT);
  pinMode(pinChB, INPUT);
  digitalWrite(pinChA, HIGH); //pullup
  digitalWrite(pinChB, HIGH); //pullup
  PCintPort::attachInterrupt(pinChA, &intEncA, CHANGE);
  PCintPort::attachInterrupt(pinChB, &intEncB, CHANGE);
}

int encoderRead()
{
  int temp = count;
  count = 0;
  return temp;
}

void intEncA()
{   //aka if chA == chB
  if (((*portChA & maskChA) == 0) == ((*portChB & maskChB) == 0))
    count++;
  else
    count--;
}

void intEncB()
{  //aka if chA == chB
  if (((*portChA & maskChA) == 0) == ((*portChB & maskChB) == 0))
    count--;
  else
    count++;
}
