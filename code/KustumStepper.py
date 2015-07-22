import time
import math
import sys
import numpy as np
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

global XMotor1
global XMotor2
global XMotor3
global XMotor4

global YMotor1
global YMotor2
global YMotor3
global YMotor4

global SpindleRelay 
global ZRelay

global XLimitSwitch
global YLimitSwitch

global DeltaX
global DeltaY

global XDim 
global YDim 

global X 
global Y 

XMotor1 = 7
XMotor2 = 11
XMotor3 = 13
XMotor4 = 15

YMotor1 = 12
YMotor2 = 16
YMotor3 = 18
YMotor4 = 22

SpindleRelay = 31 
ZRelay = 33

XLimitSwitch = 32
YLimitSwitch = 36

XDelta = 1e-3 #m
YDelta = 1e-3 #m
Delay = 0.05
XDim = 1e-2 #m
YDim = 1e-2 #m

X = 0
Y = 0

#def XHome(channel):

#def YHome(channel):

GPIO.setup(XMotor1, GPIO.OUT)
GPIO.setup(XMotor2, GPIO.OUT)
GPIO.setup(XMotor3, GPIO.OUT)
GPIO.setup(XMotor4, GPIO.OUT)

GPIO.setup(YMotor1, GPIO.OUT)
GPIO.setup(YMotor2, GPIO.OUT)
GPIO.setup(YMotor3, GPIO.OUT)
GPIO.setup(YMotor4, GPIO.OUT)

GPIO.setup(SpindleRelay, GPIO.OUT)
GPIO.setup(ZRelay, GPIO.OUT)

GPIO.setup(XLimitSwitch, GPIO.IN)
GPIO.setup(YLimitSwitch, GPIO.IN)

#GPIO.add_event_detect(XLimitSwitch, GPIO.RISING, callback=XHome)
#GPIO.add_event_detect(YLimitSwitch, GPIO.RISING, callback=YHome)

def Step(axis, dir):
    if axis==0:
        if dir<0:
            GPIO.output(XMotor1,1)
            GPIO.output(XMotor3,0)
            GPIO.output(XMotor2,0)
            GPIO.output(XMotor4,0)
            time.sleep(Delay)
            GPIO.output(XMotor1,0)
            GPIO.output(XMotor3,1)
            GPIO.output(XMotor2,0)
            GPIO.output(XMotor4,0)
            time.sleep(Delay)
            GPIO.output(XMotor1,0)
            GPIO.output(XMotor3,0)
            GPIO.output(XMotor2,1)
            GPIO.output(XMotor4,0)
            time.sleep(Delay)
            GPIO.output(XMotor1,0)
            GPIO.output(XMotor3,0)
            GPIO.output(XMotor2,0)
            GPIO.output(XMotor4,1)
            time.sleep(Delay)
        else:
            GPIO.output(XMotor1,0)
            GPIO.output(XMotor3,0)
            GPIO.output(XMotor2,0)
            GPIO.output(XMotor4,1)
            time.sleep(Delay)
            GPIO.output(XMotor1,0)
            GPIO.output(XMotor3,0)
            GPIO.output(XMotor2,1)
            GPIO.output(XMotor4,0)
            time.sleep(Delay)
            GPIO.output(XMotor1,0)
            GPIO.output(XMotor3,1)
            GPIO.output(XMotor2,0)
            GPIO.output(XMotor4,0)
            time.sleep(Delay)
            GPIO.output(XMotor1,1)
            GPIO.output(XMotor3,0)
            GPIO.output(XMotor2,0)
            GPIO.output(XMotor4,0)
            time.sleep(Delay)
    
    elif axis==1:
        if dir<0:
            GPIO.output(YMotor1,1)
            GPIO.output(YMotor3,0)
            GPIO.output(YMotor2,0)
            GPIO.output(YMotor4,0)
            time.sleep(Delay)
            GPIO.output(YMotor1,0)
            GPIO.output(YMotor3,1)
            GPIO.output(YMotor2,0)
            GPIO.output(YMotor4,0)
            time.sleep(Delay)
            GPIO.output(YMotor1,0)
            GPIO.output(YMotor3,0)
            GPIO.output(YMotor2,1)
            GPIO.output(YMotor4,0)
            time.sleep(Delay)
            GPIO.output(YMotor1,0)
            GPIO.output(YMotor3,0)
            GPIO.output(YMotor2,0)
            GPIO.output(YMotor4,1)
            time.sleep(Delay)
        else:
            GPIO.output(YMotor1,0)
            GPIO.output(YMotor3,0)
            GPIO.output(YMotor2,0)
            GPIO.output(YMotor4,1)
            time.sleep(Delay)
            GPIO.output(YMotor1,0)
            GPIO.output(YMotor3,0)
            GPIO.output(YMotor2,1)
            GPIO.output(YMotor4,0)
            time.sleep(Delay)
            GPIO.output(YMotor1,0)
            GPIO.output(YMotor3,1)
            GPIO.output(YMotor2,0)
            GPIO.output(YMotor4,0)
            time.sleep(Delay)
            GPIO.output(YMotor1,1)
            GPIO.output(YMotor3,0)
            GPIO.output(YMotor2,0)
            GPIO.output(YMotor4,0)
            time.sleep(Delay)

def Travel(Xprime, Yprime):
    global X
    global Y
    X0=X
    Y0=Y
    XDistance=XPrime-X
    YDistance=YPrime-Y
    XSteps = np.round(abs(XDistance)/XDelta)
    YSteps = np.round(abs(YDistance)/YDelta)
    XDir = np.sign(XDistance)
    YDir = np.sign(YDistance)
    
    print 'XSteps ', XSteps
    print 'YSteps ', YSteps
    if XSteps = 0:
        i = 0
        print 'Step Y'
        while i<YSteps:
            Step(1, YDir)
            i=i+1
            Y=Y+YStep*YDir
    elif YSteps = 0:
        print 'Step X'        
        i = 0
        while i<XSteps:
            Step(0, XDir)
            i=i+1
            X=X+XStep*XDir        
    else:
        Slope = YDistance/YDistance
        if abs(Slope)<=0.5:
            i=0
            while i<XSteps:
                Step(0, XDir)
                i=i+1
                X=X+XStep*XDir                
                Yi = Y
                Yi1 = Y+YStep*Ydir
                if abs((Yi1-Y0)-Slope*(X-X0))<abs((Yi-Y0)-Slope*(X-X0)):
                    Y=Yi1
                else:
                    Y=Yi
        else:
            i=0
            while i<YSteps:
                Step(1, YDir)
                i=i+1
                Y=Y+YStep*YDir                
                Xi = X
                Xi1 = X+XStep*Xdir
                if abs((Xi1-X0)-1/Slope*(Y-Y0))<abs((Xi-X0)-1/Slope*(Y-Y0)):
                    X=Xi1
                else:
                    X=Xi

def Spindle(DurationSpindle):
    GPIO.output(SpindleRelay,1)
    time.sleep(DurationSpindle)
    GPIO.output(SpindleRelay,0)

def ZSolenoid(DurationZ,DurationSpindle):
    GPIO.output(ZRelay,1)
    time.sleep((DurationZ-DurationSpindle)/2)
    Spindle(DurationSpindle)
    time.sleep((DurationZ-DurationSpindle)/2)
    GPIO.output(ZRelay,0)

Travel(.1,.1)
ZSolenoid(1,.5):
Travel(0,0)
        
GPIO.cleanup()
quit()
