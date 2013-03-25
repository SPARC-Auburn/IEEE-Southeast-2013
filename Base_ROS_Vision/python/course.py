#!bin/usr/env python
""" 
    
    This module provides a representation of the course.
    Handles path planning and graph manipulation.

"""

import string
import math

#NON STANDARD LIBRARY
import networkx
import numpy
import matplotlib.pyplot as pyplot

#INTERNAL
import block
import course_utils

class Course(object):

    def __init__(self, x=course_utils.COURSE_WIDTH,y=course_utils.COURSE_HEIGHT):
        self.grid = numpy.zeros((y,x), dtype=object)
        self.loading_zone = [None] * 14
        self.rail_zone = [None] * 6
        self.sea_zone = [None] * 6
        self.air_zone = [None] * 2

        #X, Y, Theta position of robot
        self.robot_position = (0, 0, 0)

        #Dictionary holding Block/BlockZone objects
        #Convenient lookup to determine what properties a 
        #particular coordinate has
        self.course_constructs = {}

        #graph representing path connections
        self.graph = networkx.DiGraph()

        course_utils.initialize_course_constructs(self.course_constructs)
        self.initialize_grid()



    #TODO: Add key
    #TODO: FIX ALL INDEXING


    def initialize_grid(self):
        course_utils.initialize_starting_area(self.grid)
        self.initialize_loading_zone()
        self.initialize_rail_zone()
        self.initialize_sea_zone()
        self.initialize_air_zone()
        self.initialize_ramp_area()

            # TODO: Finish adding whiteline stuff         
        #self.grid[START_ZONE_Y_START:START_ZONE_Y_END + WHITE_LINE_SIZE,
         #         START_ZONE_X_END + INDEX_BUFFER:WHITE_LINE_SIZE] = WHITE_LINE_CODE

        #self.grid[START_ZONE_Y_END + INDEX_BUFFER,
         #         START_ZONE_X_START:START_ZONE_X_END + INDEX_BUFFER] = WHITE_LINE_CODE
                  

    def initialze_ramp_area(self):
        pass
        #Unaccesible portions
        #self.grid[640:800][:] = BLOCKED_PATH_CODE
        #Top portion of ramp
        #self.grid[500:640][:] = RAMP_CODE
        
        #Ramp entrance
        #TODO: Make this more reasonable
        #self.grid[400:500][RAMP_START_X:] = RAMP_ENTRANCE_CODE

    def initialize_loading_zone(self):
        pass

    def initialize_rail_zone(self):
        pass
        #for i in xrange(SEA_ZONE_Y_START, SEA_ZONE_Y_END, DESTINATION_ZONE_WIDTH * 2 + 1):
         #   print i
          #  self.grid[i][SEA_ZONE_X_START:SEA_ZONE_X_END] = WHITE_LINE_CODE
    
    def initialize_sea_zone(self):
        """
        SEA_ZONE_Y_START = START_ZONE_Y_END + (INDEX_BUFFER * 9)
        SEA_ZONE_Y_END = SEA_ZONE_Y_START + (INDEX_BUFFER * 2.5)
        
        SEA_ZONE_X_START = 0
        SEA_ZONE_X_END = INDEX_BUFFER * 4
       """ 
        #TODO: Fix the spacing. It should just be adding WHITE_SPACE
        #TODO: or something like that. WAY over indexing now
       
        #for i in xrange(1, SEA_ZONE_COUNT):
         #   self.grid[SEA_ZONE_Y_START * i:SEA_ZONE_Y_END * i,
          #            SEA_ZONE_X_START:SEA_ZONE_X_END] = SEA_ZONE_CODE
            #self.grid[SEA_INITIAL_EDGE_X]
            #self.grid[FIRST_SEA_BLOCK_Y_START:,
             #         FIRST_SEA_BLOCK_X_START * i:FIRST_SEA_BLOCK_X_END * i] = WHITE_LINE_CODE

    def initialize_air_zone(self):
        pass

    def initialize_ramp_area(self):
        pass

    def clear_graph(self):
        self.graph.clear()
        
    def plan_route(self):
        """ Generates queue of Command Packets """
        pass

    def get_next_node(self):
        pass

    def generate_graph(self):
        #Always start from clean slate
        self.clear_graph()

        #Add connections the robot has to loading zone
        loading_zone_edges = self.get_loading_zone_edges()
        self.graph.add_weighted_edges_from()
        #Add connections the loading zone has to rail
 #       self.graph.add_weighted_edges_from()
        #Add connections loading zone has to sea
#        self.graph.add_weighted_edges_from()
        #Add connections loading zone has to air
#        self.graph.add_weighted_edges_from()

    def randomize_grid(self, seed=None):
        pass

    def get_loading_zone(self):
        pass

    def get_rail_zone(self):
        pass

    def get_sea_zone(self):
        pass

    def get_air_zone(self):
        pass

    def is_drivable(x,y):
        #if code is this, yes
        #if code is this, no
        pass
    
    def decode_orientation_packet(self, orientation_packet):
        #Intent is to use this information to populate the real course
        #Ideally we have already figured out this information elsewhere.
        pass
    
if __name__ == "__main__":
    C = Course()    
    """
    course_utils.fill_loading_zone(C.grid, 1, 0b11)
    course_utils.fill_loading_zone(C.grid, 2, 0b11)
    course_utils.fill_loading_zone(C.grid, 3, 0b11)
    course_utils.fill_loading_zone(C.grid, 4, 0b11)
    course_utils.fill_loading_zone(C.grid, 5, 0b11)
    course_utils.fill_loading_zone(C.grid, 6, 0b11)
    course_utils.fill_loading_zone(C.grid, 7, 0b11)
    course_utils.fill_loading_zone(C.grid, 8, 0b11)
    course_utils.fill_loading_zone(C.grid, 9, 0b11)
    course_utils.fill_loading_zone(C.grid, 10, 0b11)
    course_utils.fill_loading_zone(C.grid, 11, 0b11)
    course_utils.fill_loading_zone(C.grid, 12, 0b11)
    course_utils.fill_loading_zone(C.grid, 13, 0b11)
    course_utils.fill_loading_zone(C.grid, 14, 0b11)
    """
    """
    course_utils.fill_sea_zone(C.grid, 1, 0b11)
    course_utils.fill_sea_zone(C.grid, 2, 0b11)
    course_utils.fill_sea_zone(C.grid, 3, 0b11)
    course_utils.fill_sea_zone(C.grid, 4, 0b11)
    course_utils.fill_sea_zone(C.grid, 5, 0b11)
    course_utils.fill_sea_zone(C.grid, 6, 0b11)
    """
    course_utils.fill_rail_zone(C.grid, 1, 0b11)
    course_utils.fill_rail_zone(C.grid, 2, 0b11)
    course_utils.fill_rail_zone(C.grid, 3, 0b11)
    course_utils.fill_rail_zone(C.grid, 4, 0b11)
    course_utils.fill_rail_zone(C.grid, 5, 0b11)
    course_utils.fill_rail_zone(C.grid, 6, 0b11)
    pass
