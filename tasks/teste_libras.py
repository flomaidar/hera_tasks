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
        rospy.set_param('/story/title', 'teste_libras')
        rospy.set_param('/story/storyline',[
            ])
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

        ########################################################################
        ########################################################################

        i = 1
        while (True):
            # actions.goto('bin0')
            rospy.sleep(3)
            if i==1:
                actions.goto('bin1')
                actions.talk('Recebendo pedido')
                rospy.sleep(3)
                # msg = self.message
                actions.goto('end')
                rospy.sleep(3)
                # talk = 'Table 1 asked' + msg
                # talking = gTTS(talk, lang='en')
                # talking.save('talking.mp3')
                # os.system('start talking.mp3')
                rospy.sleep(3)
                actions.goto('bin1')
                rospy.sleep(3)
                actions.goto('bin0')
                rospy.sleep(3)
                i+=1
            if i==2:
                actions.goto('coleection')
                rospy.sleep(3)
                # msg = self.message
                actions.goto('end')
                rospy.sleep(3)
                # talk2 = 'Table 2 asked' + msg
                # talking2 = gTTS(talk2, lang='en')
                # talking2.save('talking2.mp3')
                # os.system('start talking2.mp3')
                rospy.sleep(3)
                actions.goto('coleection')
                rospy.sleep(3)
                actions.goto('bin0')
                rospy.sleep(3)
                i-=1

        # def callback(self,data):
        # rospy.loginfo(rospy.get_caller_id() + "%s", data.data)
        # self.message = str(data.data)

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass