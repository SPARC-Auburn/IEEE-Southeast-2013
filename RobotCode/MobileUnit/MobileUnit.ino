/*
 * Auburn University Department of Electrical and Computer Engineering
 * Student Project and Research Committee (SPaRC)
 * MobileUnit Code for IEEE Secon 2013 Hardware Competition
 * 
 * Version: 2/12/2013
 */
 
// Libraries and Headers
#include "location.h"
#include <ps2.h>
#include <PinChangeInt.h>

// Constants
#define THETA_RESOLUTION   10000    // Multiply radians by this to get stored theta value
#define X_RESOLUTION         500    // Multiply inches by this to get stored x value
#define Y_RESOLUTION         500    // Multiply inches by this to get stored y value
#define COMM_TIMEOUT        2000    // Timeout listening for response
#define COMM_LONG_TIMEOUT  10000    // After this give up
#define HALF_WIDTH             5 
 
// Pin Definitions begin with P_
#define P_XBEE_IN   14
#define P_XBEE_OUT  15
#define P_LEFT_MOUSE_CLOCK 2
#define P_LEFT_MOUSE_DATA 3
#define P_RIGHT_MOUSE_CLOCK 4
#define P_RIGHT_MOUSE_DATA 5
#define P_RIGHT_MOTOR_L1 6
#define P_RIGHT_MOTOR_L2 7
#define P_RIGHT_MOTOR_EN 8
#define P_LEFT_MOTOR_L1 9
#define P_LEFT_MOTOR_L2 10
#define P_LEFT_MOTOR_EN 11
#define P_ENC_LEFT_A 18    //left wheel, channel A
#define P_ENC_LEFT_B 19    //etc.
#define P_ENC_RIGHT_A 20   //these "ENC" pins MUST
#define P_ENC_RIGHT_B 21   // BE INTERRUPT PINS!!!!

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

// Global Variable and Object Declarations
byte globalError;            // This will be reported by any function in loop to cancel the command and go straight to communication
location currentLocation;    // Where we are right now.  This can be updated by the odometry function.
location start;              // Where we are at the beginning of the block.
location destination;        // Our target position for this block.
int motorPath[3];            // The three motor positions of the moves, set by commandConversion and used by main loop.
boolean linesPath[3];        // The boolean values for whether to look for lines in the three moves, set by commandConversion.
location partOneDest;        // Where we are going for the first move.
location partTwoDest;        // Where we are going for the second move.
byte commandStatus;          // The flags as received from base station (or made up)
int commandEndAction;        // The end action of the current command (high 3 bits)
int commandEndColor;         // The color block as reported from base station (middle 3 bits of end action byte)
int commandEndLength;        // The length of block as reported from base station (low 2 bits of end action byte)

// Odometry-related Objects and Variables
PS2 leftMouse(P_LEFT_MOUSE_CLOCK, P_LEFT_MOUSE_DATA);
PS2 rightMouse(P_RIGHT_MOUSE_CLOCK, P_RIGHT_MOUSE_DATA);

// Method Declarations
void openHandshake();        // For the first communication until first command is determined.
byte commandConversion();    // Will convert command to three moves for the drive functions, returns global error
byte doublePivot();          // Daughter function of commandConversion
void setMotorPosition(int whichPosition);  // Just changes motor directions.
int driveTurn(double newTheta, boolean useLines);  // Return error
int driveStraight(location target, boolean useLines);  // Return error
boolean getBaseCommand();    // Communicates with base station and gets command, returns false if timeout with failed communication.
void getBackupCommand();     // Figures out best command from backup list.
int odometry();              // Runs the math to update currentLocation, returns global error (0 = success)
int endAction();             // Manages claw and color, length sensors to pick up or drop off blocks.
double error(location target, location current);
double dist(location a, location b);
double arcdist(double theta1, double theta2, double radius);

// Functions (math-related, not really methods)
byte commError(byte message[], int thisLength);  // Calculates error for communication.
double adjustTheta( double theta ); // !!! should probably go somewhere more universal
location relativeCoordinates(location origin, location absoluteTarget);
location absoluteCoordinates(location origin, location relativeTarget);

/*
 * Setup Function
 * This will assign pins as input/output.
 * Initializes global variables.
 * Sets up tools using appropriate functions
 * Then, calls opening handshake sequence.
 */ 
void setup() {
   // Only for debugging
   // Serial.begin(9600);
   
   // Assign pins
   Serial3.begin(9600);
   pinMode(P_RIGHT_MOTOR_L1, OUTPUT);  
   pinMode(P_RIGHT_MOTOR_L2, OUTPUT);
   pinMode(P_RIGHT_MOTOR_EN, OUTPUT);
   pinMode(P_LEFT_MOTOR_L1, OUTPUT);
   pinMode(P_LEFT_MOTOR_L2, OUTPUT);
   pinMode(P_LEFT_MOTOR_EN, OUTPUT);
   
   // Initialize global variables.

   
   // Setup Functions
   odometrySetup();
   
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
    if(driveTurn(partOneDest.theta, linesPath[0]) > 0) break;
    // Straight move
    setMotorPosition(motorPath[1]);
    if(driveStraight(partTwoDest, linesPath[1]) > 0) break;
    // Second turn
    setMotorPosition(motorPath[2]);
    if(driveTurn(destination.theta, linesPath[2]) > 0) break;
    // End action
    endAction();
  } while(false);
  
  // Communicate with base station and determine next move.  
  if (!getBaseCommand()) {
    getBackupCommand();
  }
  
  /* 
  //Debug functions
  commTest();
  Serial.println("WAITING");
  while(Serial.available()){Serial.read();}
  while(!Serial.available()){}
  while(Serial.available()){Serial.read();}
  Serial.println("GO!");
  */
}
