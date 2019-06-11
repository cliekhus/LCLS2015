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
from makeXES import makeXES

ReEnterData = False
FPlots = True

NumTTSteps = 50
NumTTStepsPlots = 25

if ReEnterData:

    #FileNums = [155]
    FileNums = list(range(182,188+1))
    XOn, LOn, StageDelay, Diode2, Ipm2Sum, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ScanNum, RowlandY = loadData(FileNums, False)


Filter = makeFilter(Diode2, Ipm2Sum, RowlandY, XOn, LOn, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, FPlots, ScanNum, 2)

TTDelay = [x*1000 + y*1e15 for x,y in zip(TimeTool,StageDelay)]

TTSteps = np.linspace(-1000,100,NumTTSteps+1)

XESOn_Norm, XESOff_Norm, Num_On, Num_Off, NormFactor_Off, NormFactor_On = makeXES(NumTTSteps, Ipm2Sum, RowlandY, Filter, LOn, XOn, TTDelay, TTSteps, FPlots)

XESDiff = [x-XESOff_Norm for x in XESOn_Norm]

TCenters = []
for ii in range(len(TTSteps)-1):
    TCenters = TCenters + [(TTSteps[ii]+TTSteps[ii])/2]

t0 = find_t0_XES(TCenters, XESDiff, FPlots)






TTDelay = [x - t0 for x in TTDelay]

TTSteps = np.linspace(-150, 800, NumTTStepsPlots+1)

XESOn_Norm, XESOff_Norm, Num_On, Num_Off, NormFactor_Off, NormFactor_On = makeXES(NumTTStepsPlots, Ipm2Sum, RowlandY, Filter, LOn, XOn, TTDelay, TTSteps, FPlots)

XESDiff = [x-XESOff_Norm for x in XESOn_Norm]

TCenters = []
for ii in range(len(TTSteps)-1):
    TCenters = TCenters + [(TTSteps[ii]+TTSteps[ii])/2]


plt.figure()
plt.plot(TCenters, XESDiff, marker = 'o')