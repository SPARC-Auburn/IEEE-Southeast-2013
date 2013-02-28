#!/usr/bin/env python
import roslib; roslib.load_manifest('base_station')
import rospy
from std_msgs.msg import String


def serial_in():
    pub = rospy.Publisher('report_packet', String)
    rospy.init_node('serial_in')
    while not rospy.is_shutdown():
        rospy.sleep(1.0)

if __name__ == '__main__':
    try:
        serial_in()
    except rospy.ROSInterruptException:
        pass
