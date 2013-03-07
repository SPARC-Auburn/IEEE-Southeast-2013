// Advanced encoder test

#define MAGIC_SCALE_FACTOR .0049741883681838 // = pi * DIAM / (RESOLUTION * RATIO),  uses D = 1.9
#define WIDTH 9.187 //distance between wheels in inches

void encoderAdvanced() {
  odometryClear();
  delay(20);
  double derivL;
  double derivR;
  double xdot, ydot, thetadot;
  derivL = encoderReadL() / (20.0) * MAGIC_SCALE_FACTOR * 1000;
  derivR = -encoderReadR() / (20.0) * 1000 * MAGIC_SCALE_FACTOR;
  xdot = cos(currentLocation.theta) * (derivL / 2 + derivR / 2);
  ydot = sin(currentLocation.theta) * (derivL / 2 + derivR / 2);
  thetadot = derivR / WIDTH - derivL / WIDTH;
  currentLocation.x += xdot * (20.0) / 1000.0;
  currentLocation.y += ydot * (20.0) / 1000.0;
  currentLocation.theta += thetadot * (20.0) / 1000.0;
  currentLocation.theta = adjustTheta(currentLocation.theta);
}

void encoderAdvancedDriver() {
  double derivL;
  double derivR;
  for(dataIndex = 0; dataIndex < 500; dataIndex++) {
    odometry();
    delay(20);    
    if (dataIndex == 400) {
      setMotorPosition(M_BRAKE);
    }
  }
  for(dataIndex = 0; dataIndex < 500; dataIndex++) {
    Serial.print(dataIndex);
    Serial.print("\t");
    Serial.print(data[0][dataIndex]);
    Serial.print("\t");
    Serial.print(data[1][dataIndex]);
    Serial.print("\t");
    Serial.print(datad[0][dataIndex]);
    Serial.print("\t");
    Serial.println(datad[1][dataIndex]);
  }
}
