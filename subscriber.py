import paho.mqtt.client as paho
from paho import mqtt
from time import sleep

secrets = {
    'username': 'peshani99',
    'password': 'peshani1999',
    'broker': '46e735a039be4769b6c437177efe5fc0.s1.eu.hivemq.cloud',
    'port': 8883,
    'topic': 'sliit/temp-humid'
}


def on_connect(client, userdata, flags, rc, properties=None):
    print('Connected with code %d.', rc)


def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)

client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
# set username and password
client.username_pw_set(secrets['username'], secrets['password'])
# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(secrets['broker'], secrets['port'])

# subscribe to topic
client.subscribe(secrets['topic'], qos=1)
client.loop_forever()