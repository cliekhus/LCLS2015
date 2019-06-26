# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 18:12:34 2019

@author: chelsea
"""

import numpy as np
import matplotlib.pyplot as plt
from itertools import compress
from loadData import loadData

if False:

    FileNums = [180]+ list(range(182,188+1))
    #FileNums = [182]
    #FileNums = [156,157,158,160,161,162,163,164]
    XOn, LOn, StageDelay, Diode2, Ipm2Sum, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ScanNum, RowlandY, RowOffset = loadData(FileNums, False)

TTDelay = [(x*1e-12 + y)*1e15 for x,y in zip(TimeTool,StageDelay)]

NumTTSteps = 100

TTSteps = np.linspace(-2000,0,NumTTSteps+1)

Ideal = [(w-v)/x for v,w,x,y,z in zip(RowOffset, RowlandY, Diode2, LOn, XOn) if y and z and x>0]
Times = [x for w,x,y,z in zip(Diode2, TTDelay, LOn, XOn) if y and z and w>0]

Idealp = []

for ii in range(NumTTSteps):
    filt = [x>=TTSteps[ii] and x < TTSteps[ii+1] for x in Times]
    Idealp = Idealp + [sum(list(compress(Ideal, filt)))/sum([int(x) for x in filt])]

plt.figure(), plt.scatter(Times, Ideal)
plt.figure(), plt.scatter(TTSteps[1:], Idealp)


plt.figure(), plt.scatter([x for x,y,z in zip(TTDelay,XOn, LOn) if y and z], [(x-z)/y for x,y,z,a,b in zip(RowlandY, Diode2, RowOffset, XOn, LOn) if a and b], alpha=.1)
