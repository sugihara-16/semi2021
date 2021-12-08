#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2
import math

def callback(msg):
    rospy.loginfo("get")

    try:
        bridge = CvBridge()
        orig = bridge.imgmsg_to_cv2(msg,"bgr8") #opencv用に変換
        
        imgMsg = bridge.cv2_to_imgmsg(orig,"bgr8")
        pub = rospy.Publisher('optical_flow',Image,queue_size=10)
        pub.publish(imgMsg)
        
    except Exception as err:
        print err






if __name__ == '__main__':
    try:
        rospy.init_node("image")
        rospy.loginfo('optical_flow start')
        rospy.Subscriber("/tello/image_raw/h264", Image, callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass