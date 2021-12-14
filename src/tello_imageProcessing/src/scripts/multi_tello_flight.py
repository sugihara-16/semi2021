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
count = 0
limit_count = 0


class MultiTello():
    def __init__(self):
        rospy.init_node('multi_tello_flight')
        rospy.loginfo('activate')
        
        self.tello_flight_status = False
        self.tello_active = True
        self.ar_detect = False
        self.takeoff_1_pub = rospy.Publisher('/tello1/takeoff', Empty, queue_size = 10)
        self.takeoff_2_pub = rospy.Publisher('/tello2/takeoff', Empty, queue_size = 10)
        self.land_1_pub = rospy.Publisher('/tello1/land', Empty, queue_size = 10)
        self.land_2_pub = rospy.Publisher('/tello2/land', Empty, queue_size = 10)
        self.cmd_vel_1_pub = rospy.Publisher('/tello1/cmd_vel', Twist, queue_size = 10)
        self.cmd_vel_2_pub = rospy.Publisher('/tello2/cmd_vel', Twist, queue_size = 10)
        self.count = 0
        self.ar_sub = rospy.Subscriber('/ar_pose_marker',AlvarMarkers,self.callback)

    def callback(self, msg):
        global count,limit_count
        ar_pose = msg.markers
        twist = Twist()
        if not (self.tello_flight_status) and (self.tello_active):
            self.takeoff_1_pub.publish()
            self.takeoff_2_pub.publish()
            self.tello_flight_status = True
        if not ar_pose:
            limit_count += 1
            """
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
        else:
            rospy.loginfo("detected")
            pose = ar_pose[0].pose.pose
            position = pose.position
            px = position.x
            py = position.y
            pz = position.z    
            twist.linear.x = 0
            twist.linear.y = 0
            twist.linear.z = 0
            twist.angular.x = twist.angular.y = twist.angular.z = 0.0
            self.cmd_vel_2_pub.publish(twist)
            rospy.loginfo(count)
            if count == 10:
                count = 0
                if px < -0.1 or 0.1 < px:
                    velo = 1 * (px)/abs(px)*-1
                    twist.linear.x = velo
                    rospy.loginfo("px = %f",px)
                    rospy.loginfo("vx= %f",velo)
                if py < -0.07 or 0.07 < py:
                    twist.linear.z = 1 * (py)/abs(py) 
                    rospy.loginfo("py = %f",py)
                    rospy.loginfo("vz = %f",twist.linear.z)
                if pz < 0.8 or 1.2 < pz:
                    twist.linear.y = 1 * (pz-1.0)/abs(pz-1.0)*-1
                    rospy.loginfo("pz = %f",pz)
                    rospy.loginfo("vy = %f",twist.linear.y)
                self.cmd_vel_2_pub.publish(twist)
            count += 1
            limit_count = 0
                
                
                
            
            
            
if __name__=="__main__":
    try:
        multi_tello = MultiTello();
        rospy.spin()
    except rospy.ROSInterruptException: pass
