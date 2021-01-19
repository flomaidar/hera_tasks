#!/usr/bin/env python

import math
import time
import rospy
import json
import traceback
from random import randint

from std_msgs.msg import UInt32

from Actions import Actions

from agent.util.enuns import Side

class PingPong():
    def __init__(self):

        rospy.set_param('/story/title', 'Pingpong task')
        rospy.set_param('/story/storyline', ['Ping pong'])

        self.pub_vizbox_step = rospy.Publisher('/ping_step', UInt32, queue_size=80)

        actions = Actions()

        actions.goto('entrance')

        while True:
            actions.goto('kitchen')
            time.sleep(2)
            actions.goto('living_room')
            time.sleep(2)
            actions.goto('office')
            time.sleep(2)
            actions.goto('bedroom')
            time.sleep(2)    

if __name__ == "__main__":
    try:
        rospy.init_node('Task')
        PingPong()
    except KeyboardInterrupt:
        pass
