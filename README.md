# ROS-scripts / Robot used : Turtlebot3 Burger

Extract data from rosbagfiles / Suggestion to resolve Bug related to SLAM 

files description : 

extract_images.py : Extraction of compressed images recorded by a raspicam camera fixed on Turtlebot3 Burger robot.

Reformat_data.py : Extraction of data from AMCL, SCAN and Image rostopics into csv files (script to process these recorded data will be added soon).

Odom_Correction.py : I applied SLAM (Simultaneous Localization and Mapping) in order to record data published on AMCL topic (amcl is a probabilistic localization system for a robot moving in 2D). For research purposes, I allowed the robot to make collisions. However, I have noticed that the approximated map was moving while the robot remains in the same position due to an obstacle. In fact the wheels were still running so that informaion published on /odom topic was modified. The drawing below explains the link between odom and amcl :

![alt text](https://github.com/marwa9/ROS-scripts/blob/master/odometry_localization.PNG)

Reference [http://wiki.ros.org/amcl]

So what i decided to do is to create a subscriber to /scan topic to detect collisions and publisher on the /odom topic that is responsible of keeping /odom data unmodified in case of collisions. 
