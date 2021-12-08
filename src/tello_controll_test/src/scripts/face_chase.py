#!/usr/bin/env python 
# license removed for brevity
from re import I
import rospy
from std_msgs.msg import String
from std_msgs.msg import Empty
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist
import math
import time
from opencv_apps.msg import FaceArrayStamped 
import cv2

pre_x = 0
pre_y = 0
count = 0

def callback(msg):
    global pre_x
    global pre_y
    global count

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

        twist = Twist()
        pub = rospy.Publisher('/tello/cmd_vel', Twist, queue_size=10)


        if msg.faces:
            face = msg.faces[0].face
            x = face.x
            y = face.y
            center_x = 300
            center_y = 250

            if count == 0:
                pre_x = center_x - x
                pre_y = center_y - y
                count += 1

            #Pゲイン
            Kp = 10
            #Iゲイン
            Ki = 1
            #Dゲイン
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

            pre_x = x - twist

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
        pass