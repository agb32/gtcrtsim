import base.readConfig
import util.tel
import util.sci
import util.guideStar
import util.centroid
import util.atmos
import util.dm
base.readConfig.init(globals())

tstep=1/500. # Simulation time step (500Hz).
AOExpTime=0.#continuous simulation (no set number of iterations).
telDiam=10.4 # telescope diameter in m.
telSec=1.04 # Telescope central obscuration size in m.
npup=240. # number of phase pixels across telescope pupil.
nlayers=3 # number of atmospheric layers (used only in the config file)
r0=0.16 # r0 in metres
l0=10.  # outer scale in m.
wfslam=700. # wavelength of WFS in nm (used only in the config file)
sciLam=1650. # wavelength of a science source (used only in config file)
layerList={"allLayers":["L0","L1","L2"]} # specify which iscrn object makes which layers.  In this case, we only have one, which makes all layers.
pupil=util.tel.Pupil(npup,npup/2,npup/2*telSec/telDiam) # telescope pupil function.  Used only in the config file.
onaxis=[0.,0.] #on-axis direction in polar coords
offaxis=[10.,0.] # off-axis direction in polar coords
fluxlevel=100. # photons/subap/frame (used only in config file)
spotpsf=util.centroid.createAiryDisc(24,3.,0.5,0.5).astype("f")#Chosen so that images look similar to canary ones (spot patterns)

#Create an overview of the science objects.  Note, in gtcsim.py, science object c isn't used.  However, it is included here as an example.  Each source specifies a different direction or wavelength.
sciOverview=util.sci.sciOverview({
    "a":util.sci.sciInfo("a",onaxis[0],onaxis[1],pupil,wfslam),
    "auncorr":util.sci.sciInfo("auncorr",onaxis[0],onaxis[1],pupil,wfslam,sciPath="a"),
    "b":util.sci.sciInfo('b',onaxis[0],onaxis[1],pupil,sciLam,phslam=wfslam),
    "buncorr":util.sci.sciInfo('buncorr',onaxis[0],onaxis[1],pupil,sciLam,phslam=wfslam,sciPath="b"),
    "c":util.sci.sciInfo('c',offaxis[0],offaxis[1],pupil,sciLam,phslam=wfslam),
})

#Create an overview of the WFS objects.  In this case, there is only 1 with 20x20 subapertures, and 12x12 phase pixels per sub-aperture.
wfsOverview=util.guideStar.wfsOverview({
    "a":util.guideStar.NGS('a',nsubx=20,theta=onaxis[0],phi=onaxis[1],phasesize=12,pupil=pupil,sourcelam=wfslam,sig=fluxlevel,reconList=["darc"],spotpsf=spotpsf)
})

#Create a dictionary of atmospheric layer objects.
layerDict={
    "L0":util.atmos.layer(height=0.,direction=0.,speed=7.5,strength=0.7,seed=11),
    "L1":util.atmos.layer(height=4000.,direction=330.,speed=12.5,strength=0.2,seed=12),
    "L2":util.atmos.layer(height=10000.,direction=135.,speed=15.,strength=0.1,seed=13),
}
#And create the atmosphere geometry object, which encompasses layer heights and source directions.
atmosGeom=util.atmos.geom(layerDict,wfsOverview.values()+sciOverview.values(),npup,npup,telDiam,r0,l0)


dmInfoList=[]
#The DM - which acts in directions a and b.
dmInfoList.append(util.dm.dmInfo('dm',["a","b"],height=0.,nact=21,minarea=0.1,actuatorsFrom="darc",reconstructList="all",interpType="pspline",maxActDist=1.))
#The TT mirror - which acts in directions a and b.
dmInfoList.append(util.dm.dmInfo('tt',["a","b"],height=0.,nact=3,minarea=0.1,zonalDM=0,actuatorsFrom="darc"))
#The DM object.
dmObj=util.dm.dmOverview(dmInfoList, atmosGeom)

#Values specific to the wfscent module
this.wfscent=new()
this.wfscent.imageOnly=2 # Only produce the image, since darc will do slope calculation.

#values specific to predarc module:
this.predarc=new()
this.predarc.readnoise=[0.1]
this.predarc.background=[0.]
this.predarc.npxlxDarc=[240]

#values specific to the postdarc module:
this.darcsim=new()
this.darcsim.useExistingDarc=1#Darc will be started elsewhere
this.darcsim.npxlx=240**2
this.darcsim.npxly=1
this.darcsim.nactsDarc=375

