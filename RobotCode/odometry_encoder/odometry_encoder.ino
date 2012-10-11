enc1 = Encoder(pinA, pinB); //left encoder, clockwise
enc2 = Encoder(pinC, pinD); //right encoder, counterclockwise

void setup() {
   enc1.init();
   enc2.init();
}

//distance between left and right wheels
int rldiff = 0;

//displacement of center point (d) and its x and y components
double d = 0;
double x = 0;
double y = 0;

//change in angle
double theta = 0;

#define diam 2.0 //diameter in inches
#define width 12.0 //distance between wheels in inches
#define resolution 64 //encoder resolution
#define ratio 19 //gearbox ratio

void loop() {
  //clockwise encoder
  int L = enc1.read();
  //counterclockwise encoder
  int R = -1 * enc2.read();
  
  //forward difference between left and right wheels in ticks
  if (R > L)
    rldiff += abs(R - L);
  else if (R < L)
    rldiff += abs(L - R);
  
  //convert ticks to inches
  double rl_length = (rldiff * PI * diam) / (resolution * ratio);
  
  /* Finding distance travelled by center point of axle
  ------------------------------------------------------ */
  
  //if both wheels move same distance, center point also moves this distance
  if (R == L) 
    d += (R * PI * diam) / (resolution * ratio);
    
  //otherwise, average of left and right wheel motion == movement of center of axle
  /*forward case */
  else if (L > 0 && R > 0                  // both move forward
        || L > 0 && R < 0 && L > abs(R)    // L moves forward more than R moves backward
        || L < 0 && R > 0 && R > abs(L)    // R moves forward more than L moves backward
        || R == 0 && L > 0                 // L moves forward and R doesn't move
        || L == 0 && R > 0)                // R moves forward anf L doesn't move
          d += rl_length / 2;        
  /*backward case */
  else 
          d -= rl_length / 2;  
   
  
  /* Find change in angle
  ------------------------------------------------------ */
  //if m and n are slopes of two lines: tan(theta) == (m-n)/(1+mn)
  //new slope of robot m == difference in wheel position / distance between wheels or rl_length / width
  //treat original slope n as 0, so tan(theta) == (m-0)/(1+0) == m
  //either find arctan or use small angle approximation
  theta += atan(rl_length/width);
  
  //with distance d and angle theta, find x and y change of center point
  x += d * sin(theta); //component of d in lateral direction
  y += d * cos(theta); //component of d in longitudinal direction (ex: if angle doesn't change, theta = 0 so y = d)
  

  if (Serial.available() > 0)
  {
    incoming = Serial.read();
    
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
  
  
 
