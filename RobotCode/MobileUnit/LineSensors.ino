// This function monitors the line sensors

int lineSensors()
{  
  int onLines = 0;
  allLineSensors();
  //lineSensorValues[0] = readLineCalibrated(P_LINE_FRONT_1, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[0] < LINE_BOUNDARY) onLines++;
  //lineSensorValues[1] = readLineCalibrated(P_LINE_FRONT_2, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[1] < LINE_BOUNDARY) onLines++;
  //lineSensorValues[2] = readLineCalibrated(P_LINE_FRONT_3, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[2] < LINE_BOUNDARY) onLines++;
  //lineSensorValues[3] = readLineCalibrated(P_LINE_FRONT_4, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[3] < LINE_BOUNDARY) onLines++;
  //lineSensorValues[4] = readLineCalibrated(P_LINE_FRONT_5, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[4] < LINE_BOUNDARY) onLines++;
  //lineSensorValues[5] = readLineCalibrated(P_LINE_FRONT_6, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[5] < LINE_BOUNDARY) onLines++;
  //lineSensorValues[6] = readLineCalibrated(P_LINE_FRONT_7, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[6] < LINE_BOUNDARY) onLines++;
  //lineSensorValues[7] = readLineCalibrated(P_LINE_FRONT_8, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[7] < LINE_BOUNDARY) onLines++;
  //lineSensorValues[8] = readLineCalibrated(P_LINE_BACK_L, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  //if (lineSensorValues[8] < LINE_BOUNDARY) onLines++;
  //lineSensorValues[9] = readLineCalibrated(P_LINE_BACK_R, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  //if (lineSensorValues[9] < LINE_BOUNDARY) onLines++;
  return onLines;
}

