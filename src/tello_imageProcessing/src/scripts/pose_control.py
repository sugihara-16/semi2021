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
        rospy.init_node('pose_control', anonymous=True)

        self.flight_status = False
        self.clock = 0
        self.throw_count = 0

        self.right_wrist_motion_x = []
        self.right_wrist_motion_y = []
        
        self.pose_sub = rospy.Subscriber('/edgetpu_human_pose_estimator/output/poses', PeoplePoseArray, self.pose_callback)
        self.throw_pub = rospy.Publisher('/throwing', String , queue_size=10)
                
       


    def pose_callback(self,msg):
        right_wrist = (False, 0)
        right_shoulder = (False, 0)
        self.throw_pub.publish('')

        if msg.poses and (self.clock >= 250):
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
            if len(self.right_wrist_motion_x) == 50:
                del self.right_wrist_motion_x[0]
                del self.right_wrist_motion_y[0]
            if len(self.right_wrist_motion_x) > 10:
                x_max_pos_ind = np.argmax(np.array(self.right_wrist_motion_x))
                x_min_pos_ind = np.argmin(np.array(self.right_wrist_motion_x))

                x_max = self.right_wrist_motion_x[x_max_pos_ind]
                y_at_max = self.right_wrist_motion_y[x_max_pos_ind] 
                x_min = self.right_wrist_motion_x[x_min_pos_ind]
                y_at_min = self.right_wrist_motion_y[x_min_pos_ind]
                
                if (abs(x_max - x_min) > 250) and (y_at_max > y_at_min):
                   rospy.loginfo('righ throw!!')
                   rospy.loginfo('x_max = %f',x_max)
                   rospy.loginfo('x_min = %f',x_min)
                   rospy.loginfo('y_at_max = %f', y_at_max)
                   rospy.loginfo('y_at_min = %f', y_at_min)
                   self.throw_pub.publish('left')
                   self.right_wrist_motion_x = []
                   self.right_wrist_motion_y = []
                   self.clock = 0
                   self.throw_count += 1
                   
                if (abs(x_max - x_min) > 250) and (y_at_max < y_at_min):
                   rospy.loginfo('left throw!!')
                   rospy.loginfo('x_max = %f',x_max)
                   rospy.loginfo('x_min = %f',x_min)
                   rospy.loginfo('y_at_max = %f', y_at_max)
                   rospy.loginfo('y_at_min = %f', y_at_min)
                   self.throw_pub.publish('right')
                   self.right_wrist_motion_x = []
                   self.right_wrist_motion_y = []
                   self.clock = 0
                   self.throw_count += 1
        if self.throw_count < 4:
            self.clock += 1
        else:
            self.throw_pub.publish('flip')
            rospy.loginfo('flip')
        if self.clock >= 250:
            rospy.loginfo('Ready!')
                
                
                    
if __name__ == '__main__':
    try:
       throw =  ThrowDetection()
       rospy.spin()
        
    except rospy.ROSInterruptException: pass
