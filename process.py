import paho.mqtt.client as mqtt
import time
import requests
import json
from datetime import datetime
from struct import *

from yeelight import discover_bulbs, Bulb
from yeelight import LightType

bulbs = discover_bulbs()
bulb = Bulb(bulbs[0]['ip'])

def flashLight():    
    bulb.turn_on()
    time.sleep(0.5)
    bulb.turn_off()
    time.sleep(0.5)
    bulb.turn_on()
    time.sleep(0.5)
    bulb.turn_off()
    time.sleep(0.5)
    bulb.turn_on()
    time.sleep(0.5)
    bulb.turn_off()

url = "https://worldtimeapi.org/api/timezone/America/Los_Angeles"
soundThreshold = 0;

def on_connect(client, userdata, flags, rc, properties):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    client.subscribe("severing/sound1")
    client.message_callback_add("severing/sound1", sound_on_message)

def sound_on_message(client, userdata, msg):
    response = requests.get(url)
    
    if response.status_code == 200:
        jsonRequest = response.json()
        day = jsonRequest['day_of_week']
        unixTime = jsonRequest['unixtime']
        time = convertTime(unixTime)
        if day >= 1 and day <= 4 or day == 7: #weekday
            if time >= 22 or time <= 7 : 
                soundThreshold = 150
            else: 
                soundThreshold = 300
        else: #weekend
            if time >= 0 and time < 9:
                soundThreshold = 150
            else: 
                soundThreshold = 300        
        soundString = str(msg.payload, "utf-8")
        print("Sound level:", soundString)
        if (len(soundString) > 0):
            sound = int(float(soundString))
            if sound > soundThreshold:
                flashLight();
            else: 
                if sound < int(0.25*soundThreshold):
                    bulb.set_brightness(25)
                elif sound < int(0.5*soundThreshold):
                    bulb.set_brightness(50)
                elif sound < int(0.75*soundThreshold):
                    bulb.set_brightness(75)
                else:
                    bulb.set_brightness(99)
            

#Default message callback
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#client = mqtt.Client()
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.on_connect = on_connect

#Testing different brokers
#client.connect(host="broker.emqx.io", port=1883, keepalive=60)
client.connect("test.mosquitto.org", 1883, 60)

client.loop_start()

def convertTime(unixTime):
    dt = datetime.fromtimestamp(unixTime)
    hour = dt.hour
    return hour

while True:
    time.sleep(0.1)
