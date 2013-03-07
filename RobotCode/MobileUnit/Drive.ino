/*
 * This file will contain the driveTurn and driveStraight functions.
 *
 * The motors will already be set; these functions will only need to run
 * a delay loop.  Inside the loop must be adjustment routines,
 * including a call to odometry, motor calibration for traveling straight,
 * escape condition when either target has been reached or line detected,
 * and acceleration calculation adjustment.
 */

//calculate some stuff ahead of time
const double ACC_SQ_RATIO = (DECELERATION_CONSTANT / ACCELERATION_CONSTANT) * (DECELERATION_CONSTANT / ACCELERATION_CONSTANT);
const double FWD_TO_TOTAL_RATIO = ACC_SQ_RATIO / (1 + ACC_SQ_RATIO);
const double SPD_ACC_RATIO = MAX_SPEED/ACCELERATION_CONSTANT;
const double ACC_DIST = (SPD_ACC_RATIO*SPD_ACC_RATIO) - ADDED_DISTANCE;
const double ACC_THETA = ACC_DIST / WIDTH;
const double SPD_DEC_RATIO = MAX_SPEED/DECELERATION_CONSTANT;
const double DEC_DIST = (SPD_DEC_RATIO*SPD_DEC_RATIO) - ADDED_DISTANCE_REV;
const double DEC_THETA = DEC_DIST / WIDTH;
const int ACCEL_ARRAY[21] = {65, 68, 80, 91, 100, 109, 117, 124, 131, 138, 144, 151, 156, 162, 168, 173, 178, 183, 188, 193, 195};
//const int ACCEL_ARRAY[21] = {80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80,80};
const int DECEL_ARRAY[21] = {195, 195, 195, 180, 160, 138, 122, 108, 96, 86, 77, 69, 65, 65, 65, 65, 65, 65, 65, 65, 65};
//const int DECEL_ARRAY[21] = {195, 140, 110, 90, 75, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65};
//const int DECEL_ARRAY[21] = {80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80,80};

// What to do for a turn
int driveTurn(double newTheta, boolean useLines) {
  
  long turnTime = millis();  // Used to monitor timeout
  int motorSpeed = 0;
  
  // These are various reference angles
  const double maxTheta = newTheta - currentLocation.theta; // Analagous to distance we will need to travel, signed, remains constant
  double umbrella = abs(maxTheta); // This is the closest we've been so far, will change dynamically as we get closer
  const double halfwayThetaF = maxTheta * FWD_TO_TOTAL_RATIO; // NOTE: halfway isn't really half the distance,
  const double halfwayThetaR = maxTheta - halfwayThetaR;      // it's actually the point at which the acceleration and deceleration curves meet.
  double startTheta = currentLocation.theta; // Constant beginning point
  double forwardTheta = 0; // Dynamic forward progress, how far we've moved from beginning
  double remainingTheta = maxTheta; // Dynamic ground left to cover, how far we are from the end
  
  // Move until arriving within THETA_PRECISION of angle
  while(abs2(adjustTheta(newTheta - currentLocation.theta)) > THETA_PRECISION) {
      
      // Update Odometry
      if (odometry() > 0) return globalError;
      
      // Update Motor Speeds
      analogWrite(P_LEFT_MOTOR_EN, TURN_SPEED_LEFT);
      analogWrite(P_RIGHT_MOTOR_EN, TURN_SPEED_RIGHT);
      
      // Update dynamic reference angles
      forwardTheta = abs2(adjustTheta(currentLocation.theta - startTheta));
      remainingTheta = abs2(adjustTheta(newTheta - currentLocation.theta));
      if (abs(remainingTheta) < umbrella) umbrella = abs(remainingTheta); // Umbrella update
      
      // Escape conditions
      if (abs(remainingTheta) > umbrella + UMBRELLA_THETA) break; // Umbrella escape
      if (millis() > turnTime + TURN_TIMEOUT) {globalError = 5; break;} // Timeout escape
      // Will need to add useLines conditions
      
      // Accelleration Algorithm (not currently used)
      if (forwardTheta < halfwayThetaF)
      {
        if (forwardTheta >= ACC_THETA)
          motorSpeed = MAX_SPEED;  //keep at max
        else
          motorSpeed = constrain(sqrt((forwardTheta*WIDTH)+ADDED_DISTANCE)*ACCELERATION_CONSTANT, MIN_SPEED, MAX_SPEED);
      }
      if (remainingTheta < halfwayThetaR)
      {
        if (remainingTheta >= DEC_THETA)
          motorSpeed = MAX_SPEED;
        else
          motorSpeed = constrain(sqrt((remainingTheta*WIDTH)+ADDED_DISTANCE_REV)*DECELERATION_CONSTANT, MIN_SPEED, MAX_SPEED);
      }
  }
  
  // Braking sequence
  setMotorPosition(M_BRAKE);
  analogWrite(P_LEFT_MOTOR_EN, 255);
  analogWrite(P_RIGHT_MOTOR_EN, 255);
  delay(100); 
  
  // Finished braking, set output to zero
  analogWrite(P_LEFT_MOTOR_EN, 0);
  analogWrite(P_RIGHT_MOTOR_EN, 0);
  
  // Check odometry one last time
  if (odometry() > 0) return globalError;
  
  // Success
  return 0;
}

