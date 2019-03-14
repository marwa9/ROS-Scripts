#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: marwa.kechaou
"""

"""   Extract images from a rosbag  """

import string
import os
import time
import cv2
import shutil 

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import rosbag, csv


count = 0

for bagFile in listOfBagFiles:
	count += 1
	print "reading file " + str(count) + " of  " + numberOfFiles + ": " + bagFile

	""" access bag """
	bag = rosbag.Bag(bagFile)
	bagContents = bag.read_messages()
	bagName = bag.filename


	""" create a new directory """
	folder = string.rstrip(bagName, ".bag")
	try:	#else already exists
		os.makedirs(folder)
	except:
		pass
	shutil.copyfile(bagName, folder + '/' + bagName)


	""" get list of topics from the bag """
	listOfTopics = []
	for topic, msg, t in bagContents:
		if topic not in listOfTopics:
			listOfTopics.append(topic)
	
        for topicName in listOfTopics:
		if topicName == '/raspicam_node/image/compressed':	
    			bridge = CvBridge()
			count = 0
			for topic, msg, t in bag.read_messages(topicName):
	    			cv_img = bridge.compressed_imgmsg_to_cv2(msg)
				
            			cv2.imwrite("frame%06i.png" % count, cv_img)
	    			print "Wrote image %i" % count

	    			count += 1

	bag.close()

print "Done reading all " + numberOfFiles + " bag files."
