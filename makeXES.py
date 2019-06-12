# -*- coding: utf-8 -*-
"""
Created on Mon May 13 17:34:21 2019

@author: chelsea
"""

def makeXES(NumTTSteps, Ipm2Sum, RowlandY, Filter, LOn, XOn, TTDelay, TTSteps, ploton):
    
    from itertools import compress
    import matplotlib.pyplot as plt
    
    XESOn = [0 for y in range(NumTTSteps)]
    NormFactor_On = [0 for y in range(NumTTSteps)]
    XESOn_Norm = [0 for y in range(NumTTSteps)]
    Num_On = [0 for y in range(NumTTSteps)]

    off = [not a and b for a,b in zip(LOn, Filter)]
    XESOff = sum(list(compress(RowlandY, off)))

    NormFactor_Off = sum(list(compress(Ipm2Sum, off)))
    Num_Off = sum([int(x) for x in off])
    
    if Num_Off == 0:
        XESOff_Norm = 0
    else:
        XESOff_Norm = XESOff/NormFactor_Off
        
    for ii in range(NumTTSteps):
    
        on = [bool(a) and bool(b) and bool(c >= TTSteps[ii]) and bool(c < TTSteps[ii+1]) and d for a,b,c,d in zip(LOn, Filter, TTDelay, XOn)]
        XESOn[ii] = sum(list(compress(RowlandY, on)))
        
        NormFactor_On[ii] = sum(list(compress(Ipm2Sum, on)))
        Num_On[ii] = sum([int(x) for x in on])
    
        if Num_On[ii] == 0:
            XESOn_Norm[ii] = 0
        else:
            XESOn_Norm[ii] = XESOn[ii]/NormFactor_On[ii]

                
    if ploton:
        
        plt.figure()
        plt.plot(TTSteps[1:],XESOn_Norm)
        plt.plot([TTSteps[1], TTSteps[-1]], [XESOff_Norm, XESOff_Norm])
        plt.xlabel('time')
        plt.ylabel('XES')
        
        plt.figure()
        plt.plot(TTSteps[1:],NormFactor_On)
        plt.xlabel('time')
        plt.ylabel('norm factor')
            
    return XESOn_Norm, XESOff_Norm, Num_On, Num_Off, NormFactor_Off, NormFactor_On