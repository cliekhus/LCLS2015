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
from makeFilter import makeFilter
from find_t0_XAS import find_t0_XAS
from loadData import loadData
from scipy.signal import savgol_filter
from makeXAS import makeXAS
from APSCalibration import findEnergyShift
import math

ReEnterData = True
FPlots = False

#Set up the scans and the number of time steps

NumTTSteps = 20
NumTTStepsPlots = int(NumTTSteps/5)

if ReEnterData:

    FileNums = list(range(373,395+1))
    XOn, LOn, XEnergyRaw, Diode2, Ipm2Sum, Ipm2Median, Ipm2STD, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, ScanNum, RowlandY = loadData(FileNums)

Filter = makeFilter(Ipm2Sum, Ipm2Median, Ipm2STD, Diode2, XOn, LOn, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, FPlots)

TTDelay = [x*1000 for x in TimeTool]
TTSteps = np.linspace(-200,50,NumTTSteps+1)

XEnergy = [round(x*1000,1) for x in XEnergyRaw]
UniXEnergy = np.unique(list(compress(XEnergy, [x >= 7108 and x <= 7120 for x in XEnergy])))

NumEnergySteps = len(UniXEnergy)
XASOn_Norm, XASOff_Norm, EnergyPlot, Num_On, Num_Off = makeXAS(NumEnergySteps, NumTTSteps, Ipm2Sum, Diode2, UniXEnergy, XEnergy, Filter, LOn, XOn, TTDelay, TTSteps, FPlots)

EnergyShift = findEnergyShift(XASOff_Norm, UniXEnergy, True)
XEnergy = [round(x*1000,1)+EnergyShift for x in XEnergyRaw]
UniXEnergy = np.unique(list(compress(XEnergy, [x >= 7109 and x <= 7121 for x in XEnergy])))
NumEnergySteps = len(UniXEnergy)






XASDiff = [[0 for x in range(NumEnergySteps)] for y in range(NumTTSteps)]

Peak = []

for ii in range(NumTTSteps):
    xasdiff = [a - b for a,b in zip(XASOn_Norm[ii], XASOff_Norm)]
    XASDiff[ii] = xasdiff
    Peak = Peak + [sum(compress(xasdiff, [a and b for a,b in zip((EnergyPlot >= np.float64(7114)), (EnergyPlot <= np.float64(7117)))]))]

t0 = find_t0_XAS(TTSteps, Peak, True)



TTSteps = np.linspace(-40,120,NumTTStepsPlots+1)

XASOn_Norm_t0, XASOff_Norm_t0, EnergyPlot, Num_On, Num_Off = makeXAS(NumEnergySteps, NumTTStepsPlots, Ipm2Sum, Diode2, UniXEnergy, XEnergy, Filter, LOn, XOn, TTDelay-t0, TTSteps, FPlots)







TTDelayPlot = []

XASDiffPlot = [[0 for x in range(NumEnergySteps)] for y in range(NumTTStepsPlots)]
XASDiffError = [[0 for x in range(NumEnergySteps)] for y in range(NumTTStepsPlots)]

for ii in range(NumTTStepsPlots):
    for jj in range(NumEnergySteps):
        XASDiffPlot[ii][jj] = XASOn_Norm_t0[ii][jj] - XASOff_Norm_t0[jj]
        if Num_On[ii][jj] > 0 or Num_Off[jj] > 0:
            XASDiffError[ii][jj] = XASDiffPlot[ii][jj]*(math.sqrt(1/Num_On[ii][jj]+1/Num_Off[jj]))
        else:
            XASDiffError[ii][jj] = 0







LegendLabel = []
fig = plt.figure()

for ii in range(NumTTStepsPlots):
    
    LegendLabel = LegendLabel + plt.plot(EnergyPlot, savgol_filter(XASDiffPlot[ii],7,2), marker='.')

plt.xlabel('x-ray energy (keV)')
plt.ylabel('change in x-ray absorption')

LegendWords = []
for ii in range(NumTTStepsPlots):
    LegendWords = LegendWords + [str(round(TTSteps[ii],0)) + ' to ' + str(round(TTSteps[ii+1])) + ' fs delay']

plt.legend(LegendLabel, LegendWords)





LegendLabel = []
fig = plt.figure()

for ii in range(NumTTStepsPlots):
    
    plt.errorbar(EnergyPlot, savgol_filter(XASDiffPlot[ii],7,2), XASDiffError[ii], marker='.', label = str(round(TTSteps[ii],0)) + ' to ' + str(round(TTSteps[ii+1])) + ' fs delay')

plt.xlabel('x-ray energy (keV)')
plt.ylabel('change in x-ray absorption')
plt.legend()



print(EnergyShift)
print(t0)