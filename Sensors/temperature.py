#!/usr/bin/python
import Adafruit_DHT as ada

gpioPin = 4
sensorModel = ada.DHT11

def getMeasurement():
    humidity, temperature = ada.read_retry(sensorModel, gpioPin)
    measurement = temperature
    return measurement
