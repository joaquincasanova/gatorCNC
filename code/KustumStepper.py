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
global Z 

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

def Travel(X1, Y1, Z1):
    global X
    global Y
    global Z

    X0=X
    Y0=Y
    Z0=Z
    XDistance=X1-X0
    YDistance=Y1-Y0
    XSteps = np.round(abs(XDistance)/XDelta)
    YSteps = np.round(abs(YDistance)/YDelta)
    XDir = np.sign(XDistance)
    YDir = np.sign(YDistance)

    steep = (YSteps) > (XSteps)
    if Z1>0:
        GPIO.output(ZRelay,True)
    else:
        GPIO.output(ZRelay,False)
    Z=Z1

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
        Slope = YDistance/XDistance
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

def Arc(lines):
    old_x_pos=x_pos;
    old_y_pos=y_pos;
    
    [x_pos,y_pos]=XYposition(lines);
    [i_pos,j_pos]=IJposition(lines);
    
    xcenter=old_x_pos+i_pos;   #center of the circle for interpolation
    ycenter=old_y_pos+j_pos;
           
           
    Dx=x_pos-xcenter;
    Dy=y_pos-ycenter;      #vector [Dx,Dy] points from the circle center to the new position
           
    r=sqrt(i_pos**2+j_pos**2);   # radius of the circle
    
    e1=[-i_pos,-j_pos]; #pointing from center to current position
    if (lines[0:3]=='G02'): #clockwise
        e2=[e1[1],-e1[0]];      #perpendicular to e1. e2 and e1 forms x-y system (clockwise)
    else:                   #counterclockwise
        e2=[-e1[1],e1[0]];      #perpendicular to e1. e1 and e2 forms x-y system (counterclockwise)
        
            #[Dx,Dy]=e1*cos(theta)+e2*sin(theta), theta is the open angle
        
    costheta=(Dx*e1[0]+Dy*e1[1])/r**2;
    sintheta=(Dx*e2[0]+Dy*e2[1])/r**2;        #theta is the angule spanned by the circular interpolation curve
               
    if costheta>1:  # there will always be some numerical errors! Make sure abs(costheta)<=1
        costheta=1;
    elif costheta<-1:
        costheta=-1;
 
    theta=arccos(costheta);
    if sintheta<0:
        theta=2.0*pi-theta;
        
    no_step=int(round(r*theta/dx/5.0));   # number of point for the circular interpolation
    
    for i in range(1,no_step+1):
        tmp_theta=i*theta/no_step;
        tmp_x_pos=xcenter+e1[0]*cos(tmp_theta)+e2[0]*sin(tmp_theta);
        tmp_y_pos=ycenter+e1[1]*cos(tmp_theta)+e2[1]*sin(tmp_theta);
        moveto(MX,tmp_x_pos,dx,MY, tmp_y_pos,dy,speed,True);
       

def XYposition(lines):
    #given a movement command line, return the X Y position
    xchar_loc=lines.index('X')
    i=xchar_loc+1
    while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
        i+=1
    x_pos=float(lines[xchar_loc+1:i])    
   
    ychar_loc=lines.index('Y')
    i=ychar_loc+1
    while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
        i+=1
    y_pos=float(lines[ychar_loc+1:i])    
   
    zchar_loc=lines.index('Z')
    i=zchar_loc+1
    while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
        i+=1
    z_pos=float(lines[zchar_loc+1:i])    
 
    return x_pos,y_pos,z_pos

def IJposition(lines):
    #given a G02 or G03 movement command line, return the I J position
    ichar_loc=lines.index('I');
    i=ichar_loc+1;
    while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
        i+=1;
    i_pos=float(lines[ichar_loc+1:i]);    
   
    jchar_loc=lines.index('J');
    i=jchar_loc+1;
    while (47<ord(lines[i])<58)|(lines[i]=='.')|(lines[i]=='-'):
        i+=1;
    j_pos=float(lines[jchar_loc+1:i]);    
 
    return i_pos,j_pos;

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
    GPIO.output(ZRelay,False)
    global Z
    Z=0

filename = sys.argv[1])
try:#read and execute G code
    for lines in open(filename,'r'):
        if lines==[]:
            1 #blank lines
        elif lines[0:3]=='G90':
            print 'start'
           
        elif lines[0:3]=='G20':# working in inch
            dx/=25.4
            dy/=25.4
            print 'Working in inch'
             
        elif lines[0:3]=='G21':# working in mm
            print 'Working in mm'  
           
        elif lines[0:3]=='M05':
            GPIO.output(SpindleRelay,False)
            print 'Laser turned off'
           
        elif lines[0:3]=='M03':
            GPIO.output(SpindleRelay,True)
            print 'Laser turned on'

        elif lines[0:3]=='G04':#dwell
 
        elif lines[0:3]=='M02':
            GPIO.output(SpindleRelay,False)
            print 'finished. shuting down'
            break
        elif (lines[0:3]=='G1F')|(lines[0:4]=='G1 F'):
            1#do nothing
        elif (lines[0:3]=='G0 ')|(lines[0:3]=='G1 ')|(lines[0:3]=='G01'):#|(lines[0:3]=='G02')|(lines[0:3]=='G03'):
            #linear engraving movement
            [x_pos,y_pos,zpos]=XYposition(lines)
            if (lines[0:3]=='G0 '):
                Travel(x_pos,y_pos,z_pos)
            else:
                Travel(x_pos,y_pos,z_pos)          
               
        elif (lines[0:3]=='G02')|(lines[0:3]=='G03'): #circular interpolation

Home()
time.sleep(10)
GPIO.cleanup()
quit()
