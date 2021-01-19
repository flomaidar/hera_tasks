#!/usr/bin/env python

import traceback
import rospy
import math
import json
import time
import tf

from std_msgs.msg import UInt32
from gsr_ros.msg import Opcs
from gsr_ros.srv import StartRequest

from Actions import Actions

class Task():
    """docstring for Task"""
    def __init__(self):
        rospy.init_node('Task')
        rospy.sleep(1)
        listener = tf.TransformListener()

        # set vizbox story and publisher
        rospy.set_param('/story/title', 'Receptionist')
        rospy.set_param('/story/storyline',[])
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

        srv_names = StartRequest()
        srv_names.spec = [
            'Hunter',
            'William']

        srv_drinks = StartRequest()
        srv_drinks.spec = [
            'Lemonade',
            'Water']

        ########################################################################
        ########################################################################

        actions.talk('Hello! My name is HERA.')
        actions.talk('Please, talk to me after the bip.')
        #actions.pose('start')


        actions.talk('Starting Receptionist task')

        # talk = False
        # while not json.loads(actions.question('is_front_free').result):
        #     if not talk:
        #         actions.talk('Waiting to open the door')
        #         talk = True
	    #     continue
        # actions.talk('The door is open!')
        #
        # actions.talk('Going to reception!')
	    # actions.move('foward', seconds=3.0)
	    # actions.goto('announcement'('reception')
        # actions.talk('I reach the reception location!')
        # actions.manip("close")

        actions.talk('Going to reception')
        actions.goto('announcement')

        # actions.manip("close")
        # actions.talk('Waiting for a new guest')
        # time.sleep(3)
        # actions.talk('Waiting for a new guest')
        # while True:
        #     try:
        #         actions.head(0.0,0.0)
        #         time.sleep(5)
        #         people = actions.people().people
        #     except Exception as e:
        #         print e
        #     if len(people) > 0:
        #         break

        # dist = 1000
        # while dist > 1.3:
        #     dist = math.sqrt( math.pow(people[0].pose.position.x,2) + math.pow(people[0].pose.position.y,2) )
        #     ang = math.atan2(people[0].pose.position.y, people[0].pose.position.x)
        #     if dist > 1.3:
        #         actions.talk('please, come close')
        #     time.sleep(3)

        time.sleep(2)
        actions.talk('please, come close')
        time.sleep(3)

        actions.talk('Hi, my name is HERA. Welcome to the party.')
        name_1 = ''
        while name_1 == '':
            actions.talk('Please, what is your name?')
            speech = actions.hear(srv_names)
            name_1 = speech.result
        actions.talk('Hi '+ name_1)
        drink_1 = ''
        while drink_1 == '':
            actions.talk('Please, what is your favorite drink?')
            speech = actions.hear(srv_drinks)
            drink_1 = speech.result
        actions.talk('Your favorite drink is '+ drink_1)
        actions.talk('Please, follow me')
        actions.goto('announcement')
        actions.talk('Hi John. This is ' + name_1)
        #actions.manip("point", -1.4)
        # actions.goto('announcement'('John')
        actions.talk('His favorite drink is ' + drink_1)
        # actions.goto('announcement'('person_2')
        actions.talk(name_1 + ', this is john')

        # while True:
        #     try:
        #         people = actions.people().people
        #     except Exception as e:
        #         print e
        #     if len(people) > 0:
        #         break
        #ang = 0.2
        # ang = math.atan2(people[0].pose.position.y, people[0].pose.position.x)

        # actions.manip("point", ang)
        #actions.goto('announcement'('')
        actions.talk('His favorite drink is coke')
        #actions.manip("point", ang - 0.7)
        actions.goto('announcement')
        actions.talk(name_1 + ', feel free to take a seet')
        actions.talk('Enjoy the party')

        actions.talk("Going to recception")
        # actions.manip("home")
        actions.goto('announcement')

###########################################################################

        actions.talk('Waiting for a new guest')

        # actions.manip("close")
        actions.talk('Waiting for a new guest')
        # while True:
        #     try:
        #         actions.head(0.0,0.0)
        #         time.sleep(5)
        #         people = actions.people().people
        #     except Exception as e:
        #         print e
        #     if len(people) > 0:
        #         break
        #
        # dist = 1000
        # while dist > 1.3:
        #     dist = math.sqrt( math.pow(people[0].pose.position.x,2) + math.pow(people[0].pose.position.y,2) )
        #     ang = math.atan2(people[0].pose.position.y, people[0].pose.position.x)
        #     if dist > 1.3:
        #         actions.talk('please, come close')
        #     time.sleep(3)
        # actions.talk('Hi, my name is HERA. Welcome to the party.')


        name_2 = ''
        while name_2 == '':
            actions.talk('Please, what is your name?')
            speech = actions.hear(srv_names)
            name_2 = speech.result
        actions.talk('Hi '+ name_2)
        drink_2 = ''
        while drink_2 == '':
            actions.talk('Please, what is your favorite drink?')
            speech = actions.hear(srv_drinks)
            drink_2 = speech.result
        actions.talk('Your favorite drink is '+ drink_2)
        actions.talk('Please, follow me')
        actions.goto('announcement')
        actions.talk('Hi John and '+ name_1 +'. This is ' + name_2)
        # actions.manip("point", -1.4)
        actions.talk('His favorite drink is ' + drink_2)
        actions.talk(name_2 + ', this is john')

        # while True:
        #     try:
        #         people = actions.people().people
        #     except Exception as e:
        #         print e
        #     if len(people) > 0:
        #         break
        ang = -0.5
        # ang = math.atan2(people[0].pose.position.y, people[0].pose.position.x)

        # actions.manip("point", ang)
        actions.talk('His favorite drink is coke')
        actions.talk('and this is ' + name_1)

        # while True:
        #     try:
        #         people = actions.people().people
        #     except Exception as e:
        #         print e
        #     if len(people) > 0:
        #         break

        ang = 0.2

        # actions.manip("point", ang)
        actions.talk('His favorite drink is ' + drink_1)
        actions.talk(name_2 + ', feel free to take a seet')
        actions.goto('announcement')
        # actions.manip("point", ang - 0.3)
        actions.talk('Enjoy the party')
        actions.talk("Going to reception")
        actions.goto('announcement')

###########################################################################

        actions.talk('End task')

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
