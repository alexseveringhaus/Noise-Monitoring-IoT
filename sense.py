import time
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import paho.mqtt.client as mqtt
import datetime

now = datetime.datetime.now()

GPIO.setmode(GPIO.BOARD)
chan_list = [11]
GPIO.setup(chan_list, GPIO.OUT)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#setting up mqtt client
def on_connect(client, userdata, flags, rc, properties):
  print("Connected to server with result code " + str(rc))

def on_message(client, userdata, message):
  print("Topic: " + message.topic + " and the message is: " + str(message.payload, "utf-8"))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_message = on_message
client.on_connect = on_connect

#Testing different brokers
#client.connect(host="broker.emqx.io", port=1883, keepalive=60)
client.connect("test.mosquitto.org", 1883, 60)

client.loop_start()


lux_threshold=400  # change this value
sound_threshold=500 # change this value

client.publish("severing/sound1", payload="", retain=True) 

count = 0
sum = 0
while True:
  time.sleep(.5)
  #SOUND SENSOR
  soundvalue = mcp.read_adc(1)
  sum = sum + soundvalue
  if count == 10:
    count = 0
    average = sum/10
    sum = 0
    client.publish("severing/sound1", average, retain=False)
    count = count + 1
