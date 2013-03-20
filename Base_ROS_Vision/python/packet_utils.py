#!/usr/bin/env python

import packet_eater

#TODO: change name to packet_utils

NIBBLE_OFFSET = 4
BYTE_OFFSET = 8

#Length codes
UNKNOWN_LENGTH_FORMAT = 0b0000
FOUR_INCH_FORMAT = 0b0001
THREE_INCH_FORMAT = 0b0010
TWO_INCH_FORMAT = 0b0011

FOUR_INCH = 4
THREE_INCH = 3
TWO_INCH = 2

#Color codes
UNKNOWN_COLOR_FORMAT = 0b0000
YELLOW_FORMAT = 0b0001
ORANGE_FORMAT = 0b0010
BROWN_FORMAT = 0b0011
GREEN_FORMAT = 0b0100
RED_FORMAT = 0b0101
BLUE_FORMAT = 0b0110

def byte_to_string(binary_value):
    #Must cast binary value to bin to ensure 0b appears in string
    binary_string = str(bin(binary_value))[2:]
    binary_string = "0" * (-len(binary_string) % BYTE_OFFSET) + binary_string

    return binary_string

def nibble_to_string(binary_value):
    #Must cast binary value to bin to ensure 0b appears in string
    binary_string = str(bin(binary_value))[2:]
    binary_string = "0" * (-len(binary_string) % NIBBLE_OFFSET) + binary_string

    return binary_string

def decode_length(binary_string, length_nibble_position):
    """ Decode length portion of the packet """
    length_info = packet_eater.read_nibbles(binary_string, 
                                            length_nibble_position)

    length_info = bin(length_info)

    if length_info == UNKNOWN_LENGTH_FORMAT:
        length = None
    elif length_info == FOUR_INCH_FORMAT:
        length = 4
    elif length_info == THREE_INCH_FORMAT:
        length = 3
    elif length_info == TWO_INCH_FORMAT:
        length = 2
    
    return length

def decode_color(binary_string, color_nibble_position):
    """ Decode color portion of the packet """

    color_info = packet_eater.read_nibbles(binary_string, 
                                           color_nibble_position)
    color_info = bin(color_info)

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

def encode_color(color):
    """ Encode color portion of block byte """

    color_binary = ""
    
    #TODO: Determine input values

    if color == YELLOW_RANGE:
        color_binary = YELLOW_FORMAT
    elif color_binary == ORANGE_RANGE:
        color_binary = ORANGE_FORMAT
    elif color == BROWN_RANGE:
        color_binary = BROWN_FORMAT
    elif color == GREEN_RANGE:
        color_binary = GREEN_FORMAT
    elif color == RED_RANGE:
        color_binary = RED_FORMAT
    else:
        color_binary = UNKNOWN_COLOR_FORMAT

    return byte_to_string(color_binary)

def encode_length(length):
    """ Encode length portion of block byte """
    
    length_binary = ""

    if length == FOUR_INCH:
        length_binary = FOUR_INCH_FORMAT
    elif length == THREE_INCH:
        length_binary = THREE_INCH_FORMAT
    elif length == TWO_INCH:
        length_binary = TWO_INCH_FORMAT
    else:   
        length_binary = UNKNOWN_LENGTH_FORMAT
    
    return byte_to_string(length_binary)
