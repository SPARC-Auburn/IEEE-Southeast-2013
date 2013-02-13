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

//method declaration
location calcWaypoint(location A, location B, signed char& dir); //may need to add some flags

byte commandConversion() {
  // For now, assume no lines to be used in navigation
  linesPath[0] = 0;
  linesPath[1] = 0;
  linesPath[2] = 0;
  return doublePivot(); // For now, assume two pivots and a straight move.
}

byte doublePivot() {
  double midTheta = adjustTheta(atan2(destination.y - currentLocation.y, destination.x - currentLocation.x));
  partOneDest.x = currentLocation.x;
  partOneDest.y = currentLocation.y;
  partOneDest.theta = midTheta;
  partTwoDest.x = destination.x;
  partTwoDest.y = destination.y;
  partTwoDest.theta = midTheta;
  if (adjustTheta(midTheta - partOneDest.theta) > 0) {
    motorPath[0] = M_PIVOT_LEFT;
  }
  else {
    motorPath[0] = M_PIVOT_RIGHT;
  }
  motorPath[1] = M_FORWARD;
  if (adjustTheta(partTwoDest.theta - midTheta) > 0) {
    motorPath[2] = M_PIVOT_LEFT;
  }
  else {
    motorPath[2] = M_PIVOT_RIGHT;
  }
}

// return.theta gives the 
location calcWaypoint(location A, location B, signed char& dir) {
  location wp; //waypoint to be returned
  dir = signbit(adjustTheta(atan2((B.y-A.y),(B.x-A.x))-A.theta));
  wp.theta = atan2( (B.y-A.y+HALF_WIDTH*(cos(B.theta)-cos(A.theta))*dir),
                    (B.x-A.x-HALF_WIDTH*(sin(B.theta)-sin(A.theta))*dir));
  wp.x = B.x - dir*HALF_WIDTH*(sin(B.theta)-sin(wp.theta));
  wp.y = B.y + dir*HALF_WIDTH*(cos(B.theta)-cos(wp.theta));  
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

// returns target from the perspective of the origin
// if origin is (0, 1, 0), target will be itself with y shifted down 1.
location relativeCoordinates(location origin, location absoluteTarget) {
  return absoluteTarget;
}

// opposite of relativeCoordinates
// assume relativeTarget is from perspective of origin, and return
// what would be the absolute location of the target
location absoluteCoordinates(location origin, location relativeTarget) {
  return relativeTarget;
}
