import logging
import os
import paho.mqtt.client as mqtt

from abstract_feed import ApplicationBackend


class MqttBackend(ApplicationBackend):
    def __init__(self):
        super().__init__()
        self.mqttc = mqtt.Client()
        self.mqttc.on_message = self.on_message
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_subscribe = self.on_subscribe

        self.mqttc.username_pw_set(username="Python", password="1OQ$7LAdn&*nC3a%rZdbXU&XNsreCc#1")
        self.mqttc.connect("m24.cloudmqtt.com", 18142, 60)
        self.mqttc.subscribe("Fortnite/#", 0)

    def on_connect(self, mqttc, obj, flags, rc):
        logging.info("rc: " + str(rc))

    def on_message(self, mqttc, obj, msg):
        if self.callback:
            for client in self.clients['Shiqan']:
                self.callback(client, msg.payload)

    def on_subscribe(self, mqttc, obj, mid, granted_qos):
        logging.info("Subscribed: " + str(mid) + " " + str(granted_qos))

    def start(self):
        self.mqttc.loop_start()
