"""
with sample of python documentation
"""

from naoqi import *
import time
check = 0


# create python module
class myModule(ALModule):
  """python class myModule test auto documentation : comment needed to create a new python module"""


  def pythondatachanged(self, strVarName, value):
    """callback when data change"""
    print "datachanged", strVarName, " ", value, " ", strMessage
    global check
    check = 1

  def _pythonPrivateMethod(self, param1, param2, param3):
    global check


broker = ALBroker("pythonBroker","",9999,"192.168.2.162",9559)


# call method
try:

  pythonModule = myModule("pythonModule")
  prox = ALProxy("ALMemory")
  #prox.insertData("val",1) # forbiden, data is optimized and doesn't manage callback
  prox.subscribeToEvent("FaceDetected","pythonModule", "pythondatachanged") #  event is case sensitive !
  #prox.subscribeToEvent("MiddleTactileTouched","pythonModule","pythondatachanged")

except Exception,e:
  print "error"
  print e
  exit(1)

while (1):
  time.sleep(2)