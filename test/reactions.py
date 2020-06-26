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
ttw = {"affirmative": ["right_answer"],
       "negative": ["wrong_answer"],
       "no": ["wrong_answer"]
       }
anims.addTagsToWords(ttw)

def initialize():
    motion.wakeUp()
    motion.setStiffnesses("Body", 1.0)
    postureProxy.goToPosture("Sit", 1.0)


def right_answer(right_answer):

    #^start(animations/Sit/Emotions/Positive/Happy_2)
    anims.say("^start(Sit/Emotions/Positive/Happy_2)" + right_answer + "^wait(Sit/Emotions/Positive/Happy_2)", configuration)
    time.sleep(6)
    postureProxy.goToPosture("Sit", 1.0)
    

def wrong_answer(wrong_answer):
    #"^start(No_3)" +
    anims.say("^start(Sit/Emotions/Negative/Frustrated_1) " + wrong_answer + "^wait(Sit/Emotions/Negative/Frustrated_1)", configuration)
    time.sleep(6)
    postureProxy.goToPosture("Sit", 1.0)


def put_to_rest():
    postureProxy.goToPosture("Sit", 1.0)
    motion.rest()