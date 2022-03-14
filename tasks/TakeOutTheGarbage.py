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

        
        # actions.talk('Please, talk to me')
        # actions.pose('door')

        while (True):
            actions.talk('Bom dia')
            
                    ######
                    # talk = False
                    # while not json.loads(actions.question('is_front_free').result):
                    #     if not talk:
                    #         actions.talk('Waiting to open the door')
                    #         talk = True
                    #     continue
                    # actions.talk('The door is open!')
                    # actions.move('foward', seconds=5.0)

            # cont = 1
            # while cont <= 20:
                # actions.talk('I will now go the bin location')
            # actions.goto('bin0')
                # actions.talk("Please give me the bag")
                # actions.manip("open")
                # actions.manip("", x=0.3, y=0.0, z=0.2, rx=0.0, ry=0.8, rz=0.0)
                # time.sleep(6)
                # actions.manip("close")
                # actions.manip("home")
# 
                # actions.talk('Going to collection zone')
                # actions.goto('collection')
                # actions.talk("I will now drop the bags in the collection zone")
                # actions.manip("", x=0.28, y=0.0, z=-0.01, rx=0.0, ry=1.0, rz=0.0)
                # time.sleep(4.9)
                # actions.manip("open")
                # actions.manip("reset")
                # time.sleep(4)
# 
                # cont += 1
            # 
            # actions.goto('end')
            # return None
# 
        

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
