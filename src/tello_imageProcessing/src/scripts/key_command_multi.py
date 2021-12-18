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
    pub_3_takeoff =rospy.Publisher ('/tello3/takeoff', Empty, queue_size = 10)
    pub_1_land =rospy.Publisher ('/tello1/land', Empty, queue_size = 10)
    pub_2_land =rospy.Publisher ('/tello2/land', Empty, queue_size = 10)
    pub_3_land =rospy.Publisher ('/tello3/land', Empty, queue_size = 10)
    pub_1_cmd_vel = rospy.Publisher('/tello1/cmd_vel', Twist, queue_size = 10)
    pub_2_cmd_vel = rospy.Publisher('/tello2/cmd_vel', Twist, queue_size = 10)
    pub_3_cmd_vel = rospy.Publisher('/tello3/cmd_vel', Twist, queue_size = 10)

    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        
        cm = raw_input('INPUT COMMAND : ')

        if cm == 'takeoff': 
            pub_1_takeoff.publish()
            pub_2_takeoff.publish()
            pub_3_takeoff.publish()

        elif cm == 'land':
            pub_1_land.publish()
            pub_2_land.publish()
            pub_3_land.publish()
        elif any(chr.isdigit() for chr in cm): # other
            cm_list = cm.split()
            type = cm_list[0]   # linear or angular
            dire = cm_list[1]   # direction
            timer = float(cm_list[2])  # time

            twist1 = Twist()
            twist2 = Twist()
            twist3 = Twist()
            if cm_list[0] == 'l':   # linear
                velo =  5* (timer/abs(timer))
                t = timer

                if cm_list[1] == 'x':
                    twist1.linear.x = twist2.linear.x=twist3.linear.x= velo
                elif cm_list[1] == 'y':
                    twist1.linear.y =  twist2.linear.y = twist3.linear.y=velo
                elif cm_list[1] == 'z':
                    twist1.linear.z =twist2.linear.z = twist3.linear.z = velo
                pub_1_cmd_vel.publish(twist1)
                pub_2_cmd_vel.publish(twist2)
                pub_3_cmd_vel.publish(twist3)
                time.sleep(abs(t))
                twist1.linear.x = twist1.linear.y = twist1.linear.z = 0.0
                twist2.linear.x = twist2.linear.y = twist2.linear.z = 0.0
                twist3.linear.x = twist3.linear.y = twist3.linear.z = 0.0
                pub_1_cmd_vel.publish(twist1)
                pub_2_cmd_vel.publish(twist2)
                pub_3_cmd_vel.publish(twist3)
            elif cm_list[0] == 'a':   # angular
                l = 60
                velo = 100 * (timer/abs(timer))
                t = timer
             
                twist1.angular.z = velo
                twist2.angular.z = velo
                twist1.linear.x = -velo
                twist2.linear.x = 0
            
                pub_1_cmd_vel.publish(twist1)
                pub_2_cmd_vel.publish(twist2)
                time.sleep(abs(t))
                twist1.angular.x = twist1.angular.y = twist1.angular.z = 0.0
                twist2.angular.x = twist2.angular.y = twist2.angular.z = 0.0
                twist1.linear.x = twist1.linear.y = twist1.linear.z = 0.0
                twist2.linear.x = twist2.linear.y = twist2.linear.z = 0.0
                pub_1_cmd_vel.publish(twist1)
                pub_2_cmd_vel.publish(twist2)
            

        r.sleep()



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
