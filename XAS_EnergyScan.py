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
import math
import statistics as stat
from makeIntensityFilter import makeDiodeFilter

ReEnterData = True

#Set up the scans and the number of time steps

NumTTSteps = 4
NumTTStepsPlots = NumTTSteps

if ReEnterData:

    FileNums = list(range(371,371+1))
    
    #Initialize the necessary lists
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
    
    TimeTool = []
    TTMedian = []
    TTSTD = []
    TTAmp = []
    TTAmpMedian = []
    TTAmpSTD = []
    TTFWHM = []
    TTFWHMMedian = []
    TTFWHMSTD = []
    
    ScanNum = []
    

    #Fill the lists with data from the h5 file
    for filenum in FileNums:
        
        ScanName = h5py.File('Data\ldat_xppj6715_Run' + str(filenum) + '.h5')
        
        xOn = list(map(bool, ScanName['/lightStatus/xray']))
        XOn = XOn + xOn
        LOn = LOn + list(map(bool, ScanName['/lightStatus/laser']))
        XEnergyRaw = XEnergyRaw + list(ScanName['/scan/var0'])

        diode = [x[2] for x in list(ScanName['/diodeU/channels'])]                  #Quad cell 2 from diode - this one has an output
        Diode2 = Diode2 + diode
        
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
        
        timetool = [float(x) for x in list(ScanName['/ttCorr/tt'])]
        TimeTool = TimeTool + timetool
        
        statmedian = stat.median(compress(timetool, [a and b for a,b in zip(LOn, XOn)]))
        TTMedian = TTMedian + [float(statmedian) for x in range(len(timetool))]
        statstdev = stat.stdev(compress(timetool, [a and b for a,b in zip(LOn, XOn)]))
        TTSTD = TTSTD + [float(statstdev) for x in range(len(timetool))]
        
        timetoolamp = [float(x) for x in list(ScanName['/tt/XPP_TIMETOOL_AMPL'])]
        TTAmp = TTAmp + timetoolamp
        
        statmedian = stat.median(compress(timetoolamp, [a and b for a,b in zip(LOn, XOn)]))
        TTAmpMedian = TTAmpMedian + [float(statmedian) for x in range(len(timetoolamp))]
        statstdev = stat.stdev(compress(timetoolamp, [a and b for a,b in zip(LOn, XOn)]))
        TTAmpSTD = TTAmpSTD + [float(statstdev) for x in range(len(timetoolamp))]
        
        timetoolfwhm = [float(x) for x in list(ScanName['/tt/XPP_TIMETOOL_AMPL'])]
        TTFWHM = TTFWHM + timetoolfwhm
        
        statmedian = stat.median(compress(timetoolfwhm, [a and b for a,b in zip(LOn, XOn)]))
        TTFWHMMedian = TTFWHMMedian + [float(statmedian) for x in range(len(timetoolfwhm))]
        statstdev = stat.stdev(compress(timetoolfwhm, [a and b for a,b in zip(LOn, XOn)]))
        TTFWHMSTD = TTFWHMSTD + [float(statstdev) for x in range(len(timetoolfwhm))]
        
        ScanNum = ScanNum + [filenum for x in range(len(diode))]


#Set up the intensity filter - the diode and cspad sum should respond linearly with the x-ray intensity
IpmNumSTDs = 6
IpmFilter = list(a < b+IpmNumSTDs*c and a > b-IpmNumSTDs*c for a,b,c in zip(Ipm2Sum, Ipm2Median, Ipm2STD))

DiodeFilter = makeDiodeFilter(Ipm2Sum, Diode2, XOn, LOn, DiodeIpmSlope, DISMedian, DISSTD)

IntensityFilter = [a and b for a,b in zip(IpmFilter, DiodeFilter)]


#Convert the timetool signal into femtosecond delays and create the time tool filters
TTSTDs = 3
TTValueFilter = list(a < b+TTSTDs*c and a > b-TTSTDs*c for a,b,c in zip(TimeTool, TTMedian, TTSTD))

TTAmpSTDs = 3
TTAmpFilter = list(a < b+TTAmpSTDs*c and a > b-TTAmpSTDs*c for a,b,c in zip(TTAmp, TTAmpMedian, TTAmpSTD))

TTFWHMSTDs = 3
TTFWHMFilter = list(a < b+TTFWHMSTDs*c and a > b-TTFWHMSTDs*c for a,b,c in zip(TTFWHM, TTFWHMMedian, TTFWHMSTD))

