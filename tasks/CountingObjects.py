#!/usr/bin/env python

import traceback
import rospy
import math
import json
import time

from std_msgs.msg import UInt32
from gsr_ros.msg import Opcs
from gsr_ros.srv import StartRequest
from hera_objects.msg import DetectedObjectArray, ObjectPosition

from Actions import Actions

class Task():
    """docstring for Task"""
    def __init__(self):
        rospy.sleep(1)

        # set vizbox story and publisher
        rospy.set_param('/story/title', 'CountingObjects')
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

        rospy.Subscriber('/dodo_detector_ros/detected', DetectedObjectArray, self.get_detected_objects)
        self._objects = list()

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
                    actions.talk('Starting Counting Objects task')

                    talk = False
                    while not json.loads(actions.question('is_front_free').result):
                        if not talk:
                            actions.talk('Waiting to open the door')
                            talk = True
                        continue
                    actions.talk('The door is open!')


                    actions.talk('Going to shelf')
                    actions.move('foward', seconds=5.0)
                    actions.goto('shelf')

                    time.sleep(8)
                    actions.head(0.0,0.2)
                    time.sleep(8)
                    objec = self._objects
                    num_objec = len(objec)
                    ini = rospy.get_time()
                    while not (rospy.get_time() - ini) > 1.0:
                        aux = self._objects
                        if len(aux) > len(objec):
                            objec = aux
                            num_objec = len(objec)

                    actions.talk("I'm seeing %d objects"%(num_objec))

                    time.sleep(2)

                    actions.talk("From left to right")
                    actions.talk("I'm seeing")
                    d = {'Biscuit':'Snacks','Waffer':'Snacks','Snack': 'Snacks','Chocolate_milk': 'Drinks','Orange_juice':'Drinks','Soda_bottle':'Drinks','Soda_can':'Drinks','Canned_corn' :'Food','Cup_noodles' :'Food','Noodles' : 'Food','Gelatine' :'Food','Toothpaste' : 'Personal Care','Cup' :'Personal Care'}
                    for obj in objec:
                        actions.talk("a %s"%(obj.replace('_',' ')))
                        actions.talk("from category "+d[obj])

                    time.sleep(10)
                    actions.goto('end')
                    actions.talk('going to end')
                    actions.talk('end task')

            except Exception as e:
                traceback.print_exc()

    def get_detected_objects(self, array):
        if not len(array.detected_objects) == 0:
            self._objects *= 0
            for detection in array.detected_objects:
                self._objects.append(detection.type.data)

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
