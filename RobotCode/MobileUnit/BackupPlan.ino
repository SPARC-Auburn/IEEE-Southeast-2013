/*
 * This file contains the backupPlan function which will set destination
 * according to best knowledge.
 * It must store some version of the course, and pick up one block at a time.
 * Will be simple and no worry about optimal algorithm.
 */

void getBackupCommand() {
  /*  Use this if necessary to debug, it moves forward 10 inches
  currentLocation.x = 20;
  currentLocation.y = 30;
  currentLocation.theta = 0;
  destination.x = 30;
  destination.y = 30;
  destination.theta = 0;
  return;
  */
  
  // Nothing exciting right now, just go to where you are.
  delay(100);
  odometry();
  destination.x = currentLocation.x;
  destination.y = currentLocation.y;
  destination.theta = currentLocation.theta;
  commandStatus = 0;
  commandEndAction = EA_NONE;
  commandEndColor = EC_NONE;
  commandEndLength = 0;
  linesPath[0] = 0;
  linesPath[1] = 0;
  linesPath[2] = 0;
  return;
}
