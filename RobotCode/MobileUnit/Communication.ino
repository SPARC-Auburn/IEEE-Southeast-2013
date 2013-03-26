    /*
 * This file contains getBaseCommand() function and all supporting functions.
 *
 * First, this will create the Report package and send it to the base station.
 * It will follow the protocol in waiting for a command message.
 * Once a command message is heard, it will check it according to protocol.
 * When finished, the function will have set the following variables:
 *        byte commandStatus
 *        int commandEndAction
 *        int commandEndColor
 *        int commandEndLength
 *        location currentLocation
 *        location destination
 * Once message is properly received, it sends an Ack message.
 * If a long timeout occurs, the function returns false.
 */
boolean getBaseCommand() {
  long finalTime = millis() + COMM_LONG_TIMEOUT;  // Give-up timeout if nothing heard
  commTimesSent = 0;
  commPacketsReceived = 0;
  long i, j;
  double temptheta;
  
  // Continually Send Report message and Listen
  while(true) {
    
    commTimesSent++;
    i = 8;
    j = 0;
    
    // Assemble Report Message
    reportMessage[0] = globalError;
    reportMessage[1] = ((int)(currentLocation.x * X_RESOLUTION)) / 256;
    reportMessage[2] = ((int)(currentLocation.x * X_RESOLUTION)) % 256;
    reportMessage[3] = ((int)(currentLocation.y * Y_RESOLUTION)) / 256;
    reportMessage[4] = ((int)(currentLocation.y * Y_RESOLUTION)) % 256;
    temptheta = currentLocation.theta;
    if (temptheta < 0) {
        temptheta += 2*PI;
    }
    reportMessage[5] = int(temptheta * THETA_RESOLUTION / 256);
    reportMessage[6] = int(temptheta * THETA_RESOLUTION) % 256;
    if(false) {} // Possible extra data
    else {
      reportMessage[7] = commError(reportMessage, 7); // Error Checking
    }
    
    // Send Report Message
    while(Serial3.available()) {Serial3.read();}
    for (j = 0; j < i; j++) {
      Serial3.write(reportMessage[j]);
    }
    
    Serial3.flush();
    
    i = millis();
    
    // Listen for Response, and loop back to top when short timeout expires
    while(millis() < i + COMM_TIMEOUT) {
      
      // Check for Long Timeout Failure
      if (millis() > finalTime) {
        return false;
      }
      
      // Continuous checking for incoming serial message
      if (Serial3.available()) {
        
        // Get message sent
        j = 0;
        commPacketsReceived++;
        while (Serial3.available()) {
          receivedMessage[j] = Serial3.read();
          j++;
          if(j>15) break;
          if(!Serial3.available()) {
            delay(20);
          }
        }
        
        // Was this an Again Message?  Need to re-send Report
        if(receivedMessage[0] == 0xFE) {
          break;
        }
        
        // error-check received message
        if(receivedMessage[15] != commError(receivedMessage, 15)) {
           // Send Error Message
           Serial3.write(0xFB);
           Serial3.flush();
           i = millis();  // Restart long timeout
           continue; 
        }
        
        // acknowledge received
        Serial3.write(0xFD); // Ack
           Serial3.flush();
        Serial3.write(0xFD); // Ack
           Serial3.flush();
        Serial3.write(0xFD); // Ack
           Serial3.flush();
        Serial3.write(0xFD); // Ack
           Serial3.flush();
        Serial3.write(0xFD); // Ack
           Serial3.flush();
        
        // extract parts of received message
        commandStatus = receivedMessage[0];
        if (!bitRead(commandStatus, CS_USE_OWN_CURLOC)) { 
          // Should use own Current Location
          currentLocation.x = ((double)receivedMessage[1]*256 + receivedMessage[2]) / X_RESOLUTION;
          currentLocation.y = ((double)receivedMessage[3]*256 + receivedMessage[4]) / Y_RESOLUTION;
          currentLocation.theta = adjustTheta(((double)receivedMessage[5]*256 + receivedMessage[6]) / THETA_RESOLUTION);
        }
        destination.x = ((double)receivedMessage[7]*256 + receivedMessage[8]) / X_RESOLUTION;
        destination.y = ((double)receivedMessage[9]*256 + receivedMessage[10]) / Y_RESOLUTION;
        destination.theta = adjustTheta(((double)receivedMessage[11]*256 + receivedMessage[12]) / THETA_RESOLUTION);
        commandEndAction = (End_action)(bitRead(receivedMessage[13], 7)*4 + bitRead(receivedMessage[13], 6)*2 + bitRead(receivedMessage[13], 5));
        commandEndColor = bitRead(receivedMessage[13], 4)*4 + bitRead(receivedMessage[13], 3)*2 + bitRead(receivedMessage[13], 2);
        commandEndLength = bitRead(receivedMessage[13], 1)*2 + bitRead(receivedMessage[13], 0);
        
        // message successfully received and interpreted
        return true;
      }
    }
  } 
  // failure
  return false;
}

// calculates the error checking byte for a partial message
byte commError(byte message[], int thisLength) {
  int thisByte;
  byte result = 0;
  for (thisByte = 0; thisByte < thisLength; thisByte++) {
    result = result ^ message[thisByte]; // XOR with next byte
  }
  return result;
}
