#define DIAM 2.0 //diameter in inches
#define WIDTH 12.0 //distance between wheels in inches
#define RESOLUTION 64 //encoder resolution
#define RATIO 19 //gearbox ratio

//distance between left and right wheels
int rldiff = 0;

//displacement of center point (d) and its x and y components
double d = 0;
double x = 0;
double y = 0;

//change in angle
double theta = 0;

void encSetup()
{
  encoderInitL(PinEncLA, PinEncLB);
  encoderInitR(PinEncRA, PinEncRB);
}

void encCalc()
{
  //clockwise encoder
  int L = enc1.read();
  //counterclockwise encoder
  int R = -enc2.read(); //may or may not need to do this, we'll see.
  
  //forward difference between left and right wheels in ticks
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
  
  double temp_theta = theta; //hold old theta
  theta += atan(rl_length/WIDTH);
  temp_theta = (temp_theta + theta)/2; //hold the average of the old and new thetas.
    //we'll use this as an approximation for the direction of the movement
  
  //with distance d and angle theta, find x and y change of center point
  x += d * sin(temp_theta); //component of d in lateral direction
  y += d * cos(temp_theta); //component of d in longitudinal direction (ex: if angle doesn't change, theta = 0 so y = d)
}

double getEncX() {return x;}
double getEncY() {return y;}
double getEncThetat() {return theta;}

void setEncX( double newX ) { x = newX; }
void setEncY( double newY ) { y = newY; }
void setEncTheta( double newTheta ) { theta = newTheta; }

