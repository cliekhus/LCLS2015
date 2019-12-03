# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 14:34:21 2019

@author: chelsea
"""

def MakeRawBoot(peaksRawData):
    
    import random
    import numpy as np
    import RawDataClass as RDC
    
    
    
    nn = len(peaksRawData.XOn)
    
    XOn = np.empty(nn, dtype=bool)
    LOn = np.empty(nn, dtype=bool)
    StageDelay = np.empty(nn)
    Diode2 = np.empty(nn)
    Ipm2Sum = np.empty(nn)
    TimeTool = np.empty(nn)
    TTAmp = np.empty(nn)
    TTFWHM = np.empty(nn)
    ScanNum = np.empty(nn)
    RowlandY = np.empty(nn)
    Offset = np.empty(nn)
    L3E = np.empty(nn)
    CspadSum = np.empty(nn)
    TTFP = np.empty(nn)
    
    
    for ii in range(nn):
        
        index = random.randint(0,nn-1)
        
        XOn[ii] = peaksRawData.XOn[index]
        LOn[ii] = peaksRawData.LOn[index]
        StageDelay[ii] = peaksRawData.StageDelay[index]
        Diode2[ii] = peaksRawData.Diode2[index]
        Ipm2Sum[ii] = peaksRawData.Ipm2Sum[index]
        TimeTool[ii] = peaksRawData.TimeTool[index]
        TTAmp[ii] = peaksRawData.TTAmp[index]
        TTFWHM[ii] = peaksRawData.TTFWHM[index]
        ScanNum[ii] = peaksRawData.ScanNum[index]
        RowlandY[ii] = peaksRawData.RowlandY[index]
        Offset[ii] = peaksRawData.Offset[index]
        L3E[ii] = peaksRawData.L3E[index]
        CspadSum[ii] = peaksRawData.CspadSum[index]
        TTFP[ii] = peaksRawData.TTFP[index]


    xesRawData = RDC.PeaksRawData()

    xesRawData.changeValue(XOn = XOn, LOn = LOn, StageDelay = StageDelay, Diode2 = Diode2, Ipm2Sum = Ipm2Sum, TimeTool = TimeTool, \
       TTAmp = TTAmp, TTFWHM = TTFWHM, ScanNum = ScanNum, RowlandY = RowlandY, Offset = Offset, L3E = L3E, CspadSum = CspadSum, TTFP = TTFP)
    
    
    return xesRawData
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
