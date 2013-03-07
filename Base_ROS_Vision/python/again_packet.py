#!/usr/bin/env

from communication_packet import CommunicationPacket

"""

Module for all operations specific to the Again Packet

"""

class AgainPacket(CommunicationPacket):
    
    #0xFE
    AGAIN_PACKET_FORMAT = 11111110
    
    def __init__(self, packetStr):
        CommunicationPacket.__init__(self, packetStr)

    def decode_packet():
        pass
        
    def encode_packet():
        return 11111110
     
