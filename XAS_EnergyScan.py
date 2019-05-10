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
import math
from makeFilter import makeFilter
from find_t0_XAS import find_t0_XAS
from loadData import loadData

ReEnterData = False
FPlots = False

#Set up the scans and the number of time steps

NumTTSteps = 3
NumTTStepsPlots = 2

if ReEnterData:

    FileNums = list(range(373,373+1))
    XOn, LOn, XEnergyRaw, Diode2, Ipm2Sum, Ipm2Median, Ipm2STD, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, ScanNum, RowlandY = loadData(FileNums)

Filter = makeFilter(Ipm2Sum, Ipm2Median, Ipm2STD, Diode2, XOn, LOn, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, FPlots)

#t0 = find_t0_XAS(XOn, LOn, XEnergyRaw, TimeTool, Ipm2Sum, RowlandY, Filter, True)

t0 = -50

TTDelay = [x*1000 - t0 for x in TimeTool]
#TTSteps = np.array([float(-500), float(0), float(500)])
TTSteps = np.linspace(-100,100,NumTTSteps+1)

#Make XAS spectra
XEnergy = [round(x,5)*1000+.75 for x in XEnergyRaw]
#XEnergy = XEnergyRaw
UniXEnergy = np.unique(XEnergy)
#UniXEnergy = np.linspace(min(XEnergy), max(XEnergy), )

XASOn = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]
XASOff = [0 for x in range(len(UniXEnergy))]

On_NumScan = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]
Off_NumScan = [0 for x in range(len(UniXEnergy))]

NormFactor_On = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]
NormFactor_Off = [0 for x in range(len(UniXEnergy))]

NanCheck = [not a and not b for a,b in zip([math.isnan(x) for x in Diode2], [math.isnan(x) for x in Ipm2Sum])]

for jj in range(len(UniXEnergy)):
    
    SelectedRuns = list(a and b and c and d for a,b,c,d in zip(XOn, (XEnergy == UniXEnergy[jj]), NanCheck, Filter))
    
    off = list(not a and b for a,b in zip(LOn, SelectedRuns))
    XASOff[jj] = sum(list(compress(Diode2, off)))
    
    Off_NumScan[jj] = sum([int(x) for x in off])
    NormFactor_Off[jj] = sum(list(compress(Ipm2Sum, off)))
    
    for ii in range(len(TTSteps)-1):
        
        on = list(bool(a and b and c and d) for a,b,c,d in zip(LOn, SelectedRuns, (TTDelay > TTSteps[ii]), (TTDelay <= TTSteps[ii+1])))
        XASOn[ii][jj] = sum(list(compress(Diode2, on)))
        
        On_NumScan[ii][jj] = sum([int(x) for x in on])
        NormFactor_On[ii][jj] = sum(list(compress(Ipm2Sum, on)))

fig = plt.figure()

XASOn_Norm = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]

LegendLabel = []

for ii in range(NumTTSteps):
    for jj in range(len(UniXEnergy)):
        
        if NormFactor_On[ii][jj] == 0:
            XASOn_Norm[ii][jj] = 0
        else:
            XASOn_Norm[ii][jj] = XASOn[ii][jj]/NormFactor_On[ii][jj]

    LegendLabel = LegendLabel + plt.plot(UniXEnergy, XASOn_Norm[ii])
    
plt.xlabel('x-ray energy (keV)')
plt.ylabel('x-ray absorption')

XASOff_Norm = [0 for x in range(len(UniXEnergy))]

for ii in range(len(UniXEnergy)):
    if NormFactor_Off[ii] == 0:
        XASOff_Norm[ii] = 0
    else:
        XASOff_Norm[ii] = XASOff[ii]/NormFactor_Off[ii]
    
LegendLabel = LegendLabel + plt.plot(UniXEnergy, XASOff_Norm)
plt.xlabel('x-ray energy (keV)')
plt.ylabel('x-ray absorption')

LegendWords = []
for ii in range(NumTTSteps):
    LegendWords = LegendWords + [str(round(TTSteps[ii],0)) + ' to ' + str(round(TTSteps[ii+1],0)) + ' fs delay']

LegendWords = LegendWords + ['Off']

plt.legend(LegendLabel, LegendWords)

XASDiff = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]
for ii in range(len(TTSteps)-1):
    XASDiff[ii] = [a - b for a,b in zip(XASOn_Norm[ii], XASOff_Norm)]


LegendLabel = []
plt.figure()

for ii in range(NumTTSteps):
    
    LegendLabel = LegendLabel + plt.plot(UniXEnergy, XASDiff[ii], marker='.')
    
plt.xlabel('x-ray energy (keV)')
plt.ylabel('difference in x-ray absorption (on-off)')

#LegendWords.pop()

plt.legend(LegendLabel, LegendWords)

