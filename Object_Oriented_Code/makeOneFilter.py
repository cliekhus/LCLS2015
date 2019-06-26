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
    from itertools import compress
    import matplotlib.pyplot as plt
    import statistics as stat
    import math
        

    IpmNumSTDs = 2
    
    Ipm2Median = stat.median([x for x in xasRawData.Ipm2Sum if not math.isnan(x)])
    Ipm2STD = stat.stdev([x for x in xasRawData.Ipm2Sum if not math.isnan(x)])
    
    IpmFilter = list(a < Ipm2Median+Ipm2STD*IpmNumSTDs and a > Ipm2Median-Ipm2STD*IpmNumSTDs for a in xasRawData.Ipm2Sum)
    
    
    L3ENumSTDs = 1
    
    L3EMedian = stat.median(xasRawData.L3E)
    L3ESTD = stat.stdev(xasRawData.L3E)
    
    L3EFilter = list(a < L3EMedian+L3ESTD*L3ENumSTDs and a > L3EMedian-L3ESTD*L3ENumSTDs for a in xasRawData.L3E)
    
    CspadSumSTDs = 2
    
    CspadSumMedian = stat.median(list(compress(xasRawData.CspadSum, selectedRuns)))
    CspadSumSTD = stat.stdev(list(compress(xasRawData.CspadSum, selectedRuns)))
    
    CspadSumFilter = list(a < CspadSumMedian+CspadSumSTD*CspadSumSTDs and a > CspadSumMedian-CspadSumSTD*CspadSumSTDs for a in xasRawData.CspadSum)
    
    
    plt.xlabel('shot number')
    if ploton:
        plt.figure()
        plt.plot(xasRawData.L3E)
        plt.plot(list(compress(xasRawData.L3E, L3EFilter)))
        plt.title('L3E')
        
        plt.figure()
        plt.plot(xasRawData.Ipm2Sum)
        plt.plot(list(compress(xasRawData.Ipm2Sum, IpmFilter)))
        plt.title('Ipm')
        plt.xlabel('shotnumber')
        
        plt.figure()
        plt.plot(xasRawData.CspadSum)
        plt.plot(list(compress(xasRawData.CspadSum, CspadSumFilter)))
        plt.title('Cspad')
        plt.xlabel('shotnumber')
    
    
    if choice == 1:
        DiodeFilter, Offset = makeOneDiodeFilter(xasRawData.CspadSum, xasRawData.Diode2, xasRawData.XOn, selectedRuns, ploton)
        IntensityFilter = [a and b and b and d for a,b,c,d in zip(IpmFilter, DiodeFilter, L3EFilter, CspadSumFilter)]
    elif choice == 2:
        RowlandFilter, Offset = makeOneRowlandFilter(xasRawData.Diode2, xasRawData.RowlandSum, xasRawData.XOn, ploton)
        IntensityFilter = [a and b and c and d for a,b,c,d in zip(IpmFilter, RowlandFilter, L3EFilter, CspadSumFilter)]

    #Convert the timetool signal into femtosecond delays and create the time tool filters
    TTSTDs = 3
    TTMedian = stat.median(xasRawData.TimeTool)
    TTSTD = stat.stdev(xasRawData.TimeTool)
    TTValueFilter = list(a < TTMedian+TTSTDs*TTSTD and a > TTMedian-TTSTDs*TTSTD for a in xasRawData.TimeTool)
    
    TTAmpSTDs = 2
    TTAmpMedian = stat.median(xasRawData.TTAmp)
    TTAmpSTD = stat.stdev(xasRawData.TTAmp)
    TTAmpFilter = list(a < TTAmpMedian+TTAmpSTDs*TTAmpSTD and a > TTAmpMedian-TTAmpSTDs*TTAmpSTD for a in xasRawData.TTAmp)
    
    TTFWHMSTDs = 2
    TTFWHMMedian = stat.median(xasRawData.TTFWHM)
    TTFWHMSTD = stat.stdev(xasRawData.TTFWHM)
    TTFWHMFilter = list(a < TTFWHMMedian+TTFWHMSTDs*TTFWHMSTD and a > TTFWHMMedian-TTFWHMSTDs*TTFWHMSTD for a in xasRawData.TTFWHM)
    
    TTFilter = list(((a and b and c) or not e) and d for a,b,c,d,e in zip(TTValueFilter, TTAmpFilter, TTFWHMFilter, xasRawData.XOn, xasRawData.LOn))
    
    if ploton:
            
        fig=plt.figure()
        fig.add_subplot(121)
        plt.hist(list(compress(xasRawData.TimeTool, [a and b for a,b in zip(xasRawData.XOn, xasRawData.LOn)])), 1000)
        plt.title('time tool before filters')
        fig.add_subplot(122)
        plt.hist(list(compress(xasRawData.TimeTool, [a and b and c for a,b,c in zip(TTFilter, xasRawData.XOn, xasRawData.LOn)])), 1000)
        plt.title('time tool after filters')
    
    Filter = list(a and b for a,b in zip(TTFilter, IntensityFilter))

    return Filter, Offset