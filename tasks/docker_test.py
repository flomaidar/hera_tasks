#!/usr/bin/env python

# import traceback
import rospy
# import math
import json
# import time
# import tf

from std_msgs.msg import UInt32
# from gsr_ros.msg import Opcs
# from gsr_ros.srv import StartRequest
from social_worlds.srv import *

from Actions import Actions

class Task():
    def __init__(self):
        rospy.init_node('Task')
        rospy.sleep(1)
        # listener = tf.TransformListener()

        #set vizbox story and publisher
        rospy.set_param('/story/title', 'Receptionist')
        rospy.set_param('/story/storyline', [])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        #Task Variables
        actions = Actions()
        robotnames = ['Robot', 'Hera', 'Zeus']
        locals = json.loads(actions.question('know_places').result)
        specs = [
            '<robotnames>',
            'Start task'
        ]

        #Task init
        # actions.talk('Hello! My name is HERA.')
        # actions.talk('This is a test in docker environment')
        
       
        for i in range(3):
            actions.move('spin_right', seconds=1.0)
        for i in range(2):
            actions.move('spin_left', seconds=1.0)

if __name__ == "__main__":
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass