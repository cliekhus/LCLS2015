# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 13:49:49 2019

@author: chelsea
"""

class XESRawData:

    _defaults = "XOn", "LOn", "Angle", "Diode2", "Ipm2Sum", "TimeTool", "TTAmp", "TTFWHM", "ScanNum", "RowlandY", "Offset", "L3E", "CspadSum"
    _default_value = None
    
    def __init__(self, **kwargs):

        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)
        
    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)
        
class PeaksRawData:
    
    _defaults = "XOn", "LOn", "StageDelay", "Diode2", "Ipm2Sum", "TimeTool", "TTAmp", "TTFWHM", "ScanNum", "RowlandY", "Offset", "L3E", "CspadSum"
    _default_value = None
    
    def __init__(self, **kwargs):
        
        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        
    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)
        
class XASRawData:
    
    _defaults = "XOn", "LOn", "XEnergyRaw", "Diode2", "Ipm2Sum", "TimeTool", "TTAmp", "TTFWHM", "ScanNum", "RowlandY", "Offset", "L3E", "CspadSum"
    _default_value = None
    
    def __init__(self, **kwargs):

        self.__dict__.update(dict.fromkeys(self._defaults, self._default_value))
        self.__dict__.update(kwargs)
        
    def changeValue(self, **kwargs):
        self.__dict__.update(kwargs)