# -*- coding: utf-8 -*-
"""
Created on Fri May  3 11:07:12 2019

@author: chelsea
"""
def makeFilter(Diode2, Ipm2Sum, Signal, XOn, LOn, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ploton, ScanNum, choice):
    
    from makeIntensityFilter import makeDiodeFilter
    from makeIntensityFilter import makeRowlandFilter
    from itertools import compress
    import matplotlib.pyplot as plt
    from getMedianAndSTD import getMedianAndSTD
        
    #Set up the intensity filter - the diode and cspad sum should respond linearly with the x-ray intensity
    IpmNumSTDs = 1
    
    Ipm2Median, Ipm2STD = getMedianAndSTD(Ipm2Sum, ScanNum)
    
    IpmFilter = list(a < b+IpmNumSTDs*c and a > b-IpmNumSTDs*c for a,b,c in zip(Ipm2Sum, Ipm2Median, Ipm2STD))
    
    if choice == 1:
        DISMedian, DISSTD = getMedianAndSTD(DiodeIpmSlope, ScanNum)
        DiodeFilter = makeDiodeFilter(Ipm2Sum, Signal, XOn, LOn, DiodeIpmSlope, DISMedian, DISSTD, ploton)
        IntensityFilter = [a and b for a,b in zip(IpmFilter, DiodeFilter)]
    elif choice == 2:
        RowlandFilter = makeRowlandFilter(Diode2, Signal, XOn, ploton)
        IntensityFilter = [a and b for a,b in zip(IpmFilter, RowlandFilter)]
    
    
    #Convert the timetool signal into femtosecond delays and create the time tool filters
    TTSTDs = 1
    TTMedian, TTSTD = getMedianAndSTD(TimeTool, ScanNum)
    TTValueFilter = list(a < b+TTSTDs*c and a > b-TTSTDs*c for a,b,c in zip(TimeTool, TTMedian, TTSTD))
    
    TTAmpSTDs = 1
    TTAmpMedian, TTAmpSTD = getMedianAndSTD(TTAmp, ScanNum)
    TTAmpFilter = list(a < b+TTAmpSTDs*c and a > b-TTAmpSTDs*c for a,b,c in zip(TTAmp, TTAmpMedian, TTAmpSTD))
    
    TTFWHMSTDs = 1
    TTFWHMMedian, TTFWHMSTD = getMedianAndSTD(TTFWHM, ScanNum)
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