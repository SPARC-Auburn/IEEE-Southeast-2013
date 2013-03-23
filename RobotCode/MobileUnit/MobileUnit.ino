
/*
 * Auburn University Department of Electrical and Computer Engineering
 * Student Project and Research Committee (SPaRC)
 * MobileUnit Code for IEEE Secon 2013 Hardware Competition
 * 
 * Version: 3/7/2013
 *
 * To debug: Go to first lines of loop() and uncomment rcTest() or debugging(),
 * and change prompt() in debugging_loop to step through program.
 */
 
// Libraries and Headers
#include "location.h"
//#include <ps2.h> // This would have been used for the mice.
#include <PinChangeInt.h>
#include <PID_v1.h>

// Parameters
#define THETA_RESOLUTION   10000    // Multiply radians by this to get stored theta value
#define X_RESOLUTION         500    // Multiply inches by this to get stored x value
#define Y_RESOLUTION         500    // Multiply inches by this to get stored y value
#define COMM_TIMEOUT         500    // Timeout listening for response
#define COMM_LONG_TIMEOUT  20000    // After this give up
#define SPECIAL_MOVE_DISTANCE 10    // Goes this many inches backward when sent special move command
#define TARGET_PRECISION      .1    // If < this distance from target, automatic success
#define UMBRELLA_ERROR         1    // If we get this much farther from target than we were before, return an error.
#define THETA_PRECISION      .03    // If < this angle from target, automatic success
#define UMBRELLA_THETA       .03    // If we get this much farther form target than we were before, return an error.
#define STRAIGHT_TIMEOUT   20000    // No more than this many milliseconds spent moving straight
#define TURN_TIMEOUT       15000    // No more than this many milliseconds spent turning
#define MIN_SPEED             60    // PWM minimum, except for PID
#define FW_CONST_SPEED_R      80    // This will be constant speed for straight move
#define FW_CONST_SPEED_L      62    // This will be constant speed for straight move
#define MAX_SPEED            195    // PWM maximum, except for PID
#define ADDED_DISTANCE       0.3    // in inches, the amount to add to the forward distance to have the effect of adding some initial velocity
#define ADDED_DISTANCE_REV     0
#define ACCELERATION_CONSTANT 51.4  // 51.4  corresponds to 0 to full speed (230) in about 20 inches, 59.4 in 15 inches, 72.7 in 10 inches
#define DECELERATION_CONSTANT 72.7  // 46.0 means 0 to 230 in 25 inches, 42.0 means 0 to 230 in 30 inches
#define DIAM                 1.9    // diameter in inches.
#define WIDTH              9.187    // distance between wheels in inches
#define HALF_WIDTH     (WIDTH/2)    // Patrick, if you read this, this isn't my fault
#define RESOLUTION            64    // encoder resolution
#define RATIO              18.75    // gearbox ratio
//#define MAGIC_SCALE_FACTOR   0.005235987756 // = pi * DIAM / (RESOLUTION * RATIO),  uses D = 2.0
#define MAGIC_SCALE_FACTOR .0049741883681838 // = pi * DIAM / (RESOLUTION * RATIO),  uses D = 1.9
#define TURN_SPEED_RIGHT      80    // When turning, this will be the speed
#define TURN_SPEED_LEFT       62    // When turning, this will be the speed
#define GREETING_TIMEOUT    3000
#define HANDSHAKE_BACK_TIME 2500
#define HANDSHAKE_TURN_TIME 2000
#define HS_BACK_SPEED_LEFT    67
#define HS_BACK_SPEED_RIGHT   80
#define LINE_BOUNDARY 500    // Percent that marks boundary
#define LINE_TIMEOUT 100000  // Micros timeout
#define LINE_CALIB_LOW 0     // Low calibration indicator
#define LINE_CALIB_HIGH 1000 // High calibration indicator