int driveStraight(location target, boolean useLines) {
  
  long straightTime = millis(); // Used to monitor timeout
  int motorSpeed = 0;
  
  // Distance references
  start = currentLocation; // Constant start location
  const double maxDist = dist(start, target); // total trip distance, constant
  double umbrella = maxDist; // This is the closest we've been so far, dynamic
  const double halfwayDistF = maxDist * FWD_TO_TOTAL_RATIO;  // NOTE: halway isn't really half the distance,
  const double halfwayDistR = maxDist - halfwayDistF; // it's actually the point at which the acceleration and deceleration curves meet.
  double remainingDist = maxDist;  // How much further we have left to go, dynamic
  double forwardDist = 0; // How far we've gone from start, dynamic
  
  // If we're already there, no reason to move
  if (remainingDist < TARGET_PRECISION) {setMotorPosition(M_BRAKE); return 0;}
  
  // Pid Setup
  int pidCounter = 0;
  
  // Check to see if we're traveling backward
  int backwardCorrection = 1;
  if (motorPath[1] == M_BACKWARD) backwardCorrection = -1;
  
  // Umbrella is primary escape condition
  while(remainingDist < umbrella + UMBRELLA_ERROR) {
    
      // Update Odometry
      if (odometry() > 0) return globalError;
      
      // Update motor Speed
      analogWrite(P_LEFT_MOTOR_EN, motorSpeed+PIDOutput * constrain(1-1/remainingDist, 0, 100)*backwardCorrection); // Added two correction factors, one for a backward move and the other to avoid last second quick adjustments
      analogWrite(P_RIGHT_MOTOR_EN, motorSpeed-PIDOutput * constrain(1-1/remainingDist, 0, 100)*backwardCorrection);
      
      // Dynamic variable update
      if (remainingDist < umbrella) umbrella = remainingDist; // Umbrella update
      forwardDist = dist(start, currentLocation);
      remainingDist = dist(currentLocation, target);
      
      // Escape conditions
      if (millis() > straightTime + STRAIGHT_TIMEOUT) {globalError = 5; break;}
      // Will need to add useLines conditions
            
      // Accelleration Algorithm (calculation version)
      /*
      if (forwardDist < halfwayDistF)
      {
        if (forwardDist >= ACC_DIST)
          motorSpeed = MAX_SPEED;  //keep at max
        else
          motorSpeed = constrain(sqrt(forwardDist+ADDED_DISTANCE)*ACCELERATION_CONSTANT, MIN_SPEED, MAX_SPEED);
      }
      if (remainingDist < halfwayDistR)
      {
        if (remainingDist >= DEC_DIST)
          motorSpeed = MAX_SPEED;
        else
          motorSpeed = constrain(sqrt(remainingDist+ADDED_DISTANCE_REV)*DECELERATION_CONSTANT, MIN_SPEED, MAX_SPEED);
      }
      */
      
      // Acceleration Algorithm (array version)
      if (forwardDist > 10 && remainingDist > 10) {
        motorSpeed = MAX_SPEED;
      }
      else if (remainingDist > 10) {
        motorSpeed = ACCEL_ARRAY[(int)forwardDist * 2];
      }
      else if (forwardDist > 10) {
        motorSpeed = DECEL_ARRAY[21-(int)remainingDist * 2];
      }
      else if (ACCEL_ARRAY[(int)forwardDist * 2] < DECEL_ARRAY[21-(int)remainingDist * 2]) {
        motorSpeed = ACCEL_ARRAY[(int)forwardDist * 2];
      }
      else {
        motorSpeed = DECEL_ARRAY[21-(int)remainingDist * 2] + 15;
      }
      
      // Acceleration Algorithm (constant version)
      //motorSpeed = 150;
      
      // PID update
      PIDInput = error(target, start, currentLocation);
      odomPID.Compute();
  }
  
  // Brake sequence
  setMotorPosition(M_BRAKE);
  analogWrite(P_LEFT_MOTOR_EN, 255);
  analogWrite(P_RIGHT_MOTOR_EN, 255);
  delay(100); 
  
  // Finished breaking, set output to zero
  analogWrite(P_LEFT_MOTOR_EN, 0);
  analogWrite(P_RIGHT_MOTOR_EN, 0);
  
  // Check odometry one last time
  if (odometry() > 0) return globalError;
  
  // Finished
  return globalError;
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
