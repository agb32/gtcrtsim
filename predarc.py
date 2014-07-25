import numpy
import base.aobase
class Predarc(base.aobase.aobase):
    def __init__(self,parent,config,args={},forGUISetup=0,debug=None,idstr=None):
        if type(parent)!=type({}):
            parent={"1":parent}
        base.aobase.aobase.__init__(self,parent,config,args,forGUISetup=forGUISetup,debug=debug,idstr=idstr)
        """PArents will be a-d for NGS, e-h for LGS, j for LOFS.  Need to rotate these, then combine (interleave, add pixels, etc).
        """
        self.readnoise=self.config.getVal("readnoise")#a list, one for each WFS.
        self.bg=self.config.getVal("background")#a list, either of floats, or of images.
        self.fliprot=self.config.getVal("fliprotateWFS",raiseerror=0)#angle in degrees which to rotate wfs by.  A list. ngs then lgs then lofs.
        self.npxlxDarc=self.config.getVal("npxlxDarc")#image size in darc.  For each camera.
        self.keyList=self.config.getVal("predarcKeyList",default=["a"])
        self.outputData=numpy.zeros((numpy.array(self.npxlxDarc)**2).sum(),numpy.float32)

    def newParent(self,parent,idstr=None):
        raise Exception("Please don't call newParent for predarc module")
        
    def generateNext(self,ms=None):
        if self.generate==1:
            if self.newDataWaiting:
                self.dataValid=1
                for key in self.parent.keys():
                    if self.parent[key].dataValid==0:
                        self.dataValid=0
            if self.dataValid:
                self.getInputData()
        else:
            self.dataValid=0
            

    def getInputData(self):
        pos=0
        for i in range(len(self.keyList)):#0-3=ngs, 4-7=lgs, 8=lofs.
            key=self.keyList[i]
            img=self.parent[key].outputData
            #first, rotate (wrt the truth).
            if self.fliprot!=None and self.fliprot[i]!=0:
                if self.fliprot[i]==1:#symmetry about vertical axis
                    img[:]=img.copy()[:,::-1]
                elif self.fliprot[i]==4:#rotation of 180 degrees and vertical flip.  Or, rotation of 90 and horiz flip.
                    img=numpy.rot90(img,1)[:,::-1]
                elif self.fliprot[i]==7:#transpose + rotation of 180.  Or, rotation of 90 and vertical flip.
                    img=numpy.rot90(img,1)[::-1]
                elif self.fliprot[i]==9:#symmetry about horiz axis
                    img[:]=img.copy()[::-1]
                elif self.fliprot[i]==3:#rotation of 180 degrees
                    img[:]=numpy.rot90(img,2)
                else:
                    raise Exception("Symmetry code %d not yet implemented"%self.fliprot[i])
            #then add a background and readnoise in the extra pixels
            tmp=self.outputData
            tmp.shape=self.npxlxDarc[i],self.npxlxDarc[i]
            tmp[:]=numpy.random.normal(scale=self.readnoise[i],size=(self.npxlxDarc[i],self.npxlxDarc[i]))
            #then insert the image into the extra pixels.
            f=(self.npxlxDarc[i]-img.shape[0])/2
            if f==0:
                tmp+=img
            else:
                tmp[f:-f,f:-f]+=img
            #and add the background (single value or array).
            tmp+=self.bg[i]
            #And now paste the image into the pixel array (outputData)

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

