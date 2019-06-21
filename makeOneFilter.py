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
def makeOneFilter(Diode2, Ipm2Sum, Signal, XOn, LOn, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, L3E, CspadSum, ploton, choice):

    from makeIntensityFilter import makeDiodeFilter
    from makeIntensityFilter import makeOneRowlandFilter
    from itertools import compress
    import matplotlib.pyplot as plt
    from getMedianAndSTD import getMedianAndSTD
    import statistics as stat
    import math
        

    IpmNumSTDs = 2
    
    Ipm2Median = stat.median([x for x in Ipm2Sum if not math.isnan(x)])
    Ipm2STD = stat.stdev([x for x in Ipm2Sum if not math.isnan(x)])
    
    IpmFilter = list(a < Ipm2Median+Ipm2STD*IpmNumSTDs and a > Ipm2Median-Ipm2STD*IpmNumSTDs for a in Ipm2Sum)
    
    
    L3ENumSTDs = 2
    
    L3EMedian = stat.median(L3E)
    L3ESTD = stat.stdev(L3E)
    
    L3EFilter = list(a < L3EMedian+L3ESTD*L3ENumSTDs and a > L3EMedian-L3ESTD*L3ENumSTDs for a in L3E)
    
    CspadSumSTDs = 2
    
    CspadSumMedian = stat.median(CspadSum)
    CspadSumSTD = stat.stdev(CspadSum)
    
    CspadSumFilter = list(a < CspadSumMedian+CspadSumSTD*CspadSumSTDs and a > CspadSumMedian-CspadSumSTD*CspadSumSTDs for a in CspadSum)
    
    if ploton:
        plt.figure()
        plt.plot(L3E)
        plt.plot(list(compress(L3E, L3EFilter)))
        plt.title('L3E')
        plt.xlabel('shot number')
        
        plt.figure()
        plt.plot(Ipm2Sum)
        plt.plot(list(compress(Ipm2Sum, IpmFilter)))
        plt.title('Ipm')
        plt.xlabel('shotnumber')
        
        plt.figure()
        plt.plot(CspadSum)
        plt.plot(list(compress(CspadSum, CspadSumFilter)))
        plt.title('Cspad')
        plt.xlabel('shotnumber')
    
    
    if choice == 1:
        DISMedian, DISSTD = getMedianAndSTD(DiodeIpmSlope, ScanNum)
        DiodeFilter = makeDiodeFilter(Ipm2Sum, Signal, XOn, LOn, DiodeIpmSlope, DISMedian, DISSTD, ploton)
        IntensityFilter = [a and b for a,b in zip(IpmFilter, DiodeFilter)]
    elif choice == 2:
        RowlandFilter, Offset = makeOneRowlandFilter(Diode2, Signal, XOn, ploton)
        IntensityFilter = [a and b and c and d for a,b,c,d in zip(IpmFilter, RowlandFilter, L3EFilter, CspadSumFilter)]

    #Convert the timetool signal into femtosecond delays and create the time tool filters
    TTSTDs = 3
    TTMedian = stat.median(TimeTool)
    TTSTD = stat.stdev(TimeTool)
    TTValueFilter = list(a < TTMedian+TTSTDs*TTSTD and a > TTMedian-TTSTDs*TTSTD for a in TimeTool)
    
    TTAmpSTDs = 2
    TTAmpMedian = stat.median(TTAmp)
    TTAmpSTD = stat.stdev(TTAmp)
    TTAmpFilter = list(a < TTAmpMedian+TTAmpSTDs*TTAmpSTD and a > TTAmpMedian-TTAmpSTDs*TTAmpSTD for a in TTAmp)
    
    TTFWHMSTDs = 2
    TTFWHMMedian = stat.median(TTFWHM)
    TTFWHMSTD = stat.stdev(TTFWHM)
    TTFWHMFilter = list(a < TTFWHMMedian+TTFWHMSTDs*TTFWHMSTD and a > TTFWHMMedian-TTFWHMSTDs*TTFWHMSTD for a in TTFWHM)
    
    TTFilter = list(((a and b and c) or not e) and d for a,b,c,d,e in zip(TTValueFilter, TTAmpFilter, TTFWHMFilter, XOn, LOn))
    
    if ploton:
            
        fig=plt.figure()
        fig.add_subplot(121)
        plt.hist(list(compress(TimeTool, [a and b for a,b in zip(XOn, LOn)])), 1000)
        plt.title('time tool before filters')
        fig.add_subplot(122)
        plt.hist(list(compress(TimeTool, [a and b and c for a,b,c in zip(TTFilter, XOn, LOn)])), 1000)
        plt.title('time tool after filters')
    
    Filter = list(a and b for a,b in zip(TTFilter, IntensityFilter))

    return Filter, Offset