#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Frieder Keilholz"
__version__ = "26.06.2020"
__email__ = "frieder.keilholz@th-wildau.de"

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import sys
import time
import requests
import json

import naoGetModules
import reactions

# Global variables
BumperIF = None
memory = None
QRReader = None

# Callback class to register a touch on the right bumper
class BumperIFModule(ALModule):
    pressed = False
    pressedLeft = False
    pressedRight = False
    
    def __init__(self, name):
        ALModule.__init__(self, name)
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("RightBumperPressed","BumperIF","onTouched")
        memory.subscribeToEvent("LeftBumperPressed","BumperIF","onLeftTouched")

    def subscribeAgain(self,*_args):
        memory.subscribeToEvent("RightBumperPressed","BumperIF","onTouched")
        memory.subscribeToEvent("LeftBumperPressed","BumperIF","onLeftTouched")

    def onLeftTouched(self, *_args):
        print "Left Bumper touched"
        memory.unsubscribeToEvent("RightBumperPressed","BumperIF")
        memory.unsubscribeToEvent("LeftBumperPressed","BumperIF")
        self.pressed = True
        self.pressedLeft = True

    def onTouched(self,*_args):
        print "Right Bumper touched"
        memory.unsubscribeToEvent("RightBumperPressed","BumperIF")
        memory.unsubscribeToEvent("LeftBumperPressed","BumperIF")
        self.pressed = True
        self.pressedRight = True

# Callback class to register QR-Codes
class myEventHandler(ALModule):
    lastQRcode = None
    active = True
    def myCallback(self, key, value, msg):
        print "Received \"" + str(key) + "\" event with data: " + str(value)
        if value != []:
            self.lastQRcode = value[0][0]
            self.active = False
            memory.unsubscribeToEvent("BarcodeReader/BarcodeDetected", "QRReader")



# Function to read just one QR Code and return its value
def readFirstQR():
    try:
        QRReader.active = True
        memory.subscribeToEvent("BarcodeReader/BarcodeDetected", "QRReader", "myCallback")
        while QRReader.active == True:
            time.sleep(1)        
        return str(QRReader.lastQRcode)
    except KeyboardInterrupt:
        myBroker.shutdown()
        sys.exit(0)

#time.sleep(1)

myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       "127.0.0.1",
       #"192.168.2.162",         # parent broker IP
       9559)       # parent broker port

global BumperIF
BumperIF = BumperIFModule("BumperIF")

global QRReader
QRReader = myEventHandler("QRReader")

tts = ALProxy("ALTextToSpeech")
tts.say("\\vol=50\\ ")
tts.say("NAO laedt das eingeplante Modul")

#time.sleep(1)

# Load planned JSON Files
try:
    naoGetModules.get_todays_modules()
    print "Loaded module"
    tts.say("Das Modul wurde geladen.")
except:
    print "Failed to load module"
    tts.say("Das Modul konnte nicht geladen werden.")
    tts.say("NAO fuehrt jetzt das zuletzt geladene Modul aus.")

f=open("/home/nao/json_modules/next_module.json", "r")
module_json = json.loads(f.read())

print module_json["module_name"]
module_title = module_json["module_name"]
module_descr = module_json["module_description"]

# Present the Module
tts.say("Das Modul heisst ")
tts.say(str(module_title))
tts.say(str(module_descr))
# Wait for the RightBumper to be touched
tts.say("Druecke meinen rechten Fuss, wenn das Modul beginnen soll.")
try:
    while BumperIF.pressed == False:
            time.sleep(1)
            print BumperIF.pressed
except KeyboardInterrupt:
    print "Interrupted by user, shutting down"
    myBroker.shutdown()
    sys.exit(0)

reactions.initialize()

tts.say(str(module_json["module_greeting"]))


# Asks to begin the comparision

comparision_active = True
while comparision_active:
    tts.say("Druecke meinen rechten Fuss, wenn du die Aufgaben vergleichen willst.")
    tts.say("Druecke meinen linken Fuss, wenn du das Modul beenden willst.")
    try:
        BumperIF.pressed = False
        BumperIF.pressedRight = False
        BumperIF.pressedLeft = False
        BumperIF.subscribeAgain()
        while BumperIF.pressed == False:
            time.sleep(1)
            print BumperIF.pressed
    except KeyboardInterrupt:
        print "Interrupted by user, shutting down"
        myBroker.shutdown()
        sys.exit(0)

    if BumperIF.pressedLeft == True:
        print "exit comparision"
        break

    # Compare each task
    for task in module_json['tasks']:
        print task['task_title']
        tts.say(str(task['task_title']))

        task_intro = str(task['task_introduction'])
        tts.say(task_intro)
        # ask each question
        i = 1
        time.sleep(1)
        for question in task['questions']:
            tts.say("Frage "+str(i))
            time.sleep(1)
            i+=1
            correct = False
            while correct == False:
                tts.say(str(question['question_question']))
                # say each answer
                possibleInputs = []
                
                correct_answers = []
                for answer in question['answers']:
                    print answer
                    tts.say(str(answer['answer_symbol']))
                    tts.say(str(answer['answer_text']))
                    possibleInputs.append(str(answer['answer_card_id']))
                    if 'answer_correct' in answer:
                        correct_answers.append(str(answer['answer_card_id']))
                inputQR = readFirstQR()
                if inputQR in possibleInputs:
                    selected_answer = None
                    for ans in question['answers']:
                        if ans['answer_card_id'] == inputQR:
                            selected_answer = ans
                    print "Input is done"
                    if inputQR in correct_answers:
                        correct = True
                        #tts.say("Juhu deine Antwort ist richtig")
                        reactions.right_answer("Deine Antwort ist richtig")
                    else:
                        #tts.say("ob du dumm bischt!")
                        reactions.wrong_answer(str(selected_answer['answer_explanation']))
                    
                        tts.say("Versuche es noch einmal.")
                        tts.say("Ein Tip ")
                        tts.say(str(question['question_help']))
    tts.say("Du hast alle Aufgaben verglichen.")

tts.say(str(module_json['module_goodby']))
myBroker.shutdown()
print "Programm finished"
