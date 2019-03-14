#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: Marwa Kechaou

"""

import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry


class Odom:
    def __init__(self):
        #rospy.init_node('oodometry', anonymous=True) #make node 
        self.x = np.array([0,0])
        self.y = np.array([0,0])
        self.z= np.array([0,0])
        self.vx= np.array([0,0])
        self.vy= np.array([0,0])
        self.vz= np.array([0,0])
        self.odom = Odometry()

    def odometryCb(self,msg1):
        self.x[1] = msg1.pose.pose.position.x 
        self.y[1] = msg1.pose.pose.position.y 
        self.z[1] = msg1.pose.pose.position.z 
        self.vx[1] = msg1.twist.twist.linear.x 
        self.vy[1] = msg1.twist.twist.linear.y 
        self.vz[1] = msg1.twist.twist.angular.z 
        

    def callback(self,msg2):
        if (msg2.ranges[0] < 0.05) : #or (msg2.ranges[180] < 0.03) :
            self.odom.pose.pose.position.x = self.x[0]
            self.odom.pose.pose.position.y = self.y[0]
            self.odom.pose.pose.position.z = self.z[0]
            self.odom.twist.twist.linear.x = self.vx[0]
            self.odom.twist.twist.linear.y = self.vy[0]
            self.odom.twist.twist.angular.z = self.vz[0]
            self.pub.publish(self.odom)
        else :
            self.x[0] = self.x[1] 
            self.y[0] = self.y[1]
            self.z[0] = self.z[1] 
            self.vx[0] = self.vx[1] 
            self.vy[0] = self.vy[1] 
            self.vz[0] = self.vz[1] 
            
    def Correct_Odom(self):
        while not rospy.is_shutdown():
            rospy.Subscriber('odom',Odometry,self.odometryCb)
            self.sub = rospy.Subscriber('/scan', LaserScan, self.callback) # Create a Subscriber to the /scan topic
            self.pub = rospy. Publisher('/odom', Odometry, queue_size=10)# Create a publisher on the /odom topic
            self.odom = Odometry()
            rospy.spin()

if __name__ == '__main__':
    odom = Odom()
    odom.Correct_Odom()
