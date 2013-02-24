#!/usr/bin/env python
"""

This module is the home for all Orientation Packet 
specific operations

"""

from block import Block
from base_packet import BasePacket
from block_zone import BlockDestinationZone
from communications.packet import packet_eater

class OrientationPacket(BasePacket):
    
    HANDSHAKE_FORMAT = '11111100'
    
    def __init__(self, binary_string):
        BasePacket.__init__(self, binary_string)
        
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
        self.reserved = []

        #byte 24
        #Error Checking
        self.errors = []


    def _read_handshake():
        """ Read byte 1. Flag errors """
        self.handshake = packet_eater.read_bytes(self.packet_payload, 1)
        if self.handshake != HANDSHAKE_FORMAT:
            errorMsg = "Incorrect handshake format" 
            log_error(msg, func)
            return False

        return True
        

    def _read_loading_zone_blocks():
        """ Decode loading zone information """
        #bytes 2-15
        packet_segment = packet_eater.read_bytes(self.packet_payload, 2, 15)
        byte_list = packet_eater.split_bytes(packet_segment)
        self.loading_zone_blocks = [Block(byte) for byte in byte_list]

        return

    def _read_rail_colors():
        """ Decode rail colors """
        #bytes 16-18 
        packet_segment = packet_eater.read_bytes(self.packet_payload, 16, 18)
        nibble_list = packet_eater.split_bytes(packet_segment)
        
        self.rail_colors = [BlockDestinationZone(nibble, 'rail') for nibble in nibble_list]

        return


    def _read_sea_colors():
        """ Decode sea colors """
        #bytes 19-21 
        packet_segment = packet_eater.read_bytes(self.packet_payload, 19, 21)
        nibble_list = packet_eater.split_bytes(packet_segment)A

        self.sea_colors = [BlockDestinationZone(nibble, 'sea') for nibble in nibble_list]
        return


    def _read_air_colors():
        """ Decode air colors """
        #byte 22    
        packet_segment = packet_eater.read_bytes(self.packet_payload, 22)
        packet_list = packet_eater.split_bytes(packet_segment)

        self.air_colors = [BlockDestinationZone(nibble, 'air') for nibble in nibble_list]
        return


    def _read_errors():
        """ Decode errors byte """
        #byte 24
        packet_segment = packet_eater.read_bytes(self.packet_payload, 24)


    def read_packet():
       """ Deciphers packet information """ 
        
        #TODO: add error checking
        _read_handshake()
        _read_loading_zone_blocks()
        _read_rail_colors()
        _read_sea_colors()
        _read_air_colors()
    
        return





