#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: marwa.kechaou
"""

import os
import rosbag
import cv2
from cv_bridge import CvBridge
import pandas as pd
import threading


class Reformat:
    def __init__(self):
        self.filename1 = "amcl_pose.csv"
        self.filename2 = "scan.csv"
        self.filename3 = "compressed_image.csv"
        # Create a dict for rostopics to extract 
        self.rostopics = {"amcl_pose":"/amcl_pose","scan":"/scan","image":"/raspicam_node/image/compressed"}
        self.count = 0

    @staticmethod
    def create_databases_folders(path):
        df_amcl = pd.DataFrame(columns=['S','Nsecs','X', 'Y','Orien_z','Orien_w'])
        df_amcl.to_csv(os.path.join(path,"amcl_pose.csv"), decimal=',', sep=',')
        df_scan = pd.DataFrame(columns=['S','Nsecs','ranges'])
        df_scan.to_csv(os.path.join(path,"scan.csv"), decimal=',', sep=',')
        df_image = pd.DataFrame(columns=['S','Nsecs'])
        df_image.to_csv(os.path.join(path,"compressed_image.csv"), decimal=',', sep=',')
        
        
    """ AMCL """
    @staticmethod
    def amcl(msg,filewriter,rostopic="/amcl_pose"):
        if rostopic == "/amcl_pose":
            new_row = pd.DataFrame([[msg.header.stamp.secs,msg.header.stamp.nsecs,msg.pose.pose.position.x,
                                     msg.pose.pose.position.y,msg.pose.pose.orientation.z,
                                     msg.pose.pose.orientation.w]],columns = ['S','Nsecs','X', 'Y','Orien_z','Orien_w'])
            new_row.to_csv(filewriter, header=False)
    
    """ Lidar Data """
    @staticmethod
    def scan(msg,filewriter,rostopic="scan.csv"):
        if rostopic == "/scan":      
            new_row = pd.DataFrame([[msg.header.stamp.secs,msg.header.stamp.nsecs,msg.ranges]],
                                   columns = ['S','Nsecs','ranges'])
            new_row.to_csv(filewriter, header=False)
    
    """ Image Data """
    @staticmethod
    def Image(first_path,path,bridge,msg,filewriter,count,rostopic="compressed_image.csv"):
        if rostopic == "/raspicam_node/image/compressed":
            new_row = pd.DataFrame([[msg.header.stamp.secs,msg.header.stamp.nsecs]],columns = ['S','Nsecs'])
            new_row.to_csv(filewriter, header=False)
            cv_img = bridge.compressed_imgmsg_to_cv2(msg)
            new_path = os.path.join(first_path,'images')
            cv2.imwrite(os.path.join(new_path,"%06i.jpg" % count), cv_img)
            
    def get_filename(self,topic_name):
        if topic_name=="/amcl_pose":
            return self.filename1
        elif topic_name=="/scan":
            return self.filename2
        else:
            return self.filename3
        
    def thread(self,first_path,path,bagFile,df):
        rostopics = list(self.rostopics.values())
        p1 = threading.Thread(target=self.extraction,args=(first_path,path,bagFile,df,rostopics[0]))
        p2 = threading.Thread(target=self.extraction,args=(first_path,path,bagFile,df,rostopics[1]))
        p3 = threading.Thread(target=self.extraction,args=(first_path,path,bagFile,df,rostopics[2]))
        
        p1.start()
        p2.start()
        p3.start()
            
        p1.join()
        p2.join()
        p3.join()        
          
    def extraction(self,first_path,path,bagFile,df,i):
        filename = os.path.join(path,self.get_filename(i))
        with open(filename, 'a') as f:
            with rosbag.Bag(os.path.join(path,bagFile), "r") as bag:
                for topic, msg, timestamp in bag.read_messages(topics=i):
                    if (msg.header.stamp.secs>=int(df['Start'])) & (msg.header.stamp.secs<=int(df['Stop'])):
                        self.amcl(msg,f,i)
                        self.scan(msg,f,i)
                        self.Image(first_path,path,CvBridge(),msg,f,self.count,i)
                    
                        self.count += 1               
    
    def main(self,path):    
        with open(os.path.join(path,'begin_stop_extraction.csv'), 'r') as f:
            df_bs = pd.read_csv(f,decimal=",") # bs => begin stop
        folders = []
        for dirname, dirnames,_ in os.walk(path): 
            if dirname == path:
                folders = dirnames
                break
            
        # Create a folder for images
        if not os.path.exists(os.path.join(path,'images')):
            os.makedirs(os.path.join(path,'images'))
        first_path = os.path.join(path,'images')
        
        for i in folders:
            if i!='images' :
                path_subfolder = os.path.join(path,i)
                ListofBagFiles = [f for f in os.listdir(path_subfolder) if f[-4:] == ".bag"]
                self.create_databases_folders(path_subfolder)
                self.thread(first_path,path_subfolder,ListofBagFiles[0],df_bs[df_bs['Name Folder']==i])
        
if __name__ == '__main__' :
    path = "store_data_path"  
    reformat = Reformat()
    reformat.main(path)
