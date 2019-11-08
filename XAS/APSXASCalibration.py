# -*- coding: utf-8 -*-
"""
Created on Thu May  2 15:24:58 2019
@author: chelsea
"""




def findEnergyShift(XASOff, UniXEnergy, ploton):
        
    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.signal as scisig
    import scipy.io
    
    ALSName = scipy.io.loadmat('D:\LCLS_Data\ALS\IronII.mat')
    
    incident_axis = np.array(ALSName['enII'])
    
    ALSXASNorm = np.array(ALSName['datafeII'])
    ALSXASNorm = (ALSXASNorm-min(ALSXASNorm))/np.sum(ALSXASNorm)*100
    fit = np.polyfit(incident_axis.flatten(), ALSXASNorm.flatten(), 3)
    poly = np.poly1d(fit)
    
    UniXEnergy = UniXEnergy[XASOff>0]
    UniXEnergy = np.array(UniXEnergy)
    XASOff = XASOff[XASOff>0]

    XASOff_Norm = (XASOff-min(XASOff))/np.sum(XASOff)*100
    fitData = np.polyfit(UniXEnergy, XASOff_Norm,3)
    polyData = np.poly1d(fitData)
    
    if ploton:
        plt.figure()
        plt.plot(incident_axis, ALSXASNorm, marker='.', label='APS')
        plt.plot(incident_axis, poly(incident_axis), label='APS Fit')
        plt.plot(UniXEnergy, XASOff_Norm, marker = '.', label='LCLS')
        plt.plot(UniXEnergy, polyData(UniXEnergy), label='LCLS Fit')
        
        plt.xlabel('x-ray energy (keV)')
        plt.ylabel('x-ray absorption')
        plt.legend()
    
    Fitted = ALSXASNorm - poly(incident_axis)
    Fitted[np.logical_or(incident_axis > 7118, incident_axis < 7112)] = 0
    pos, pro = scisig.find_peaks(Fitted.flatten(), threshold = 0.028)
    
    FittedData = XASOff_Norm - polyData(UniXEnergy)
    FittedData[np.logical_or(UniXEnergy > 7118, UniXEnergy < 7112)] = 0
    posData, pro = scisig.find_peaks(FittedData, threshold = 0.045)
    
    APSEnergies = list(incident_axis[pos])
    LCLSEnergies = list(UniXEnergy[posData])
    
    EnergyShift = (APSEnergies[0]-LCLSEnergies[-1]+APSEnergies[1]-LCLSEnergies[-2])/2

    
    if ploton:
        plt.figure()
        plt.plot(incident_axis, Fitted, label='ALS')
        plt.plot(incident_axis[pos], Fitted[pos], 'o', label='ALS fit')
        plt.plot(UniXEnergy, FittedData, label='LCLS')
        plt.plot(UniXEnergy[posData], FittedData[posData], 'o', label='LCLS fit')
        plt.legend()
        plt.xlabel('X-ray energy (keV)')
        plt.title(str(EnergyShift) + ' energy shift')
        
        plt.figure()
        plt.plot(incident_axis, ALSXASNorm, label='ALS')
        plt.plot(incident_axis[pos], ALSXASNorm[pos], 'o', label='ALS fit')
        plt.plot(UniXEnergy+EnergyShift, XASOff_Norm, label='LCLS')
        plt.plot(UniXEnergy[posData]+EnergyShift, XASOff_Norm[posData], 'o', label='LCLS fit')
        plt.legend()
        plt.xlabel('X-ray energy (keV)')
        plt.title('with ' + str(EnergyShift) + ' energy shift applied')
    
    return EnergyShift






def findEnergyShiftAPS(XASOff, UniXEnergy, ploton):
        
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
    
    UniXEnergy = UniXEnergy[XASOff>0]
    UniXEnergy = np.array(UniXEnergy)
    XASOff = XASOff[XASOff>0]

    XASOff_Norm = (XASOff-min(XASOff))/np.sum(XASOff)*100
    fitData = np.polyfit(UniXEnergy, XASOff_Norm,3)
    polyData = np.poly1d(fitData)
    
    if ploton:
        plt.figure()
        plt.plot(incident_axis, APSXASNorm, marker='.', label='APS')
        plt.plot(incident_axis, poly(incident_axis), label='APS Fit')
        plt.plot(UniXEnergy, XASOff_Norm, marker = '.', label='LCLS')
        plt.plot(UniXEnergy, polyData(UniXEnergy), label='LCLS Fit')
        
        plt.xlabel('x-ray energy (keV)')
        plt.ylabel('x-ray absorption')
        plt.legend()
    
    Fitted = APSXASNorm - poly(incident_axis)
    pos, pro = scisig.find_peaks(Fitted, threshold = 0.004)
    
    FittedData = XASOff_Norm - polyData(UniXEnergy)
    posData, pro = scisig.find_peaks(FittedData, threshold = 0.01, distance = 15)
    
    APSEnergies = list(incident_axis[pos])
    LCLSEnergies = list(UniXEnergy[posData])
    
    EnergyShift = (APSEnergies[0]-LCLSEnergies[-1]+APSEnergies[1]-LCLSEnergies[-2])/2

    
    if ploton:
        plt.figure()
        plt.plot(incident_axis, Fitted, label='APS')
        plt.plot(incident_axis[pos], Fitted[pos], 'o', label='APS fit')
        plt.plot(UniXEnergy, FittedData, label='LCLS')
        plt.plot(UniXEnergy[posData], FittedData[posData], 'o', label='LCLS fit')
        plt.legend()
        plt.xlabel('X-ray energy (keV)')
        plt.title(str(EnergyShift) + ' energy shift')
    
    return EnergyShift