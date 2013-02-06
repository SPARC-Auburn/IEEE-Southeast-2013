/*
 * This file will contain the driveTurn and driveStraight functions.
 */

//Some method declarations:
double error(location target, location current);
double dist(location a, location b);
 
int driveTurn(double newTheta, boolean useLines) {
  return 0;
}

int driveStraight(location target, boolean useLines) {
  return 0;
}

double error(location target, location start, location current) {
  return (((current.x-start.x)*(target.y-start.y))-((current.y-start.y)*(target.x-start)))/dist(start, target);
}

double dist(location a, location b) {
  return sqrt(((b.y-a.y)*(b.y-a.y)) - ((b.x-a.x)*(b.x-a.x)));
}

double arcdist(double theta1, double theta2, double radius) {
  return (theta2 - theta1)*radius;
}