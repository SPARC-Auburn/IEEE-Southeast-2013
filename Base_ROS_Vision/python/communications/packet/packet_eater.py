#!bin/usr/env python
""" 
    
    This module provides functionality to easily retrieve 
    specific bytes and nibbles from a binary string

"""

BYTE_OFFSET = 8
NIBBLE_OFFSET = 4

def read_nibbles(binary_string, first_nibble, final_nibble=None):

    """

        Def Name: readNibbles
         
        Return: 
            first_nibble from binary_string.
            If final_nibble is included, all nibbles starting
            from first_nibble to final_nibble are included.
           
        Description:
            Extract nibble(s) from binary_string.
            Function assumes that first_nibble and
            final_nibble will be present.

        Usage:
            #returns 0000
            readNibbles('0000', 1)
            #returns 00010101
            readNibbles('000000010101', 2, 3)

           
    """ 

    final_index = first_nibble * NIBBLE_OFFSET
    first_index = final_index - NIBBLE_OFFSET
    if final_nibble is not None:
        final_index = final_nibble * NIBBLE_OFFSET       

    return binary_string[first_index:final_index]

def read_bytes(binary_string, first_byte, final_byte=None):

    """
        Def Name: readBytes
         
        Return: 
            first_byte from binary_string.
            If final_byte is included, all nibbles starting
            from first_byte to final_byte are included.
           
        Description: 
            Extract byte(s) from binary_string.
            Function assumes that first_byte
            and final_byte will be present.

         Usage:            
            #returns 00000000
            readBytes('00000000', 1)
            #returns 1000000101010101
            readBytes('000000001000000101010101, 2, 3)

    """

    final_index = first_byte * BYTE_OFFSET
    first_index = final_index - BYTE_OFFSET
    if final_byte is not None:
        final_index =  final_byte * BYTE_OFFSET 
    
    return binary_string[first_index:final_index]        

def split_bytes(binary_string):
    byte_list = []
    for i in xrange(0, len(binary_string), BYTE_OFFSET):
        byte_list.append(binary_string[i:BYTE_OFFSET + i])
    
    return byte_list

def split_nibbles(binary_string):
    nibble_list = []
    for i in xrange(0, len(binary_string), NIBBLE_OFFSET):
        nibble_list.append(binary_string[i:NIBBLE_OFFSET + i])

    return nibble_list

if __name__ == "__main__":
    pass 
    """
    b1 = '00000000'
    b2 = '11111111'
    b3 = '01010101'
    b4 = '10101010'

    print splitBytes(b1)
    print splitBytes(b1 + b2)
    print splitBytes(b1 + b2 + b3)
    print splitBytes(b1 + b2 + b3 + b4)


    print splitNibbles(b1)
    print splitNibbles(b1 + b2)
    print splitNibbles(b1 + b2 + b3)
    print splitNibbles(b1 + b2 + b3 + b4)
    """

