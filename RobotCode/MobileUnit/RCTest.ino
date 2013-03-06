void rcTest() {
  setMotorPosition(M_BRAKE);
  analogWrite(P_LEFT_MOTOR_EN, 100);
  analogWrite(P_RIGHT_MOTOR_EN, 100);
  long nextUpdate = millis() + 1000;
  while(true) {
    processIn();
    odometry();
    //delay(100);
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

void processIn()
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
      case 'h': // HELP.
        Serial.print("HELP:\n\tw: Move forward.\n\ta: Turn left.\n\ts: Move backward. \n\td: Turn left.\n");
        Serial.print("\tq: Move forward and left (right wheel drive only).\n\te: Move forward and right (left wheel drive only).\n");
        Serial.print("\tz: Move backwards and left (left wheel drive only).\n\tc: Move backwards and right (right wheel drive only).\n\tx: Wait.\n");
        delay(1000);
        break;
    }
  }
}
