#darc, the Durham Adaptive optics Real-time Controller.
#Copyright (C) 2010 Alastair Basden.

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as
#published by the Free Software Foundation, either version 3 of the
#License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Affero General Public License for more details.

#You should have received a copy of the GNU Affero General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#This is a configuration file for SPHERE.
#Aim to fill up the control dictionary with values to be used in the RTCS.

#import correlation
import FITS
import tel
import numpy

#
# This configuration file corresponds to the GTCAO system
# Main configuration parameters:
# Single Conjugate Adaptive Optics (SCAO)
# 20x20 subapertures Shack Hartmann array
# 373 actuators CILAS DM (21 across pupil), sFPDP and RS485 interface
# Firstlight OCam2 Camera with 240x240 pixels E2V CCD220, 1500fps
# Tip-tilt correction with GTC M2
# 

ncam=1# This is the number of camera objects in the system [11.1]

nsubaps=20 # This is the number of subapertures across the pupil diameter 
nact=nsubaps+1
nacts=375# 373 + 2 (TT).   

npxl=10 # This is the number of pixels per side of each subaperture 
subapPitch=12# 12 pixels between subaps
#I doubt between 10 or 12 for this parameter. Camera is 240x240 pixels, so 12x12 per subaperture, but what about guard pixels??

npxlx=numpy.zeros((ncam,),numpy.int32) # number of pixels in the horizontal direction [11.4]
npxlx[:]=240#nsubaps*npxl 
npxly=npxlx.copy() # number of pixels in the vertical direction [11.5]
nsuby=npxly.copy()
nsuby[:]=nsubaps
nsubx=nsuby.copy()
nsub=(nsuby*nsubx).sum()  # number of subapertures [11.3]



subapFlag=tel.Pupil(nsubaps,nsubaps/2.,2,nsubaps).subflag.ravel().astype("i")# specifies whether this subaperture should be used or not [11.9]

# subapFlag needed to compute subapLocation

# go [11.10] defined directly in "control"

# Defining subapLocation, specifies the layout of subapertures for the system [11.7]

subapLocation=numpy.zeros((nsub,6),"i")
nsubapsCum=numpy.zeros((ncam+1,),numpy.int32)
ncentsCum=numpy.zeros((ncam+1,),numpy.int32)
for i in range(ncam):
    nsubapsCum[i+1]=nsubapsCum[i]+nsuby[i]*nsubx[i]
    ncentsCum[i+1]=ncentsCum[i]+subapFlag[nsubapsCum[i]:nsubapsCum[i+1]].sum()*2

# now set up a default subap location array...
#this defines the location of the subapertures.
subx=npxl
suby=npxl
xoff=1#1 pixel inset due to guard ring.
yoff=1
for k in range(ncam):
    for i in range(nsuby[k]):
        for j in range(nsubx[k]):
            indx=nsubapsCum[k]+i*nsubx[k]+j
            if subapFlag[indx]:
                subapLocation[indx]=(yoff+i*subapPitch,yoff+i*subapPitch+suby,1,xoff+j*subapPitch,xoff+j*subapPitch+subx,1)

windowMode="basic" #string either "basic", "adaptive" or "global" windowing mode [11.8]

pxlCnt=numpy.zeros((nsub,),"i")
# set up the pxlCnt array - number of pixels to wait until each subap is ready.  Here assume identical for each camera. Computed from subapLocation [11.7]
for k in range(ncam):
    # tot=0#reset for each camera
    for i in range(nsuby[k]):
        for j in range(nsubx[k]):
            indx=nsubapsCum[k]+i*nsubx[k]+j
            n=(subapLocation[indx,1]-1)*npxlx[k]+subapLocation[indx,4]
            pxlCnt[indx]=n



# pause [11.12] defined directly in "control"

# printTime [11.13] defined directly in "control"

# ncamThreads [11.14]
ncamThreads=numpy.ones((ncam,),numpy.int32)*4 # Array spcifying the number of Threads for each frame grabber 

# switchRequested [11.15] defined directly in "control"

# actuators [11.16]
actuators=None #(numpy.random.random((3,52))*1000).astype("H"),#None,#an array of actuator values.

#threadAffinity  [11.17]
threadAffinity=None 

# threadPriority [11.18]
threadPriority=numpy.ones((ncamThreads.sum()+1,),numpy.int32)*10

# threadPriority [11.19]
delay=0

# threadPriority [11.20]
clearErrors=0

# threadPriority [11.21]
camerasOpen=1 #set to 0 if you don't want the cameras open at start.  Usually useful to have it set to 1 (unless your cameras/interface doesn't exist).

# cameraParams[11.22]
#Define Camera parameters. The params are dependent on the interface library used.
#You will need a darc interface library that is suitable for your ocam and matrox frame grabber.  cameraName should then point to this, and cameraParams will be dependent on what is required for this library.

#Here, define one to connect to the simulation.
host="localhost"
while len(host)%4!=0:
    host+='\0'

