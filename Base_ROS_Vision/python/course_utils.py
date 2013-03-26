import string
import math

#NON STANDARD LIB
import networkx
import numpy

#INTERNAL
import block
import packet_utils
import packet_eater

DEBUG = True

INCH = 1
INDEX_SIZE = INCH * .5
INDEX_BUFFER = INCH * 50
TOP_BUFFER = INDEX_BUFFER * 15
LEFT_BUFFER = INDEX_BUFFER * 8.5
BOTTOM_BUFFER = INDEX_BUFFER * 32.5

MOBILE_COORDINATE_INCREMENT = INCH * 500

REAL_COURSE_WIDTH = INCH * 96
REAL_COURSE_HEIGHT = INCH * 48

COURSE_WIDTH = 6400
COURSE_HEIGHT = 4200

BLOCK_VARIATION_COUNT = 7
RAIL_BLOCK_COUNT = 6
SEA_BLOCK_COUNT = 6
RAMP_BLOCK_COUNT = 2
GROUND_BLOCK_COUNT = 14

#TODO: Make keys more logical
#TODO: Keys should be based on protocol when applicable
START_ZONE_CODE = 0b111

#Protocol (Command Status)
#bit 3
WHITE_LINE_CODE = 0b00000100
RAMP_CODE = 0b00001000
RAMP_ENTRANCE_CODE = 0b00010000

BLOCKED_PATH_CODE = 0b10

LOADING_ZONE_CODE = 0b100
RAIL_ZONE_CODE = 0b101
SEA_ZONE_CODE = 0b110
AIR_ZONE_CODE = 0b110

UNKNOWN_COLOR_FORMAT = 0b0000
YELLOW_FORMAT = 0b0001
ORANGE_FORMAT = 0b0010
BROWN_FORMAT = 0b0011
GREEN_FORMAT = 0b0100
RED_FORMAT = 0b0101
BLUE_FORMAT = 0b0110

SEA_ZONE_COUNT = 6

BLOCK_ZONE_WIDTH = INCH * INDEX_BUFFER * 2.5

#Height of all drop off zones
#Recall LENGTH may be in X direction
LOADING_ZONE_LENGTH =  INCH * INDEX_BUFFER * 6
RAIL_LENGTH = INCH * INDEX_BUFFER *  5
SEA_LENGTH = INCH * INDEX_BUFFER * 4
AIR_LENGTH = INCH * INDEX_BUFFER * 3

WHITE_LINE_SIZE = INDEX_BUFFER * .5

RAMP_X_START = COURSE_WIDTH - (INDEX_BUFFER * 24)

#Start and end locations of FIRST zone
#Must calculate position of offset blocks
#based on initial locations
START_ZONE_X_START = 0
START_ZONE_Y_START = 0

START_ZONE_X_END = INDEX_BUFFER * 12
START_ZONE_Y_END = INDEX_BUFFER * 12

RAIL_ZONE_Y_START = 0
RAIL_ZONE_Y_END = RAIL_LENGTH

#TODO: CORRECT THESE MEASUREMENTS
#      The ones listed on the diagram are not correct
RAIL_ZONE_X_START = (START_ZONE_X_END + BOTTOM_BUFFER + (2 * WHITE_LINE_SIZE))
RAIL_ZONE_X_END = RAIL_ZONE_X_START + BLOCK_ZONE_WIDTH

SEA_ZONE_Y_START = START_ZONE_Y_END + (2 * WHITE_LINE_SIZE) + LEFT_BUFFER
SEA_ZONE_Y_END  = SEA_ZONE_Y_START + BLOCK_ZONE_WIDTH

SEA_ZONE_X_START = 0
SEA_ZONE_X_END =  int(SEA_LENGTH)

#TODO: CORRECT THESE MEASUREMENTS
#      The ones listed on the diagram are not correct
LOADING_ZONE_X_START = math.ceil(TOP_BUFFER + WHITE_LINE_SIZE)
LOADING_ZONE_X_END =  math.ceil(LOADING_ZONE_X_START + BLOCK_ZONE_WIDTH)

LOADING_ZONE_Y_END = REAL_COURSE_HEIGHT * INDEX_BUFFER
LOADING_ZONE_Y_START = LOADING_ZONE_Y_END - LOADING_ZONE_LENGTH

AIR_ZONE_Y_START = LOADING_ZONE_Y_END + (2 * WHITE_LINE_SIZE)
AIR_ZONE_Y_END = AIR_ZONE_Y_START + BLOCK_ZONE_WIDTH

AIR_ZONE_X_START  = 0
AIR_ZONE_X_END = AIR_LENGTH

def distance(point_one, point_two):
    diff_x_squared = math.pow(point_two[1] - point_one[1], 2)
    diff_y_squared = math.pow(point_two[0] - point_one[0], 2)

    return numpy.sqrt(diff_x_squared + diff_y_squared)

def fill_block_zones(loading_zone, rail, sea, air):
    #TODO: implement
    #parameters are lists of objects
    pass


def fill_loading_zone(grid, zone_position, zone_code):
    
   
    loading_x_start, loading_x_end = adjust_widths(LOADING_ZONE_X_START,
                                                   LOADING_ZONE_X_END,
                                                   zone_position)
    #TODO: Verify loading zone coordinates
    #      send robit to a reasonable location
