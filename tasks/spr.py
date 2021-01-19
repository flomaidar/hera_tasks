#!/usr/bin/env python

import math
import time
import rospy
import json
import traceback
from random import randint
from gsr_ros.srv import StartRequest
from gsr_ros.msg import Opcs


from std_msgs.msg import UInt32

# from hera.robot import Robot as HERA
from Actions import Actions

from agent.util.enuns import Side

from spr_data import *

class SPR():
    """docstring for SPR"""
    def __init__(self):

        # set vizbox story
        rospy.set_param('/story/title', 'SPR task')
        rospy.set_param('/story/storyline', ['Riddles  game'])
        # vizbox publishers
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        actions = Actions()

        # start agent
        # self.hera = HERA()
        # report.title = 'SPR Report'

        self.questions = ['What is the nickname of the Sydney Harbour Bridge', 'What is the nickname of Sydney','Are Funnel Web Spiders dangerous', 'Where did AC DC start its carreer', 'Where did Richard Clapton start its carreer', 'How strong is Sydney Harbour Bridge', 'Who has the Guinness World Record for the largest swimsuit group', 'What is the oldest street in Australia', 'What can you tell me about the Sydney Opera House', 'What can you tell me about the Grand Organ', 'What can you tell me about the Australian Museum', 'What can you tell me about the Mint Building', 'What can you tell me about the University of Sydney', 'Who attended the National Institute of Dramatic Art', 'What can you tell me about the Great Barrier Reef', 'Are spiders eaten in Australia', 'Where can I find Kangaroo', 'How many kangaroos there are in Australia', 'What is a kangaroo', 'What is a box jellyfish', 'Are there snakes in Australia', 'Do Tasmanian Devil really exist', 'Do Australians like beer', 'Do Australians like wine', 'Are there pink lakes', 'What is the heros name in The Legend of Zelda', 'What are the names of the ghosts who chase Pac Man and Ms. Pac Man', 'What is the name of the Mythbusters crash test dummy', 'What is an Oxford comma', 'Who was the captain of the Enterprise in the pilot episode of Star Trek', 'What is the symbol for the modulus operator in C', 'What function is automatically called at the beginning of a C++ program', 'Which computer programming languages was introduced by IBM in 1957', 'What does the acronym SMTP represent', 'What does the acronym MPEG represent', 'What does the acronym GIMP represent', 'What does the acronym GNU represent', 'Who is considered as the first programmer', 'Has a robot ever killed a person', 'Who was HitchBOT', 'Are self-driving cars safe', 'Who invented the compiler', 'Who created the Python Programming Language', 'Is Mark Zuckerberg a robot', 'What did the robot call its creator', 'Why did you run away', 'What kind of salad do robots like', 'What did you ate for lunch', 'Why did robots get angry so often', 'Why shouldnt R2D2 be allowed in movies', 'What is your favorite style of music']


        self.answer = ['The Coathanger, because of its arch-based design', 'Sin City because organised crime took over the city', 'A Sydney Funnel Web Spider bite can kill a human in 15 minutes, piercing into gloves and fingernails', 'AC/DC stared its carreer here, in Sydney', 'Richard Clapton stared its carreer here, in Sydney.', 'Much, I know it can stand 96 railway engines.', 'Bondi Beach in Sydney, with 1,010 women wearing bikinis in 2007', 'George Street is the oldest street in Australia.', 'It was completed in 1973, took 14 years and 10 thousand construction workers to build', 'With 10,154 pipes, its the largest mechanical tracker-action pipe organ in the world', 'It is Australias oldest natural history museum', 'It was originally built to be a hospital in 1814 and the contractors were paid with 45,000 gallons of rum', 'It was established in 1850 and is the oldest university in Australia', 'Mel Gibson, Judy Davis, Baz Luhrmann, and Cate Blanchett', 'It is the largest organic construction on earth', 'The average person in Australia swallows three spiders a year', 'Kangaroo meat can be purchased from the supermarket and on restaurant. It is leaner and healthier alternative to beef or lamb', 'There are about 40 million kangaroos in Australia', 'Kangaroo is Aboriginal for, I dont understand what you are saying', 'It is the worlds most venomous marine creature', 'Out of the top 25 deadliest snakes in the world, 20 are found in Australia', 'The Tasmanian Devil does exist, and it has the jaw strength of a crocodile', 'Aussies drink about 680 bottles of beer per adult each year', 'They do. There are 60 wine regions in Australia', 'Western Australia is home to a number of Pink Lakes such as Lake Hillier', 'Despite most peoples believes, hes called Link', 'Inky, Blinky, Pinky, and Clyde', 'The Mythbusters crash test dummy is called Buster', 'The hotly contested punctuation before a conjunction in a list', 'The captain of the Enterprise in the pilot episode was Captain Pike', 'The percentage symbol is used as modulus operator in C', 'The main function', 'Fortran was introduced by IBM in 1957', 'SMTP stands for Simple Mail Transport Protocol', 'MPEG stands for Moving Picture Experts Group', 'GNU Image Manipulation Program', 'GNU is a recursive acronym meaning GNU is Not Unix', 'The first programmer was Ada Lovelac', 'The first known case of robot homicide occurred in 1981, when a robotic arm crushed a Japanese Kawasaki factory worker', 'A hitchhiking robot that relied on the kindness of strangers to travel the world and was slain by humans', 'Yes. Car accidents are product of human misconduct', 'Grace Hoper. She wrote it in her spare time', 'Python was invented by Guido van Rossum', 'Sure. Ive never seen him drink water', 'Da-ta', 'I heard an electric can opener', 'Salads made with ice-borg lettuce.', 'I had a byte', 'People kept pushing our buttons.', 'He says so many foul words they have to bleep everything he says!', 'I like electronic and heavy Metal']

        self.robotnames = ['Robot', 'Hera', 'Ivy']
        #self.locals = json.loads(actions.question('know_places').result)

        self.spec = [
            '<robotnames>',
            'go to <locals>',
            'Start task',
            'Leave arena']

        # speech variables
        self.srv = StartRequest()
        self.srv.spec = self.spec
        self.srv.choices.append(Opcs(id="robotnames", values=self.robotnames))
        self.srv.choices.append(Opcs(id="locals", values=self.locals))

        actions.talk('Hello!')
        #actions.pose('door')

        while (True):
            try:
                speech = actions.hear(self.srv)

                if (speech.result == '<robotnames>'):
                    person = actions.face_recognition()
                    actions.talk('Hello ' + person)
                elif (speech.result == 'Start task'):
                    actions.talk('Starting speech and person recognition task!')

                    talk = False
                    while not json.loads(actions.question('is_front_free').result):
                        if not talk:
                            actions.talk('Waiting to open the door')
                            talk = True
                        continue

                    actions.talk('The door is open!')
                    actions.talk('Going to the crowd location')
                    actions.move('foward', seconds=4.0)
                    actions.goto('a')
                    actions.goto('b')
                    actions.goto('crowd')
                    try:
                        actions.head(0.0,0.0)
                        time.sleep(8)
                        people = actions.people()
                        num_people = len(people.people)
                    except Exception as e:
                        print e
                        num_people = 5

                    actions.talk("I'm seeing %d people"%(num_people))

                    female = 2
                    male = num_people - female
                    try:

                        male, female = actions.face_attributes()
                    except Exception as e:
                        print e

                    actions.talk("I see " + str(male) + " man and " + str(female) + " woman!")
                    actions.talk('Who want to play riddles with me?')
                    time.sleep(5)
                    actions.talk('Please, ask me something only after the beep or wait for the next beep.')
                    i = 0
                    while i < 5:
                        try:
                            srv_question = StartRequest()
                            srv_question.spec = self.questions
                            speech = actions.hear(srv_question)
                            if speech.result is '': continue
                            if speech.result in self.questions:
                                # confirm = ''
                                # while not confirm == 'yes':
                                #     actions.talk('Did you ask'+speech.result)
                                #     actions.talk('Say yes or no')
                                #     srv_confirm = StartRequest()
                                #     srv_confirm.spec = ['yes','no']
                                #     speech = actions.hear(srv_confirm)
                                #     follow = speech.result.lower()
                                # if confirm == 'yes':
                                #     index = self.questions.index(speech.result)
                                #     answer = self.answer[index]
                                # else:
                                #     continue
                                index = self.questions.index(speech.result)
                                answer = self.answer[index]
                            else:
                                answer = "Sorry, I could not find an answer to that"
                                actions.talk(answer)
                            i += 1

                        except Exception as e:
                            rospy.logerr(e.message)
                            traceback.print_exc()
                        actions.talk('Finish riddles game')

                    actions.talk("Leaving arena!")
                    actions.talk("Going to end!")
                    actions.goto("end")

            except Exception as e:
                actions.talk('Sorry, I can not do that right now!')
                rospy.logerr(e.message)
                traceback.print_exc()
            except Exception as e:
                rospy.logerr(e.message)
                traceback.print_exc()
            except KeyboardInterrupt:
                rospy.loginfo('Shuting down..')
                traceback.print_exc()
                break

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        SPR()
    except KeyboardInterrupt:
        pass
