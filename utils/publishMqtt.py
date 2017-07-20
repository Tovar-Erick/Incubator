import paho.mqtt.client as mqtt
import socket
import logging

channel = None
sensors_channel = 'JICA/Plantitas/Sensors'
camera_channel = 'JICA/Plantitas/Camera'
activate_channel = 'JICA/Plantitas/Activate'

broker_address = "test.mosquitto.org"
port = 1883
keepalive = 60
client_id = socket.gethostname()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe(channel)
    else:
        raise RuntimeError('Error connecting to {0} with rc: {1}'.format(channel, rc))

def on_log(client, userdata, level, buf):
    print("log: ", buf)

def publishMessage(jsonData):
    #New instance
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    # client.on_log = on_log
    client.connect(broker_address, port, keepalive)
    client.loop_start()
    # logging.debug('Posting [{}]'.format(jsonData))
    client.publish(channel, jsonData)
    client.disconnect()
    client.loop_stop()

def publishSensor(jsonData):
    global channel
    channel  = sensors_channel
    publishMessage(jsonData)

def publishCamera(jsonData):
    global channel
    channel = camera_channel
    publishMessage(jsonData)

def publishActivate(jsonData):
    global channel
    channel = activate_channel
    publishMessage(jsonData)
