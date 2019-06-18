# -*- coding: utf-8 -*-
"""
Created on Tue May 21 09:55:23 2019

@author: chelsea
"""

def makeConversion(UniqueAnglep, SpectraOff, ploton):
    
    import numpy as np
    import h5py
    from fittingfunctions import lorwoffset
    from scipy.optimize import curve_fit
    import matplotlib.pyplot as plt
    
    APSName = h5py.File('D:\LCLS_Data\APS\APS_Aug_2015_Fesamples.mat')
    
    FeRuXES = np.array(APSName['/FeRu_XES'])
    FeRuXESSignal = FeRuXES[1][410:600]
    FeRuXESEnergy = FeRuXES[0][410:600]
    
    APSparams,cov = curve_fit(lorwoffset, FeRuXESEnergy, FeRuXESSignal, p0 = [0.004, 6.404, 5000, 257000, -40000])
    
    if ploton:
            
        plt.figure()
        plt.plot(FeRuXESEnergy, FeRuXESSignal)
        plt.plot(FeRuXESEnergy, lorwoffset(FeRuXESEnergy, APSparams[0], APSparams[1], APSparams[2], APSparams[3], APSparams[4]))
        plt.xlabel('keV')
        plt.ylabel('APS signal')
    
    LCLSparams,cov = curve_fit(lorwoffset, UniqueAnglep, SpectraOff, p0 = [0.07,76.56,300000,0,0])
    
    if ploton:
            
        plt.figure()
        plt.plot(UniqueAnglep, SpectraOff)
        plt.plot(UniqueAnglep, lorwoffset(UniqueAnglep, LCLSparams[0], LCLSparams[1], LCLSparams[2], LCLSparams[3], LCLSparams[4]))
        plt.xlabel('keV')
        plt.ylabel('LCLS signal')
    
    slope = APSparams[0]/LCLSparams[0]
    x0 = APSparams[1]-slope*LCLSparams[1]
    
    LCLSEnergy = [xx*slope+x0 for xx in UniqueAnglep]
    
    if ploton:
        plt.figure()
        line1 = plt.plot(FeRuXESEnergy, [x/max(FeRuXESSignal) for x in FeRuXESSignal])
        line2 = plt.plot(LCLSEnergy, [x/max(SpectraOff) for x in SpectraOff])
        plt.legend((line1[0], line2[0]), ('APS', 'LCLS'))
    
    return LCLSEnergy, slope, x0

def convertAngle2Energy(slope, x0, Angle):
    
    if len(Angle) > 1:
        return [xx*slope+x0 for xx in Angle]
    else:
        return Angle*slope+x0