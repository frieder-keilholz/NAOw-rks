#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Julia Reinke"
__version__ = "19.06.2020"
__email__ = "jure5622@th-wildau.de"
"""
This class is the implementation of blabla..
"""

#IMPORTS
import os
import sys
import time
import json
import logging
from naoqi import ALProxy
from naoqi import ALBehavior
from naoqi import ALModule
from naoqi import ALBroker

#SET IP AND PORT
IP = "192.168.2.172"
PORT = 9559

# VARIOUS MODULES FOR USE
motion = ALProxy("ALMotion", IP, PORT)
tracker = ALProxy("ALTracker", IP, PORT)
behavior = ALProxy("ALBehaviorManager", IP, PORT)
tts = ALProxy("ALTextToSpeech", IP, PORT)
anims = ALProxy("ALAnimatedSpeech", IP, PORT)
postureProxy = ALProxy("ALRobotPosture", IP, PORT)
memoryProxy = ALProxy("ALMemory", IP, PORT)

################ USEFUL COMMANDS ##############################
# \\vct=150\\ Change pitch of voice
# \\pau=1000\\ set pause
# \\rspd=50\\ change speed of text
# \\vol=50\\ change volume

class Test(ALModule):

    def connect_to_webserver(self):


    def read_JSON_greeting(self):
        try:
            # trying to open the JSON file to read from it
            self.logger.info('inTRY')
            file = open(os.path.join(self.behaviorAbsolutePath(), 'fullsession.json'))
            self.logger.info('opened json file')
            data = json.load(file)
            self.logger.info('loaded json')

            # sending the data to the onData output of the script box
            self.onData(json.dumps(data['module_greeting']))
            file.close()



            self.logger.info("reading")
        except Exception as e:
            self.logger.error(e)


tts.say("")
#motion.wakeUp()
#motion.setStiffnesses("Body", 1.0)
#postureProxy.goToPosture("Sit", 1.0)
#motion.rest()


if __name__ == '__main__':
