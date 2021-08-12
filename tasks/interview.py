#!/usr/bin/env python

import traceback
import rospy
import math
import json
import time

from std_msgs.msg import UInt32
from gsr_ros.msg import Opcs
from gsr_ros.srv import StartRequest

from Actions import Actions

class Task():
    """docstring for Task"""
    def __init__(self):
        rospy.sleep(1)

        # set vizbox story and publisher
        rospy.set_param('/story/title', 'TakeOutTheGarbage')
        rospy.set_param('/story/storyline',[
            ])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        actions = Actions()

        # task variables
        robotnames = ['Robot','Hera','Ivy']
        locals = json.loads(actions.question('know_places').result)
        specs = [
            '<robotnames>',
            'Start task'
        ]

        # speech variables
        self.srv = StartRequest()
        self.srv.spec = specs
        self.srv.choices.append(Opcs(id="robotnames", values=robotnames))
        self.srv.choices.append(Opcs(id="locals", values=locals))


        ########################################################################
        ########################################################################

        while (True):
            actions.goto('starting_point')
            actions.talk('Bom dia Bruno')
            actions.goto('table')
            actions.manip("open")
            actions.manip("", x=0.35, y=0.0, z=0.1, rx=0.0, ry=0.0, rz=0.0)
            time.sleep(0.5)
            actions.manip("close")
            actions.manip("", x=0.15, y=0.0, z=0.2, rx=0.0, ry=0.0, rz=0.0)
            actions.goto('couch')
            actions.manip("", x=0.25, y=0.0, z=0.0, rx=0.0, ry=0.0, rz=0.0)
            actions.goto('end_point')

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
