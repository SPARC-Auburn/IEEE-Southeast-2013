void motorControllerSetup() // Enable motor controller and pins, set motors to 'brake'.
{
  pinMode(PinML1, OUTPUT);
  pinMode(PinML2, OUTPUT);
  pinMode(PinMR1, OUTPUT);
  pinMode(PinMR2, OUTPUT);
  pinMode(PinEnL, OUTPUT);
  pinMode(PinEnR, OUTPUT);
  
  digitalWrite(PinEnL, LOW);
  digitalWrite(PinEnR, LOW);
  digitalWrite(PinML1, LOW);
  digitalWrite(PinML2, LOW);
  digitalWrite(PinMR1, LOW);
  digitalWrite(PinMR2, LOW);
  
  //Serial.println("Type 'h' for HELP.\nInitial speed: 100%");
}

void motorFwd()
{
  digitalWrite(PinML1, LOW);
  digitalWrite(PinML2, HIGH);
  digitalWrite(PinMR1, LOW);
  digitalWrite(PinMR2, HIGH);
}

void motorLeft()
{
  digitalWrite(PinML1, HIGH);
  digitalWrite(PinML2, LOW);
  digitalWrite(PinMR1, LOW);
  digitalWrite(PinMR2, HIGH);
}

void motorRev()
{
  digitalWrite(PinML1, HIGH);
  digitalWrite(PinML2, LOW);
  digitalWrite(PinMR1, HIGH);
  digitalWrite(PinMR2, LOW);
}

void motorRight()
{
  digitalWrite(PinML1, LOW);
  digitalWrite(PinML2, HIGH);
  digitalWrite(PinMR1, HIGH);
  digitalWrite(PinMR2, LOW);
}

void motorFwdLeft()
{
  digitalWrite(PinML1, LOW);
  digitalWrite(PinML2, HIGH);
  digitalWrite(PinMR1, LOW);
  digitalWrite(PinMR2, LOW);
}

void motorFwdRight()
{
  digitalWrite(PinML1, LOW);
  digitalWrite(PinML2, LOW);
  digitalWrite(PinMR1, LOW);
  digitalWrite(PinMR2, HIGH);
}

void motorRevLeft()
{
  digitalWrite(PinML1, HIGH);
  digitalWrite(PinML2, LOW);
  digitalWrite(PinMR1, LOW);
  digitalWrite(PinMR2, LOW);
}

void motorRevRight()
{
  digitalWrite(PinML1, LOW);
  digitalWrite(PinML2, LOW);
  digitalWrite(PinMR1, HIGH);
  digitalWrite(PinMR2, LOW);
}

void motorBrake()
{
  digitalWrite(PinML1, LOW);
  digitalWrite(PinML2, LOW);
  digitalWrite(PinMR1, LOW);
  digitalWrite(PinMR2, LOW);
}


