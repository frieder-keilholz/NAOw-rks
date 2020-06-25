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


memoryProxy = ALProxy("ALMemory", IP, PORT)




class naoGetModules():

    def get_BodyID(self):
        bodyID = memoryProxy.getData("Device/DeviceList/ChestBoard/BodyId")
        return bodyID

    def get_todays_modules(self):
        URL = "http://comoffice.org:41031/assigned_modules?nao_id=" + self.get_BodyID()
        r = requests.get(URL)
        print r.text
        return


    def main(self):
        self.get_todays_modules()

if __name__ == '__main__':
    global naoGetModules
    naoGetModules = naoGetModules()
    naoGetModules.main()