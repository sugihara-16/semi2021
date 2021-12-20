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
import numpy as np

class ThrowDetection():
    def __init__(self):
        rospy.init_node('throw_detector', anonymous=True)

        self.flight_status = False
        self.clock = 200
        self.clock_switch = False

        self.right_wrist_motion_x = []
        self.right_wrist_motion_y = []
        
        self.pose_sub = rospy.Subscriber('/edgetpu_human_pose_estimator/output/poses', PeoplePoseArray, self.pose_callback)
        self.throw_pub = rospy.Publisher('/throwing', String , queue_size=10)
                
       


    def pose_callback(self,msg):
        right_wrist = (False, 0)
        right_shoulder = (False, 0)
        self.throw_pub.publish('')

        if msg.poses:
            poses = msg.poses
            limb_names = poses[0].limb_names
            pose = poses[0].poses
            for i,item in enumerate(limb_names):
                if item == 'right wrist':
                    right_wrist = (True,i)
                elif item == 'right shoulder':
                    right_shoulder = (True,i)
            
            if right_wrist[0]:
                right_wrist_pos = pose[right_wrist[1]].position
                self.right_wrist_motion_x.append(right_wrist_pos.x)
                self.right_wrist_motion_y.append(right_wrist_pos.y)
            if len(self.right_wrist_motion_x) == 30:
                del self.right_wrist_motion_x[0]
                del self.right_wrist_motion_y[0]
            if len(self.right_wrist_motion_x) > 10:
                x_max_pos_ind = np.argmax(np.array(self.right_wrist_motion_x))
                x_min_pos_ind = np.argmin(np.array(self.right_wrist_motion_x))

                x_max = self.right_wrist_motion_x[x_max_pos_ind]
                y_at_max = self.right_wrist_motion_y[x_max_pos_ind] 
                x_min = self.right_wrist_motion_x[x_min_pos_ind]
                y_at_min = self.right_wrist_motion_y[x_min_pos_ind]
                
                if (abs(x_max - x_min) > 200) and (y_at_max > y_at_min) and (self.clock >=200):
                   rospy.loginfo('left throw!!')
                   self.throw_pub.publish('left')
                   self.right_wrist_motion_x = []
                   self.right_wrist_motion_y = []
                   self.clock_switch = True
                   self.clock = 0
                   
                if (abs(x_max - x_min) > 200) and (y_at_max < y_at_min) and (self.clock >= 200):
                   rospy.loginfo('rigth throw!!')
                   self.throw_pub.publish('right')
                   self.right_wrist_motion_x = []
                   self.right_wrist_motion_y = []
                   self.clock_switch = True
                   self.clock = 0

        if self.clock_switch:
            self.clock += 1
                   
                
                
                    
if __name__ == '__main__':
    try:
       throw =  ThrowDetection()
       rospy.spin()
        
    except rospy.ROSInterruptException: pass
