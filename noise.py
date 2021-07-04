import time
import sys
import ibmiotf.application
import ibmiotf.device
import random
import json

#Provide your IBM Watson Device Credentials
organization = "j5mx67"
deviceType = "iotdevice"
deviceId = "1001"
authMethod = "token"
authToken = "987654321"


# Initialize the device client.
n=0
la=0
lg=0
def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data['command'])


        if cmd.data['command']=='lighton':
                print("LIGHT ON IS RECEIVED")
                
                
        elif cmd.data['command']=='lightoff':
                print("LIGHT OFF IS RECEIVED")
        
        if cmd.command == "setInterval":
                if 'interval' not in cmd.data:
                        print("Error - command is missing required information: 'interval'")
                else:
                        interval = cmd.data['interval']
        elif cmd.command == "print":
                if 'message' not in cmd.data:
                        print("Error - command is missing required information: 'message'")
                else:
                        print(cmd.data['message'])

try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions)
	#..............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

# Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()

while True:
        n=88
        la=16.5062
        lg=80.6480
        #Send waterlevel & light intensity to IBM Watson
        data = {"d":{ 'noise' : n, 'latitude': la, 'longitude': lg, }}
        #print data
        def myOnPublishCallback():
            print ("Published noise = %s units" % n, "latitude in degrees = %s " % la, "longitude in degrees = %s " % lg , "to IBM Watson")

        success = deviceCli.publishEvent("Data", "json", data, qos=0, on_publish=myOnPublishCallback)
        if not success:
            print("Not connected to IoTF")
        time.sleep(1)
        
        deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
