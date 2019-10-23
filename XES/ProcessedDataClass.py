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
        
    def makeProXES(self, xasRawData, MaxTime, MinTime, FPlots):
        from makeStaticXES import makeStaticXES
        
        XESOn_Norm, XESOff_Norm, Error_On, Error_Off = makeStaticXES(xasRawData, self, MaxTime, MinTime, FPlots)
        
        self.__dict__.update(XESOn_Norm = XESOn_Norm, XESOff_Norm = XESOff_Norm, Error_On = Error_On, Error_Off = Error_Off)
        
    def energyConversion(self, FPlots):
        from APSXESCalibration import makeConversion
        
        LCLSEnergy, slope, x0 = makeConversion(self, FPlots)
        
        self.__dict__.update(KaEnergy = LCLSEnergy)
        
    def makeStaticPlot(self):
        from makeStaticPlot import makeStaticPlot
        
        makeStaticPlot(self)

class PeaksProcessedData:
    
    _defaults = "Delay", "XASOn_Norm", "XASOff_Norm", "Num_On", "Num_Off", "TTSteps", "Error_On", "Error_Off"
    _default_value = None
    
    def __init__(self, **kwargs):

        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)
        
    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def makeProPeaks(self, xasRawData, DorH, FPlots):
        from makePeaks import makePeaks
        
        XASOn_Norm, XASOff_Norm, Num_On, Num_Off, Error_On, Error_Off = makePeaks(xasRawData, self, DorH, FPlots)
        
        self.__dict__.update(XASOn_Norm = XASOn_Norm, XASOff_Norm = XASOff_Norm, Num_On = Num_On, Num_Off = Num_Off, Error_On = Error_On, Error_Off = Error_Off)