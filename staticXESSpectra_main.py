# -*- coding: utf-8 -*-
"""
Created on Fri Jun  7 11:03:44 2019

@author: chelsea
"""

import numpy as np
import matplotlib.pyplot as plt
from loadData import loadData
from makeStaticXES import makeStaticXES
from scipy.signal import savgol_filter
from APSXESCalibration import makeConversion
import os
import pickle


ReEnterData = False
FPlots = False

#Set up the scans and the number of time steps


if ReEnterData:

    FileNums = list(range(190,190+1))
    XOn, LOn, Angle, Diode2, Ipm2Sum, DiodeIpmSlope, TimeTool, TTAmp, TTFWHM, ScanNum, RowlandY, RowOffset = loadData(FileNums, False, 2)

folder = "D://LCLS_Data/LCLS_python_data/XES_conversion_info/"
exists = os.path.isfile(folder+'t0.pkl')

if exists:
    with open(folder + "t0.pkl", "rb") as f:
        t0 = pickle.load(f)
    TDelay = [(x*1e-12 - 1.4e-12)*1e15 - t0 for x in TimeTool]
    Times = np.linspace(-0.2, 0.15, num=11)
    print('read')
else:
    TDelay = TimeTool
    Times = np.linspace(-0.2, 0.15, num=11)


RowlandWOffset = [x-y for x,y in zip(RowlandY, RowOffset)]
UniqueAngle = np.unique(Angle)


plt.figure()

for ii in range(len(Times)-1):
    
    MaxTime = Times[ii+1]
    MinTime = Times[ii]
    
    SpectraOn, SpectraOff, UniqueAnglep = makeStaticXES(Angle, UniqueAngle, RowlandWOffset, Diode2, Ipm2Sum, XOn, LOn, DiodeIpmSlope, TDelay, TTAmp, TTFWHM, ScanNum, MaxTime, MinTime, FPlots)
            
    LCLSEnergy, slope, x0 = makeConversion(UniqueAnglep, SpectraOff, False)
            
    
    #plt.plot(LCLSEnergy, SpectraOn, marker = 'o')
    #plt.plot(LCLSEnergy, SpectraOff, marker = 'o')
    
    #SpectraOnNorm = [x/max(SpectraOn) for x in SpectraOn]
    #SpectraOffNorm = [x/max(SpectraOff) for x in SpectraOff]
    SpectraOffSmooth = savgol_filter(SpectraOff, 5, 2)
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




















