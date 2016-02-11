#import stuff
import base.readConfig
from util.tel import Pupil
from util.sci import sciInfo,sciOverview
from util.guideStar import NGS,wfsOverview
from util.centroid import createAiryDisc
from util.atmos import layer,geom
from util.dm import dmInfo,dmOverview
base.readConfig.init(globals())
#THIS parameter file must be called along with paramsUser.py.  i.e.
#python gtcsim.py paramsUser.py paramsMain.py


#First get stuff from paramsUser:
telDiam=this.globals.telDiam
telSec=this.globals.telSec
r0=this.globals.r0
l0=this.globals.l0
layerDict=this.globals.layerDict
wfsWavelength=this.globals.wfsWavelength
sciWavelength=this.globals.sciWavelength
nsubx=this.globals.nsubx
readnoise=this.globals.readnoise

#simulation stuff
AOExpTime=0.#continuous simulation (no set number of iterations).

#telescope stuff
npup=240 # number of phase pixels across telescope pupil.
pupil=Pupil(npup,npup/2,npup/2*telSec/telDiam) # telescope pupil function.  Used only in the config file.

#atmosphere stuff
layerList={"allLayers":layerDict.keys()} # specify which iscrn object makes which layers.  In this case, we only have one, which makes all layers.

#target definitions
onaxis=[0.,0.] #on-axis direction in polar coords
offaxis=[10.,0.] # off-axis direction in polar coords. This isn't used in gtcsim.py - if you want an off-axis source, consider using gtcsim2sci.py.
fluxlevel=100. # photons/subap/frame (used only in config file)
spotpsf=createAiryDisc(24,3.,0.5,0.5).astype("f")#Chosen so that images look similar to canary ones (spot patterns)

#Create an overview of the science objects.  Note, in gtcsim.py, science object c isn't used.  However, it is included here as an example.  Each source specifies a different direction or wavelength.
sciOverview=sciOverview({
    "a":sciInfo("a",onaxis[0],onaxis[1],pupil,wfsWavelength),
    "auncorr":sciInfo("auncorr",onaxis[0],onaxis[1],pupil,wfsWavelength,sciPath="a"),
    "b":sciInfo('b',onaxis[0],onaxis[1],pupil,sciWavelength,phslam=wfsWavelength),
    "buncorr":sciInfo('buncorr',onaxis[0],onaxis[1],pupil,sciWavelength,phslam=wfsWavelength,sciPath="b"),
    "c":sciInfo('c',offaxis[0],offaxis[1],pupil,sciWavelength,phslam=wfsWavelength),
})

#Create an overview of the WFS objects.  In this case, there is only 1 with 20x20 subapertures, and 12x12 phase pixels per sub-aperture.
wfsOverview=wfsOverview({
    "a":NGS('a',nsubx=nsubx,theta=onaxis[0],phi=onaxis[1],phasesize=npup/nsubx,pupil=pupil,sourcelam=wfsWavelength,sig=fluxlevel,reconList=["darc"],spotpsf=spotpsf)
})

#And create the atmosphere geometry object, which encompasses layer heights and source directions.
atmosGeom=geom(layerDict,wfsOverview.values()+sciOverview.values(),npup,npup,telDiam,r0,l0)


dmInfoList=[]
#The DM - which acts in directions a and b.
dmInfoList.append(dmInfo('dm',["a","b"],height=0.,nact=nsubx+1,minarea=0.1,actuatorsFrom="darc",reconstructList="all",interpType="pspline",maxActDist=1.))
#The TT mirror - which acts in directions a and b.
dmInfoList.append(dmInfo('tt',["a","b"],height=0.,nact=3,minarea=0.1,zonalDM=0,actuatorsFrom="darc"))
#The DM object.
dmObj=dmOverview(dmInfoList, atmosGeom)

#Values specific to the wfscent module
this.wfscent=new()
this.wfscent.imageOnly=2 # Only produce the image, since darc will do slope calculation.

#values specific to predarc module:
this.predarc=new()
this.predarc.readnoise=[readnoise]
this.predarc.background=[0.]
this.predarc.npxlxDarc=[240]

#values specific to the postdarc module:
this.darcsim=new()
this.darcsim.useExistingDarc=1#Darc will be started elsewhere
this.darcsim.npxlx=240**2
this.darcsim.npxly=1
this.darcsim.nactsDarc=375

