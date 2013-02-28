import argparse
import serial
from subprocess import call
RATE = 9600

class CameraController(object):
    def __init__(self, serial_port):
        self.serial_port = serial_port
        self.initialize_serial()
        self.dongle = serial.Serial(serial_port, RATE)
        self.dongle.open()
        self._theta = 0
        self._phi = 0

    def initialize_serial(self):
        command = ['sudo', 'stty', '-F', self.serial_port, str(RATE), 'ignbrk', '-brkint', '-icrnl', '-imaxbel', '-opost',
                   '-onlcr', '-isig', '-icanon', '-iexten', '-echo', '-echok', '-echoctl', '-echoke', 'noflsh', '-ixon', '-crtscts']
        call(command)
        command = ['sudo', 'chmod', '666', self.serial_port]
        call(command)

    def set_theta(self, value):
        self._theta = value
        self.position_camera()

    def set_phi(self, value):
        self._phi = value
        self.position_camera()

    def set_position(self, theta, phi):
        self._theta = theta
        self._phi = phi
        self.position_camera()

    def position_camera(self):
        self.dongle.write("\nm %d %d" % (self._theta, self._phi))

    def close(self):
        self.dongle.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('serial_post')
    parser.add_argument('theta', type=int)
    parser.add_argument('phi', type=int)
    args = parser.parse_args()
    c = CameraController(args.serial_port)
    c.set_position(args.theta, args.phi)
    c.close()
