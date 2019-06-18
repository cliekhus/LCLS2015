# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 16:45:18 2019

@author: chelsea
"""

#XOn, LOn, Angle, Diode2, Ipm2Sum, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ScanNum, RowlandY, RowOffset

import random
import math
import numpy as np
import numpy.matlib
import matplotlib.pyplot as plt
from makeXES import makeXES
from itertools import compress
from fittingfunctions import lorwoffset
import statistics as stat

numAngle = 31
multiplier = 100
num = numAngle*multiplier

TimeTool = [-random.randint(-700,700)/1000 for x in range(num)]

Angle = np.linspace(75.638,75.238,numAngle)
Angle = [round(x,3) for x in Angle]
Angle = np.matlib.repmat(Angle,1,multiplier)
Angle = Angle[0]

#LOn = [False for x in range(num)]
LOn = [bool(random.randint(0,1)) for x in range(num)]

XOn = [True for x in range(num)]
#XOn = [bool(random.randint(0,1)) for x in range(num)]

Diode2 = [random.randint(900,1000)/1000 for x in range(num)]
#Diode2 = [int(x)+.5 for x in LOn]

#Diode2 = [w for w,x,y in zip(TimeTool, XOn, LOn)]

rowland = lorwoffset(Angle, 0.07, 75.438, 300000,0,0)



#RowlandY = [w*int(y)*(x+v*int(z)) for v,w,x,y,z in zip(TimeTool, Diode2, rowland, XOn, LOn)]
RowlandY = [w*int(y)*(x+int(z)) for v,w,x,y,z in zip(TimeTool, Diode2, rowland, XOn, LOn)]

RowOffset = [0 for x in range(len(RowlandY))]

Filter = [True for x in range(num)]

Ipm2Sum = Diode2

DiodeIpmSlope = [1 for x in range(len(Diode2))]

TTAmp = [random.randint(900,1000)/1000 for x in range(num)]

TTFWHM = [random.randint(900,1000)/1000 for x in range(num)]

ScanNum = [1 for x in range(len(Diode2))]

FPlots = True

plt.figure(), plt.scatter(TimeTool, RowlandY)

plt.figure(), plt.scatter(Angle, RowlandY)

UniqueAngle = np.unique(Angle)

IdealOn = []
IdealOff = []
UniqueAnglep = []
MeanTime = []

minTime = 0
maxTime = .1

for angle in UniqueAngle:
    
    rowlandon = sum([w for w,y,z,v,u in zip(RowlandY, XOn, LOn, Angle, TimeTool) if y and z and v == angle and u < maxTime and u > minTime])
    diodeon = sum([w for w,y,z,v,u in zip(Diode2, XOn, LOn, Angle, TimeTool) if y and z and v == angle and u < maxTime and u > minTime])
    rowlandoff = sum([w for w,y,z,v,u in zip(RowlandY, XOn, LOn, Angle, TimeTool) if y and not z and v == angle and u < maxTime and u > minTime])
    diodeoff = sum([w for w,y,z,v,u in zip(Diode2, XOn, LOn, Angle, TimeTool) if y and not z and v == angle and u < maxTime and u > minTime])
    
    
    if rowlandon > 0 and rowlandoff > 0:
               
        IdealOn = IdealOn + [rowlandon/diodeon]
        IdealOff = IdealOff + [rowlandoff/diodeoff]
        UniqueAnglep = UniqueAnglep + [angle]
        time = stat.mean([u for y,z,v,u in zip(XOn, LOn, Angle, TimeTool) if y and not z and v == angle and u < maxTime and u > minTime])
        MeanTime = MeanTime + [time]

Diff = [x-y for x,y in zip(IdealOn, IdealOff)]

plt.figure()
plt.plot(UniqueAnglep, Diff)

#plt.figure()
#plt.plot(UniqueAnglep, MeanTime)

#plt.figure()
#plt.plot(UniqueAnglep, [x/y for x,y in zip(Diff, MeanTime)])

"""
Ideal = [w/x for w,x,y,z in zip(RowlandY, Diode2, LOn, XOn) if y and z and x>0]
Times = [x for w,x,y,z in zip(Diode2, TimeTool, LOn, XOn) if y and z and w>0]

Idealp = []

for ii in range(NumTTSteps):
    filt = [x>=TTSteps[ii] and x < TTSteps[ii+1] for x in Times]
    Idealp = Idealp + [sum(list(compress(Ideal, filt)))/sum([int(x) for x in filt])]

plt.figure(), plt.scatter(Times, Ideal)
plt.figure(), plt.scatter(TTSteps[1:], Idealp)



XESOn_Norm, XESOff_Norm, Num_On, Num_Off, NormFactor_Off, NormFactor_On = makeXES(NumTTSteps, Diode2, RowlandY, Filter, LOn, XOn, TTDelay, TTSteps, FPlots)
"""