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
from scipy.signal import savgol_filter
from APSXASCalibration import findEnergyShift
import ProcessedDataClass as PDC
import pickle

ReEnterData = False
FPlots = False
ReLoadData = False
SaveData = False
folder = "D://LCLS_Data/LCLS_python_data/XAS/"

DorH = True #True is diode, False is HERFD



NumTTSteps = 40
NumTTStepsPlots = 5

if ReEnterData:

    FileNums = list(range(372, 395+1))
    #FileNums = list(range(371,373+1))+list(range(375,377+1))+list(range(379,382+1))+list(range(384,391+1))+list(range(393,394+1))
    #FileNums = list(range(372, 374+1))
    xasRawData = loadData(FileNums, True, 1)


if ReLoadData:

    with open(folder + "xasRawData.pkl", "rb") as f:
        xasRawData = pickle.load(f)

xasProData = PDC.XASProcessedData(TTSteps = np.linspace(-200,100,NumTTSteps+1), TTDelay = 1000*xasRawData.TimeTool, \
                              XEnergy = np.round(xasRawData.XEnergyRaw*500,1)*2)
uniXEnergy = np.unique(xasProData.XEnergy)
xasProData.changeValue(UniXEnergy = uniXEnergy[np.logical_and(uniXEnergy >= 7108, uniXEnergy <= 7120)])
xasProData.makeProXAS(xasRawData, DorH, FPlots)







XASDiff = np.empty((NumTTSteps, len(xasProData.UniXEnergy)))
Peak = np.empty(NumTTSteps)

for ii in range(NumTTSteps):
    xasdiff = xasProData.XASOn_Norm[ii] - xasProData.XASOff_Norm
    XASDiff[ii,:] = xasdiff
    peakchoice = np.logical_and(xasProData.EnergyPlot >= np.float64(7114.5), xasProData.EnergyPlot <= np.float64(7117.5))
    Peak[ii] = sum(xasdiff[peakchoice])/sum(xasProData.XASOff_Norm[peakchoice])

t0 = find_t0_XAS(xasProData.TTSteps, Peak, True)
EnergyShift = findEnergyShift(xasProData.XASOff_Norm, xasProData.UniXEnergy, True)
EnergyShift = 1







xasProData_t0 = PDC.XASProcessedData(TTSteps = np.linspace(-150,100,NumTTStepsPlots+1), TTDelay = 1000*xasRawData.TimeTool-t0, \
                              XEnergy = np.round((xasRawData.XEnergyRaw+EnergyShift/1000)*200,1)*5)
uniXEnergy = np.unique(xasProData_t0.XEnergy)
xasProData_t0.changeValue(UniXEnergy = uniXEnergy[np.logical_and(uniXEnergy >= 7110, uniXEnergy <= 7120)])
xasProData_t0.makeProXAS(xasRawData, DorH, FPlots)


XASDiffPlot = np.empty((NumTTStepsPlots, len(xasProData_t0.UniXEnergy)))
XASDiffError = np.empty((NumTTStepsPlots, len(xasProData_t0.UniXEnergy)))
PeakA = np.empty(NumTTStepsPlots)
PeakB = np.empty(NumTTStepsPlots)
PeakC = np.empty(NumTTStepsPlots)
Times = np.empty(0)

for ii in range(NumTTStepsPlots):
    
    xasdiff = xasProData_t0.XASOn_Norm[ii] - xasProData_t0.XASOff_Norm
    XASDiffPlot[ii,:] = xasdiff
    xasdifferror = np.sqrt((np.square(xasProData_t0.Error_On[ii,:])+np.square(xasProData_t0.Error_Off))/np.square(xasProData_t0.XASOff_Norm)+np.square(xasProData_t0.Error_Off)*np.square(xasdiff)/np.square(np.square(xasProData_t0.XASOff_Norm)))
    XASDiffError[ii,:] = xasdifferror
    
    peakchoiceA = np.logical_and(xasProData_t0.EnergyPlot >= np.float64(7111), xasProData_t0.EnergyPlot <= np.float64(7111.5))
    PeakA[ii] = sum(xasdiff[peakchoiceA])/sum(xasProData_t0.XASOff_Norm[peakchoiceA])
    peakchoiceB = np.logical_and(xasProData_t0.EnergyPlot >= np.float64(7113.5), xasProData_t0.EnergyPlot <= np.float64(7114.5))
    PeakB[ii] = sum(xasdiff[peakchoiceB])/sum(xasProData_t0.XASOff_Norm[peakchoiceB])
    peakchoiceC = np.logical_and(xasProData_t0.EnergyPlot >= np.float64(7116), xasProData_t0.EnergyPlot <= np.float64(7117.5))
    PeakC[ii] = sum(xasdiff[peakchoiceC])/sum(xasProData_t0.XASOff_Norm[peakchoiceC])
    Times = np.append(Times,(xasProData_t0.TTSteps[ii]+xasProData_t0.TTSteps[ii+1])/2)
    
