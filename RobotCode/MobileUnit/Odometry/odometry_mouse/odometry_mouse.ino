#include <ps2.h>

/*
 * an arduino sketch to interface with a ps/2 mouse.
 * Also uses serial protocol to talk back to the host
 * and report what it finds.
 */
 
// This value is calculated from the theoretic robot measurements as detailed in the loop().
#define RADIUS 7.2111
#define POINTSPERINCH 764

/*
 * Mice should be initialized using PS2 mouse(Data, Clock);
 * Feel free to use whatever pins are convenient.
 */
PS2 mouse1(13, 12); // These values are theory.
PS2 mouse2(10, 11); // Please update.

/*
 * initialize the mouse. Reset it, and place it into remote
 * mode, so we can get the encoder data on demand.
 */
void mouse_init()
{
  mouse1.write(0xff);  // reset
  mouse1.read();  // ack byte
  mouse1.read();  // blank */
  mouse1.read();  // blank */
  mouse1.write(0xf0);  // remote mode
  mouse1.read();  // ack
  mouse2.write(0xff);  // reset
  mouse2.read();  // ack byte
  mouse2.read();  // blank */
  mouse2.read();  // blank */
  mouse2.write(0xf0);  // remote mode
  mouse2.read();  // ack
  delayMicroseconds(100);
}

void setup()
{
  Serial.begin(9600);
  Serial.println("Assuming starting coordinates (0,0) with angle 0 radians:");
  mouse_init();
}

/*
 * get a reading from the mouse and report it back to the
 * host via the serial line.
 */
 
 float posX = 0;
 float posY = 0;
 float angle = 0;

void loop()
{
  char m1x, m2x;
  char m1y, m2y;
  char incoming;
  
  /* get a reading from the mouse */
  mouse1.write(0xeb);  // give me data!
  mouse1.read();       // ignore ack
  mouse1.read();       // ignore status
  m1x = mouse1.read();
  m1y = mouse1.read();
  mouse2.write(0xeb);  // give me data!
  mouse2.read();       // ignore ack
  mouse2.read();       // ignore status
  m2x = mouse2.read();
  m2y = mouse2.read();
  
  // The following assumes a 10" square robot, with wheels mounted 8" apart, 6" in front of the mice, similarly mounted 8" apart.
  // The sensors on the mice are therefore mounted sqrt(6^2 + 4^2)", or ~7.2111", from the center of rotation of the robot.
  
  
  // Assuming that if the x displacement is greater than the y displacement, we are in a rotation.
  if ( abs(m1x) > abs(m1y) || abs(m2x) > abs(m2y))
  {
    // Since the mice are mounted parallel with the robot's frame, rather than oriented towards the center, the net movement of the mouse is sqrt(mx^2 + my^2).
    // I am averaging the net movement of both mice.
    // This value is analogous to the movement along the theoretical circle of rotation around the center of the axle that contains both mice on its boundary.
    float netRotation = (sqrt(m1x * m1x + m1y * m1y) + sqrt(m2x * m2x + m2y * m2y))/2;
    // Ideally the average displacement would accurately reflect the displacement of the robot in any scenario.
    
    // This value is the change, in radians, of the angle of the robot. 
    // netRotation is converted into inches, then divided by the circumference (2piRADIUS) then this ratio is converted into radians (*2pi).
    float angularDisplacement = (netRotation/POINTSPERINCH)/RADIUS;
    
    // If the x values are positive, the robot is rotating to the left, if negative, to the right.
    if ( m1x > 0 && m2x > 0)
        angle -= angularDisplacement;
    else if ( m1x < 0 && m2x < 0)
        angle += angularDisplacement;
  }       
  else 
  {
    // Averaging forward displacements.
    float avgY = (m1y/POINTSPERINCH + m2y/POINTSPERINCH)/2;
    
    // Angles in programming languages start at the positive Y-axis and increase clockwise.
    posY += avgY/cos(angle);
    posX += avgY/sin(angle);
  }
  
  if (Serial.available() > 0)
  {
    incoming = Serial.read();
    
    if (incoming == 'r')
    {
      // Print angle and position on command.
      // Values should be in degrees and inches.
      float angleDeg = angle * 180 / PI;
      
      Serial.print(angleDeg, DEC);
      Serial.print("\tX=");
      Serial.print(posX, DEC);
      Serial.print("\tY=");
      Serial.print(posY, DEC);
      Serial.println();
    }
  }
//  delay(20);  /* twiddle */
}