// Pin Definitions begin with P_
#define P_XBEE_IN          14
#define P_XBEE_OUT         15
//#define P_LEFT_MOUSE_CLOCK 52  // These were for mice
//#define P_LEFT_MOUSE_DATA  53  // These were for mice
//#define P_RIGHT_MOUSE_CLOCK 54 // These were for mice
//#define P_RIGHT_MOUSE_DATA 55  // These were for mice
#define P_RIGHT_MOTOR_L1   12
#define P_RIGHT_MOTOR_L2   11
#define P_RIGHT_MOTOR_EN   13  //should be PWM
#define P_LEFT_MOTOR_L1     8
#define P_LEFT_MOTOR_L2     9 
#define P_LEFT_MOTOR_EN    10 //should be PWM
#define P_ENC_LEFT_A       18 // Encoders
#define P_ENC_LEFT_B       19 // Encoders
#define P_ENC_RIGHT_A      20 // Encoders
#define P_ENC_RIGHT_B      21 // Encoders
#define P_LINE_FRONT_1     38
#define P_LINE_FRONT_2     40
#define P_LINE_FRONT_3     42
#define P_LINE_FRONT_4     44
#define P_LINE_FRONT_5     46
#define P_LINE_FRONT_6     48
#define P_LINE_FRONT_7     50
#define P_LINE_FRONT_8     52
#define P_LINE_BACK_L      37
#define P_LINE_BACK_R      39
#define P_LINE_EN          41

// Enumerations
enum Motor_State {
     M_BRAKE, M_FORWARD, M_BACKWARD, 
     M_FORWARD_RIGHT, M_SPIN_RIGHT, M_BACK_RIGHT, 
     M_FORWARD_LEFT, M_SPIN_LEFT, M_BACK_LEFT, M_CORRECT_ME  // Correct Me means function correctTurn() needs to be called to change to either spin left or right
};
enum Command_Status {
     CS_SPIN_BEGINNING = 6, CS_SPIN_END = 5, 
     CS_GO_UP_RAMP = 4, CS_ON_RAMP = 3, CS_EXPECT_LINE = 2, 
     CS_USE_OWN_CURLOC = 1, CS_SPECIAL = 0
};
enum End_action {
     EA_NONE, EA_PU_1_BLOCK, EA_PU_2_BLOCK, 
     EA_DO_STACKED, EA_DO_SINGLE, EA_AIR_WAY, EA_FINISHED
};
enum End_color {
     EC_NONE, EC_YELLOW, EC_ORANGE, EC_BROWN, 
     EC_GREEN, EC_RED, EC_BLUE
};

// Global Variable and Object Declarations used for ordinary operation
byte globalError;            // This will be reported by any function in loop to cancel the command and go straight to communication
location currentLocation;    // Where we are right now.  This can be updated by the odometry function.
location start;              // Where we are at the beginning of the command.
location destination;        // Our target position for this command.
int motorPath[3];            // The three motor positions of the moves, set by commandConversion and used by main loop.
boolean linesPath[3];        // The boolean values for whether to look for lines in the three moves, set by commandConversion.
location partOneDest;        // Where we are going for the first move.
location partTwoDest;        // Where we are going for the second move.
byte receivedMessage[16];    // Last message received by Communications
byte reportMessage[14];      // Last message sent by Communications
byte commandStatus;          // The flags as received from base station (or made up)
End_action commandEndAction; // The end action of the current command (high 3 bits)
int commandEndColor;         // The color block as reported from base station (middle 3 bits of end action byte)
int commandEndLength;        // The length of block as reported from base station (low 2 bits of end action byte)
double PIDSetpoint, PIDInput, PIDOutput;
PID odomPID(&PIDInput, &PIDOutput, &PIDSetpoint, 3, 2, 15, DIRECT); //
int lineSensorValues[10];     // 1 for line detected, 0 for no line detected

// Debug-related Global Variables
int debugIntData[2][500];    // For storing info for debugging purposes
double debugDoubleData[2][500];  // For storing info for debugging purposes
int dataIndex;               // For storing info for debugging purposes
int commTimesSent, commPacketsReceived; // For debugging

