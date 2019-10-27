#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict, Union

import paho.mqtt.client as mqtt
import RPi.GPIO as gpio


def gpioSetup():
    gpio.setmode(gpio.BCM)
    gpio.setup(2, gpio.OUT)


def connectionStatus(client, userdata, flags, rc):
    mqttClient.subscribe("rpi/gpio")


def messageDecoder(client, userdata, msg):
    message = msg.payload.decode(encoding='UTF-8')

    if message == "on":
        gpio.output(2, gpio.HIGH)
        print("Program initiated")
    elif message == "off":
        gpio.output(2, gpio.LOW)
        print("Program is terminated")
    elif message == "%I:%M %p AM" or "%I:%M %p PM":
        print("Here")
        current_dict: = {"start_time": "8:30 AM", "how_long": "10", "how_often": "12", "off": "False", "auto": "True", "rain_delay": "False"}
        print(current_dict)

        def replace_value_with_input(key_to_find, definition):
            for key in current_dict.keys():
                if key == key_to_find:
                    current_dict[key] = definition
                    print("Here in function")

        # Changed code in RPi crash below and above?
        replace_value_with_input('start_time', message)
        current_dict_str = str(current_dict)
        print(current_dict_str)
        f = open("config.json", "w")
        f.write(current_dict_str)
        f.close()
        print("OPERATION DONE")
    else:
        print("Unknown message!")


gpioSetup()

clientName = "RPI"

serverAddress = "192.168.1.16"

mqttClient = mqtt.Client(clientName)

mqttClient.on_connect = connectionStatus

mqttClient.on_message = messageDecoder

mqttClient.connect(serverAddress)

mqttClient.loop_forever()
