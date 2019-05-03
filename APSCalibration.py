# -*- coding: utf-8 -*-
"""
Created on Thu May  2 15:24:58 2019

@author: chelsea
"""

import h5py
import numpy as np
import matplotlib.pyplot as plt
import math
from itertools import compress
from makeIntensityFilter import makeDiodeFilter
import statistics as stat

fileNums = list(range(373,395+1))

XOn = []
LOn = []
XEnergyRaw = []
Diode2 = []

Ipm2Sum = []
Ipm2Median = []
Ipm2STD = []
DiodeIpmSlope = []
DISMedian = []
DISSTD = []

for fileNum in fileNums:
    
    ScanName = h5py.File('Data\ldat_xppj6715_Run' + str(fileNum) + '.h5')
    
    xOn = list(map(bool, ScanName['/lightStatus/xray']))
    XOn = XOn + xOn
    LOn = LOn + list(map(bool, ScanName['/lightStatus/laser']))
    XEnergyRaw = XEnergyRaw + [round(x,4) for x in list(ScanName['/scan/var0'])]
    diode = [x[2] for x in list(ScanName['/diodeU/channels'])]                  #Quad cell 2 from diode - this one has an output
    Diode2 = Diode2 + diode
    ipm2 = [float(x[1])+float(x[3]) for x in list(ScanName['/ipm2/channels'])]  #Intensity (and position) monitor #2.  Quad cells 1 and 3 had signal - use these
    Ipm2Sum = Ipm2Sum + ipm2
    
    ipm2 = [float(x[1])+float(x[3]) for x in list(ScanName['/ipm2/channels'])]  #Intensity (and position) monitor #2.  Quad cells 1 and 3 had signal - use these
    Ipm2Sum = Ipm2Sum + ipm2
    statmedian = stat.median(compress(ipm2, xOn))
    Ipm2Median = Ipm2Median + [float(statmedian) for x in range(len(ipm2))]
    statstdev = stat.stdev(compress(ipm2, xOn))
    Ipm2STD = Ipm2STD + [float(statstdev) for x in range(len(ipm2))]
    
    slope = [y/x for y,x in zip(diode, ipm2)]
    DiodeIpmSlope = DiodeIpmSlope + slope
    statmedian = stat.median([x for x in slope if not math.isnan(x)])
    DISMedian = [float(statmedian) for x in range(len(ipm2))]
    statstdev = stat.stdev([i-statmedian*d for d,i in zip(diode, ipm2)])
    DISSTD = DISSTD + [float(statstdev) for x in range(len(ipm2))]

APSName = h5py.File('Data/APS/APS_Aug_2015_Fesamples.mat')

FeRuRIXS = np.array(APSName['/FeRu_RIXS'])

incident_axis = np.array(APSName['/Fe_RIXS_incident_axis'])
emitted_axis = np.array(APSName['/Fe_RIXS_emitted_axis'])
xp,yp = np.meshgrid(emitted_axis,incident_axis)

UniXEnergy = np.unique(XEnergyRaw)

XASOff = [0 for x in range(len(UniXEnergy))]

Off_NumScan = [0 for x in range(len(UniXEnergy))]

NormFactor_Off = [0 for x in range(len(UniXEnergy))]

NanCheck = [not a and not b for a,b in zip([math.isnan(x) for x in Diode2], [math.isnan(x) for x in Ipm2Sum])]
IpmNumSTDs = 6
IpmFilter = list(a < b+IpmNumSTDs*c and a > b-IpmNumSTDs*c for a,b,c in zip(Ipm2Sum, Ipm2Median, Ipm2STD))

DiodeFilter = makeDiodeFilter(Ipm2Sum, Diode2, XOn, LOn, DiodeIpmSlope, DISMedian, DISSTD)

IntensityFilter = [a and b for a,b in zip(IpmFilter, DiodeFilter)]

for jj in range(len(UniXEnergy)):
    
    SelectedRuns = list(a and b and c and d and e for a,b,c,d,e in zip(XOn, (XEnergyRaw == UniXEnergy[jj]), NanCheck, IntensityFilter))
    
    off = list(not a and b for a,b in zip(LOn, SelectedRuns))
    XASOff[jj] = sum(list(compress(Diode2, off)))
    
    Off_NumScan[jj] = sum([int(x) for x in off])
    NormFactor_Off[jj] = sum(list(compress(Ipm2Sum, off)))

plt.figure()
plt.pcolor(xp, yp, FeRuRIXS)


plt.figure()
plt.plot(emitted_axis[0], np.sum(FeRuRIXS, axis=0), marker='.')

plt.xlabel('emitted energy (keV)')
plt.ylabel('emittance')

APSXASNorm = np.sum(FeRuRIXS, axis = 1)

plt.figure()
plt.plot(incident_axis, np.sum(FeRuRIXS, axis=1), marker='.')
plt.plot(UniXEnergy, [x/y for x,y in zip(XASOff, NormFactor_Off)])

plt.xlabel('x-ray energy (keV)')
plt.ylabel('x-ray absorption')

def 