#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import math
import rospy
import telegram
import json
import time
from emoji import emojize, demojize

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

# from robot_model.hera.hera import Hera
# from hera.robot import Robot as HERA
from Actions import Actions

from geometry_msgs.msg import Twist

stop = u'•'
foward = u'↑'
backward = u'↓'
left = u'←'
right = u'→'
spin_left = u'⭯'
spin_right = u'⭮'
spin_left_front = u'↶'
spin_left_back = u'⤾'
spin_right_front = u'↷'
spin_right_back = u'⤿'
up_left = u'↖'
up_right = u'↗'
down_left = u'↙'
down_right = u'↘'
vel_up = ':red_triangle_pointed_up:'
vel_down = ':red_triangle_pointed_down:'
close = ':cross_mark:'

def chunkIt(seq, num):
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + num)])
        last += num
    return out

class Bot():
    """docstring for Bot."""
    def __init__(self):

        self.cont = 0
        self.drink = 'bebida'

        # start agent
        # self.hera = HERA()
        self.hera = Actions()

        self.vel = 0.3

        self.token='681796380:AAHfmEQFSK8uTacxL8p-stLungtqE8SOPnw'
        updater = Updater(token=self.token, use_context = True)
        dispatcher = updater.dispatcher

        f1_handler 	    = CommandHandler('f', self.f1)

        hello_handler       = CommandHandler('hello', self.hello)
        help_handler        = CommandHandler('help', self.help)
        talk_handler        = CommandHandler('talk', self.talk)
        goto_handler        = CommandHandler('goto', self.goto)
        move_handler        = CommandHandler('move', self.move)
        ps_handler          = CommandHandler('ps', self.ps)
        savelocal_handler   = CommandHandler('savelocal', self.savelocal)
        manip_handler       = CommandHandler('manip', self.manip)

        unknown_handler     = MessageHandler(Filters.command, self.unknown)
        echo_handler        = MessageHandler(Filters.text, self.echo)

        dispatcher.add_handler(f1_handler)

        dispatcher.add_handler(hello_handler)
        dispatcher.add_handler(help_handler)
        dispatcher.add_handler(talk_handler)
        dispatcher.add_handler(goto_handler)
        dispatcher.add_handler(move_handler)
        dispatcher.add_handler(ps_handler)
        dispatcher.add_handler(savelocal_handler)

        dispatcher.add_handler(unknown_handler)
        dispatcher.add_handler(echo_handler)

        updater.start_polling(poll_interval=0.1)


##############################
    def f1(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,text='Executando f1')
        self.hera.talk("Iniciando tarefa final")
        print update.message.chat_id

        self.hera.talk("bom dia, meu nome eh HERA, uma assistente pessoal.")
        self.hera.talk("Bem vindos ao ambiente ati rome.")
        self.hera.talk("Aqui eh onde assistentes como eu saum desenvolvidos e testados.")
        self.hera.talk("Normalmente eu converso em inglez com as pessoas, mas eu aprendi a falar portugues especialmente para esta apresentassaum")

        self.hera.talk("Irei demonstrar agora uma de minhas aplicassonhis como assistente de ambientes hospitalares")
        self.hera.talk("Fiquem a vontade e espero que aproveitem")

        self.hera.talk("Agora irei aguardar por novos pacientes")
        self.hera.goto('reception')
        time.sleep(5)

        self.hera.talk("Bem vindo ao hospital at romi")
        self.hera.talk("por favor, siga-me para a sala de espera")
        self.hera.goto('sofa')
        self.hera.talk("por favor, aguarde um momento. irei buscar algo para voce beber")
        self.hera.goto('refrigerator0')


        bot.send_message(chat_id=887545041,
            text='Oi, aqui é a HERA.')
        self.hera.talk("Oi, aqui eh a HERA.")

        bot.send_message(chat_id=887545041,
            text='Esse é um dos sistemas de interação com humano que eu possuo.')
        self.hera.talk("Esse eh um dos sistemas de interassaum com humano que eu possuo.")

        bot.send_message(chat_id=887545041,
            text='Com este sistema, é possível que nós comuniquemos mesmo de longe.')
        self.hera.talk("Com este sistema, eh possivel que nos comuniquemos mesmo de longe.")


        bot.send_message(chat_id=887545041,
            text='Agora estou na cozinha do hospital. Estas são as bebidas disponiveis:')
        self.hera.talk("Agora estou na cozinha do hospital. Estas sao as bebidas disponiveis:")

        bot.send_photo(chat_id=887545041, photo=open('/home/robotathome/catkin_hera/Final.jpg', 'rb'))

        bot.send_chat_action(chat_id=887545041,
            action=telegram.ChatAction.TYPING)
        bot.send_message(chat_id=887545041,
            text='O que voce deseja beber?')
        self.hera.talk("O que voce deseja beber?")


