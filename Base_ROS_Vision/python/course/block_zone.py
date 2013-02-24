#!/usr/bin/env python

import course_utils

class BlockDestinationZone(object):

    def __init__(self, binary_string, zone_type):
        self.binary_representation = binary_string
        self._zone_type = zone_type

        self._color = ""
        
        read_properties()

        return

    def _read_color():
        self._color = course_utils.read_color(self.binary_representation,
                                              COLOR_NIBBLE_POSITION)

        return

    def get_color(self):
        return _self.color

    def get_zone(self):
        return self._zone_type
