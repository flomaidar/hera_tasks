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

class Restaurant():
    """docstring for Restaurant"""

    def __init__(self):
        # set vizbox story and publisher
        rospy.set_param('/story/title', 'Restaurant')
        rospy.set_param('/story/storyline', [])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        actions = Actions()

        robotnames = ['Robot','Hera','Ivy']
        locals = json.loads(actions.question('know_places').result)
        beverage = ['Coke','Soda Can']
        food = ['Snack','Potato']

        specs = [
            '<robotnames>',
            'Start task'
        ]

        spec_order = [
            'I want a <beverage>',
            'I want a <food>']

        self.srv = StartRequest()
        self.srv.spec = specs
        self.srv.choices.append(Opcs(id="robotnames", values=robotnames))

        actions.talk('Hello! My name is HERA.')
        actions.talk('Please, talk to me after the bip.')
        actions.pose('restaurant')

        while (True):
            try:
                speech = actions.hear(self.srv)

                if (speech.result == '<robotnames>'):
                    person = actions.face()
                    actions.talk('Hello ' + person.result)
                elif (speech.result == 'Start task'):
                    actions.talk('Starting Restaurant task')

                    # actions.goto('restaurant')
                    actions.talk("Waiting for a costumer")
                    actions.talk("Please, wave for me!")
                    time.sleep(5)
                    actions.talk("Please, wave for me!")
                    time.sleep(5)
                    actions.talk("I see 1 guest calling me next to table 4")
                    # self.__hera.talk.execute("I see 1 guest calling me next to table B")

                    ############################################### pedido 1
                    actions.talk("going to table 4")
                    actions.goto('start')
                    actions.goto('table_a')
                    actions.talk("Hello, I'm goint to take your order")
                    actions.talk("What do you want to order?")
                    i = 0
                    while True:
                        i += 1
                        srv_order = StartRequest()
                        srv_order.spec = spec_order
                        srv_order.choices.append(Opcs(id="beverage", values=beverage))
                        srv_order.choices.append(Opcs(id="food", values=food))
                        speech = actions.hear(srv_order)
                        if speech.result == 'I want a <beverage>':
                            actions.talk("I'm going to take your drink, just a moment")
                            rec_order = speech.choices[0].values[0]
                            actions.talk("I'm going to your "+rec_order)
                            break
                        elif speech.result == 'I want a <food>':
                            actions.talk("I'm going to take your food, just a moment")
                            rec_order = speech.choices[0].values[0]
                            actions.talk("I'm going to your "+rec_order)
                            break
                        elif i == 2:
                            rec_order = 'Coke'
                            actions.talk("I'm going to your "+rec_order)
                            break

                        ############################################### service 1
                    actions.goto('intermed')
                    actions.goto('bar')
                    actions.talk("I want a {} to table 4".format(rec_order))
                    #actions.talk("please, take the tray in my hand")
                    actions.talk("please, take the order in my hand")
                    actions.manip('open')
                    # actions.manip('', x=0.37, y=0.0, z=0.25, rx = 1.57)
                    actions.manip('', x=0.3, y=0.0, z=0.32)
                    actions.talk("I goint to close my hand")
                    time.sleep(1)
                    actions.manip('close')
                    actions.manip('home')
                    actions.talk("going to table 4")

                    actions.goto('start')
                    actions.goto('table_a')
                    actions.talk("here is your order")
                    # actions.head(0.0,0.5)
                    # time.sleep(2)
                    actions.manip('place', x=0.38, y=0.0, z=0.3)
                    # actions.head(0.0,0.0)
                    actions.talk("Please, hold it, I'm goint to release it in 5 seconds")
                    time.sleep(4)
                    actions.manip('open')
                    actions.manip('reset')

                    # actions.goto('table_a')
                    # actions.talk("here is your order")
                    # actions.manip('', x=0.38, y=0.0, z=0.1)
                    # actions.talk("Are you holding it? Say yes or no")
                    # hold = ''
                    # while not hold == 'yes':
                    #     srv_hold = StartRequest()
                    #     srv_hold.spec = ['yes','no']
                    #     speech = actions.hear(srv_hold)
                    #     hold = speech.result.lower()
                    # actions.manip('open')
                    # actions.manip('reset')

                    # actions.goto('delivery_a')
                    # actions.talk("here is your order")
                    # actions.talk("I'm goint to place it in the table")
                    # actions.manip('place', x=0.40, y=0.0, z=-0.09)

                    ############################################### wait new costumer
                    actions.goto('intermed')
                    actions.goto('restaurant')
                    actions.talk("Waiting for a costumer")
                    actions.talk("Please, wave for me!")
                    time.sleep(5)
                    actions.talk("Please, wave for me!")
                    time.sleep(5)
                    actions.talk("I see 1 guest calling me next to table 15")
                    ############################################### pedido 2
                    actions.talk("going to table 15")
                    actions.goto('start')
                    actions.goto('table_b')
                    actions.talk("Hello, I'm goint to take your order")
                    actions.talk("What do you want to order?")
                    i = 0
                    while True:
                        i += 1
                        srv_order = StartRequest()
                        srv_order.spec = spec_order
                        srv_order.choices.append(Opcs(id="beverage", values=beverage))
                        srv_order.choices.append(Opcs(id="food", values=food))
                        speech = actions.hear(srv_order)
                        if speech.result == 'I want a <beverage>':
                            actions.talk("I'm going to take your drink, just a moment")
                            rec_order = speech.choices[0].values[0]
                            actions.talk("I'm going to your "+rec_order)
                            break
                        elif speech.result == 'I want a <food>':
                            actions.talk("I'm going to take your food, just a moment")
                            rec_order = speech.choices[0].values[0]
                            actions.talk("I'm going to your "+rec_order)
                            break
                        elif i == 2:
                            rec_order = 'Snack'
                            actions.talk("I'm going to your "+rec_order)
                            break

                    ############################################### service 2
                    actions.goto('intermed')
                    actions.goto('bar')
                    actions.talk("I want a {} to table 15".format(rec_order))
                    actions.talk("please, take the order in my hand")
                    actions.manip('open')
                    actions.manip('', x=0.3, y=0.0, z=0.32)
                    actions.talk("I goint to close my hand")
                    time.sleep(1)
                    actions.manip('close')
                    actions.manip('home')
                    actions.talk("going to table 15")

                    actions.goto('start')
                    actions.goto('table_b')
                    actions.talk("here is your order")
                    # actions.head(0.0,0.5)
                    # time.sleep(2)
                    actions.manip('place', x=0.38, y=0.0, z=0.3)
                    # actions.head(0.0,0.0)
                    actions.talk("Please, hold it, I'm goint to release it in 5 seconds")
                    time.sleep(4)
                    actions.manip('open')
                    actions.manip('reset')

                    # actions.goto('table_b')
                    # actions.talk("here is your order")
                    # actions.manip('', x=0.38, y=0.0, z=0.1)
                    # actions.talk("Are you holding it? Say yes or no")
                    # hold = ''
                    # while not hold == 'yes':
                    #     srv_hold = StartRequest()
                    #     srv_hold.spec = ['yes','no']
                    #     speech = actions.hear(srv_hold)
                    #     hold = speech.result.lower()
                    # actions.manip('open')
                    # actions.manip('reset')

                    # actions.goto('delivery_b')
                    # actions.talk("here is your order")
                    # actions.talk("I'm goint to place it in the table")
                    # actions.manip('place', x=0.40, y=0.0, z=-0.09)

                    ######################################## finish


                    actions.talk("going to end")
                    actions.goto('start')
                    actions.talk("I finish this task")

            except Exception as e:
                traceback.print_exc()

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Restaurant()
    except KeyboardInterrupt:
        pass
