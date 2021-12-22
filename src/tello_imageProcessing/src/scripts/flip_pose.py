#!/usr/bin/env python                                                                           
import rospy
from geometry_msgs.msg import Point
from std_msgs.msg import String
from std_msgs.msg import Empty
from std_msgs.msg import UInt8
from geometry_msgs.msg import Twist
from jsk_recognition_msgs.msg import PeoplePoseArray
import time
import math


class ThrowTrash():
    def __init__(self):
        rospy.init_node('trash_throwing')
        rospy.loginfo('activate')
        self.flip_count = 0
        self.land_count = 0
        self.flip = False
        self.detection = False
        self.goal = False
        self.move_count =0
        self.cmd_vel_1_pub = rospy.Publisher('/tello1/cmd_vel', Twist, queue_size = 10)
        self.cmd_vel_2_pub = rospy.Publisher('/tello2/cmd_vel', Twist, queue_size = 10)
        self.cmd_vel_3_pub = rospy.Publisher('/tello3/cmd_vel', Twist, queue_size = 10)
        self.count = 0
        self.pose_sub = rospy.Subscriber('/edgetpu_human_pose_estimator/output/poses', PeoplePoseArray, self.pose_cb)
        self.flip_sub = rospy.Subscriber('/throwing',String, self.flip_cb)
        self.land_1_pub = rospy.Publisher('/tello1/land', Empty, queue_size = 10)
        self.land_2_pub = rospy.Publisher('/tello2/land', Empty, queue_size = 10)
        self.land_3_pub = rospy.Publisher('/tello3/land', Empty, queue_size = 10)
        self.flip_1_pub = rospy.Publisher('/tello1/flip', UInt8, queue_size = 10)
        self.flip_2_pub = rospy.Publisher('/tello2/flip', UInt8, queue_size = 10)
        self.flip_3_pub = rospy.Publisher('/tello3/flip', UInt8, queue_size = 10)

    def pose_cb(self, msg):
        right_wrist = (False, 0)
        right_shoulder = (False, 0)
        left_wrist = (False,0)
        left_shoulder = (False,0)
        nose = (False,0)

        center_x = 480
        center_y = 360

        if msg.poses:
            rospy.loginfo('stanby')
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
            if left_wrist[0]:
                left_wrist_pos = pose[left_wrist[1]].position
            if right_shoulder[0]:
                right_shoulder_pos = pose[right_shoulder[1]].position
            if left_shoulder[0]:
                left_shoulder_pos = pose[left_shoulder[1]].position
        
            if right_wrist[0] and right_shoulder[0] and ( right_wrist_pos.y < right_shoulder_pos.y):
                self.flip_count += 1
                rospy.loginfo(self.flip_count)
                if self.flip_count > 30:
                    rospy.loginfo('flip')
                    self.flip_1_pub.publish(2)
                    self.flip_2_pub.publish(2)
                    self.flip_3_pub.publish(2)
                    self.flip_count = 0
            else:
                self.flip_count = 0

            if left_wrist[0] and left_shoulder[0] and ( left_wrist_pos.y < left_shoulder_pos.y):
                self.land_count += 1
                rospy.loginfo(self.land_count)
                if self.land_count > 30:
                    rospy.loginfo('land')
                    self.land_pub.publish()
                    self.flight_status = False
                    self.land_count = 0
            else:
                self.land_count = 0
                
        
    def flip_cb(self, msg):
        trash = msg.data
        if trash == 'flip':
            self.move_count += 1
            if self.move_count > 150:
                rospy.loginfo('flip stanby')
                self.flip = True
        
                
                        
                
        
              
if __name__=="__main__":
    try:
        trash_throw = ThrowTrash()
        rospy.spin()
    except rospy.ROSInterruptException: pass
