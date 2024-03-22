import paho.mqtt.client as mqtt
import socket
import time

HOSTNAME = "10.0.0.21"  # "192.168.0.110"
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
    listeners = []
    connected = False

    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_message = self.__on_message

        while not self.connected:
            try:
                self.connect()
            except:
                print("Could not connect to mqtt.  Waiting...")
                time.sleep(2)

    def connect(self):
        self.client.connect(get_hostname(), BROKER_PORT, 60)
        self.client.loop_start()
        self.connected = True

    def __on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT broker with result code: " + str(rc))
        client.subscribe(TOPIC)

    def __on_message(self, client, userdata, message):
        # print("Message received: " + message.payload.decode())
        for listener in self.listeners:
            if listener is not None:
                listener(message.payload.decode())

    def publish(self, message):
        self.client.publish(TOPIC, message)

    def listen(self, listener):
        self.listeners.append(listener)
