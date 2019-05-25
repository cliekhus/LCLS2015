# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:34:43 2019

@author: chelsea
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import compress
from makeFilter import makeFilter
from find_t0 import find_t0_XES
from loadData import loadData
from scipy.signal import savgol_filter
from makeXES import makeXES
from APSXESCalibration import convertPixel2Energy
import math

ReEnterData = False
FPlots = False

NumTTSteps = 10
NumTTStepsPlots = 50

if ReEnterData:

    FileNums = [180, 182,183]
    #FileNums = list(range(123,124+1))
    XOn, LOn, StageDelay, Diode2, Ipm2Sum, Ipm2Median, Ipm2STD, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, ScanNum, RowlandYRaw = loadData(FileNums, False)


UniXEnergy, RowlandY = convertPixel2Energy(RowlandYRaw)
XEnergy = UniXEnergy

#RowlandY = RowlandYRaw

RowlandSum = [sum(x) for x in RowlandYRaw]

Filter = makeFilter(Diode2, Ipm2Sum, Ipm2Median, Ipm2STD, RowlandSum, XOn, LOn, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, FPlots, False)

TTDelay = [x*1000 + y*1e15 for x,y in zip(TimeTool,StageDelay)]

TTSteps = np.linspace(-160,40,NumTTSteps+1)

NumEnergySteps = len(UniXEnergy)
XESOn_Norm, XESOff_Norm, EnergyPlot, Num_On, Num_Off, Norm_Off, Norm_On = makeXES(NumEnergySteps, NumTTSteps, Diode2, RowlandY, UniXEnergy, XEnergy, Filter, LOn, XOn, TTDelay, TTSteps, FPlots)

NumEnergySteps = len(UniXEnergy)


plt.figure()
plt.plot(EnergyPlot, XESOff_Norm, marker='.', label=str('off'))
for ii in range(NumTTSteps):
    plt.plot(EnergyPlot, XESOn_Norm[ii], marker='.', label = str(TTSteps[ii]))




XESDiff = [[0 for x in range(NumEnergySteps)] for y in range(NumTTSteps)]

Peak1 = []
Peak2 = []

plt.figure()
for ii in range(NumTTSteps):
    xesdiff = [a - b for a,b in zip(XESOn_Norm[ii], XESOff_Norm)]
    XESDiff[ii] = xesdiff
    if Num_On[ii]>0:
        filteredxes = savgol_filter(xesdiff, 5, 3)
        #filteredxes = xesdiff
        plt.plot(EnergyPlot, filteredxes, marker='.', label = str(TTSteps[ii]))
        Peak1 = Peak1 + [sum(compress(filteredxes, [x<=74 and x>=70 for x in EnergyPlot]))]
        Peak2 = Peak2 + [sum(compress(filteredxes, [x<=80 and x>=76 for x in EnergyPlot]))]
        
plt.legend()

plt.figure()
plt.plot(TTSteps[1:], Peak1, marker='o')
plt.plot(TTSteps[1:], Peak2, marker='o')
#t0 = find_t0_XES(TTSteps, Peak1, True)
"""
TTSteps = np.linspace(-2000,2000,NumTTStepsPlots+1)

XESOn_Norm_t0, XESOff_Norm_t0, EnergyPlot, Num_On, Num_Off = makeXES(NumEnergySteps, NumTTSteps, Ipm2Sum, RowlandY, UniXEnergy, XEnergy, Filter, LOn, XOn, TTDelay-t0, TTSteps, Diode2, FPlots)







TTDelayPlot = []

XESDiffPlot = [[0 for x in range(NumEnergySteps)] for y in range(NumTTStepsPlots)]
XESDiffError = [[0 for x in range(NumEnergySteps)] for y in range(NumTTStepsPlots)]

for ii in range(NumTTStepsPlots):
    for jj in range(NumEnergySteps):
        XESDiffPlot[ii][jj] = XESOn_Norm_t0[ii][jj] - XESOff_Norm_t0[jj]
        if Num_On[ii][jj] > 0 or Num_Off[jj] > 0:
            XESDiffError[ii][jj] = XESDiffPlot[ii][jj]*(math.sqrt(1/Num_On[ii][jj]+1/Num_Off[jj]))
        else:
            XESDiffError[ii][jj] = 0







LegendLabel = []
fig = plt.figure()

for ii in range(NumTTStepsPlots):
    
    LegendLabel = LegendLabel + plt.plot(EnergyPlot, savgol_filter(XESDiffPlot[ii],7,2), marker='.')

plt.xlabel('x-ray energy (keV)')
plt.ylabel('change in x-ray absorption')

LegendWords = []
for ii in range(NumTTStepsPlots):
    LegendWords = LegendWords + [str(round(TTSteps[ii],0)) + ' to ' + str(round(TTSteps[ii+1])) + ' fs delay']

plt.legend(LegendLabel, LegendWords)





LegendLabel = []
fig = plt.figure()

for ii in range(NumTTStepsPlots):
    
    plt.errorbar(EnergyPlot, savgol_filter(XESDiffPlot[ii],7,2), XESDiffError[ii], marker='.', label = str(round(TTSteps[ii],0)) + ' to ' + str(round(TTSteps[ii+1])) + ' fs delay')

plt.xlabel('x-ray energy (keV)')
plt.ylabel('change in x-ray absorption')
plt.legend()



print(EnergyShift)
print(t0)
"""