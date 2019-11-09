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
def makeOneFilter(xasRawData, ploton):

    import matplotlib.pyplot as plt
    import numpy as np
        

    NanCheck = np.logical_not(np.logical_or.reduce((np.isnan(xasRawData.Diode2), np.isnan(xasRawData.Ipm2Sum), np.isnan(xasRawData.CspadSum), np.isnan(xasRawData.L3E))))

    IpmNumSTDs = 2
    Ipm2Median = np.nanmedian(xasRawData.Ipm2Sum[xasRawData.XOn])
    Ipm2STD = np.nanstd(xasRawData.Ipm2Sum[xasRawData.XOn])
    IpmFilter = np.abs(xasRawData.Ipm2Sum - Ipm2Median) < Ipm2STD*IpmNumSTDs
                               
    
    L3ENumSTDs = 1
    L3EMedian = np.nanmedian(xasRawData.L3E[xasRawData.XOn])
    L3ESTD = np.nanstd(xasRawData.L3E[xasRawData.XOn])
    L3EFilter = np.abs(xasRawData.L3E - L3EMedian) < L3ESTD*L3ENumSTDs
    
    
    CspadSumSTDs = 2
    CspadSumMin = 0.1
    CspadSumMedian = np.nanmedian(xasRawData.CspadSum[xasRawData.XOn])
    CspadSumSTD = np.nanstd(xasRawData.CspadSum[xasRawData.XOn])
    CspadSumFilter = np.logical_and(np.abs(xasRawData.CspadSum - CspadSumMedian) < CspadSumSTD*CspadSumSTDs, xasRawData.CspadSum > CspadSumMin*CspadSumMedian)

    
    RowlandSTDs = 2
    RowlandMedian = np.nanmedian(xasRawData.RowlandY[xasRawData.XOn])
    RowlandSTD = np.nanstd(xasRawData.RowlandY[xasRawData.XOn])
    RowlandFilter = np.abs(xasRawData.RowlandY - RowlandMedian) < RowlandSTD*RowlandSTDs
    
    
    DiodeSTDs = 2
    DiodeMin = 0.1
    DiodeMedian = np.nanmedian(xasRawData.Diode2[xasRawData.XOn])
    DiodeSTD = np.nanstd(xasRawData.Diode2[xasRawData.XOn])
    DiodeFilter = np.logical_and(np.abs(xasRawData.Diode2 - DiodeMedian) < DiodeSTD*DiodeSTDs, xasRawData.Diode2 > DiodeMin*DiodeMedian)
    
    
    AllFilter = np.logical_and.reduce((IpmFilter, L3EFilter, CspadSumFilter, RowlandFilter, DiodeFilter, NanCheck, xasRawData.XOn))
    
    if ploton:
        plt.figure()
        plt.plot(xasRawData.L3E)
        plt.plot(xasRawData.L3E[L3EFilter])
        plt.title('L3E')
        plt.xlabel('shot number')
        
        plt.figure()
        plt.plot(xasRawData.Ipm2Sum)
        plt.plot(xasRawData.Ipm2Sum[IpmFilter])
        plt.title('Ipm')
        plt.xlabel('shotnumber')
        
        plt.figure()
        plt.plot(xasRawData.CspadSum)
        plt.plot(xasRawData.CspadSum[CspadSumFilter])
        plt.title('Cspad')
        plt.xlabel('shotnumber')
        
        plt.figure()
        plt.plot(xasRawData.RowlandY)
        plt.plot(xasRawData.RowlandY[RowlandFilter])
        plt.title('RowlandY')
        plt.xlabel('shotnumber')
        
        plt.figure()
        plt.plot(xasRawData.Diode2)
        plt.plot(xasRawData.Diode2[RowlandFilter])
        plt.title('Diode2')
        plt.xlabel('shotnumber')
    
    
    TTSTDs = 5
    TTMedian = np.median(xasRawData.TimeTool[np.logical_and(xasRawData.XOn, xasRawData.LOn)])
    TTSTD = np.std(xasRawData.TimeTool[np.logical_and(xasRawData.XOn, xasRawData.LOn)])
    TTValueFilter = np.abs(xasRawData.TimeTool - TTMedian) < TTSTDs*TTSTD
    
    
    TTAmpSTDs = 2
    TTAmpMedian = np.median(xasRawData.TTAmp[np.logical_and(xasRawData.XOn, xasRawData.LOn)])
    TTAmpSTD = np.std(xasRawData.TTAmp[np.logical_and(xasRawData.XOn, xasRawData.LOn)])
    TTAmpFilter = np.abs(xasRawData.TTAmp - TTAmpMedian) < TTAmpSTDs*TTAmpSTD
    
    
    TTFWHMSTDs = 2
    TTFWHMMedian = np.median(xasRawData.TTFWHM[np.logical_and(xasRawData.XOn, xasRawData.LOn)])
    TTFWHMSTD = np.std(xasRawData.TTFWHM[np.logical_and(xasRawData.XOn, xasRawData.LOn)])
    TTFWHMFilter = np.abs(xasRawData.TTFWHM - TTFWHMMedian) < TTFWHMSTDs*TTFWHMSTD

    
    TTFilter = np.logical_and.reduce((TTValueFilter, TTAmpFilter, TTFWHMFilter))
    
    if ploton:
            
        fig=plt.figure()
        fig.add_subplot(121)
        plt.hist(xasRawData.TimeTool[np.logical_and(xasRawData.XOn, xasRawData.LOn)], 1000)
        plt.title('time tool before filters')
        fig.add_subplot(122)
        plt.hist(xasRawData.TimeTool[np.logical_and.reduce((TTFilter, xasRawData.XOn, xasRawData.LOn))], 1000)
        plt.title('time tool after filters')
    

    return AllFilter, TTFilter