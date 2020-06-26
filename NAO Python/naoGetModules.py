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
#IP = "192.168.2.162"
IP = "127.0.0.1"
PORT = 9559

memoryProxy = ALProxy("ALMemory", IP, PORT)
tts = ALProxy("ALTextToSpeech", IP, PORT)


def get_todays_modules():
    bodyID = memoryProxy.getData("Device/DeviceList/ChestBoard/BodyId")
    URL = "http://comoffice.org:41031/assigned_modules?nao_id=" + bodyID
    #URL = "http://192.168.2.162:41031/assigned_modules?nao_id=" + bodyID
    re = requests.get(URL)
    raw_data = re.text
    modules = json.loads(raw_data)
    module_ID = modules[0]["module_id"]

    module_text = requests.get("http://comoffice.org:41031/modulerq?module_id=" + module_ID)
    #module_text = requests.get("http://192.168.2.162:41031/modulerq?module_id=" + module_ID)

    #only use on NAO because forslashes are not usable in directories in Windows
    #json_file = open("home/nao/json_modules/next_module.json", "w+")
    json_file = open("/home/nao/json_modules/next_module.json", "w+")
    json_file.write(module_text.text)

if __name__ == '__main__':
    get_todays_modules()
    tts.say("Juhu es funktioniert")
    #while not (memoryProxy.getData("RightBumperPressed")):
    #    print "no"
    #tts.say("hihi das kitzelt am rechten Fuss")
