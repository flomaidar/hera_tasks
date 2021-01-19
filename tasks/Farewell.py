#!/usr/bin/env python

import traceback
import rospy
import math
import json

from std_msgs.msg import UInt32
from gsr_ros.msg import Opcs
from gsr_ros.srv import StartRequest

from Actions import Actions

class Task():
    """docstring for Task"""
    def __init__(self):
        rospy.sleep(1)

        # set vizbox story and publisher
        rospy.set_param('/story/title', 'Farewell')
        rospy.set_param('/story/storyline',[
            'Person recognition',
            'Navigation to person',
            'Ask if person want to leave',
            'Ask person\'s name',
            'Take person\'s coat',
            'Navigation to person',
            'Delivery person\'s coat',
            'Ask person to follow',
            'Navigation to outside home',
            'Find cabman',
            'Navigation to cabman',
            'Navigation to inside home',
        ])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        actions = Actions()

        # task variables
        robotnames = ['Robot','Hera','Ivy']
        locals = json.loads(actions.question('know_places').result)
        specs = [
            '<robotnames>',
            'go to <locals>',
            'Start task'
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

        while (True):
            try:
                speech = actions.hear(self.srv)

                if (speech.result == '<robotnames>'):
                    person = actions.face()
                    actions.talk('Hello ' + person.result)
                elif(speech.result == 'go to <locals>'):
                    local = speech.choices[0].values[0]
                    actions.talk("Going to " + local)
                    actions.goto(local)
                elif (speech.result == 'Start task'):

                    self.pub_vizbox_step.publish(0) # TODO: Person recognition (waving)
                    person = None
                    self.pub_vizbox_step.publish(1) # TODO: Navigation to person (woman)
                    actions.goto(person)
                    self.pub_vizbox_step.publish(2) # TODO: Ask if person want to leave
                    actions.talk("Hi, dou you want to leave?")
                    self.pub_vizbox_step.publish(3) # TODO: Ask person's name
                    actions.talk("What's you name?")
                    self.pub_vizbox_step.publish(4) # TODO: Take person's coat
                    actions.goto('coat_rack')
                    self.pub_vizbox_step.publish(5) # TODO: Navigation to person
                    actions.goto(person)
                    self.pub_vizbox_step.publish(6) # TODO: Delivery person's coat
                    self.pub_vizbox_step.publish(7) # TODO: Ask person to follow
                    actions.talk("Please, follow me.")
                    self.pub_vizbox_step.publish(8) # TODO: Navigation to outside home
                    actions.goto('exit')
                    self.pub_vizbox_step.publish(9) # TODO: Find cabman
                    self.pub_vizbox_step.publish(10) # TODO: Navigation to cabman
                    actions.goto('cabman')
                    self.pub_vizbox_step.publish(11) # TODO: Navigation to inside home
                    actions.goto('office')

            except Exception as e:
                traceback.print_exc()

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
