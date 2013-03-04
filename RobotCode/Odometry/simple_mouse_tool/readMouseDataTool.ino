// This function adds mouse readings to given x and y integers
// It interfaces with mouse and accounts for negative flag.
void readMouseData(PS2 thisMouse, int *mouseX, int *mouseY) {
  int mouseStat, mouseXnew, mouseYnew;
  thisMouse.write(0xeb); // give data command
  thisMouse.read(); // ignore ack
  mouseStat = thisMouse.read();
  mouseXnew = thisMouse.read();
  mouseYnew = thisMouse.read();
  if (bitRead(mouseStat, 5) == 1) mouseYnew = -256 + mouseYnew;
  if (bitRead(mouseStat, 4) == 1) mouseXnew = -256 + mouseXnew;
  *mouseX = *mouseX + mouseXnew;
  *mouseY = *mouseY + mouseYnew;  
}