cameraParams=numpy.zeros((2+len(host)//4,),numpy.int32)
cameraParams[0]=1#asfloat
cameraParams[1]=8000#port
cameraParams[2:]=numpy.fromstring(host,dtype=numpy.int32)
mirrorParams=numpy.zeros((7+len(host)//4,),"i")
mirrorParams[0]=1#timeout
mirrorParams[1]=8000#port on receiver
mirrorParams[2]=1#affin el size
mirrorParams[3]=1#priority
mirrorParams[4]=-1#affinity
mirrorParams[5]=0#send prefix
mirrorParams[6]=1#as float
mirrorParams[7:]=numpy.fromstring(host,dtype=numpy.int32)


# cameraName[11.23]
cameraName="libcamsocket.so" #which needs creating!
 
#for testing - comment out the next 5 lines when finished:

# mirrorOpen [11.24]
mirrorOpen=1

# mirrorName [11.25]
mirrorName="libmirrorSocket.so"


# mirrorParams [11.30]
#Define Mirror parameters. The params are dependent on the interface library used.
#Defined above.



# frameno [11.26]
frameno=0

# nsteps [11.27]
nsteps=0

# closeLoop [11.28] 
closeLoop=1 #Probably you want this set to 0 here, and only when you've configured the system (uploaded reference slopes, calibration images, control matrix etc), then set closeLoop to 1.  Otherwise you risk sending bad commands to the DM.
#Actually - since you start with mirrorOpen equal to zero this has the same effect.

# mirrorParams [11.30] (Ver mas arriba, despues de [11.25])

# addActuators [11.31] 0 to replace RTC computed values by user defined actuarotes or 1 to add them
addActuators=0

# actSequence [11.32] used when actuators are specified: defines the no of times each set of actuators should be placed on the mirror
actSequence=None    #numpy.ones((3,),"i")*1000,

# recordCents [11.33] used to compute an interaction matrix of reference slopes. 
recordCents=0

# averageImg [11.34] used by GUI/in scripting. no of frames to averaget calibrated images for before publishin the result
averageImg=0

# actuatorMask [11.38] a mask of size equal to the number of actuators to specify which user defined actuators shoule be used
actuatorMask=None

# dmDescription [11.39] 

#Now describe the DM - this is for the GUI only, not the RTC.
#The format is: ndms, N for each DM, actuator numbers...
#Where ndms is the number of DMs, N is the number of linear actuators for each, and the actuator numbers are then an array of size NxN with entries -1 for unused actuators, or the actuator number that will set this actuator in the DMC array.

dmDescription=numpy.zeros((nact*nact+1+1,),numpy.int16)
dmDescription[0]=1#1 DM
dmDescription[1]=nact #1st DM has nact linear actuators
tmp=dmDescription[2:]
tmp[:]=-1
tmp.shape=nact,nact
dmflag=tel.Pupil(nact,nact/2.,1).fn.ravel()
numpy.put(tmp,dmflag.nonzero()[0],numpy.arange(nacts))

# averageCent [11.40] equal to the no of frames to average centroids too before publishing result once to the generic stream
averageCent=0

# I THINK THE FOLLOWING 3 PARAMETERS SHOULD BE AT THE 11.58 FIGURE SENSOR INTERFACE????

# figureOpen [11.42]
figureOpen=0
    
# figureName [11.43]
figureName="figureSL240"

# figureParams [11.44]
figureParams=None

# reconName [11.45]
reconName="libreconmvm.so"

# reconlibOpen [11.46]
reconlibOpen=1

# Calibration interface (librtccalibrate.so) [11.53]
powerFactor=1.#raise pixel values to this power.[11.53.1]
bgImage=None#FITS.Read("shimgb1stripped_bg.fits")[1].astype("f")#numpy.zeros((npxls,),"f") [11.53.2]
darkNoise=None#FITS.Read("shimgb1stripped_dm.fits")[1].astype("f") [11.53.3]
flatField=None#FITS.Read("shimgb1stripped_ff.fits")[1].astype("f") [11.53.4]
thresholdAlgo=1 #[11.53.5]
thresholdValue=0. #could also be an array.[11.53.6]
pxlWeight=None #[11.53.7]
fakeCCDImage=None #(numpy.random.random((npxls,))*20).astype("i") [11.53.8]
useBrightest=0 #[11.53.12] - this one is well worth investigating when you have the system working.  Depending on spot size, I recommend a value between -15 to -40.
# end calibration interface

# Slope interface [11.54]
centroidMode="CoG" #text string "WPU", "CoG", "Gaussian", "CorrelationCoG", "CorrelationGaussian" [11.54.1]
centroidWeight=None #[11.54.2]
refCentroids=None# [11.54.3]
adaptiveWinGain=0.5#a gain factor to be used when adaptive windowing[11.54.4]
fluxThreshold=0 #[11.54.9]
maxAdapOffset=0 #[11.54.10]
centCalSteps=None # [11.54.11]
centCalData=None # [11.54.12]
centCalBounds=None# [11.54.13]
# end slope interface

# MVM reconstruction interface [11.55]
decayFactor=None #used in libreconmvm.so [11.55.1]
reconstructMode="simple" #string with value "simple", "truth" , "open" or "offfset" [11.55.3]
ncents=subapFlag.sum()*2
v0=numpy.ones((nacts,),"f")*32768 #initial voltages [11.55.5]
rmx=numpy.zeros((nacts,ncents)).astype("f")#FITS.Read("rmxRTC.fits")[1].transpose().astype("f") [11.55.6]
E=numpy.zeros((nacts,nacts),"f") # the E matrix (Basden 2012) [11.55.7]
gain=numpy.ones((nacts,),"f")#actuator gain, specifique for each [11.55.8]
#end MVM reconstruction interface

# Typical mirror interfaces [11.56]
bleedGain=0.0 #0.05,#a gain for the piston bleed...[11.56.1]
actMax=numpy.ones((nacts,),numpy.float32)*65535#4095,#max actuator value [11.56.2]
actMin=numpy.zeros((nacts,),numpy.float32)#4095,#max actuator value [11.56.3]
maxClipped=nacts/10 #maximum number of actuators allowed to be clipped before an error is raised [11.56.4]
# end typical mirror interfaces

# Figure sensor interface [11.58]
figureGain=1 #[11.58.1]
# end of figure sensor interface

# THESE PARAMETERS ARE NOT COMMENTED IN THE DARC MANUAL
switchTime=numpy.zeros((1,),"d")[0] # not essential but stores a timestamp (generated by darc) of when the parameters were last changed.
#Mode="basic" 
#nsubapsTogether=1 # No longer used
printUnused=1   #Prints out a list of unused parameters.  Not important.

##################################################################################
# Define parameters of control loop

control={
    "ncam":ncam,
    "nacts":nacts,
    "nsub":nsuby*nsubx,
    "npxly":npxly,
    "npxlx":npxlx,
    "subapLocation":subapLocation,
    "windowMode":windowMode,
    "subapFlag":subapFlag,
    "go":1, 
    "pxlCnt":pxlCnt,
    "pause":0,
    "printTime":0,#whether to print time/Hz
    "ncamThreads":ncamThreads,
    "switchRequested":0,#this is the only item in a currently active buffer that can be changed...
    "actuators":None,#(numpy.random.random((3,52))*1000).astype("H"),#None,#an array of actuator values.
    "threadAffinity":threadAffinity,
    "threadPriority":threadPriority,
    "delay":delay,
    "clearErrors":clearErrors,
    "camerasOpen":camerasOpen,
    "cameraName":cameraName,#"camfile",
    "cameraParams":cameraParams,
    "mirrorOpen":mirrorOpen,   
    "mirrorName":mirrorName,
    "mirrorParams":mirrorParams,
    "frameno":frameno,
    "nsteps":nsteps,
    "closeLoop":closeLoop,
    "addActuators":addActuators,
    "actSequence":None,#numpy.ones((3,),"i")*1000,
    "recordCents":recordCents,
    "averageImg":averageImg,
    "actuatorMask":actuatorMask,
    "dmDescription":dmDescription,  
    "averageCent":averageCent,
    "figureOpen":figureOpen,
    "figureName":figureName,
    "figureParams":figureParams,
    "reconName":reconName,
    "reconlibOpen":reconlibOpen,
# calibration interface
    "powerFactor":powerFactor,#raise pixel values to this power.
    "bgImage":bgImage,
    "darkNoise":darkNoise,
    "flatField":flatField,#numpy.random.random((npxls,)).astype("f"),
    "thresholdAlgo":thresholdAlgo,
    "thresholdValue":thresholdValue,#could also be an array.
    "pxlWeight":pxlWeight,
    "fakeCCDImage":fakeCCDImage,
    "useBrightest":useBrightest,
#end calibration interface
#
# Slope interface   
    "centroidMode":centroidMode,#whether data is from cameras or from WPU.
    "centroidWeight":centroidWeight,
    "refCentroids":refCentroids,
    "adaptiveWinGain":adaptiveWinGain,
    "fluxThreshold":fluxThreshold,
    "maxAdapOffset":maxAdapOffset,
    "centCalSteps":centCalSteps, 
    "centCalData":centCalData, 
    "centCalBounds":centCalBounds,
# end slope interface    
#
# Typical Mirror Interface 
    "bleedGain":bleedGain,#0.05,#a gain for the piston bleed... [11.56.1]
    "actMax":actMax,#4095,#max actuator value [11.56.2]
    "actMin":actMin,#4095,#max actuator value [11.56.3]
    "maxClipped":nacts,#[11.56.4]
# end typical mirror interface
#
# MVM reconstruction interface
    "decayFactor":decayFactor,#used in libreconmvm.so
    "reconstructMode":reconstructMode,
    "ncents":ncents,
    "v0":v0,    
    "rmx":rmx,
    "E":E,
    "gain":gain,
# end MVM reconstruction interface
#
# Figure sensor interface 
    "figureGain":figureGain,
# end of figure sensor interface
#
    "switchTime":switchTime, 
    #"Mode":Mode,
    #"nsubapsTogether":nsubapsTogether,
    "printUnused":printUnused,   
    "version":" "*120,
    }


