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
from itertools import compress
from find_t0 import find_t0_XAS
from loadData import loadData
from scipy.signal import savgol_filter
#from makeXAS import makeXAS
from APSXASCalibration import findEnergyShift
import math
import ProcessedDataClass as PDC
import pickle

ReEnterData = False
FPlots = False
ReLoadData = False
SaveData = False
folder = "D://LCLS_Data/LCLS_python_data/XAS/"



NumTTSteps = 10
NumTTStepsPlots = 4

if ReEnterData:

    #FileNums = list(range(372, 395+1))
    #FileNums = list(range(371,373+1))+list(range(375,377+1))+list(range(379,382+1))+list(range(384,391+1))+list(range(393,394+1))
    FileNums = list(range(372, 372+1))
    xasRawData = loadData(FileNums, True, 1)


if ReLoadData:

    with open(folder + "xasRawData.pkl", "rb") as f:
        xasRawData = pickle.load(f)

xasProData = PDC.XASProcessedData(TTSteps = np.linspace(-200,-50,NumTTSteps+1), TTDelay = [x*1000 for x in xasRawData.TimeTool], \
                              XEnergy = [round(x*500,1)*2 for x in xasRawData.XEnergyRaw])
xasProData.changeValue(UniXEnergy = np.unique(list(compress(xasProData.XEnergy, [x >= 7108 and x <= 7120 for x in xasProData.XEnergy]))))
xasProData.makeProHERFD(xasRawData, FPlots)




XASDiff = [[0 for x in range(len(xasProData.UniXEnergy))] for y in range(NumTTSteps)]
Peak = []

for ii in range(NumTTSteps):
    xasdiff = [a - b for a,b in zip(xasProData.XASOn_Norm[ii], xasProData.XASOff_Norm)]
    XASDiff[ii] = xasdiff
    Peak = Peak + [sum(compress(xasdiff, [a and b for a,b in zip((xasProData.EnergyPlot >= np.float64(7114)), (xasProData.EnergyPlot <= np.float64(7117)))]))]

t0 = find_t0_XAS(xasProData.TTSteps, Peak, True)
EnergyShift = findEnergyShift(xasProData.XASOff_Norm, xasProData.UniXEnergy, False)




xasProData_t0 = PDC.XASProcessedData(TTSteps = np.linspace(-75,125,NumTTStepsPlots+1), TTDelay = [x*1000 - t0 for x in xasRawData.TimeTool], \
                              XEnergy = [round((x+EnergyShift/1000)*1000,1) for x in xasRawData.XEnergyRaw])
xasProData_t0.changeValue(UniXEnergy = np.unique(list(compress(xasProData_t0.XEnergy, [x >= 7109 and x <= 7121 for x in xasProData_t0.XEnergy]))))

xasProData_t0.makeProXAS(xasRawData, FPlots)





TTDelayPlot = []

XASDiffPlot = [[0 for x in range(len(xasProData_t0.UniXEnergy))] for y in range(NumTTStepsPlots)]
XASDiffError = [[0 for x in range(len(xasProData_t0.UniXEnergy))] for y in range(NumTTStepsPlots)]

for ii in range(NumTTStepsPlots):
    for jj in range(len(xasProData_t0.UniXEnergy)):
        XASDiffPlot[ii][jj] = xasProData_t0.XASOn_Norm[ii][jj] - xasProData_t0.XASOff_Norm[jj]
        if xasProData_t0.Num_On[ii][jj] > 0 and xasProData_t0.Num_Off[jj] > 0:
            XASDiffError[ii][jj] = XASDiffPlot[ii][jj]*(math.sqrt(1/xasProData_t0.Num_On[ii][jj]+1/xasProData_t0.Num_Off[jj]))
        else:
            XASDiffError[ii][jj] = 0





LegendLabel = []
fig = plt.figure()

for ii in range(NumTTStepsPlots):
    
    #LegendLabel = LegendLabel + plt.plot(xasProData_t0.EnergyPlot, savgol_filter(XASDiffPlot[ii],7,2), marker='.')
    LegendLabel = LegendLabel + plt.plot(xasProData_t0.EnergyPlot, XASDiffPlot[ii], marker='.')


plt.xlabel('x-ray energy (eV)')
plt.ylabel('change in x-ray absorption')

LegendWords = []
for ii in range(NumTTStepsPlots):
    LegendWords = LegendWords + [str(round(xasProData_t0.TTSteps[ii],0)) + ' to ' + str(round(xasProData_t0.TTSteps[ii+1])) + ' fs delay']

plt.legend(LegendLabel, LegendWords)




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

