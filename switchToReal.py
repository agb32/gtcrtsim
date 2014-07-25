import sys
import string
import numpy
import darc
if len(sys.argv)>1:
    print "Using config file %s"%sys.argv[1]
    execfile(sys.argv[1])
    cameraName=control["cameraName"]
    mirrorName=control["mirrorName"]
    cameraParams=control["cameraParams"]
    mirrorParams=control["mirrorParams"]
else:
    raise Exception("Not yet implemented")
d=darc.Control()
d.Set(["cameraName","mirrorName","camerasOpen","mirrorOpen","cameraParams","mirrorParams"],[cameraName,mirrorName,1,0,cameraParams,mirrorParams])
print cameraParams

print mirrorParams
