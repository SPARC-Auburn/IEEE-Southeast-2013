#include <ps2.h>

/*
 * an arduino sketch to interface with a ps/2 mouse.
 * Also uses serial protocol to talk back to the host
 * and report what it finds.
 */

/*
 * Pin 5 is the mouse data pin, pin 6 is the clock pin
 * Feel free to use whatever pins are convenient.
 */
PS2 mouse(13, 12);

/*
 * initialize the mouse. Reset it, and place it into remote
 * mode, so we can get the encoder data on demand.
 */
void mouse_init()
{
  mouse.write(0xff);  // reset
  mouse.read();  // ack byte
  mouse.read();  // blank */
  mouse.read();  // blank */
  mouse.write(0xf0);  // remote mode
  mouse.read();  // ack
  delayMicroseconds(100);
}

void setup()
{
  Serial.begin(9600);
  mouse_init();
}

/*
 * get a reading from the mouse and report it back to the
 * host via the serial line.
 */
int totalX = 0;
int totalY = 0;

void loop()
{
  char mstat;
  char mx;
  char my;
  char incoming;
  
  /* get a reading from the mouse */
  mouse.write(0xeb);  // give me data!
  mouse.read();      // ignore ack
  mstat = mouse.read();
  mx = mouse.read();
  my = mouse.read();
    
  totalX += mx;
  totalY += my;
  
  if (Serial.available() > 0)
  {
    incoming = Serial.read();
    
    if (incoming == 'r')
    {
      
      /* send the data back up */
      Serial.print(mstat, BIN);
      Serial.print("\tX=");
      Serial.print(totalX, DEC);
      Serial.print("\tY=");
      Serial.print(totalY, DEC);
      Serial.println();
      
      totalX = 0;
      totalY = 0;
    }
  }
//  delay(20);  /* twiddle */
}
