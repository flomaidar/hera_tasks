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
        rospy.set_param('/story/title', 'CarryMyLuggage')
        rospy.set_param('/story/storyline',[
            'Person recognition',
            'Navigation to person',
            'Bag recognition',
            'Take the bag',
            'Start follow',
            'Obstacle avoidance',
            'Stop follow',
            'Back to arena'
            ])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        actions = Actions()

        # task variables
        robotnames = ['Robot','Hera','Ivy']
        locals = json.loads(actions.question('know_places').result)
        specs = [
            '<robotnames>',
            'Start task',
            'Stop following',
            'Thank you'
        ]

        # speech variables
        self.srv = StartRequest()
        self.srv.spec = specs
        self.srv.choices.append(Opcs(id="robotnames", values=robotnames))
        self.srv.choices.append(Opcs(id="locals", values=locals))

        ########################################################################
        ########################################################################

        actions.talk('Hello! My name is HERA.')
        actions.talk('Please, talk to me after the bip.')
        actions.pose('start')

        if True:
        while (True):
            try:
                speech = actions.hear(self.srv)

                if (speech.result == '<robotnames>'):
                    person = actions.face()
                    actions.talk('Hello ' + person.result)
                elif (speech.result == 'Start task'):
                    actions.talk('Starting Carry My Luggage task')

                    talk = False
                    while not json.loads(actions.question('is_front_free').result):
                        if not talk:
                            actions.talk('Waiting to open the door')
                            talk = True
                        continue
                    actions.talk('The door is open!')

                    actions.talk('Going to office!')
                    actions.move('foward', seconds=5.0)
                    actions.goto('office')

                    actions.move('spin_left')
                    time.sleep(22)
                    actions.move('stop')


                    self.pub_vizbox_step.publish(0) # TODO: Person recognition: Pointing
                    self.pub_vizbox_step.publish(1) # TODO: Navigation to person
                    self.pub_vizbox_step.publish(2) # TODO: Bag recognition

                    self.pub_vizbox_step.publish(3) # Take the bag
                    actions.talk('Hi, I am here to help you with the luggage')
                    actions.talk('searching for the bag')
                    actions.talk('please, wait a moment')
                    actions.head(0.0,0.9)
                    actions.manip("point")
                    actions.talk('Please, put the bag in my hand')
                    actions.head(0.0,0.5)
                    actions.manip("open")
                    time.sleep(5)

                    actions.talk('Thank you')
                    actions.manip("close")
                    actions.talk('please, wait a moment')
                    actions.manip("home")

                    self.pub_vizbox_step.publish(4) # Start follow
                    actions.talk('Please, stand in front of me.')
                    actions.talk('I will memorize you!')
                    actions.head(0.0,0.2)
                    # person = 'nearest'
                    # person = 'robot_2/base_link'
                    person = 'Person_0_Neck'
                    time.sleep(5)
                    actions.talk('Operator saved with success!')
                    actions.talk('Please, say stop following me when you want to stop!')
                    actions.talk('I am ready to follow you!')
                    time.sleep(4)
                    actions.move('foward', seconds=1.0)

                    # actions.follow(person, False)
                    actions.goto("a")
                    actions.goto("b")
                    actions.goto("c")
                    actions.goto("d")
                    actions.goto("e")
                    actions.goto("f")
                    actions.goto("g")
                    actions.goto("end")

                    # while True:
                    #     actions.goto(person,wait=False)
                    #     time.sleep(3)

                    self.pub_vizbox_step.publish(5) # Obstacle avoidance (crowd, small object, 3D object, retractable area)

                # elif (speech.result == 'Stop following'):
                #     self.pub_vizbox_step.publish(6) # Stop follow
                #     actions.goto(None)
                #     actions.talk('Ok. I am stop following')
                #     actions.talk('Please, take the bag from my hand')
                #     time.sleep(5)
                #     self.pub_vizbox_step.publish(7) # Back to arena
                #     actions.talk('Going back to arena')
                #     actions.goto('office')
                #     actions.talk('End task')
                #
                #
                # elif (speech.result == 'Thank you'):
                #     self.pub_vizbox_step.publish(6) # Stop follow
                #     actions.goto(None)
                #     actions.talk('You welcome. I am stop following')
                #     actions.talk('Please, take the bag from my hand')
                #     time.sleep(5)
                #     self.pub_vizbox_step.publish(7) # Back to arena
                #     actions.talk('Going back to arena')
                #     actions.goto('office')
                #     actions.talk('End task')

            # except Exception as e:
            #     traceback.print_exc()

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
