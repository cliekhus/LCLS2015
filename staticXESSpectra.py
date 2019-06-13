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

ReEnterData = False
FPlots = True

#Set up the scans and the number of time steps

NumTTSteps = 30
NumTTStepsPlots = 3

if ReEnterData:

    FileNums = list(range(190,190+1))
    XOn, LOn, Angle, Diode2, Ipm2Sum, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ScanNum, RowlandY, RowOffset = loadData(FileNums, False)

RowlandWOffset = [x-y for x,y in zip(RowlandY, RowOffset)]

Filter, Offset = makeFilter(Diode2, Ipm2Sum, RowlandWOffset, XOn, LOn, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, FPlots, ScanNum, 2)

Filter = [True for x in Filter]

AngleFiltered = list(compress(Angle, Filter))
RowlandYFiltered = list(compress(RowlandY, Filter))

UniqueAngle = np.unique(AngleFiltered)

Spectra = []

for angle in UniqueAngle:
    
    Spectra = Spectra + [sum(list(compress(RowlandYFiltered, [x == angle for x in AngleFiltered])))]
    
plt.figure()
plt.plot(UniqueAngle, Spectra)