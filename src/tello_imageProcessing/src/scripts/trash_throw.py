#!/usr/bin/env python                                                                           
import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import String
from std_msgs.msg import Empty
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist
from ar_track_alvar_msgs.msg import AlvarMarkers
import time
import math


class ThrowTrash():
    def __init__(self):
        rospy.init_node('trash_throwing')
        rospy.loginfo('activate')
        self.count = 0
        self.drop_count = 0
        self.move_count = 0
        self.trash = False
        self.detection = False
        self.goal = False
        self.cmd_vel_1_pub = rospy.Publisher('/tello1/cmd_vel', Twist, queue_size = 10)
        self.cmd_vel_2_pub = rospy.Publisher('/tello2/cmd_vel', Twist, queue_size = 10)
        self.cmd_vel_3_pub = rospy.Publisher('/tello3/cmd_vel', Twist, queue_size = 10)
        self.count = 0
        self.ar_sub = rospy.Subscriber('/ar_pose_marker',AlvarMarkers,self.ar_cb)
        self.trash_sub = rospy.Subscriber('/trash',String, self.trash_cb)
        self.land_1_pub = rospy.Publisher('/tello1/land', Empty, queue_size = 10)
        self.land_2_pub = rospy.Publisher('/tello2/land', Empty, queue_size = 10)
        self.land_3_pub = rospy.Publisher('/tello3/land', Empty, queue_size = 10)

    def ar_cb(self, msg):
        if not self.trash:
            return
        twist1 = Twist()
        twist2 = Twist()
        twist3 = Twist()
        self.cmd_vel_1_pub.publish(twist1)
        self.cmd_vel_2_pub.publish(twist2)
        self.cmd_vel_3_pub.publish(twist3)


        ar_markers = msg.markers
        for i, item in enumerate(ar_markers):
            if item.id == 2:
                self.detection = True
                ar_pose = item
                pose = ar_pose.pose.pose
                position = pose.position
                pxg = position.x
                pyg = position.y
                pzg = position.z
                if( self.count > 1) and (not self.goal):
                    self.count = 0
                    if (pxg < -0.1) or (0.1 < pxg):
                        velo = 0.5 * (pxg)/abs(pxg)
                        twist1.linear.x = velo
                        twist2.linear.x = velo
                        twist3.linear.x = velo
                    if pyg < -0.15 or -0.15  < pyg:
                        twist1.linear.z = 0.2 * (pyg)/abs(pyg)*-1  
                        twist2.linear.z = 0.2 * (pyg)/abs(pyg)*-1  
                        twist3.linear.z = 0.2 * (pyg)/abs(pyg)*-1
                    if (pzg < 1.7-0.15)  or (1.7+0.15 < pzg):
                        twist1.linear.y = 0.6 * (pzg-1.1)/abs(pzg-1.1)
                        twist2.linear.y = 0.6 * (pzg-1.1)/abs(pzg-1.1)
                        twist3.linear.y = 0.6 * (pzg-1.1)/abs(pzg-1.1)
                    self.cmd_vel_1_pub.publish(twist1)                    
                    self.cmd_vel_2_pub.publish(twist2)
                    self.cmd_vel_3_pub.publish(twist3)
                    if twist1.linear.x == 0 and twist1.linear.y == 0:
                        self.goal = True
                        rospy.loginfo('ok')
                self.count += 1
        if not self.detection:
            rospy.loginfo('recieved')
            twist1.linear.x = 0.6
            twist2.linear.x = 0.6
            twist3.linear.x = 0.6
            self.cmd_vel_1_pub.publish(twist1)
            self.cmd_vel_2_pub.publish(twist2)
            self.cmd_vel_3_pub.publish(twist3)
        if self.goal:
            self.drop_count += 1
            twist1.linear.z = 0.4
            self.cmd_vel_1_pub.publish(twist1)
            time.sleep(10)
            self.land_1_pub.publish()
            self.land_2_pub.publish()
            self.land_3_pub.publish()

    def trash_cb(self, msg):
        trash = msg.data
        if trash == 'Go':
            self.move_count += 1
            #rospy.loginfo('received')
            if self.move_count > 150:
                self.trash = True
        
                
                        
                
        
              
if __name__=="__main__":
    try:
        trash_throw = ThrowTrash()
        rospy.spin()
    except rospy.ROSInterruptException: pass
