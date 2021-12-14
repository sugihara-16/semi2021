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


pid_switch = True
count = 0



def talker():
    rospy.init_node('controler', anonymous=True)
    global pid_switch
    commands = {
        'takeoff' : [None, '/tello1/takeoff', Empty],
        'land' : [None, '/tello1/land',Empty],
        'emergency' : [None, '/tello1/emergency', Empty],
        'fast_mode' : [None, '/tello1/fast_mode', Empty],
        'flattrim' : [None, '/tello1/flattrimm', Empty],
        'flip' : [None, '/tello1/flip', UInt8],
        'palm_land' : [None, '/tello1/palm_land', Empty],
        'throw_takeoff' : [None, '/tello1/throw_takeoff', Empty],
        'position' : [None, '/tello1/cmd_vel', Twist]

    }
    pub_1_takeoff =rospy.Publisher ('/tello1/takeoff', Empty, queue_size = 10)
    pub_2_takeoff =rospy.Publisher ('/tello2/takeoff', Empty, queue_size = 10)
    pub_1_land =rospy.Publisher ('/tello1/land', Empty, queue_size = 10)
    pub_2_land =rospy.Publisher ('/tello2/land', Empty, queue_size = 10)
    pub_1_cmd_vel = rospy.Publisher('/tello1/cmd_vel', Twist, queue_size = 10)
    pub_2_cmd_vel = rospy.Publisher('/tello2/cmd_vel', Twist, queue_size = 10)
    

    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        
        cm = raw_input('INPUT COMMAND : ')

        if cm == 'takeoff': 
            pub_1_takeoff.publish()
            pub_2_takeoff.publish()

        elif cm == 'land':
            pub_1_land.publish()
            pub_2_land.publish()
        elif any(chr.isdigit() for chr in cm): # other
            cm_list = cm.split()
            type = cm_list[0]   # linear or angular
            dire = cm_list[1]   # direction
            scale = float(cm_list[2])  # scale

            twist = Twist()

            if cm_list[0] == 'l':   # linear
                velo = 50.0 * (scale/abs(scale))
                t = scale/velo

                if cm_list[1] == 'x':
                    twist.linear.x = velo
                elif cm_list[1] == 'y':
                    twist.linear.y = velo
                elif cm_list[1] == 'z':
                    twist.linear.z = velo
                pub_1_cmd_vel.publish(twist)
                pub_2_cmd_vel.publish(twist)
                time.sleep(t)
                twist.linear.x = twist.linear.y = twist.linear.z = 0.0
                pub_1_cmd_vel.publish(twist)
                pub_2_cmd_vel.publish(twist)
                break
            """
            elif cm_list[0] == 'a':   # angular
                velo = 2/math.pi * (scale/abs(scale))
                t = (scale/180*math.pi)/velo
            
                if cm_list[1] == 'x':
                    twist.angular.x = velo
                elif cm_list[1] == 'y':
                    twist.angular.y = velo
                elif cm_list[1] == 'z':
                    twist.angular.z = velo
                pub = rospy.Publisher('/tello1/cmd_vel', Twist, queue_size=10)
                pub.publish(twist)
                time.sleep(t)
                twist.angular.x = twist.angular.y = twist.angular.z = 0.0
                pub.publish(twist)
                break
            """
        r.sleep()



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
