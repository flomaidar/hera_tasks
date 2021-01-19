# -*- coding: utf-8 -*-

import json
import rospy
import sqlite3
import datetime
import calendar
from random import randint

class spr_data():

    def answer_to_string(self, choices, cmd, template):
        c = [choices[x].values[0] for x in range(0,len(choices))]
        ans = eval(cmd)
        return template.format(*c,_ans=ans)

    def answering_questions(self, speech):
            question = speech.result
            choices = speech.choices
            return self.answer_to_string(
                choices,
                self.question[question][0],
                self.question[question][1])

    def sql_query(self, choices, template):
        c = [choices[x].values[0] for x in range(0,len(choices))]
        query = template.format(*c)

        self.db = sqlite3.connect(self.robot_db)
        self.cursor = self.db.cursor()
        self.cursor.execute(query)
        ans = self.cursor.fetchone()[0]
        self.db.close()

        return ans


    """docstring for speech_words"""
    def __init__(self):

        self.robot_db = rospy.get_param('/robot_resources') + '/robot.db'
        self.db = sqlite3.connect(self.robot_db)
        self.cursor = self.db.cursor()

        self.cursor.execute('''SELECT value, cmd, ans FROM question''')
        self.question = {row[0].encode("utf-8"):[
                         row[1].encode("utf-8"),
                         row[2].encode("utf-8")]
                         for row in self.cursor.fetchall()}

        self.cursor.execute('''SELECT value FROM object''')
        self.object = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM placement''')
        self.placement = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM beacon''')
        self.beacon = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM room''')
        self.room = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM people''')
        self.people = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM gesture''')
        self.gesture = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM posppl''')
        self.posppl = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM posprs''')
        self.posprs = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM gprsng''')
        self.gprsng = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM gprsn''')
        self.gprsn = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM color''')
        self.color = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM category''')
        self.category = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM adja''')
        self.adja = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.cursor.execute('''SELECT value FROM adjr''')
        self.adjr = [row[0].encode("utf-8") for row in self.cursor.fetchall()]

        self.db.close()


        self.spec = self.question.keys()
        self.choices = [
            {'id':'object',     'values':self.object},
            {'id':'placement',  'values':self.placement},
            {'id':'beacon',     'values':self.beacon},
            {'id':'room',       'values':self.room},
            {'id':'people',     'values':self.people},
            {'id':'gesture',    'values':self.gesture},
            {'id':'posppl',     'values':self.posppl},
            {'id':'posprs',     'values':self.posprs},
            {'id':'gprsng',     'values':self.gprsng},
            {'id':'gprsn',      'values':self.gprsn},
            {'id':'color',      'values':self.color},
            {'id':'category',   'values':self.category},
            {'id':'adja',       'values':self.adja},
            {'id':'adjr',       'values':self.adjr}
            ]
