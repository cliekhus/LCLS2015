# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:34:21 2019

@author: chelsea
"""

def makeHERFD(xasRawData, xasProData, ploton):
    
    import math
    from itertools import compress
    import matplotlib.pyplot as plt
    from makeOneFilter import makeOneFilter
    
    NumEnergySteps = len(xasProData.UniXEnergy)
    NumTTSteps = len(xasProData.TTSteps)-1
    
    XASOn = [[0 for x in range(NumEnergySteps)] for y in range(NumTTSteps)]
    XASOff = [0 for x in range(NumEnergySteps)]
    
    NormFactor_On = [[0 for x in range(NumEnergySteps)] for y in range(NumTTSteps)]
    NormFactor_Off = [0 for x in range(NumEnergySteps)]
    
    XASOn_Norm = [[0 for x in range(NumEnergySteps)] for y in range(NumTTSteps)]
    XASOff_Norm = [0 for x in range(NumEnergySteps)]
    
    Num_On = [[0 for x in range(NumEnergySteps)] for y in range(NumTTSteps)]
    Num_Off = [0 for x in range(NumEnergySteps)]
    
    NanCheck = [not math.isnan(a) and not math.isnan(b) for a,b in zip(xasRawData.RowlandY, xasRawData.Ipm2Sum)]
    
    for jj in range(NumEnergySteps):

        SelectedRuns = list(a and b and c for a,b,c in zip(xasRawData.XOn, (xasProData.XEnergy == xasProData.UniXEnergy[jj]), NanCheck))
        
        ffilter, Offset = makeOneFilter(xasRawData, SelectedRuns, ploton, 1)
        
        SelectedRuns = [a and b for a,b in zip(SelectedRuns, ffilter)]
        
        off = list(not a and b for a,b in zip(xasRawData.LOn, SelectedRuns))
        XASOff[jj] = sum(list(compress(xasRawData.RowlandY, off)))

        NormFactor_Off[jj] = sum(list(compress(xasRawData.Ipm2Sum, off)))
        Num_Off[jj] = sum([int(x) for x in off])
        

        
        if NormFactor_Off[jj] == 0:
            XASOff_Norm[jj] = 0
        else:
            XASOff_Norm[jj] = XASOff[jj]/NormFactor_Off[jj]
        
        for ii in range(NumTTSteps):
            
            on = list(bool(a and b and c and d) for a,b,c,d in zip(xasRawData.LOn, SelectedRuns, \
                      (xasProData.TTDelay > xasProData.TTSteps[ii]), (xasProData.TTDelay <= xasProData.TTSteps[ii+1])))
            XASOn[ii][jj] = sum(list(compress(xasRawData.RowlandY, on)))

            NormFactor_On[ii][jj] = sum(list(compress(xasRawData.Ipm2Sum, on)))
            Num_On[ii][jj] = sum([int(x) for x in on])
            
            if NormFactor_On[ii][jj] == 0:
                XASOn_Norm[ii][jj] = 0
            else:
                XASOn_Norm[ii][jj] = XASOn[ii][jj]/NormFactor_On[ii][jj]
    
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