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
 * use two spins and one straight move.
 */

//parameters
#define SPECIAL_MOVE_DISTANCE 10

//method declaration
location calcWaypoint(location A, location B, signed char& dir); //may need to add some flags

byte commandConversion() {
  if (bitRead(commandStatus, CS_SPECIAL) && destination.x == 0) {
    // Do special straight backwards move
    destination.x = currentLocation.x - SPECIAL_MOVE_DISTANCE * cos(currentLocation.theta);
    destination.y = currentLocation.y - SPECIAL_MOVE_DISTANCE * sin(currentLocation.theta);
    destination.theta = currentLocation.theta;
    motorPath[0] = M_CORRECT_ME;
    motorPath[1] = M_BACKWARD;
    motorPath[2] = M_CORRECT_ME;
    partOneDest = currentLocation;
    partTwoDest = destination;
    return 0;
  }
  if(currentLocation.x == destination.x && currentLocation.y == destination.y) {
    partOneDest = destination;
    partTwoDest = destination;
    motorPath[0] = M_CORRECT_ME;
    motorPath[1] = M_FORWARD;
    motorPath[2] = M_CORRECT_ME;
    return 0;
  }
  // For now, assume no lines to be used in navigation
  linesPath[0] = 0;
  linesPath[1] = 0;
  linesPath[2] = 0;
  doubleSpin();
  return 0;
  //return doubleSpin(); // For now, assume two spins and a straight move.
}

byte doubleSpin() {
  double midTheta = adjustTheta(atan2(destination.y - currentLocation.y, destination.x - currentLocation.x));
  partOneDest.x = currentLocation.x;
  partOneDest.y = currentLocation.y;
  partOneDest.theta = midTheta;
  partTwoDest.x = destination.x;
  partTwoDest.y = destination.y;
  partTwoDest.theta = midTheta;
  if (adjustTheta(midTheta - currentLocation.theta) > 0) {
    motorPath[0] = M_SPIN_LEFT;
  }
  else {
    motorPath[0] = M_SPIN_RIGHT;
  }
  motorPath[1] = M_FORWARD;
  if (adjustTheta(destination.theta - midTheta) > 0) {
    motorPath[2] = M_SPIN_LEFT;
  }
  else {
    motorPath[2] = M_SPIN_RIGHT;
  }
  motorPath[2] = M_CORRECT_ME; // will correct
  return 0;
}

// return.theta gives the 
byte calcWaypoint(location A, location B) {
  location wp; //waypoint to be returned
  signed char dir = signbit(adjustTheta(atan2((destination.y-currentLocation.y),
                      (destination.x-currentLocation.x))-currentLocation.theta));
  if (dir == 1)
    motorPath[0] = M_FORWARD_LEFT;
  else
    motorPath[0] = M_FORWARD_RIGHT;
  motorPath[2] = 
  //motorPath[0]
  
  partOneDest.theta = atan2( (destination.y-currentLocation.y+HALF_WIDTH*(cos(destination.theta)-cos(currentLocation.theta))*dir),
                    (destination.x-currentLocation.x-HALF_WIDTH*(sin(destination.theta)-sin(currentLocation.theta))*dir));
  partOneDest.x = currentLocation.x + dir*HALF_WIDTH*(sin(partOneDest.theta)-sin(currentLocation.theta));
  partOneDest.y = currentLocation.y - dir*HALF_WIDTH*(cos(partOneDest.theta)-cos(currentLocation.theta));
  partTwoDest.theta = partOneDest.theta;
  partTwoDest.x = destination.x - dir*HALF_WIDTH*(sin(destination.theta)-sin(partOneDest.theta));
  partTwoDest.y = destination.y + dir*HALF_WIDTH*(cos(destination.theta)-cos(partOneDest.theta));  
  return 0;
}

double adjustTheta( double theta )
{
  while (theta > PI)
    theta -= 2*PI;
  while (theta < -PI)
    theta += 2*PI;
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

void correctTurn(int which) {
  if(motorPath[which] == M_CORRECT_ME) {
    if (adjustTheta(partOneDest.theta - currentLocation.theta) > 0) {
      motorPath[which] = M_SPIN_LEFT;
    }
    else {
      motorPath[which] = M_SPIN_RIGHT;
    }
  }
}
