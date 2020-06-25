#! /usr/bin/env python
# -*- encoding: UTF-8 -*-
"""Example: A Simple class to get & read BarcodeDetection Events"""

import qi
from naoqi import ALProxy
import argparse
import sys
import time


class BarcodeReader(object):
    """
    A simple class to react to barcode detection events.
    """
    sawCode = False
    active = True

    def __init__(self, app):
        super(BarcodeReader, self).__init__()
        # start application and get session
        app.start()
        session = app.session
        # Get the services ALBarcodeReader and ALMemory.
        self.memory_service = session.service("ALMemory")
        self.barcode_service = session.service("ALBarcodeReader")
        self.subscriber = self.memory_service.subscriber("BarcodeReader/BarcodeDetected")
        self.subscriber.signal.connect(self.on_barcode_detected)
        self.barcode_service.subscribe("test_barcode")

    def on_barcode_detected(self, value):
        """
        Callback for event BarcodeReader/BarcodeDetected
        """
        print "I saw a barcode"
        print "The event data are: " +str(value)
        #print value.CodeData
        if self.sawCode == False:
            self.sawCode = True
            print "mutX"
            tts = ALProxy("ALTextToSpeech", "192.168.2.162", 9559)
            tts.setLanguage("German")
            tts.say("")
            #tts.say(value)
        self.sawCode = False
        self.active = False

    def run(self):
        """
        Loop on, wait for events until manual interruption.
        """
        print "Starting BarcodeReader"
        try:
            while self.active == True:
                time.sleep(1)
            print "Unsubscribe BarcodeReader"
            self.barcode_service.unsubscribe("test_barcode")
        except KeyboardInterrupt:
            print "Interrupted by user, stopping BarcodeReader"
            self.barcode_service.unsubscribe("test_barcode")
            # Stop
            sys.exit(0)


if __name__ == "__main__":
    #parser = argparse.ArgumentParser()
    ##parser.add_argument("--ip", type=str, default="127.0.0.1",
    ##                    help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
	#parser.add_argument("--ip", type=str, default="192.168.2.172", help="Robot IP address. On robot or Local Naoqi: use '192.168.2.172'.")
    #parser.add_argument("--port", type=int, default=9559, help="Naoqi port number")

    #args = parser.parse_args()
    try:
        # Initialize qi framework.
        #connection_url = "tcp://" + args.ip + ":" + str(args.port)
        connection_url = "tcp://" + "192.168.2.162" + ":" + "9559"
        print connection_url
        app = qi.Application(["BarcodeReader", "--qi-url=" + connection_url])    
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    
    barcode_reader = BarcodeReader(app)
    barcode_reader.run()
