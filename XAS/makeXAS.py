# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:34:21 2019

@author: chelsea
"""

def makeXAS(xasRawData, xasProData, ploton):
    
    import matplotlib.pyplot as plt
    from makeOneFilter import makeOneFilter
    import numpy as np
    
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
    
    NanCheck = np.logical_and(np.isnan(xasRawData.Diode2), np.isnan(xasRawData.Ipm2Sum))
    
    for jj in range(NumEnergySteps):

        SelectedRuns = np.logical_and.reduce((xasRawData.XOn, (xasProData.XEnergy == xasProData.UniXEnergy[jj]), np.logical_not(NanCheck)))
        
        print('makeXAS line 35')
        print(sum(SelectedRuns.astype(int)))
        print(xasProData.UniXEnergy[jj])
        
        ffilter, Offset = makeOneFilter(xasRawData, SelectedRuns, ploton, 1)
        
        SelectedRuns = np.logical_and(SelectedRuns, ffilter)
        
        off = np.logical_and(xasRawData.LOn, SelectedRuns)
        XASOff[jj] = sum(xasRawData.Diode2[off])

        NormFactor_Off[jj] = sum(xasRawData.Ipm2Sum[off])
        Num_Off[jj] = sum(off.astype(int))

        
        for ii in range(NumTTSteps):
            
            on = np.logical_and.reduce((xasRawData.LOn, SelectedRuns, \
                      (xasProData.TTDelay > xasProData.TTSteps[ii]), (xasProData.TTDelay <= xasProData.TTSteps[ii+1])))
            XASOn[ii,jj] = sum(xasRawData.Diode2[on])

            NormFactor_On[ii,jj] = sum(xasRawData.Ipm2Sum[on])
            Num_On[ii,jj] = sum(on.astype(int))
    
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
            
    return XASOn_Norm, XASOff_Norm, EnergyPlot, Num_On, Num_Off