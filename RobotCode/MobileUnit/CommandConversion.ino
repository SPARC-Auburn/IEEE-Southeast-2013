/*
 * This file contains command conversion function and all supporting functions.
 * Takes the following variables:
 *        byte commandStatus
 *        int commandEndAction
 *        int commandEndColor
 *        int commandEndLength
 *        location destination
 * And determines the following variables:
 *        int motorPath[3]
 *        boolean linesPath[3]
 *        location partOneDest
 *        location partTwoDest
 * The basic process is to have two single-wheel turns and one straight move.
 *        If destination is in front of current location, first move will be forward turn.
 *        If destination is behind current location, first move will be backward turn.
 * Exception: If destination is within turning diameter of current location,
 * use two pivots and one straight move.
 */
byte commandConversion() {
  motorPath[0] = M_FORWARD_RIGHT;
  motorPath[1] = M_FORWARD;
  motorPath[2] = M_FORWARD_LEFT;
  linesPath[0] = false;
  linesPath[1] = false;
  linesPath[2] = false;
  partOneDest.x = 10000;
  partOneDest.y = 10000;
  partOneDest.theta = 0;
  partTwoDest.x = 20000;
  partTwoDest.y = 20000;
  partTwoDest.theta = 0;
  return 0;
}