XASDiffError[np.isnan(XASDiffError)] = 0


fig = plt.figure()

for ii in range(NumTTStepsPlots):
    
    plt.plot(xasProData_t0.EnergyPlot, XASDiffPlot[ii]/xasProData_t0.XASOff_Norm, marker='.', label = str(round(xasProData_t0.TTSteps[ii],0)) + ' to ' + str(round(xasProData_t0.TTSteps[ii+1])) + ' fs delay')

plt.xlabel('x-ray energy (eV)')
plt.ylabel('change in x-ray absorption')
plt.legend()

fig = plt.figure()
plt.plot(Times, PeakA, label = "Peak A, 7111 - 7111.5 eV")
plt.plot(Times, PeakB, label = "Peak B, 7113.5 - 7114.5 eV")
plt.plot(Times, PeakC, label = "Peak C, 7116 - 7117.5 eV")
plt.xlabel('time delay (fs)')
plt.legend()





xasProData_one = PDC.XASProcessedData(TTSteps = np.linspace(-50,100,1+1), TTDelay = 1000*xasRawData.TimeTool-t0, \
                              XEnergy = np.round((xasRawData.XEnergyRaw+EnergyShift/1000)*200,1)*5)
uniXEnergy = np.unique(xasProData_one.XEnergy)
xasProData_one.changeValue(UniXEnergy = uniXEnergy[np.logical_and(uniXEnergy >= 7110, uniXEnergy <= 7120)])
xasProData_one.makeProXAS(xasRawData, DorH, FPlots)

XASDiffPlot = np.empty((NumTTStepsPlots, len(xasProData_one.UniXEnergy)))
XASDiffError = np.empty((NumTTStepsPlots, len(xasProData_one.UniXEnergy)))

for ii in range(1):
    
    xasdiff = xasProData_one.XASOn_Norm[ii] - xasProData_one.XASOff_Norm
    XASDiffPlot[ii,:] = xasdiff
    xasdifferror = np.sqrt((np.square(xasProData_one.Error_On[ii,:])+np.square(xasProData_one.Error_Off))/np.square(xasProData_one.XASOff_Norm)+np.square(xasProData_one.Error_Off)*np.square(xasdiff)/np.square(np.square(xasProData_one.XASOff_Norm)))
    XASDiffError[ii,:] = xasdifferror
    
XASDiffError[np.isnan(XASDiffError)] = 0


fig = plt.figure()

plt.plot(xasProData_one.EnergyPlot, xasProData_one.XASOn_Norm[0], marker='.', label = str(round(xasProData_one.TTSteps[ii],0)) + ' to ' + str(round(xasProData_one.TTSteps[ii+1])) + ' fs delay')

plt.plot(xasProData_one.EnergyPlot, xasProData_one.XASOff_Norm, marker='.', label = 'laser off')
plt.xlabel('x-ray energy (eV)')
plt.ylabel('x-ray absorption')
plt.legend()


LegendLabel = []
fig = plt.figure()

#    plt.errorbar(xasProData_one.EnergyPlot, savgol_filter(XASDiffPlot[ii]/xasProData_one.XASOff_Norm,5,2), XASDiffError[ii], \
#                 marker='.', label = str(round(xasProData_one.TTSteps[ii],0)) + ' to ' + str(round(xasProData_one.TTSteps[ii+1])) + ' fs delay')

plt.errorbar(xasProData_one.EnergyPlot, XASDiffPlot[ii]/xasProData_one.XASOff_Norm, XASDiffError[ii], \
             marker='.', label = str(round(xasProData_one.TTSteps[ii],0)) + ' to ' + str(round(xasProData_one.TTSteps[ii+1])) + ' fs delay')

plt.xlabel('x-ray energy (eV)')
plt.ylabel('change in x-ray absorption')
plt.legend()



if SaveData:
        
    with open(folder + "xasRawData.pkl", "wb") as f:
        pickle.dump(xasRawData, f)
            
    with open(folder + "xasProData.pkl", "wb") as f:
        pickle.dump(xasProData, f)

