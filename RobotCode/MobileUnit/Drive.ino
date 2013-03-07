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
#define UMBRELLA_THETA   .03 // If we get this much farther form target than we were before, return an error
#define STRAIGHT_TIMEOUT 20000 // No moves for longer than 20 seconds
#define TURN_TIMEOUT     15000

#define MIN_SPEED 60
#define MAX_SPEED 195
#define ADDED_DISTANCE  0.3 //in inches, the amount to add to the forward distance to have the effect of adding some initial velocity
#define ADDED_DISTANCE_REV  0
#define ACCELERATION_CONSTANT 51.4 //really, the sqrt of the acceleration
      //  = 51.4  corresponds to an accelleration of 0 to full speed (230) in about 20 inches
      //  = 59.4  corresponds to an accelleration of 0 to full speed (230) in about 15 inches
      //  = 72.7  corresponds to an accelleration of 0 to full speed (230) in about 10 inches
#define DECELERATION_CONSTANT 72.7
      //  = 46.0 means 0 to 230 in 25 inches
      //  = 42.0 means 0 to 230 in 30 inches
#define TURN_RADIUS 9.25

//calculate some stuff ahead of time
const double ACC_SQ_RATIO = (DECELERATION_CONSTANT / ACCELERATION_CONSTANT) * (DECELERATION_CONSTANT / ACCELERATION_CONSTANT);
const double FWD_TO_TOTAL_RATIO = ACC_SQ_RATIO / (1 + ACC_SQ_RATIO);
const double SPD_ACC_RATIO = MAX_SPEED/ACCELERATION_CONSTANT;
const double ACC_DIST = (SPD_ACC_RATIO*SPD_ACC_RATIO) - ADDED_DISTANCE;
const double ACC_THETA = ACC_DIST / TURN_RADIUS;
const double SPD_DEC_RATIO = MAX_SPEED/DECELERATION_CONSTANT;
const double DEC_DIST = (SPD_DEC_RATIO*SPD_DEC_RATIO) - ADDED_DISTANCE_REV;
const double DEC_THETA = DEC_DIST / TURN_RADIUS;
const int ACCEL_ARRAY[21] = {65, 68, 80, 91, 100, 109, 117, 124, 131, 138, 144, 151, 156, 162, 168, 173, 178, 183, 188, 193, 195};
const int DECEL_ARRAY[21] = {195, 195, 195, 180, 160, 138, 122, 108, 96, 86, 77, 69, 65, 65, 65, 65, 65, 65, 65, 65, 65};
//const int DECEL_ARRAY[21] = {195, 140, 110, 90, 75, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65, 65};
//const int ACCEL_ARRAY[21] = {80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80,80, 80, 80, 80,80, 80, 80, 80,80};
//const int DECEL_ARRAY[21] = {80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80,80};

double abs2( double blah ) { double res = abs(blah); return res; }

