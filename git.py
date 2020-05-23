#sudo pip install requests==1.1.0 (dont need)
#python -m pip install --upgrade pip setuptools wheel
#pip install firebase-admin
#change 
"""
1)rename .async into .async_
2)open__init__ file and change .async into .async_
3)open firebase.py and change .async into .async_
because of .async is the keyword now is current version in python
Done>>>>>>>>>>
"""
#Importing folders
import busio
import digitalio
import board                                        #Replaces(GPIO.setmode(GPIO.BOARD/BCM)) defaults to BCM v*
import git as DB
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn     #MCP3008/Sound

import RPi.GPIO as GPIO                             #RGB & Relay/Fan

import time                                         #Clock
import threading
import json

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('serviceAccountKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://pythondb-6b948.firebaseio.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('/py_command/')
#GPIO ----------------------------------------------------------------------------------------------------------------
#print(ref.get())
GPIO.setup(5,GPIO.OUT)      #RED                                    #Setting 1 RGB LED off (Must turn off again in code vv)
GPIO.output(5,0)
GPIO.setup(6,GPIO.OUT)      #GREEN
GPIO.output(6,0)
GPIO.setup(13,GPIO.OUT)     #BLUE
GPIO.output(13,0)

GPIO.setup(21, GPIO.OUT)    #Relay                                  #Setting Relay off
GPIO.output(21,1)


spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)  #Setting MCP3008 pin set to zero_(P0)
cs = digitalio.DigitalInOut(board.D5)
mcp = MCP.MCP3008(spi, cs)
chan = AnalogIn(mcp, MCP.P0)

#GLOBAL VAR
stop_threads = False

#Functions---------------------------------------------------------------------------------------------------------
def fan_on(pin):
    GPIO.output(pin, GPIO.LOW)   # Turn on

def fan_off(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn off
    
def rgb(r,g,b):
    GPIO.output(5,int(r))
    GPIO.output(6,int(g))
    GPIO.output(13,int(b))
class Livemode:
    def __init__(self):
        self._running = True
    def terminate(self):
        self._running = False
        print(self._running)
        
    def run(self):
        rgb(0,0,0)
        zero = int(chan.value/1000)
        rgb(0,0,0)
        time.sleep(1)
        while self._running:
            rgb(0,0,0)
            val = int(chan.value/1000)
            rgb(0,0,0)
            if(val == zero):
                #print(val)
                rgb(0,0,0)
                time.sleep(.035)
            if(val == zero+1):
                #print(val)
                rgb(0,1,0)
                time.sleep(.035)
            if(val == zero+2):
                #print(val)
                rgb(1,0,0)
                time.sleep(.035)
            if(val == zero+3):
                #print(val)
                rgb(1,0,0)
                time.sleep(.035)
            if(val == zero-1):
                #print(val)
                rgb(0,0,1)
                time.sleep(.035)
            

def live(stopper):
    rgb(0,0,0)
    zero = int(chan.value/1000)
    rgb(0,0,0)
    time.sleep(1)
    while(True):
        rgb(0,0,0)
        val = int(chan.value/1000)
        rgb(0,0,0)

        if(val == zero):
            #print(val)
            rgb(0,0,0)
            time.sleep(.035)
        if(val == zero+1):
            #print(val)
            rgb(0,1,0)
            time.sleep(.035)
        if(val == zero+2):
            #print(val)
            rgb(1,0,0)
            time.sleep(.035)
        if(val == zero+3):
            #print(val)
            rgb(1,0,0)
            time.sleep(.035)
        if(val == zero-1):
            #print(val)
            rgb(0,0,1)
            time.sleep(.035)

        if (stopper == 'TTT'):
            break
    
#DB Listener -------------------------------------------------------    


def listener(event):
    thr = Livemode()
    #print(event.event_type)  # can be 'put' or 'patch'
    #print(event.path)  # relative to the reference, it seems
    print(event.data)  # new data at /reference/event.path. None if deleted
    temp = json.dumps(event.data)
    data = json.loads(temp)
    command = data["command"]
    color = data["color"]
    print(command)
    if(command == 'Stop'):
        GPIO.cleanup()
        exit()
    elif(command == 'FAN'):
        FAN = fan_on(21)
    elif(command == 'FAN OFF'):
        FAN = fan_off(21)
        
    elif(command =='LVOFF'):
        thr.terminate()
        rgb(0,0,0)
        print("LEDs are OFF")
        time.sleep(1)
            
    elif(command == "LIVEMODE"):
        rgb(0,0,0)
        print("live mode ON")
        time.sleep(.5)
        stop_threads = False
        t1 = threading.Thread(target = thr.run)
        t1.start()
            
    elif (command == 'LED'):
        if(color == 'BLACKOUT'):
            rgb(0,0,0)
            time.sleep(1)
            print("LED turned OFF.")
        if(color == 'RED'):
            rgb(1,0,0)
            time.sleep(1)
            print("LED turned red.")
        if(color == 'GREEN'):
            rgb(0,1,0)
            time.sleep(1)
            print("LED turned green.")
        if(color == 'BLUE'):
            rgb(0,0,1)
            time.sleep(1)
            print("LED turned blue.")
        if(color == 'WHITE'):
            rgb(1,1,1)
            time.sleep(1)
            print("LED turned white.")
        if(color == 'LTBLUE'):
            rgb(0,1,1)
            time.sleep(1)
            print("LED turned light blue.")
        if(color == 'PURP'):
            rgb(1,0,1)
            time.sleep(1)
            print("LED turned purple.")
        if(color == 'YELLOW'):
            rgb(1,1,0)
            time.sleep(1)
            print("LED turned yellow.")
    
    
rgb(0,0,0)
firebase_admin.db.reference('/py_command/').listen(listener)
