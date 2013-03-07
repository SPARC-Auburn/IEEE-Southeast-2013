import serial
from struct import *
import time
global lastmessage
global lastmessagelength
lastmessage = ''
lastmessagelength = 0

def main():
	thistest = mobilecommtest()
	thistest.main()
####

class mobilecommtest(object):
	
	def __init__(self):
		self.lastmessage = ''
		self.lastmessagelength = 0
		self.lastreportreceived = {}
		self.lastx = 0
		self.lasty = 0
		self.lasttheta = 0.0
	####
		
	def monitorReceived(this, s, packFile, thisDelay):
		if (thisDelay == 0):
			thisDelay = input("How long would you like to monitor? >> ")
		####
		thisTime = time.clock()
		newpacket = 0
		lastPacket = time.clock() + 10000
		packFile.write("\nReceived:\n")
		packetarray = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		while (time.clock() < thisTime + thisDelay):
			if (s.inWaiting() != 0) :
				thisInput = s.read()
				packFile.write(str(unpack('B', thisInput)[0]))
				packFile.write(", ")
				print(str(unpack('B', thisInput)[0])),
				packetarray[newpacket] = unpack('B', thisInput)[0]
				newpacket+=1
				if newpacket >= 8 or unpack('B', thisInput)[0] == 253:
					packFile.write("\n")
					newpacket = 0
					this.lastx = (packetarray[1]*256 + packetarray[2])/500
					this.lasty = (packetarray[3]*256 + packetarray[4])/500
					this.lasttheta = (packetarray[5]*256 + packetarray[6])/10000.0
					if this.lasttheta > 3.14:
						this.lasttheta = this.lasttheta - 6.28
				lastPacket = time.clock()
			else:
				if (time.clock() > lastPacket + .05):
					packFile.write("\n")
					newPacket = 0
					lastPacket = time.clock() + 10000
				####
			####
		####
		print
	####
				
	def sendRaw(this, s, packFile):
		messageLength = input("Message Length >> ")
		message = ""
		for i in range(0, messageLength):
			message += pack("B", (input("Byte " + str(i) + ":")))
		####
		this.sendMessage(s, packFile, message, messageLength)
	####
		
	def sendMessage(this, s, packFile, message, messageLength):
		listen = input("number of listening seconds after >> ")
		if (input("0 to send immediately, 1 to wait for receive >> ")):
			s.flushInput()
			s.flushOutput()
			while (s.inWaiting() == 0):
				pass
			####
			this.monitorReceived(s, packFile, .1)
		####
		print ("Sending:")
		print repr(message)
		s.write(message)
		packFile.write("\nSent:\n" + str(unpack('B'*messageLength, message)) + "\n")
		if (listen):
			this.monitorReceived(s, packFile, listen)
		####
		this.lastmessage = message
		this.lastmessagelength = messageLength
	####
	
	def examinelast(this):
		print
		print ("Last message received:")
		print ("X: " + str(this.lastx))
		print ("Y: " + str(this.lasty))
		print ("Theta: " + str(this.lasttheta))
		print
	####
	
	def messageSendWizard(this, s, packFile):
		messageLength = 16
		message = ""
		message += pack("B", (input("Status byte: ")))
		#print("Will add current location to packet")
		xstart = input("Start in x direction: ")
		ystart = input ("Start in y direction: ")
		thetastart = input ("Start in theta direction: ")
		xmove= input("Move in x direction: ")
		ymove = input ("Move in y direction: ")
		thetamove = input ("Move in theta direction: ")
		message += pack("B", (xstart*500)/256)
		message += pack("B", (xstart*500)%256)
		message += pack("B", (ystart*500)/256)
		message += pack("B", (ystart*500)%256)
		while thetastart < 0:
			thetastart+=6.28
		message += pack("B", (thetastart*10000)/256)
		message += pack("B", (thetastart*10000)%256)
		message += pack("B", (xmove*500)/256)
		message += pack("B", (xmove*500)%256)
		message += pack("B", (ymove*500)/256)
		message += pack("B", (ymove*500)%256)
		while thetamove < 0:
			thetamove+=6.28
		message += pack("B", (thetamove*10000)/256)
		message += pack("B", (thetamove*10000)%256)
		EndAction = 0
		EndAction += input("EndAction(0,1=PU1,2=PU2,3=DO2,4=D01,5=AIR,6=FIN): ") * 32
		EndAction += input("EndColor(0,1=Y,2=Or,3=Br,4=Gr,5=R,6=Bl): ") * 4
		EndAction += input("EndLength(0,1=4in,2=3in,3=2in): ")
		message += pack("B", EndAction)
		message += pack("B", (input("Reserved Byte: ")))
		listen = input("number of listening seconds after >> ")
		errorCheck = 0
		sofarMessage = unpack('B'*15, message)
		for y in sofarMessage:
			errorCheck ^= y
		####
		message += pack("B", errorCheck)		
		print ("Waiting...")
		s.flushInput()
		s.flushOutput()
		while (s.inWaiting() == 0):
			pass
		####
		this.monitorReceived(s, packFile, .1)
		print ("Sending:")
		print repr(message)
		s.write(message)
		packFile.write("\nSent:\n" + str(unpack('B'*messageLength, message)) + "\n")
		if (listen):
			this.monitorReceived(s, packFile, listen)
		####
		this.lastmessage = message
		this.lastmessagelength = messageLength
	####
	
	def main(this):
		# Test for mobile unit comm
		s = serial.Serial(port='/dev/ttyUSB0', baudrate='9600')
		packFile = open("/home/sparc/path_planning/mobile_comm_test/packet_results.csv", "w")
		print ("Mobile Comm Test: Serial port 3 found")
		while(1):
			print ("Comm Test Main Menu:")
			print ("1. Monitor Input")
			print ("2. Clear Buffers")
			print ("3. Send raw message")
			print ("4. Send last message again")
			print ("5. Message send wizard")
			print ("6. Examine last packet received")
			print ("0. Exit")
			choice = input(">> ")
			if (choice == 1):
				this.monitorReceived(s, packFile, 0)
			elif (choice == 2):
				s.flushOutput()
				s.flushInput()
				print ("Buffers flushed")
			elif (choice == 3):
				this.sendRaw(s, packFile)
			elif (choice == 4):
				this.sendMessage(s, packFile, this.lastmessage, this.lastmessagelength)
			elif (choice == 5):
				this.messageSendWizard(s, packFile)
			elif (choice == 6):
				this.examinelast()
			elif (choice == 0):
				break
			####
		####
		packFile.close()
		return 0
	####
####

if __name__ == '__main__':
	main()
####
