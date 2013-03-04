#!/usr/bin/env python
import roslib; roslib.load_manifest('base_station')
import rospy
from std_msgs.msg import String


def find_blocks():
    pub = rospy.Publisher('block_map', String)
    rospy.init_node('find_blocks')
    while not rospy.is_shutdown():
        #str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(str)
        #pub.publish(String(str))
        rospy.sleep(1.0)

if __name__ == '__main__':
    try:
        find_blocks()
    except rospy.ROSInterruptException:
        pass
