import numpy
import base.aobase
import util.tel
class Postdarc(base.aobase.aobase):
    def __init__(self,parent,config,args={},forGUISetup=0,debug=None,idstr=None):
        base.aobase.aobase.__init__(self,parent,config,args,forGUISetup=forGUISetup,debug=debug,idstr=idstr)
        """Expect 375 actuators from darc, which we have to convert to 376 for the simulation, because zdm expects piston..."""
        self.outputData=numpy.zeros((376,),numpy.float32)
        self.firsttime=1
        if forGUISetup:
            self.outputData=self.outputData.shape,self.outputData.dtype

    def generateNext(self,ms=None):
        self.dataValid=1
        if self.generate==1:
            if self.newDataWaiting:
                self.dataValid=1
                if self.parent.dataValid==0:
                    self.dataValid=self.firsttime
                    self.firsttime=0
            if self.dataValid:
                self.getInputData()
        else:
            self.dataValid=0

    def getInputData(self):
        p=self.parent
        data=p.outputData
        self.outputData[:373]=data[:373]-32768
        self.outputData[374:]=data[373:]-32768
        


    def plottable(self,objname="$OBJ"):
        """Return a XML string which contains the commands to be sent
        over a socket to obtain certain data for plotting.  The $OBJ symbol
        will be replaced by the instance name of the object - e.g.
        if scrn=mkscrns.Mkscrns(...) then $OBJ would be replaced by scrn."""
        if self.idstr==None:
            id=""
        else:
            id=" (%s)"%self.idstr
        txt=""
        txt+="""<plot title="predarc output%s" cmd="data=%s.outputData" ret="data" type="pylab" when="rpt" palette="gray"/>\n"""%(id,objname)
        return txt

    def getParams(self):
        """parameters required for this module, in the form of {"paramName":defaultValue,...}
        These params can then be placed in the config file... if not set by the
        user, the param should still be in config file as default value for
        future reference purposes.
        """
        #This is a working example.  Please feel free to change the parameters
        #required. (if you do, also change the config.getParam() calls too).
        paramList=[]
        paramList.append(base.dataType.dataType(description="telDiam",typ="f",val="42.",comment="TODO: Telescope diameter (m)"))
        return paramList

