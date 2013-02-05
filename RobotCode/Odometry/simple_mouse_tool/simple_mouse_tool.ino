#include <ps2.h>

/*
  Contains read mouse data function in other file.
  This file is an example of how to implement.
*/

//Mice should be initialized using PS2 mouse(Clock, Data);
PS2 mouse1(A1, A0);
PS2 mouse2(A3, A2);
int m2x, m2y;
int m1x, m1y;

void readMouseData(PS2 thisMouse, int *mouseX, int *mouseY);


void mouse_init()
{
  mouse1.write(0xff);  // reset
  mouse1.read();  // ack byte
  mouse1.read();  // blank */
  mouse1.read();  // blank */
  mouse1.write(0xf0);  // remote mode
  mouse1.read();  // ack
  delayMicroseconds(100);
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
  Serial.println("I'm Here!");
  mouse_init();
  m1x = 0;
  m1y = 0;
}

void loop()
{
  static int count = 0;
  readMouseData(mouse1, &m1x, &m1y);
  readMouseData(mouse2, &m2x, &m2y);
  if (count > 100) {
    Serial.print("X1=");
    Serial.print(m1x);
    Serial.print("\tY1=");
    Serial.print(m1y);
    Serial.print("\tX2=");
    Serial.print(m2x);
    Serial.print("\tY2=");
    Serial.print(m2y);
    Serial.println();
    count = 0;
  }
  count++;
}

