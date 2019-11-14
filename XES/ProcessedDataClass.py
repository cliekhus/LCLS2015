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
        
    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def makeProXES(self, xesRawData, MaxTime, MinTime, FPlots):
        from makeStatic import makeStaticXES
        
        XESOn_Norm, XESOff_Norm, Error_On, Error_Off = makeStaticXES(xesRawData, self, MaxTime, MinTime, FPlots)
        
        self.__dict__.update(XESOn_Norm = XESOn_Norm, XESOff_Norm = XESOff_Norm, Error_On = Error_On, Error_Off = Error_Off)
        
    def energyConversion(self, FPlots):
        from APSXESCalibration import makeConversion
        import numpy as np
        
        LCLSEnergy, slope, x0 = makeConversion(self, FPlots)
                
        self.__dict__.update(KaEnergy = np.array(LCLSEnergy)*1000)
        
    def makeStaticPlot(self):
        from makeStaticPlot import makeStaticPlot
        
        makeStaticPlot(self)
        
        


class PeaksProcessedData:
    
    _defaults = "Delay", "XESOn_Norm", "XESOff_Norm", "TTSteps", "Error_On", "Error_Off", "RowWOffset", "TimeSteps", "XESDiff", "EnergyLabel"
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
        
        
        
        
        
        
        
        