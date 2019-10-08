# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:34:21 2019

@author: chelsea
"""

def makeXAS(xasRawData, xasProData, DorH, ploton):
    
    import matplotlib.pyplot as plt
    from makeOneFilter import makeOneFilter
    import numpy as np
    from makeIntensityFilter import makeOneDiodeFilter
    
    NumEnergySteps = len(xasProData.UniXEnergy)
    NumTTSteps = len(xasProData.TTSteps)-1
    
    XASOn = np.empty((NumTTSteps, NumEnergySteps))
    XASOff = np.empty(NumEnergySteps)
    
    NormFactor_On = np.empty((NumTTSteps, NumEnergySteps))
    NormFactor_Off = np.empty(NumEnergySteps)
    
    XASOn_Norm = np.empty((NumTTSteps, NumEnergySteps))
    XASOff_Norm = np.empty(NumEnergySteps)
    
    Num_On = np.empty((NumTTSteps, NumEnergySteps))
    Num_Off = np.empty(NumEnergySteps)
    
    Error_On = np.empty((NumTTSteps, NumEnergySteps))
    Error_Off = np.empty(NumEnergySteps)
    
    
    AllFilter, TTFilter = makeOneFilter(xasRawData, ploton)
    
    for jj in range(NumEnergySteps):

        selectedRuns = np.logical_and(AllFilter, xasProData.XEnergy == xasProData.UniXEnergy[jj])

        DiodeFilter, Offset = makeOneDiodeFilter(xasRawData, selectedRuns, ploton)
        
        off = np.logical_and.reduce((np.logical_not(xasRawData.LOn), selectedRuns, DiodeFilter))
        
        NormFactor_Off[jj] = sum(xasRawData.CspadSum[off])
        Num_Off[jj] = sum(off.astype(int))
        
        if DorH:
            
            XASOff[jj] = sum(xasRawData.Diode2[off])
            Error_Off[jj] = np.nanstd(xasRawData.Diode2[off]/xasRawData.CspadSum[off])/np.sqrt(Num_Off[jj])

        else:
            
            XASOff[jj] = sum(xasRawData.RowlandY[off])
            Error_Off[jj] = np.nanstd(xasRawData.RowlandY[off]/xasRawData.CspadSum[off])/np.sqrt(Num_Off[jj])
        
        for ii in range(NumTTSteps):
            
            on = np.logical_and.reduce((xasRawData.LOn, selectedRuns, TTFilter, DiodeFilter, \
                      (xasProData.TTDelay > xasProData.TTSteps[ii]), (xasProData.TTDelay <= xasProData.TTSteps[ii+1])))

            NormFactor_On[ii,jj] = sum(xasRawData.CspadSum[on])
            Num_On[ii,jj] = sum(on.astype(int))
            
            if DorH:
                    
                XASOn[ii,jj] = sum(xasRawData.Diode2[on])
                Error_On[ii,jj] = np.nanstd(xasRawData.Diode2[on]/xasRawData.CspadSum[on])/np.sqrt(Num_On[ii,jj])
                
            else:

                XASOn[ii,jj] = sum(xasRawData.RowlandY[on])
                Error_On[ii,jj] = np.nanstd(xasRawData.RowlandY[on]/xasRawData.CspadSum[on])/np.sqrt(Num_On[ii,jj])

    XASOff_Norm = XASOff/NormFactor_Off
    XASOn_Norm = XASOn/NormFactor_On
    
    XASOff_Norm[np.isinf(XASOff_Norm)] = 0
    XASOn_Norm[np.isinf(XASOn_Norm)] = 0
    XASOff_Norm[np.isnan(XASOff_Norm)] = 0
    XASOn_Norm[np.isnan(XASOn_Norm)] = 0
    
    EnergyPlot = xasProData.UniXEnergy
                
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
            
    return XASOn_Norm, XASOff_Norm, EnergyPlot, Num_On, Num_Off, Error_On, Error_Off