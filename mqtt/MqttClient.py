import time
import paho.mqtt.client as mqtt


HOSTNAME = "http://10.0.2.4"
BROKER_PORT = 1883
TOPIC = "mqtt/timemachine"


class MqttClient(object):
    client = None

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        self.client.connect(HOSTNAME, BROKER_PORT, 60)
        self.client.loop_start()

    def __on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code: " + str(rc))
        client.subscribe(TOPIC)

    def __on_message(self, client, userdata, message):
        print("Message received: " + message.payload.decode())

    def publish(self, message):
        self.client.publish(TOPIC, message)