#    loading_x_start = math.ceil(loading_x_start)
#    loading_x_end = math.ceil(loading_x_end)
    grid[LOADING_ZONE_Y_START:LOADING_ZONE_Y_END,
         loading_x_start:loading_x_end] = zone_code

    if DEBUG:
        print LOADING_ZONE_X_START
        print LOADING_ZONE_X_END

        print loading_x_start
        print loading_x_end


        print grid[LOADING_ZONE_Y_START-1:LOADING_ZONE_Y_END+1,
                   loading_x_start-1:loading_x_end+1]


def fill_rail_zone(grid, zone_position, zone_code):
    """ """
   
    rail_x_start, rail_x_end = adjust_widths(RAIL_ZONE_X_START,
                                             RAIL_ZONE_X_END,
                                             zone_position)
    
    
    grid[RAIL_ZONE_Y_START:RAIL_ZONE_Y_END, 
         rail_x_start : rail_x_end ] = zone_code

    if DEBUG:
        print RAIL_ZONE_X_START
        print RAIL_ZONE_X_END

        print rail_x_start
        print rail_x_end


        print grid[RAIL_ZONE_Y_START:RAIL_ZONE_Y_END+1,
                   rail_x_start-1:rail_x_end+1]


#first element is zone closest to 
def fill_sea_zone(grid, zone_position, zone_code):
    """ """ 

    sea_y_start, sea_y_end = adjust_widths(SEA_ZONE_Y_START, 
                                           SEA_ZONE_Y_END,
                                           zone_position)

    grid[sea_y_start:sea_y_end, 
         SEA_ZONE_X_START : SEA_ZONE_X_END ] = zone_code


    if DEBUG:
        print zone_position
        print SEA_ZONE_Y_START
        print SEA_ZONE_Y_END

        print sea_y_start
        print sea_y_end


        print grid[sea_y_start - 1:sea_y_end + 1,
                   SEA_ZONE_X_START:SEA_ZONE_X_END + 1]



def fill_air_zone(grid, zone_position, zone_code):
    """ """
    

    air_y_start, air_y_end = adjust_widths(AIR_ZONE_Y_START,
                                           AIR_ZONE_Y_END,
                                           zone_position)                               
    grid[air_y_start:air_y_end,
         AIR_ZONE_X_START:AIR_ZONE_X_END] = zone_code

    if DEBUG:
        print zone_position
        print AIR_ZONE_Y_START
        print AIR_ZONE_Y_END

        print air_y_start
        print air_y_end


        print grid[air_y_start - 1:air_y_end + 1,
                   AIR_ZONE_X_START:AIR_ZONE_X_END + 1]



def initialize_starting_area(grid):
    """ Sets starting zone area codes """ 
    #TODO: Change this to robot code?

    grid[START_ZONE_Y_START:START_ZONE_Y_END, 
         START_ZONE_X_START:START_ZONE_X_END] = START_ZONE_CODE


def adjust_widths(start_width, end_width, zone_position):
    """ 
        Adds appropriate padding to block zone width coordinates.
        
    """
    if zone_position > 1:
        start_width += ((BLOCK_ZONE_WIDTH + WHITE_LINE_SIZE) * (zone_position - 1))
        end_width = (start_width + BLOCK_ZONE_WIDTH)

    return (int(start_width), int(end_width))
    

def initialize_course_constructs(course_constructs):
    unknown_block = packet_eater.nibble_to_string(packet_utils.UNKNOWN_COLOR_FORMAT)
    yellow_block = packet_eater.nibble_to_string(packet_utils.YELLOW_FORMAT)
    orange_block = packet_eater.nibble_to_string(packet_utils.ORANGE_FORMAT)
    brown_block = packet_eater.nibble_to_string(packet_utils.BROWN_FORMAT)
    green_block = packet_eater.nibble_to_string(packet_utils.GREEN_FORMAT)
    red_block = packet_eater.nibble_to_string(packet_utils.RED_FORMAT)
    blue_block =  packet_eater.nibble_to_string(packet_utils.BLUE_FORMAT)

    unknown_length_string = packet_eater.nibble_to_string(packet_utils.UNKNOWN_LENGTH_FORMAT)
    four_inch_string = packet_eater.nibble_to_string(packet_utils.FOUR_INCH_FORMAT)
    three_inch_string = packet_eater.nibble_to_string(packet_utils.THREE_INCH_FORMAT)
    two_inch_string = packet_eater.nibble_to_string(packet_utils.TWO_INCH_FORMAT)
   

    colors = [unknown_block, yellow_block, orange_block, brown_block, green_block,
              red_block, blue_block]    
    lengths = [unknown_length_string, four_inch_string, three_inch_string,
               two_inch_string]

    initialize_block_zones_constructs(colors, course_constructs)
    initialize_block_constructs(colors, lengths, course_constructs)        


def initialize_block_zones_constructs(colors, course_constructs):
    course_constructs = {}
    for color in colors:
        course_constructs[color] = block.BlockZone(color)          

    return course_constructs

def initialize_block_constructs(colors, lengths, course_constructs):
    for color in colors:
        unknown_block_str = string.join([lengths[0], color], '')
        rail_block_str = string.join([lengths[1], color], '')
        sea_block_str = string.join([lengths[2], color], '')
        air_block_str = string.join([lengths[3], color], '')
        
        course_constructs[unknown_block_str] = block.Block(unknown_block_str)
        course_constructs[rail_block_str] = block.Block(rail_block_str)
        course_constructs[sea_block_str] = block.Block(sea_block_str)
        course_constructs[air_block_str] = block.Block(air_block_str)

def get_construct( key):
    return course_constructs[key]

if __name__ == "__main__":

    pass
