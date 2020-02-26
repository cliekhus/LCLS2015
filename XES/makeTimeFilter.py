# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 18:57:49 2020

@author: chelsea
"""
def makeTimeFilter(xesRawData, ploton):

    import matplotlib.pyplot as plt
    import numpy as np

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
            
        fig=plt.figure()
        fig.add_subplot(121)
        plt.hist(xesRawData.TimeTool[np.logical_and(xesRawData.XOn, xesRawData.LOn)], 1000)
        plt.title('time tool before filters')
        fig.add_subplot(122)
        plt.hist(xesRawData.TimeTool[np.logical_and.reduce((TTFilter, xesRawData.XOn, xesRawData.LOn))], 1000)
        plt.title('time tool after filters')
        
    return TTFilter