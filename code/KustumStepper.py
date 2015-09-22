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

global XDelta
global YDelta

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

def XHome(channel):
    print("XLimit")
    Step(0, 1)
    if GPIO.input(XLimitSwitch):
        pass
    else:
        Step(0,-1)
        Step(0,-1)

def YHome(channel):
    print("YLimit")
    Step(1, 1)
    if GPIO.input(YLimitSwitch):
        pass
    else:
        Step(1,-1)
        Step(1,-1)

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

#GPIO.add_event_detect(XLimitSwitch, GPIO.FALLING, callback=XHome)
#GPIO.add_event_detect(YLimitSwitch, GPIO.FALLING, callback=YHome)

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

def Travel(X1, Y1):
    global X
    global Y
    X0=X
    Y0=Y
    XDistance=X1-X0
    YDistance=Y1-Y0
    XSteps = np.round(abs(XDistance)/XDelta)
    YSteps = np.round(abs(YDistance)/YDelta)
    XDir = np.sign(XDistance)
    YDir = np.sign(YDistance)

    steep = (YSteps) > (XSteps)
    
    print 'XSteps ', XSteps
    print 'YSteps ', YSteps
    if XSteps == 0:
        i = 0
        print 'Step Y'
        while i<YSteps:
            Step(1, YDir)
            i=i+1
            Y=Y+YDelta*YDir
    elif YSteps == 0:
        print 'Step X'        
        i = 0
        while i<XSteps:
            Step(0, XDir)
            i=i+1
            X=X+XDelta*XDir        
    else:
        Slope = YDistance/YDistance
        if abs(Slope)<=1:
            i=0
            while i<XSteps:
                Step(0, XDir)
                print "Step X"
                i=i+1
                X=X+XDelta*XDir                
                Yi = Y
                Yi1 = Y+YDelta*YDir
                if abs((Yi1-Y0)-Slope*(X-X0))<YDelta/2:
                    Y=Yi1
                    Step(1, YDir)
                    print "Step Y"
                else:
                    Y=Yi
        else:
            i=0
            while i<YSteps:
                Step(1, YDir)
                print "Step Y"
                i=i+1
                Y=Y+YDelta*YDir                
                Xi = X
                Xi1 = X+XDelta*XDir
                if abs((Xi1-X0)-1/Slope*(Y-Y0))<XDelta/2:
                    X=Xi1
                    Step(0, XDir)
                    print "Step X"
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

def Home():
    while not GPIO.input(XLimitSwitch):
        Step(0,-1)
        print("Step")

    while not GPIO.input(YLimitSwitch):
        Step(1,-1)
        print("Step")

    global X
    X=0
    global Y
    Y=0

#Home()
Travel(.5,.25)

Travel(-.25,-.5)

for i in range(0,20):
    ZSolenoid(10,5)
    time.sleep(10)

#Home()
GPIO.cleanup()
quit()
