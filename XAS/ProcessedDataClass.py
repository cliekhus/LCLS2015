# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 17:19:10 2019

@author: chelsea
"""

class XASProcessedData:
    
    _defaults = "TTDelay", "XEnergy", "UniXEnergy", "XASOn_Norm", "XASOff_Norm", "EnergyPlot", "Num_On", "Num_Off", "TTSteps"
    _default_value = None
    
    def __init__(self, **kwargs):

        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)
        
    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)
        
    def makeProXAS(self, xasRawData, FPlots):
        from makeXAS import makeXAS
        
        XASOn_Norm, XASOff_Norm, EnergyPlot, Num_On, Num_Off = makeXAS(xasRawData, self, FPlots)
        
        self.__dict__.update(XASOn_Norm = XASOn_Norm, XASOff_Norm = XASOff_Norm, EnergyPlot = EnergyPlot, Num_On = Num_On, Num_Off = Num_Off)
        