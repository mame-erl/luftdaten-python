#!/usr/bin/env python3

import sys
import os
import yaml
import time
import json
import requests
import logging
from recursive_json import extract_values

# modded file by Markus Meier
# goal: load data from Smart Citizen Kit API and transfer to luftdaten.info

# Config
with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

# Logging
logging.basicConfig(level=logging.DEBUG)


class Measurement:
    def __init__(self):

        # define URL of the Smart Citizen Kit
        sckurl = config['luftdaten'].get('sckurl')
        # request URL response
        req = requests.get(sckurl)
        # convert response to json
        pjson=req.json()
        # get dedicated values
        values = extract_values(pjson["data"], 'value')

        self.pm25_value  = values[8]
        self.pm10_value  = values[7]
        self.temperature = values[10]
        self.humidity    = values[9]
        self.pressure    = values[5]


    def sendLuftdaten(self):
        if not config['luftdaten']['enabled']:
            return


        self.__pushLuftdaten('https://api.luftdaten.info/v1/push-sensor-data/', 1, {
            "P1": self.pm10_value,
            "P2": self.pm25_value,
        })
        self.__pushLuftdaten('https://api.luftdaten.info/v1/push-sensor-data/', 7, {
            "temperature": self.temperature,
            "pressure":    self.pressure*1000,
            "humidity":    self.humidity,
        })


    def __pushLuftdaten(self, url, pin, values):
        requests.post(url,
            json={
                "software_version": "python-sck 0.0.1",
                "sensordatavalues": [{"value_type": key, "value": val} for key, val in values.items()],
            },
            headers={
                "X-PIN":    str(pin),
                "X-Sensor": sensorID,
            }
        )


def run():
    m = Measurement()

    print('pm2.5     = {:f} '.format(m.pm25_value))
    print('pm10      = {:f} '.format(m.pm10_value))
    print('Temp      = {:0.2f} deg C'.format(m.temperature))
    print('Humidity  = {:0.2f} %'.format(m.humidity))
    print('Pressure  = {:0.2f} kPa'.format(m.pressure))

    m.sendLuftdaten()


sensorID  = config['luftdaten'].get('sensor')
starttime = time.time()

while True:
    print("running ...")
    run()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))

print("Stopped")
