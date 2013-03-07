// Uses encoder functions in "encoder" to convert to a position value

location encoderLoc = {0,0,0};

void encSetup()
{
  encoderInitL(P_ENC_LEFT_A, P_ENC_LEFT_B);
  encoderInitR(P_ENC_RIGHT_A, P_ENC_RIGHT_B);
}

void encCalc()
{
  //clockwise encoder
  int L = encoderReadL();
  //counterclockwise encoder
  int R = -encoderReadR();
  
  //forward difference between left and right wheels in ticks
  int rldiff = (L - R);
  
  //convert ticks to inches
  double rl_length = rldiff * MAGIC_SCALE_FACTOR;
  
  /* Finding distance travelled by center point of axle
  ------------------------------------------------------ */
  //center moves average of L and R
  double d = ((R + L) / 2.0) * MAGIC_SCALE_FACTOR; 
  
  /* Find change in angle
  ------------------------------------------------------ */
  //if m and n are slopes of two lines: tan(theta) == (m-n)/(1+mn)
  //new slope of robot m == difference in wheel position / distance between wheels or rl_length / width
  //treat original slope n as 0, so tan(theta) == (m-0)/(1+0) == m
  //either find arctan or use small angle approximation
  
  double temp_theta = encoderLoc.theta; //hold old theta
  encoderLoc.theta -= atan(rl_length/WIDTH);
  //encoderLoc.theta -= (rl_length/WIDTH);
  temp_theta = (temp_theta + encoderLoc.theta)/2; //hold the average of the old and new thetas.
    //we'll use this as an approximation for the direction of the movement
  
  
  //with distance d and angle theta, find x and y change of center point
  encoderLoc.y += d * sin(temp_theta); //component of d in lateral direction
  encoderLoc.x += d * cos(temp_theta); //component of d in longitudinal direction (ex: if angle doesn't change, theta = 0 so y = d)
  encoderLoc.theta = adjustTheta(encoderLoc.theta);
}

void encClearReg() {
  encoderReadL(); //clears the encoder count register, don't care about the return value
  encoderReadR(); // ditto
}
  

double encGetX() {return encoderLoc.x;}
double encGetY() {return encoderLoc.y;}
double encGetTheta() {return encoderLoc.theta;}
location encGetLocation() {return encoderLoc;}

void encSetX( double newX ) { encoderLoc.x = newX; }
void encSetY( double newY ) { encoderLoc.y = newY; }
void encSetTheta( double newTheta ) { encoderLoc.theta = newTheta; }
void encSetLocation( location newLoc ) { encoderLoc = newLoc; }
  

