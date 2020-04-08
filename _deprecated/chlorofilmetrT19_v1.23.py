import datetime
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep
import os
from fractions import Fraction
import numpy as np
from PIL import Image
import argparse

path = '/home/pi/chlorofilmetr/'

def GetCurrTime():
    currtime = str(datetime.datetime.now().date()) + '_'+ str(datetime.datetime.now().strftime("%H-%M-%S.%f"))
    return currtime

def SetGPIO():
    GPIO.setmode(GPIO.BOARD) # or GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(15, GPIO.IN)
    GPIO.setup(16, GPIO.OUT)
    LED = 0
#    LED = GPIO.PWM(8,5000)          #GPIO19 as PWM output, with 100Hz frequency
#    LED.start(0)                    #generate PWM signal with 0% duty cycle
    return LED

def SetCamera(awb_gains_set):
    camera = PiCamera()
    camera.rotation = 180
    #camera.resolution = (256,192)
    camera.resolution = (1280, 720)
    camera.start_preview(alpha=255)
    
#    camera.shutter_speed = 100
#    camera.analog_gain = 100
#    camera.digital_gain = 100

    GPIO.output(16, GPIO.HIGH)
    camera.shutter_speed = camera.exposure_speed
    print(" - shutter/exposure speed: " + str(camera.exposure_speed))
    camera.exposure_mode = 'off'
    
##   CALIBRATION:    
#    for measurement in range(1000000):
#        g = camera.awb_gains
#        print(" - awb_gains/awb_gains: " + str(g))
#        sleep(0.1)
#    camera.awb_mode = 'off'
#    camera.awb_gains = g
    
    camera.awb_mode = 'off'
#    awb_gains = (Fraction(47, 128), Fraction(177, 128))
    awb_gains = (Fraction(awb_gains_set[0], awb_gains_set[1]), Fraction(awb_gains_set[2], awb_gains_set[3]))
    #camera.awb_gains = awb_gains
    camera.awb_gains = (1.1, 2.5)
    print(" - awb_gains: " + str(awb_gains))
#    camera.iso = 800
#    GPIO.output(16, GPIO.LOW)

    return camera

def MakeRepository(path):
    path = path + "testframes/"
    currtime = GetCurrTime()
    newrepos = path + currtime + "/"
    if not os.path.exists(newrepos):
        os.mkdir(newrepos)
        print("Directory created:")
        print(" - " + newrepos)
    else:    
        print("Directory already exists:\n ")
        print(" - " + newrepos)
    return newrepos, currtime

def MakeLogfile(repos,currtime):
    logfile = str(repos + "log" + currtime + ".csv")
    with open(logfile, 'w') as f:
        f.write("measurement;R_;G_;B_;r;g;b;mean_rgb;ExG;ExG_n;honza_1;vasek_1;\n")
        f.close 
    return logfile

def ArgParser():
    parser = argparse.ArgumentParser(description='CHLOROFILMETR T19\nThe MIT License (MIT)\nCopyright (c) 2019 CULS Prague')
    parser.add_argument('awb_gains_1', type=int, help='awb_gains_1')
    parser.add_argument('awb_gains_2', type=int, help='awb_gains_2')
    parser.add_argument('awb_gains_3', type=int, help='awb_gains_3')
    parser.add_argument('awb_gains_4', type=int, help='awb_gains_4')
    args = parser.parse_args()
#    parser.print_help()
    return args
    
def DoneIndication():
    for x in range(10):
        sleep(0.1)
        GPIO.output(16, not GPIO.input(16))
#        LED.ChangeDutyCycle((x%2) * 20)
#        print(" - actual pwm:", str((x%2) * 20))
#        LED.ChangeDutyCycle(x * 2)
#        print(" - actual pwm:", str((x * 2)))

if __name__ == "__main__":
    try:
        args = ArgParser()
        awb_gains_1 = args.awb_gains_1
        awb_gains_2 = args.awb_gains_2
        awb_gains_3 = args.awb_gains_3
        awb_gains_4 = args.awb_gains_4
    except:
        awb_gains_1 = 65
        awb_gains_2 = 256
        awb_gains_3 = 315
        awb_gains_4 = 128
        print(" - set default awb_gains values")
    awb_gains_set = [awb_gains_1,awb_gains_2,awb_gains_3,awb_gains_4]
        
    
#    print(str(args))


    # =============================================================================
    # SETUP
    # =============================================================================
    print("\n\nCHLOROFILMETR T19") 
    print("The MIT License (MIT)")
    print("Copyright (c) 2019 CULS Prague TF")
    
    print ("_" * 70)
    print("Setup:")   
     
    LED = SetGPIO()
    camera = SetCamera(awb_gains_set)
    repos,currtime = MakeRepository(path)
    logfile = MakeLogfile(repos,currtime)
    
    print ("_" * 70)
    print("Measurement:")
    print(" - touch button for capture, hold for exit")
    
    # =============================================================================
    # MAIN
    # =============================================================================
    measurement = 1
    while True:
        button_value = GPIO.input(15) 
        
        if button_value > 0:
            GPIO.output(16, GPIO.HIGH)
#            LED.ChangeDutyCycle(20)

            sleep(0.8)            
            if GPIO.input(15) > 0:
                break
                
            for loop in range(5):
                print(loop)
                capture_file = ('frame_%03d' % measurement) + '.jpg'
                camera.capture(repos + capture_file)
                        
                three_matrix = np.asarray(Image.open(repos + capture_file))
                mean_r = np.mean(three_matrix[:,:,0])
                mean_g = np.mean(three_matrix[:,:,1])
                mean_b = np.mean(three_matrix[:,:,2])
                mean_rgb = np.mean(three_matrix)
            
                R_ = mean_r/255
                G_ = mean_g/255
                B_ = mean_b/255
                ExG = 2 *  G_ - R_ - B_
                        
                r = R_ / (R_ + G_ + B_)
                g = G_ / (R_ + G_ + B_)
                b = B_ / (R_ + G_ + B_)
                ExG_n = 2 *  g - r - b
                print("ExG_n: ",ExG_n) 
            
                honza_1 = ((mean_g / mean_rgb) - 1) * 1000
                vasek_1 = np.abs(180 - (((1 - ExG_n) * 100) - 199.8) * 1000)

                measured_values = [measurement,R_,G_,B_,r,g,b,mean_rgb,ExG,ExG_n,honza_1,vasek_1]
                with open(logfile, 'a') as f:
                    for value in range(len(measured_values)):
                        f.write(str(measured_values[value]))
                        f.write(";")
                    f.write("\n")
                    f.close 
                #print([measurement,R_,G_,B_,r,g,b,mean_rgb,ExG,ExG_n,honza_1,vasek_1])
            
            print ("." * 70)
            print("MEASUREMENT #" + str(measurement))
            print(capture_file + ' saved in time: ' + GetCurrTime())
            print("R_ = " + str(R_))
            print("G_ = " + str(G_))
            print("B_ = " + str(B_))
            print("r = " + str(r))
            print("g = " + str(g))
            print("b = " + str(b))
            print("whole = " + str(mean_rgb))
            print("ExG = " + str(ExG))
            print("ExG_n = " + str(ExG_n))
            print("honza_1 = " + str(honza_1))
            print("vasek_1 = " + str(vasek_1))
            print(" - awb_gains/awb_gains: " + str(camera.awb_gains))
            
            DoneIndication()
            measurement += 1

        else:
            a=1
            #GPIO.output(16, GPIO.LOW)
    
    GPIO.cleanup()        
    print("end")