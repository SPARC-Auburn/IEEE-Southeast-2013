/*
 * This file will contain the driveTurn and driveStraight functions.
 *
 * The motors will already be set; these functions will only need to run
 * a delay loop.  Inside the loop must be adjustment routines,
 * including a call to odometry, motor calibration for traveling straight,
 * escape condition when either target has been reached or line detected,
 * and acceleration calculation adjustment.
 */
#define TARGET_PRECISION 5 // Must be this distance from target to return success
#define STRAY_ERROR      1 // If we get this much farther from target than we were before, return an error.
#define THETA_PRECISION  .03 // Must be this many radians from target angle for success
#define STRAY_ERROR_TH   .01 // If we get this much farther form target than we were before, return an error
#define STRAIGHT_TIMEOUT 5000 // No moves for longer than 15 seconds
 
int driveTurn(double newTheta, boolean useLines) {
  int motorSpeed = 0;
  double umbrella = newTheta - currentLocation.theta; // This is the closest we've been so far
  while(newTheta - currentLocation.theta > THETA_PRECISION) {
      if (odometry() > 0) return globalError;
      analogWrite(P_LEFT_MOTOR_EN, motorSpeed);
      analogWrite(P_RIGHT_MOTOR_EN, motorSpeed);
      
      // Escape conditions
      if (newTheta - currentLocation.theta < umbrella) umbrella = newTheta - currentLocation.theta; // Umbrella update
      //else if (newTheta - currentLocation.theta > umbrella + STRAY_ERROR_TH) {globalError = 5; return 5;} // Stray error
      // Will need to add useLines conditions
      
      // Accelleration Algorithm
      motorSpeed = 255;  // Full steam ahead!
  }
  setMotorPosition(M_BRAKE);
  analogWrite(P_LEFT_MOTOR_EN, 255);
  analogWrite(P_RIGHT_MOTOR_EN, 255);
  return 0; // Success
}

int driveStraight(location target, boolean useLines) {
  long straightTime = millis();
  int motorSpeed = 0;
  double umbrella = dist(currentLocation, target); // This is the closest we've been so far
  while(dist(currentLocation, target) > TARGET_PRECISION) {
      if (odometry() > 0) return globalError;
      analogWrite(P_LEFT_MOTOR_EN, motorSpeed);
      analogWrite(P_RIGHT_MOTOR_EN, motorSpeed);
      
      // Escape conditions
      if (dist(currentLocation, target) < umbrella) umbrella = dist(currentLocation, target); // Umbrella update
      //else if (dist(currentLocation, target) > umbrella + STRAY_ERROR) {globalError = 5; return 5;} // Stray error
      if (millis() > straightTime + STRAIGHT_TIMEOUT) break;
      // Will need to add useLines conditions
      
      // Accelleration Algorithm
      motorSpeed = 255;  // Full steam ahead!
  }
  setMotorPosition(M_BRAKE);
  analogWrite(P_LEFT_MOTOR_EN, 255);
  analogWrite(P_RIGHT_MOTOR_EN, 255);
  
  return 0; // Success
}

double error(location target, location start, location current) {
  return (((current.x-start.x)*(target.y-start.y))-((current.y-start.y)*(target.x-start.x)))/dist(start, target);
}

double dist(location a, location b) {
  return  sqrt(((b.y-a.y)*(b.y-a.y)) + ((b.x-a.x)*(b.x-a.x)));
}

double arcdist(double theta1, double theta2, double radius) {
  return (theta2 - theta1)*radius;
}
