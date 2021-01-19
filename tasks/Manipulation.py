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
        rospy.set_param('/story/title', 'Manipulation')
        rospy.set_param('/story/storyline',[
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
        actions.pose('door')

        while (True):
            try:
                speech = actions.hear(self.srv)

                if (speech.result == '<robotnames>'):
                    person = actions.face()
                    actions.talk('Hello ' + person.result)
                elif (speech.result == 'Start task'):
                    actions.talk('Starting Storing Groceries task')

                    talk = False
                    while not json.loads(actions.question('is_front_free').result):
                        if not talk:
                            actions.talk('Waiting to open the door')
                            talk = True
                        continue
                    actions.talk('The door is open!')

                    actions.move('foward', seconds=5.0)

                    i = ''
                    j=0
                    cont = 0
                    while cont < 5:
                        actions.talk('Going to objects location')
                        actions.goto('refrigerator'+i)
                        # if cont == 0:
                        #     actions.talk('Please, remove the chairs')
                        # time.sleep(10)
                        actions.head(0.0,0.45)
                        #pick the object
                        aux = False
                        while not aux:
                            actions.talk('Looking for objects')
                            coordinates = actions.FindObject('closest')
                            if not coordinates == None:
                                coordinates.z += 0.03
                                actions.talk('I gonna take it')
                                aux = actions.manip_goal(coordinates, 'pick')
                            if not aux:
                                # actions.talk('I failed')
                                if i == '':
                                    i = '0'
                                elif i == '0':
                                    i = ''
                                actions.goto('refrigerator'+i)

                        #place the object
                        # actions.talk('Gotcha!')
                        actions.talk('Going to shelf')
                        actions.goto('shelf'+str(j))
                        actions.head(0.0,0.0)
                        actions.talk('I going to place the object in the shelf')
                        actions.manip('place', x=0.33, y=0.0, z=0.35)
                        # actions.talk('Done!')

                        if j == 3:
                            j = 0
                        else:
                            j += 1
                        cont += 1

                    actions.talk('Leaving the arena!')
                    actions.goto('end')
                    actions.talk('End task')

            except Exception as e:
                traceback.print_exc()

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
