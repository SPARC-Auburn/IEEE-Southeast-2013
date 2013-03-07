/*
 * This file contains all functions necessary for the debugging process with remote-control protocol
 * The computer will be able to send instructions to the robot for execution
 * Also a good platform for odometry testing
*/
void rcTest() {
  
  setMotorPosition(M_BRAKE);
  analogWrite(P_LEFT_MOTOR_EN, 100);
  analogWrite(P_RIGHT_MOTOR_EN, 100);
  
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
      case 'h': // HELP.
        Serial.print("HELP:\n\tw: Move forward.\n\ta: Turn left.\n\ts: Move backward. \n\td: Turn left.\n");
        Serial.print("\tq: Move forward and left (right wheel drive only).\n\te: Move forward and right (left wheel drive only).\n");
        Serial.print("\tz: Move backwards and left (left wheel drive only).\n\tc: Move backwards and right (right wheel drive only).\n\tx: Wait.\n");
        delay(1000);
        break;
    }
  }
  return 0;
}
