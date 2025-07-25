#!/usr/bin/env python3

import rospy
import pyrealsense2 as rs
import numpy as np
import cv2

from cv_bridge import CvBridge
from sensor_msgs.msg import Image

def main():
    rospy.init_node('realsense', anonymous=True)
    pub = rospy.Publisher('/camera/color/image_raw', Image, queue_size=10)
    bridge = CvBridge()

    # Configure RealSense pipeline
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    # Start camera
    pipeline.start(config)
    rospy.loginfo("RealSense camera started...")

    rate = rospy.Rate(30)  # Hz

    try:
        while not rospy.is_shutdown():
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            # Convert to NumPy array
            color_image = np.asanyarray(color_frame.get_data())

            # Convert to ROS Image message
            ros_image = bridge.cv2_to_imgmsg(color_image, encoding="bgr8")

            # Publish
            pub.publish(ros_image)

            rate.sleep()
    except rospy.ROSInterruptException:
        pass
    finally:
        pipeline.stop()
        rospy.loginfo("Stopped RealSense pipeline.")

if __name__ == '__main__':
    main()
