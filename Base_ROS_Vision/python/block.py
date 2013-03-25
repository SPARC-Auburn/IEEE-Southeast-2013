#!/usr/bin/env python

import packet_utils

INCH = 1

# Measurement is in inches
BLOCK_LENGTH = 3/2

RAIL_BLOCK_LENGTH = 4
SEA_BLOCK_LENGTH = 3
AIR_BLOCK_LENGTH = 2

LENGTH_NIBBLE_POSITION = 1
BLOCK_COLOR_NIBBLE_POSITION = 2

ZONE_COLOR_NIBBLE_POSITION = 1

class Block(object):

    def __init__(self, binary_string):
        self._binary_representation = binary_string
        self._length = None
        self._color = None
        self._type = None

        self.read_properties()
    
    def __str__(self):
        ret_str = "\nType: " + str(self._type)
        ret_str += "\nColor: " + str(self._color)
        ret_str += "\nLength: " + str(self._length) + "\n"
        
        return ret_str

    def _read_length(self):
        """ Decode length portion of the packet """
        self._length = packet_utils.decode_length(self._binary_representation, 
                                                  LENGTH_NIBBLE_POSITION)

        return

    def _read_color(self):
        """ Decode color portion of the packet """
        self._color = packet_utils.decode_color(self._binary_representation, 
                                                BLOCK_COLOR_NIBBLE_POSITION)
        return

    def _read_type(self):
        if self._length == RAIL_BLOCK_LENGTH:
            self._type = "rail"
        elif self._length == SEA_BLOCK_LENGTH:
            self._type = "sea"
        elif self._length == AIR_BLOCK_LENGTH:
            self._type = "air"
        else:
            self._type = "unknown"

    def read_properties(self):
        self._read_length()
        self._read_color()
        self._read_type()

    def get_length(self):
        return self._length

    def get_color(self):
        return self._color

    def get_binary_form(self):
        return self._binary_representation

class BlockZone(object):

    def __init__(self, binary_string, midpoint=None, zone_type=None, block=None):
        self._binary_representation = binary_string
                
        self._midpoint = midpoint
        self._zone_type = zone_type
        self._block = block

        
        self._color = ""
        
        self.read_properties()

        return

    def __str__(self):
        ret_str = "\n Binary: " + str(self._binary_representation)
        ret_str += "\nType: " + str(self._zone_type)
        ret_str += "\nColor: " + str(self._color)
        
        return ret_str

    def get_color(self):
        return self._color

    def get_zone(self):
        return self._zone_type

    def get_midpoint(self):
        return self._midpoint

    def encode_binary_form(self):
        pass
    
    def read_properties(self):
        self._read_color()

        return 

    def _read_color(self):
        self._color = packet_utils.decode_color(self._binary_representation,
                                                ZONE_COLOR_NIBBLE_POSITION)
        return

    
