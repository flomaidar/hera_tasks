import traceback
import rospy
import math
import json
import time

from std_msgs.msg import UInt32
from std_msgs.msg import String
from gsr_ros.msg import Opcs
from gsr_ros.srv import StartRequest


from Actions import Actions
class Task():
    """docstring for Task"""
    def __init__(self):
        rospy.sleep(1)

        rospy.init_node('listener', anonymous=True)
        self.message_subscriber = rospy.Subscriber("message", String, self.callback)

        # set vizbox story and publisher
        rospy.set_param('/story/title', 'GoAndGetIt')
        rospy.set_param('/story/storyline',[
            ])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        actions = Actions()

        # task variables
        locals = ['GoalArea','DeliveryArea','FoodArea','LeftPerson','RightPerson']
        #locals = json.loads(actions.question('know_places').result)
        specs = ['go to <locals>','Start task']

        # speech variables
        self.srv = StartRequest()
        self.srv.spec = specs
        #self.srv.choices.append(Opcs(id="robotnames", values=robotnames))
        self.srv.choices.append(Opcs(id="locals", values=locals))
    
        #keeps python from exiting until this node is stopped
        rospy.spin()

        #----
        msg = self.message
        splitted_msg = msg.split()
        size = len(splitted_msg)
        x = 0
        for i in range(size):
            if(splitted_msg[x] == 'to'):
                break
            x+=1
        if(x==1):
            food_name = splitted_msg[0]
            person = splitted_msg[3]
        elif (x==2):
            food_name == splitted_msg[0] + ' ' + splitted_msg[1]
            person == splitted_msg[4]
        elif (x==3):
            food_name = splitted_msg[0] + ' ' + splitted_msg[1] + ' ' + splitted_msg[2]
            person = splitted_msg[5]
        elif (x==4):
            food_name = splitted_msg[0] + ' ' + splitted_msg[1] + ' ' + splitted_msg[2] + ' ' + splitted_msg[3]
            person = splitted_msg[6]


        actions.goto('GoalArea')
        actions.goto('FoodArea')
        coordinates = actions.FindSpecificObject('food_name')
        actions.manip_goal(coordinates, 'pick')
        actions.goto('DeliveryArea')

        if (person == "left"):
            actions.goto('LeftPerson')
        else:
            actions.goto('RightPerson')

        if (self.message == "done"):
            return "success"

    #subscriber
    def callback(self,data):
        rospy.loginfo(rospy.get_caller_id() + "%s", data.data)
        self.message = str(data.data)

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass