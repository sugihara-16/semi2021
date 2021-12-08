#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import Empty
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


def callback():
    rospy.loginfo('activated')
    pub.publish()

if __name__ == '__main__':
    try:
        rospy.init_node('takeoff')
        pub = rospy.Publisher('/tello/takeoff',Empty)
        callback()
        rospy.spin()
    except rospy.ROSInterruptException: pass