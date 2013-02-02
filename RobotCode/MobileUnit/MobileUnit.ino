/*
 * Auburn University Department of Electrical and Computer Engineering
 * Student Project and Research Committee (SPaRC)
 * MobileUnit Code for IEEE Secon 2013 Hardware Competition
 * 
 * Version: 2/1/2013
 */
 
// Libraries and Headers
#include "location.h"

// Constants
#define THETA_RESOLUTION   10000    // Multiply radians by this to get stored theta value
#define X_RESOLUTION         500    // Multiply inches by this to get stored x value
#define Y_RESOLUTION         500    // Multiply inches by this to get stored y value

// Pin Definitions begin with P_
#define P_XBEE_IN   14
#define P_XBEE_OUT  15

// Motor Logical States begin with M_
#define M_BRAKE            0
#define M_FORWARD          1
#define M_BACKWARD         2
#define M_FORWARD_RIGHT    3
#define M_PIVOT_RIGHT      4
#define M_BACK_RIGHT       5
#define M_FORWARD_LEFT     6
#define M_PIVOT_LEFT       7
#define M_BACK_LEFT        8

// Global Variable Declarations
byte globalError;            // This will be reported by any function in loop to cancel the command and go straight to communication
location currentLocation;    // Where we are right now.  This can be updated by the odometry function.
location start;              // Where we are at the beginning of the block.
location destination;        // Our target position for this block.
int motorPath[3];            // The three motor positions of the moves, set by commandConversion and used by main loop.
boolean linesPath[3];        // The boolean values for whether to look for lines in the three moves, set by commandConversion.
location partOneDest;        // Where we are going for the first move.
location partTwoDest;        // Where we are going for the second move.

// Method Declarations
void openHandshake();        // For the first communication until first command is determined.
byte commandConversion();    // Will convert command to three moves for the drive functions, returns global error
void setMotorPosition(int whichPosition);  // Just changes motor directions.
int driveTurn(double newTheta, boolean useLines);  // Return error
int driveStraight(location target, boolean useLines);  // Return error
boolean getBaseCommand();    // Communicates with base station and gets command, returns false if timeout with failed communication.
void getBackupCommand();     // Figures out best command from backup list.
int odometry();              // Runs the math to update currentLocation, returns global error (0 = success)
int endAction();             // Manages claw and color, length sensors to pick up or drop off blocks.

/*
 * Setup Function
 * This will assign pins as input/output.
 * Initializes global variables.
 * Then, calls opening handshake sequence.
 */ 
void setup() {
   // Assign pins
   
   
   // Initialize global variables.
   
   
   // Call opening handshake sequence
   openHandshake();
}

/*
 * Main Loop function
 * Calls functions to:
 *  1) Interpret command in terms of three moves.
 *  2) Make the first turn.
 *  3) Make the straight move.
 *  4) Make the second turn.
 *  5) Peform the end action.
 *  6) Communicate with base station to determine next command.
 * Will be able to handle errors, including accessing backup
 * command in case commmunication fails, and report to base station.
 */
void loop() {
  
  globalError = 0;
  
  // The first time this runs, the first command will already be set.
  
  do {  // This is only run once but is used so break command will work.  
    // Command conversion
    if (commandConversion() > 0) break;
    // First turn
    setMotorPosition(motorPath[0]);
    driveTurn(partOneDest.theta, linesPath[0]);
    // Straight move
    setMotorPosition(motorPath[1]);
    driveStraight(partTwoDest, linesPath[1]);
    // Second turn
    setMotorPosition(motorPath[2]);
    driveTurn(destination.theta, linesPath[2]);
    // End action
    endAction();
  } while(false);
  
  // Communicate with base station and determine next move.  
  if (!getBaseCommand()) {
    getBackupCommand();
  }
}