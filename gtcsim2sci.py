#mpirun -np 1 -hostlist n1-c437  /usr/local/bin/mpipython $PWD/thisfile.py
#Python code created using the simulation setup GUI...
#Order of execution may not be quite optimal - you can always change by hand
#for large simulations - typically, the order of sends and gets may not be
#quite right.  Anyway, enjoy...
import numpy
import util.Ctrl
import base.mpiGet
import base.mpiSend
import base.shmGet
import base.shmSend
import Scientific.MPI
import science.infAtmos
import science.xinterp_dm
import science.wfscent
import science.darcsim
import science.science
import science.zdm
import predarc
import postdarc
import science.infScrn
ctrl=util.Ctrl.Ctrl(globals=globals())
print "Rank %d imported modules"%ctrl.rank
#Set up the science modules...
newMPIGetList=[]
newMPISendList=[]
newSHMGetList=[]
newSHMSendList=[]
infAtmosList=[]
dmList=[]
wfscentList=[]
DarcList=[]
scienceList=[]
PredarcList=[]
PostdarcList=[]
infScrnList=[]
#Add any personal code after this line and before the next, and it won't get overwritten
if ctrl.rank==0:
    PostdarcList.append(postdarc.Postdarc(None,ctrl.config,args={},idstr=None))
    infScrnList.append(science.infScrn.infScrn(None,ctrl.config,args={},idstr="L0"))
    infScrnList.append(science.infScrn.infScrn(None,ctrl.config,args={},idstr="L1"))
    infScrnList.append(science.infScrn.infScrn(None,ctrl.config,args={},idstr="L2"))
    infAtmosList.append(science.infAtmos.infAtmos({"L0":infScrnList[0],"L1":infScrnList[1],"L2":infScrnList[2],},ctrl.config,args={},idstr="a"))
    scienceList.append(science.science.science(infAtmosList[0],ctrl.config,args={},idstr="auncorr"))
    dmList.append(science.zdm.dm({"1":infAtmosList[0],"2":PostdarcList[0],},ctrl.config,args={},idstr="tta"))
    dmList.append(science.xinterp_dm.dm({"1":dmList[0],"2":PostdarcList[0],},ctrl.config,args={},idstr="dma"))
    wfscentList.append(science.wfscent.wfscent(dmList[1],ctrl.config,args={},idstr="a"))
    PredarcList.append(predarc.Predarc({"a":wfscentList[0],},ctrl.config,args={},idstr=None))
    DarcList.append(science.darcsim.Darc({"a":PredarcList[0],},ctrl.config,args={},idstr="darc"))
    scienceList.append(science.science.science(dmList[1],ctrl.config,args={},idstr="a"))
    scienceList.append(science.science.science(dmList[1],ctrl.config,args={},idstr="b"))
    scienceList.append(science.science.science(infAtmosList[0],ctrl.config,args={},idstr="buncorr"))
    infAtmosList.append(science.infAtmos.infAtmos({"L0":infScrnList[0],"L1":infScrnList[1],"L2":infScrnList[2],},ctrl.config,args={},idstr="c"))
    dmList.append(science.zdm.dm({"1":infAtmosList[1],"2":PostdarcList[0],},ctrl.config,args={},idstr="ttc"))
    dmList.append(science.xinterp_dm.dm({"1":dmList[2],"2":PostdarcList[0],},ctrl.config,args={},idstr="dmc"))
    scienceList.append(science.science.science(dmList[3],ctrl.config,args={},idstr="c"))
    PostdarcList[0].newParent(DarcList[0],None)
    execOrder=[PostdarcList[0],infScrnList[0],infScrnList[1],infScrnList[2],infAtmosList[0],scienceList[0],dmList[0],dmList[1],wfscentList[0],PredarcList[0],DarcList[0],scienceList[1],scienceList[2],scienceList[3],infAtmosList[1],dmList[2],dmList[3],scienceList[4],]
    ctrl.mainloop(execOrder)
print "Simulation finished..."
#Add any personal code after this, and it will not get overwritten
Scientific.MPI.world.abort(0)

