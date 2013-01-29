#include <Servo.h>

//#define DEBUG_MODE 1

const int TRIM_L = 90;
const int TRIM_R = 90;
const int SPEED = 40; //must be < (90 - |trim-90|)
const int DRIVE_TIME = 500; //in ms
const int TURN_TIME = 500; //in ms

#ifdef DEBUG_MODE
  #define NUM_COMMANDS 32
  const char command[] = "fffflllbbbblllffffrrrffffrrrpppp";
#endif



int servoLPin = 9;
int servoRPin = 10;

Servo servoL;
Servo servoR;

#ifdef DEBUG_MODE
int i;
#endif

void setup()
{
  servoL.attach(servoLPin);
  servoR.attach(servoRPin);

  servoL.write(TRIM_L);
  servoR.write(TRIM_R);
  Serial.begin(9600);

}

void loop()
{
  char incoming = -1;
#ifndef DEBUG_MODE
  Serial.print('!');
  if (Serial.available()) {
    incoming = Serial.read();
    Serial.print(incoming);
  }
#else
  incoming = command[i];
  i++;
  i %= NUM_COMMANDS;
#endif

  switch (incoming)
  {
    case 'f':
      servoL.write(TRIM_L+SPEED);
      servoR.write(TRIM_R-SPEED);
      delay(DRIVE_TIME);
      break;
    case 'b':
      servoL.write(TRIM_L-SPEED);
      servoR.write(TRIM_R+SPEED);
      delay(DRIVE_TIME);
      break;
    case 'r':
      servoL.write(TRIM_L-SPEED);
      servoR.write(TRIM_R-SPEED);
      delay(TURN_TIME);
      break;
    case 'l':
      servoL.write(TRIM_L+SPEED);
      servoR.write(TRIM_R+SPEED);
      delay(TURN_TIME);
      break;
    case 'p':
      delay(DRIVE_TIME); //pause
      break;
    default:
      break; //nothing
  }
  servoL.write(TRIM_L); //back to 0 speed
  servoR.write(TRIM_R);
  /*
  analogWrite(9, 0);
  analogWrite(10, 0);
  delay(1000);
  analogWrite(9,255);
  analogWrite(10,255);
  delay(1000);
  */
}
  
      
    
    

