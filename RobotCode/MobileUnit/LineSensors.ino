// This function monitors the line sensors

int lineSensors()
{
  int onLines = 0;
  lineSensorValues[0] = readLineCalibrated(P_LINE_FRONT_1, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[0] > LINE_BOUNDARY) onLines++;
  lineSensorValues[1] = readLineCalibrated(P_LINE_FRONT_2, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[1] > LINE_BOUNDARY) onLines++;
  lineSensorValues[2] = readLineCalibrated(P_LINE_FRONT_3, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[2] > LINE_BOUNDARY) onLines++;
  lineSensorValues[3] = readLineCalibrated(P_LINE_FRONT_4, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[3] > LINE_BOUNDARY) onLines++;
  lineSensorValues[4] = readLineCalibrated(P_LINE_FRONT_5, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[4] > LINE_BOUNDARY) onLines++;
  lineSensorValues[5] = readLineCalibrated(P_LINE_FRONT_6, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[5] > LINE_BOUNDARY) onLines++;
  lineSensorValues[6] = readLineCalibrated(P_LINE_FRONT_7, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[6] > LINE_BOUNDARY) onLines++;
  lineSensorValues[7] = readLineCalibrated(P_LINE_FRONT_8, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  if (lineSensorValues[7] > LINE_BOUNDARY) onLines++;
  lineSensorValues[8] = readLineCalibrated(P_LINE_BACK_L, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  //if (lineSensorValues[8] > LINE_BOUNDARY) onLines++;
  lineSensorValues[9] = readLineCalibrated(P_LINE_BACK_R, LINE_CALIB_LOW, LINE_CALIB_HIGH);
  //if (lineSensorValues[9] > LINE_BOUNDARY) onLines++;
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
