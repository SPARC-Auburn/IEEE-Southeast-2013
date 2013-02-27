/*
 *  This file contains the openHandshake() function and all supporting functions.
 *
 *  Requirements: once this method ends, the main program should have its first
 *  command stored in global variables
 *        byte commandStatus
 *        int commandEndAction
 *        int commandEndColor
 *        int commandEndLength
 *        location destination
 *  The sequence should be as follows
 *  1) Begin sending greeting messages while heading toward center of course and maintaining odometry.
 *  2) If reach center, continue sending greetings and waiting.
 *  3) While not sending greeting messages, be listening for Orientation packet
 *  4) When Orientation packet is heard, send report message and if necessary receive correction to Orientation message.
 *  5) Send report message automatically if Orientation message is not heard by timeout.
 *  6) Wait for command or again message, and send report again if necessary.
 *  7) When command is received, set global variables and return.
 *  8) If no command is heard by timeout, call backup plan to set global variables.
 */

void openHandshake() {
  currentLocation.x = 20;
  currentLocation.y = 30;
  currentLocation.theta = 0;
  destination.x = 20;
  destination.y = 30;
  destination.theta = 0;
  return;
}
