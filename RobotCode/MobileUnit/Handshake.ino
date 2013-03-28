/*
 *  This file contains the openHandshake() function and all supporting functions.
 *
 *  Requirements: once this method ends, the main program should have its first
 *  command stored in global variables
 *        byte commandStatus
 *        int commandEndAction
 *        int commandEndColor
 *        int commandEndLength
 *        location destination
 *  The sequence should be as follows
 *  1) Begin sending greeting messages while heading toward center of course and maintaining odometry.
 *  2) If reach center, continue sending greetings and waiting.
 *  3) While not sending greeting messages, be listening for Orientation packet
 *  4) When Orientation packet is heard, send report message and if necessary receive correction to Orientation message.
 *  5) Send report message automatically if Orientation message is not heard by timeout.
 *  6) Wait for command or again message, and send report again if necessary.
 *  7) When command is received, set global variables and return.
 *  8) If no command is heard by timeout, call backup plan to set global variables.
 */
void openHandshake() {
  
  // For now, just set current location for testing purposes
  currentLocation.x = 7;
  currentLocation.y = 7;
  currentLocation.theta = 3.14;
  
  return;
  
  // Poll comm until Greeting is received
  while(true) {
    if(Serial3.available()) {
      if(Serial3.read() == 0xFF) {
        break;
      }
    }
  }
  
  
  // Prepare opening move  
  setMotorPosition(M_BACKWARD);
  analogWrite(P_LEFT_MOTOR_EN, HS_BACK_SPEED_LEFT);
  analogWrite(P_RIGHT_MOTOR_EN, HS_BACK_SPEED_RIGHT);
  long openingTime = millis();
  long timeoutTime = millis();
  odometryClear();
  int orientMessRec[22];
  
  // Loop while waiting for Orientation
  while (millis() < timeoutTime + GREETING_TIMEOUT) {
    
    odometry();
    
    // See if there is a message coming
    if (Serial3.available()) {
      
      // If it is another greeting, reset timeout
      if(Serial3.read() == 0xFF) {
        timeoutTime = millis();
      }
      
      // If it is something else, exit immediately
      else {
        while(millis() < openingTime + HANDSHAKE_BACK_TIME) {
          odometry();
        }
        
        // Brake
        setMotorPosition(M_BRAKE);
        analogWrite(P_LEFT_MOTOR_EN, 255);
        analogWrite(P_RIGHT_MOTOR_EN, 255);
        delay(100);
        analogWrite(P_LEFT_MOTOR_EN, 0);
        analogWrite(P_RIGHT_MOTOR_EN, 0);
        odometry();
        
        break;
      }
      
    }
    
    // See if the opening move is complete
    if (millis() > openingTime + HANDSHAKE_BACK_TIME) {
      // Brake
      setMotorPosition(M_BRAKE);
      analogWrite(P_LEFT_MOTOR_EN, 255);
      analogWrite(P_RIGHT_MOTOR_EN, 255);
      delay(100);
      analogWrite(P_LEFT_MOTOR_EN, 0);
      analogWrite(P_RIGHT_MOTOR_EN, 0);
      odometry();
    }
    
  }
  
  // Process Orientation Message
  int j = 0;
  while (Serial3.available()) {
    orientMessRec[j] = Serial3.read();
    j++;
    if(j>21) break;
    if(!Serial3.available()) {
      delay(20);
    }
  }
  // Later, use this space to save all the information in the orientation packet
  // For now, leave not implemented
  
  // Quick Backward Turn
  setMotorPosition(M_BACK_LEFT);
  analogWrite(P_LEFT_MOTOR_EN, 100);
  openingTime = millis();
  while(millis() < openingTime + HANDSHAKE_TURN_TIME) {
    odometry();
  }
  
  // Brake
  setMotorPosition(M_BRAKE);
  analogWrite(P_LEFT_MOTOR_EN, 255);
  analogWrite(P_RIGHT_MOTOR_EN, 255);
  delay(100);
  analogWrite(P_LEFT_MOTOR_EN, 0);
  analogWrite(P_RIGHT_MOTOR_EN, 0);
  odometry();
}
