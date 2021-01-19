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
        rospy.set_param('/story/title', 'StoringGroceries')
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
        #actions.talk('Please, talk to me after the bip.')
        #actions.pose('start')

#        actions.head(0.0,0.4)
#        sleep(5)
#        actions.head(0.0,0.0)


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
                #elif (speech.result == 'Start task'):
                elif (1 == 1):
                    actions.talk('Starting Storing Groceries task')

                    # talk = False
                    # while not json.loads(actions.question('is_front_free').result):
                    #     if not talk:
                    #         actions.talk('Waiting to open the door')
                    #         talk = True
                    #     continue
                    # actions.talk('The door is open!')

                    #actions.move('foward', seconds=5.0)
                    #actions.goto('shelf')
                    #actionslocation.talk('Mapping shelf')
                    # mapear shelf

                    i=0
                    j=0
                    cont = 0
                    old_coord_ref = 0
                    while cont < 3:
                        actions.talk('Going to table')
                        #actions.goto('table')
                        # if cont == 0:
                        #     actions.talk('Please, remove the chairs')
                        # sleep(10)
                        actions.head(0.0,0.0)
                        actions.goto('table'+str(i))
                        #actions.head(0.0,0.45)
                        #pick the object
                        #actions.manip('pick', x=0.30, y=0.0, z=0.25)
                        #i += 1
                        aux = False
                        while not aux:
                            actions.head(0.0,0.5)
                            rospy.sleep(3)
                            coordinates = actions.FindObject('closest')
                            if not coordinates == None:
                                if coordinates.x == old_coord_ref or coordinates.x == 10:
                                    coordinates.x = 10
                                    coordinates.y = 10
                                    coordinates.z = 10
				    #aux = False
                                else:
                                    old_coord_ref = coordinates.x
				    #aux = actions.manip_goal(coordinates, 'pick')
                                coordinates.z += 0.05
                            print coordinates
                            aux = actions.manip_goal(coordinates, 'pick')
                            if not aux:
                                if i == 2:
                                    i = 0
                                else:
                                    i += 1
            			actions.goto('table'+str(i))

                        #place the object
                        actions.talk('Going to shelf')
                        actions.head(0.0,0.0)
                        actions.goto('shelf0')
                        actions.head(0.0,0.7)
                        rospy.sleep(3)
                        #set coordinate y for place:
                        y_place = -0.15 + 0.075 * cont
                        actions.manip('', x=0.40, y=y_place, z=0.25)
                        actions.manip('open', x=0.30, y=0.0, z=0.25)
                        actions.manip('reset', x=0.30, y=0.0, z=0.25)


                        j+=1
                        cont += 1

                    actions.talk('End task')

            except Exception as e:
                traceback.print_exc()

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
