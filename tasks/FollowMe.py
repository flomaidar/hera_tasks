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
        rospy.set_param('/story/title', 'FollowMe')
        rospy.set_param('/story/storyline',[
            ])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        actions = Actions()

        # task variables
        robotnames = ['Robot','Hera','Ivy']
        locals = json.loads(actions.question('know_places').result)
        specs = [
            '<robotnames>',
            '<locals>',
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
        # actions.pose('door')
        actions.pose('start_follow')

        while (True):
            try:
                speech = actions.hear(self.srv)

                if (speech.result == '<robotnames>'):
                    person = actions.face()
                    actions.talk('Hello ' + person.result)
                elif (speech.result == 'Start task'):
                    actions.talk('Starting follow me task')

                    # talk = False
                    # while not json.loads(actions.question('is_front_free').result):
                    #     if not talk:
                    #         actions.talk('Waiting to open the door')
                    #         talk = True
                    #     continue
                    # actions.talk('The door is open!')


                    # actions.talk('Going to Living Room')
                    # actions.move('foward', seconds=5.0)
                    # actions.goto('living_room')

                    actions.talk("I'm ready to guide you")
                    actions.talk('Where do you want to go?')
                    while True:
                        srv_guide = StartRequest()
                        srv_guide.spec = ['go to <locals>', '<robotnames>']
                        comodos = ['office','bedroom']
                        srv_guide.choices.append(Opcs(id="robotnames", values=robotnames))
                        srv_guide.choices.append(Opcs(id="locals", values=comodos))
                        speech = actions.hear(srv_guide)
                        if speech.result == 'go to <locals>':
                            local = speech.choices[0].values[0]
                            actions.talk('Goint to, '+local)
                            if local == 'office':
                                actions.goto('intermed')
                            actions.goto(local)
                            break
                        elif (speech.result == '<robotnames>'):
                            actions.talk('Hello ')

                    #Follow person
                    actions.talk("We reach the "+local)
                    time.sleep(4)
                    actions.move('spin_left')
                    time.sleep(18)
                    actions.move('stop')
                    actions.talk("Please, stand in front of me, I will memorize you")
                    time.sleep(5)
                    actions.talk("I'm ready to follow you")
                    actions.talk("Say yes when you want me to start following you")
                    follow = ''
                    while not follow == 'yes':
                        srv_follow = StartRequest()
                        srv_follow.spec = ['yes','no']
                        speech = actions.hear(srv_follow)
                        follow = speech.result.lower()
                    actions.talk("You can walk now")
                    time.sleep(4)
                    if local == 'bedroom':
                        actions.goto('a')
                        actions.goto('b')
                        actions.goto('c')
                        actions.goto('d')
                        actions.goto('e')
                        actions.goto('f')
                        actions.goto('end')
                    elif local == 'office':
                        actions.goto('g')
                        actions.goto('h')
                        actions.goto('i')
                        actions.goto('e')
                        actions.goto('f')
                        actions.goto('end')
                    else:
                        actions.goto('end')

                    # actions.talk('End task')
                    actions.move('spin_left')

            except Exception as e:
                traceback.print_exc()

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
