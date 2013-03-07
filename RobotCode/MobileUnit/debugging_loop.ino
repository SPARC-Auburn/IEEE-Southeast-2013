//  Loop with debugging
void debugging() {
  int moves = 0;
  while(true) {
    Serial.println("---------------------------------------");
    Serial.print("Move number: ");
    Serial.println(++moves);
    globalError = 0;
    // The first time this runs, the first command will already be set.
    
    do {  // This is only run once but is used so break command will work.  
      Serial.print("Starting position: (");
      Serial.print(currentLocation.x);
      Serial.print(", ");
      Serial.print(currentLocation.y);
      Serial.print(", ");
      Serial.print(currentLocation.theta);
      Serial.println(")");
      Serial.print("Destination: (");
      Serial.print(destination.x);
      Serial.print(", ");
      Serial.print(destination.y);
      Serial.print(", ");
      Serial.print(destination.theta);
      Serial.println(")");
      prompt();
      Serial.print("Command Conversion: ");
      // Command conversion
      if (commandConversion() > 0) break;
      Serial.print("Motor state 1: ");
      Serial.println(motorPath[0]);
      Serial.print("Part One: to (");
      Serial.print(partOneDest.x);
      Serial.print(", ");
      Serial.print(partOneDest.y);
      Serial.print(", ");
      Serial.print(partOneDest.theta);
      Serial.println(")");
      Serial.print("Motor state 2: ");
      Serial.println(motorPath[1]);
      Serial.print("Part One: to (");
      Serial.print(partTwoDest.x);
      Serial.print(", ");
      Serial.print(partTwoDest.y);
      Serial.print(", ");
      Serial.print(partTwoDest.theta);
      Serial.println(")");
      Serial.print("Motor state 3: ");
      Serial.println(motorPath[2]);      
      prompt();
      // First turn
      Serial.println("Starting first turn");
      correctTurn(0);
      setMotorPosition(motorPath[0]);
      if(driveTurn(partOneDest.theta, linesPath[0]) > 0) break;
      Serial.print("Position after first move: (");
      Serial.print(currentLocation.x);
      Serial.print(", ");
      Serial.print(currentLocation.y);
      Serial.print(", ");
      Serial.print(currentLocation.theta);
      Serial.println(")");
      prompt();
      // Straight move
      Serial.println("Starting straight move");
      setMotorPosition(motorPath[1]);
      Serial.println(dist(partTwoDest, currentLocation));
      if(driveStraight(partTwoDest, linesPath[1]) > 0) break;
      Serial.print("Position after second move: (");
      Serial.print(currentLocation.x);
      Serial.print(", ");
      Serial.print(currentLocation.y);
      Serial.print(", ");
      Serial.print(currentLocation.theta);
      Serial.println(")");
      prompt();
      // Second turn
      Serial.println("Starting second turn");
      correctTurn(2);
      Serial.print("Motor state 3 (corrected): ");
      Serial.println(motorPath[2]);   
      setMotorPosition(motorPath[2]);
      if(driveTurn(destination.theta, linesPath[2]) > 0) break;
      // End action
      Serial.print("Position after third move: (");
      Serial.print(currentLocation.x);
      Serial.print(", ");
      Serial.print(currentLocation.y);
      Serial.print(", ");
      Serial.print(currentLocation.theta);
      Serial.println(")");
      Serial.print("End Action: ");
      Serial.println(commandEndAction);
      globalError = endAction();
    } while(false);
    Serial.print("Out of loop: ");
    Serial.println(globalError);
    // Communicate with base station and determine next move.  
    Serial.println("Comm function ready!");
    prompt();
    Serial.println("Going to comm function: ");
    if (!getBaseCommand()) {
      Serial.println("Fetching Backup: ");
      getBackupCommand();
    }
    commTest();
    prompt();
//    Serial.println("OdomTestValues");
//    for (odomArrayIndex = 0; odomArrayIndex < 100; odomArrayIndex++) {
//      Serial.print("L: ");
//      Serial.print(LodomArray[odomArrayIndex]);
//      Serial.print(" R: ");
//      Serial.println(RodomArray[odomArrayIndex]);
//    }
  }
  Serial.println("Escaped");
}

// Prompt now does nothing!  This acts like a normal operation but sends responses
void prompt() {
    return;
    Serial.println("Waiting for continue command...");
    while(Serial.available()){Serial.read();}
    while(!Serial.available()){}
    while(Serial.available()){Serial.read();}
    Serial.println("Command Received!");
}