##############################

    def hello(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
            text='Hello, my name is HERA! How can I /help you?')

    def help(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
            text='Help:\n' +
            '/hello - Show a welcome message.\n' +
            '/help - Show help.\n' +
            '/talk - Use followed by a phrase to make the robot to talk.\n' +
            '/goto - Send the robot to a location.\n' +
            '/move - Teleoperate the robot.\n' +
            '/ps - Take a printscreen from robot monitor.\n' +
            '/savelocal - Save robot\'s current local.')

    def talk(self, bot, update):
        phrase = update.message.text.replace('/talk', '')
        if(phrase != ''):
            self.hera.talk(phrase)
            # bot.send_chat_action(chat_id=update.message.chat_id,
            #     action=telegram.ChatAction.RECORD_AUDIO)
            # bot.send_chat_action(chat_id=update.message.chat_id,
            #     action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=update.message.chat_id, text=phrase)
            # bot.send_audio(chat_id=update.message.chat_id, voice=open('/home/robotathome/.ros/talk.mp3', 'rb'))

    def goto(self, bot, update):
        local = update.message.text.replace('/goto ', '')
	locals = json.loads(self.hera.question('know_places').result)

#        locals = [
#            'living room', 'end', 'office', 'garage', 'shelf', 'start',
#            'corridor', 'bedroom', 'door', 'chair', 'table', 'kitchen']

        if(local == 'None'):
            reply_markup = telegram.ReplyKeyboardRemove()
            self.hera.goto(None)
            bot.send_message(chat_id=update.message.chat_id,
                text='Stopping move_base.')
            return

        if(local not in locals):
            cmds = ['/goto ' + s for s in locals]
            custom_keyboard = chunkIt(cmds, 2)
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
            # bot.send_chat_action(chat_id=update.message.chat_id,
            #     action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=update.message.chat_id,
                text='Choose a valid destination:',
                reply_markup=reply_markup)
        else:
            reply_markup = telegram.ReplyKeyboardRemove()
            # bot.send_chat_action(chat_id=update.message.chat_id,
            #     action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=update.message.chat_id,
                text='Going to ' + local +' ...',
                reply_markup=reply_markup)
            self.hera.goto(local)
            # bot.send_chat_action(chat_id=update.message.chat_id,
            #     action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=update.message.chat_id,
                text='I have reached the ' + local + '.')

    def move(self, bot, update):
        custom_keyboard = [
            [up_left,   spin_left_front, foward,   spin_right_front, up_right,   emojize(vel_up)],
            [left,      spin_left,       stop,     spin_right,       right,      emojize(vel_down)],
            [down_left, spin_left_back,  backward, spin_right_back,  down_right, emojize(close)]]

        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
        bot.send_message(chat_id=update.message.chat_id,
            text='Choose a command:\n vel = ' + str(self.vel),
            reply_markup=reply_markup)

    def ps(self, bot, update):
        os.system('gnome-screenshot -w -f /tmp/ps.png')
        # bot.send_chat_action(chat_id=update.message.chat_id,
        #     action=telegram.ChatAction.UPLOAD_PHOTO)
        bot.send_photo(chat_id=update.message.chat_id, photo=open('/tmp/ps.png', 'rb'))

    def savelocal(self, bot, update):
        local = update.message.text.replace('/savelocal', '')
        if(local == ''):
            bot.send_message(chat_id=update.message.chat_id,
                text='Send this command with a local name.')
        else:
            local = local.replace(' ', '')
	    bot.send_message(chat_id=update.message.chat_id,
                text=local)
            self.hera.savelocal(local)
            bot.send_message(chat_id=update.message.chat_id,
                text='New local saved with success.')

    def manip(self, bot, update):
        command = update.message.text.replace('/manip', '')
        if(command == ''):
            bot.send_message(chat_id=update.message.chat_id,
                text='Send this command with a command name.')
        else:
            command = local.replace(' ', '')
	    bot.send_message(chat_id=update.message.chat_id,
                text=command)
            if(command=="point"):
                self.hera.manip("point", 0)
                bot.send_message(chat_id=update.message.chat_id,
                    text='Robot pointing to front.')
            if(command=="close"):
                self.hera.manip("close")
                bot.send_message(chat_id=update.message.chat_id,
                    text='Manip close.')
            if(command=="open"):
                self.hera.manip("open")
                bot.send_message(chat_id=update.message.chat_id,
                    text='Manip open.')

    def unknown(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
            text='Sorry, I didn\'t understand that command.')


    def echo(self, bot, update):
        cmd=update.message.text

        if(cmd == '1'):
            self.drink = 'suco de laranja'

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='OK eu vou pegar o suco de laranja')

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='irei levar sua bebida em breve')

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='Enquanto isso, irei realizar sua triagem.')

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='por favor, responda algumas questoes.')

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='Você sente alguma dor?')


        elif(cmd == '2'):
            self.drink = 'nescau'

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='OK eu vou pegar o nescau')

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='irei levar sua bebida em breve')

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='Enquanto isso, irei realizar sua triagem.')

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='por favor, responda algumas questoes.')

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='Você sente alguma dor?')


        elif(cmd == '3'):
            self.drink = 'refrigerante'

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='OK eu vou pegar o refrigerante')

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='irei levar sua bebida em breve')

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='Enquanto isso, irei realizar sua triagem.')

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='por favor, responda algumas questoes.')

            bot.send_chat_action(chat_id=887545041,
                action=telegram.ChatAction.TYPING)
            bot.send_message(chat_id=887545041,
                text='Você sente alguma dor?')


        elif(cmd == 'Sim' or cmd == 'Nao'):
            if (self.cont == 0):
                self.cont = self.cont+1
                bot.send_chat_action(chat_id=887545041,
                    action=telegram.ChatAction.TYPING)
                bot.send_message(chat_id=887545041,
                    text='Você se sente febril?')
            elif (self.cont == 1):
                self.cont = self.cont+1
                bot.send_chat_action(chat_id=887545041,
                    action=telegram.ChatAction.TYPING)
                bot.send_message(chat_id=887545041,
                    text='Sente algum enjôo?')
            elif (self.cont == 2):
                self.cont = self.cont+1
                bot.send_chat_action(chat_id=887545041,
                    action=telegram.ChatAction.TYPING)
                bot.send_message(chat_id=887545041,
                    text='Obrigada!')

                bot.send_chat_action(chat_id=887545041,
                    action=telegram.ChatAction.TYPING)
                bot.send_message(chat_id=887545041,
                    text='Em breve darei seu diagnóstico.')


                self.hera.talk("o paciente deseja um " + self.drink)
                self.hera.head(0.0,0.45)
                self.hera.talk('eu vou procurar pelo objeto')
                #pick the object
                aux = False
                coordinates = self.hera.FindObject('closest')
                if not coordinates == None:
                    coordinates.z += 0.03
                    self.hera.talk('vou tentar pegar')
                    aux = self.hera.manip_goal(coordinates, 'pick')
                    if not aux:
                        self.hera.talk('eu nao consigo pegar sozinha')
                        self.hera.talk("por favor, coloque no meu manipulador")
                        self.hera.manip('open')
                        self.hera.manip('', x=0.35, y=0.0, z=0.3)
                        self.hera.talk("eu vou fechar minha maum")
                        time.sleep(5)
                        self.hera.manip('close')
                        self.hera.manip('home')
                else:
                    self.hera.talk('eu naum consigo pegar sozinha')
                    self.hera.talk("por favor, coloque no meu manipulador")
                    self.hera.manip('open')
                    self.hera.manip('', x=0.35, y=0.0, z=0.3)
                    self.hera.talk("eu vou fechar minha maum")
                    time.sleep(5)
                    self.hera.manip('close')
                    self.hera.manip('home')
                self.hera.goto('sofa')


                self.hera.talk("Oi, estou de volta com sua bebida")
                self.hera.talk("Por favor, pegue sua bebida em meu manipulador")

                self.hera.manip('', x=0.38, y=0.0, z=0.1)
                self.hera.talk("Eu vou soltar em 5 segundos")
                time.sleep(5)
                self.hera.manip('open')
                self.hera.manip('reset')

                self.hera.talk("Seu diagnostico esta pronto!")
                self.hera.talk("Seu caso nao eh grave, mas em breve o doutor vira te examinar.")
                self.hera.talk("Obrigada por esperar.")

                #self.hera.goto('sofa')



        elif(cmd == up_left):
            self.hera.move('up_left', self.vel)
        elif(cmd == spin_left_front):
            self.hera.move('spin_left_front', self.vel)
        elif(cmd == foward):
            self.hera.move('foward', self.vel)
        elif(cmd == spin_right_front):
            self.hera.move('spin_right_front', self.vel)
        elif(cmd == up_right):
            self.hera.move('up_right', self.vel)
        elif(cmd == left):
            self.hera.move('left', self.vel)
        elif(cmd == spin_left):
            self.hera.move('spin_left', self.vel)
        elif(cmd == stop):
            self.hera.move('stop', self.vel)
        elif(cmd == spin_right):
            self.hera.move('spin_right', self.vel)
        elif(cmd == right):
            self.hera.move('right', self.vel)
        elif(cmd == down_left):
            self.hera.move('down_left', self.vel)
        elif(cmd == spin_left_back):
            self.hera.move('spin_left_back', self.vel)
        elif(cmd == backward):
            self.hera.move('backward', self.vel)
        elif(cmd == spin_right_back):
            self.hera.move('spin_right_back', self.vel)
        elif(cmd == down_right):
            self.hera.move('down_right', self.vel)

        elif(demojize(cmd) == vel_up):
            self.vel += 0.02
            bot.send_message(chat_id=update.message.chat_id,
                text='vel = ' + str(self.vel))
            pass
        elif(demojize(cmd) == vel_down):
            self.vel -= 0.02
            bot.send_message(chat_id=update.message.chat_id,
                text='vel = ' + str(self.vel))
            pass
        elif(demojize(cmd) == close):
            reply_markup = telegram.ReplyKeyboardRemove()
            bot.send_message(chat_id=update.message.chat_id,
                text='Close teleop control.',
                reply_markup=reply_markup)
        else:
            pass

if __name__ == '__main__':
    try:
        rospy.init_node('Bot')
        Bot()
    except KeyboardInterrupt:
        pass
