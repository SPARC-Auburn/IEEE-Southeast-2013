#ifndef ENCODER_H
#define ENCODER_H

#include <Arduino.h>

class Encoder {
public:
    Encoder(int chAPin, int chBPin);
    ~Encoder();
    void init();
    int read();
protected:
    uint8_t& pinToPort(int pin);
    uint8_t pinToMask(int pin);
    void intEncA();
    void intEncB();
    int pinChA;
    int pinChB;
    volatile uint8_t& portChA;
    volatile uint8_t& portChB;
    volatile unsigned char maskChA;
    volatile unsigned char maskChB;
    volatile int count;
};
#endif