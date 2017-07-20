import picamera
from time import sleep
from datetime import datetime
import sys
sys.path.insert(0,'../utils')
import ledMatrix

def getPhotoName():
    image_format = '.jpg'
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    this_camera = __file__[:-3]
    photo_name = this_camera + now + image_format
    return photo_name

#Warm-up time
def warmUp():
    warmUp_time = 2
    sleep(warmUp_time)

def getCamera():
    #TODO: Modify depending on how light affects the image: https://www.raspberrypi.org/documentation/raspbian/applications/camera.md
    camera = picamera.PiCamera()
    camera.led = True
    # camera.resolution = (1920, 1080) # 16:9
    # camera.resolution = (3280, 2464) # 4:3
    camera.resolution = (1640, 1232) # 4:3

    #For iso, a simple rule of thumb is that 100 and 200 are reasonable
    #values for daytime, while 400 and 800 are better for low light.
    camera.iso = 100
    # Wait for the automatic gain control to settle
    warmUp()
    # Now fix the values
    camera.shutter_speed = camera.exposure_speed
    camera.exposure_mode = 'off'
    gains = camera.awb_gains
    camera.awb_mode = 'off'
    camera.awb_gains = gains
    return camera

def capturePhoto():
    #TODO: Turn on lights
    ledMatrix.flashOn()
    camera = None

    try:
        camera = getCamera()
        camera.start_preview()
        warmUp()
        photo_name = getPhotoName()
        camera.capture(photo_name)
        camera.stop_preview()
        pass
    except Exception, e:
        print "Couldn't do it: %s" % e
        raise
    finally:
        if camera:
            camera.close()

    ledMatrix.flashOff()
    return photo_name

if __name__ == '__main__':
    capturePhoto()