int driveTurn(double newTheta, boolean useLines) {
  ebrakeOff();
  long turnTime = millis();
  int motorSpeed = 0;
  const double maxTheta = newTheta - currentLocation.theta;
  double umbrella = abs(maxTheta); // This is the closest we've been so far
  const double halfwayThetaF = maxTheta * FWD_TO_TOTAL_RATIO; // NOTE: halway isn't really half the distance,
                // it's actually the point at which the acceleration and deceleration curves meet.
  const double halfwayThetaR = maxTheta - halfwayThetaR;
  double startTheta = currentLocation.theta;
  double forwardTheta = 0;
  double remainingTheta = maxTheta;
  //Serial.println(adjustTheta(newTheta - currentLocation.theta));
  //Serial.println(abs2(adjustTheta(newTheta - currentLocation.theta)));
  while(abs2(adjustTheta(newTheta - currentLocation.theta)) > THETA_PRECISION) {
      if (odometry() > 0) return globalError;
      analogWrite(P_LEFT_MOTOR_EN, motorSpeed);
      analogWrite(P_RIGHT_MOTOR_EN, motorSpeed);
      
      forwardTheta = abs2(adjustTheta(currentLocation.theta - startTheta));
      remainingTheta = abs2(adjustTheta(newTheta - currentLocation.theta));
      // Escape conditions
      if (abs(remainingTheta) < umbrella) umbrella = abs(remainingTheta); // Umbrella update
      else if (abs(remainingTheta) > umbrella + UMBRELLA_THETA) {break;}
      if (millis() > turnTime + TURN_TIMEOUT) {globalError = 5; break;}
      // Will need to add useLines conditions
      //Serial.println(currentLocation.theta);
      
      // Accelleration Algorithm
      if (forwardTheta < halfwayThetaF)
      {
        if (forwardTheta >= ACC_THETA)
          motorSpeed = MAX_SPEED;  //keep at max
        else
          motorSpeed = constrain(sqrt((forwardTheta*TURN_RADIUS)+ADDED_DISTANCE)*ACCELERATION_CONSTANT, MIN_SPEED, MAX_SPEED);
      }
      if (remainingTheta < halfwayThetaR)
      {
        if (remainingTheta >= DEC_THETA)
          motorSpeed = MAX_SPEED;
        else
          motorSpeed = constrain(sqrt((remainingTheta*TURN_RADIUS)+ADDED_DISTANCE_REV)*DECELERATION_CONSTANT, MIN_SPEED, MAX_SPEED);
      }
      motorSpeed = 65;  // not Full steam ahead!
  }
  setMotorPosition(M_BRAKE);
  analogWrite(P_LEFT_MOTOR_EN, 255);
  analogWrite(P_RIGHT_MOTOR_EN, 255);
  delay(100); // Brake, then set output to zero
  analogWrite(P_LEFT_MOTOR_EN, 0);
  analogWrite(P_RIGHT_MOTOR_EN, 0);
  if (odometry() > 0) return globalError;
  return 0; // Success
}

int driveStraight(location target, boolean useLines) {
  //odomArrayIndex = 0;
  long straightTime = millis();
  int motorSpeed = 0;
  start = currentLocation;
  const double maxDist = dist(start, target); //total trip distance
  double umbrella = maxDist; // This is the closest we've been so far
  const double halfwayDistF = maxDist * FWD_TO_TOTAL_RATIO;  // NOTE: halway isn't really half the distance,
                // it's actually the point at which the acceleration and deceleration curves meet.
  const double halfwayDistR = maxDist - halfwayDistF;
  double remainingDist = maxDist;  // How much further we have left to go
  double forwardDist = 0;
  if (remainingDist < TARGET_PRECISION) {setMotorPosition(M_BRAKE); return 0;}
  int pidCounter = 0;
  int backwardCorrection = 1;
  if (motorPath[1] == M_BACKWARD) backwardCorrection = -1;
  while(remainingDist < umbrella + UMBRELLA_ERROR) {
      //odomArrayIndex++;
      if (odometry() > 0) return globalError;
      analogWrite(P_LEFT_MOTOR_EN, motorSpeed+PIDOutput * constrain(1-1/remainingDist, 0, 100)*backwardCorrection); // Added two correction factors, one for a backward move and the other to avoid last second quick adjustments
      analogWrite(P_RIGHT_MOTOR_EN, motorSpeed-PIDOutput * constrain(1-1/remainingDist, 0, 100)*backwardCorrection);
      
      // Escape conditions
      if (remainingDist < umbrella) umbrella = remainingDist; // Umbrella update
      if (millis() > straightTime + STRAIGHT_TIMEOUT) {globalError = 5; break;}
      // Will need to add useLines conditions
      
      
      // Accelleration Algorithm
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
        
      //motorSpeed = 150;  // not Full steam ahead!
      forwardDist = dist(start, currentLocation);
      remainingDist = dist(currentLocation, target);
      
      PIDInput = error(target, start, currentLocation);
      odomPID.Compute();
  }
  setMotorPosition(M_BRAKE);
  analogWrite(P_LEFT_MOTOR_EN, 255);
  analogWrite(P_RIGHT_MOTOR_EN, 255);
  ebrakeOn();
  delay(100); // Brake, then set output to zero
  analogWrite(P_LEFT_MOTOR_EN, 0);
  analogWrite(P_RIGHT_MOTOR_EN, 0);
  if (odometry() > 0) return globalError;
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

void ebrakeOn()
{
  pinMode(P_EBRAKE, OUTPUT);
  analogWrite(P_EBRAKE, 30);
  delay(400);
}

void ebrakeOff()
{
  analogWrite(P_EBRAKE, 200);
 // delay(100);
 // pinMode(P_EBRAKE, INPUT);
}
