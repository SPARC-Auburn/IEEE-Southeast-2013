#include <PinChangeInt.h>

#define PIN_A 6
#define PIN_B 7

volatile boolean state;
volatile boolean successA;
volatile boolean successB;

void setup()
{
  Serial.begin(9600);
  pinMode(PIN_A, OUTPUT);
  pinMode(PIN_B, OUTPUT);
  digitalWrite(PIN_A, LOW);
  digitalWrite(PIN_B, LOW);
  state = false;
  successA = successB = false;
  PCintPort::attachInterrupt(PIN_A, &intA, CHANGE);
  PCintPort::attachInterrupt(PIN_B, &intB, CHANGE);
}

void loop()
{
  delay(1000);
  successA = successB = false;
  delay(1000);
  Serial.println("Changing pin A...");
  delay(1000);
  state = !state;
  digitalWrite(PIN_A, state);
  delay(1000);
  if (successA)
    Serial.println("intA successful!");
  if (successB)
    Serial.println("intB successful!!!!!");
}


void intA()
{
  //slow and time wasting
  for (int i = 0; i < 1000; i++);
  successA = true;
  digitalWrite(PIN_B, state);
  for (int i = 0; i < 10000; i++);
}

void intB()
{
  successB = true;
}
