# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:03:44 2019

@author: chelsea
"""

import numpy as np
import matplotlib.pyplot as plt
from loadData import loadData
from APSXESCalibration import makeConversion
from makeStaticXES import makeStaticXES

ReEnterData = False
FPlots = False

#Set up the scans and the number of time steps


if ReEnterData:

    FileNums = list(range(190,190+1))
    XOn, LOn, Angle, Diode2, Ipm2Sum, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ScanNum, RowlandY, RowOffset = loadData(FileNums, False, 2)

RowlandWOffset = [x-y for x,y in zip(RowlandY, RowOffset)]
#RowlandWOffset = RowlandY
UniqueAngle = np.unique(Angle)


Times = np.linspace(-0.2, 0.1, num=10)
plt.figure()

for ii in range(len(Times)):
    
    MaxTime = Times[ii]+0.1
    MinTime = Times[ii]
    
    SpectraOn, SpectraOff, UniqueAnglep = makeStaticXES(Angle, UniqueAngle, RowlandWOffset, Diode2, Ipm2Sum, XOn, LOn, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ScanNum, MaxTime, MinTime, FPlots)
            
    UniqueAnglep = [76*2-x for x in UniqueAnglep]
    LCLSEnergy, slope, x0 = makeConversion(UniqueAnglep, SpectraOff, FPlots)
            
    
    #plt.plot(LCLSEnergy, SpectraOn, marker = 'o')
    #plt.plot(LCLSEnergy, SpectraOff, marker = 'o')
    
    #SpectraOnNorm = [x/max(SpectraOn) for x in SpectraOn]
    #SpectraOffNorm = [x/max(SpectraOff) for x in SpectraOff]
    
    diff = [(x-y)/y for x,y in zip(SpectraOn, SpectraOff)]
    
    if ii == 0:
        
        Matrix = [diff]
    
    else:
        Matrix.append(diff)
    
    plt.plot(LCLSEnergy, diff, marker = 'o')

#plt.figure()
#plt.plot(LCLSEnergy, [x-y for x,y in zip(SpectraOnNorm, SpectraOffNorm)], marker = 'o')

plt.figure()
plt.pcolor(Matrix)




















