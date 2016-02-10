import HelpConfigLib

# Simulation steps
tstep=1/500. # Simulation time step (500Hz).
AOExpTime=0.#continuous simulation (no set number of iterations).

# Global Values used in config file
onaxis=[0.,0.] #on-axis direction in polar coords
offaxis=[10.,0.] # off-axis direction in polar coords

# Telescope conf
telDiam=10.4 # telescope diameter in m.
telSec=1.04 # Telescope central obscuration size in m.
npup=240. # number of phase pixels across telescope pupil.

pupil=createPupil(npup,npup/2,npup/2*telSec/telDiam) # telescope pupil function.  Used only in the config file.

# Atmosphere configuratin
r0=0.16 # r0 in metres
l0=10.  # outer scale in m.

#Create a dictionary of atmospheric layer objects.
layerset={ {"L0",height=0.,direction=0.,speed=7.5,strength=0.7,seed=11},
           {"L1",height=4000.,direction=330.,speed=12.5,strength=0.2,seed=12},
           {"L2",height=10000.,direction=135.,speed=15.,strength=0.1,seed=13)
         }


fluxlevel=100. # photons/subap/frame (used only in config file)
spotpsf=createAiryDisc(24,3.,0.5,0.5).astype("f")#Chosen so that images look similar to canary ones (spot patterns)

#Create an overview of the WFS objects.  In this case, there is only 1 with 20x20 subapertures, and 12x12 phase pixels per sub-aperture.
wfs_1=
wfsOverview=
{"a":guideStar.NGS('a',nsubx=20,theta=onaxis[0],phi=onaxis[1],phasesize=12,pupil=pupil,sourcelam=wfslam,sig=fluxlevel,reconList=["darc"],spotpsf=spotpsf)
})


#Create an overview of the science objects.  Note, in gtcsim.py, science object c isn't used.  However, it is included here as an example.  Each source specifies a different direction or wavelength.

science_a={"a",onaxis[0],onaxis[1],pupil,wfslam},
science_auncorr={"auncorr",onaxis[0],onaxis[1],pupil,wfslam,sciPath="a"}
science_b={'b',onaxis[0],onaxis[1],pupil,sciLam,phslam=wfslam}
science_buncorr={"buncorr":{'buncorr',onaxis[0],onaxis[1],pupil,sciLam,phslam=wfslam,sciPath="b"}
science_c={'c',offaxis[0],offaxis[1],pupil,sciLam,phslam=wfslam}


#And create the atmosphere geometry object, which encompasses layer heights and source directions.
atmosGeom=geom(layerDict,wfsOverview.values()+sciOverview.values(),npup,npup,telDiam,r0,l0)



#dmInfoList=[]
#The DM - which acts in directions a and b.
dm_1=dmInfo('dm',["a","b"],height=0.,nact=21,minarea=0.1,actuatorsFrom="darc",reconstructList="all",interpType="pspline",maxActDist=1.)
#The TT mirror - which acts in directions a and b.
dm_2=dmInfo('tt',["a","b"],height=0.,nact=3,minarea=0.1,zonalDM=0,actuatorsFrom="darc")
#The DM object.
#dmOverview(dmInfoList, atmosGeom)

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

