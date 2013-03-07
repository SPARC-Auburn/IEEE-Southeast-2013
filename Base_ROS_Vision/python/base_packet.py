#!/usr/bin/env python

"""

Base class for all Packet objects

"""

import packet_utils

class BasePacket(object):

    def __init__(self, bytes_=None):
        self.packet_payload = bytes_
        self.packet_payload_string = ""
        if bytes_ is not None:
            self.packet_payload_string = packet_utils.byte_to_string(byte)


    def read_packet():
        pass

    def log_error(errorMsg):
        error_time = time()
        
