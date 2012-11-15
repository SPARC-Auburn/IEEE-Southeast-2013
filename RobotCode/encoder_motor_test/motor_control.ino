void motorControllerSetup() // Enable motor controller and pins, set motors to 'brake'.
{
  pinMode(L1, OUTPUT);
  pinMode(L2, OUTPUT);
  pinMode(L3, OUTPUT);
  pinMode(L4, OUTPUT);
  pinMode(E1n2, OUTPUT);
  pinMode(E3n4, OUTPUT);
  
  digitalWrite(E1n2, LOW);
  digitalWrite(E3n4, LOW);
  digitalWrite(L1, LOW);
  digitalWrite(L2, LOW);
  digitalWrite(L3, LOW);
  digitalWrite(L4, LOW);
  
  Serial.println("Type 'h' for HELP.\nInitial speed: 100%");
}

void motorFwd()
{
  digitalWrite(L1, LOW);
  digitalWrite(L2, HIGH);
  digitalWrite(L3, LOW);
  digitalWrite(L4, HIGH);
}

void motorLeft()
{
  digitalWrite(L1, HIGH);
  digitalWrite(L2, LOW);
  digitalWrite(L3, LOW);
  digitalWrite(L4, HIGH);
}

void motorRev()
{
  digitalWrite(L1, HIGH);
  digitalWrite(L2, LOW);
  digitalWrite(L3, HIGH);
  digitalWrite(L4, LOW);
}

void motorRight()
{
  digitalWrite(L1, LOW);
  digitalWrite(L2, HIGH);
  digitalWrite(L3, HIGH);
  digitalWrite(L4, LOW);
}

void motorFwdLeft()
{
  digitalWrite(L1, LOW);
  digitalWrite(L2, HIGH);
  digitalWrite(L3, LOW);
  digitalWrite(L4, LOW);
}

void motorFwdRight()
{
  digitalWrite(L1, LOW);
  digitalWrite(L2, LOW);
  digitalWrite(L3, LOW);
  digitalWrite(L4, HIGH);
}

void motorRevLeft()
{
  digitalWrite(L1, HIGH);
  digitalWrite(L2, LOW);
  digitalWrite(L3, LOW);
  digitalWrite(L4, LOW);
}

void motorRevRight()
{
  digitalWrite(L1, LOW);
  digitalWrite(L2, LOW);
  digitalWrite(L3, HIGH);
  digitalWrite(L4, LOW);
}

void motorBrake()
{
  digitalWrite(L1, LOW);
  digitalWrite(L2, LOW);
  digitalWrite(L3, LOW);
  digitalWrite(L4, LOW);
}


