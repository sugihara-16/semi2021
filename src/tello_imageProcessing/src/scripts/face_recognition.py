#!/usr/bin/env python 
# license removed for brevity
# -*- coding: utf-8 -*-

from re import I
import rospy
from std_msgs.msg import String
from std_msgs.msg import Empty
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist
import math
import time
from opencv_apps.msg import FaceArrayStamped 

pre_x = 0
pre_y = 0
count = 0
count2 = 0

def callback(msg):
    global pre_x
    global pre_y
    global count
    global count2

    commands = {
        'takeoff' : [None, '/tello/takeoff', Empty],
        'land' : [None, '/tello/land',Empty],
        'emergency' : [None, '/tello/emergency', Empty],
        'fast_mode' : [None, '/tello/fast_mode', Empty],
        'flattrim' : [None, '/tello/flattrimm', Empty],
        'flip' : [None, '/tello/flip', UInt8],
        'palm_land' : [None, '/tello/palm_land', Empty],
        'throw_takeoff' : [None, '/tello/throw_takeoff', Empty], 
        'position' : [None, '/tello/cmd_vel', Twist]

    }
    #pub = rospy.Publisher(topic, type, queue_size=10)
    

    try:
        if count2 == 0:
            pub = rospy.Publisher('/tello/takeoff',Empty, queue_size=10)
            pub.publish()
            pub.publish()
            count2 += 1
        twist = Twist()
        pub = rospy.Publisher('/tello/cmd_vel', Twist, queue_size=10)


        if msg.rects:
            face = msg.rects
            x = face[0]
            y = face[1]
            center_x = 480
            center_y = 360

            if count == 0:
                pre_x = center_x - x
                pre_y = center_y - y
                count += 1

            #P_gain
            Kp = 10
            #I_gain
            Ki = 1
            #D_gain
            Kd = 10

            dt = 0.06

            p_x = center_x - x
            i_x = p_x*dt
            d_x = (p_x-pre_x)/dt

            p_y = center_y - y
            i_y = p_y*dt
            d_y = (p_y-pre_y)/dt


            twist.linear.x = Kp*p_x + Ki*i_x + Kd*d_x
            twist.linear.y = Kp*p_y + Ki*i_y + Kd*d_y

            pre_x = pre_x - twist.linear.x*dt
            pre_y = pre_y - twist.linear.y*dt

            pub.publish(twist) 

        else:
            count = 0
            twist.angular.z = 20.0
            pub.publish(twist)
            

            
    except Exception as err:
        print err

if __name__ == '__main__':
    try:
        rospy.init_node('FR_Control')
        rospy.loginfo('FR_Control starts')
        rospy.Subscriber('/face_recognition/output', FaceArrayStamped, callback)
        rospy.spin()
    except rospy.ROSInterruptException:
        pub = rospy.Publisher('/tello/land',Empty, queue_size=10)
        pub.publish()
        pub.publish()
        pass
