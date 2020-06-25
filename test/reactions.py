#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Julia Reinke"
__version__ = "19.06.2020"
__email__ = "jure5622@th-wildau.de"

# IMPORTS
import os
import sys
import time
import json
import logging
import requests
from naoqi import ALProxy
from naoqi import ALBehavior
from naoqi import ALModule
from naoqi import ALBroker

# SET IP AND PORT
IP = "192.168.2.162"
PORT = 9559

motion = ALProxy("ALMotion", IP, PORT)
tracker = ALProxy("ALTracker", IP, PORT)
behavior = ALProxy("ALBehaviorManager", IP, PORT)
tts = ALProxy("ALTextToSpeech", IP, PORT)
anims = ALProxy("ALAnimatedSpeech", IP, PORT)
postureProxy = ALProxy("ALRobotPosture", IP, PORT)
memoryProxy = ALProxy("ALMemory", IP, PORT)
configuration = {"bodylanguageMode" : "contextual"}
tfa = {"right_answer": ["animations/Sit/Emotions/Positive/Happy_2"],
       "wrong_answer": ["animations/Sit/Emotions/Negative/Frustrated_1"]
       }
anims.declareTagForAnimations(tfa)


def right_answer(right_answer):
    motion.wakeUp()
    motion.setStiffnesses("Body", 1.0)
    anims.say("^start(animations/Sit/Emotions/Positive/Happy_2)" + right_answer, configuration)
    time.sleep(2)
    motion.rest()

def wrong_answer(wrong_answer):
    motion.wakeUp()
    motion.setStiffnesses("Body", 1.0)
    anims.say("^start(animations/Sit/Emotions/Negative/Frustrated_1)" + wrong_answer, configuration)
    time.sleep(2)
    motion.rest()