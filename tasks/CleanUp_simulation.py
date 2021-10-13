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
        rospy.set_param('/story/title', 'CleanUp')
        rospy.set_param('/story/storyline',[
            ])
        self.pub_vizbox_step = rospy.Publisher('/challenge_step', UInt32, queue_size=80)

        actions = Actions()
        objects_class = [
        "food",
        "food",
        "food",
        "food",
        "food",
        "food",
        "food",
        "food",
        "food",
        "food",
        "food",
        "food",
        "food",
        "food",
        "food",
        "food",
        "food",
        "kitchen",
        "kitchen",
        "kitchen",
        "kitchen",
        "kitchen",
        "kitchen",
        "kitchen",
        "kitchen",
        "kitchen",
        "shape",
        "shape",
        "shape",
        "shape",
        "shape",
        "shape",
        "shape",
        "shape",
        "shape",
        "shape",
        "shape",
        "task",
        "tool",
        "tool"]

        objects_name = [
        "jell-o chocolate pudding box",
        "cheez-it cracker box",
        "domino sugar box",
        "master chef coffee can",
        "french's mustard bottle",
        "plastic apple",
        "plastic banana",
        "plastic lemon",
        "plastic orange",
        "plastic peach",
        "plastic pear",
        "plastic plum",
        "plastic strawberry",
        "spam potted meat can",
        "jell-o strawberry gelatin box",
        "tomato soup can",
        "starkist tuna fish can",
        "bowl",
        "cleanser bottle",
        "fork",
        "mug",
        "pitcher base",
        "plate",
        "spatula",
        "sponge",
        "spoon",
        "baseball",
        "chain",
        "cups",
        "dice",
        "foam bricks",
        "golf ball",
        "marbles",
        "mini soccer ball",
        "racquetball",
        "soft ball",
        "tennis ball",
        "toy airplane",
        "clamps",
        "large marker"]

        locals_colect = [
        "Table_corner_1",
        "Table_corner_2"]

        locals_deposit = [
        'Drawer_left',
        'Drawer_top', 
        'Drawer_bottom', 
        'Tray_A', 
        'Tray_B', 
        'Container_A', 
        'Container_B',
        'Bin_A',
        'Bin_B']
        l=0
        while True:
            while True:
                # Setar dois locais no mapa, que peguem as pontas da mesa para que seja manipulado na mesa
                actions.goto(locals_colect[l])

                # Saber qual é o objeto mais próximo e qual o nome desse objeto
                coordinates_closest = actions.FindObject('closest')
                if coordinates_closest == None:
                    l += 1
                    break 
                
                for i in len(objects_name):
                    coordinates_name = actions.FindSpecificObject(objects_name[i])
                    if coordinates_closest == coordinates_name:
                        name_object     = objects_name[i]
                        class_object    = objects_class[i]
                        break
                
                actions.manip_goal(coordinates_closest, 'pick')
                actions.manip_goal('front')

                if class_object == "food":
                    ## locais que depositam comida
                    ## pensar como caracterizar e mudar qual será
                    actions.goto(locals_deposit[3])
                    actions.goto(locals_deposit[4])

                elif class_object == "kitchen":
                    ## locais que depositam objetos da cozinha
                    actions.goto(locals_deposit[5])

                elif class_object == "shape":
                    actions.goto(locals_deposit[0])
                
                elif class_object == "tool":
                    actions.goto(locals_deposit[1])
                    actions.goto(locals_deposit[2])
                
                elif class_object == "task":
                    actions.goto(locals_deposit[7])

                # Abrir em um local x -- passar as coordenadas
                actions.manip_goal('', 'open')

    

if __name__ == '__main__':
    try:
        rospy.init_node('Task')
        Task()
    except KeyboardInterrupt:
        pass
