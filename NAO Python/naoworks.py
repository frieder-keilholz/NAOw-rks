from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import sys
import time
import requests
import json

# Load planned JSON Files
import naoGetModules
naoGetModules.get_todays_modules()

# Wait for the RightBumper to be touched
# After touch the NAO will present the module
BumperIF = None
memory = None


class BumperIFModule(ALModule):
    pressed = False
    """ A simple module able to react
    to facedetection events

    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("RightBumperPressed","BumperIF","onTouched")

    def subscribeAgain(self,*_args):
        memory.subscribeToEvent("RightBumperPressed","BumperIF","onTouched")

    def onTouched(self,*_args):
        print "TEST"
        memory.unsubscribeToEvent("RightBumperPressed","BumperIF")
        self.pressed = True
        #print "ReSub"
        #memory.subscribeToEvent("RightBumperPressed","BumperIF","onTouched")


myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       "192.168.2.162",         # parent broker IP
       9559)       # parent broker port

global BumperIF
BumperIF = BumperIFModule("BumperIF")

try:
    while BumperIF.pressed == False:
            time.sleep(1)
            print BumperIF.pressed
except KeyboardInterrupt:
    print "Interrupted by user, shutting down"
    myBroker.shutdown()
    sys.exit(0)



# Present the Module
tts = ALProxy("ALTextToSpeech")
f=open("json_modules/next_module.json", "r")
module_json = json.loads(f.read())
print module_json["module_name"]
module_title = module_json["module_name"]
module_descr = module_json["module_description"]
tts.say("Das Module heisst ")
tts.say(str(module_title))
tts.say(str(module_descr))

# Asks to begin the comparision
tts.say("Druecke meinen rechten Bumper, wenn du die Aufgaben vergleichen willst.")
try:
    BumperIF.pressed = False
    BumperIF.subscribeAgain()
    while BumperIF.pressed == False:
            time.sleep(1)
            print BumperIF.pressed
except KeyboardInterrupt:
    print "Interrupted by user, shutting down"
    myBroker.shutdown()
    sys.exit(0)

# Compare each task



myBroker.shutdown()
print "done"