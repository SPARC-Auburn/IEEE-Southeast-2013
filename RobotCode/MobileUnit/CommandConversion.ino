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
 * The basic process will eventually be to have two single-wheel turns and one straight move.
 *        If destination is in front of current location, first move will be forward turn.
 *        If destination is behind current location, first move will be backward turn.
 * Exception: If destination is within turning diameter of current location,
 * use two spins and one straight move.
 */

byte commandConversion() {
  
  // First, see if this should be a special move
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
  
  // Next, see if you just need to turn in place
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

  // For now, just use the double spin simple calculation
  doubleSpin(); 
  return 0;
}

// This method of command conversion models the move as simply spin to straight to spin
byte doubleSpin() {
  
  // The direction you will move is midTheta
  double midTheta = adjustTheta(atan2(destination.y - currentLocation.y, destination.x - currentLocation.x));
  
  // Turn in-place
  partOneDest.x = currentLocation.x;
  partOneDest.y = currentLocation.y;
  partOneDest.theta = midTheta;
  
  // End up at destination facing where you moved
  partTwoDest.x = destination.x;
  partTwoDest.y = destination.y;
  partTwoDest.theta = midTheta;
  
  // Set motorPaths based on need to move right or left
  if (adjustTheta(midTheta - currentLocation.theta) > 0) {
    motorPath[0] = M_SPIN_LEFT;
  }
  else {
    motorPath[0] = M_SPIN_RIGHT;
  }
  motorPath[1] = M_FORWARD;
  motorPath[2] = M_CORRECT_ME; // will correct when correctTurn is called
  return 0;
}

// Not used right now
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

// Keeps theta between -PI and PI
double adjustTheta( double theta )
{
  while (theta > PI)
    theta -= 2*PI;
  while (theta < -PI)
    theta += 2*PI;
  return theta;
}

// Not used right now
// Should return target from the perspective of the origin
// if origin is (0, 1, 0), target will be itself with y shifted down 1.
location relativeCoordinates(location origin, location absoluteTarget) {
  return absoluteTarget;
}

// Not used right now
// opposite of relativeCoordinates
// assume relativeTarget is from perspective of origin, and should return
// what would be the absolute location of the target
location absoluteCoordinates(location origin, location relativeTarget) {
  return relativeTarget;
}

// Sets motorPath variable saved as M_CORRECT_ME to either spin left or right
void correctTurn(int whichSegment) {
  
  if(motorPath[whichSegment] == M_CORRECT_ME) {
    
    if (adjustTheta(partOneDest.theta - currentLocation.theta) > 0) {
      motorPath[whichSegment] = M_SPIN_LEFT;
    }    
    else {
      motorPath[whichSegment] = M_SPIN_RIGHT;
    }
    
  }
  
}
