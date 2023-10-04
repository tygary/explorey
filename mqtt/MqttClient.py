import paho.mqtt.client as mqtt
import socket

HOSTNAME = "10.0.2.4"
BROKER_PORT = 1883
TOPIC = "mqtt/timemachine"

def get_hostname():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    current_ip = s.getsockname()[0]
    s.close()
    if current_ip == HOSTNAME:
        return "127.0.0.1"
    else:
        return HOSTNAME


class MqttClient(object):
    client = None

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message
        self.client.connect(get_hostname(), BROKER_PORT, 60)
        self.client.loop_start()

    def __on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code: " + str(rc))
        client.subscribe(TOPIC)

    def __on_message(self, client, userdata, message):
        print("Message received: " + message.payload.decode())

    def publish(self, message):
        self.client.publish(TOPIC, message)

