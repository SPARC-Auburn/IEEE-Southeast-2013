/*
 * This file contains the endAction() function and all supporting functions.
 * Follows directions in these variables using claw motor.
 *   int commandEndAction;        // The end action of the current command (high 3 bits)
 *   int commandEndColor;         // The color block as reported from base station (middle 3 bits of end action byte)
 *   int commandEndLength;        // The length of block as reported from base station (low 2 bits of end action byte)
 * Returns any error encountered, or 0 for no error.
 */

int endAction() {
  switch (commandEndAction) {
    case EA_NONE:
    case EA_AIR_WAY:
      // Waypoint, no need to do anything
      return 0;
    case EA_PU_1_BLOCK:
      // Unimplemented action
      return 1;
    case EA_PU_2_BLOCK:
      // Unimplemented action
      return 1;
    case EA_DO_STACKED:
      // Unimplemented action
      return 1;
    case EA_DO_SINGLE:
      // Unimplemented action
      return 1;
    case EA_FINISHED:
      // Done forever
      // Do a dance
      while(true);
  }  
  return 32;
}
