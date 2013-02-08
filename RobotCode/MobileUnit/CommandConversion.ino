/*
 * This file contains command conversion function and all supporting functions.
 * Takes the following variables:
 *        byte commandStatus
 *        int commandEndAction
 *        int commandEndColor
 *        int commandEndLength
 *        location destination
 * And determines the following variables:
 *        int motorPath[3]
 *        boolean linesPath[3]
 *        location partOneDest
 *        location partTwoDest
 * The basic process is to have two single-wheel turns and one straight move.
 *        If destination is in front of current location, first move will be forward turn.
 *        If destination is behind current location, first move will be backward turn.
 * Exception: If destination is within turning diameter of current location,
 * use two pivots and one straight move.
 */
 
#define HALF_WIDTH 5  // !!! should probably go somewhere more universal
 
//method declaration
location calcWaypoint(location A, location B, signed char& dir); //may need to add some flags
double adjustTheta( double theta ); // !!! should probably go somewhere more universal


byte commandConversion() {
  motorPath[0] = M_FORWARD_RIGHT;
  motorPath[1] = M_FORWARD;
  motorPath[2] = M_FORWARD_LEFT;
  linesPath[0] = false;
  linesPath[1] = false;
  linesPath[2] = false;
  partOneDest.x = 10000;
  partOneDest.y = 10000;
  partOneDest.theta = 0;
  partTwoDest.x = 20000;
  partTwoDest.y = 20000;
  partTwoDest.theta = 0;
  return 0;
}

// return.theta gives the 
location calcWaypoint(location A, location B, signed char& dir) {
  location wp; //waypoint to be returned
  dir = signbit(adjustTheta(atan2((B.y-A.y),(B.x-A.x))-A.theta));
  wp.theta = atan2( (B.y-A.y+HALF_WIDTH*(cos(B.theta)-cos(A.theta))*dir),
                    (B.x-A.x-HALF_WIDTH*(sin(B.theta)-sin(A.theta))*dir));
  wp.x = B.x - dir*HALF_WIDTH*(sin(B.theta)-sin(wp.theta));
  wp.y = B.y + dir*HALF_WDITH*(cos(B.theta)-cos(wp.theta));  
  return wp;
}

double adjustTheta( double theta )
{
  while (theta > PI)
    theta -= PI;
  while (theta < -PI)
    theta += PI;
  return theta;
}
