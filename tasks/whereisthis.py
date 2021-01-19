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

        question_list = ['where can i eat something',
            'where can i use a computer',
            'where can i chill out',
            'where can i find a book to read',
            'where can i take a sunbath']
        srv_question = StartRequest()
        srv_question.spec = question_list
        
        srv_response = StartRequest()
        srv_response.spec = [
            'yes',
            'no'
        ]

        name = {
            'p1':'',
            'p2':'',
            'p3':'',
            'p4':''
        }
        question = {
            'p1':'',
            'p2':'',
            'p3':'',
            'p4':''
        }
        places = {
            'kitchen':'',
            'office':'',
            'living_room':'',
            'bedroom':'',
            'garden':''
        }
        people_place = {
            'p1':'',
            'p2':'',
            'p3':'',
            'p4':''
        }
        

        # actions.talk('Waiting for visitors')
        for i in range(3):
            p='p'+str(i+1)
            #Pessoa entra e para em frente a hera
            while name[p] == '':
                actions.talk('Hi! my name is Hera and i am here to help you. Please, what is your name?')
                speech = actions.hear(srv_names)
                name[p] = speech.result
                actions.talk('Your name is '+name[p]+' right?')
                speech2 = actions.hear(srv_response)
                response = speech2.result
                if response == 'yes':
                    break
                else:
                    name[p] = ''
            
            while question[p] == '':    
                actions.talk('How can i help you, '+ name[p]+'?')
                speech = actions.hear(srv_question)
                question[p] = speech.result
                actions.talk('You asked '+question[p]+', right?')
                speech = actions.hear(srv_response)
                response = speech.result
                if response == 'yes':
                    break
                else:
                    name[p] = ''
            
            ### Condicional
            if question[p] == question_list[0]:
                
                answer = 'You can grab something from this balcony beside me, or go to the kitchen wich is located right behind the balcony, just move forward'
                if places['kitchen'] == '':
                    actions.talk(answer)
                    places['kitchen'] = name[p]
                else:
                    actions.talk(answer + ' you will find '+ places['kitchen'])
                people_place[p] = 'kitchen'
                
            elif question[p] == question_list[1]:
                if places['office'] == '':
                    actions.talk('You can go to the office, you will find a computer there, in front of the kitchen, just move forward and turn right in the second door')
                    places['office'] = name[p]
                elif places['bedroom'] == '':
                    actions.talk(places['office']+' is using offices computer, but you can find a laptop at the bedroom, it is the first door to your right')
                    places['bedroom'] = name[p]
                else:
                    actions.talk('i am sorry, all of our computers are in use at this moment')
            
            elif question[p] == question_list[2]:
                if places['living_room'] == '':
                    answer = 'you can sit on that couch over there, right beside the entrance of the house'
                    actions.talk(answer)
                    places['living_room'] == name[p]
                else:
                    actions.talk(answer + ', you will find '+ places['living_room']+ ' there')
                people_place[p] = 'living_room'
                    

            elif question[p] == question_list[3]:
                if places['bedroom'] == '':
                    actions.talk('you can find a bookshelf in the bedroom, right beside the bed, it is located in the first door to your right.')
                    places['bedroom'] == name[p]
                else:
                    actions.talk('you can find a bookshelf in the bedroom, right beside the bed, it is located in the first door to your right, you will find '+ places['bedroom']+' there')
                people_place[p] = 'bedroom'
                    
            
            elif question[p] == question_list[4]:
                if places['garden'] == '':
                    actions.talk('we have sun chairs in our garden, in front of the kitchen, just move forward and turn right in the second door, than you move forward and pass the office')
                    places['garden'] == name[p]
                else:
                    actions.talk('we have sun chairs in our garden, in front of the kitchen, just move forward and turn right in the second door, than you move forward and pass the office, you will find '+ places['garden']+' there')
                people_place[p] = 'garden'
        
        for i in range(3):
            p='p'+str(i+1)
            actions.talk('hey, '+name[p]+', how was at '+people_place[p]+'? Can i help you with something else?')
            question[p] = ''
            places[people_place[p]] = ''
            while question[p] == '':
                speech = actions.hear(srv_question)
                question[p] = speech.result
                actions.talk('You asked '+question[p]+', right?')
                speech = actions.hear(srv_response)
                response = speech.result
                if response == 'yes':
                    break
                else:
                    question[p] = ''

            if question[p] == question_list[0]:
                
                answer = 'You can grab something from this balcony beside me, or go to the kitchen wich is located right behind the balcony, just move forward'
                if places['kitchen'] == '':
                    actions.talk(answer)
                    places['kitchen'] = name[p]
                else:
                    actions.talk(answer + ' you will find '+ places['kitchen'])
                people_place[p] = 'kitchen'
                
            elif question[p] == question_list[1]:
                if places['office'] == '':
                    actions.talk('You can go to the office, you will find a computer there, in front of the kitchen, just move forward and turn right in the second door')
                    places['office'] = name[p]
                elif places['bedroom'] == '':
                    actions.talk(places['office']+' is using offices computer, but you can find a laptop at the bedroom, it is the first door to your right')
                    places['bedroom'] = name[p]
                else:
                    actions.talk('i am sorry, all of our computers are in use at this moment')
            
            elif question[p] == question_list[2]:
                if places['living_room'] == '':
                    answer = 'you can sit on that couch over there, right beside the entrance of the house'
                    actions.talk(answer)
                    places['living_room'] == name[p]
                else:
                    actions.talk(answer + ', you will find '+ places['living_room']+ ' there')
                people_place[p] = 'living_room'
                    

            elif question[p] == question_list[3]:
                if places['bedroom'] == '':
                    actions.talk('you can find a bookshelf in the bedroom, right beside the bed, it is located in the first door to your right.')
                    places['bedroom'] == name[p]
                else:
                    actions.talk('you can find a bookshelf in the bedroom, right beside the bed, it is located in the first door to your right, you will find '+ places['bedroom']+' there')
                people_place[p] = 'bedroom'
                    
            
            elif question[p] == question_list[4]:
                if places['garden'] == '':
                    actions.talk('we have sun chairs in our garden, in front of the kitchen, just move forward and turn right in the second door, than you move forward and pass the office')
                    places['garden'] == name[p]
                else:
                    actions.talk('we have sun chairs in our garden, in front of the kitchen, just move forward and turn right in the second door, than you move forward and pass the office, you will find '+ places['garden']+' there')
                people_place[p] = 'garden'
            




    ###########################################################################

            

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass