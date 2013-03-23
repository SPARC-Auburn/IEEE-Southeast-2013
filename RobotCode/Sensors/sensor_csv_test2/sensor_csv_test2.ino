
const int P_COLOR_S0 = 2;//pinA
const int P_COLOR_S1 = 3;//pinB
const int P_COLOR_S2 = 6;//pine
const int P_COLOR_S3 = 7;//pinF
const int P_COLOR_OUT = 4;//pinC
const int P_COLOR_LED = 5;//pinD

float w[50];
float r[50];
float b[50];
float g[50];
long tw[50];
long tr[50];
long tb[50];
long tg[50];

void setup() {
  colorSetup();
  Serial.begin(9600);
  delay(100);
}

// primary loop takes color readings from all four channels and displays the raw values once per second.
// What you might wish to do with those values is up to you...
void loop() {
//  double w, r, g, b;
//  long tw, tr, tg, tb;
  
  Serial.print("\n\nwhite time,white value,red time,red value,");
  Serial.println("blue time,blue value,green time,green value,");
  for (int i = 0; i < 50; i++)
  {
    tw[i] = micros();
    w[i] = colorRead(0,1);
    tr[i] = micros();
    r[i] = colorRead(1,1);
    tg[i] = micros();
    g[i] = colorRead(3,1);
    tb[i] = micros();
    b[i] = colorRead(2,1);
  }
  for (int i = 0; i < 50; i++)
  { 
    Serial.print(tw[i]);
    Serial.print(',');
    Serial.print(w[i]);
    Serial.print(',');
    Serial.print(tr[i]);
    Serial.print(',');
    Serial.print(r[i]);
    Serial.print(',');
    Serial.print(tg[i]);
    Serial.print(',');
    Serial.print(g[i]);
    Serial.print(',');
    Serial.print(tb[i]);
    Serial.print(',');
    Serial.print(b[i]);
    Serial.println(',');
  }
  while(1);
}

int detectColor(){

  float white = colorRead(0,1);
  float red = colorRead(1,1);
  float blue = colorRead(2,1);
  float green = colorRead(3,1);
  
  Serial.print("white ");
  Serial.println(white);
  
  Serial.print("red ");
  Serial.println(red);
  
  Serial.print("blue ");
  Serial.println(blue);
  
  Serial.print("green ");
  Serial.println(green);

}

/*
This section will return the pulseIn reading of the selected color.  
It will turn on the sensor at the start taosMode(1), and it will power off the sensor at the end taosMode(0)
color codes: 0=white, 1=red, 2=blue, 3=green
if LEDstate is 0, LED will be off. 1 and the LED will be on.
P_COLOR_OUT is the ouput pin of the TCS3200.
*/
float colorRead(int color, boolean LEDstate){ 
  
  //turn on sensor and use highest frequency/sensitivity setting
  taosMode(1);
  
  //setting for a delay to let the sensor sit for a moment before taking a reading.
  int sensorDelay = 100;
  
  //set the S2 and S3 pins to select the color to be sensed 
  if(color == 0){//white
    digitalWrite(P_COLOR_S3, LOW); //S3
    digitalWrite(P_COLOR_S2, HIGH); //S2
    // Serial.print(" w");
  }
  
  else if(color == 1){//red
    digitalWrite(P_COLOR_S3, LOW); //S3
    digitalWrite(P_COLOR_S2, LOW); //S2
    // Serial.print(" r");
  }
  
  else if(color == 2){//blue
  digitalWrite(P_COLOR_S3, HIGH); //S3
  digitalWrite(P_COLOR_S2, LOW); //S2 
  // Serial.print(" b");
  }
  
  else if(color == 3){//green
    digitalWrite(P_COLOR_S3, HIGH); //S3
    digitalWrite(P_COLOR_S2, HIGH); //S2 
    // Serial.print(" g");
  }
  
  // create a var where the pulse reading from sensor will go
  float readPulse;
  
  //  turn LEDs on or off, as directed by the LEDstate var
  if(LEDstate == 0){
      digitalWrite(P_COLOR_LED, LOW);
  }
  if(LEDstate == 1){
      digitalWrite(P_COLOR_LED, HIGH);
  }
  
  // wait a bit for LEDs to actually turn on, as directed by sensorDelay var
  delay(sensorDelay);
  
  // now take a measurement from the sensor, timing a low pulse on the sensor's "out" pin
  readPulse = pulseIn(P_COLOR_OUT, LOW, 80000);
  
  //if the pulseIn times out, it returns 0 and that throws off numbers. just cap it at 80k if it happens
  if(readPulse < .1){
    readPulse = 80000;
  }
  
  //turn off color sensor and LEDs to save power 
  taosMode(0);
  
  // return the pulse value back to whatever called for it... 
  return readPulse;

}

// Operation modes area, controlled by hi/lo settings on S0 and S1 pins.
//setting mode to zero will put taos into low power mode. taosMode(0);

void taosMode(int mode){
    
    if(mode == 0){
    //power OFF mode-  LED off and both channels "low"
    digitalWrite(P_COLOR_LED, LOW);
    digitalWrite(P_COLOR_S0, LOW); //S0
    digitalWrite(P_COLOR_S1, LOW); //S1
    //  Serial.println("mOFFm");
    
    }else if(mode == 1){
    //this will put in 1:1, highest sensitivity
    digitalWrite(P_COLOR_S0, HIGH); //S0
    digitalWrite(P_COLOR_S1, HIGH); //S1
    // Serial.println("m1:1m");
    
    }else if(mode == 2){
    //this will put in 1:5
    digitalWrite(P_COLOR_S0, HIGH); //S0
    digitalWrite(P_COLOR_S1, LOW); //S1
    //Serial.println("m1:5m");
    
    }else if(mode == 3){
    //this will put in 1:50
    digitalWrite(P_COLOR_S0, LOW); //S0
    digitalWrite(P_COLOR_S1, HIGH); //S1 
    //Serial.println("m1:50m");
    }
    
    return;

}

void colorSetup(){

    //initialize pins
    pinMode(P_COLOR_LED,OUTPUT); //LED pinD
    
    //color mode selection
    pinMode(P_COLOR_S2,OUTPUT); //S2 pinE
    pinMode(P_COLOR_S3,OUTPUT); //s3 pinF
    
    //color response pin (only actual input from taos)
    pinMode(P_COLOR_OUT, INPUT); //P_COLOR_OUT pinC
    
    //communication freq (sensitivity) selection
    pinMode(P_COLOR_S0,OUTPUT); //S0 pinB
    pinMode(P_COLOR_S1,OUTPUT); //S1 pinA 
    
    return;

}
