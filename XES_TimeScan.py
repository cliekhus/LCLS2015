# -*- coding: utf-8 -*-
"""
Created on Mon May 20 10:34:43 2019

@author: chelsea
"""

import numpy as np
import matplotlib.pyplot as plt
from makeFilter import makeFilter
from find_t0 import find_t0_XES
from loadData import loadData
from makeXES import makeXES
from fitXES import fitXES

ReEnterData = False
FPlots = False

NumTTSteps = 200
NumTTStepsPlots = 50

if ReEnterData:

    FileNums = [180]+ list(range(182,188+1))
    #FileNums = list(range(155, 158+1)) + list(range(160, 164+1))
    XOn, LOn, StageDelay, Diode2, Ipm2Sum, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ScanNum, RowlandY, RowOffset = loadData(FileNums, False)

RowlandWOffset = [x-y for x,y in zip(RowlandY, RowOffset)]

Filter, IpmOffset = makeFilter(Diode2, Ipm2Sum, RowlandWOffset, XOn, LOn, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, FPlots, ScanNum, 2)

IpmWOffset = [x-IpmOffset for x in Diode2]

TTDelay = [(x*1e-12 + y)*1e15 for x,y in zip(TimeTool,StageDelay)]

TTSteps = np.linspace(-2000,0,NumTTSteps+1)

XESOn_Norm, XESOff_Norm, Num_On, Num_Off, NormFactor_Off, NormFactor_On = makeXES(NumTTSteps, IpmWOffset, RowlandWOffset, Filter, LOn, XOn, TTDelay, TTSteps, FPlots)

XESDiff = [x-XESOff_Norm for x in XESOn_Norm]

TCenters = []
for ii in range(len(TTSteps)-1):
    TCenters = TCenters + [(TTSteps[ii]+TTSteps[ii+1])/2]
    

t0 = find_t0_XES(TCenters, XESDiff, FPlots)






TTDelayp = [x - t0 for x in TTDelay]

TTSteps = np.linspace(-150, 800, NumTTStepsPlots+1)

XESOn_Norm, XESOff_Norm, Num_On, Num_Off, NormFactor_Off, NormFactor_On = makeXES(NumTTStepsPlots, IpmWOffset, RowlandWOffset, Filter, LOn, XOn, TTDelayp, TTSteps, FPlots)

XESDiff = [(x-XESOff_Norm)*1000/XESOff_Norm for x in XESOn_Norm]

TCenters = []
for ii in range(len(TTSteps)-1):
    TCenters = TCenters + [(TTSteps[ii]+TTSteps[ii])/2]


Fit1, Fit2, params, info = fitXES(TCenters, XESDiff, 1, FPlots)

plt.figure()
plt.plot(TCenters, XESDiff, 'o')
plt.plot(TCenters, Fit1)
plt.title('time resolved XES')
plt.ylabel('$\Delta$ T x 10$^3$')
plt.xlabel('time delay (fs)')


plt.figure()
plt.plot(TCenters, [x-y for x,y in zip(XESDiff,Fit)], 'o')