int allLineSensors() {
  int onLines = 0;
  boolean done[10];
  done[0] = false;
  done[1] = false;
  done[2] = false;
  done[3] = false;
  done[4] = false;
  done[5] = false;
  done[6] = false;
  done[7] = false;
  done[8] = false;
  done[9] = false;
  unsigned long rawSensorValue;
  lineSensorValues[0] = 1000;
  lineSensorValues[1] = 1000;
  lineSensorValues[2] = 1000;
  lineSensorValues[3] = 1000;
  lineSensorValues[4] = 1000;
  lineSensorValues[5] = 1000;
  lineSensorValues[6] = 1000;
  lineSensorValues[7] = 1000;
  lineSensorValues[8] = 1000;
  lineSensorValues[9] = 1000;
  digitalWrite(P_LINE_FRONT_1, HIGH);
  digitalWrite(P_LINE_FRONT_2, HIGH);
  digitalWrite(P_LINE_FRONT_3, HIGH);
  digitalWrite(P_LINE_FRONT_4, HIGH);
  digitalWrite(P_LINE_FRONT_5, HIGH);
  digitalWrite(P_LINE_FRONT_6, HIGH);
  digitalWrite(P_LINE_FRONT_7, HIGH);
  digitalWrite(P_LINE_FRONT_8, HIGH);
  digitalWrite(P_LINE_BACK_L, HIGH);
  digitalWrite(P_LINE_BACK_R, HIGH);
  pinMode(P_LINE_FRONT_1, OUTPUT);
  pinMode(P_LINE_FRONT_2, OUTPUT);
  pinMode(P_LINE_FRONT_3, OUTPUT);
  pinMode(P_LINE_FRONT_4, OUTPUT);
  pinMode(P_LINE_FRONT_5, OUTPUT);
  pinMode(P_LINE_FRONT_6, OUTPUT);
  pinMode(P_LINE_FRONT_7, OUTPUT);
  pinMode(P_LINE_FRONT_8, OUTPUT);
  pinMode(P_LINE_BACK_L, OUTPUT);
  pinMode(P_LINE_BACK_R, OUTPUT);
  delayMicroseconds(10);
  pinMode(P_LINE_FRONT_1, INPUT);
  pinMode(P_LINE_FRONT_2, INPUT);
  pinMode(P_LINE_FRONT_3, INPUT);
  pinMode(P_LINE_FRONT_4, INPUT);
  pinMode(P_LINE_FRONT_5, INPUT);
  pinMode(P_LINE_FRONT_6, INPUT);
  pinMode(P_LINE_FRONT_7, INPUT);
  pinMode(P_LINE_FRONT_8, INPUT);
  pinMode(P_LINE_BACK_L, INPUT);
  pinMode(P_LINE_BACK_R, INPUT);
  digitalWrite(P_LINE_FRONT_1, LOW);
  digitalWrite(P_LINE_FRONT_2, LOW);
  digitalWrite(P_LINE_FRONT_3, LOW);
  digitalWrite(P_LINE_FRONT_4, LOW);
  digitalWrite(P_LINE_FRONT_5, LOW);
  digitalWrite(P_LINE_FRONT_6, LOW);
  digitalWrite(P_LINE_FRONT_7, LOW);
  digitalWrite(P_LINE_FRONT_8, LOW);
  digitalWrite(P_LINE_BACK_L, LOW);
  digitalWrite(P_LINE_BACK_R, LOW);
  
  unsigned long start_time = micros();
  while (micros() - start_time < LINE_TIMEOUT)
  {
    unsigned long delta_time = micros() - start_time;
    if (digitalRead(P_LINE_FRONT_1) == LOW && !done[0])
    {
      done[0] = true;
      rawSensorValue = delta_time;
      if (rawSensorValue > LINE_CALIB_HIGH) {
        lineSensorValues[0] = 1000;
      }
      else if (rawSensorValue < LINE_CALIB_LOW) {
        lineSensorValues[0] = 0;
      }
      else {
        lineSensorValues[0] = map(rawSensorValue, LINE_CALIB_LOW, LINE_CALIB_HIGH, 0, 1000);
      }
    }
    if (digitalRead(P_LINE_FRONT_2) == LOW && !done[1])
    {
      done[1] = true;
      rawSensorValue = delta_time;
      if (rawSensorValue > LINE_CALIB_HIGH) {
        lineSensorValues[1] = 1000;
      }
      else if (rawSensorValue < LINE_CALIB_LOW) {
        lineSensorValues[1] = 0;
      }
      else {
        lineSensorValues[1] = map(rawSensorValue, LINE_CALIB_LOW, LINE_CALIB_HIGH, 0, 1000);
      }
    }
    if (digitalRead(P_LINE_FRONT_3) == LOW && !done[2])
    {
      done[2] = true;
      rawSensorValue = delta_time;
      if (rawSensorValue > LINE_CALIB_HIGH) {
        lineSensorValues[2] = 1000;
      }
      else if (rawSensorValue < LINE_CALIB_LOW) {
        lineSensorValues[2] = 0;
      }
      else {
        lineSensorValues[2] = map(rawSensorValue, LINE_CALIB_LOW, LINE_CALIB_HIGH, 0, 1000);
      }
    }
    if (digitalRead(P_LINE_FRONT_4) == LOW && !done[3])
    {
      done[3] = true;
      rawSensorValue = delta_time;
      if (rawSensorValue > LINE_CALIB_HIGH) {
        lineSensorValues[3] = 1000;
      }
      else if (rawSensorValue < LINE_CALIB_LOW) {
        lineSensorValues[3] = 0;
      }
      else {
        lineSensorValues[3] = map(rawSensorValue, LINE_CALIB_LOW, LINE_CALIB_HIGH, 0, 1000);
      }
    }
    if (digitalRead(P_LINE_FRONT_5) == LOW && !done[4])
    {
      done[4] = true;
      rawSensorValue = delta_time;
      if (rawSensorValue > LINE_CALIB_HIGH) {
        lineSensorValues[4] = 1000;
      }
      else if (rawSensorValue < LINE_CALIB_LOW) {
        lineSensorValues[4] = 0;
      }
      else {
        lineSensorValues[4] = map(rawSensorValue, LINE_CALIB_LOW, LINE_CALIB_HIGH, 0, 1000);
      }
    }
    if (digitalRead(P_LINE_FRONT_6) == LOW && !done[5])
    {
      done[5] = true;
      rawSensorValue = delta_time;
      if (rawSensorValue > LINE_CALIB_HIGH) {
        lineSensorValues[5] = 1000;
      }
      else if (rawSensorValue < LINE_CALIB_LOW) {
        lineSensorValues[5] = 0;
      }
      else {
        lineSensorValues[5] = map(rawSensorValue, LINE_CALIB_LOW, LINE_CALIB_HIGH, 0, 1000);
      }
    }
    if (digitalRead(P_LINE_FRONT_7) == LOW && !done[6])
    {
      done[6] = true;
      rawSensorValue = delta_time;
      if (rawSensorValue > LINE_CALIB_HIGH) {
        lineSensorValues[6] = 1000;
      }
      else if (rawSensorValue < LINE_CALIB_LOW) {
        lineSensorValues[6] = 0;
      }
      else {
        lineSensorValues[6] = map(rawSensorValue, LINE_CALIB_LOW, LINE_CALIB_HIGH, 0, 1000);
      }
    }
    if (digitalRead(P_LINE_FRONT_8) == LOW && !done[7])
    {
      done[7] = true;
      rawSensorValue = delta_time;
      if (rawSensorValue > LINE_CALIB_HIGH) {
        lineSensorValues[7] = 1000;
      }
      else if (rawSensorValue < LINE_CALIB_LOW) {
        lineSensorValues[7] = 0;
      }
      else {
        lineSensorValues[7] = map(rawSensorValue, LINE_CALIB_LOW, LINE_CALIB_HIGH, 0, 1000);
      }
    }
    if (digitalRead(P_LINE_BACK_L) == LOW && !done[8])
    {
      done[8] = true;
      rawSensorValue = delta_time;
      if (rawSensorValue > LINE_CALIB_HIGH) {
        lineSensorValues[8] = 1000;
      }
      else if (rawSensorValue < LINE_CALIB_LOW) {
        lineSensorValues[8] = 0;
      }
      else {
        lineSensorValues[8] = map(rawSensorValue, LINE_CALIB_LOW, LINE_CALIB_HIGH, 0, 1000);
      }
    }
    if (digitalRead(P_LINE_BACK_R) == LOW && !done[9])
    {
      done[9] = true;
      rawSensorValue = delta_time;
      if (rawSensorValue > LINE_CALIB_HIGH) {
        lineSensorValues[9] = 1000;
      }
      else if (rawSensorValue < LINE_CALIB_LOW) {
        lineSensorValues[9] = 0;
      }
      else {
        lineSensorValues[9] = map(rawSensorValue, LINE_CALIB_LOW, LINE_CALIB_HIGH, 0, 1000);
      }
    }
  }
  return onLines;
}

int readLineSensor(int pin)
{
  int lineSensorValue = LINE_TIMEOUT;
  digitalWrite(pin, HIGH);
  pinMode(pin, OUTPUT);
  
  delayMicroseconds(10);
  
  pinMode(pin, INPUT);
  digitalWrite(pin, LOW);
  
  unsigned long start_time = micros();
  while (micros() - start_time < LINE_TIMEOUT)
  {
    unsigned long delta_time = micros() - start_time;
    if(digitalRead(pin) == LOW && delta_time < lineSensorValue)
    {
      lineSensorValue = delta_time;
    }
  }
  
  return lineSensorValue;
}

int readLineCalibrated(int pin, short High, short Low)
{
  int rawSensorValue = readLineSensor(pin);
  if (rawSensorValue > High)
    return 1000;
  if (rawSensorValue < Low)
    return 0;
  return map(rawSensorValue, Low, High, 0, 1000); 
}
