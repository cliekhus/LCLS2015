# -*- coding: utf-8 -*-
"""
Created on Fri May  3 10:37:18 2019

@author: chelsea
"""

def loadData(FileNums, XAS, setting):
    
    import h5py
    import numpy as np
    import math
    import RawDataClass as RDC
    
    if XAS:
        xasRawData = RDC.XASRawData()
    
    #Initialize the necessary lists
    XOn = np.empty(0)
    LOn = np.empty(0)
    Var0 = np.empty(0)
    Diode2 = np.empty(0)
    
    Ipm2Sum = np.empty(0)
    
    TimeTool = np.empty(0)
    TTAmp = np.empty(0)
    TTFWHM = np.empty(0)
    
    ScanNum = []
    
    RowlandY = np.empty(0)
    Offset = np.empty(0)
    
    L3E = np.empty(0)
    CspadSum = np.empty(0)
    
    #Fill the lists with data from the h5 file
    for filenum in FileNums:
        print(filenum)
        if XAS:
            ScanName = h5py.File('D:\LCLS_Data\XAS\ldat_xppj6715_Run' + str(filenum) + '.h5')
        else:
            ScanName = h5py.File('D:\LCLS_Data\XES\ldat_xppj6715_Run' + str(filenum) + '.h5')
        
        xOn = np.array(list(map(bool, ScanName['/lightStatus/xray'])))
        XOn = np.append(XOn, xOn)
        LOn = np.append(LOn, np.array(list(map(bool, ScanName['/lightStatus/laser']))))
        Var0 = np.append(Var0, np.array(ScanName['/scan/var0']))
    
        diode = [x[2] for x in list(ScanName['/diodeU/channels'])]                  #Quad cell 2 from diode - this one has an output
        Diode2 = np.append(Diode2, np.array(diode))
        
        ipm2 = [float(x[1])+float(x[3]) for x in list(ScanName['/ipm2/channels'])]  #Intensity (and position) monitor #2.  Quad cells 1 and 3 had signal - use these
        Ipm2Sum = np.append(Ipm2Sum, np.array(ipm2))
        
        timetool = [float(x) for x in list(ScanName['/ttCorr/tt'])]
        TimeTool = np.append(TimeTool, np.array(timetool))
        
        timetoolamp = [float(x) for x in list(ScanName['/tt/XPP_TIMETOOL_AMPL'])]
        TTAmp = np.append(TTAmp, np.array(timetoolamp))

        timetoolfwhm = [float(x) for x in list(ScanName['/tt/XPP_TIMETOOL_AMPL'])]
        TTFWHM = np.append(TTFWHM, np.array(timetoolfwhm))
        
        ScanNum = ScanNum + [filenum for x in range(len(diode))]
        
        rowlandy = list(ScanName['/Rowland/ROI_proj_ythres'])
        
        RowlandY = np.append(RowlandY, np.array([sum(x) for x in rowlandy]))
        
        if setting == 1:
            Offset = np.append(Offset, np.array([(np.mean(x[0:50])+np.mean(x[100:150]))/2*len(x) for x in rowlandy]))
        elif setting == 2:
            Offset = np.append(Offset, np.array([(sum(x[150:175]))/25*len(x) for x in rowlandy]))
        
        l3e = [float(x) for x in list(ScanName['/ebeam/L3Energy'])]
        L3E = np.append(L3E, np.array(l3e))
        
        cspad = list(ScanName['cspad/azav'])
        cspadsum = []
        for cs in cspad:
            cspadsum = cspadsum + [sum([x for x in cs if not math.isnan(x)])]
        CspadSum = np.append(CspadSum, np.array(cspadsum))
    
    
    
    if XAS:
        xasRawData.changeValue(XOn = XOn, LOn = LOn, XEnergyRaw = Var0, Diode2 = Diode2, Ipm2Sum = Ipm2Sum, TimeTool = TimeTool, \
                           TTAmp = TTAmp, TTFWHM = TTFWHM, ScanNum = ScanNum, RowlandY = RowlandY, Offset = Offset, L3E = L3E, CspadSum = CspadSum)
    
    return xasRawData

























