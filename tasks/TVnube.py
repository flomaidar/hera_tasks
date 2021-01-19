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
        rospy.set_param('/story/title', 'Demo')
        rospy.set_param('/story/storyline', [])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        actions = Actions()

        # task variables
        robotnames = ['Robot','Hera','Ivy']
        # locals = json.loads(actions.question('know_places').result)
        specs = [
            '<robotnames>',
            'go to <locals>',
            'Introduce yourself',
            'What is your name',
            'What is your teams called',
            'How much is two plus two',
            'Thank you'
        ]

        # speech variables
        self.srv = StartRequest()
        self.srv.spec = specs
        self.srv.choices.append(Opcs(id="robotnames", values=robotnames))
        # self.srv.choices.append(Opcs(id="locals", values=locals))

        ########################################################################
        ########################################################################

        actions.goto('start')
        actions.talk('Hello! I am HERA, a robot developed by RoboFEI team.')
        actions.talk('I was developed for working in a home environment, helping people to solve diary tasks, like take out the garbage or storing groceries')
        actions.talk('I will show you')
        actions.goto('bin') #local onde ta a lixeira
        actions.manip('open')
        actions.manip("", x=0.35, y=0.0, z=0.0, rx=0.0, ry=1.5, rz=0.0)
        time.sleep(0.5)
        actions.manip("close")
        actions.manip("home")
        actions.talk('Taking out the garbage')
        actions.goto('collection')
        actions.manip("", x=0.35, y=0.0, z= 0.0, rx=0.0, ry=1.5, rz=0.0)
        actions.manip("open")
        actions.manip("reset")
        time.sleep(2)
        actions.goto('start')

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
