#!/usr/bin/env python

import packet_eater

#Length codes
UNKNOWN_LENGTH_FORMAT = '0000'
FOUR_INCH_FORMAT = '0001'
THREE_INCH_FORMAT = '0010'
TWO_INCH_FORMAT = '0011'

#Color codes
UNKNOWN_COLOR_FORMAT = '0000'
YELLOW_FORMAT = '0001'
ORANGE_FORMAT = '0010'
BROWN_FORMAT = '0011'
GREEN_FORMAT = '0100'
RED_FORMAT = '0101'
BLUE_FORMAT = '0110'


def read_length(binary_string, length_nibble_position):
    """ Decode length portion of the packet """

    length_info = packet_eater.read_nibbles(self.binary_representation, 
                                            length_nibble_position)

    if length_info == UNKNOWN_LENGTH_FORMAT:
        length = None
    elif length_info == FOUR_INCH_FORMAT:
        length = 4
    elif length_info == THREE_INCH_FORMAT:
        length = 3
    elif length_info == TWO_INCH_FORMAT:
        length = 2
    
    return length

def read_color(binary_string, color_nibble_position):
    """ Decode color portion of the packet """

    color_info = packet_eater.read_nibbles(self.binary_representation, 
                                           color_nibble_position)
    
    if color_info == UNKNOWN_COLOR_FORMAT:
        color = None
    elif color_info == YELLOW_FORMAT:
        color = 'yellow'
    elif color_info == ORANGE_FORMAT:
        color = 'orange'
    elif color_info == BROWN_FORMAT:
        color = 'brown'
    elif color_info == GREEN_FORMAT:
        color = 'green'
    elif color_info == RED_FORMAT:
        color = 'red'

    return color
