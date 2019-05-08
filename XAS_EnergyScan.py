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

NumTTSteps = 20
NumTTStepsPlots = 2

if ReEnterData:

    FileNums = list(range(373,373+1))
    XOn, LOn, XEnergyRaw, Diode2, Ipm2Sum, Ipm2Median, Ipm2STD, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, ScanNum, RowlandY = loadData(FileNums)

Filter = makeFilter(Ipm2Sum, Ipm2Median, Ipm2STD, Diode2, XOn, LOn, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, FPlots)

#t0 = find_t0_XAS(XOn, LOn, XEnergyRaw, TimeTool, Ipm2Sum, RowlandY, Filter, True)

t0 = -50

TTDelay = [x*1000 - t0 for x in TimeTool]
#TTSteps = np.array([float(-500), float(0), float(500)])
TTSteps = np.linspace(-1000,1000,NumTTSteps+1)

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

#fig = plt.figure()

XASOn_Norm = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]

AtleastOne = [x > 0 for x in Off_NumScan]

for ii in range(NumTTSteps):
    AtleastOne = [a and sum(b) > 0 for a,b in zip(AtleastOne, On_NumScan[ii])]

LegendLabel = []

for ii in range(NumTTSteps):

    XASOn_Norm[ii] = [a/b for a,b,c in zip(XASOn[ii], NormFactor_On[ii], AtleastOne) if c]
    #XASOn_Norm[ii] = [a/b for a,b,c in zip(XASOn[ii], On_NumScan[ii], AtleastOne) if c]
    LegendLabel = LegendLabel + plt.plot(list(compress(UniXEnergy, AtleastOne)), XASOn_Norm[ii])
    
#plt.xlabel('x-ray energy (keV)')
#plt.ylabel('x-ray absorption')

XASOff_Norm = [a/b for a,b,c in zip(XASOff, NormFactor_Off, AtleastOne) if c]

OutEnergy = list(compress(UniXEnergy, [x > 0 for x in AtleastOne]))

XASDiff = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]
for ii in range(len(TTSteps)-1):
    XASDiff[ii] = [a - b for a,b in zip(XASOn_Norm[ii], XASOff_Norm)]

"""
LegendLabel = LegendLabel + plt.plot(list(compress(UniXEnergy, AtleastOne)), XASOff_Norm)
plt.xlabel('x-ray energy (keV)')
plt.ylabel('x-ray absorption')

LegendWords = []
for ii in range(NumTTStepsPlots):
    LegendWords = LegendWords + [str(round(TTSteps[ii],0)) + ' to ' + str(round(TTSteps[ii+1],0)) + ' fs delay']

LegendWords = LegendWords + ['Off']

plt.legend(LegendLabel, LegendWords)

LegendLabel = []
plt.figure()
for ii in range(NumTTStepsPlots):
    
    LegendLabel = LegendLabel + plt.plot(list(compress(UniXEnergy, [x > 0 and y > 0 for x,y in zip(On_NumScan[ii], AtleastOne)])), [a - b for a,b in zip(XASOn_Norm[ii], XASOff_Norm)], marker='.')
    #plt.plot(UniXEnergy, [a/sum(XESOn[ii]) - b/sum(XESOff) for a,b, in zip(XESOn[ii], XESOff)])
    
plt.xlabel('x-ray energy (keV)')
plt.ylabel('difference in x-ray absorption (on-off)')

LegendWords.pop()

plt.legend(LegendLabel, LegendWords)

"""