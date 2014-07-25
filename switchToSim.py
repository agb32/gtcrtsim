#make sure the rtsim and darc are running first...
import numpy
import darc
d=darc.Control()
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
cpOrig=d.Get("cameraParams")
mpOrig=d.Get("mirrorParams")
d.Set(["cameraName","mirrorName","camerasOpen","mirrorOpen","cameraParams","mirrorParams","closeLoop"],["libcamsocket.so","libmirrorSocket.so",1,1,cameraParams,mirrorParams,1])
print "Original:"
print cpOrig
print mpOrig

print "Final:"
print cameraParams
print mirrorParams
