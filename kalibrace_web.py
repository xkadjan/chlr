import picamera
import picamera.array
import numpy as np
import RPi.GPIO as GPIO

def SetGPIO():
    GPIO.setmode(GPIO.BOARD) # or GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(15, GPIO.IN)
    GPIO.setup(16, GPIO.OUT)
    LED = 0
#    LED = GPIO.PWM(8,5000)          #GPIO19 as PWM output, with 100Hz frequency
#    LED.start(0)                    #generate PWM signal with 0% duty cycle
    return LED


LED = SetGPIO()
GPIO.output(16, GPIO.HIGH)
with picamera.PiCamera() as camera:
    while True:
        if GPIO.input(15) > 0:
            GPIO.output(16, GPIO.LOW)
            break
        camera.resolution = (1280, 720)
        camera.awb_mode = 'off'
        # Start off with ridiculously low gains
        rg, bg = (0.5, 0.5)
        camera.awb_gains = (rg, bg)
        with picamera.array.PiRGBArray(camera, size=(128, 72)) as output:
            # Allow 30 attempts to fix AWB
            for i in range(100000):
                # Capture a tiny resized image in RGB format, and extract the
                # average R, G, and B values
                camera.capture(output, format='rgb', resize=(128, 72), use_video_port=True)
                r, g, b = (np.mean(output.array[..., i]) for i in range(3))
                print('R:%5.2f, B:%5.2f = (%5.2f, %5.2f, %5.2f)' % (
                    rg, bg, r, g, b))
                # Adjust R and B relative to G, but only if they're significantly
                # different (delta +/- 2)
                if abs(r - g) > 2:
                    if r > g:
                        rg -= 0.1
                    else:
                        rg += 0.1
                if abs(b - g) > 1:
                    if b > g:
                        bg -= 0.1
                    else:
                        bg += 0.1
                camera.awb_gains = (rg, bg)
                output.seek(0)
                output.truncate()