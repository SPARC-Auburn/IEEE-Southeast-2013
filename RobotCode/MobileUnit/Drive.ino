/*
 * This file will contain the driveTurn and driveStraight functions.
 *
 * The motors will already be set; these functions will only need to run
 * a delay loop.  Inside the loop must be adjustment routines,
 * including a call to odometry, motor calibration for traveling straight,
 * escape condition when either target has been reached or line detected,
 * and acceleration calculation adjustment.
 */
#define TARGET_PRECISION .1 // Must be this distance from target to return success
#define UMBRELLA_ERROR      1 // If we get this much farther from target than we were before, return an error.
#define THETA_PRECISION  .03 // Must be this many radians from target angle for success
#define STRAY_ERROR_TH   .01 // If we get this much farther form target than we were before, return an error
#define STRAIGHT_TIMEOUT 50000 // No moves for longer than 15 seconds
#define TURN_TIMEOUT     10000

#define MIN_SPEED 60
#define MAX_SPEED 230
#define ADDED_DISTANCE  0.3 //in inches, the amount to add to the forward distance to have the effect of adding some initial velocity
#define ACCELERATION_CONSTANT 51.4 //really, the sqrt of the acceleration
      //  = 51.4  corresponds to an accelleration of 0 to full speed (230) in about 20 inches
      //  = 59.4  corresponds to an accelleration of 0 to full speed (230) in about 15 inches
      //  = 72.7  corresponds to an accelleration of 0 to full speed (230) in about 10 inches
#define TURN_RADIUS 9.25

double abs2( double blah ) { double res = abs(blah); return res; }

int driveTurn(double newTheta, boolean useLines) {
  int motorSpeed = 0;
  double maxTheta = newTheta - currentLocation.theta;
  double umbrella = maxTheta; // This is the closest we've been so far
  double halfwayTheta = maxTheta / 2;
  double startTheta = currentLocation.theta;
  double forwardTheta = 0;
  double remainingTheta = maxTheta;
  double temp = MAX_SPEED/ACCELERATION_CONSTANT;
  double accelerationTheta = (temp*temp - ADDED_DISTANCE)/TURN_RADIUS;
  //Serial.println(adjustTheta(newTheta - currentLocation.theta));
  //Serial.println(abs2(adjustTheta(newTheta - currentLocation.theta)));
  while(abs2(adjustTheta(newTheta - currentLocation.theta)) > THETA_PRECISION) {
      if (odometry() > 0) return globalError;
      analogWrite(P_LEFT_MOTOR_EN, motorSpeed);
      analogWrite(P_RIGHT_MOTOR_EN, motorSpeed);
      
      forwardTheta = abs2(adjustTheta(currentLocation.theta - startTheta));
      remainingTheta = abs2(adjustTheta(newTheta - currentLocation.theta));
      // Escape conditions
      if (remainingTheta < umbrella) umbrella = remainingTheta; // Umbrella update
      //else if (newTheta - currentLocation.theta > umbrella + STRAY_ERROR_TH) {globalError = 5; return 5;} // Stray error
      // Will need to add useLines conditions
      //Serial.println(currentLocation.theta);
      
      
      // Accelleration Algorithm
      if (forwardTheta < halfwayTheta)
      {
        if (forwardTheta >= accelerationTheta)
          motorSpeed = MAX_SPEED;  //keep at max
        else
          motorSpeed = constrain(sqrt((forwardTheta*TURN_RADIUS)+ADDED_DISTANCE)*ACCELERATION_CONSTANT, MIN_SPEED, MAX_SPEED);
      }
      if (remainingTheta < halfwayTheta)
      {
        if (remainingTheta >= accelerationTheta)
          motorSpeed = MAX_SPEED;
        else
          motorSpeed = constrain(sqrt((remainingTheta*TURN_RADIUS)+ADDED_DISTANCE)*ACCELERATION_CONSTANT, MIN_SPEED, MAX_SPEED);
      }
      motorSpeed = 150;  // not Full steam ahead!
  }
  setMotorPosition(M_BRAKE);
  analogWrite(P_LEFT_MOTOR_EN, 255);
  analogWrite(P_RIGHT_MOTOR_EN, 255);
  return 0; // Success
}

int driveStraight(location target, boolean useLines) {
  long straightTime = millis();
  int motorSpeed = 0;
  start = currentLocation;
  double maxDist = dist(start, target); //total trip distance
  double umbrella = maxDist; // This is the closest we've been so far
  double halfwayDist = maxDist/2;  // The halfway point
  double remainingDist = maxDist;  // How much further we have left to gp
  double temp = MAX_SPEED/ACCELERATION_CONSTANT;
  double accelerationDist = temp*temp - ADDED_DISTANCE;
  double forwardDist = 0;
  if (remainingDist < TARGET_PRECISION) {setMotorPosition(M_BRAKE); return 0;}
  while(remainingDist < umbrella + UMBRELLA_ERROR) {
      if (odometry() > 0) return globalError;
      analogWrite(P_LEFT_MOTOR_EN, motorSpeed-PIDOutput);
      analogWrite(P_RIGHT_MOTOR_EN, motorSpeed+PIDOutput);
      
      // Escape conditions
      if (remainingDist < umbrella) umbrella = remainingDist; // Umbrella update
      if (millis() > straightTime + STRAIGHT_TIMEOUT) {globalError = 5; break;}
      // Will need to add useLines conditions
      
      
      // Accelleration Algorithm
      if (forwardDist < halfwayDist)
      {
        if (forwardDist >= accelerationDist)
          motorSpeed = MAX_SPEED;  //keep at max
        else
          motorSpeed = constrain(sqrt(forwardDist+ADDED_DISTANCE)*ACCELERATION_CONSTANT, MIN_SPEED, MAX_SPEED);
      }
      if (remainingDist < halfwayDist)
      {
        if (remainingDist >= accelerationDist)
          motorSpeed = MAX_SPEED;
        else
          motorSpeed = constrain(sqrt(remainingDist+ADDED_DISTANCE)*ACCELERATION_CONSTANT, MIN_SPEED, MAX_SPEED);
      }
  
        
      //motorSpeed = 150;  // not Full steam ahead!
      forwardDist = dist(start, currentLocation);
      remainingDist = dist(currentLocation, target);
      
      PIDInput = error(target, start, currentLocation);
      odomPID.Compute();
  }
  setMotorPosition(M_BRAKE);
  analogWrite(P_LEFT_MOTOR_EN, 255);
  analogWrite(P_RIGHT_MOTOR_EN, 255);
  
  return globalError; // Success
}

//positive error means you're too far to the right, neg means left
double error(location target, location start, location current) {
  return (((current.x-start.x)*(target.y-start.y))-((current.y-start.y)*(target.x-start.x)))/dist(start, target);
}

double dist(location a, location b) {
  return  sqrt(((b.y-a.y)*(b.y-a.y)) + ((b.x-a.x)*(b.x-a.x)));
}

double arcdist(double theta1, double theta2, double radius) {
  return (theta2 - theta1)*radius;
}
