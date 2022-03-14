#!/usr/bin/env python

import traceback
import rospy
import math
import json
import time
from gtts import gTTS
import os

from std_msgs.msg import UInt32
from std_msgs.msg import String
from gsr_ros.msg import Opcs
from gsr_ros.srv import StartRequest


from Actions import Actions
class Task():
    def __init__(self):
        rospy.sleep(1)

        # rospy.init_node('listener', anonymous=True)
        # self.message_subscriber = rospy.Subscriber("message", String, self.callback)

        rospy.set_param('/story/title', 'libras_restaurant')
        rospy.set_param('/story/storyline',[
            ])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        actions = Actions()

        robotnames = ['Robot','Hera','Ivy'] 
        locals = ['bin0', 'bin1', 'collection', 'end']

        specs = [
            '<robotnames>',
            '<locals>',
            'Start task'
        ]

        self.srv = StartRequest()
        self.srv.spec = specs
        self.srv.choices.append(Opcs(id="robotnames", values=robotnames))
        self.srv.choices.append(Opcs(id="locals", values=locals))
    
        rospy.spin()

        # i = 1       
        while (True):
        actions.goto('bin0')
    #         rospy.sleep(3)
    #         if i==1:
    #             actions.goto('bin1')
    #             rospy.sleep(3)
    #             # msg = self.message
    #             actions.goto('end')
    #             rospy.sleep(3)
    #             # talk = 'Table 1 asked' + msg
    #             # talking = gTTS(talk, lang='en')
    #             # talking.save('talking.mp3')
    #             # os.system('start talking.mp3')
    #             rospy.sleep(3)
    #             actions.goto('bin1')
    #             rospy.sleep(3)
    #             actions.goto('bin0')
    #             rospy.sleep(3)
    #             i+=1

    #         if i==2:
    #             actions.goto('coleection')
    #             rospy.sleep(3)
    #             # msg = self.message
    #             actions.goto('end')
    #             rospy.sleep(3)
    #             # talk2 = 'Table 2 asked' + msg
    #             # talking2 = gTTS(talk2, lang='en')
    #             # talking2.save('talking2.mp3')
    #             # os.system('start talking2.mp3')
    #             rospy.sleep(3)
    #             actions.goto('coleection')
    #             rospy.sleep(3)
    #             actions.goto('bin0')
    #             rospy.sleep(3)
    #             i-=1
    
    # # def callback(self,data):
    # #     rospy.loginfo(rospy.get_caller_id() + "%s", data.data)
    # #     self.message = str(data.data)

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass