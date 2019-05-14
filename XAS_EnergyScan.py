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

ReEnterData = True
FPlots = False

#Set up the scans and the number of time steps

NumTTSteps = 1
NumTTStepsPlots = int(NumTTSteps/1)
#NumEnergySteps = 35

if ReEnterData:

    FileNums = list(range(385,385+1))
    XOn, LOn, XEnergyRaw, Diode2, Ipm2Sum, Ipm2Median, Ipm2STD, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, ScanNum, RowlandY = loadData(FileNums)

Filter = makeFilter(Ipm2Sum, Ipm2Median, Ipm2STD, Diode2, XOn, LOn, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, FPlots)

TTDelay = [x*1000 for x in TimeTool]
TTSteps = np.linspace(-200,100,NumTTSteps+1)

#Make XAS spectra
XEnergy = [round(x*1000,1) for x in XEnergyRaw]
#XEnergy = [round(x,5)*1000+.75 for x in XEnergyRaw]
#XEnergy = XEnergyRaw
UniXEnergy = np.unique(compress(XEnergy, [x >= 7108 and x <= 7120 for x in XEnergy]))
#UniXEnergy = np.linspace(7108, 7120, NumEnergySteps+1)
#UniXEnergy = np.linspace(min(XEnergy), max(XEnergy), )

NumEnergySteps = len(UniXEnergy)

XASOn_Norm, XASOff_Norm, EnergyPlot = makeXAS(NumEnergySteps, NumTTSteps, Ipm2Sum, Diode2, UniXEnergy, XEnergy, Filter, LOn, XOn, TTDelay, TTSteps, False)

XASDiff = [[0 for x in range(NumEnergySteps)] for y in range(NumTTSteps)]

Peak = []

for ii in range(NumTTSteps):
    xasdiff = [a - b for a,b in zip(XASOn_Norm[ii], XASOff_Norm)]
    XASDiff[ii] = xasdiff
    Peak = Peak + [sum(compress(xasdiff, [a and b for a,b in zip((EnergyPlot >= np.float64(7114)), (EnergyPlot <= np.float64(7117)))]))]

t0 = find_t0_XAS(TTSteps, Peak, False)

TTSteps = np.linspace(round(-200-t0,0),round(100-t0,0),NumTTSteps+1)

XASOn_Norm_t0, XASOff_Norm_t0, EnergyPlot = makeXAS(NumEnergySteps, NumTTStepsPlots, Ipm2Sum, Diode2, UniXEnergy, XEnergy, Filter, LOn, XOn, TTDelay-t0, TTSteps, False)

TTDelayPlot = []

XASDiffPlot = [[0 for x in range(NumEnergySteps)] for y in range(NumTTStepsPlots)]

for ii in range(NumTTStepsPlots):
    for jj in range(NumEnergySteps):
        XASDiffPlot[ii][jj] = XASOff_Norm_t0[jj] - XASOn_Norm_t0[ii][jj]


LegendLabel = []
fig = plt.figure()

for ii in range(NumTTStepsPlots):
    
    LegendLabel = LegendLabel + plt.plot(EnergyPlot, savgol_filter(XASDiffPlot[ii],5,4))
    #LegendLabel = LegendLabel + plt.plot(EnergyPlot, XASDiffPlot[ii])
plt.xlabel('x-ray energy (keV)')
plt.ylabel('x-ray absorption')

LegendWords = []
for ii in range(NumTTStepsPlots):
    LegendWords = LegendWords + [str(round(TTSteps[ii],0)) + ' to ' + str(round(TTSteps[ii+1])) + ' fs delay']

plt.legend(LegendLabel, LegendWords)
