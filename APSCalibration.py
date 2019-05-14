# -*- coding: utf-8 -*-
"""
Created on Thu May  2 15:24:58 2019

@author: chelsea
"""
def findEnergyShift(XASOff, UniXEnergy, ploton):
        
    import h5py
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.signal as scisig
    
    APSName = h5py.File('D:\LCLS_Data\APS\APS_Aug_2015_Fesamples.mat')
    
    FeRuRIXS = np.array(APSName['/FeRu_RIXS'])
    
    incident_axis = 1000*np.array(APSName['/Fe_RIXS_incident_axis'])
    emitted_axis = 1000*np.array(APSName['/Fe_RIXS_emitted_axis'])
    xp,yp = np.meshgrid(emitted_axis,incident_axis)
    
    incident_axis = incident_axis[:,0]
    
    if ploton:
        plt.figure()
        plt.pcolor(xp, yp, FeRuRIXS)
        
        plt.figure()
        plt.plot(emitted_axis[0], np.sum(FeRuRIXS, axis=0), marker='.')
        
        plt.xlabel('emitted energy (keV)')
        plt.ylabel('emittance')
    
    APSXASNorm = np.sum(FeRuRIXS, axis = 1)
    APSXASNorm = (APSXASNorm-min(APSXASNorm))/np.sum(APSXASNorm)*100
    fit = np.polyfit(incident_axis, APSXASNorm, 3)
    poly = np.poly1d(fit)
    
    XASOff_Norm = (XASOff-min(XASOff))/sum(XASOff)*100
    fitData = np.polyfit(UniXEnergy, XASOff_Norm,3)
    polyData = np.poly1d(fitData)
    
    if ploton:
        plt.figure()
        plt.plot(incident_axis, APSXASNorm, marker='.')
        plt.plot(incident_axis, poly(incident_axis))
        plt.plot(UniXEnergy, XASOff_Norm, marker = '.')
        plt.plot(UniXEnergy, polyData(UniXEnergy))
        
        plt.xlabel('x-ray energy (keV)')
        plt.ylabel('x-ray absorption')
    
    Fitted = APSXASNorm - poly(incident_axis)
    pos, pro = scisig.find_peaks(Fitted, threshold = 0.0043)
    
    FittedData = XASOff_Norm - polyData(UniXEnergy)
    posData, pro = scisig.find_peaks(FittedData, threshold = 0.03)
    
    if ploton:
        plt.figure()
        plt.plot(incident_axis, Fitted)
        plt.plot(incident_axis[pos], Fitted[pos], 'o')
        plt.plot(UniXEnergy, FittedData)
        plt.plot(UniXEnergy[posData], FittedData[posData], 'o')
    
    APSEnergies = list(incident_axis[pos])
    LCLSEnergies = list(UniXEnergy[posData])
    
    EnergyShift = (APSEnergies[0]-LCLSEnergies[0]+APSEnergies[1]-LCLSEnergies[1])/2
    
    return EnergyShift