# -*- coding: utf-8 -*-
"""
Created on Fri May  3 10:37:18 2019

@author: chelsea
"""

def loadData(FileNums):
    
    import h5py
    import numpy as np
    from itertools import compress
    import math
    import statistics as stat
    
    
    #Initialize the necessary lists
    XOn = []
    LOn = []
    XEnergyRaw = []
    Diode2 = []
    
    Ipm2Sum = []
    Ipm2Median = []
    Ipm2STD = []
    DiodeIpmSlope = []
    DISMedian = []
    DISSTD = []
    
    TimeTool = []
    TTMedian = []
    TTSTD = []
    TTAmp = []
    TTAmpMedian = []
    TTAmpSTD = []
    TTFWHM = []
    TTFWHMMedian = []
    TTFWHMSTD = []
    
    ScanNum = []
    
    RowlandY = []
    
    
    #Fill the lists with data from the h5 file
    for filenum in FileNums:
        
        ScanName = h5py.File('Data\ldat_xppj6715_Run' + str(filenum) + '.h5')
        
        xOn = list(map(bool, ScanName['/lightStatus/xray']))
        XOn = XOn + xOn
        LOn = LOn + list(map(bool, ScanName['/lightStatus/laser']))
        XEnergyRaw = XEnergyRaw + list(ScanName['/scan/var0'])
    
        diode = [x[2] for x in list(ScanName['/diodeU/channels'])]                  #Quad cell 2 from diode - this one has an output
        Diode2 = Diode2 + diode
        
        ipm2 = [float(x[1])+float(x[3]) for x in list(ScanName['/ipm2/channels'])]  #Intensity (and position) monitor #2.  Quad cells 1 and 3 had signal - use these
        Ipm2Sum = Ipm2Sum + ipm2
        statmedian = stat.median(compress(ipm2, xOn))
        Ipm2Median = Ipm2Median + [float(statmedian) for x in range(len(ipm2))]
        statstdev = stat.stdev(compress(ipm2, xOn))
        Ipm2STD = Ipm2STD + [float(statstdev) for x in range(len(ipm2))]
        
        slope = [y/x for y,x in zip(diode, ipm2)]
        DiodeIpmSlope = DiodeIpmSlope + slope
        statmedian = stat.median([x for x in slope if not math.isnan(x)])
        DISMedian = [float(statmedian) for x in range(len(ipm2))]
        statstdev = stat.stdev([i-statmedian*d for d,i in zip(diode, ipm2)])
        DISSTD = DISSTD + [float(statstdev) for x in range(len(ipm2))]
        
        timetool = [float(x) for x in list(ScanName['/ttCorr/tt'])]
        TimeTool = TimeTool + timetool
        
        statmedian = stat.median(compress(timetool, [a and b for a,b in zip(LOn, XOn)]))
        TTMedian = TTMedian + [float(statmedian) for x in range(len(timetool))]
        statstdev = stat.stdev(compress(timetool, [a and b for a,b in zip(LOn, XOn)]))
        TTSTD = TTSTD + [float(statstdev) for x in range(len(timetool))]
        
        timetoolamp = [float(x) for x in list(ScanName['/tt/XPP_TIMETOOL_AMPL'])]
        TTAmp = TTAmp + timetoolamp
        
        statmedian = stat.median(compress(timetoolamp, [a and b for a,b in zip(LOn, XOn)]))
        TTAmpMedian = TTAmpMedian + [float(statmedian) for x in range(len(timetoolamp))]
        statstdev = stat.stdev(compress(timetoolamp, [a and b for a,b in zip(LOn, XOn)]))
        TTAmpSTD = TTAmpSTD + [float(statstdev) for x in range(len(timetoolamp))]
        
        timetoolfwhm = [float(x) for x in list(ScanName['/tt/XPP_TIMETOOL_AMPL'])]
        TTFWHM = TTFWHM + timetoolfwhm
        
        statmedian = stat.median(compress(timetoolfwhm, [a and b for a,b in zip(LOn, XOn)]))
        TTFWHMMedian = TTFWHMMedian + [float(statmedian) for x in range(len(timetoolfwhm))]
        statstdev = stat.stdev(compress(timetoolfwhm, [a and b for a,b in zip(LOn, XOn)]))
        TTFWHMSTD = TTFWHMSTD + [float(statstdev) for x in range(len(timetoolfwhm))]
        
        ScanNum = ScanNum + [filenum for x in range(len(diode))]
        
        RowlandY = RowlandY + list(ScanName['/Rowland/ROI_proj_ythres'])
        
    return XOn, LOn, XEnergyRaw, Diode2, Ipm2Sum, Ipm2Median, Ipm2STD, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, ScanNum, RowlandY