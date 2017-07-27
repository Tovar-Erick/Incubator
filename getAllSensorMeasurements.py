import os
import sys
import base64
import math
import logging
import socket
import json
import string
import random
from datetime import datetime

this_program = sys.argv[0]
this_fullpath = os.path.realpath(__file__)
this_path = this_fullpath[:-len(this_program)]
utils_path = this_path+'utils'

sys.path.insert(0, utils_path)
import compressImages as ci
import publishMqtt as myMqtt
import ledMatrix

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Setup sensor and camera modules
sensor_names = [ 'temperature'
               , 'humidity'
               ]
camera_name = 'piCamera'

sensors_subfolder = 'Sensors'
cameras_subforder = 'Cameras'

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getModules():
    """ This function enables the sensors and cameras used by the RB
        Sensors are contained in subdirectory Sensors, and listed as list in sensor_names
        Camera is contained in subdirectory Cameras, and listed as variable in camera_name"""
    this_path = os.path.dirname(os.path.abspath(__file__))
    sensors_path = os.path.join(this_path, sensors_subfolder)
    sys.path.insert(0, sensors_path)
    camera_path = os.path.join(this_path, cameras_subforder)
    sys.path.insert(0, camera_path)
    sensor_modules = (__import__(sensor_name) for sensor_name in sensor_names)
    camera_module = __import__(camera_name)
    return sensor_modules, camera_module

def convertPhotoToBase64(photo_name):
    with open(name=photo_name, mode='rb') as image_file:
        encodedImage = base64.b64encode(image_file.read())
    return encodedImage

def getSplitMessage(message):
    chunkSize = 3000
    length = len(message)
    no_of_chunks = int(math.ceil(length / chunkSize))
    chunks = []

    for chunk_number in range(no_of_chunks):
        if(chunk_number == no_of_chunks-1):
            chunks.append(message[(chunk_number*chunkSize) : ])
        else:
            chunks.append(message[ (chunk_number*chunkSize) : ((chunk_number+1)*chunkSize) ])
    return chunks
# "soy un mensajin " + str(now)
def getRBunit():
    return socket.gethostname()

def getJsonSensorMessage(sensor_name, measurement):
    data = {'sensor_name': sensor_name\
           ,'measurement':measurement\
           ,'datetime':now\
           ,'RBunit': getRBunit()\
           ,'message_type': 'sensor'}
    jsonData = json.JSONEncoder().encode(data)
    return jsonData

def getRandomId():
    return ''.join(random.choice(string.lowercase) for iter in range(10))

def getJsonCameraMessage(cameraData):
    random_id = getRandomId()
    dataOutput = []
    for dataChunk, chunk_number in zip(cameraData, range(1,len(cameraData)+1)):
        tmpData = {'message_number':chunk_number\
                  ,'total_messages':len(cameraData)\
                  ,'message_id':random_id\
                  ,'camera_name': camera_name\
                  ,'data':dataChunk\
                  ,'datetime':now\
                  ,'RBunit': getRBunit()\
                  ,'message_type': 'camera'}
        # jsonData = json.JSONEncoder().encode(tmpData)
        jsonData = json.dumps(tmpData)
        dataOutput.append(jsonData)
    return dataOutput

def getCameraData():
    # Get camera image
    photo_name = camera_module.capturePhoto()
    logging.debug('Photo pathname: {}'.format(photo_name))

    # Compress image
    compressor = ci.CompressImage() #Object from CompressImage class
    photo_name = compressor.processfile(photo_name) #compress image
    logging.debug('Image compressed {}'.format(photo_name))

    # Encode image to text
    encodedImage = convertPhotoToBase64(photo_name)
    splitedMessage = getSplitMessage(message=encodedImage)
    return splitedMessage

if __name__ == '__main__':
    sensor_modules, camera_module = getModules()
    ledMatrix.flashOn(100)
    # Get measurement from each sensor, invokes getMeasurement() from each sensor programm
    measurements = (sensor_module.getMeasurement() for sensor_module  in sensor_modules)

    jsonSensorsData = (getJsonSensorMessage(sensor_name, measurement) for (sensor_name, measurement) in zip(sensor_names, measurements))

    cameraData = getCameraData()
    jsonCameraData = getJsonCameraMessage(cameraData)

    # Publish data to Mqtt
    for dataCam in jsonCameraData:
        myMqtt.publishCamera(dataCam)

    for dataSen in jsonSensorsData:
        myMqtt.publishSensor(dataSen)

    #TODO: Delete image from disk

    #TODO: Implement a confirmation routine for incomplete transferred images
