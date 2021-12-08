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

    rospy.init_node('controler', anonymous=True)

    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        
        cm = raw_input('INPUT COMMAND : ')

        for i in commands:
            if cm == i: # Empty Type
                topic = commands[cm][1]
                type = commands[cm][2]
                pub = rospy.Publisher(topic, type, queue_size=10)
                pub.publish()
                break

            elif 'flip' in cm:  #flip
                cm_list = cm.split()
                pub = rospy.Publisher('/tello1/flip', UInt8, queue_size=10)
                pub.publish(int(cm_list[1]) )
                print("flip")
                break

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
                    pub = rospy.Publisher('/tello1/cmd_vel', Twist, queue_size=10)
                    pub.publish(twist)
                    time.sleep(t)
                    twist.linear.x = twist.linear.y = twist.linear.z = 0.0
                    pub.publish(twist)
                    break

        
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
        r.sleep()

def callback(msg):
    global pid_switch
    global count
    count += 1

    

    if msg.rects:
        face = msg.rects
        rospy.loginfo(face)
        rospy.loginfo(count )
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

        if (-10<dx<10) and (-10<dy<10) and (-20<dw<20):
            pid_switch = False
            twist.linear.x = twist.linear.z = twist.linear.y = 0.0
            pub.publish(twist)
        else:
            twist.linear.x = -dx*0.02
            twist.linear.z = dy*0.02
            twist.linear.y = -dy*0.02
            pub = rospy.Publisher('/tello/cmd_vel', Twist, queue_size=10)
            pub.publish(twist)



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
