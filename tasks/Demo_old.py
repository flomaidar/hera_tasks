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
        robotnames = ['Robot','Hera']
        # locals = json.loads(actions.question('know_places').result)
        specs = [
            '<robotnames>',
            'go to <locals>',

        ]

        # speech variables
        self.srv = StartRequest()
        self.srv.spec = specs
        self.srv.choices.append(Opcs(id="robotnames", values=robotnames))
        # self.srv.choices.append(Opcs(id="locals", values=locals))

        ########################################################################
        ########################################################################

    actions.talk('Hello! My name is HERA.')
	actions.talk('I am a service robot and I will demonstrate some tasks for you.')

	# actions.pose('start')
	 actions.talk('I will go to the kitchen')
	 actions.goto('kitchen')
	 actions.head(0.0,0.35)
	 coordinates = actions.FindObject('closest')
	 coordinates.z += 0.10
	 actions.manip_goal(coordinates, 'pick')
	 actions.goto('start')
         actions.talk('Here it is')
	 actions.manip('', x=0.30, y=0.0, z=0.5)
	 actions.manip('open')

        # actions.move('spin_left')
        # time.sleep(15)
        # actions.move('stop')

	# while(True):
        #actions.manip('pick', 0.25, 0.10, -0.1)
        #actions.manip('point', 1.2)
		# actions.manip('close')
		# actions.manip('reset')
		#actions.manip('pick', 0.25, 0.1, -0.1)
		#actions.manip('close')
		#actions.manip('place', 0.25, 0.1, -0.10)
		# actions.talk("Hello!")

        #while (True):
            # try:
            #     speech = actions.hear(self.srv)
            #
            #     if (speech.result == '<robotnames>'):
            #         person = actions.face()
            #         actions.talk('Hello ' + person.result)
            #     elif(speech.result == 'go to <locals>'):
            #         local = speech.choices[0].values[0]
            #         actions.talk("Going to " + local)
            #         actions.goto(local)
            #     elif (speech.result == 'Introduce yourself'):
            #         actions.talk('Hi, I am HERA! Home Environment Robot Assistant.')
            #         actions.talk('Nice to meet you.')
            #         ac            #
            # except Exception as e:
            #     traceback.print_exc()tions.talk('I am a service robot developed by RoboFEI team .')
            #         actions.talk('I have a omni directional base to make me go foward.')
            #         actions.move('foward', seconds=1.0)
            #         actions.talk('backward.')
            #         actions.move('backward', seconds=1.0)
            #         actions.talk('spin.')
            #         actions.move('spin_left', seconds=1.0)
            #         actions.move('spin_right', seconds=1.0)
            #         actions.move('spin_right', seconds=1.0)
            #         actions.move('spin_left', seconds=1.0)
            #         actions.talk('go to left.')
            #         actions.move('left', seconds=1.0)
            #         actions.move('right', seconds=1.0)
            #         actions.talk('and right.')
            #         actions.move('right', seconds=1.0)
            #         actions.move('left', seconds=1.0)
            #         actions.talk('I have a Hokuyo laser rangefinder to help me navigate.')
            #         actions.talk('A manipulator with five degrees of freedon.')
            #         # actions.manipulator("wave")
            #         actions.talk('A full High Definition camera to help me to recognize faces and objects.')
            #         actions.talk('A Kinect sensor to help me to recognize people.')
            #         actions.talk('A speech recognition and synthesis system to human robot interaction and a cute face.')
            #         actions.talk('Please, follow me.')
            #         actions.goto("chair")
            #         actions.talk('Please, take a seat.')
            #         actions.talk('Welcome to my at home arena.')
            #         actions.talk('The RoboCup at Home league aims to develop service and assistive robot technology.')
            #         actions.talk('with high relevance for future personal domestic applications.')
            #         actions.talk('It is the largest international annual competition for autonomous service robots.')
            #         actions.talk('and is part of the RoboCup initiative.')
            #         actions.talk('A set of benchmark tests is used to evaluate the robots abilities.')
            #         actions.talk('and performance in a realistic non-standardized home environment setting.')
            #         actions.talk('Please, feel free to ask me someting.')
            #     elif (speech.result == 'What is your name'):
            #         actions.talk('My name is HERA! Home Environment Robot Assistant')
            #     elif (speech.result == 'What is your teams called'):
            #         actions.talk('I am from the Robo FEI team')
            #     elif (speech.result == 'How much is two plus two'):
            #         actions.talk('The answer is four')
            #     elif (speech.result == 'Thank you'):
            #         actions.talk('You are welcome!')
            #
            # except Exception as e:
            #     traceback.print_exc()

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
