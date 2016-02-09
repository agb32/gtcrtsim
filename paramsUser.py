from util.atmos import layer
#simulation stuff
tstep=1/500. # Simulation time step (500Hz).

#telescope stuff
telDiam=10.4 # telescope diameter in m.
telSec=1.04 # Telescope central obscuration size in m.

#atmosphere stuff
nlayers=3 # number of atmospheric layers (used only in the config file)
r0=0.16 # r0 in metres
l0=10.  # outer scale in m.
#Create a dictionary of atmospheric layer objects.
layerDict={
    "L0":layer(height=0.,direction=0.,speed=7.5,strength=0.7),
    "L1":layer(height=4000.,direction=330.,speed=12.5,strength=0.2),
    "L2":layer(height=10000.,direction=135.,speed=15.,strength=0.1),
}

#target definitions
wfsWavelength=700. # wavelength of WFS in nm (used only in the config file)
sciWavelength=1650. # wavelength of a science source (used only in config file)

#wfs stuff
nsubx=20 # 20x20 subaps
readnoise=0.1 # electrons per pixel rms
