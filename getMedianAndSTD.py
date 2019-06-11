# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 17:42:15 2019

@author: chelsea
"""

def getMedianAndSTD(Value, ScanNum):
    
    import numpy as np
    import statistics as stat
    
    UniScanNum = np.unique(ScanNum)
    
    Median = []
    STD = []
    
    for a in UniScanNum:
        value = [x for x,y in zip(Value, ScanNum) if y == a]
        
        median = stat.median(value)
        Median = Median + [median for x in range(len(value))]
        
        std = stat.stdev(value)
        STD = STD + [std for x in range(len(value))]
        
    return Median, STD