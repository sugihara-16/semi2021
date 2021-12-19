#!/usr/bin/env python
# license removed for brevity
from re import I
import rospy
from std_msgs.msg import String
from std_msgs.msg import Empty
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist
from jsk_recognition_msgs.msg import PeoplePoseArray
import math
import time

class ThrowDetection():
    def __init__(self):
        rospy.init_node('throw_detector', anonymous=True)

        self.flight_status = False
        
        self.pose_sub = rospy.Subscriber('/edgetpu_human_pose_estimator/output/poses', PeoplePoseArray, self.pose_callback)
        self.takeoff_pub =rospy.Publisher('/tello1/takeoff', Empty, queue_size=1)
        self.land_pub = rospy.Publisher('/tello1/land', Empty, queue_size=11)
                
       


    def pose_callback(self,msg):
        right_wrist = (False, 0)
        right_shoulder = (False, 0)
        left_wrist = (False,0)
        left_shoulder = (False,0)
        nose = (False,0)

        center_x = 480
        center_y = 360


        if msg.poses:
            poses = msg.poses
            limb_names = poses[0].limb_names
            pose = poses[0].poses
            for i,item in enumerate(limb_names):
                if item == 'right wrist':
                    right_wrist = (True,i)
                elif item == 'right shoulder':
                    right_shoulder = (True,i)
                elif item == 'left wrist':
                    left_wrist = (True,i)
                elif item == 'left shoulder':
                    left_shoulder = (True,i)
        
            if right_wrist[0]:
                right_wrist_pos = pose[right_wrist[1]].position
                rospy.loginfo(right_wrist_pos.y)
            if left_wrist[0]:
                left_wrist_pos = pose[left_wrist[1]].position
            if right_shoulder[0]:
                right_shoulder_pos = pose[right_shoulder[1]].position
            if left_shoulder[0]:
                left_shoulder_pos = pose[left_shoulder[1]].position
        
            if right_wrist[0] and right_shoulder[0] and ( right_wrist_pos.y < right_shoulder_pos.y):
                rospy.loginfo('takeoff')
                self.takeoff_pub.publish()
                self.flight_status = True

            if left_wrist[0] and left_shoulder[0] and ( left_wrist_pos.y < left_shoulder_pos.y):
                rospy.loginfo('land')
                self.land_pub.publish()
                self.flight_status = False

            
        



if __name__ == '__main__':
    try:
       throw =  ThrowDetection()
       rospy.spin()
        
    except rospy.ROSInterruptException: pass
