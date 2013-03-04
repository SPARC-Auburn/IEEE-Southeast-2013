#!/usr/bin/env python

"""

Base class for all Packet objects

"""

from time import time

class BasePacket(object):

    def __init__(self, binary_string):
        self.packet_payload = binary_string

    def read_packet():
        pass

    def log_error(errorMsg):
        error_time = time()
        
