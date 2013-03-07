#!/usr/bin/env python
"""

This module is the home for all Orientation Packet 
specific operations

"""

import packet_eater
import packet_utils

from base_packet import BasePacket

from block import Block
from block_zone import BlockDestinationZone

class OrientationPacket(BasePacket):
    
    #0xFC
    HANDSHAKE_FORMAT = 0b11111100

    #Destination constants
    RAIL = "rail"
    SEA = "sea"
    AIR = "air"

    def __init__(self, bytes_):
        BasePacket.__init__(self, bytes_=bytes_)
        
        #Byte Contents

        #byte 1
        #0xFC/0b11111100, the standard orientation signature handshake
        self.handshake = ""
        
        #bytes 2-15
        #Block pick-up colors and sizes, in the +x direction 
        #each 1 byte long as described below 
        #list of blocks. Last block will have the highest +x direction
        self.loading_zone_blocks = []
        
        #bytes 16-18 
        #6 Rail destination blocks 
        #  contains color/+x direction (4 bits per slot)      
        self.rail_colors = []
        
        #bytes 19-21 
        #6 Sea destination blocks
        #  contains color/+y direction (4 bits per slot)
        self.sea_colors = []

        #byte 22    
        #2 Air destination blocks
        #  contains color/+y direction (4 bits per slot) 
        self.air_colors = []
        
        #byte 23
        #Reserved
        self.reserved = ""

        #byte 24
        #Error Checking
        self.errors = ""


    def _decode_handshake(self):
        """ Read byte 1. Flag errors """
        self.handshake = packet_eater.read_bytes(self.packet_payload_string, 1)
        if self.handshake != HANDSHAKE_FORMAT:
            errorMsg = "Incorrect handshake format" 
            log_error(msg, func)
            return False

        return True
        

    def _decode_loading_zone_blocks(self):
        """ Decode loading zone information """
        #bytes 2-15
        packet_segment = packet_eater.read_bytes(self.packet_payload_string, 2, 15)
        byte_list = packet_eater.split_bytes(packet_segment)
        self.loading_zone_blocks = [Block(byte) for byte in byte_list]

        return

    def _decode_rail_colors(self):
        """ Decode rail colors """
        #bytes 16-18 
        packet_segment = packet_eater.read_bytes(self.packet_payload_string, 16, 18)
        nibble_list = packet_eater.split_bytes(packet_segment)
        
        self.rail_colors = [BlockDestinationZone(nibble, RAIL) for nibble in nibble_list]

        return


    def _decode_sea_colors(self):
        """ Decode sea colors """
        #bytes 19-21 
        packet_segment = packet_eater.read_bytes(self.packet_payload_string, 19, 21)
        nibble_list = packet_eater.split_bytes(packet_segment)

        self.sea_colors = [BlockDestinationZone(nibble, SEA) for nibble in nibble_list]
        return


    def _decode_air_colors(self):
        """ Decode air colors """
        #byte 22    
        packet_segment = packet_eater.read_bytes(self.packet_payload_string, 22)
        packet_list = packet_eater.split_bytes(packet_segment)

        self.air_colors = [BlockDestinationZone(nibble, AIR) for nibble in nibble_list]
        return

    #TODO: Figure out what to do with reserved byte
    def _decode_reserved(self):
        #byte 23
        self.reserved = packet_eater.read_bytes(self.packet_payload_string, 23)

    def _decode_errors(self):
        """ Decode errors byte """
        #byte 24
        self.errors = packet_eater.read_bytes(self.packet_payload_string, 24)


    def decode_packet(self):
       """ Deciphers packet information """ 
        
        #TODO: add error checking
        _decode_handshake()
        _decode_loading_zone_blocks()
        _decode_rail_colors()
        _decode_sea_colors()
        _decode_air_colors()
    
        return
    
    
    def _encode_handshake(self):
        """ Encode handshake """

        self.handshake = HANDSHAKE_FORMAT

        return 

    def _encode_loading_zone_segment(self, length, color):
        """ Encode one loading zone block """

        block_length = packet_utils.encode_length(length)
        block_color = packet_utils.encode_color(color)
        block_binary_form = block_length + block_color
        self.loading_zone_blocks.append(Block(block_binary_form))

        return
    
    def _encode_block_destination(self, destination, color):
        """ Encode one destination (rail,sea,air) color """

        destination_color = packet_utils.encode_color(color)
        
        if destination == RAIL:
            block_zone = BlockDestinationZone(destination_color, RAIL)
            self.rail_colors.append(block_zone)
        elif destination == SEA:
            block_zone = BlockDestinationZone(destination_color, SEA)
            self.sea_colors.append(block_zone)
        elif destination == AIR:
            block_zone = BlockDestinationZone(destination_color, AIR)
            self.air_colors.append(block_zone)
        
        return

    def _encode_reserved(self, reserved=None):
        #TODO: Find what to do with this

        if reserved is None:
            self.reserved = 0b00000000
            
        return

    def _encode_errors(self, error):
        #TODO: find error codes
        pass

    #TODO: Flesh this out
    #TODO: Need use cases, who is calling this, etc
    def encode_packet(self, var, var, var):
        self._encode_handshake()
        #Loop to encode all loading zone blocks
        #Loop to encode all destination zones
        #Encode reserved
        #Encode errors
        return
