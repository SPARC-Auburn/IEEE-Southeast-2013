#include "encoder.h"
#include <PinChangeInt.h>

//constructor
Encoder::Encoder(int chAPin, int chBPin)
{
    pinChA = chAPin;
    pinChB = chBPin;
    portChA = pinToPort( chAPin );
    portChB = pinToPort( chBPin );
    maskChA = pinToMask( chAPin );
    maskChB = pinToMask( chBPin );
}

Encoder::~Encoder()
{
    //nothing to destruct
}

void Encoder::init()
{
    pinMode(pinChA, INPUT);
    pinMode(pinChB, INPUT);
    digitalWrite(pinChA, HIGH); //pullup
    digitalWrite(pinChB, HIGH); //pullup
    PCintPort::attachInterrupt(pinChA, &intEncA, CHANGE);
    PCintPort::attachInterrupt(pinChB, &intEncB, CHANGE);
}

int Encoder::read()
{
    int temp = count;
    count = 0;
    return temp;
}

void Encoder::intEncA() //ISR for chA
{
    if (((portChA & maskChA) == 0) == ((portChB & maskChB) == 0)) //aka if chA == chB
      count++;
    else
      count--;
}

void Encoder::intEncB() //ISR for chB
{
    if (((portChA & maskChA) == 0) == ((portChB & maskChB) == 0)) //aka if chA == chB
      count--;
    else
      count++;
}
    
uint8_t& Encoder::pinToPort( int pin )
{
    if (pin <= 7) { //pins D0-D7
        return &PORTD; }
    if (pin <= 13) { //pins D8-D13
        return &PORTB; }
    return &PORTC; //pins A0-A5
}

uint8_t Encoder::pinToMask( int pin )
{
    int tempPin = pin;
    if (pin > 19) //error
        return 0;
    else if (pin > 13)
        tempPin -= 14;
    else if (pin > 7)
        tempPin -= 8;
    return (1 << tempPin);
}

