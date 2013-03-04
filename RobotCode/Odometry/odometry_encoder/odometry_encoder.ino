#define DIAM 2.0 //diameter in inches
#define WIDTH 12.0 //distance between wheels in inches
#define RESOLUTION 64 //encoder resolution
#define RATIO 19 //gearbox ratio

enc1 = Encoder(pinA, pinB); //left encoder, clockwise
enc2 = Encoder(pinC, pinD); //right encoder, counterclockwise

//distance between left and right wheels
int rldiff = 0;

//displacement of center point (d) and its x and y components
double d = 0;
double x = 0;
double y = 0;

//change in angle
double theta = 0;

void setup() {
   enc1.init();
   enc2.init();
}

void loop() {
  //clockwise encoder
  int L = enc1.read();
  //counterclockwise encoder
  int R = -enc2.read();
  
  //forward difference between left and right wheels in ticks
  
//  if (R > L)
//    rldiff += abs(R - L);
//  else if (R < L)
    rldiff += abs(L - R);
  
  //convert ticks to inches
  double rl_length = (rldiff * PI * DIAM) / (RESOLUTION * RATIO);
  
  /* Finding distance travelled by center point of axle
  ------------------------------------------------------ */
  
  //center moves average of L and R
  
  d = ((R + L) / 2) * (PI * DIAM) / (RESOLUTION * RATIO);  
   
  
  /* Find change in angle
  ------------------------------------------------------ */
  //if m and n are slopes of two lines: tan(theta) == (m-n)/(1+mn)
  //new slope of robot m == difference in wheel position / distance between wheels or rl_length / width
  //treat original slope n as 0, so tan(theta) == (m-0)/(1+0) == m
  //either find arctan or use small angle approximation
  theta += atan(rl_length/WIDTH);
  
  //with distance d and angle theta, find x and y change of center point
  x += d * sin(theta); //component of d in lateral direction
  y += d * cos(theta); //component of d in longitudinal direction (ex: if angle doesn't change, theta = 0 so y = d)
  

  if (Serial.available() > 0)
  {
    char incoming = Serial.read();
    
    if (incoming == 'r')
    {
      //convert radians to degrees
      theta = theta * 180 / PI;
      
      // send the data back up 
      Serial.print("X=");
      Serial.print(x, DEC);
      Serial.print("\tY=");
      Serial.print(y, DEC);
      Serial.print("\tAngle=");
      Serial.print(theta, DEC);
      Serial.print(" degrees");
      Serial.println();
      
      rldiff = 0;
      d = 0;
      x = 0;
      y = 0;
      theta = 0;
    }
  }
}
  
  
 
