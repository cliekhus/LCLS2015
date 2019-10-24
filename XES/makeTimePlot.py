# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 14:21:20 2019

@author: chelsea
"""

def makeTimePlot(TCentersP, TCentersM, peaksProDataP, peaksProDataM, minTime, maxTime, ploton):
        
    import matplotlib.pyplot as plt
    from fitXES import fitXES
    import numpy as np
    from fittingfunctions import convolved
        
    
    pluscolor = '#0070DF'
    minuscolor = '#54A60C'
    darkpluscolor = '#004B95'
    darkminuscolor = '#376E08'
    
    
    Fitp, Fitm, params, info = fitXES(TCentersP, TCentersM, peaksProDataP.XESDiff, peaksProDataM.XESDiff, 0, ploton)
    tt = np.linspace(minTime, maxTime, 1000)
    
    plt.figure()
    line0 = plt.plot(TCentersP, peaksProDataP.XESDiff, 'o', color = pluscolor)
    line1 = plt.plot(TCentersM, peaksProDataM.XESDiff, 's', color = minuscolor)
    line2 = plt.plot(tt, convolved(tt, params[0], params[1], params[2], params[6], params[7]), color = darkpluscolor)
    line3 = plt.plot(tt, convolved(tt, params[3], params[4], params[5], params[6], params[7]), '--', color = darkminuscolor)
    plt.ylabel('$\Delta$ T x 10$^3$')
    plt.xlabel('time delay (fs)')
    plt.legend((line0[0], line1[0], line2[0], line3[0]), (peaksProDataP.EnergyLabel +' eV', peaksProDataM.EnergyLabel +' eV', peaksProDataP.EnergyLabel +' eV fit', peaksProDataM.EnergyLabel +' eV fit'))
    
    Residualp = Fitp - peaksProDataP.XESDiff
    Residualm = Fitm - peaksProDataM.XESDiff
    
    plt.figure()
    line0 = plt.plot(TCentersP, Residualp, marker = 'o', color = pluscolor)
    line1 = plt.plot(TCentersM, Residualm, marker = 's', color = minuscolor)
    plt.ylabel('residuals')
    plt.xlabel('time delay (fs)')
    plt.legend((line0[0], line1[0]), (peaksProDataP.EnergyLabel +' eV', peaksProDataM.EnergyLabel +' eV'))

    
    HammingWindowp = np.hamming(len(Residualp))
    HammingWindowm = np.hamming(len(Residualm))
    
    FTp = np.fft.rfft([x*y for x,y in zip(Residualp, HammingWindowp)])
    FTm = np.fft.rfft([x*y for x,y in zip(Residualm, HammingWindowm)])
    
    Freq = np.fft.rfftfreq(len(Residualp), d=(TCentersP[0]-TCentersP[1])*1e-15)
    
    Freq = [-x*1e-12*33.356 for x in Freq]
    
    plt.figure()
    line0 = plt.plot(Freq, np.abs(FTp), color = pluscolor)
    line1 = plt.plot(Freq, np.abs(FTm), color = minuscolor)
    plt.ylabel('fourier amplitude')
    plt.xlabel('cm$^{-1}$')
    plt.legend((line0[0], line1[0]), (peaksProDataP.EnergyLabel +' eV', peaksProDataM.EnergyLabel +' eV'))
    plt.title('with Hamming window')
    