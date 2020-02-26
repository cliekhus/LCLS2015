# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:07:12 2019

@author: chelsea
"""
def makeMedFilter(xesRawData, Filter, ploton):

    import matplotlib.pyplot as plt
    import numpy as np
        

    SelectFilter = np.logical_and(Filter, xesRawData.XOn)
    NanCheck = np.logical_not(np.logical_or.reduce((np.isnan(xesRawData.Diode2), np.isnan(xesRawData.Ipm2Sum), np.isnan(xesRawData.CspadSum), np.isnan(xesRawData.L3E))))

    IpmNumSTDs = 3
    Ipm2Median = np.nanmedian(xesRawData.Ipm2Sum[SelectFilter])
    Ipm2STD = np.nanstd(xesRawData.Ipm2Sum[SelectFilter])
    IpmFilter = np.abs(xesRawData.Ipm2Sum - Ipm2Median) < Ipm2STD*IpmNumSTDs
                               
    
    L3ENumSTDs = 1
    L3EMedian = np.nanmedian(xesRawData.L3E[SelectFilter])
    L3ESTD = np.nanstd(xesRawData.L3E[SelectFilter])
    L3EFilter = np.abs(xesRawData.L3E - L3EMedian) < L3ESTD*L3ENumSTDs
    
    
    CspadSumSTDs = 2
    CspadSumMin = 0.1
    CspadSumMedian = np.nanmedian(xesRawData.CspadSum[SelectFilter])
    CspadSumSTD = np.nanstd(xesRawData.CspadSum[SelectFilter])
    CspadSumFilter = np.logical_and(np.abs(xesRawData.CspadSum - CspadSumMedian) < CspadSumSTD*CspadSumSTDs, xesRawData.CspadSum > CspadSumMin*CspadSumMedian)

    
    RowlandSTDs = 1
    RowlandMedian = np.nanmedian(xesRawData.RowlandY[SelectFilter])
    RowlandSTD = np.nanstd(xesRawData.RowlandY[SelectFilter])
    RowlandFilter = np.abs(xesRawData.RowlandY - RowlandMedian) < RowlandSTD*RowlandSTDs
    
    
    DiodeSTDs = 1
    DiodeMin = 0.1
    DiodeMedian = np.nanmedian(xesRawData.Diode2[SelectFilter])
    DiodeSTD = np.nanstd(xesRawData.Diode2[SelectFilter])
    DiodeFilter = np.logical_and(np.abs(xesRawData.Diode2 - DiodeMedian) < DiodeSTD*DiodeSTDs, xesRawData.Diode2 > DiodeMin*DiodeMedian)

    
    AllFilter = np.logical_and.reduce((IpmFilter, L3EFilter, CspadSumFilter, RowlandFilter, DiodeFilter, NanCheck, xesRawData.XOn))
    
    if ploton:
        plt.figure()
        plt.plot(xesRawData.L3E)
        plt.plot(xesRawData.L3E[L3EFilter])
        plt.title('L3E')
        plt.xlabel('shot number')
        
        plt.figure()
        plt.plot(xesRawData.Ipm2Sum)
        plt.plot(xesRawData.Ipm2Sum[IpmFilter])
        plt.title('Ipm')
        plt.xlabel('shotnumber')
        
        plt.figure()
        plt.plot(xesRawData.CspadSum)
        plt.plot(xesRawData.CspadSum[CspadSumFilter])
        plt.title('Cspad')
        plt.xlabel('shotnumber')
        
        plt.figure()
        plt.plot(xesRawData.RowlandY)
        plt.plot(xesRawData.RowlandY[RowlandFilter])
        plt.title('RowlandY')
        plt.xlabel('shotnumber')
        
        plt.figure()
        plt.plot(xesRawData.Diode2)
        plt.plot(xesRawData.Diode2[DiodeFilter])
        plt.title('Diode2')
        plt.xlabel('shotnumber')


    return AllFilter