TTFilter = list((a and b and c) or not d or not e for a,b,c,d,e in zip(TTValueFilter, TTAmpFilter, TTFWHMFilter, XOn, LOn))

TTDelay = [x*1000 for x in TimeTool]
TTSteps = np.array([float(-220), float(-160), float(-100), float(-40), float(20)])
#TTSteps = np.linspace(min(TTDelay),max(TTDelay),NumTTSteps+1)

fig=plt.figure()
fig.add_subplot(121)
plt.hist(list(compress(TTDelay, [a and b for a,b in zip(XOn, LOn)])), 1000)
plt.title('time tool before filters')
fig.add_subplot(122)
plt.hist(list(compress(TTDelay, [a and b and c for a,b,c in zip(TTFilter, XOn, LOn)])), 1000)
plt.title('time tool after filters')


#Make XAS spectra
XEnergy = [round(x,4)*1000+.75 for x in XEnergyRaw]
UniXEnergy = np.unique(XEnergy)

XASOn = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]
XASOff = [0 for x in range(len(UniXEnergy))]

On_NumScan = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]
Off_NumScan = [0 for x in range(len(UniXEnergy))]

NormFactor_On = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]
NormFactor_Off = [0 for x in range(len(UniXEnergy))]

NanCheck = [not a and not b for a,b in zip([math.isnan(x) for x in Diode2], [math.isnan(x) for x in Ipm2Sum])]

for jj in range(len(UniXEnergy)):
    
    SelectedRuns = list(a and b and c and d and e for a,b,c,d,e in zip(XOn, (XEnergy == UniXEnergy[jj]), NanCheck, IntensityFilter, TTFilter))
    
    off = list(not a and b for a,b in zip(LOn, SelectedRuns))
    XASOff[jj] = sum(list(compress(Diode2, off)))
    
    Off_NumScan[jj] = sum([int(x) for x in off])
    NormFactor_Off[jj] = sum(list(compress(Ipm2Sum, off)))
    
    for ii in range(len(TTSteps)-1):
        
        on = list(a and b and c and d for a,b,c,d in zip(LOn, SelectedRuns, (TTDelay >= TTSteps[ii]), (TTDelay < TTSteps[ii+1])))
        XASOn[ii][jj] = sum(list(compress(Diode2, on)))
        
        On_NumScan[ii][jj] = sum([int(x) for x in on])
        NormFactor_On[ii][jj] = sum(list(compress(Ipm2Sum, on)))

fig = plt.figure()

XASOn_Norm = [[0 for x in range(len(UniXEnergy))] for y in range(len(TTSteps)-1)]

AtleastOne = [x > 0 for x in Off_NumScan]

for ii in range(NumTTStepsPlots):
    AtleastOne = [a and b > 0 for a,b in zip(AtleastOne, On_NumScan[ii])]

LegendLabel = []

for ii in range(NumTTStepsPlots):

    XASOn_Norm[ii] = [a/b for a,b,c in zip(XASOn[ii], NormFactor_On[ii], AtleastOne) if c]
    LegendLabel = LegendLabel + plt.plot(list(compress(UniXEnergy, AtleastOne)), XASOn_Norm[ii])
    
plt.xlabel('x-ray energy (keV)')
plt.ylabel('x-ray absorption')

XASOff_Norm = [a/b for a,b,c in zip(XASOff, NormFactor_Off, AtleastOne) if c]

LegendLabel = LegendLabel + plt.plot(list(compress(UniXEnergy, AtleastOne)), XASOff_Norm)
plt.xlabel('x-ray energy (keV)')
plt.ylabel('x-ray absorption')

LegendWords = []
for ii in range(NumTTStepsPlots):
    LegendWords = LegendWords + [str(round(TTSteps[ii],0)) + ' to ' + str(round(TTSteps[ii+1],0)) + ' fs delay']

LegendWords = LegendWords + ['Off']

plt.legend(LegendLabel, LegendWords)

LegendLabel = []
plt.figure()
for ii in range(NumTTStepsPlots):
    
    LegendLabel = LegendLabel + plt.plot(list(compress(UniXEnergy, [x > 0 and y > 0 for x,y in zip(On_NumScan[ii], AtleastOne)])), [a - b for a,b in zip(XASOn_Norm[ii], XASOff_Norm)])
    #plt.plot(UniXEnergy, [a/sum(XESOn[ii]) - b/sum(XESOff) for a,b, in zip(XESOn[ii], XESOff)])
    
plt.xlabel('x-ray energy (keV)')
plt.ylabel('difference in x-ray absorption (on-off)')

LegendWords.pop()

plt.legend(LegendLabel, LegendWords)