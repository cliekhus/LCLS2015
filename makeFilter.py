# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:07:12 2019

@author: chelsea
"""
def makeFilter(Diode2, Ipm2Sum, Ipm2Median, Ipm2STD, Signal, XOn, LOn, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, ploton, diode):
    
    from makeIntensityFilter import makeDiodeFilter
    from makeIntensityFilter import makeRowlandFilter
    from itertools import compress
    import matplotlib.pyplot as plt
        
    #Set up the intensity filter - the diode and cspad sum should respond linearly with the x-ray intensity
    IpmNumSTDs = 3
    IpmFilter = list(a < b+IpmNumSTDs*c and a > b-IpmNumSTDs*c for a,b,c in zip(Ipm2Sum, Ipm2Median, Ipm2STD))
    
    if diode:
        DiodeFilter = makeDiodeFilter(Ipm2Sum, Signal, XOn, LOn, DiodeIpmSlope, DISMedian, DISSTD, ploton)
        IntensityFilter = [a and b for a,b in zip(IpmFilter, DiodeFilter)]
    else:
        RowlandFilter = makeRowlandFilter(Diode2, Signal, XOn, ploton)
        IntensityFilter = [a and b for a,b in zip(IpmFilter, RowlandFilter)]
    
    
    #Convert the timetool signal into femtosecond delays and create the time tool filters
    TTSTDs = 3
    TTValueFilter = list(a < b+TTSTDs*c and a > b-TTSTDs*c for a,b,c in zip(TimeTool, TTMedian, TTSTD))
    
    TTAmpSTDs = 3
    TTAmpFilter = list(a < b+TTAmpSTDs*c and a > b-TTAmpSTDs*c for a,b,c in zip(TTAmp, TTAmpMedian, TTAmpSTD))
    
    TTFWHMSTDs = 3
    TTFWHMFilter = list(a < b+TTFWHMSTDs*c and a > b-TTFWHMSTDs*c for a,b,c in zip(TTFWHM, TTFWHMMedian, TTFWHMSTD))
    
    TTFilter = list((a and b and c) or not d or not e for a,b,c,d,e in zip(TTValueFilter, TTAmpFilter, TTFWHMFilter, XOn, LOn))
    
    if ploton:
            
        fig=plt.figure()
        fig.add_subplot(121)
        plt.hist(list(compress(TimeTool, [a and b for a,b in zip(XOn, LOn)])), 1000)
        plt.title('time tool before filters')
        fig.add_subplot(122)
        plt.hist(list(compress(TimeTool, [a and b and c for a,b,c in zip(TTFilter, XOn, LOn)])), 1000)
        plt.title('time tool after filters')
    
    Filter = list(a and b for a,b in zip(TTFilter, IntensityFilter))
    
    return Filter