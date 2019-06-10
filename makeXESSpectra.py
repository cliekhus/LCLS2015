# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:03:44 2019

@author: chelsea
"""

import numpy as np
from itertools import compress
import matplotlib.pyplot as plt
from makeFilter import makeFilter
from loadData import loadData

ReEnterData = True
FPlots = True

#Set up the scans and the number of time steps

NumTTSteps = 30
NumTTStepsPlots = 3

if ReEnterData:

    FileNums = list(range(190,190+1))
    XOn, LOn, Angle, Diode2, Ipm2Sum, Ipm2Median, Ipm2STD, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, ScanNum, RowlandY = loadData(FileNums, False)

Filter = makeFilter(Diode2, Ipm2Sum, Ipm2Median, Ipm2STD, RowlandY, XOn, LOn, DiodeIpmSlope, DISMedian, DISSTD, TimeTool, TTMedian, TTSTD, TTAmp, TTAmpMedian, TTAmpSTD, TTFWHM, TTFWHMMedian, TTFWHMSTD, FPlots, False)

#Filter = [True for x in Filter]

AngleFilter = list(compress(Angle, Filter))
RowlandYFilter = list(compress(RowlandY, Filter))

UniqueAngle = np.unique(AngleFilter)

Spectra = []

for angle in UniqueAngle:
    
    Spectra = Spectra + [sum(list(compress(RowlandYFilter, [x == angle for x in AngleFilter])))]
    
plt.figure()
plt.plot(UniqueAngle, Spectra)