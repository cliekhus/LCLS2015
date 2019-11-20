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
from fitXASDiff import fitXASDiff
from fitXASDiff import fitXASPiecewiseDiff
from fitXASDiff import fitXASPiecewiseLor
from fitXASDiff import fitXASPiecewiseGauss
from fittingfunctions import lorwslope
import matplotlib.gridspec as gridspec
from scipy import signal
import scipy.stats as ss
from fittingfunctions import lorwoff
import random

ReEnterData = False
FPlots = False
ReLoadData = False
SaveData = False
Redot0 = False
Boot = False
numBoot = 1000
folder = "D://LCLS_Data/LCLS_python_data/XAS_Spectra/"

DorH = False #True is diode, False is HERFD


  
NumTTSteps = 40
MinTime = -15
MaxTime = 30

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



else:

    with open(folder + "xasProData.pkl", "rb") as f:
        xasProData = pickle.load(f)
        
    with open(folder + "xasProData_one.pkl", "rb") as f:
        xasProData_one = pickle.load(f)
        
    with open(folder + "t0.pkl", "rb") as f:
        t0 = pickle.load(f)






EnergyShift = findEnergyShift(xasProData.XASOff_Norm, xasProData.UniXEnergy, FPlots)






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
    
    xasProData_boot = xasProData_one
    
    XASDiffBoot = np.empty((np.shape(xasProData_one.EnergyPlot)[0],numBoot))
    
    TT = np.matlib.repmat(True,1,int((np.shape(xasRawData.XOn)[0])/2))
    FF = np.matlib.repmat(False,1,int((np.shape(xasRawData.XOn)[0])/2))
    TF = np.concatenate((TT,FF))

    TF = TF.flatten()    
    for ii in range(numBoot):

        random.shuffle(TF)  
        
        xasProData_boot.makeBootXAS(xasRawData, DorH, TF, FPlots)
        
        XASDiffBoot[:,ii] = xasProData_boot.XASOn_Norm[0,:] - xasProData_boot.XASOff_Norm
    
    XASDiffBootF = np.mean(XASDiffBoot,1)
    XASDiffBootE = np.std(XASDiffBoot,1)
        
    if True:
        
        plt.figure()
        plt.plot(xasProData_one.EnergyPlot, XASDiffBoot)
        
    plt.figure()
    plt.errorbar(xasProData_one.EnergyPlot, XASDiffBootF, XASDiffBootE)
    
    Fit,Params,ParamsA,ParamsB,cov,info = \
        fitXASPiecewiseLor(xasProData_one.EnergyPlot, XASDiffBootF, xasProData_one.XASOff_Norm, xasProData_one.XASOn_Norm, True)

    with open(folder + "XASDiffBootF.pkl", "wb") as f:
        pickle.dump(XASDiffBootF, f)
        
    with open(folder + "XASDiffBootE.pkl", "wb") as f:
        pickle.dump(XASDiffBootE, f)

else:
    
    with open(folder + "XASDiffBootF.pkl", "rb") as f:
        XASDiffBootF = pickle.load(f)
        
    with open(folder + "XASDiffBootE.pkl", "rb") as f:
        XASDiffBootE = pickle.load(f)
        
    Fit,Params,ParamsA,ParamsB,covA,covB = \
        fitXASPiecewiseGauss(xasProData_one.EnergyPlot, XASDiffBootF, xasProData_one.XASOff_Norm, xasProData_one.XASOn_Norm, True)

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