import paho.mqtt.client as paho
from paho import mqtt
from time import sleep

import Adafruit_DHT
import RPi.GPIO as GPIO

secrets = {
    'username': 'peshani99',
    'password': 'peshani1999',
    'broker': '46e735a039be4769b6c437177efe5fc0.s1.eu.hivemq.cloud',
    'port': 8883,
    'topic': 'sliit/temp-humid'
}

sensor = Adafruit_DHT.DHT22

# Raspberry PI with DHT22 sensor connected to GPIO-23 and LED to GPIO-17
dhtt22_pin = 23
led_pin = 14

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)


def on_connect(client, userdata, flags, rc, properties=None):
    print('Connected with code %d.', rc)


def on_publish(client, userdata, mid, properties=None):
    print("on_publish -> mid: "+str(mid))


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message
client.on_subscribe = on_subscribe

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(secrets['username'], secrets['password'])
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(secrets['broker'], secrets['port'])

killed = False
while not killed:
    # Measure temperature and humidity
    humidity, temperature, heat_index = 0, 0, 0
    json = ''
    try:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, dhtt22_pin)
        heat_index = -42.379 + 2.04901523*temperature + 10.14333127 * humidity - .22475541*temperature*humidity - .00683783*temperature*temperature - .05481717*humidity * humidity + .00122874*temperature*temperature*humidity + .00085282*temperature*humidity*humidity - .00000199*temperature*temperature*humidity*humidity
        json = "{\"temperature\": " + str(round(temperature,3)) + ",\"humidity\": " + str(round(humidity,3)) + ",\"heat_index\": " + str(round(heat_index,3)) +"}"
        GPIO.output(led_pin, GPIO.HIGH)
    except Exception as e:
        print("Measurement failure\n", e)
 # Send to HiveMQ Cloud
    try:
        print("\tMessage for queue: " + json)
        client.publish(secrets['topic'], payload=json, qos=1)
        GPIO.output(led_pin, GPIO.LOW)
    except Exception as e:
        print("\tMQTT publish Failed, retrying\n", e)
        killed = True
        continue

    # Sleep a second
    sleep(2)

# subscribe to topic
# client.subscribe(secrets['topic'], qos=1)
# client.loop_forever()
