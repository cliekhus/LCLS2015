# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:20:36 2019

@author: chelsea
"""

def makeFakeData(totallength):
    
    import numpy as np
    from itertools import compress
    import math
    import statistics as stat
    from pylab import exp
    
    #Initialize the necessary lists
    XOn = []
    LOn = []
    XEnergyRaw = []
    Diode2 = []
    Ipm2Sum = []
    
    DiodeIpmSlope = []
    DISMedian = []
    DISSTD = []
    
    TimeTool = []
    TTAmp = []
    TTFWHM = []
    
    ScanNum = []
    
    RowlandY = []
    rowlandblank = np.zeros(184,)
    rowlandblank[36] = 2
    rowlandblank[71] = 1
    
    for ii in range(totallength):
        
        XOn = XOn + [ii < totallength/2]
        LOn = LOn + [ii < (totallength/4) or (ii >= (totallength/2) and ii < (3*totallength/4))]
        XEnergyRaw = XEnergyRaw + [7108 + ii%16]
    
        Diode2 = Diode2 + [ii%32/1000+0.01]
        
        ipm2Sum = ii%32/100
        #if ii%32 == 10 or ii%32 == 20:
        #    ipm2Sum = ipm2Sum + 0.1
        Ipm2Sum = Ipm2Sum + [ipm2Sum+0.1]
        
        TimeTool = TimeTool + [ii%64/100]
        
        TTAmp = TTAmp + [ii%128/100]
        
        TTFWHM = TTFWHM + [ii%256/100]
        
        RowlandY = RowlandY + [rowlandblank*exp(-(ii%32/100-16/100)**2)]
        
    statmedian = stat.median(compress(Ipm2Sum, XOn))
    Ipm2Median = [float(statmedian) for x in range(len(Ipm2Sum))]
    statstdev = stat.stdev(compress(Ipm2Sum, XOn))
    Ipm2STD = [float(statstdev) for x in range(len(Ipm2Sum))]
    
    DiodeIpmSlope = [y/x for y,x in zip(Diode2, Ipm2Sum)]
    statmedian = stat.median([x for x in DiodeIpmSlope if not math.isnan(x)])
    DISMedian = [float(statmedian) for x in range(len(Ipm2Sum))]
    statstdev = stat.stdev([i-statmedian*d for d,i in zip(Diode2, Ipm2Sum)])
    DISSTD = DISSTD + [float(statstdev) for x in range(len(Ipm2Sum))]
    
    statmedian = stat.median(compress(TimeTool, [a and b for a,b in zip(LOn, XOn)]))
    TTMedian = [float(statmedian) for x in range(len(TimeTool))]
    statstdev = stat.stdev(compress(TimeTool, [a and b for a,b in zip(LOn, XOn)]))
    TTSTD = [float(statstdev) for x in range(len(TimeTool))]
    
    statmedian = stat.median(compress(TTAmp, [a and b for a,b in zip(LOn, XOn)]))
    TTAmpMedian = [float(statmedian) for x in range(len(TTAmp))]
    statstdev = stat.stdev(compress(TTAmp, [a and b for a,b in zip(LOn, XOn)]))
    TTAmpSTD = [float(statstdev) for x in range(len(TTAmp))]
    
    statmedian = stat.median(compress(TTFWHM, [a and b for a,b in zip(LOn, XOn)]))
    TTFWHMMedian = [float(statmedian) for x in range(len(TTFWHM))]
    statstdev = stat.stdev(compress(TTFWHM, [a and b for a,b in zip(LOn, XOn)]))
    TTFWHMSTD = [float(statstdev) for x in range(len(TTFWHM))]
            
    return XOn, LOn, XEnergyRaw, Diode2, Ipm2Sum, Ipm2Median, Ipm2STD, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, ScanNum, RowlandY