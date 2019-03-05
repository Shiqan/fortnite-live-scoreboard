import logging
import os
import paho.mqtt.client as mqtt

from abstract_feed import ApplicationBackend

MQTT_URL = os.environ.get('MQTT_URL', 'm24.cloudmqtt.com')
MQTT_PORT = int(os.environ.get('MQTT_PORT', '18142'))
MQTT_USERNAME = os.environ.get('MQTT_USERNAME', 'Python')
MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', '1OQ$7LAdn&*nC3a%rZdbXU&XNsreCc#1')



class MqttBackend(ApplicationBackend):
    def __init__(self):
        super().__init__()
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_subscribe = self.on_subscribe

        self.mqttc.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
        self.mqttc.connect(MQTT_URL, MQTT_PORT, 60)
        self.mqttc.subscribe("Fortnite/#", 1)

    def on_connect(self, mqttc, obj, flags, rc):
        logging.info("rc: " + str(rc))

    def on_message(self, mqttc, obj, msg):
        if self.callback:
            topic = msg.topic.split('/')[-1]
            for client in self.clients.get(topic, []):
                self.callback(client, msg.payload)

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        logging.info("Subscribed: " + str(mid) + " " + str(granted_qos))

    def start(self):
        self.mqttc.loop_start()
