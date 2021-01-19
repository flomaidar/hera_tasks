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
        

    actions.talk('Waiting for visitors')
    for i in range(4):
        p='p'+str(i+1)
        #Pessoa entra e para em frente a hera
        actions.talk('Hi! my name is Hera and i am here to help you. Please, what is your name?')
        speech = actions.hear(srv_names)
        name[p] = speech.result
        actions.talk('How can i help you, '+ name[p]+'?')
        speech = actions.hear(srv_question)
        question[p] = speech.result
        
        ### Condicional
        if question[p] == question_list[0]:
            answer = 'You can grab something from this balcony beside me, or go to the kitchen wich is located right behind it'
            if places['kitchen'] == '':
                actions.talk(answer)
                places['kitchen'] = name[p]
            else:
                actions.talk(answer + 'you will find '+ places['kitchen'])
                places['kitchen'] = [places['kitchen'], name[p]] 
            
        elif question[p] == question_list[1]:
            if places['office'] == '':
                actions.talk('You can go to the office, you will find a computer there, it is located at the second door to the right')
                places['office'] = name[p]
            elif places['bedroom'] == '':
                actions.talk(places['office']+' is using offices computer, but you can find a laptop at the bedroom, it is the first door right after the living room')
                places['bedroom'] = name[p]
            else:
                actions.talk('i am sorry, all of our computers are in use at this moment, let me help you with something else')
        
        elif question[p] == question_list[2]:
            if places['living_room'] == '':
                answer = 'you can sit on the couch right beside the entrance of the house'
                actions.talk(answer)
                places['living_room'] == name[p]
            else:
                actions.talk(answer + ', you will find '+ places['living_room']+ ' there')
                places['living_room'] == [places['living_room'], name[p]]

        elif question[p] == question_list[3]:
            if places['bedroom'] == '':
                actions.talk('you can find a bookshelf in the bedroom, it is the first door right after the living room')
                places['bedroom'] == name[p]
            else:
                actions.talk('you can find a bookshelf in the bedroom, it is the first door right after the living room, you will find '+ places['bedroom']+' there')
                places['bedroom'] == [places['bedroom'], name[p]]
        
        elif question[p] == question_list[4]:
            if places['garden'] == '':
                actions.talk('we have sun chairs in our garden, in the second door at right, after the office')
                places[''] == name[p]
            else:
                actions.talk('we have sun chairs in our garden, in the second door at right, after the office, you will find '+ places['garden']+' there')
                places['garden'] == [places['garden'], name[p]]

    actions.talk('Finished my work today')
        
if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass                    

        
        

        
        
        