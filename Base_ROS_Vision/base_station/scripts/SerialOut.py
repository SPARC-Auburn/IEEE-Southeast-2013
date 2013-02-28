#!/usr/bin/env python
import roslib; roslib.load_manifest('base_station')
import rospy
from std_msgs.msg import String

def data_packet_callback(data):
    rospy.loginfo(rospy.get_name() + ": I heard %s" % data.data)
def serial_out():
    sub = rospy.Subscriber('command_packet', String, data_packet_callback)
    rospy.init_node('serial_out')
    rospy.spin()

if __name__ == '__main__':
    try:
        serial_out()
    except rospy.ROSInterruptException:
        pass
