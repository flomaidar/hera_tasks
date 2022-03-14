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
from social_worlds.srv import *

from Actions import Actions

class Task():
    def __init__(self):
        rospy.init_node('Task')
        rospy.sleep(1)
        listener = tf.TransformListener()

        #set vizbox story and publisher
        rospy.set_param('/story/title', 'Receptionist')
        rospy.set_param('/story/storyline', [])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        #Task Variables
        actions = Actions()
        robotnames = ['Robot', 'Hera', 'Zeus']
        locals = json.loads(actions.question('know_places').result)
        specs = [
            '<robotnames>',
            'Start task'
        ]

        # #Speech Variables
        self.srv= StartRequest()
        self.srv.spec = specs
        self.srv.choices.append(Opcs(id="robotnames", values=robotnames))
        self.srv.choices.append(Opcs(id="locals", values=locals))
        srv_names = StartRequest()
        srv_names.spec= [
            'William',
            'Alex',
            'Christian',
            'Robert',
            'Piper'
        ]

        srv_drinks = StartRequest()
        srv_drinks.spec = [
            'Lemonade',
            'Water',
            'Beer',
            'Wine',
            'Orange Juice'
        ]

        srv_age = StartRequest()
        ages = [i for i in range(150)]
        str_ages = [str(i) for i in ages]


        ##People Dictionary
        name =  {p1  : '',
                 p2   : '',
                 p3 : ''}

        age =   {p1 : '',
                 p2 : '',
                 p3 : ''}

        drink = {p1 : '',
                 p2 : '',
                 p3 : ''}
        
        #Task init
        actions.talk('Hello! My name is HERA.')
        actions.talk('Starting Receptionst task')
        # actions.talk('Going to reception')
        # actions.goto('reception')
        # actions.talk('Waiting for a new guest')

       
        for i in range(3):
            p = 'p'+str(i+1)
            actions.talk('Going to reception')
            actions.goto('reception')
            actions.talk('Waiting for a new guest')
            #world(p)
            actions.talk('Hi, my name is HERA. Welcome to the party')
            while name[p] == '':
                actions.talk('Please, what is your name?')
                speech = actions.hear(srv_names)
                name[p] = speech.result
            while age[p] == '':
                actions.talk('I am sorry to ask, but how old are you?')
                speech = actions.hear(srv_age)
                age[p] = speech.result
            while drink[p] == '':
                actions.talk('Please, what is your favorite drink?')
                speech = actions.hear(srv_drinks)
                drink[p] = speech.result
                if age[p] <18 and drink[p] == 'beer':
                    actions.talk('I am sorry but you do not have enough age to ask for beer')
                    drink[p] == ''
            actions.talk('Hi '+ name[p])
            actions.talk('Your favorite drink is ' + drink[p])
            actions.talk('Please, follow me')
            actions.goto('party')
            actions.talk('Hi John.')
            actions.move('spin_right', seconds=1.0)
            actions.talk('This is '+ name[p])
            actions.move('spin_left', seconds=1.0)
            actions.talk('He is '+ age[p] +'years old and his favorite drink is '+ drink[p])
            actions.move('spin_right', seconds=1.0)
            actions.talk(name[p] +', this is John')
            actions.move('spin_right', seconds=1.0)
            actions.move('spin_left', seconds=1.0)
            actions.talk('His favorite drink is coke')

            if i == 0:
                #Condicao de primeira pessoa indo para a poltrona
                bigger = age[p]
                actions.talk(name[p]+'Please, seat in the armchair')

            elif i == 1:
                #Condicao para a segunda pessoa
                aux = age[p]
                if age[p] > bigger:
                    #Pessoa ja sentada sai e vai para sentar do lado do John
                    actions.talk(name[int(p-1)]+'Please, sit on the couch next to john')
                    #Mais velha senta na poltrona
                    actions.talk(name[int(p)]+'Seat in the armchair, please')
                else:
                    action.talk(name[p]+'Please, sit on the couch next to john')
            elif i == 2:
                #Condicao para a terceira pessoa
                if age[p]>bigger:
                    #Primeira pessoa ja sentada, sai e vai para o outro sofa
                    actions.talk(name[int(p-2)]+'Please, sit on the empty couch')
                    #Mais velha senta na poltrona
                    actions.talk(name[int(p)]+'Seat in the armchair, please')
                elif age[p]>aux:
                    #Segunda pessoa ja sentada, sai e vai para o outro sofa
                    actions.talk(name[int(p-1)]+'Please, sit on the empty couch')
                    #Mais velha senta na poltrona
                    actions.talk(name[int(p)]+'Seat in the armchair, please')
                else:
                    actions.talk(name[int(p)]+'Please, sit on the empty couch')
        actions.goto('announcement') #local virado para todos onde ira se comunicar
        actions.talk('Now that we are all comfortable, lets start the party')
        actions.talk('End task')
if __name__ == "__main__":
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass