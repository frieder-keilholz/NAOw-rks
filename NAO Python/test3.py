#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import sys
import time

BumperIF = None
memory = None

class BumperIFModule(ALModule):
    """ A simple module able to react
    to facedetection events

    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("RightBumperPressed","BumperIF","onTouched")

    def onTouched(self,*_args):
        print "TEST"
        memory.unsubscribeToEvent("RightBumperPressed","BumperIF")
        print "ReSub"
        memory.subscribeToEvent("RightBumperPressed","BumperIF","onTouched")



myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       "192.168.2.162",         # parent broker IP
       9559)       # parent broker port

global BumperIF
BumperIF = BumperIFModule("BumperIF")

try:
    while True:
            time.sleep(1)
except KeyboardInterrupt:
    print "Interrupted by user, shutting down"
    myBroker.shutdown()
    sys.exit(0)