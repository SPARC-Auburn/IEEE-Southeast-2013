#include <ps2.h>

/*
 * an arduino sketch to interface with a ps/2 mouse.
 * Also uses serial protocol to talk back to the host
 * and report what it finds.
 */
 

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
  mouse_init();
}

/*
 * Collects movement data in an array
 * for testing purposes.
 */
 
 // I can't find a way to create an "infinite" array, so I just made them all 1000 objects long.
 char m1xArray[1000], m1yArray[1000];
 char m2xArray[1000], m2yArray[1000];
 char totalX1 = 0;
 char totalY1 = 0;
 char totalX2 = 0;
 char totalY2 = 0;
 int count = 0;

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
  
  // Update total positions.
  totalX1 += m1x;
  totalX2 += m2x;
  totalY1 += m1y;
  totalY2 += m2y;
  
  // Add values to the array.
  m1xArray[count] = m1x;
  m1yArray[count] = m1y;
  m2xArray[count] = m2x;
  m2yArray[count] = m2y;
  
  count++;
  
  // Print arrays and totals.
  if (Serial.available() > 0)
  {
    incoming = Serial.read();
    
    if (incoming == 'r')
    {
      for (int i = 0; i < count; i++)
      {
        Serial.print("X1=");
        Serial.print(m1xArray[i], DEC);
        Serial.print("\tY1=");
        Serial.print(m1yArray[i], DEC);
        Serial.print("\tX2=");
        Serial.print(m2xArray[i], DEC);
        Serial.print("\tY2=");
        Serial.print(m2yArray[i], DEC);
        Serial.println();
      }
      
      Serial.print("TotalX1=");
      Serial.print(totalX1, DEC);
      Serial.print("\tTotalY1=");
      Serial.print(totalY1, DEC);
      Serial.print("\tTotalX2=");
      Serial.print(totalX2, DEC);
      Serial.print("\tTotalY2=");
      Serial.print(totalY2, DEC);
      Serial.println();
      
      // Reintialize values.
      totalX1 = 0;
      totalX2 = 0;
      totalY1 = 0;
      totalY2 = 0;
      count = 0;
    }
  }
//  delay(20);  /* twiddle */
}
