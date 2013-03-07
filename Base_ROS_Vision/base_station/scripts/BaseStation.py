#!/usr/bin/env python
import roslib; roslib.load_manifest('base_station')
import rospy
from std_msgs.msg import String

def data_packet_callback(data):
    rospy.loginfo(rospy.get_name() + ": I heard %s" % data.data)
def find_block_callback(data):
    rospy.loginfo(rospy.get_name() + ": I heard %s" % data.data)
def base_station():
    pub = rospy.Publisher('command_packet', String)
    sub = rospy.Subscriber('report_packet', String, data_packet_callback)
    sub_blocks = rospy.Subscriber('block_map', String, find_block_callback) 
    rospy.init_node('base_station')
    rospy.spin()

if __name__ == '__main__':
    try:
        base_station()
    except rospy.ROSInterruptException:
        pass
