#!/usr/bin/env python3

import sys
import os
import yaml
import time
import json
import requests


# Config
with open("config.yml", 'r') as ymlfile:
    config = yaml.load(ymlfile)

# Logging
import logging
logging.basicConfig(level=logging.DEBUG)


class Measurement:
    def __init__(self):
        self.pm25_value  = pm25_values
        self.pm10_value  = pm10_values
        self.temperature = bme280.read_temperature()
        self.humidity    = bme280.read_humidity()
        self.pressure    = bme280.read_pressure()


    def sendLuftdaten(self):
        if not config['luftdaten']['enabled']:
            return


        self.__pushLuftdaten('https://api.luftdaten.info/v1/push-sensor-data/', 1, {
            "P1": self.pm10_value,
            "P2": self.pm25_value,
        })
        self.__pushLuftdaten('https://api.luftdaten.info/v1/push-sensor-data/', 11, {
            "temperature": self.temperature,
            "pressure":    self.pressure,
            "humidity":    self.humidity,
        })


    def __pushLuftdaten(self, url, pin, values):
        requests.post(url,
            json={
                "software_version": "python-dusty 0.0.1",
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
    print('Pressure  = {:0.2f} hPa'.format(m.pressure/100))

    m.sendLuftdaten()
    m.sendInflux()


sensorID  = config['luftdaten'].get('sensor')
starttime = time.time()

while True:
    print("running ...")
    run()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))

print("Stopped")
