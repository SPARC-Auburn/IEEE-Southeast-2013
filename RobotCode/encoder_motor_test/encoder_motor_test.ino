// Pins: L's should be digital, Enables should be PWM.---
int PinML1 = 6;
int PinML2 = 7;
int PinMR1 = 8;
int PinMR2 = 9;
int PinEnL = 10;
int PinEnR = 11;
// ---------------------------------------------------------
char incoming;
int motorDelay = 500;
int motorSpeed = 100;
//int wheelSpeedL = 0;
//int wheelSpeedR = 0;

void setup()
{
  Serial.begin(9600);
  motorControllerSetup();
}

void loop()
{
  processIn();
}

void processIn()
{
  if (Serial.available() > 0)
  {
    analogWrite(PinEnL, 0);
    analogWrite(PinEnR, 0);
    incoming = Serial.read();
    
    switch (incoming)
    {
      case 'w': // Move forward at variable speed.
        motorFwd();
        break;
      case 'a': // Turn left.
        motorLeft();
        break;
      case 's': // Move backward.
        motorRev();
        break;
      case 'd': // Turn right.
        motorRight();
        break;
      case 'q': // Up and left.
        motorFwdLeft();
        break;
      case 'e': // Up and right.
        motorFwdRight();
        break;
      case 'z': // Back and left.
        motorRevLeft();
        break;
      case 'c': // Back and right.
        motorRevRight();
        break;
      case 'x': // Pause.
        motorBrake();
        break;
      case 'h': // HELP.
        Serial.print("HELP:\n\tW: Move forward.\n\tA: Turn left.\n\tS: Move backward. \n\tD: Turn left.\n");
        Serial.print("\tQ: Move forward and left (right wheel drive only).\n\tE: Move forward and right (left wheel drive only).\n");
        Serial.print("\tZ: Move backwards and left (left wheel drive only).\n\tC: Move backwards and right (right wheel drive only).\n\tX: Wait.\n");
        //Serial.print("\tM: Custom movement.\n\tP: Edit parameters: Want to go faster? Check here.\n");        
        delay(1000);
        break;
      /*case 'p': // Parameters. (bars for readability)--------------------------------------------------------
        Serial.print("Change drive time (positive int in half-seconds (int * 500 ms)):\n");
        while (!Serial.available());
        motorDelay = Serial.read() * 500;
        delay(500);
        do
        {
          Serial.print("Enter drive speed (int 1 to 10):\n");
          while (!Serial.available());
          motorSpeed = Serial.read();
          delay(1000);
        } while (motorSpeed < 1 || motorSpeed > 10);
        delay(1000);
        break;
      case 'm': // Movement (custom). -----------------------------------------------------------------------
        // Disable motors.
        digitalWrite(PinEnL, LOW);
        digitalWrite(PinEnR, LOW);
        
        do // Adjust for left wheel speed.
        {
          Serial.print("Left wheel speed (int -10 to 10):\n");
          wheelSpeedL = Serial.read();
          delay(50);
        } while (wheelSpeedL < -10 || wheelSpeedL > 10);
        if (wheelSpeedL > 0) // Prepare to move left wheel forward.
        {
          digitalWrite(PinML1, LOW);
          digitalWrite(PinML2, HIGH);
        }
        else // Prepare to move left wheel backward.
        {
          digitalWrite(PinML1, HIGH);
          digitalWrite(PinML2, LOW);
        }
        
        do // Adjust for right wheel speed.
        { 
          Serial.print("Right wheel speed (int -10 to 10):\n");
          wheelSpeedR = Serial.read();
          delay(50);
        } while (wheelSpeedR < -10 || wheelSpeedR > 10);
        if (wheelSpeedR > 0) // Prepare to move right wheel forward.
        {
          digitalWrite(PinMR1, LOW);
          digitalWrite(PinMR2, HIGH);
        }
        else // Prepare to move right wheel backward.
        {
          digitalWrite(PinMR1, HIGH);
          digitalWrite(PinMR2, LOW);
        }
        // Re-enable prepped motors.
        analogWrite(PinEnL, 25*abs(wheelSpeedL));
        analogWrite(PinEnR, 25*abs(wheelSpeedR));
        delay(motorDelay);
        break; // -------------------------------------------------------------------------------------------*/
        default:
        motorBrake();
        break;
    }
    
  analogWrite(PinEnL, motorSpeed);
  analogWrite(PinEnR, motorSpeed);
  delay(motorDelay);
  motorBrake();
  analogWrite(PinEnL, 255);
  analogWrite(PinEnR, 255);
  //analogWrite(PinEnL, 0);
  //analogWrite(PinEnR, 0);

  }
}
