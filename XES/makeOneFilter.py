# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 18:02:52 2019

@author: chelsea
"""

# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:07:12 2019

@author: chelsea
"""
def makeOneFilter(xesRawData, ploton):

    import matplotlib.pyplot as plt
    import numpy as np
    

    NanCheck = np.logical_not(np.logical_or.reduce((np.isnan(xesRawData.Diode2), np.isnan(xesRawData.Ipm2Sum), np.isnan(xesRawData.CspadSum), np.isnan(xesRawData.L3E))))

    IpmNumSTDs = 3
    Ipm2Median = np.nanmedian(xesRawData.Ipm2Sum[xesRawData.XOn])
    Ipm2STD = np.nanstd(xesRawData.Ipm2Sum[xesRawData.XOn])
    IpmFilter = np.abs(xesRawData.Ipm2Sum - Ipm2Median) < Ipm2STD*IpmNumSTDs
                               
    
    L3ENumSTDs = 1
    L3EMedian = np.nanmedian(xesRawData.L3E[xesRawData.XOn])
    L3ESTD = np.nanstd(xesRawData.L3E[xesRawData.XOn])
    L3EFilter = np.abs(xesRawData.L3E - L3EMedian) < L3ESTD*L3ENumSTDs
    
    
    CspadSumSTDs = 2
    CspadSumMin = 0.1
    CspadSumMedian = np.nanmedian(xesRawData.CspadSum[xesRawData.XOn])
    CspadSumSTD = np.nanstd(xesRawData.CspadSum[xesRawData.XOn])
    CspadSumFilter = np.logical_and(np.abs(xesRawData.CspadSum - CspadSumMedian) < CspadSumSTD*CspadSumSTDs, xesRawData.CspadSum > CspadSumMin*CspadSumMedian)

    
    RowlandSTDs = 1
    RowlandMedian = np.nanmedian(xesRawData.RowlandY[xesRawData.XOn])
    RowlandSTD = np.nanstd(xesRawData.RowlandY[xesRawData.XOn])
    RowlandFilter = np.abs(xesRawData.RowlandY - RowlandMedian) < RowlandSTD*RowlandSTDs
    
    
    DiodeSTDs = 1
    DiodeMin = 0.1
    DiodeMedian = np.nanmedian(xesRawData.Diode2[xesRawData.XOn])
    DiodeSTD = np.nanstd(xesRawData.Diode2[xesRawData.XOn])
    DiodeFilter = np.logical_and(np.abs(xesRawData.Diode2 - DiodeMedian) < DiodeSTD*DiodeSTDs, xesRawData.Diode2 > DiodeMin*DiodeMedian)

    
    AllFilter = np.logical_and.reduce((IpmFilter, L3EFilter, CspadSumFilter, RowlandFilter, DiodeFilter, NanCheck, xesRawData.XOn))
    
    if ploton:
        plt.figure(figsize = (5,7))
        plt.subplot(3,2,1)
        plt.plot(xesRawData.L3E/np.max(xesRawData.L3E))
        plt.plot(xesRawData.L3E[L3EFilter]/np.max(xesRawData.L3E))
        plt.title('electron bunch energy')
        plt.xlabel('shot number')
        
        #plt.figure()
        plt.subplot(3,2,2)
        plt.plot(xesRawData.Ipm2Sum/np.nanmax(xesRawData.Ipm2Sum))
        plt.plot(xesRawData.Ipm2Sum[IpmFilter]/np.nanmax(xesRawData.Ipm2Sum))
        plt.title('x-ray intensity')
        plt.xlabel('shotnumber')
        
        #plt.figure()
        plt.subplot(3,2,3)
        plt.plot(xesRawData.CspadSum/np.max(xesRawData.CspadSum))
        plt.plot(xesRawData.CspadSum[CspadSumFilter]/np.max(xesRawData.CspadSum))
        plt.title('cspad sum')
        plt.xlabel('shotnumber')
        
        #plt.figure()
        plt.subplot(3,2,4)
        plt.plot(xesRawData.RowlandY/np.max(xesRawData.RowlandY))
        plt.plot(xesRawData.RowlandY[RowlandFilter]/np.max(xesRawData.RowlandY))
        plt.title('rowland measurement')
        plt.xlabel('shotnumber')
        
        #plt.figure()
        plt.subplot(3,2,5)
        plt.plot(xesRawData.Diode2/np.max(xesRawData.Diode2))
        plt.plot(xesRawData.Diode2[DiodeFilter]/np.max(xesRawData.Diode2))
        plt.title('TFY diode')
        plt.xlabel('shotnumber')
    
    
    TTSTDs = 3
    TTMedian = np.median(xesRawData.TimeTool[np.logical_and(xesRawData.XOn, xesRawData.LOn)])
    TTSTD = np.std(xesRawData.TimeTool[np.logical_and(xesRawData.XOn, xesRawData.LOn)])
    TTValueFilter = np.abs(xesRawData.TimeTool - TTMedian) < TTSTDs*TTSTD
    
    
    TTAmpSTDs = 3
    TTAmpMedian = np.median(xesRawData.TTAmp[np.logical_and(xesRawData.XOn, xesRawData.LOn)])
    TTAmpSTD = np.std(xesRawData.TTAmp[np.logical_and(xesRawData.XOn, xesRawData.LOn)])
    TTAmpFilter = np.abs(xesRawData.TTAmp - TTAmpMedian) < TTAmpSTDs*TTAmpSTD
    
    
    TTFWHMSTDs = 3
    TTFWHMMedian = np.median(xesRawData.TTFWHM[np.logical_and(xesRawData.XOn, xesRawData.LOn)])
    TTFWHMSTD = np.std(xesRawData.TTFWHM[np.logical_and(xesRawData.XOn, xesRawData.LOn)])
    TTFWHMFilter = np.abs(xesRawData.TTFWHM - TTFWHMMedian) < TTFWHMSTDs*TTFWHMSTD
    

    TTFPMax = 600
    TTFPMin = 200
    TTFPFilter = np.logical_and(xesRawData.TTFP <= TTFPMax, xesRawData.TTFP >= TTFPMin)
    TTFPFilter[np.logical_not(np.logical_or(TTFPFilter==False, TTFPFilter==True))] = False

    
    TTFilter = np.logical_and.reduce((TTValueFilter, TTAmpFilter, TTFWHMFilter, TTFPFilter))
    
    if ploton:
            
        #fig=plt.figure()
        #fig.add_subplot(121)
        plt.subplot(3,2,6)
        plt.plot(xesRawData.TimeTool[np.logical_and(xesRawData.XOn, xesRawData.LOn)]/np.max(xesRawData.TimeTool[np.logical_and(xesRawData.XOn, xesRawData.LOn)]))
        plt.plot(xesRawData.TimeTool[np.logical_and.reduce((TTFilter, xesRawData.XOn, xesRawData.LOn))]/np.max(xesRawData.TimeTool[np.logical_and(xesRawData.XOn, xesRawData.LOn)]))
        plt.title('time tool')
        plt.tight_layout()
    

    return AllFilter, TTFilter