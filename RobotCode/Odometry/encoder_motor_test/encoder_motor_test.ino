//encoder pins:
#define PinEncLA 2
#define PinEncLB 3
#define PinEncRA 4
#define PinEncRB 5
//motor control pins
#define PinML1 7
#define PinML2 6
#define PinMR1 9
#define PinMR2 8
#define PinEnL 10 //should be PWM
#define PinEnR 11 //should be PWM
// ---------------------------------------------------------
char incoming;
unsigned int motorDelay = 500;
unsigned int motorSpeed = 100;
//int wheelSpeedL = 0;
//int wheelSpeedR = 0;
unsigned int tempNum;

void setup()
{
  Serial.begin(9600);
  motorControllerSetup();
  encSetup();
}

void loop()
{
  processIn();
  encCalc();
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
        Serial.print("HELP:\n\tw: Move forward.\n\ta: Turn left.\n\ts: Move backward. \n\td: Turn left.\n");
        Serial.print("\tq: Move forward and left (right wheel drive only).\n\te: Move forward and right (left wheel drive only).\n");
        Serial.print("\tz: Move backwards and left (left wheel drive only).\n\tc: Move backwards and right (right wheel drive only).\n\tx: Wait.\n");
        Serial.print("\t[number]D: Set motor delay to [number] ms.\n\t[number]S: Set motor speed to [number], 0 to 255.\n");
        Serial.print("\tp: Print the data from the encoder odometry.");
        //Serial.print("\tM: Custom movement.\n\tP: Edit parameters: Want to go faster? Check here.\n");        
        delay(1000);
        break;
      case '0': case '1': case '2': case '3': case '4':
      case '5': case '6': case '7': case '8': case '9':
        tempNum = tempNum * 10 + (incoming - 0x30);
        break;
      case '-':
        tempNum = 0;
        break;
      case 'S':
        motorSpeed = constrain(tempNum, 0, 255);\
        tempNum = 0;
        Serial.print("Speed: ");
        Serial.println(motorSpeed);
        break;
      case 'D':
        motorDelay = tempNum;
        tempNum = 0;
        Serial.print("Delay: ");
        Serial.println(motorDelay);
        break;
      case 'p':
        Serial.print("(x,y): ( ");
        printDouble(encGetX(), 2);
        Serial.print(" , ");
        printDouble(encGetY(), 2);
        Serial.print(" )\ntheta: ");
        printDouble(encGetTheta(), 4);
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

//used to print the encoder statistics
//function written by user "mem" on the Arduino forums: http://arduino.cc/forum/index.php/topic,44216.0.html
void printDouble( double val, byte precision){
  // prints val with number of decimal places determine by precision
  // precision is a number from 0 to 6 indicating the desired decimial places
  // example: printDouble( 3.1415, 2); // prints 3.14 (two decimal places)

  Serial.print (int(val));  //prints the int part
  if( precision > 0) {
    Serial.print("."); // print the decimal point
    unsigned long frac;
    unsigned long mult = 1;
    byte padding = precision -1;
    while(precision--)
       mult *=10;
       
    if(val >= 0)
      frac = (val - int(val)) * mult;
    else
      frac = (int(val)- val ) * mult;
    unsigned long frac1 = frac;
    while( frac1 /= 10 )
      padding--;
    while(  padding--)
      Serial.print("0");
    Serial.print(frac,DEC) ;
  }
}
