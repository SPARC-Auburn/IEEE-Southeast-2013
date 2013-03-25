/*
 * This file contains all functions necessary for the debugging process with remote-control protocol
 * The computer will be able to send instructions to the robot for execution
 * Also a good platform for odometry testing
*/
void rcTest() {
  
  setMotorPosition(M_BRAKE);
  analogWrite(P_LEFT_MOTOR_EN, 150);
  analogWrite(P_RIGHT_MOTOR_EN, 150);
  
  // This is when we'll next send currentLocation
  long nextUpdate = millis() + 1000;  
  
  // Do this forever
  while(true) {
    
    if(processIn()) return;  // Handle commands
    
    // **** \\// Inside here play with odometry \\// ****
    
    odometry();
    //delay(100);
    
    // **** //\\ Inside here play with odometry //\\ ****
    
    // Send currentLocation report
    if (millis() > nextUpdate) {
      nextUpdate = millis() + 1000;
      Serial.print("Current position: (");
      Serial.print(currentLocation.x);
      Serial.print(", ");
      Serial.print(currentLocation.y);
      Serial.print(", ");
      Serial.print(currentLocation.theta);
      Serial.println(")");
    }
  }
}

// Incoming messages
int processIn()
{
  if (Serial.available() > 0)
  {
    char incoming = Serial.read();
    switch (incoming)
    {
      case 'w': // Move forward at variable speed.
        setMotorPosition(M_FORWARD);
        break;
      case 'a': // Turn left.
        setMotorPosition(M_SPIN_LEFT);
        break;
      case 's': // Move backward.
        setMotorPosition(M_BACKWARD);
        break;
      case 'd': // Turn right.
        setMotorPosition(M_SPIN_RIGHT);
        break;
      case 'q': // Up and left.
        setMotorPosition(M_FORWARD_LEFT);
        break;
      case 'e': // Up and right.
        setMotorPosition(M_FORWARD_RIGHT);
        break;
      case 'z': // Back and left.
        setMotorPosition(M_BACK_LEFT);
        break;
      case 'c': // Back and right.
        setMotorPosition(M_BACK_RIGHT);
        break;
      case 'x': // Pause.
        setMotorPosition(M_BRAKE);
        break;
      case 'r': // Exit remote mode permanently
        return 1;
      case 'l': 
        // calibrateLineSensor() for each of the 10 line sensors
        calibrateLineSensor(P_LINE_FRONT_1);
        calibrateLineSensor(P_LINE_FRONT_2);
        calibrateLineSensor(P_LINE_FRONT_3);
        calibrateLineSensor(P_LINE_FRONT_4);
        calibrateLineSensor(P_LINE_FRONT_5);
        calibrateLineSensor(P_LINE_FRONT_6);
        calibrateLineSensor(P_LINE_FRONT_7);
        calibrateLineSensor(P_LINE_FRONT_8);
        calibrateLineSensor(P_LINE_BACK_L);
        calibrateLineSensor(P_LINE_BACK_R);
        break;
      case 'h': // HELP.
        Serial.print("HELP:\n\tw: Move forward.\n\ta: Turn left.\n\ts: Move backward. \n\td: Turn left.\n");
        Serial.print("\tq: Move forward and left (right wheel drive only).\n\te: Move forward and right (left wheel drive only).\n");
        Serial.print("\tz: Move backwards and left (left wheel drive only).\n\tc: Move backwards and right (right wheel drive only).\n\tx: Wait.\n");
        Serial.print("\tr: Exit Remote mode permanently\n");
        Serial.print("\tl: Calibrate line sensors\n");
        delay(1000);
        break;
    }
  }
  return 0;
}

void calibrateLineSensor(int pin)
{
  // Do 10 reads, and find max/min of that set of reads
  int j;
  int currentMax = 0, currentMin = 10000;
  for(j = 0; j < 20; j++)
  {
    int rawSensorValue = readLineSensor(pin);
    if (rawSensorValue > currentMax)
      currentMax = rawSensorValue;
    if (rawSensorValue < currentMin)
      currentMin = rawSensorValue;
  }
  Serial.print("Pin: ");
  Serial.println(pin);
  Serial.print("Lowest Value: ");
  Serial.println(currentMin);
  Serial.print("Highest Value: ");
  Serial.println(currentMax);
  return;
}
