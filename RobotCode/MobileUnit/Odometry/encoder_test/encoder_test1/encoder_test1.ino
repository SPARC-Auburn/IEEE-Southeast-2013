//Some code for reading the encoders, using hardware interrupts
//channels A and B MUST be attached to pins 2 and 3 for this to work

//pin 2 = intrpt 0, pin3 = intrpt 1
#define PIN_ENC_A 2
#define PIN_ENC_B 3
#define ENC_MASK 0b00001100

volatile int count;
volatile int state, prevState;

void setup()
{
  Serial.begin(9600);
  
  prevState = state = PORTD & ENC_MASK; 
  if (((PIN_ENC_A == 2) && (PIN_ENC_B == 3)) || ((PIN_ENC_A == 3) && (PIN_ENC_B == 2)) {
     attachInterrupt(PIN_ENC_A - 2, readEncoder, CHANGE);
     attachInterrupt(PIN_ENC_B - 2, readEncoder, CHANGE);
  }
  else {
    Serial.println("ERROR.  Invalid encoder pins.");
  }
  
}

void loop()
{
  Serial.print("Count = ");
  Serial.println(count);
  delay(100);
  
  
}

void readEncoder()
{
  prevState = state;
  state = PORTD & ENC_MASK;
  if (state ^ prevState == 0b1000) { //then A changed
    if ((state == 0b1100) || (state == 0b0000)) {
      count++; }
    else {
      count--; }
  } else {
    if ((state == 0b1100) || (state == 0b0000)) {
      count--; }
    else {
      count++; }
  }
}
