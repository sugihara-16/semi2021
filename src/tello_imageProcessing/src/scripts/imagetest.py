#!/usr/bin/env python
# license removed for brevity
from re import I
import rospy
from std_msgs.msg import String
from std_msgs.msg import Empty
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist
from jsk_recognition_msgs.msg import RectArray
import math
import time


def callback(msg):

    pub = rospy.Publisher('/tello/takeoff', Empty, queue_size=10)
    pub.publish()
    pub.publish()


    if msg.rects:
        face = msg.rects
        rospy.loginfo(face)
        face_x = face[0].x
        face_y = face[0].y
        face_width = face[0].width
        center_x = 480
        center_y = 360
        ref_width = 300
        dx = center_x - face_x
        dy = center_y - face_y
        dw = ref_width - face_width

        twist = Twist()
        pub = rospy.Publisher('/tello/cmd_vel', Twist, queue_size=10)

        if (-10<dx<10) and (-10<dy<10) and (-20<dw<20):
            pid_switch = False
            twist.linear.x = twist.linear.z = twist.linear.y = 0.0
            pub.publish(twist)
        else:
            twist.linear.x = -dx*0.02
            twist.linear.z = -dy*0.02
            twist.linear.y = dy*0.02
            pub.publish(twist)
            time.sleep(0.05)
            twist.linear.x = twist.linear.z = twist.linear.y = 0.0
            pub.publish(twist)



if __name__ == '__main__':
    try:
        rospy.init_node('controler', anonymous=True)
        rospy.Subscriber('/edgetpu_face_detector/output/rects', RectArray, callback)
        rospy.spin()
        
    except rospy.ROSInterruptException: pass