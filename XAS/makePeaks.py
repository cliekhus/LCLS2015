# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:34:21 2019

@author: chelsea
"""

def makePeaks(xasPeaksData, peaksProData, DorH, ploton):
    
    import matplotlib.pyplot as plt
    from makeOneFilter import makeOneFilter
    import numpy as np
    from makeIntensityFilter import makeOneDiodeFilter
    
    NumTTSteps = len(peaksProData.TTSteps)-1
    
    XASOn = np.empty(NumTTSteps)
    XASOff = np.empty(NumTTSteps)
    
    NormFactor_On = np.empty(NumTTSteps)
    NormFactor_Off = np.empty(NumTTSteps)
    
    XASOn_Norm = np.empty(NumTTSteps)
    XASOff_Norm = np.empty(NumTTSteps)
    
    Num_On = np.empty(NumTTSteps)
    Num_Off = np.empty(NumTTSteps)
    
    Error_On = np.empty(NumTTSteps)
    Error_Off = np.empty(NumTTSteps)
    
    
    selectedRuns, TTFilter = makeOneFilter(xasPeaksData, ploton)
    DiodeFilter, Offset = makeOneDiodeFilter(xasPeaksData, selectedRuns, ploton)
    off = np.logical_and.reduce((np.logical_not(xasPeaksData.LOn), selectedRuns, DiodeFilter))

    NormFactor_Off = sum(xasPeaksData.CspadSum[off])
    Num_Off = sum(off.astype(int))
    
    if DorH:
            
        XASOff = sum(xasPeaksData.Diode2[off])
        Error_Off = np.nanstd(xasPeaksData.Diode2[off]/xasPeaksData.CspadSum[off])/np.sqrt(Num_Off)
            
    else:
        
        XASOff = sum(xasPeaksData.RowlandY[off])
        Error_Off = np.nanstd(xasPeaksData.RowlandY[off]/xasPeaksData.CspadSum[off])/np.sqrt(Num_Off)


    for jj in range(NumTTSteps):
        
        on = np.logical_and.reduce((xasPeaksData.LOn, selectedRuns, TTFilter, DiodeFilter, \
                                    (peaksProData.Delay > peaksProData.TTSteps[jj]), (peaksProData.Delay <= peaksProData.TTSteps[jj+1])))
        
        NormFactor_On[jj] = sum(xasPeaksData.CspadSum[on])
        Num_On[jj] = sum(on.astype(int))
        
        if DorH:
            
            XASOn[jj] = sum(xasPeaksData.Diode2[on])
            Error_On[jj] = np.nanstd(xasPeaksData.Diode2[on]/xasPeaksData.CspadSum[on])/np.sqrt(Num_On[jj])

        else:
            
            XASOn[jj] = sum(xasPeaksData.RowlandY[on])
            Error_On[jj] = np.nanstd(xasPeaksData.RowlandY[on]/xasPeaksData.CspadSum[on])/np.sqrt(Num_On[jj])
        

    XASOff_Norm = XASOff/NormFactor_Off
    XASOn_Norm = XASOn/NormFactor_On
    
    XASOn_Norm[np.isinf(XASOn_Norm)] = 0
    XASOn_Norm[np.isnan(XASOn_Norm)] = 0
                
    if ploton:
        
        plt.figure()
        
        for ii in range(NumTTSteps):
            
            plt.plot(XASOn[ii])
        
        plt.plot(XASOff)
        plt.xlabel('x-ray energy (keV)')
        plt.ylabel('x-ray absorption')
        
        plt.figure()
        
        for ii in range(NumTTSteps):

            plt.plot(NormFactor_On[ii])
        
        plt.plot(NormFactor_Off)
        plt.xlabel('x-ray energy (keV)')
        plt.ylabel('x-ray absorption')
            
    return XASOn_Norm, XASOff_Norm, Num_On, Num_Off, Error_On, Error_Off