// This file contains the odometry() function and all supporting functions
// The only output required by odometry is:
//              1) Update currentLocation
//              2) Set globalError and return an error if there is a problem.
//

int odometrySetup() {
  encSetup();
  // Other forms of odometry...
  return 0; // "I never have errors!"
}

int odometry() {
  encSetLocation( currentLocation );
  encCalc();
  currentLocation = encGetLocation();
  // Other forms of odometry...
  return 0; // "No errors here, bro!"
}

// Run this to throw away all odometry information
void odometryClear() {
  encClearReg();
}