// Method Declarations
void getBackupCommand();     // Figures out best command from backup list.
byte commandConversion();    // Will convert command to three moves for the drive functions, returns global error
byte doubleSpin();           // Daughter function of commandConversion
byte calcWaypoint(location A, location B, signed char& dir); // Daughter of commandConversion, may need to add some flags
void correctTurn(int whichSegment);  // Sets motorPath variable saved as M_CORRECT_ME to either spin left or right
void setMotorPosition(int whichPosition);  // Just changes motor directions.
int driveTurn(double newTheta, boolean useLines);  // Return error
int driveStraight(location target, boolean useLines);  // Return error
boolean getBaseCommand();    // Communicates with base station and gets command, returns false if timeout with failed communication.
int odometry();              // Runs the math to update currentLocation, returns global error (0 = success)
int endAction();             // Manages claw and color, length sensors to pick up or drop off blocks.
void openHandshake();        // For the first communication until first command is determined.
double error(location target, location current);
double dist(location a, location b);
double arcdist(double theta1, double theta2, double radius);
void debugging();
void rcTest();

// Functions (math-related, not really methods)
double adjustTheta( double theta );
location relativeCoordinates(location origin, location absoluteTarget);
location absoluteCoordinates(location origin, location relativeTarget);
byte commError(byte message[], int thisLength);  // Calculates error for communication.
double abs2( double blah ) { double res = abs(blah); return res; } // This is actually the function itself LOL

/*
 * Setup Function
 * This will assign pins as input/output.
 * Initializes global variables.
 * Sets up tools using appropriate functions
 * Then, calls opening handshake sequence.
 */ 
void setup() {
   // Only for debugging
   Serial.begin(9600);
   
   // Assign pins
   Serial3.begin(9600);  // Communication with base station
   setMotorPosition(M_BRAKE);
   pinMode(P_RIGHT_MOTOR_L1, OUTPUT);  
   pinMode(P_RIGHT_MOTOR_L2, OUTPUT);
   pinMode(P_RIGHT_MOTOR_EN, OUTPUT);
   pinMode(P_LEFT_MOTOR_L1, OUTPUT);
   pinMode(P_LEFT_MOTOR_L2, OUTPUT);
   pinMode(P_LEFT_MOTOR_EN, OUTPUT);
   pinMode(P_LINE_EN, OUTPUT);
   
   // Initialize global variables.
   PIDSetpoint = 0;
   
   // Setup Functions
   setMotorPosition(M_BRAKE);
   odometrySetup();
   odomPID.SetOutputLimits(-60, 60);
   odomPID.SetMode(AUTOMATIC);
   odomPID.SetSampleTime(50);
   digitalWrite(P_LINE_EN, HIGH);   
  
   rcTest();       // Uncomment to enter RC mode on startup
  
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
  debugging();    // Uncomment to use Debug mode, this is an infinite loop that cannot be escaped
  
  // Communicate with base station and determine next move.  
  if (!getBaseCommand()) {
    
    getBackupCommand();
  
  }
  
  odometryClear();  // Avoid any weird odometry problems when receiving a new location from base station.
  
  globalError = 0;
  
  // The first time this runs, the first command will already be set.
  
  do {  // This is only run once but do...while is used so break command will work.  
    
    // Command conversion
    if (commandConversion() > 0) break;
    
    // First turn
    correctTurn(0);
    setMotorPosition(motorPath[0]);
    if(driveTurn(partOneDest.theta, linesPath[0]) > 0) break;
    
    // Straight move
    setMotorPosition(motorPath[1]);
    if(driveStraight(partTwoDest, linesPath[1]) > 0) break;
    
    // Second turn
    correctTurn(2);
    setMotorPosition(motorPath[2]);
    if(driveTurn(destination.theta, linesPath[2]) > 0) break;
    setMotorPosition(M_BRAKE);
    
    // End action
    globalError = endAction();
    
  } while(false);
}
