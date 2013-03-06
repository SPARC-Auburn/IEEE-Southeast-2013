// Communcation test file

void commTest() {
    Serial.println("\n\nCOMM TEST REPORT");
    Serial.print("Times Sent: ");
    Serial.println(commTimesSent);
    int j;
    for (j = 0; j < 14; j++) {
      Serial.print("Last Sent ");
      Serial.print(j);
      Serial.print(": ");
      Serial.print((int)reportMessage[j]);
      Serial.println();
    }
    Serial.print("Number Packets Received: ");
    Serial.println(commPacketsReceived);
    for (j = 0; j < 16; j++) {
      Serial.print("Last Received ");
      Serial.print(j);
      Serial.print(": ");
      Serial.print((int)receivedMessage[j]);
      Serial.println();
    }
    
}
