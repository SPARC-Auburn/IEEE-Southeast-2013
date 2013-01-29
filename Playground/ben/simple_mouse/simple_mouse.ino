#include <ps2.h>

/*
 * an arduino sketch to interface with a ps/2 mouse.
 * Also uses serial protocol to talk back to the host
 * and report what it finds.
 */
 

/*
 * Mice should be initialized using PS2 mouse(Clock, Data);
 * Feel free to use whatever pins are convenient.
 */
PS2 mouse1(A1, A0); // These values are theory.

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
  delayMicroseconds(100);
}

void setup()
{
  Serial.begin(9600);
  Serial.println("I'm Here!");
  mouse_init();
}

void loop()
{
  int m1ack, m1stat, m1x, m1y;
  mouse1.write(0xeb);  // give me data!
  m1ack = mouse1.read();       // ignore ack
  m1stat = mouse1.read();       // ignore status
  m1x = mouse1.read();
  m1y = mouse1.read();
  
  Serial.print("X1=");
  Serial.print(m1x);
  Serial.print("\tY1=");
  Serial.print(m1y);
  Serial.print("\tAck=");
  Serial.print(m1ack);
  Serial.print("\tStat=");
  Serial.print(m1stat);
  Serial.println();  
}
