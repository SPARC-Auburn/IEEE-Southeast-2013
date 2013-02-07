/*
 * This file will contain the driveTurn and driveStraight functions.
 *
 * The motors will already be set; these functions will only need to run
 * a delay loop.  Inside the loop must be adjustment routines,
 * including a call to odometry, motor calibration for traveling straight,
 * escape condition when either target has been reached or line detected,
 * and acceleration calculation adjustment.
 */

//Some method declarations:
double error(location target, location current);
double dist(location a, location b);
double arcdist(double theta1, double theta2, double radius);
 
int driveTurn(double newTheta, boolean useLines) {
  return 0;
}

int driveStraight(location target, boolean useLines) {
  return 0;
}

double error(location target, location start, location current) {
  return (((current.x-start.x)*(target.y-start.y))-((current.y-start.y)*(target.x-start.x)))/dist(start, target);
}

double dist(location a, location b) {
  return sqrt(((b.y-a.y)*(b.y-a.y)) - ((b.x-a.x)*(b.x-a.x)));
}

double arcdist(double theta1, double theta2, double radius) {
  return (theta2 - theta1)*radius;
}
