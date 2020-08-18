# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 17:19:10 2019

@author: chelsea
"""

class XESProcessedData:
    
    _defaults = "TTDelay", "KaEnergy", "UniAngle", "XESOn_Norm", "XESOff_Norm", "Error_On", "Error_Off", "RowWOffset"
    _default_value = None
    
    def __init__(self, **kwargs):

        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)
    
    def makeLaserXES(self, xesRawData, MaxTime, MinTime, FPlots):
        from makeStatic import makeLaserXES
        
        XESOn_Norm, XESOff_Norm, Error_On, Error_Off, UniAngle = makeLaserXES(xesRawData, self, MaxTime, MinTime, FPlots)
        
        self.__dict__.update(XESOn_Norm = XESOn_Norm, XESOff_Norm = XESOff_Norm, Error_On = Error_On, Error_Off = Error_Off, UniAngle = UniAngle)
        
    
    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def makeProXES(self, xesRawData, MaxTime, MinTime, FPlots):
        from makeStatic import makeStaticXES
        
        XESOn_Norm, XESOff_Norm, Error_On, Error_Off, UniAngle = makeStaticXES(xesRawData, self, MaxTime, MinTime, FPlots)
        
        self.__dict__.update(XESOn_Norm = XESOn_Norm, XESOff_Norm = XESOff_Norm, Error_On = Error_On, Error_Off = Error_Off, UniAngle = UniAngle)
        
    def energyConversion(self, FPlots):
        from APSXESCalibration import makeConversion
        import numpy as np
        
        LCLSEnergy, slope, x0 = makeConversion(self, FPlots)
                
        self.__dict__.update(KaEnergy = np.array(LCLSEnergy)*1000)
        
    def getEnergy(self):
        from APSXESCalibration import Angle2Energy
        import numpy as np
        
        LCLSEnergy =  Angle2Energy(self.UniAngle)
        
        self.__dict__.update(KaEnergy = np.array(LCLSEnergy)*1000)
        
    def makeStaticPlot(self):
        from makeStaticPlot import makeStaticPlot
        
        makeStaticPlot(self)
        
    def add(self, otherProXES):
        import numpy as np
        
        if np.all(self.UniAngle != otherProXES.UniAngle):
            print('stop, there was an angle problem, ProcessedDataClass.py line 53')
            
        XESOn_Norm = np.vstack((self.XESOn_Norm,otherProXES.XESOn_Norm))
        XESOff_Norm = np.vstack((self.XESOff_Norm,otherProXES.XESOff_Norm))
        Error_On = np.vstack((self.Error_On,otherProXES.Error_On))
        Error_Off = np.vstack((self.Error_Off,otherProXES.Error_Off))
        UniAngle = np.vstack((self.UniAngle,otherProXES.UniAngle))
        KaEnergy = np.vstack((self.KaEnergy,otherProXES.KaEnergy))

        self.__dict__.update(XESOn_Norm = XESOn_Norm, XESOff_Norm = XESOff_Norm, Error_On = Error_On, Error_Off = Error_Off, UniAngle = UniAngle, KaEnergy = KaEnergy)
        
    def boot_ave(self):
        import numpy as np
        
        self.__dict__.update(XESOn_Norm = np.mean(self.XESOn_Norm,0), XESOff_Norm = np.mean(self.XESOff_Norm,0), \
                             Error_On = np.std(self.XESOn_Norm,0), Error_Off = np.std(self.XESOff_Norm,0), \
                             UniAngle = np.mean(self.UniAngle,0), KaEnergy = np.mean(self.KaEnergy,0))



class PeaksProcessedData:
    
    _defaults = "Delay", "XESOn_Norm", "XESOff_Norm", "TTSteps", "Error_On", "Error_Off", "RowWOffset", "TimeSteps", "XESDiff", "EnergyLabel", "XESDiffE", "FT", "FTE", "TCenters", "Freq"
    _default_value = None
    
    def __init__(self, **kwargs):

        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)
        
    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def makeProPeaks(self, peaksRawData, NumTTSteps, MinTime, MaxTime, ploton):
        from makeXES import makeXES
        
        XESOn_Norm, XESOff_Norm, Error_On, Error_Off, TimeSteps = makeXES(self, peaksRawData, NumTTSteps, MinTime, MaxTime, ploton)
        
        self.__dict__.update(XESOn_Norm = XESOn_Norm, XESOff_Norm = XESOff_Norm, Error_On = Error_On, Error_Off = Error_Off, TimeSteps = TimeSteps, XESDiff = (XESOn_Norm-XESOff_Norm)/XESOff_Norm)
        
    def makeBootPeaks(self, peaksRawData, NumTTSteps, MinTime, MaxTime, TF, ploton):
        from makeXES import makeBootXES
        
        XESOn_Norm, XESOff_Norm, Error_On, Error_Off, TimeSteps = makeBootXES(self, peaksRawData, NumTTSteps, MinTime, MaxTime, TF, ploton)
        
        self.__dict__.update(XESOn_Norm = XESOn_Norm, XESOff_Norm = XESOff_Norm, Error_On = Error_On, Error_Off = Error_Off, TimeSteps = TimeSteps, XESDiff = (XESOn_Norm-XESOff_Norm)/XESOff_Norm)
        
        
        
        
        
        
        
        