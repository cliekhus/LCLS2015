# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:48:43 2019

@author: chelsea
"""
"""
XES energy scan - k beta

"""
import h5py
import numpy as np
import matplotlib.pyplot as plt
from itertools import compress
from matplotlib.widgets import Cursor
import math
import statistics as stat

#Set up the scans and the number of time steps
FileNums = list(range(371,371+1))

NumTTSteps_ES = 1
NumTTStepsPlots_ES = NumTTSteps_ES


#Initialize the necessary lists
XOn = []
LOn = []
XEnergy = []
TimeTool = []
Diode2 = []

Ipm2Sum = []
Ipm2Median = []
Ipm2STD = []
DiodeIpmSlope = []
DISMedian = []
DISSTD = []

CspadSum = []
CspadMedian = []
CspadSTD = []
DiodeCspadSlope = []
DCSMedian = []
DCSSTD = []

ScanNum = []


#Fill the lists with data from the h5 file
for filenum in FileNums:
    
    ScanName = h5py.File('Data\ldat_xppj6715_Run' + str(filenum) + '.h5')
    
    xOn = list(map(bool, ScanName['/lightStatus/xray']))
    XOn = XOn + xOn
    LOn = LOn + list(map(bool, ScanName['/lightStatus/laser']))
    XEnergy = XEnergy + [round(2*x,3)/2 for x in list(ScanName['/scan/var0'])]
    TimeTool = TimeTool + list(ScanName['/ttCorr/tt'])
    diode = [x[2] for x in list(ScanName['/diodeU/channels'])]                  #Quad cell 2 from diode - this one has an output
    Diode2 = Diode2 + diode
   
    ipm2 = [float(x[1])+float(x[3]) for x in list(ScanName['/ipm2/channels'])]  #Intensity (and position) monitor #2.  Quad cells 1 and 3 had signal - use these
    Ipm2Sum = Ipm2Sum + ipm2
    statmedium = stat.median(compress(ipm2, xOn))
    Ipm2Median = Ipm2Median + [float(statmedium) for x in range(len(ipm2))]
    statstdev = stat.stdev(compress(ipm2, xOn))
    Ipm2STD = Ipm2STD + [float(statstdev) for x in range(len(ipm2))]
    
    slope = [y/x for x,y in zip(diode, ipm2)]
    DiodeIpmSlope = DiodeIpmSlope + slope
    statmedium = stat.median([x for x in slope if not math.isnan(x)])
    DISMedian = [float(statmedium) for x in range(len(ipm2))]
    statstdev = stat.stdev([i-statmedium*d for d,i in zip(diode, ipm2)])
    DISSTD = DISSTD + [float(statstdev) for x in range(len(ipm2))]
    
    Cspad = []
    for cspad in list(ScanName['/cspad/azav']):
        Cspad.append(float(sum([x for x in cspad if not math.isnan(x)])))
        
    CspadSum = CspadSum + Cspad
    statmedium = stat.median(Cspad)
    CspadMedian = CspadMedian + [float(statmedium) for x in range(len(Cspad))]
    statstdev = stat.stdev(Cspad)
    CspadSTD = CspadSTD + [float(statstdev) for x in range(len(Cspad))]
    
    slope = [y/x for x,y in zip(diode, Cspad)]
    DiodeCspadSlope = DiodeCspadSlope + slope
    statmedium = stat.median(slope)
    DCSMedian = [float(statmedium) for x in range(len(diode))]
    statstdev = stat.stdev([c-statmedium*d for d,c in zip(diode, Cspad)])
    DCSSTD = DISSTD + [float(statstdev) for x in range(len(diode))]
    
    ScanNum = ScanNum + [filenum for x in range(len(diode))]


#Convert the timetool signal into femtosecond delays and create the time slices
TTDelay_ES = [x*1000 for x in TimeTool]
TTSteps = np.linspace(min(TTDelay_ES),max(TTDelay_ES),NumTTSteps_ES+1)


#Set up the intensity filter - the diode and cspad sum should respond linearly with the x-ray intensity

IpmNumSTDs = 1
IpmFilter = list(a < b+IpmNumSTDs*c and a > b-IpmNumSTDs*c for a,b,c in zip(Ipm2Sum, Ipm2Median, Ipm2STD))

DISSTDs = 1
DISFilter = list(a < b*c+DISSTDs*d and a > b*c-DISSTDs*d for a,b,c,d in zip(Ipm2Sum, Diode2, DISMedian, DISSTD))

CspadSTDs = 1
CspadFilter = list(a < b+CspadSTD*c and a > b+CspadSTD*c for a,b,c in zip(CspadSum, CspadMedian, CspadSTD))

DCSSTDs = 1
DCSFilter = list(a < b*c+DCSSTDs*d and a > b*c-DCSSTDs*d for a,b,c,d in zip(CspadSum, Diode2, DCSMedian, DCSSTD))

IntensityFilter = list(a and b and c and d for a,b,c,d in zip(IpmFilter, DISFilter, CspadFilter, DCSFilter))

UniXEnergy = np.unique(XEnergy)

XASOn = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]
XASOff = [0 for x in range(len(UniXEnergy))]

On_NumScan = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]
Off_NumScan = [0 for x in range(len(UniXEnergy))]

for jj in range(len(UniXEnergy)):
    
    SelectedRuns = list(a and b and not c for a,b,c in zip(XOn, (XEnergy == UniXEnergy[jj]), [math.isnan(x) for x in Diode2]))
    
    Off = list(not a and b for a,b in zip(LOn, SelectedRuns))
    XASOff[jj] = sum(list(compress(Diode2, Off)))
    
    Off_NumScan[jj] = sum([int(x) for x in Off])
    
    for ii in range(len(TTSteps)-1):
        
        On = list(a and b and c and d for a,b,c,d in zip(LOn, SelectedRuns, (TTDelay_ES >= TTSteps[ii]), (TTDelay_ES < TTSteps[ii+1])))
        XASOn[ii][jj] = sum(list(compress(Diode2, On)))
        
        On_NumScan[ii][jj] = sum([int(x) for x in On])

fig = plt.figure()
ax = fig.add_subplot(111)

XASOn_Norm = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]

for ii in range(NumTTStepsPlots_ES):

    XASOn_Norm[ii] = [a/b for a,b in zip(XASOn[ii], On_NumScan[ii])]
    plt.plot(UniXEnergy, XASOn_Norm[ii])
    
plt.xlabel('x-ray energy (keV)')
plt.ylabel('x-ray absorption')
plt.title('Laser On')
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

XASOff_Norm = [a/b for a,b in zip(XASOff, Off_NumScan)]

plt.figure()
ax = fig.add_subplot(111)
plt.plot(UniXEnergy, XASOff_Norm)
plt.xlabel('x-ray energy (keV)')
plt.ylabel('x-ray absorption')
plt.title('Laser Off')
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

plt.figure()
ax = fig.add_subplot(111)

for ii in range(NumTTStepsPlots_ES):
    
    plt.plot(UniXEnergy, [a - b for a,b, in zip(XASOn_Norm[ii], XASOff_Norm)])
    #plt.plot(UniXEnergy, [a/sum(XESOn[ii]) - b/sum(XESOff) for a,b, in zip(XESOn[ii], XESOff)])
    
plt.xlabel('x-ray energy (keV)')
plt.ylabel('difference in x-ray absorption (on-off)')
plt.title('raw data')
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

plt.figure()
ax = fig.add_subplot(111)

for ii in range(NumTTStepsPlots_ES):
    
    plt.plot(UniXEnergy, [a/sum(XASOn_Norm[ii]) - b/sum(XASOff_Norm) for a,b, in zip(XASOn_Norm[ii], XASOff_Norm)])
    #plt.plot(UniXEnergy, [a/sum(XESOn[ii]) - b/sum(XESOff) for a,b, in zip(XESOn[ii], XESOff)])
    
plt.xlabel('x-ray energy (keV)')
plt.ylabel('difference in x-ray absorption (on-off), extra norm')
plt.title('raw data')
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

