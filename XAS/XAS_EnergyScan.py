# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:48:43 2019
@author: chelsea
"""
"""
XES energy scan - k beta
"""

import numpy as np
import matplotlib.pyplot as plt
from find_t0 import find_t0_XAS
from loadData import loadData
from APSXASCalibration import findEnergyShift
import ProcessedDataClass as PDC
import pickle
from fitXASDiff import fitXASPiecewiseLor
from fitXASDiff import fitXASPiecewiseGauss
from fittingfunctions import lorwslope
import matplotlib.gridspec as gridspec
from scipy import signal
from MakeRawBoot import MakeRawBoot
import time
import datetime

ReEnterData = True
FPlots = False
ReLoadData = False
SaveData = False
Redot0 = True
Boot = True
numBoot = 1000
folder = "D://LCLS_Data/LCLS_python_data/XAS_Spectra/"

DorH = False #True is diode, False is HERFD


  
NumTTSteps = 25
MinTime = -35
MaxTime = 35

if ReEnterData:
    
    #FileNums = list(range(384, 395+1))
    FileNums = list(range(372, 395+1))
    #FileNums = list(range(371,373+1))+list(range(375,377+1))+list(range(379,382+1))+list(range(384,391+1))+list(range(393,394+1))
    #FileNums = list(range(372, 372+1))
    xasRawData = loadData(FileNums, "XAS", 1)


if ReLoadData:

    with open(folder + "xasRawData.pkl", "rb") as f:
        xasRawData = pickle.load(f)

if Redot0:
        
    xasProData = PDC.XASProcessedData(TTSteps = np.linspace(-200,100,NumTTSteps+1), TTDelay = 1000*xasRawData.TimeTool, \
                                  XEnergy = np.round(xasRawData.XEnergyRaw*1000,1)*1)
    uniXEnergy = np.unique(xasProData.XEnergy)
    xasProData.changeValue(UniXEnergy = uniXEnergy[np.logical_and(uniXEnergy >= 7108, uniXEnergy <= 7120)])
    xasProData.makeProXAS(xasRawData, True, FPlots)
    
    
    
    
    
    
    
    XASDiff = np.empty((NumTTSteps, len(xasProData.UniXEnergy)))
    Peak = np.empty(NumTTSteps)
    
    for ii in range(NumTTSteps):
        xasdiff = xasProData.XASOn_Norm[ii] - xasProData.XASOff_Norm
        XASDiff[ii,:] = xasdiff
        peakchoice = np.logical_and(xasProData.EnergyPlot >= np.float64(7114.5), xasProData.EnergyPlot <= np.float64(7117.5))
        Peak[ii] = sum(xasdiff[peakchoice])/sum(xasProData.XASOff_Norm[peakchoice])
    
    t0 = find_t0_XAS(xasProData.TTSteps, Peak, True, FPlots)
    
    with open(folder + "t0.pkl", "wb") as f:
        pickle.dump(t0, f)
        
    with open(folder + "xasProData.pkl", "wb") as f:
        pickle.dump(xasProData, f)
    


else:
    with open(folder + "xasProData.pkl", "rb") as f:
        xasProData = pickle.load(f)
        
    with open(folder + "t0.pkl", "rb") as f:
        t0 = pickle.load(f)




EnergyShift = findEnergyShift(xasProData.XASOff_Norm, xasProData.UniXEnergy, DorH, False, FPlots)






xasProData_one = PDC.XASProcessedData(TTSteps = np.linspace(MinTime,MaxTime,2), TTDelay = 1000*xasRawData.TimeTool-t0, \
                              XEnergy = np.round((xasRawData.XEnergyRaw+EnergyShift/1000)*500,1)*2)
uniXEnergy = np.unique(xasProData_one.XEnergy)
xasProData_one.changeValue(UniXEnergy = uniXEnergy[np.logical_and(uniXEnergy >= 7110, uniXEnergy <= 7120)])
xasProData_one.makeProXAS(xasRawData, DorH, FPlots)

XASDiffPlot = xasProData_one.XASOn_Norm[0,:] - xasProData_one.XASOff_Norm
XASDiffError = np.sqrt(np.square(xasProData_one.Error_On[0,:])+np.square(xasProData_one.Error_Off))/xasProData_one.XASOff_Norm

                       
fig = plt.figure()

plt.plot(xasProData_one.EnergyPlot, xasProData_one.XASOn_Norm[0,:], marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay')

plt.plot(xasProData_one.EnergyPlot, xasProData_one.XASOff_Norm, marker='.', label = 'laser off')
plt.xlabel('x-ray energy (eV)')
plt.ylabel('x-ray absorption')
plt.legend()





plt.figure(figsize = (4,5))

gridspec.GridSpec(10,1)

ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 3)
plt.errorbar(xasProData_one.EnergyPlot, xasProData_one.XASOff_Norm, xasProData_one.Error_Off, color = 'k')
plt.ylabel('$I_{off}$')
ax.set_xticklabels([])
plt.tight_layout()

ax = plt.subplot2grid((10,1), (3,0), colspan = 1, rowspan = 7)
plt.errorbar(xasProData_one.EnergyPlot, XASDiffPlot/xasProData_one.XASOff_Norm, XASDiffError, \
             marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay')
plt.xlabel('x-ray energy (eV)')
plt.ylabel('$(I_{on}-I_{off})/I_{off}$')
plt.legend()
plt.tight_layout()




plt.figure(figsize = (4,5))

gridspec.GridSpec(10,1)

ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 3)
plt.errorbar(xasProData_one.EnergyPlot, xasProData_one.XASOff_Norm, xasProData_one.Error_Off, color = 'k')
plt.ylabel('$I_{off}$')
ax.set_xticklabels([])
plt.tight_layout()

ax = plt.subplot2grid((10,1), (3,0), colspan = 1, rowspan = 7)
plt.errorbar(xasProData_one.EnergyPlot, signal.savgol_filter(XASDiffPlot/xasProData_one.XASOff_Norm, 5,3), XASDiffError, \
             marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay')
plt.xlabel('x-ray energy (eV)')
plt.ylabel('$(I_{on}-I_{off})/I_{off}$')
plt.legend()
plt.tight_layout()


    

Fit,Params,ParamsP,ParamsDiff,cov,info = fitXASPiecewiseLor(xasProData_one.EnergyPlot, XASDiffPlot, xasProData_one.XASOff_Norm, xasProData_one.XASOn_Norm, True)




if Boot:
    
    XASDiffBoot = np.empty((np.shape(xasProData_one.EnergyPlot)[0],numBoot))
    XASOffBoot = np.empty((np.shape(xasProData_one.EnergyPlot)[0],numBoot))
    XASOnBoot = np.empty((np.shape(xasProData_one.EnergyPlot)[0],numBoot))


    starttime = time.time()
    
    for ii in range(numBoot):

        print(ii)

        xasRawDataBoot = MakeRawBoot(xasRawData)
        
        xasProData_boot = PDC.XASProcessedData(TTSteps = np.linspace(MinTime,MaxTime,2), TTDelay = 1000*xasRawDataBoot.TimeTool-t0, \
                                  XEnergy = np.round((xasRawDataBoot.XEnergyRaw+EnergyShift/1000)*500,1)*2)
        uniXEnergy = np.unique(xasProData_boot.XEnergy)
        xasProData_boot.changeValue(UniXEnergy = uniXEnergy[np.logical_and(uniXEnergy >= 7110, uniXEnergy <= 7120)])
        xasProData_boot.makeProXAS(xasRawDataBoot, DorH, FPlots)
        
        XASDiffBoot[:,ii] = xasProData_boot.XASOn_Norm[0,:] - xasProData_boot.XASOff_Norm
        XASOffBoot[:,ii] = xasProData_boot.XASOff_Norm
        XASOnBoot[:,ii] = xasProData_boot.XASOn_Norm[0,:]
        
        elapsedtime = time.time()-starttime
        print("elapsed time: " + str(datetime.timedelta(seconds=elapsedtime)))
        print(str(datetime.timedelta(seconds=elapsedtime/(ii+1)*(numBoot-ii-1))) + " time left" )
    
    XASDiffBootF = np.mean(XASDiffBoot,1)
    XASDiffBootE = np.std(XASDiffBoot,1)
    XASOffBootF = np.mean(XASOffBoot,1)
    XASOffBootE = np.std(XASOffBoot,1)
    XASOnBootF = np.mean(XASOnBoot,1)
    XASOnBootE = np.std(XASOnBoot,1)
        
    Fit,Params,ParamsA,ParamsB,cov,info = \
        fitXASPiecewiseGauss(xasProData_one.EnergyPlot, XASDiffBootF, XASOffBootF, XASOnBootF, True)
    
    if SaveData:
            
        with open(folder + "XASDiffBoot.pkl", "wb") as f:
            pickle.dump(XASDiffBoot, f)
    
        with open(folder + "XASDiffBootF.pkl", "wb") as f:
            pickle.dump(XASDiffBootF, f)
            
        with open(folder + "XASDiffBootE.pkl", "wb") as f:
            pickle.dump(XASDiffBootE, f)
            
        with open(folder + "XASOffBootF.pkl", "wb") as f:
            pickle.dump(XASOffBootF, f)
            
        with open(folder + "XASOffBootE.pkl", "wb") as f:
            pickle.dump(XASOffBootE, f)
            
        with open(folder + "XASOnBootF.pkl", "wb") as f:
            pickle.dump(XASOnBootF, f)
            
        with open(folder + "XASOnBootE.pkl", "wb") as f:
            pickle.dump(XASOnBootE, f)

else:
    
    #with open(folder + "XASDiffBoot.pkl", "rb") as f:
    #    XASDiffBoot = pickle.load(f)
    
    with open(folder + "XASDiffBootF.pkl", "rb") as f:
        XASDiffBootF = pickle.load(f)
        
    with open(folder + "XASDiffBootE.pkl", "rb") as f:
        XASDiffBootE = pickle.load(f)
        
    with open(folder + "XASOffBootF.pkl", "rb") as f:
        XASOffBootF = pickle.load(f)
        
    with open(folder + "XASOffBootE.pkl", "rb") as f:
        XASOffBootE = pickle.load(f)
        
    with open(folder + "XASOnBootF.pkl", "rb") as f:
        XASOnBootF = pickle.load(f)
        
    with open(folder + "XASOnBootE.pkl", "rb") as f:
        XASOnBootE = pickle.load(f)
        
Fit,Params,ParamsA,ParamsB,covA,covB = \
        fitXASPiecewiseGauss(xasProData_one.EnergyPlot, XASDiffBootF, XASOffBootF, XASOnBootF, True)

pluscolor = '#009E73'
minuscolor = '#0072b2'
pluscolor2 = '#e69f00'

plt.figure(figsize = (4,5))

gridspec.GridSpec(10,1)

ax = plt.subplot2grid((10,1), (0,0), colspan = 1, rowspan = 3)
plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(xasProData_one.XASOff_Norm,-4), np.delete(xasProData_one.Error_Off,-4), color = 'k')
plt.ylabel('$I_{off}$')
ax.set_xticklabels([])
plt.tight_layout()

xA = np.linspace(7110.5, 7113, 1000)
xB = np.linspace(7112.5, 7115, 1000)

ax = plt.subplot2grid((10,1), (3,0), colspan = 1, rowspan = 7)
plt.errorbar(np.delete(xasProData_one.EnergyPlot,-4), np.delete(XASDiffBootF,-4), np.delete(XASDiffBootE,-4), \
             marker='.', label = str(MinTime) + ' to ' + str(MaxTime) + ' fs delay', color = 'k')
plt.plot(xA, lorwslope(xA,ParamsA[0],ParamsA[1],ParamsA[2],ParamsA[3],ParamsA[4]), label = 'A peak fit, ' + str(round(ParamsA[1],1)), linewidth = 5, color = pluscolor2)
plt.plot(xB, lorwslope(xB,ParamsB[0],ParamsB[1],ParamsB[2],ParamsB[3],ParamsB[4]), label = 'B peak fit, ' + str(round(ParamsB[1],1)), linewidth = 5, color = minuscolor)
plt.xlabel('x-ray energy (eV)')
plt.ylabel('$(I_{on}-I_{off})/I_{off}$')
plt.ylim([-300,200])
plt.legend()
plt.tight_layout()

with open(folder + "BmA.pkl", "wb") as f:
    pickle.dump(ParamsB[1]-ParamsA[1], f)
with open(folder + "uncertainty.pkl", "wb") as f:
    pickle.dump(np.sqrt(np.diag(covA)+np.diag(covB)), f)
        

if SaveData:
        
    with open(folder + "xasRawData.pkl", "wb") as f:
        pickle.dump(xasRawData, f)
            
    with open(folder + "xasProData_one.pkl", "wb") as f:
        pickle.dump(xasProData_one, f)
        
    with open(folder + "EnergyShift.pkl", "wb") as f:
        pickle.dump(EnergyShift, f)