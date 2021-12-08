#!/usr/bin/env python
import rospy
import sys
import cv2
from sensor_msgs.msg import Image, CompressedImage, CameraInfo
from cv_bridge import CvBridge, CvBridgeError
import numpy as np


def callback(msg):
    bridge = CvBridge()
    image_pub = rospy.Publisher('/image_transport/image_raw', Image, queue_size=1) 

    try:
        np_arr = np.fromstring(msg.data, np.uint8)
        input_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    except CvBridgeError, e:
        print e


    image_pub.publish(bridge.cv2_to_imgmsg(input_image, "bgr8"))

if __name__ == '__main__':
    rospy.init_node('compressed_image_transporter')
    rospy.Subscriber('/tello/image_raw/compressed', CompressedImage, callback)
    
    rospy.spin()