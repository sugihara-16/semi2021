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
count_2 = 0
count_3 = 0
limit_count = 0


class MultiTello():
    def __init__(self):
        rospy.init_node('multi_tello_flight')
        rospy.loginfo('activate')
        
        self.tello_flight_status = False
        self.tello_active = True
        self.ar_detect = False
        self.length = 0.7
        self.takeoff_1_pub = rospy.Publisher('/tello1/takeoff', Empty, queue_size = 10)
        self.takeoff_2_pub = rospy.Publisher('/tello2/takeoff', Empty, queue_size = 10)
        self.takeoff_3_pub = rospy.Publisher('/tello3/takeoff', Empty, queue_size = 10)
        self.land_1_pub = rospy.Publisher('/tello1/land', Empty, queue_size = 10)
        self.land_2_pub = rospy.Publisher('/tello2/land', Empty, queue_size = 10)
        self.land_3_pub = rospy.Publisher('/tello3/land', Empty, queue_size = 10)
        self.cmd_vel_1_pub = rospy.Publisher('/tello1/cmd_vel', Twist, queue_size = 10)
        self.cmd_vel_2_pub = rospy.Publisher('/tello2/cmd_vel', Twist, queue_size = 10)
        self.cmd_vel_3_pub = rospy.Publisher('/tello3/cmd_vel', Twist, queue_size = 10)
        self.count = 0
        self.ar_sub = rospy.Subscriber('/ar_pose_marker',AlvarMarkers,self.callback)

    def callback(self, msg):
        global count_2,count_3,limit_count
        ar_markers = msg.markers
        ar_pose = [0,0,0]
        for i, item in enumerate(ar_markers):
            if item.id == 0:
                ar_pose[0] = item
            if item.id == 1:
                ar_pose[1] = item
            if item.id == 2:
                ar_pose[2] = item
                
        twist1 = Twist()
        twist2 = Twist()
        twist3 = Twist()
        self.cmd_vel_2_pub.publish(twist2)
        self.cmd_vel_3_pub.publish(twist3)
        if not (self.tello_flight_status) and (self.tello_active):
            self.takeoff_1_pub.publish()
            self.takeoff_2_pub.publish()
            self.takeoff_3_pub.publish()
            self.tello_flight_status = True

        """
        if not ar_pose:
            limit_count += 1
            if limit_count > 10:
                twist = Twist()
                velo = 3/math.pi
                twist.angular.z = velo
                self.cmd_vel_pub.publish(twist)
        if limit_count == 40:
                self.land_pub.publish()
                self.tello_active = False
                limit_count = 0
        """
        rospy.loginfo("detected")
        z2 = 0.9
        x2 = 0.25
        rospy.loginfo(x2)

        limit_count += 1
        rospy.loginfo(limit_count)
        
        #tello2
        if ar_pose[0]:
           
            pose = ar_pose[0].pose.pose
            position = pose.position
            px2 = position.x
            py2 = position.y
            pz2 = position.z    
            

            if (count_2 > 1) and( limit_count > 30):
                rospy.loginfo('0found')
                count_2 = 0
                if (px2 < x2-0.05) or (x2+0.05 < px2):
                    velo = 0.2 * (px2-x2)/abs(px2-x2)*-1
                    twist2.linear.x = velo
                    rospy.loginfo("px2 = %f",px2)
                    rospy.loginfo("vx2= %f",velo)
                if py2 < -0.25 or -0.05  < py2:
                    twist2.linear.z = 0.2 * (py2+0.15)/abs(py2+0.15)  
                    rospy.loginfo("py2 = %f",py2)
                    rospy.loginfo("vz2 = %f",twist2.linear.z)
                if (pz2 < z2-0.1)  or (z2+0.1 < pz2):
                    twist2.linear.y = 0.2 * (pz2-0.9)/abs(pz2-0.9)*-1
                    rospy.loginfo("pz2 = %f",pz2)
                    rospy.loginfo("vy2 = %f",twist2.linear.y)
                self.cmd_vel_2_pub.publish(twist2)
            count_2 += 1

        #tello3
        if ar_pose[1]:
            pose = ar_pose[1].pose.pose
            position = pose.position
            px3 = position.x
            py3 = position.y
            pz3 = position.z    
                

            if( count_3 > 1) and(limit_count > 30):
                count_3 = 0
                if (px3 < -x2-0.05) or (-x2+0.05 < px3):
                    velo = 0.2 * (px3+x2)/abs(px3+x2)*-1
                    twist3.linear.x = velo
                    rospy.loginfo("px3 = %f",px3)
                    rospy.loginfo("vx3= %f",velo)
                if py3 < -0.25 or -0.05  < py3:
                    twist3.linear.z = 0.2 * (py3+0.15)/abs(py3+0.15)  
                    rospy.loginfo("py3 = %f",py3)
                    rospy.loginfo("vz3 = %f",twist3.linear.z)
                if (pz3 < z2-0.1)  or (z2+0.1 < pz3):
                    twist3.linear.y = 0.2 * (pz3-0.8)/abs(pz3-0.8)*-1
                    rospy.loginfo("pz3 = %f",pz3)
                    rospy.loginfo("vy3 = %f",twist3.linear.y)
                self.cmd_vel_3_pub.publish(twist3)
            count_3 += 1
                        
            
            
            
if __name__=="__main__":
    try:
        multi_tello = MultiTello();
        rospy.spin()
    except rospy.ROSInterruptException: pass