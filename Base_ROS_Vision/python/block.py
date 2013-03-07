#!/usr/bin/env python

import packet_utils

class Block(object):
    
    def __init__(self, binary_string):
        self._binary_representation = binary_string
        self._length = None
        self._color = None

        read_properties()

    def _read_length(self):
        """ Decode length portion of the packet """
        self._length = course_utils.read_length(self.binary_representation, 
                                                LENGTH_NIBBLE_POSITION)

        return

    def _read_color(self):
        """ Decode color portion of the packet """

        self.color = course_utils.read_color(self._binary_representation, 
                                             COLOR_NIBBLE_POSITION)
        
        return
    
    def read_properties(self);
        _read_length()
        _read_color()

    def get_length(self):
        return self._length

    def get_color(self):
        return self._color

    def get_binary_form(self):
        return binary_representation
