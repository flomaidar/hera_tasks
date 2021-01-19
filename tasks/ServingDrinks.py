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
        rospy.set_param('/story/title', 'ServingDrinks')
        rospy.set_param('/story/storyline',[
            ])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        actions = Actions()

        # task variables
        names = ['John', 'Jake', 'Peralta', 'Will', 'Amanda']
        drinks = ['Milk box','Juice bottle','Toddy box']
        robotnames = ['Robot','Hera','Ivy']
        locals = json.loads(actions.question('know_places').result)
        specs = [
            '<robotnames>',
            'go to <locals>',
            'Start task',
            '<drinks>',
            '<names>'
        ]

        # speech variables
        self.srv = StartRequest()
        self.srv.spec = specs
        self.srv.choices.append(Opcs(id="robotnames", values=robotnames))
        self.srv.choices.append(Opcs(id="locals", values=locals))
        self.srv.choices.append(Opcs(id="drinks", values=drinks))
        self.srv.choices.append(Opcs(id="names", values=names))

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
                elif (speech.result == 'Start task'):
                    actions.talk('Starting Serving Drinks task')

                    j = 0
                    cont = 0
                    while cont < 5:
                        actions.goto('start_local') #local to be defined
                        actions.head(0.0,0.0)
                        time.sleep(10)
                        while True:
                            try:
                                people = actions.people()
                                person = people.people[j]
                                break
                            except Exception as e:
                                actions.talk('Looking for people')
                        person_pose = person.pose
                        rz = math.atan2(person_pose.position.y ,person_pose.position.x)
                        person_pose.position.x -= 0.7 * math.cos(rz)
                        person_pose.position.y -= 0.7 * math.sin(rz)
                        actions.gotopose(person_pose)

                        actions.talk('Hello, my name is Hera')

                        actions.talk('Please, what is your name?')
                        while True:
                            srv_name = StartRequest()
                            srv_name.spec = ['<names>','<robotnames>']
                            srv_name.choices.append(Opcs(id="robotnames", values=robotnames))
                            srv_name.choices.append(Opcs(id="names", values=names))
                            speech = actions.hear(srv_name)
                            name = speech.choices[0].values[0]
                            if speech.result == '<names>':
                                actions.talk('Hello, '+name)
                                break

                        actions.talk('What drink do you want?')
                        while True:
                            srv_drinks = StartRequest()
                            srv_drinks.spec = ['<drinks>','<robotnames>']
                            srv_drinks.choices.append(Opcs(id="drinks", values=drinks))
                            speech = actions.hear(srv_drinks)
                            drink = speech.choices[0].values[0].replace(' ','_')
                            if speech.result == '<drinks>':
                                actions.talk('ok, I will take your drink')
                                break

                        actions.talk('Going to bar')
                        actions.goto('table0')
                        actions.head(0.0,0.6)
                        #pick the object
                        i=0
                        aux = False
                        while not aux:
                            coordinates = actions.FindSpecificObject(drink)
                            if not coordinates == None:
                                coordinates.z += 0.1
                                aux = actions.manip_goal(coordinates, 'pick')
                            if not aux:
                                if i == 3:
                                    i = 0
                                else:
                                    i += 1
                                actions.goto('table'+str(i))

                        actions.goto(person_pose)
                        actions.talk('Here is your drink')
                        actions.manip("", x=0.25, y=0, z=0.35, rx=0, ry=0, rz=0)
                        actions.talk('Please hold it with both hands, so I can release it')
                        time.sleep(3)
                        hold = ''
                        while not hold == 'yes':
                            actions.talk("Are you holding it? Say yes or no")
                            srv_hold = StartRequest()
                            srv_hold.spec = ['yes','no']
                            speech = actions.hear(srv_hold)
                            hold = speech.result.lower()
                        actions.manip("open")
                        actions.manip("reset")

                        actions.goto('start_local') #local to be defined

                        cont += 1
                        j += 1

                    actions.talk('End task')

            except Exception as e:
                traceback.print_exc()

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
