import actionlib
import rospy

from hera.msg import poseFeedback, poseResult, poseAction, poseGoal
from hera.msg import gotoFeedback, gotoResult, gotoAction, gotoGoal
from hera.msg import gotoposeFeedback, gotoposeResult, gotoposeAction, gotoposeGoal
from hera.msg import talkFeedback, talkResult, talkAction, talkGoal
from hera.msg import hearFeedback, hearResult, hearAction, hearGoal
from hera.msg import faceFeedback, faceResult, faceAction, faceGoal
from hera.msg import moveFeedback, moveResult, moveAction, moveGoal
#from hera.msg import followFeedback, followResult, followAction, followGoal
from hera.msg import savelocalFeedback, savelocalResult, savelocalAction, savelocalGoal
from hera.msg import headFeedback, headResult, headAction, headGoal

from hera.srv import question

from std_msgs.msg import Float32

from manip3.srv import Manip3
from manip3.msg import Manip3_Goal

from hera_objects.srv import FindObject, FindSpecificObject

from people.srv import Once

from social_worlds.srv import *

class Actions():
    """docstring for Actions."""
    def __init__(self):

        # init clients
        self.question = rospy.ServiceProxy('/question', question)
        self.manipulator = rospy.ServiceProxy('/manipulator', Manip3)
        self.objects = rospy.ServiceProxy('/objects', FindObject)
        self.specific_object = rospy.ServiceProxy('/specific_object', FindSpecificObject)
        self.people = rospy.ServiceProxy('/people/once', Once)
        self.client_pose = actionlib.SimpleActionClient('/pose', poseAction)
        self.client_goto = actionlib.SimpleActionClient('/goto', gotoAction)
        self.client_gotopose = actionlib.SimpleActionClient('/gotopose', gotoposeAction)
        self.client_talk = actionlib.SimpleActionClient('/talk', talkAction)
        self.client_hear = actionlib.SimpleActionClient('/hear', hearAction)
        self.client_face = actionlib.SimpleActionClient('/face', faceAction)
        self.client_move = actionlib.SimpleActionClient('/move', moveAction)
        #self.client_follow = actionlib.SimpleActionClient('/follow', followAction)
        self.client_savelocal = actionlib.SimpleActionClient('/savelocal', savelocalAction)
        self.client_head = actionlib.SimpleActionClient('/head', headAction)

        #wait for servers
        print 'wait for server: question'
        rospy.wait_for_service('/question')
        print 'wait for server: manipulator'
        #rospy.wait_for_service('/manipulator')
        print 'wait for server: objects'
        #rospy.wait_for_service('/objects')
        print 'wait for server: specific_object'
        #rospy.wait_for_service('/specific_object')
       	print 'wait for server: people'
        # rospy.wait_for_service('/people/once')


        print 'wait for server: pose'
        self.client_pose.wait_for_server()
        print 'wait for server: goto'
        self.client_goto.wait_for_server()
        print 'wait for server: gotopose'
        self.client_gotopose.wait_for_server()
        print 'wait for server: talk'
        self.client_talk.wait_for_server()
        print 'wait for server: hear'
        self.client_hear.wait_for_server()
        print 'wait for server: face'
        self.client_face.wait_for_server()
        print 'wait for server: move'
        self.client_move.wait_for_server()
        #print 'wait for server: follow'
        #self.client_follow.wait_for_server()
        print 'wait for server: savelocal'
        self.client_savelocal.wait_for_server()
        print 'wait for server: head'
        #self.client_head.wait_for_server()

    def question(q):
        resp = self.question(q)
        return resp.result

    def savelocal(self, local):
        goal = savelocalGoal(location=local)
        self.client_savelocal.send_goal(goal)
        self.client_savelocal.wait_for_result()
        return self.client_savelocal.get_result()

    def manip(self, tipo="", x=0.0, y=0, z=0, rx=0, ry=0, rz=0):
        m3 = Manip3_Goal()
        m3.x = x
        m3.y = y
        m3.z = z
        m3.rx = rx
        m3.ry = ry
        m3.rz = rz
        resp = self.manipulator(tipo, m3)
        return True if resp.result == 'SUCCEEDED' else False

    def manip_goal(self, goal, tipo=""):
	    resp = self.manipulator(tipo, goal)
	    return True if resp.result == 'SUCCEEDED' else False

    def FindObject(self, condition=""):
        resp = self.objects(condition)
        values = [resp.position.x, resp.position.y, resp.position.z]
        if all(v == 0.0 for v in values):
            return None
        else:
            return resp.position

    def FindSpecificObject(self, tipo=""):
        resp = self.specific_object(tipo)
        values = [resp.position.x, resp.position.y, resp.position.z]
        if all(v == 0.0 for v in values):
            return None
        else:
            return resp.position

    def head(self, pan, tilt):
        goal = headGoal(pan=Float32(pan),tilt=Float32(tilt))
        self.client_head.send_goal(goal)
        self.client_head.wait_for_result()
        return self.client_head.get_result()

    def pose(self, location):
        goal = poseGoal(location=location)
        self.client_pose.send_goal(goal)
        self.client_pose.wait_for_result()
        return self.client_pose.get_result()

    def people(self):
        resp = self.people()
        return resp.people

    def goto(self, location, wait=True):
        if location==None:
            self.client_goto.cancel_all_goals()
            return
        goal = gotoGoal(location=location)
        self.client_goto.send_goal(goal)
        if wait:
            self.client_goto.wait_for_result()
            return self.client_goto.get_result()

    def gotopose(self, location, frame, wait=True):
        if location==None:
            self.client_goto.cancel_all_goals()
            return
        goal = gotoGoal(location=location, reference=frame)
        self.client_goto.send_goal(goal)
        if wait:
            self.client_goto.wait_for_result()
            return self.client_goto.get_result()

    def talk(self, phrase):
        goal = talkGoal(phrase=phrase)
        self.client_talk.send_goal(goal)
        self.client_talk.wait_for_result()
        return self.client_talk.get_result()

    def hear(self, srv):
        goal = hearGoal(spec=srv.spec, choices=srv.choices)
        self.client_hear.send_goal(goal)
        self.client_hear.wait_for_result()
        return self.client_hear.get_result()

    def face(self):
        goal = faceGoal()
        self.client_face.send_goal(goal)
        self.client_face.wait_for_result()
        return self.client_face.get_result()

    def move(self, cmd, vel=0.2, seconds=0.0):
        goal = moveGoal(cmd=cmd, vel=vel, seconds=seconds)
        self.client_move.send_goal(goal)
        self.client_move.wait_for_result()
        return self.client_move.get_result()

    def follow(self, location, wait=True):
        if location==None:
            self.client_follow.cancel_all_goals()
            return

        goal = followGoal(location=location)
        self.client_follow.send_goal(goal)
        if wait:
            self.client_follow.wait_for_result()
            return self.client_follow.get_result()
