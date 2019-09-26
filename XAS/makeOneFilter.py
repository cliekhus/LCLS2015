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
def makeOneFilter(xasRawData, selectedRuns, ploton, choice):

    from makeIntensityFilter import makeOneDiodeFilter
    from makeIntensityFilter import makeOneRowlandFilter
    import matplotlib.pyplot as plt
    import statistics as stat
    import numpy as np
        

    IpmNumSTDs = 2
    
    Ipm2Median = np.nanmedian(xasRawData.Ipm2Sum[xasRawData.XOn])
    Ipm2STD = np.nanstd(xasRawData.Ipm2Sum[xasRawData.XOn])
    
    print("makeOneFilter")
    nancheck = np.isinf(xasRawData.Ipm2Sum)
    print(sum(nancheck.astype(int)))
    
    IpmFilter = np.logical_and(xasRawData.Ipm2Sum < Ipm2Median+Ipm2STD*IpmNumSTDs, xasRawData.Ipm2Sum > Ipm2Median-Ipm2STD*IpmNumSTDs)
    
    
    L3ENumSTDs = 1
    
    L3EMedian = stat.median(xasRawData.L3E)
    L3ESTD = stat.stdev(xasRawData.L3E)
    
    L3EFilter = np.logical_and(xasRawData.L3E < L3EMedian+L3ESTD*L3ENumSTDs, xasRawData.L3E > L3EMedian-L3ESTD*L3ENumSTDs)
    
    
    CspadSumSTDs = 2
    
    CspadSumMedian = np.median(xasRawData.CspadSum[selectedRuns])
    CspadSumSTD = np.std(xasRawData.CspadSum[selectedRuns])
    
    CspadSumFilter = np.logical_and(xasRawData.CspadSum < CspadSumMedian+CspadSumSTD*CspadSumSTDs, xasRawData.CspadSum > CspadSumMedian-CspadSumSTD*CspadSumSTDs)
    
    
    plt.xlabel('shot number')
    if ploton:
        plt.figure()
        plt.plot(xasRawData.L3E)
        plt.plot(xasRawData.L3E[L3EFilter])
        plt.title('L3E')
        
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
    
    
    if choice == 1:
        DiodeFilter, Offset = makeOneDiodeFilter(xasRawData.CspadSum, xasRawData.Diode2, xasRawData.XOn, selectedRuns, ploton)
        IntensityFilter = np.logical_and.reduce((IpmFilter, DiodeFilter, L3EFilter, CspadSumFilter))
    elif choice == 2:
        RowlandFilter, Offset = makeOneRowlandFilter(xasRawData.Diode2, xasRawData.RowlandSum, xasRawData.XOn, ploton)
        IntensityFilter = np.logical_and.reduce((IpmFilter, RowlandFilter, L3EFilter, CspadSumFilter))

    #Convert the timetool signal into femtosecond delays and create the time tool filters
    TTSTDs = 3
    TTMedian = stat.median(xasRawData.TimeTool)
    TTSTD = stat.stdev(xasRawData.TimeTool)
    TTValueFilter = np.logical_and(xasRawData.TimeTool < TTMedian+TTSTDs*TTSTD, xasRawData.TimeTool > TTMedian-TTSTDs*TTSTD)
    
    TTAmpSTDs = 2
    TTAmpMedian = stat.median(xasRawData.TTAmp)
    TTAmpSTD = stat.stdev(xasRawData.TTAmp)
    TTAmpFilter = np.logical_and(xasRawData.TTAmp < TTAmpMedian+TTAmpSTDs*TTAmpSTD, xasRawData.TTAmp > TTAmpMedian-TTAmpSTDs*TTAmpSTD)
    
    TTFWHMSTDs = 2
    TTFWHMMedian = stat.median(xasRawData.TTFWHM)
    TTFWHMSTD = stat.stdev(xasRawData.TTFWHM)
    TTFWHMFilter = np.logical_and(xasRawData.TTFWHM < TTFWHMMedian+TTFWHMSTDs*TTFWHMSTD, xasRawData.TTFWHM > TTFWHMMedian-TTFWHMSTDs*TTFWHMSTD)
    
    TTFilter = np.logical_and(np.logical_or(np.logical_and.reduce((TTValueFilter, TTAmpFilter, TTFWHMFilter)), np.logical_not(xasRawData.XOn)), xasRawData.LOn)
    
    if ploton:
            
        fig=plt.figure()
        fig.add_subplot(121)
        plt.hist(xasRawData.TimeTool[np.logical_and(xasRawData.XOn, xasRawData.LOn)], 1000)
        plt.title('time tool before filters')
        fig.add_subplot(122)
        plt.hist(xasRawData.TimeTool[np.logical_and.reduce((TTFilter, xasRawData.XOn, xasRawData.LOn))], 1000)
        plt.title('time tool after filters')
    
    Filter = np.logical_and(TTFilter, IntensityFilter)

    return Filter, Offset