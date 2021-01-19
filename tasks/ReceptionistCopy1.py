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

import subprocess
import os

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
            'William',
            'Christian',
            'Robert',
            'Piper']

        srv_drinks = StartRequest()
        srv_drinks.spec = [
            'Lemonade',
            'Water',
            'Beer',
            'Soda',
            'Orange Juice']

        srv_age = StartRequest()
        ages = [i for i in range(150)]
        str_ages = [str(i) for i in ages]
        srv_age.spec = str_ages

        srv_response = StartRequest()
        srv_response.spec = [
            'yes',
            'no'
        ]

        ##People Dictionary
        name =  {'p1'  : '',
                 'p2'   : '',
                 'p3' : ''}

        age =   {'p1' : '',
                 'p2' : '',
                 'p3' : ''}

        drink = {'p1' : '',
                 'p2' : '',
                 'p3' : ''}
        j=0

        actions.talk('Starting Task')
        for i in range(3):
            p = 'p'+str(i+1)
            actions.talk('Going to reception')
            actions.goto('reception')
            actions.talk('Waiting for a new guest')

            #rosservice call /task_control/receptionist/command "command:data: 'p1'"
            if i == 0:
                os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p1\'}}"')
                os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p2\'}}"')
            elif i == 1:
                os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p11\'}}"')
                os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p12\'}}"')
            elif i == 2:
                os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p21\'}}"')
                os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p22\'}}"')

            actions.talk('Hi, my name is HERA. Welcome to the party')
            while True:    
                while name[p] == '':
                    actions.talk('Please, what is your name?')
                    speech = actions.hear(srv_names)
                    name[p] = speech.result
                actions.talk('You said your name is '+ speech.result+', am i right?')
                speech = actions.hear(srv_response)
                response = speech.result
                if response == 'no':
                    name[p] = ''
                else:
                    break
            while age[p] == '':
                actions.talk('I am sorry to ask, but how old are you?')
                speech = actions.hear(srv_age)
                age[p] = speech.result
            while drink[p] == '':
                actions.talk('Please, what is your favorite drink?')
                speech = actions.hear(srv_drinks)
                drink[p] = speech.result
                # actions.talk('You said your favorite drink is '+ speech.result+', am I right?')
                # speech = actions.hear(srv_response)
                # response = speech.result
                # if response == 'no':
                #     drink[p] = ''
                # else:
                if age[p] < '18':
                    if drink[p] == 'Beer':
                        actions.talk(name[p]+', you are not 18 years old to drink Beer, choose another drink for today.')
                        drink[p] = ''
                else:
                    break
        
            #actions.talk('Hi '+ name[p])
            #actions.talk('Your favorite drink is ' + drink[p]+', am I right?')
            actions.talk('Ok, ' +name[p]+', follow me')
            actions.goto('party')

            if i == 0:
                os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p3\'}}"') 
            elif i == 1:
                os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p13\'}}"')
            elif i == 2:
                os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p23\'}}"') 
            
            # actions.talk('Hi John.')
            # actions.move('spin_left', 0.6, 8)
            # actions.move('stop')
            # actions.talk('This is '+ name[p] + '. He is '+ age[p] +' years old and his favorite drink is '+ drink[p])
            # actions.move('spin_right', 0.6, 8)
            # actions.move('stop')
            # actions.talk(name[p] +', this is John. His favorite drink is coke')

            if i == 0:
                actions.talk('Hi John.')
                actions.move('spin_left', 0.6, 8)
                actions.move('stop')
                actions.talk('This is '+ name[p] + '. He is '+ age[p] +' years old and his favorite drink is '+ drink[p])
                actions.move('spin_right', 0.6, 8)
                actions.move('stop')
                actions.talk(name[p] +', this is John. His favorite drink is coke')
                bigger = age[p]
                actions.talk(name[p]+', please, seat in the armchair')
                os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p4\'}}"')
                mai ='1'

            elif i == 1:
                actions.talk('Hi John and '+name['p1']) 
                actions.move('spin_left', 0.6, 8)
                actions.move('stop')
                actions.talk('This is '+ name[p] + '. He is '+ age[p] +' years old and his favorite drink is '+ drink[p])
                actions.move('spin_right', 0.6, 8)
                actions.move('stop')
                actions.talk(name[p] +', this is John and ' +name['p1']+'. Their favorite drinks are Coke and '+drink['p1'])
                #Condicao para a segunda pessoa
                if age[p] > bigger:
                    #Pessoa ja sentada sai e vai para sentar do lado do John
                    bigger = age[p]
                    mai='2'
                    person = str(i)
                    #mais nova sai da poltrona
                    actions.talk(name['p1']+' please, sit on the couch next to John')
                    os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p5\'}}"')
                    #Mais velha senta na poltrona
                    actions.talk(name[p]+' seat in the armchair, you are older than '+name['p1'])
                    os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p15\'}}"')
                else:
                    j = 1
                    actions.talk(name[p]+', please, sit on the empty couch')
                    os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p14\'}}"')


            elif i == 2:
                actions.talk('Hi John, '+name['p1']+' and '+ name['p2'])
                actions.move('spin_left', 0.6, 8)
                actions.move('stop')
                actions.talk('This is '+ name[p] + '. He is '+ age[p] +' years old and his favorite drink is '+ drink[p])
                actions.move('spin_right', 0.6, 8)
                actions.move('stop')
                actions.talk(name[p] +', this is John, '+name['p1']+' and '+ name['p2']+'. Their favorite drinks are Coke, '+drink['p1']+' and '+drink['p2'])
                #Condicao para a terceira pessoa
                if age[p]> age['p'+str(mai)]:
                    #Primeira pessoa ja sentada, sai e vai para o outro sofa
                    actions.talk(name['p'+str(mai)]+' please, sit on the empty couch')
                    if mai == '1':
                        os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p5\'}}"')
                    else:
                        os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p16\'}}"')
                    #Mais velha senta na poltrona
                    actions.talk(name[p]+' Seat in the armchair, you are older than '+name['p'+str(mai)])
                    os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p25\'}}"')
                else:
                    if j == 0:
                        actions.talk(name[p]+' Please, sit on the empty couch')
                        os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p24\'}}"')
                    else:
                        actions.talk(name[p]+' Please, sit on the couch next to John')
                        os.system('rosservice call /task_control/receptionist/command "{command: {data: \'p25\'}}"')

        # actions.goto('announcement') #local virado para todos onde ira se comunicar
        actions.talk('Now that we are all comfortable, lets start the party')
        actions.talk('End task')


###########################################################################

        actions.talk('End task')

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
