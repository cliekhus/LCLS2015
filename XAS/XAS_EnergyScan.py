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
#from makeXAS import makeXAS
from APSXASCalibration import findEnergyShift
import ProcessedDataClass as PDC
import pickle

ReEnterData = False
FPlots = False
ReLoadData = False
SaveData = False
folder = "D://LCLS_Data/LCLS_python_data/XAS/"



NumTTSteps = 20
NumTTStepsPlots = 5

if ReEnterData:

    #FileNums = list(range(372, 395+1))
    #FileNums = list(range(371,373+1))+list(range(375,377+1))+list(range(379,382+1))+list(range(384,391+1))+list(range(393,394+1))
    FileNums = list(range(374, 374+1))
    xasRawData = loadData(FileNums, True, 1)


if ReLoadData:

    with open(folder + "xasRawData.pkl", "rb") as f:
        xasRawData = pickle.load(f)

xasProData = PDC.XASProcessedData(TTSteps = np.linspace(-200,-50,NumTTSteps+1), TTDelay = 1000*xasRawData.TimeTool, \
                              XEnergy = np.round(xasRawData.XEnergyRaw*500,1)*2)
uniXEnergy = np.unique(xasProData.XEnergy)
xasProData.changeValue(UniXEnergy = uniXEnergy[np.logical_and(uniXEnergy >= 7108, uniXEnergy <= 7120)])
xasProData.makeProXAS(xasRawData, FPlots)




XASDiff = np.empty((NumTTSteps, len(xasProData.UniXEnergy)))
Peak = np.empty(NumTTSteps)

for ii in range(NumTTSteps):
    xasdiff = xasProData.XASOn_Norm[ii] - xasProData.XASOff_Norm
    XASDiff[ii,:] = xasdiff
    Peak[ii] = sum(xasdiff[np.logical_and(xasProData.EnergyPlot >= np.float64(7110), xasProData.EnergyPlot <= np.float64(7112))])

t0 = find_t0_XAS(xasProData.TTSteps, Peak, True)
EnergyShift = findEnergyShift(xasProData.XASOff_Norm, xasProData.UniXEnergy, False)




xasProData_t0 = PDC.XASProcessedData(TTSteps = np.linspace(-200-t0,-50-t0,NumTTStepsPlots+1), TTDelay = 1000*xasRawData.TimeTool-t0, \
                              XEnergy = np.round(xasRawData.XEnergyRaw*500,1)*2)
uniXEnergy = np.unique(xasProData.XEnergy)
xasProData_t0.changeValue(UniXEnergy = uniXEnergy[np.logical_and(uniXEnergy >= 7108, uniXEnergy <= 7120)])
xasProData_t0.makeProXAS(xasRawData, FPlots)

#xasProData_t0 = PDC.XASProcessedData(TTSteps = np.linspace(-75,125,NumTTStepsPlots+1), TTDelay = 1000*xasRawData.TimeTool-t0, \
#                              XEnergy = np.round((xasRawData.XEnergyRaw*500+EnergyShift/2),1)*2)
#uniXEnergy = np.unique(xasProData.XEnergy)
#xasProData_t0.changeValue(UniXEnergy = uniXEnergy[np.logical_and(uniXEnergy >= 7109, uniXEnergy <= 7121)])
#
#xasProData_t0.makeProXAS(xasRawData, FPlots)





XASDiffPlot = np.empty((NumTTStepsPlots, len(xasProData_t0.UniXEnergy)))
XASDiffError = np.empty((NumTTStepsPlots, len(xasProData_t0.UniXEnergy)))

for ii in range(NumTTStepsPlots):
    
    xasdiff = xasProData_t0.XASOn_Norm[ii] - xasProData_t0.XASOff_Norm
    XASDiffPlot[ii,:] = xasdiff
    xasdifferror = xasdiff*(np.sqrt(1/xasProData_t0.Num_On[ii,:]+1/xasProData_t0.Num_Off))
    XASDiffError[ii,:] = xasdifferror
    
XASDiffError[np.isnan(XASDiffError)] = 0


fig = plt.figure()

for ii in range(NumTTStepsPlots):
    
    plt.plot(xasProData_t0.EnergyPlot, XASDiffPlot[ii], marker='.', label = str(round(xasProData_t0.TTSteps[ii],0)) + ' to ' + str(round(xasProData_t0.TTSteps[ii+1])) + ' fs delay')


plt.xlabel('x-ray energy (eV)')
plt.ylabel('change in x-ray absorption')
plt.legend()



fig = plt.figure()

for ii in range(NumTTStepsPlots):
    
    plt.plot(xasProData_t0.EnergyPlot, xasProData_t0.XASOn_Norm[ii], marker='.', label = str(round(xasProData_t0.TTSteps[ii],0)) + ' to ' + str(round(xasProData_t0.TTSteps[ii+1])) + ' fs delay')


plt.xlabel('x-ray energy (eV)')
plt.ylabel('x-ray absorption')
plt.legend()




LegendLabel = []
fig = plt.figure()

for ii in range(NumTTStepsPlots):
    
    plt.errorbar(xasProData_t0.EnergyPlot, savgol_filter(XASDiffPlot[ii],5,2), XASDiffError[ii], \
                 marker='.', label = str(round(xasProData_t0.TTSteps[ii],0)) + ' to ' + str(round(xasProData_t0.TTSteps[ii+1])) + ' fs delay')

plt.xlabel('x-ray energy (eV)')
plt.ylabel('change in x-ray absorption')
plt.legend()



if SaveData:
        
    with open(folder + "xasRawData.pkl", "wb") as f:
        pickle.dump(xasRawData, f)
            
    with open(folder + "xasProData.pkl", "wb") as f:
        pickle.dump(xasProData, f)

