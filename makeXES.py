# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:34:21 2019

@author: chelsea
"""

def makeXES(NumEnergySteps, NumTTSteps, Ipm2Sum, RowlandY, UniXEnergy, XEnergy, Filter, LOn, XOn, TTDelay, TTSteps, ploton):

    from itertools import compress
    import matplotlib.pyplot as plt
    
    XESOn = [[0 for x in range(NumEnergySteps)] for y in range(NumTTSteps)]
    NormFactor_On = [[0 for x in range(NumEnergySteps)] for y in range(NumTTSteps)]
    XESOn_Norm = [[0 for x in range(NumEnergySteps)] for y in range(NumTTSteps)]
    Num_On = [[0 for x in range(NumEnergySteps)] for y in range(NumTTSteps)]
    
    off = list(not a and b for a,b in zip(LOn, Filter))
    XESOff = sum(list(compress(RowlandY, off)))

    NormFactor_Off = sum(list(compress(Ipm2Sum, off)))
    Num_Off = sum([int(x) for x in off])
    
    if NormFactor_Off == 0:
        XESOff_Norm = 0
    else:
        XESOff_Norm = [x/NormFactor_Off for x in XESOff]
        #XESOff_Norm = [x/sum(XESOff) for x in XESOff]
        
    for ii in range(NumTTSteps):
    
        on = list(bool(a and b and c and d) for a,b,c,d in zip(LOn, Filter, (TTDelay > TTSteps[ii]), (TTDelay <= TTSteps[ii+1])))
        XESOn[ii] = sum(list(compress(RowlandY, on)))
    
        NormFactor_On[ii] = sum(list(compress(Ipm2Sum, on)))
        Num_On[ii] = sum([int(x) for x in on])
    
        if NormFactor_On[ii] == 0:
            XESOn_Norm[ii] = [0 for x in range(len(XESOff_Norm))]
        else:
            XESOn_Norm[ii] = [x/NormFactor_On[ii] for x in XESOn[ii]]
            #XESOn_Norm[ii] = [x/sum(XESOn[ii]) for x in XESOn[ii]]
            
    EnergyPlot = UniXEnergy
                
    if ploton:
        
        plt.figure()
        
        for ii in range(NumTTSteps):
            
            plt.plot(XESOn[ii])
        plt.xlabel('x-ray energy (keV)')
        plt.ylabel('x-ray emission on')
        
        plt.figure()
        plt.plot(XESOff)
        plt.xlabel('x-ray energy (keV)')
        plt.ylabel('x-ray emission off')
        
        plt.figure()
        plt.plot(NormFactor_On)
        plt.xlabel('time')
        plt.ylabel('norm factor')
            
    return XESOn_Norm, XESOff_Norm, EnergyPlot, Num_On, Num_Off, NormFactor_Off, NormFactor_On