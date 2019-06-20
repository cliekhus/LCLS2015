# -*- coding: utf-8 -*-
"""
Created on Fri May  3 10:37:18 2019

@author: chelsea
"""

def loadData(FileNums, XAS, setting):
    
    import h5py
    import numpy as np
    import math
    
    
    #Initialize the necessary lists
    XOn = []
    LOn = []
    Var0 = []
    Diode2 = []
    
    Ipm2Sum = []
    DiodeIpmSlope = []
    
    TimeTool = []
    TTAmp = []
    TTFWHM = []
    
    ScanNum = []
    
    RowlandY = []
    Offset = []
    
    L3E = []
    CspadSum = []
    
    #Fill the lists with data from the h5 file
    for filenum in FileNums:
        print(filenum)
        if XAS:
            ScanName = h5py.File('D:\LCLS_Data\XAS\ldat_xppj6715_Run' + str(filenum) + '.h5')
        else:
            ScanName = h5py.File('D:\LCLS_Data\XES\ldat_xppj6715_Run' + str(filenum) + '.h5')
        
        xOn = list(map(bool, ScanName['/lightStatus/xray']))
        XOn = XOn + xOn
        LOn = LOn + list(map(bool, ScanName['/lightStatus/laser']))
        Var0 = Var0 + list(ScanName['/scan/var0'])
    
        diode = [x[2] for x in list(ScanName['/diodeU/channels'])]                  #Quad cell 2 from diode - this one has an output
        Diode2 = Diode2 + diode
        
        ipm2 = [float(x[1])+float(x[3]) for x in list(ScanName['/ipm2/channels'])]  #Intensity (and position) monitor #2.  Quad cells 1 and 3 had signal - use these
        Ipm2Sum = Ipm2Sum + ipm2
        
        slope = [y/x for y,x in zip(diode, ipm2)]
        DiodeIpmSlope = DiodeIpmSlope + slope
        
        timetool = [float(x) for x in list(ScanName['/ttCorr/tt'])]
        TimeTool = TimeTool + timetool
        
        timetoolamp = [float(x) for x in list(ScanName['/tt/XPP_TIMETOOL_AMPL'])]
        TTAmp = TTAmp + timetoolamp

        timetoolfwhm = [float(x) for x in list(ScanName['/tt/XPP_TIMETOOL_AMPL'])]
        TTFWHM = TTFWHM + timetoolfwhm
        
        ScanNum = ScanNum + [filenum for x in range(len(diode))]
        
        rowlandy = list(ScanName['/Rowland/ROI_proj_ythres'])
        
        RowlandY = RowlandY + [sum(x) for x in rowlandy]
        
        if setting == 1:
            Offset = Offset + [(np.mean(x[0:50])+np.mean(x[100:150]))/2*len(x) for x in rowlandy]
        elif setting == 2:
            Offset = Offset + [(sum(x[150:175]))/25*len(x) for x in rowlandy]
            
        L3E = L3E + list(ScanName['/ebeam/L3Energy'])
        
        cspad = list(ScanName['cspad/azav'])
        cspadsum = []
        for cs in cspad:
            cspadsum = cspadsum + [sum([x for x in cs if not math.isnan(x)])]
        CspadSum = CspadSum + cspadsum
    
    L3E = [float(x) for x in L3E]
    
    return XOn, LOn, Var0, Diode2, Ipm2Sum, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ScanNum, RowlandY, Offset, L3E, CspadSum

























