#!/usr/bin/env python

from base_packet import BasePacket


class CommandPacket(BasePacket):
    
    def __init__(bytes_=None, flags=None, current=None, destination=None):
        BasePacket.__init__(self, bytes_=bytes_)
    
        #TODO: EVERYTHING
        #TODO: Below is just placeholders
        #Byte Contents
        #1 Status - 8 Enumerated flags that qualify the instruction path.
        self.status_flags = None
        #2-7 Current position (see Data Structures Section) 
        self.current_position = (0, 0, 0)
        #8-13 Destination (see Data Structures Section) 
        self.destination = (0, 0, 0)
        #14 End action - Enumerated: block pickup, drop-off, etc.
        self.end_action = None
        #15 Reserved
        self.reserved = None
        #16 Error checking
        self.errors = None
    

    def _encode_flags(self):
        pass

    def _encode_position(self):
        pass

    def _encode_destination(self):
        pass

    def _encode_end_action(self):
        pass

    def _encode_errors(self):
        pass

