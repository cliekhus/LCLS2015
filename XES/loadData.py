# -*- coding: utf-8 -*-
"""
Created on Fri May  3 10:37:18 2019

@author: chelsea
"""

def loadData(FileNums, fileSetting, offSetting):
    
    import h5py
    import numpy as np
    import RawDataClass as RDC
    import numpy.matlib
    
    if fileSetting == "XES":
        xesRawData = RDC.XESRawData()
    elif fileSetting == "Peaks":
        xesRawData = RDC.PeaksRawData()

    
    
    #Initialize the necessary lists
    XOn = np.empty(0)
    LOn = np.empty(0)
    Var0 = np.empty(0)
    Diode2 = np.empty(0)
    
    Ipm2Sum = np.empty(0)
    
    TimeTool = np.empty(0)
    TTAmp = np.empty(0)
    TTFWHM = np.empty(0)
    TTFP = np.empty(0)
    
    ScanNum = np.empty(0)
    
    RowlandY = np.empty(0)
    Offset = np.empty(0)
    
    L3E = np.empty(0)
    CspadSum = np.empty(0)
    
    #Fill the lists with data from the h5 file
    for filenum in FileNums:

        print(filenum)
        ScanName = h5py.File('D:\LCLS_Data\XES\ldat_xppj6715_Run' + str(filenum) + '.h5')

        
        xOn = np.array(ScanName['/lightStatus/xray'])
        XOn = np.append(XOn, xOn)
        lOn = np.array(ScanName['/lightStatus/laser'])
        LOn = np.append(LOn, lOn)
        Var0 = np.append(Var0, np.array(ScanName['/scan/var0']))
    
        diode = ScanName['/diodeU/channels']                  #Quad cell 2 from diode - this one has an output
        Diode2 = np.append(Diode2, np.array(diode[:,2]))
        
        ipm2 = ScanName['/ipm2/channels']  #Intensity (and position) monitor #2.  Quad cells 1 and 3 had signal - use these
        Ipm2Sum = np.append(Ipm2Sum, np.array(ipm2[:,1])+np.array(ipm2[:,3]))
        
        TimeTool = np.append(TimeTool, np.array(ScanName['/ttCorr/tt']))
        
        TTAmp = np.append(TTAmp, np.array(ScanName['/tt/XPP_TIMETOOL_AMPL']))

        TTFWHM = np.append(TTFWHM, np.array(ScanName['/tt/XPP_TIMETOOL_AMPL']))
        
        TTFP = np.append(TTFWHM, np.array(ScanName['/tt/XPP_TIMETOOL_FLTPOS']))
        
        ScanNum = np.append(ScanNum, np.matlib.repmat(filenum, np.shape(ipm2)[0], 1))
        
        rowlandy = np.array(ScanName['/Rowland/ROI_proj_ythres'])
        
        RowlandY = np.append(RowlandY, np.sum(rowlandy, 1))
        
        if offSetting == 1:
            Offset = np.append(Offset, (np.mean(rowlandy[:,0:50],1)+np.mean(rowlandy[:,100:150],1))/2*np.shape(rowlandy)[1])
        elif offSetting == 2:
            Offset = np.append(Offset, (np.mean(rowlandy[:,150:175],1))*np.shape(rowlandy)[1])
        
        L3E = np.append(L3E, np.array(ScanName['/ebeam/L3Energy']))
        
        cspad = list(ScanName['cspad/azav'])
        cspadsum = np.empty(len(cspad))
        ii = 0
        for cs in cspad:
            cspadsum[ii] = np.nansum(cs)
            
            ii += 1
            
        CspadSum = np.append(CspadSum, np.array(cspadsum))
    
    XOn = XOn.astype(bool)    
    LOn = LOn.astype(bool)
        
    if fileSetting == "XES":
        xesRawData.changeValue(XOn = XOn, LOn = LOn, Angle = Var0, Diode2 = Diode2, Ipm2Sum = Ipm2Sum, TimeTool = TimeTool, \
                           TTAmp = TTAmp, TTFWHM = TTFWHM, ScanNum = ScanNum, RowlandY = RowlandY, Offset = Offset, L3E = L3E, CspadSum = CspadSum, TTFP = TTFP)
    
    if fileSetting == "Peaks":
        xesRawData.changeValue(XOn = XOn, LOn = LOn, StageDelay = Var0, Diode2 = Diode2, Ipm2Sum = Ipm2Sum, TimeTool = TimeTool, \
                           TTAmp = TTAmp, TTFWHM = TTFWHM, ScanNum = ScanNum, RowlandY = RowlandY, Offset = Offset, L3E = L3E, CspadSum = CspadSum, TTFP = TTFP)
    

    return xesRawData
    
    

























