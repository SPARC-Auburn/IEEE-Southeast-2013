/*
 * This file contains tools for controlling the motors.
 * It will set the motor control pins according to enumerated position.
 * i.e. if whichPosition == M_FORWARD then both motors will be set to forward.
 */

void setMotorPosition(int whichPosition) {
  switch (whichPosition) {
      case M_BRAKE:
          digitalWrite(P_RIGHT_MOTOR_L1, 0);
          digitalWrite(P_RIGHT_MOTOR_L2, 0);
          digitalWrite(P_LEFT_MOTOR_L1, 0);
          digitalWrite(P_LEFT_MOTOR_L2, 0);
          break;
      case M_FORWARD:
          digitalWrite(P_RIGHT_MOTOR_L1, 1);
          digitalWrite(P_RIGHT_MOTOR_L2, 0);
          digitalWrite(P_LEFT_MOTOR_L1, 1);
          digitalWrite(P_LEFT_MOTOR_L2, 0);
          break;
      case M_BACKWARD:
          digitalWrite(P_RIGHT_MOTOR_L1, 0);
          digitalWrite(P_RIGHT_MOTOR_L2, 1);
          digitalWrite(P_LEFT_MOTOR_L1, 0);
          digitalWrite(P_LEFT_MOTOR_L2, 1);
          break;
      case M_FORWARD_RIGHT:
          digitalWrite(P_RIGHT_MOTOR_L1, 0);
          digitalWrite(P_RIGHT_MOTOR_L2, 0);
          digitalWrite(P_LEFT_MOTOR_L1, 1);
          digitalWrite(P_LEFT_MOTOR_L2, 0);
          break;
      case M_FORWARD_LEFT:
          digitalWrite(P_RIGHT_MOTOR_L1, 1);
          digitalWrite(P_RIGHT_MOTOR_L2, 0);
          digitalWrite(P_LEFT_MOTOR_L1, 0);
          digitalWrite(P_LEFT_MOTOR_L2, 0);
          break;
      case M_PIVOT_RIGHT:
          digitalWrite(P_RIGHT_MOTOR_L1, 0);
          digitalWrite(P_RIGHT_MOTOR_L2, 1);
          digitalWrite(P_LEFT_MOTOR_L1, 1);
          digitalWrite(P_LEFT_MOTOR_L2, 0);
          break;
      case M_PIVOT_LEFT:
          digitalWrite(P_RIGHT_MOTOR_L1, 0);
          digitalWrite(P_RIGHT_MOTOR_L2, 1);
          digitalWrite(P_LEFT_MOTOR_L1, 1);
          digitalWrite(P_LEFT_MOTOR_L2, 0);
          break;
      case M_BACK_RIGHT:
          digitalWrite(P_RIGHT_MOTOR_L1, 0);
          digitalWrite(P_RIGHT_MOTOR_L2, 1);
          digitalWrite(P_LEFT_MOTOR_L1, 0);
          digitalWrite(P_LEFT_MOTOR_L2, 0);
          break;
      case M_BACK_LEFT:
          digitalWrite(P_RIGHT_MOTOR_L1, 0);
          digitalWrite(P_RIGHT_MOTOR_L2, 0);
          digitalWrite(P_LEFT_MOTOR_L1, 0);
          digitalWrite(P_LEFT_MOTOR_L2, 1);
          break;
  }
  return;
}
