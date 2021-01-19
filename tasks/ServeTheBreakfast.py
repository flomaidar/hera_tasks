#!/usr/bin/env python

import traceback
import rospy
import math

from agent.util.agent_exception import AgentException
from hera.robot import Robot as HERA
from std_msgs.msg import UInt32

class Task():
    """docstring for Task"""
    def __init__(self):
        rospy.init_node('Task')
        rospy.sleep(1)

        # set vizbox story and publisher
        rospy.set_param('/story/title', 'ServeTheBreakfast')
        rospy.set_param('/story/storyline', [])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        # start agent
        self.robot = HERA()

        # task variables
        self.spec = [
            '<robotnames>',
            'go to <locals>',
            'Start task'
        ]
        self.robotnames = ['Robot','Hera','Ivy']
        self.locals = self.robot.get_sensors('locals').strings
        self.choices = [
            {'id': "robotnames", 'values': self.robotnames},
            {'id': "locals",     'values': self.locals}]

        #
        self.run_robot(self.robot)

    def run_robot(self, robot):

        robot.actions.talk.execute('Hello!')
        robot.actions.pose.execute('start')

        while (True):
            try:
                speech = robot.actions.hear.execute(self.spec, self.choices)

                if (speech.result == '<robotnames>'):
                    person = robot.actions.face_recognition.execute()
                    robot.actions.talk.execute('Hello ' + person)
                elif(speech.result == 'go to <locals>'):
                    local = speech.choices[0].values[0]
                    robot.actions.talk.execute("Going to " + local)
                    robot.actions.goto_location.execute(local)
                elif (speech.result == 'Start task'):

                    pass

            except AgentException as e:
                robot.actions.talk.execute("Sorry, I can not do that right now!")
                traceback.print_exc()
            except Exception as e:
                traceback.print_exc()

if __name__ == '__main__':
    Task()
