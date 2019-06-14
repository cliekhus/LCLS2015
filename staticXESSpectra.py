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
FPlots = False

#Set up the scans and the number of time steps


if ReEnterData:

    FileNums = list(range(190,190+1))
    XOn, LOn, Angle, Diode2, Ipm2Sum, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ScanNum, RowlandY, RowOffset = loadData(FileNums, False, 2)

RowlandWOffset = [x-y for x,y in zip(RowlandY, RowOffset)]
#RowlandWOffset = RowlandY
UniqueAngle = np.unique(Angle)

SpectraOn = []
SpectraOff = []

ii = 0

for uangle in UniqueAngle:
    
    selectAngle = [x == uangle for x in Angle]
    ii = ii+1
    if ii%6 == 1:
        FPlots = False

    rowlandwoffset = list(compress(RowlandWOffset, selectAngle))
    diode2 = list(compress(Diode2, selectAngle))
    timetool = list(compress(TimeTool, selectAngle))


    Filter, Offset = makeFilter(list(compress(Diode2, selectAngle)), list(compress(Ipm2Sum, selectAngle)), rowlandwoffset, \
                                list(compress(XOn, selectAngle)), list(compress(LOn, selectAngle)), list(compress(DiodeIpmSlope, selectAngle)), \
                                list(compress(TimeTool, selectAngle)), list(compress(TTAmp, selectAngle)), list(compress(TTFWHM, selectAngle)), \
                                FPlots, list(compress(ScanNum, selectAngle)), 2)
    
    diode2 = [x-Offset for x in diode2]
    
    Filteroff = [x and y and not z for x,y,z in zip(Filter, XOn, LOn)]
    Filteron = [(w < .01) and (w > -.01) and x and y and z for w,x,y,z in zip(timetool, Filter, XOn, LOn)]
    

    SpectraOn = SpectraOn + [sum(list(compress(rowlandwoffset, Filteroff)))/sum(list(compress(diode2, Filteroff)))]
    SpectraOff = SpectraOff + [sum(list(compress(rowlandwoffset, Filteron)))/sum(list(compress(diode2, Filteron)))]

    if ii%6 == 1:
        FPlots = False
        
plt.figure()
plt.plot(UniqueAngle, SpectraOn)
plt.plot(UniqueAngle, SpectraOff)

plt.figure()
plt.plot(UniqueAngle, [x-y for x,y in zip(SpectraOn, SpectraOff)])
























